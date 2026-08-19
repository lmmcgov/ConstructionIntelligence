"""
FastAPI backend for GeoJSON evidence-discovery uploads.

Accepts a GeoJSON FeatureCollection of construction objects,
maps each feature to a Project, and runs the existing web
evidence discovery pipeline (RSS/sitemap feeds + tiered search +
ranking + scoring + extraction) against each one in the
background. The static frontend polls /jobs/{job_id} for live
per-project progress rather than blocking on one long request.

Run locally with:

    uv run uvicorn construction_intelligence.web_ui.app:app --reload

Requires a local SearXNG instance for the tiered-search fallback
(see README.md) -- feed-based discovery works without it, but
projects in countries with no registered feed will find nothing
if SearXNG isn't running.

SECURITY: this server has no authentication and is meant for
local, single-user use only. It binds to 127.0.0.1 by default
(uvicorn's own default) -- do not run it with --host 0.0.0.0, or
otherwise expose this port, on a network with untrusted peers.
Anyone who can reach the port can upload files and read all job
results.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from construction_intelligence.core.project import Project
from construction_intelligence.ingestion.web.evidence_discovery_service import (
    EvidenceDiscoveryService,
)
from construction_intelligence.ingestion.web.fallback_extractor import (
    FallbackExtractor,
)
from construction_intelligence.ingestion.web.feed_registry_defaults import (
    build_default_feed_registry,
)
from construction_intelligence.ingestion.web.gemini_extractor import (
    GeminiExtractor,
)
from construction_intelligence.ingestion.web.html_extractor import (
    HTMLExtractor,
)
from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)
from construction_intelligence.ingestion.web.web_evidence_ingestion_service import (
    WebEvidenceIngestionService,
)
from construction_intelligence.integrations.gemini_cli.mock_runner import (
    MockGeminiRunner,
)
from construction_intelligence.mappers.geojson_project_mapper import (
    GeoJSONProjectMapper,
)
from construction_intelligence.web_ui.job_store import (
    JobStore,
    ProjectJobStatus,
)


#
# Rejects an upload before it's fully read into memory rather
# than trusting a client-supplied Content-Length header (which
# can lie) -- enforced by reading in bounded chunks.
#
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

#
# A feature triggers a full discovery run (feeds + tiered search
# + ranking + scoring + extraction) -- bounding this keeps one
# upload from queuing an unbounded amount of background work.
#
MAX_FEATURES_PER_UPLOAD = 200

#
# Bounded so concurrent SearXNG/feed requests stay reasonable on
# a local dev instance -- this is background worker concurrency,
# not a web server thread count.
#
MAX_CONCURRENT_PROJECTS = 4

STATIC_DIR = Path(__file__).parent / "static"


app = FastAPI(
    title="Construction Intelligence -- GeoJSON Evidence Discovery"
)

job_store = JobStore()

executor = ThreadPoolExecutor(
    max_workers=MAX_CONCURRENT_PROJECTS
)

mapper = GeoJSONProjectMapper()

#
# Built once at import time and reused across worker threads.
# EvidenceDiscoveryService and its feed/search providers don't
# mutate shared state during a run (feed dedup goes through
# diskcache, which is safe for this bounded level of concurrency),
# so there's no need to rebuild this per project.
#
ingestion_service = WebEvidenceIngestionService(
    discovery_service=EvidenceDiscoveryService(
        search_provider=SearXNGSearchProvider(),
        feed_registry=build_default_feed_registry(),
    ),
    #
    # Same extractor wiring as
    # scripts/run_project_evidence_search_and_store.py --
    # MockGeminiRunner stands in for the real Gemini CLI so this
    # doesn't require an external tool to be installed.
    #
    extractor=FallbackExtractor(
        primary=HTMLExtractor(),
        fallback=GeminiExtractor(
            runner=MockGeminiRunner()
        ),
    ),
)


@app.get("/")
def index() -> FileResponse:

    return FileResponse(STATIC_DIR / "index.html")


async def _read_upload_bounded(
    file: UploadFile,
    max_bytes: int,
) -> bytes:
    """
    Read an upload in chunks, aborting once max_bytes is
    exceeded, instead of trusting Content-Length and reading
    the whole body into memory unconditionally.
    """

    chunks: list[bytes] = []

    total = 0

    while True:

        chunk = await file.read(65536)

        if not chunk:

            break

        total += len(chunk)

        if total > max_bytes:

            raise ValueError(
                f"Upload exceeds the {max_bytes} byte limit."
            )

        chunks.append(chunk)

    return b"".join(chunks)


@app.post("/upload")
async def upload(file: UploadFile) -> JSONResponse:

    try:

        raw = await _read_upload_bounded(
            file,
            MAX_UPLOAD_BYTES,
        )

    except ValueError as error:

        return JSONResponse(
            {"error": str(error)},
            status_code=413,
        )

    #
    # json.loads on untrusted input can raise more than just
    # JSONDecodeError -- e.g. RecursionError on pathologically
    # deep nesting. Catch broadly here so malformed input gets a
    # clean 400 instead of an unhandled 500.
    #
    try:

        data = json.loads(raw)

    except Exception:

        return JSONResponse(
            {"error": "Not valid JSON."},
            status_code=400,
        )

    if not isinstance(data, dict):

        return JSONResponse(
            {"error": "Expected a GeoJSON FeatureCollection object."},
            status_code=400,
        )

    features = data.get("features")

    if not isinstance(features, list) or not features:

        return JSONResponse(
            {"error": "No GeoJSON features found."},
            status_code=400,
        )

    truncated = len(features) > MAX_FEATURES_PER_UPLOAD

    features = features[:MAX_FEATURES_PER_UPLOAD]

    #
    # Skip (rather than crash on) any feature that isn't a
    # well-formed dict -- one malformed feature shouldn't fail
    # the whole upload.
    #
    projects: list[Project] = []

    for index, feature in enumerate(features):

        if not isinstance(feature, dict):

            continue

        try:

            projects.append(
                mapper.map(feature, index)
            )

        except Exception:

            continue

    if not projects:

        return JSONResponse(
            {"error": "No valid GeoJSON features found."},
            status_code=400,
        )

    job_id = str(uuid4())

    job_store.create(
        job_id,
        [project.name for project in projects],
        truncated,
    )

    for index, project in enumerate(projects):

        if not project.country:

            job_store.update_result(
                job_id,
                index,
                warning=(
                    "No country resolved from this feature -- "
                    "feed-based discovery will find nothing for "
                    "it (no safe default country for feeds)."
                ),
            )

        executor.submit(
            _process_project,
            job_id,
            index,
            project,
        )

    return JSONResponse(
        {
            "job_id": job_id,
            "feature_count": len(projects),
            "truncated": truncated,
        }
    )


def _process_project(
    job_id: str,
    index: int,
    project: Project,
) -> None:

    job_store.update_result(
        job_id,
        index,
        status=ProjectJobStatus.RUNNING,
    )

    try:

        evidence_records = ingestion_service.ingest(
            project
        )

        job_store.update_result(
            job_id,
            index,
            status=ProjectJobStatus.DONE,
            evidence_count=len(evidence_records),
            evidence=[
                {
                    "title": record.title or "(untitled)",
                    "url": record.url,
                }
                for record in evidence_records
            ],
        )

    except Exception as error:

        job_store.update_result(
            job_id,
            index,
            status=ProjectJobStatus.ERROR,
            error=str(error),
        )


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> JSONResponse:

    job = job_store.get(job_id)

    if job is None:

        return JSONResponse(
            {"error": "Unknown job id."},
            status_code=404,
        )

    return JSONResponse(
        {
            "job_id": job.id,
            "complete": job.is_complete,
            "truncated": job.truncated,
            "results": [
                {
                    "project_name": result.project_name,
                    "status": result.status.value,
                    "evidence_count": result.evidence_count,
                    "evidence": result.evidence,
                    "warning": result.warning,
                    "error": result.error,
                }
                for result in job.results
            ],
        }
    )


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)
