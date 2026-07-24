# Construction Intelligence

## Overview

Construction Intelligence is an evidence discovery and analysis platform designed to identify, collect, evaluate, and structure publicly available information about construction and infrastructure projects.

The system combines localized search intelligence, multi-source web discovery, URL ranking, candidate evaluation, and document extraction pipelines to transform unstructured web information into structured project evidence.

The primary goal is to answer questions such as:

- What construction projects are occurring in a specific area?
- Which agencies, contractors, or organizations are involved?
- Where can official project documentation be found?
- What evidence supports a project's existence, scope, and timeline?

---

# Core Concepts

## Projects

A project represents a construction or infrastructure initiative being investigated.

Projects contain:

- Project name
- Aliases
- Location
- Country
- Region
- City
- State/province
- Road or infrastructure identifiers
- Search metadata

Example:

```
Horizon Drive Roundabout
Grand Junction, Colorado
United States
```

Project metadata is used throughout the pipeline for:

- Search query generation
- Evidence ranking
- Candidate scoring
- Extraction prioritization

---

# System Architecture

The application follows a staged evidence discovery pipeline:

```
                 Project
                    |
                    v
          Search Context Generation
                    |
                    v
          Search Query Generation
                    |
                    v
            Web Discovery Layer
                    |
                    v
             URL Deduplication
                    |
                    v
            Evidence Ranking
                    |
                    v
          Candidate Quality Scoring
                    |
                    v
              Document Extraction
                    |
                    v
            Evidence Creation
                    |
                    v
          Structured Evidence Store
```

---

# Components

## Search Context

Search Context provides localized intelligence used to improve construction project discovery.

It contains:

- Regional vocabulary
- Construction terminology
- Infrastructure terminology
- Procurement terminology
- Government source signals
- Negative search filtering terms
- Source ranking preferences

Examples:

```
construction
infrastructure
capital improvement
contract
bid
RFP
procurement
```

The goal is to adapt searches based on geography and local terminology.

---

# Search Query Generation

The system generates targeted search queries from project metadata.

Example:

```
"Horizon Drive" construction Grand Junction Colorado

"Horizon Drive" construction project Grand Junction Colorado

"Horizon Drive Roundabout" construction Grand Junction Colorado

"Horizon Drive" contract Grand Junction Colorado
```

Queries are organized by evidence priority.

## Tier 1

High-value sources:

- Government websites
- Procurement systems
- Official project pages

## Tier 2

Construction-related sources:

- Contractors
- Engineering firms
- Infrastructure organizations

## Tier 3

Discovery sources:

- News
- General web results

---

# Search Providers

Search providers implement a common interface:

```python
SearchProvider
```

The architecture separates search collection from evidence processing.

Current provider:

```
SearXNGSearchProvider
```

The system is designed to support multiple search providers:

- Google Search API
- Exa Search API
- Bing Search API
- Other specialized search providers

Search providers can be replaced without modifying:

- Ranking
- Candidate scoring
- Extraction
- Evidence creation

---

# Evidence Discovery Service

The Evidence Discovery Service coordinates web discovery.

Process:

1. Retrieve project search context
2. Generate localized search queries
3. Execute searches
4. Collect candidate URLs
5. Remove duplicates

Example:

Input:

```
Project:
Horizon Drive Roundabout

Location:
Grand Junction, Colorado
```

Potential output:

```
https://www.gjcity.org/515/Horizon-Drive-Business-Improvement

https://shawconstruction.net/projects/760-horizon-drive
```

---

# Evidence Ranking

The Evidence Ranker evaluates discovered URLs before extraction.

Ranking considers:

## Source Authority

Examples:

- Government domains
- Municipal websites
- Transportation agencies
- Contractors
- Engineering firms

## Construction Signals

Examples:

```
construction
improvement
roundabout
intersection
contract
bid
award
engineering
transportation
```

## Project Similarity

The ranker evaluates:

- Project name
- Project aliases
- Road names
- Location information

