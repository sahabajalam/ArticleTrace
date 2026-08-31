---
title: AlloyCode — Deployment Guide
status: accepted
last_verified: 2026-05-20
source_of_truth: |
  docker-compose.yml, gcp.ps1, frontend/cloudbuild.yaml, orchestrator/Dockerfile,
  knowledge_engine/Dockerfile, .github/workflows/
companion_doc: SYSTEM.md  # §6 Deploy summarises; this doc has the full procedure
ai_guidance: |
  This is the accepted reference for local dev, Docker, and Cloud Run deployment
  of AlloyCode. Procedures here are tested; if a command fails, the docs win
  for the procedure but the underlying tool versions/flags may have moved —
  check the linked source files before assuming the doc is wrong. Companion to
  SYSTEM.md §6, which gives the architectural summary without the runbook
  detail.
---
# Deployment Guide — AlloyCode

> Canonical instructions for deploying AlloyCode (the EU AI Regulatory Compliance Scanner).
> Covers local development, Docker, Google Cloud Run, and best practices.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Repository Structure](#3-repository-structure)
4. [Environment Configuration](#4-environment-configuration)
5. [Local Development (UV + npm)](#5-local-development-uv--npm)
6. [Docker Deployment](#6-docker-deployment)
7. [Google Cloud Run Deployment](#7-google-cloud-run-deployment)
8. [Service Details](#7-service-details)
9. [Pipeline Scripts](#9-pipeline-scripts)
10. [Health Checks & Verification](#10-health-checks--verification)
11. [Known Issues & Workarounds](#11-known-issues--workarounds)
12. [Troubleshooting](#12-troubleshooting)
13. [Best Practices](#13-best-practices)

---

## 1. Architecture Overview

```
                         +-------------------+
                         |    Frontend        |
                         |  Next.js 16        |
                         |  Port 3000         |
                         +---------+---------+
                                   |
                                   | NEXT_PUBLIC_API_URL
                                   v
                 +-----------------+------------------+
                 |          Orchestrator               |
                 |   Multi-Agent Compliance Engine     |
                 |   LangGraph + Gemini 2.5 Flash      |
                 |   Port 8004                         |
                 +-----------------+-------------------+
                                   |
                                   v
                      +------------+---------+
                      |  Knowledge Engine    |
                      |  GraphRAG Research   |
                      |  Neo4j + Vectors     |
                      |  Port 8001           |
                      +----------------------+
```

**Data flow:**
1. User submits an AI system assessment via the frontend
2. Orchestrator runs a LangGraph workflow (Supervisor, Risk Classifier, Legal Research, Documentation Generator)
3. Legal Research Agent queries the Knowledge Engine for regulation-grounded answers
4. Results (including per-scan audit log) display in the frontend dashboard

---

## 2. Prerequisites

### Local Development

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|
| **UV** | >= 0.9.x | Python package manager & runner | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| **Python** | >= 3.11 (managed by UV) | Backend runtime | Installed automatically by UV |
| **Node.js** | >= 20.x | Frontend runtime | [nodejs.org](https://nodejs.org/) |
| **npm** | >= 10.x | Frontend package manager | Bundled with Node.js |
| **Git** | >= 2.x | Version control | [git-scm.com](https://git-scm.com/) |

### Docker / Cloud Run Deployment

| Tool | Version | Purpose |
|------|---------|---------|
| **Docker** | >= 24.x | Container runtime |
| **Docker Compose** | >= 2.x | Multi-container orchestration (local Docker) |
| **gcloud CLI** | Latest | Google Cloud deployment |

### External Services

| Service | Required | Purpose |
|---------|----------|---------|
| **Google AI Studio API Key** | Yes | Gemini 2.5 Flash LLM + `gemini-embedding-001` (3072-dim) |
| **Neo4j Aura DB** | Yes | Knowledge graph (cloud-hosted) |
| **PostgreSQL** | For Orchestrator | Scan persistence |
| **Redis** | For Orchestrator | Session state, caching (optional on Cloud Run) |

---

## 3. Repository Structure

```
Project Root/
|-- docker-compose.yml          # Master compose (all backend services)
|-- pipeline.ps1                # Unified lifecycle: -Action start|stop|restart-orch|kill-ports
|-- gcp.ps1                     # Unified GCP lifecycle: -Action setup|secrets|deploy|deploy-fast|cleanup
|-- .env                        # Root env (used by docker-compose)
|
|-- orchestrator/               # Port 8004 (local) / 8000 (Docker)
|   |-- src/
|   |   |-- api/main.py         #   FastAPI app
|   |   |-- agents/             #   LangGraph agent definitions
|   |   |-- control_plane/      #   Workflow orchestration
|   |   |-- state/              #   LangGraph state schema
|   |   |-- templates/          #   Report templates
|   |   |-- utils/              #   Helpers (cost tracker, etc.)
|   |   +-- config.py           #   Pydantic Settings
|   |-- Dockerfile
|   |-- pyproject.toml
|   +-- .env
|
|-- knowledge_engine/           # Port 8001
|   |-- src/
|   |   |-- api/main.py         #   FastAPI app
|   |   |-- stores/
|   |   |   +-- graph_store.py  #   Neo4j client (graph + native vector index)
|   |   |-- retrieval/
|   |   |   |-- engine.py       #   Hybrid retrieval (RRF)
|   |   |   +-- reasoning_engine.py
|   |   +-- config.py
|   |-- parsed_data/            #   Parsed regulatory texts
|   |-- scripts/                #   Data loading scripts (01-09)
|   |-- Dockerfile
|   |-- pyproject.toml
|   +-- .env
|
|-- frontend/                   # Port 3000 — AlloyCode Dashboard
|   |-- src/
|   |   |-- app/                #   Next.js App Router pages
|   |   |-- components/         #   Layout (Sidebar, Topbar, MainLayout)
|   |   +-- lib/api.ts          #   Centralized API URL config
|   |-- Dockerfile
|   +-- package.json
```

---

## 4. Environment Configuration

### 4.1 Root `.env` (used by `docker-compose.yml`)

```bash
# Required
GEMINI_API_KEY=<your-google-ai-studio-api-key>
GOOGLE_API_KEY=<same-key-or-separate>

# Neo4j Aura DB
NEO4J_URI=neo4j+ssc://<instance-id>.databases.neo4j.io
NEO4J_USER=<instance-id>
NEO4J_PASSWORD=<your-neo4j-password>

# Optional
ANTHROPIC_API_KEY=
SLACK_WEBHOOK_URL=
```

### 4.2 `orchestrator/.env`

```bash
GEMINI_API_KEY=<your-google-ai-studio-api-key>     # REQUIRED — no default
ANTHROPIC_API_KEY=                                   # optional fallback
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/compliance
REDIS_URL=redis://localhost:6379/0
GRAPHRAG_API_URL=http://localhost:8001
ENVIRONMENT=development
LOG_LEVEL=INFO
```

> **Critical:** The config expects `GEMINI_API_KEY`, not `OPENAI_API_KEY`. If you see a `ValidationError` for `gemini_api_key`, your `.env` has the wrong key name. See [BUG_LOG DL-005](./BUG_LOG.md).

### 4.3 `knowledge_engine/.env`

```bash
NEO4J_URI=neo4j+ssc://<instance-id>.databases.neo4j.io
NEO4J_USER=<instance-id>
NEO4J_PASSWORD=<your-neo4j-password>
NEO4J_DATABASE=<instance-id>
GOOGLE_API_KEY=<your-google-ai-studio-api-key>
PARSED_DATA_DIR=./parsed_data

# Optional — pin the embedding model explicitly so a Google deprecation
# becomes a 30-second .env edit instead of a code change. The default in
# src/config.py is `gemini-embedding-001` (3072-dim).
# EMBEDDING_MODEL=gemini-embedding-001
```

### 4.4 Frontend Environment

The frontend reads one variable at **build time**:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8004    # Set in start script
```

This is automatically set when using `pipeline.ps1 -Action start`. For Cloud Run, the orchestrator URL is baked in via Docker build arg.

---

## 5. Local Development (UV + npm)

### 5.1 One-Command Startup (Recommended)

```powershell
.\pipeline.ps1 -Action start
```

This will:
1. Check prerequisites (UV, Node.js)
2. Kill any stale processes on ports 8004, 8001, 3000
3. Clear orphaned PowerShell background jobs
4. Verify `.env` files exist for each module
5. Start knowledge_engine (8001), orchestrator (8004)
6. Start frontend (3000) with `NEXT_PUBLIC_API_URL` auto-configured
7. Wait for each service to become reachable

```powershell
# Backend only (skip frontend)
.\pipeline.ps1 -Action start -SkipFrontend

# Stop everything
.\pipeline.ps1 -Action stop

# Restart just the orchestrator (clears __pycache__, relaunches :8004)
.\pipeline.ps1 -Action restart-orch

# Free the pipeline ports without touching anything else
.\pipeline.ps1 -Action kill-ports
```

### 5.2 Manual Startup (Individual Modules)

If you need to start modules individually for debugging:

```bash
# Terminal 1 — Knowledge Engine
cd knowledge_engine
uv run python -m uvicorn src.api.main:app --reload --port 8001 --host 0.0.0.0

# Terminal 2 — Orchestrator
cd orchestrator
uv run python -m uvicorn src.api.main:app --reload --port 8004 --host 0.0.0.0

# Terminal 3 — Frontend
cd frontend
npm install       # first time only
npm run dev
```

> **Important:** Use `uv run python -m uvicorn`, NOT `uv run uvicorn`. The direct `uvicorn` script path fails when the project directory contains spaces. See [BUG_LOG DL-007](./BUG_LOG.md).

### 5.3 Startup Order

Services can start in any order, but the intended dependency chain is:

```
knowledge_engine (8001)  -->  orchestrator (8004)  -->  frontend (3000)
```

- **Orchestrator depends on:** Knowledge Engine (for legal research)
- **Frontend depends on:** Orchestrator (API calls)

---

## 6. Docker Deployment

### 6.1 Full Stack via Root Compose

```bash
# Start all backend services (detached)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Stop and remove volumes (full reset)
docker-compose down -v
```

The root `docker-compose.yml` starts 4 services:

| Service | Container | Port | Image |
|---------|-----------|------|-------|
| orchestrator | alloycode-orchestrator | 8004 | Built from `./orchestrator` |
| orchestrator-db | alloycode-orchestrator-db | 5432 | `postgres:15-alpine` |
| orchestrator-redis | alloycode-orchestrator-redis | 6379 | `redis:7-alpine` |
| graphrag-api | alloycode-knowledge-engine | 8001 | Built from `./knowledge_engine` |

### 6.2 Docker + Frontend Hybrid

Docker Compose runs the backend. For frontend development alongside:

```powershell
# Start backend via Docker
docker-compose up -d

# Start frontend locally (hot reload)
cd frontend
npm run dev
```

Or use the start script in docker mode:

```powershell
.\pipeline.ps1 -Action start -Mode docker
```

---

## 7. Google Cloud Run Deployment

### 7.1 Script Overview

| Script | Action | Purpose | Builds Images? |
|--------|--------|---------|----------------|
| `gcp.ps1` | `setup`       | First-time GCP setup (project, APIs, registry, secrets) | No |
| `gcp.ps1` | `secrets`     | Push `.env` values to Secret Manager | No |
| `gcp.ps1` | `deploy`      | Clean build + deploy (no Docker cache) | Yes |
| `gcp.ps1` | `deploy-fast` | Cached build + deploy (fast, code-only changes) | Yes |
| `gcp.ps1` | `cleanup`     | Delete all Cloud Run services, images, and secrets | No |

### 7.2 First-Time Setup

```powershell
# 1. Authenticate with Google Cloud
gcloud auth login

# 2. Ensure billing is enabled on the project
#    https://console.cloud.google.com/billing

# 3. Populate .env files for all modules (see Section 4)

# 4. Run first-time setup (creates project, APIs, registry, secrets)
.\gcp.ps1 -Action setup

# 5. Build and deploy all services
.\gcp.ps1 -Action deploy
```

### 7.3 Subsequent Deployments

```powershell
# Fast deploy (reuses Docker cache — good for code-only changes)
.\gcp.ps1 -Action deploy-fast

# Clean deploy (full rebuild — use when dependencies change)
.\gcp.ps1 -Action deploy
```

### 7.4 Updating Secrets Only

If you rotate an API key:

```powershell
# 1. Update the key in the relevant .env file
# 2. Re-push all secrets
.\gcp.ps1 -Action secrets

# 3. Redeploy to pick up new secret version
.\gcp.ps1 -Action deploy-fast
```

### 7.5 Starting From Scratch

```powershell
# Tear down everything
.\gcp.ps1 -Action cleanup

# Re-setup and deploy
.\gcp.ps1 -Action setup
.\gcp.ps1 -Action deploy
```

### 7.6 Cloud Run Configuration

| Service | Cloud Run Name | Port | Memory | CPU | Secrets |
|---------|---------------|------|--------|-----|---------|
| Knowledge Engine | `aegis-knowledge-engine` | 8001 | 2Gi | 2 | `GOOGLE_API_KEY`, `NEO4J_*` |
| Orchestrator | `aegis-orchestrator` | 8004 | 2Gi | 2 | `GEMINI_API_KEY`, `DATABASE_URL_ORCHESTRATOR` |
| Frontend | `aegis-frontend` | 3000 | 512Mi | 1 | (none) |

**Region:** `europe-west1` (Belgium) — supports domain mapping.

**Deploy order:** Knowledge Engine -> Orchestrator -> Frontend (frontend needs orchestrator URL baked in at build time).

### 7.7 Custom Domain Mapping

Domain mapping is only available in specific Cloud Run regions. `europe-west1` supports it.

```powershell
# 1. Verify domain ownership (one-time)
gcloud domains verify yourdomain.com

# 2. Map domain to frontend service
gcloud beta run domain-mappings create --service=aegis-frontend --domain=app.yourdomain.com --region=europe-west1

# 3. Add the DNS records shown by gcloud to your domain registrar
# 4. Wait 15-30 minutes for SSL certificate provisioning
```

**If domain mapping takes >1 hour:**
1. Verify DNS records are correct: `gcloud beta run domain-mappings describe --domain=app.yourdomain.com --region=europe-west1`
2. Check domain ownership: [Google Search Console](https://search.google.com/search-console)
3. Check for CAA DNS records blocking `pki.goog` (Google's certificate authority)
4. Check certificate status: `gcloud beta run domain-mappings list --region=europe-west1`
5. Alternative: use Firebase Hosting or a Global Application Load Balancer

**Regions that do NOT support domain mapping:** `europe-west2` (London), `asia-south1`, and others. See [Cloud Run locations docs](https://cloud.google.com/run/docs/locations).

### 7.8 CORS Configuration

The orchestrator's CORS settings are controlled by the `CORS_ORIGINS` environment variable:

- **Local development:** `ENVIRONMENT=development` automatically allows all origins (`*`)
- **Cloud Run:** `gcp.ps1 -Action deploy` sets `CORS_ORIGINS=*` because the frontend URL is dynamic and not known when the orchestrator deploys

For restricted production environments, do a two-pass deploy:
1. Deploy orchestrator (with `CORS_ORIGINS=*` temporarily)
2. Deploy frontend, note its URL
3. Update orchestrator: `CORS_ORIGINS=https://aegis-frontend-xxxxx.run.app`

---

## 8. Service Details

### 8.1 Orchestrator (Port 8004 local / 8000 Docker)

**Purpose:** Multi-agent AI compliance assessment engine.

**Stack:** FastAPI, LangGraph, Gemini 2.5 Flash, PostgreSQL, Redis

**Key Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/assessments` | Start a new compliance assessment |
| `GET` | `/api/v1/assessments/{session_id}` | Get assessment status/results |
| `GET` | `/api/v1/approvals` | List pending human approvals |
| `POST` | `/api/v1/approvals/{id}/decide` | Approve/reject a request |
| `GET` | `/api/v1/statistics` | System statistics |
| `GET` | `/health` | Health check |

**Agent Workflow (LangGraph):**

```
START -> Supervisor -> Risk Classifier -> Technical Assessor
                                              |
                                    Legal Research Agent
                                    (calls Knowledge Engine)
                                              |
                                    Documentation Generator -> END
```

**Config:** `orchestrator/src/config.py` — Pydantic Settings, reads from `.env`

**Required env vars:** `GEMINI_API_KEY` (no default, will crash without it)

---

### 8.2 Knowledge Engine (Port 8001)

**Purpose:** GraphRAG legal research engine for EU AI Act and GDPR.

**Stack:** FastAPI, Neo4j (Aura DB), Custom JSON Vector Store, Gemini Embeddings

**Key Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/vector/search` | Vector similarity search |
| `POST` | `/api/v1/graph/traverse` | Neo4j graph traversal |
| `POST` | `/api/v1/hybrid/search` | Combined RRF search |
| `POST` | `/api/v1/hybrid/reason` | Multi-hop reasoning with LLM synthesis |
| `GET` | `/health` | Health check |

**Knowledge Base Statistics:**
- Neo4j: 2,301 nodes (18 entity types), 4,423 relationships (13 types)
- Vector index: 2,198 embeddings across 7 logical collections (articles, recitals, interpretive, definitions, obligations, concepts, rights), all stored as `:Entity.embedding` properties
- Embedding model: Gemini `gemini-embedding-001` (3072 dimensions). The earlier `text-embedding-004` model was deprecated by Google on the `v1beta` endpoint and now returns 404 — see [BUG_LOG DL-019](./BUG_LOG.md).
- Retrieval: Reciprocal Rank Fusion (RRF) combining graph traversal + vector similarity, both sourced from the same Neo4j instance.

**Vector Store Implementation:**
Vectors live in Neo4j's native vector index (`entity_embedding`, HNSW, cosine, dim=3072) over the `:Entity` label. A single index covers all 7 logical collections; queries filter via `n.collection`. The earlier JSON-backed `VectorStore` and Weaviate sidecar were both retired in favour of this consolidated backend — see [BUG_LOG](./BUG_LOG.md). Re-embedding from raw text is handled by `scripts/05_load_vector_store.py`; bulk-loading pre-computed embeddings (e.g., from a backup) by `scripts/09_load_vectors_to_neo4j.py`.

---

### 8.3 Frontend (Port 3000)

**Purpose:** AlloyCode Compliance Dashboard — premium UI for managing assessments.

**Stack:** Next.js 16 (App Router), React 19, Tailwind CSS v4, lucide-react, framer-motion

**Pages:**

| Route | Description |
|-------|-------------|
| `/` | Dashboard — KPIs, risk distribution, recent assessments |
| `/assessments/new` | Start new assessment (6 golden test cases included) |
| `/assessments/[id]` | Assessment detail view |
| `/approvals` | Human review queue |
| `/knowledge` | Knowledge graph explorer |

**API Configuration:** All backend URLs are centralized in `frontend/src/lib/api.ts`. The base URL is set via `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8004`).

---

## 9. Pipeline Scripts

### `pipeline.ps1`

```
Usage: .\pipeline.ps1 -Action <start|stop|restart-orch|kill-ports>
                      [-Mode <docker|local>] [-SkipFrontend] [-SkipInfra]
                      [-Ports <int[]>] [-All]
Default: -Mode local
```

**Actions:**
- `start` — full pipeline startup (sequence below)
- `stop` — stop jobs, free ports (Neo4j Aura is remote, nothing to stop locally)
- `restart-orch` — kill :8004, clear orchestrator `__pycache__`, relaunch the orchestrator job
- `kill-ports` — terminate processes on `-Ports` (default 8004/8001/3000) or all user-space listeners (`-All`)

**`start` sequence:**
1. Prerequisite check (UV/Node.js or Docker)
2. Kill stale processes on ports 8004, 8001, 3000
3. Clear orphaned PowerShell background jobs
4. Verify `.env` files (copies from `.env.example` if missing)
5. Start backend services (UV or Docker Compose)
6. Wait for each service to respond (30s timeout per service)
7. Start frontend (npm dev server as background job)
8. Print endpoint summary

### Checking Running Jobs

```powershell
Get-Job                                             # List all jobs
Receive-Job -Id <job-id> -Keep                      # View output
Get-NetTCPConnection -LocalPort 8004 -ErrorAction SilentlyContinue  # Check port
```

---

## 10. Health Checks & Verification

### Quick Verification (All Services)

```bash
# Orchestrator
curl http://localhost:8004/health

# Knowledge Engine
curl http://localhost:8001/health

# Frontend
curl http://localhost:3000/
```

### End-to-End Test

Submit a test assessment to verify the full pipeline:

```bash
curl -X POST http://localhost:8004/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "system_description": "AI-powered resume screening tool that automatically filters job applications",
    "system_type": "Resume Screening AI",
    "company": "Test Corp",
    "context": "Used for hiring decisions in the EU market"
  }'
```

Expected: Returns a `session_id`. Poll `GET /api/v1/assessments/{session_id}` to watch the workflow progress.

### Golden Test Cases

The frontend includes 6 predefined test cases (GT-01 through GT-06) on the New Assessment page. These cover:
- GT-01: Resume screening AI (high-risk employment)
- GT-02: Medical diagnosis AI (high-risk healthcare)
- GT-03: Content recommendation (limited risk)
- GT-04: Spam filter (minimal risk)
- GT-05: Social scoring system (prohibited)
- GT-06: Credit scoring AI (high-risk financial)

---

## 11. Known Issues & Workarounds

### Spaces in Project Path

The project path contains spaces (`D:\60 Days\Projects\...`). This causes:

- **`uv run uvicorn` fails** — Use `uv run python -m uvicorn` instead. The start script handles this automatically.
- **PowerShell `Start-Job` PATH issues** — The start script resolves full executable paths before launching jobs.

### Python Version

UV manages its own Python. The project uses Python 3.13.x (managed by UV). Vectors are stored in Neo4j (native vector index), so there is no ChromaDB / Weaviate dependency.

### Neo4j Aura DB

The knowledge graph is hosted on Neo4j Aura DB (cloud). If the Aura instance is paused (free tier auto-pauses after 3 days of inactivity), the Knowledge Engine will fail to connect. Resume the instance from the [Neo4j Aura Console](https://console.neo4j.io/).

### PostgreSQL for Orchestrator

The orchestrator persists scan results in PostgreSQL. In local mode (without Docker), it falls back to in-memory storage if no database is reachable on `DATABASE_URL`.

### Frontend Build Warning

The Knowledge Graph page uses static data (not fetched from APIs). This is intentional — it displays verified knowledge base statistics. Live data integration is a future enhancement.

### Cloud Run Port Mismatch

Cloud Run defaults to `PORT=8080`. Each service has a custom port in its Dockerfile. The deploy script explicitly passes `--port=<port>` for each service. If you deploy manually, always include `--port`.

### Gemini Embedding Model Deprecation

Google periodically removes embedding models from the `v1beta` endpoint that the `google-genai` Python SDK targets. When this happens, every retrieval endpoint in the Knowledge Engine returns HTTP 500 and the `legal_research` agent silently produces empty `finding_citations` (the workflow still completes — only the "Legal citations" block in the scan UI is missing).

**Currently supported model:** `gemini-embedding-001` (3072-dim).
**Removed:** `text-embedding-004` (returns 404 NOT_FOUND on `embedContent`).

**Diagnose:** `curl -X POST http://localhost:8001/api/v1/vector/search -H "Content-Type: application/json" -d '{"query":"test","top_k":1}'`. A 500 here with `/health` reporting `vector_index: online` is a near-certain match for this failure mode (Neo4j is fine; the per-request Gemini embedding call is what's failing). See [BUG_LOG DL-019](./BUG_LOG.md).

### Cloud Run `PORT` Environment Variable

Cloud Run reserves `PORT` as a system environment variable. Do NOT pass it in `--set-env-vars` — Cloud Run sets it automatically from `--port`. Doing so will cause deployment to fail.

**Dockerfiles must read `$PORT` from the env, not hardcode a port.** Both backend Dockerfiles now use the shell-form CMD pattern:

```dockerfile
CMD ["sh", "-c", "exec uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8004}"]
```

`sh -c` enables `$PORT` expansion (exec form `["uvicorn", ...]` does not). `exec` replaces the shell with uvicorn so uvicorn becomes PID 1 — Cloud Run sends SIGTERM directly to PID 1 on shutdown, and a sh wrapper without `exec` swallows it, producing a 10-second termination delay on every revision rollover. See [BUG_LOG DL-022](./BUG_LOG.md).

### "Container failed to start and listen on PORT"

```
ERROR: (gcloud.run.deploy) The user-provided container failed to start
and listen on the port defined provided by the PORT=8004 environment
variable within the allocated timeout.
```

This message covers **two distinct failure modes** that look identical from the deploy CLI:

1. The process is running but binding to the wrong port (Dockerfile hardcodes a port that doesn't match `--port`).
2. The process exited (any reason) before binding any port — could be a missing dep, a config error, an import-time crash.

**Always pull the actual revision logs before assuming it's a port issue:**

```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.revision_name="<failed-revision>"' \
  --limit=30 \
  --format="value(textPayload)" \
  --project=<your-project>
```

The failed revision name is in the deploy error output (look for `revision_name=<service>-<NNNNN>-<hash>`). The application stderr/stdout from the doomed startup is the source of truth.

**Common real causes when the port is correctly configured:**

- **Missing system binary.** The orchestrator imports `code_analyzer/`, which uses GitPython. GitPython runs an import-time check that calls `exit(1)` if `git` isn't in PATH. The base `python:3.11-slim` image doesn't ship git. Fix: `apt-get install -y --no-install-recommends git` in the final stage. See [BUG_LOG DL-022](./BUG_LOG.md).
- **Database connection blocking startup.** If `lifespan` calls `await init_db()` and the database is unreachable, uvicorn blocks before binding. Either make the DB connection lazy (open on first request) or set `--timeout=600` on the deploy to give cold connections time to establish.
- **Synchronous slow imports.** Large dependency trees (e.g. importing `langchain` ecosystem) can take 20-30s. Set `--timeout=300` (the gcp.ps1 default) or higher.

---

## 12. Troubleshooting

### "Failed to canonicalize script path"

```
$ uv run uvicorn src.api.main:app --port 8004
Failed to canonicalize script path
```

**Fix:** Use `uv run python -m uvicorn src.api.main:app --port 8004`

### "ValidationError: gemini_api_key Field required"

```
pydantic_core.ValidationError: gemini_api_key Field required
```

**Fix:** Add `GEMINI_API_KEY=<your-key>` to `orchestrator/.env`. Do NOT use `OPENAI_API_KEY`.

### "API key not valid" on Cloud Run

```
Error calling model 'gemini-2.5-flash': API key not valid.
```

**Diagnose:**
1. Test your key directly: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"`
2. If invalid, generate a new one at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Update `orchestrator/.env` and re-push: `.\gcp.ps1 -Action secrets`
4. Redeploy: `.\gcp.ps1 -Action deploy-fast`

### "Attribute name 'metadata' is reserved"

```
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved
```

**Fix:** Already fixed in the codebase. If you see this error, pull the latest code.

### Backend Job Fails Silently

If a backend job shows `[X] ... failed to start!` with no error details:

```powershell
Get-Job
Receive-Job -Id <job-id> -Keep -ErrorAction SilentlyContinue
```

Common causes: missing `.env` file, port already in use, Python import error.

### Port Already in Use After Stop

```powershell
Get-NetTCPConnection -LocalPort 8004 | Select-Object OwningProcess
Get-Process -Id <pid>
Stop-Process -Id <pid> -Force
```

### Frontend Shows "Failed to connect to AlloyCode API"

Check:
1. Is the orchestrator running? `curl http://localhost:8004/health`
2. Is `NEXT_PUBLIC_API_URL` set? (Auto-set by `pipeline.ps1 -Action start` locally; baked in via Docker build arg on Cloud Run)
3. CORS configured? Orchestrator allows `*` origins in development. On Cloud Run, `CORS_ORIGINS=*` is set via env var.

### Cloud Run Deploy: "Container failed to start"

```
ERROR: The user-provided container failed to start and listen on the port
defined provided by the PORT=8080
```

**Fix:** Add `--port=<actual-port>` to the `gcloud run deploy` command. Each service listens on its own port, not 8080.

### Knowledge Engine `/api/v1/hybrid/reason` Returns 500

Symptoms: scan completes, finding rows render `mapped_articles` badges (from rule YAML), but the "Legal citations" block is missing on every expanded row. The `legal_research` agent catches HTTP errors per-rule and returns empty citations without surfacing a workflow-level warning, so the dashboard looks healthy.

**Quick check:**

```bash
curl -X POST http://localhost:8001/api/v1/vector/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test","top_k":1}'
```

If this returns `Internal Server Error` while `curl http://localhost:8001/health` returns 200, the most likely cause is a deprecated Gemini embedding model name. Confirm in the Knowledge Engine's terminal — look for `google.genai.errors.ClientError: 404 NOT_FOUND ... is not supported for embedContent`.

**Fix:** Set `EMBEDDING_MODEL=gemini-embedding-001` in `knowledge_engine/.env` (or update the default in `src/config.py`) and restart the service. The stored vectors in Neo4j (property `:Entity.embedding`) are 3072-dim and match this model — no re-embed required. See [BUG_LOG DL-019](./BUG_LOG.md).

### Neo4j Connection Timeout

The Knowledge Engine can't reach Neo4j Aura. Check:
1. Is the Aura instance running? Log in to [console.neo4j.io](https://console.neo4j.io/)
2. Are `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` correct in `knowledge_engine/.env`?
3. Is `neo4j+ssc://` (TLS) being used? Aura requires encrypted connections.

### gcloud stderr Crashes PowerShell Script

```
NativeCommandError: Listing items under project...
```

**Cause:** `$ErrorActionPreference = "Stop"` + gcloud writes info messages to stderr.
**Fix:** Wrap gcloud read-only calls in `Invoke-GcloudQuery` (already done in all deploy scripts).

### Domain Mapping Stuck / Takes Too Long

If `gcloud beta run domain-mappings create` shows pending for >30 min:
1. Verify DNS records match exactly what gcloud showed
2. Check `gcloud beta run domain-mappings describe --domain=yourdomain.com --region=europe-west1`
3. Ensure no CAA records block `pki.goog`
4. Ensure domain is verified in Google Search Console
5. Consider Firebase Hosting or ALB as alternatives

---

## 13. Best Practices

### Deployment

1. **Always test API keys before deploying.** Run a quick curl against the provider's API to verify the key works before pushing to Secret Manager.
2. **Use `gcp.ps1 -Action deploy-fast` for code-only changes.** It reuses the Docker layer cache and skips the cache prune step — typically 5-10x faster than a clean build.
3. **Use `gcp.ps1 -Action deploy` when changing dependencies.** Modified `pyproject.toml`, `package.json`, or `Dockerfile`? Do a clean build to ensure layers are rebuilt.
4. **Never hardcode Cloud Run URLs.** Use environment variables (`GRAPHRAG_API_URL`, `MONITORING_API_URL`, `NEXT_PUBLIC_API_URL`) — the deploy script resolves and injects them automatically.
5. **Tag images with timestamps.** The deploy script creates `manual-YYYYMMDD-HHmmss` tags alongside `:latest`. This makes rollback trivial: `gcloud run deploy --image=<old-tag>`.

### Secrets Management

6. **Keep `.env` files out of git.** They're in `.gitignore`. Never commit API keys.
7. **Use `gcp.ps1 -Action secrets` as the single source of truth** for pushing secrets to GCP. Don't manually create secrets in the console — it's easy to get names wrong.
8. **Test secrets after rotation.** After updating a key in `.env` and running `gcp.ps1 -Action secrets`, always redeploy to verify the new key works end-to-end.
9. **Never pipe secrets to `gcloud --data-file=-` on Windows.** PowerShell 5.1 appends `\r\n` to piped strings, and `WriteAllText` adds a UTF-8 BOM — both corrupt secret values. Use `WriteAllBytes` to write a temp file with exact bytes, then pass `--data-file=$tmpFile`. See [BUG_LOG DL-018](./BUG_LOG.md).

### PowerShell Scripting for GCP

9. **Never use `$args` as a variable name.** It's a reserved automatic variable in PowerShell. Use `$dockerArgs`, `$cmdArgs`, etc.
10. **Always wrap gcloud queries in `Invoke-GcloudQuery`.** gcloud writes informational messages to stderr, which PowerShell treats as errors under `$ErrorActionPreference = "Stop"`.
11. **Don't use `$script:` scope tricks across function boundaries.** Use return values or `Invoke-GcloudQuery` instead. Variables set as `$script:foo` inside a scriptblock passed to another function won't be visible in the calling function's local scope. Concrete failure: the `Invoke-Deploy` secret-verification step did exactly this and reported every secret as MISSING immediately after `secrets` had successfully pushed them. See [BUG_LOG DL-023](./BUG_LOG.md).
12. **Don't pass `PORT` in `--set-env-vars`.** Cloud Run reserves it. Use `--port` flag instead.

### Retrieval & Embeddings

13. **Pin the embedding model in `.env`, not as a code default.** Google deprecates models on `v1beta` without warning; an `.env`-driven name turns a deprecation into a 30-second config change instead of a code edit + redeploy. See [BUG_LOG DL-019](./BUG_LOG.md).
14. **Cross-check stored embedding dimensions against the configured model before switching.** A 768-dim model querying 3072-dim stored vectors won't 500 — it will silently produce garbage rankings, which is worse. Verify against Neo4j with `MATCH (n:Entity) WHERE n.embedding IS NOT NULL RETURN size(n.embedding) AS dim LIMIT 1`.
15. **Make `/health` exercise the retrieval path.** A health probe that only checks "store is loaded" misses deprecated-model failures. Add a synthetic embed + 1-doc cosine lookup so the probe fails the moment the embedding API stops responding.
16. **Don't let agents swallow upstream failures silently.** The `legal_research` agent catches HTTP errors per-rule (correct for partial outages) but currently produces no workflow-level signal when **every** lookup fails. If you add a new agent that depends on an upstream service, surface a top-level warning when that service is unreachable so the UI can flag it instead of rendering an empty block.

### Architecture

17. **Deploy services in dependency order.** Knowledge Engine first, then Orchestrator (needs its URL), then Frontend (needs Orchestrator URL baked in at build time).
18. **Use wildcard CORS for demos, explicit origins for production.** The deploy script sets `CORS_ORIGINS=*` which is fine for a public portfolio demo. For production, whitelist specific origins.
19. **Use `--min-instances=0` for cost efficiency.** Cold starts add 5-10 seconds but save money when the demo isn't being used. Set `--min-instances=1` for the orchestrator if cold starts are unacceptable.
20. **Choose regions that support domain mapping.** `europe-west1` (Belgium) supports it. `europe-west2` (London) does not. Check the [Cloud Run locations docs](https://cloud.google.com/run/docs/locations) before deploying.

### Container Images

21. **Don't hardcode ports in Dockerfiles.** Use `${PORT:-<default>}` via shell-form CMD so Cloud Run's injected `PORT` is honoured and local docker-compose still has a sensible default. The full pattern is `CMD ["sh", "-c", "exec uvicorn ... --port ${PORT:-8004}"]` — `exec` is critical so uvicorn becomes PID 1 and receives SIGTERM directly. See [BUG_LOG DL-022](./BUG_LOG.md).
22. **Slim base images don't ship development tools.** `python:3.11-slim` has no `git`, `curl`, `gcc`, etc. If your application imports a Python wrapper around a CLI (GitPython, pygit2, fitz/PyMuPDF compiled deps), you must `apt-get install` the underlying tool. GitPython specifically runs an import-time `git --version` check and `exit(1)` on failure, which produces the misleading "container failed to listen on PORT" Cloud Run error.
23. **Always pull Cloud Run logs before debugging a deploy failure.** The deploy CLI's "container failed to listen on PORT" error covers everything from real port misconfiguration to import-time crashes. `gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.revision_name="<failed-revision>"'` shows the actual stderr. Diagnosing from the deploy error alone routinely wastes a build cycle on the wrong fix.

### Backend Consolidation

24. **Two stateful backends mean two failure surfaces.** Every operational incident has to be triaged across both; every deploy has to wire two independent secret families; every health probe has to cover two systems. Adding a specialized store (vector DB, separate analytics warehouse, etc.) is sometimes worth it — but the cost isn't the new system in isolation. The cost is the second failure surface for everything you already have. See [BUG_LOG DL-021](./BUG_LOG.md) — the original ChromaDB → JSON → Weaviate progression each solved a problem but added fan-out, until the system landed back on a single Neo4j-hosted vector index.
25. **For a small enough corpus, the graph DB itself can host vectors.** Neo4j 5.13+ has native HNSW vector indexes. For 2,198 embeddings × 3072 floats × 4 bytes ≈ 27 MB, this fits comfortably under the Aura free tier's 200 MB allowance. Bigger corpora may genuinely need a specialised vector DB; small ones don't, and consolidation removes operational fragility.
26. **Free-tier hosted databases auto-pause — and then auto-delete. A keep-alive ping only helps with the first.** Neo4j Aura Free pauses after 3 days of inactivity and *deletes* the instance after ~30 days. Pausing is activity-based, so a cron ping resumes it; deletion is policy-based, and a `MATCH (n) RETURN count(n)` query does not reset that timer. `.github/workflows/keep-aura-alive.yml` was built on the assumption that it would, ran for two months, and the graph was destroyed twice anyway (BUG_LOG DL-025, then `e8097dda` on 2026-08-31). It was deleted rather than disabled: a workflow with a measured 0% success rate is worse than no workflow, because it looks like protection. What replaces it is `.github/workflows/backup-knowledge-graph.yml` — a weekly `10_backup_to_jsonl.py` run that self-verifies the dump and publishes it as a 90-day artifact, so deletion costs a ~4-minute restore instead of a rebuild.
