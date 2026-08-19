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

Search runs through both SearXNG (local, see README.md -- must
be running separately) and Google News (hosted, needs nothing
local but resolves each result via a headless browser, so it's
slower per-query). Either can fail independently without losing
the other's results, and feed-based discovery works without
either -- projects in countries with no registered feed and both
search backends unavailable will find nothing.

AUTH: protected by Auth0 (see .env.example for one-time setup).
The server refuses to start without AUTH0_DOMAIN, AUTH0_CLIENT_ID,
AUTH0_CLIENT_SECRET, and SESSION_SECRET_KEY set. Page routes
redirect to /login when unauthenticated; the JSON API routes
(/upload, /jobs/{job_id}) return 401 instead, since a fetch()
call following a redirect to an HTML login page would otherwise
fail confusingly on the frontend.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

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
from construction_intelligence.ingestion.web.google_news_search_provider import (
    GoogleNewsSearchProvider,
)
from construction_intelligence.ingestion.web.html_extractor import (
    HTMLExtractor,
)
from construction_intelligence.ingestion.web.multi_search_provider import (
    MultiSearchProvider,
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

from construction_intelligence.web_ui import auth


#
# auth.py loads .env and reads AUTH0_*/SESSION_* env vars at its
# own import time (see auth.py), so by the time this line runs
# they're already resolved -- this just fails fast if anything
# required is still missing, rather than starting the server in
# a half-configured state.
#
auth.require_auth_config()

auth.configure_oauth()


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

app.add_middleware(
    SessionMiddleware,
    secret_key=auth.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=auth.SESSION_COOKIE_HTTPS_ONLY,
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
# diskcache, which is safe for this bounded level of concurrency;
# GoogleNewsSearchProvider's shared browser is protected by its
# own internal lock), so there's no need to rebuild this per
# project.
#
google_news_search_provider = GoogleNewsSearchProvider()

ingestion_service = WebEvidenceIngestionService(
    discovery_service=EvidenceDiscoveryService(
        search_provider=MultiSearchProvider(
            [
                SearXNGSearchProvider(),
                google_news_search_provider,
            ]
        ),
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


@app.on_event("shutdown")
def _close_google_news_browser() -> None:
    """
    Not required for the process to exit -- avoids leaving a
    Chromium process running past server shutdown during local
    dev.
    """

    google_news_search_provider.close()


@app.get("/")
def index(request: Request):

    if auth.get_session_user(request) is None:

        return RedirectResponse(url="/login")

    return FileResponse(STATIC_DIR / "index.html")


@app.get("/login")
async def login(request: Request):

    redirect_uri = f"{auth.APP_BASE_URL}/callback"

    return await auth.oauth.auth0.authorize_redirect(
        request,
        redirect_uri,
    )


@app.get("/callback")
async def callback(request: Request):

    token = await auth.oauth.auth0.authorize_access_token(
        request
    )

    userinfo = token.get("userinfo") or {}

    #
    # Store only what the UI needs to display -- this ends up in
    # a signed (not encrypted) cookie, so nothing more sensitive
    # than basic profile info belongs here.
    #
    request.session["user"] = {
        "sub": userinfo.get("sub"),
        "email": userinfo.get("email"),
        "name": userinfo.get("name"),
    }

    return RedirectResponse(url="/")


@app.get("/logout")
def logout(request: Request):

    request.session.clear()

    logout_params = urlencode(
        {
            "client_id": auth.AUTH0_CLIENT_ID,
            "returnTo": f"{auth.APP_BASE_URL}/",
        }
    )

    return RedirectResponse(
        url=(
            f"https://{auth.AUTH0_DOMAIN}/v2/logout"
            f"?{logout_params}"
        )
    )


@app.get("/me")
def me(request: Request) -> JSONResponse:

    user = auth.get_session_user(request)

    if user is None:

        return JSONResponse({"authenticated": False})

    return JSONResponse(
        {
            "authenticated": True,
            "email": user.get("email"),
            "name": user.get("name"),
        }
    )


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
async def upload(
    request: Request,
    file: UploadFile,
) -> JSONResponse:

    if auth.get_session_user(request) is None:

        return JSONResponse(
            {"error": "Not authenticated."},
            status_code=401,
        )

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
def get_job(
    job_id: str,
    request: Request,
) -> JSONResponse:

    if auth.get_session_user(request) is None:

        return JSONResponse(
            {"error": "Not authenticated."},
            status_code=401,
        )

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