Example:

A URL such as:

```
https://shawconstruction.net/projects/760-horizon-drive
```

receives a higher ranking because it contains:

- Construction company source
- Project page indicator
- Project identifier match

---

# Candidate Scoring

After ranking, candidates are evaluated by:

```
EvidenceCandidateScoringService
```

The candidate scorer determines whether a URL should proceed to extraction.

Positive signals:

- Government domains
- Construction terminology
- Project identifiers
- Procurement references
- Document indicators

Negative signals:

- Entertainment content
- Banking pages
- Real estate listings
- Irrelevant commercial pages

Example:

Rejected:

```
https://www.playstation.com/en-us/horizon/
```

Accepted:

```
https://shawconstruction.net/projects/760-horizon-drive
```

---

# Extraction Pipeline

Candidates that pass evaluation are sent to extraction services.

The extraction pipeline supports:

- HTML extraction
- PDF extraction
- Fallback extraction methods

Extracted documents are converted into structured:

```
Evidence
```

objects.

---

# Evidence Objects

Evidence represents structured information collected from external sources.

Evidence may contain:

- Source URL
- Associated project
- Extracted content
- Document metadata
- Source information

Examples:

- Government announcements
- Construction updates
- Contractor project pages
- Procurement documents
- Engineering reports

---

# Development Workflow

## Environment Setup

Clone the repository:

```bash
git clone https://github.com/lmmcgov/ConstructionIntelligence.git

cd ConstructionIntelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Testing

## Full Evidence Pipeline

```bash
python scripts/test_evidence_pipeline.py
```

## Search Provider Test

```bash
python scripts/test_search.py
```

## Query Generation Test

```bash
python scripts/test_query_generation.py
```

## Ranker Test

```bash
python scripts/test_ranker.py
```

---

# Local SearXNG Development

The current development environment uses a local SearXNG instance.

Check running containers:

```bash
docker ps
```

Expected:

```
searxng
localhost:8080
```

Test availability:

```bash
curl http://localhost:8080
```

---

# Project Structure

```
ConstructionIntelligence/

├── src/
│
│   └── construction_intelligence/
│
│       ├── core/
│       │   ├── project.py
│       │   └── evidence.py
│       │
│       ├── ingestion/
│       │   └── web/
│       │       ├── evidence_discovery_service.py
│       │       ├── evidence_ranker.py
│       │       ├── searxng_search_provider.py
│       │       ├── search_context.py
│       │       └── search_query_generator.py
│       │
│       └── services/
│           └── evidence_candidate_scoring_service.py
│
├── scripts/
│   ├── test_search.py
│   ├── test_ranker.py
│   ├── test_query_generation.py
│   └── test_evidence_pipeline.py
│
└── README.md
```

---

# Design Principles

## Modular Architecture

Each component has a single responsibility.

Examples:

Search providers:

- Discover URLs

Rankers:

- Prioritize candidates

Scoring services:

- Filter weak candidates

Extractors:

- Retrieve document content

Evidence factories:

- Create structured evidence records

---

## Evidence First

The system prioritizes traceable information over generated summaries.

Every conclusion should be supported by:

- Source URL
- Extracted information
- Project association

---

## High Recall → High Precision

The pipeline intentionally separates discovery from evaluation.

Discovery:

```
Find many possible sources
```

Evaluation:

```
Determine which sources matter
```

This allows search coverage to expand while maintaining evidence quality.

---

# Future Development

## Multi-Provider Search

Planned search providers:

- Google Search API
- Exa Search API
- Bing Search API

The goal is to combine:

- Broad search coverage
- Semantic search
- Local fallback search

---

## Improved Extraction

Future capabilities:

- PDF table extraction
- Project timeline extraction
- Contractor identification
- Automated project summaries
- Document classification

---

## Evidence Evaluation

Future improvements:

- Confidence scoring
- Source reliability scoring
- Duplicate evidence merging
- Conflicting evidence detection

---

# License

License information pending.
