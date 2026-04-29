# EU AI Regulatory Compliance Engine — Project Completeness Analysis

**Date:** February 23, 2026  
**Scope:** Full audit of all three core modules, infrastructure, data pipeline, and integration readiness.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Module-by-Module Analysis](#2-module-by-module-analysis)
   - [Core 1 — Monitoring & Governance](#21-core-1--monitoring--governance-port-8002)
   - [Core 2 — GraphRAG Legal Research](#22-core-2--graphrag-legal-research-port-8001)
   - [Core 3 — Compliance Agent (Orchestrator)](#23-core-3--compliance-agent-orchestrator-port-8000)
3. [Data Pipeline Status](#3-data-pipeline-status)
4. [Infrastructure & DevOps](#4-infrastructure--devops)
5. [Testing Coverage](#5-testing-coverage)
6. [Cross-Module Integration](#6-cross-module-integration)
7. [What's Left To Run the Full Pipeline](#7-whats-left-to-run-the-full-pipeline)
8. [Recommended Execution Order](#8-recommended-execution-order)

---

## 1. Executive Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| **Core 1 (Monitoring)** | ✅ ~95% Complete | Fully implemented source code; needs env/DB setup only |
| **Core 2 (GraphRAG)** | ✅ ~90% Complete | All code implemented; data parsed & loaded; raw_data dir is empty (needs symlink or copy from New_Data) |
| **Core 3 (Compliance Agent)** | ✅ ~90% Complete | All 5 agents + supervisor workflow built; needs API keys and infra |
| **Data Pipeline** | ✅ ~85% Complete | Pre-parsed data exists (10 entity files, 10 relationship files, 3 interpretive files, 7 legal files); vector store JSON files exist in chroma_data/; raw_data/ is empty |
| **Docker / Infra** | ✅ ~90% Complete | All Dockerfiles, docker-compose files, master compose ready; `.env` is template only |
| **Tests** | ⚠️ ~70% Complete | Unit tests exist for all 3 modules; integration tests are mock-based; no end-to-end tests against live services |
| **Full Pipeline Runnable?** | ❌ Not Yet | Blocked by: missing API keys, empty raw_data dir, no `uv.lock` files verified, DB migrations not run |

**Bottom line:** The codebase is architecturally complete. All source files are implemented with real logic (not stubs). The blocking issues are environmental/operational, not code gaps.

---

## 2. Module-by-Module Analysis

### 2.1 Core 1 — Monitoring & Governance (Port 8002)

**Purpose:** Receives monitoring data from Core 2 and Core 3, performs EU AI Act Article 14 and GDPR Article 22 compliance checks, detects drift/bias, and sends alerts.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 55 | ✅ Complete | Pydantic Settings with all env vars |
| `src/api/main.py` | 657 | ✅ Complete | 15+ endpoints: decisions, GraphRAG queries, compliance status, violations, alerts, metrics, drift, bias |
| `src/api/middleware.py` | 68 | ✅ Complete | Prometheus metrics middleware |
| `src/api/rate_limit.py` | 64 | ✅ Complete | slowapi rate limiting with X-Forwarded-For support |
| `src/compliance/eu_ai_act.py` | 285 | ✅ Complete | Article 14 human oversight monitor with 3 rules |
| `src/compliance/gdpr.py` | 273 | ✅ Complete | Article 22 automated decision-making monitor with 5 rules |
| `src/monitoring/drift.py` | 348 | ✅ Complete | Evidently-based data/prediction/confidence drift detection |
| `src/monitoring/bias.py` | 297 | ✅ Complete | Chi-square bias detection across 10 protected attributes |
| `src/monitoring/metrics.py` | 202 | ✅ Complete | 15+ Prometheus metric definitions |
| `src/alerting/alert_manager.py` | 383 | ✅ Complete | Slack + email routing by severity, compliance violation alerts, bias alerts, drift alerts |
| `src/client/monitoring_client.py` | 248 | ✅ Complete | Client SDK for Core 2/3 to send data |
| `src/database/models.py` | 259 | ✅ Complete | 6 SQLAlchemy models: DecisionLog, GraphRAGQueryLog, ComplianceViolation, AlertLog, DriftReport, BiasReport |
| `src/database/session.py` | 72 | ✅ Complete | Engine, session factory, init_db, get_db dependency |

#### Dependencies (pyproject.toml)
- FastAPI, SQLAlchemy, asyncpg, psycopg2-binary, Alembic, Evidently, Prometheus-client, slowapi, structlog
- Dev: pytest, pytest-asyncio, pytest-cov, ruff, mypy

#### Gaps / Issues
- **No Alembic migrations folder** — `init_db()` uses `create_all()` which works but isn't production-grade
- Prometheus config (`prometheus.yml`) exists and is ready
- Grafana is commented out in docker-compose (optional)

---

### 2.2 Core 2 — GraphRAG Legal Research (Port 8001)

**Purpose:** Knowledge graph (Neo4j) + vector store for hybrid retrieval of EU AI Act and GDPR legal provisions. Exposes REST API for Core 3's Legal Research Agent.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 41 | ✅ Complete | Neo4j, ChromaDB (not actually used — see below), Google AI, retrieval params |
| `src/api/main.py` | 319 | ✅ Complete | 5 endpoints: vector/search, graph/traverse, hybrid/search, hybrid/reason, health |
| `src/schema/entities.py` | 296 | ✅ Complete | 19 entity types with Pydantic models |
| `src/schema/relationships.py` | 83 | ✅ Complete | 25 relationship types |
| `src/stores/graph_store.py` | 350 | ✅ Complete | Neo4j CRUD, batch operations, graph traversal, node counting |
| `src/stores/vector_store.py` | 186 | ✅ Complete | **Custom JSON-backed vector store** (NOT ChromaDB despite config) — cosine similarity search, metadata filtering |
| `src/retrieval/engine.py` | 248 | ✅ Complete | Hybrid Graph+Vector retrieval with RRF fusion |
| `src/retrieval/reasoning_engine.py` | 305 | ✅ Complete | LLM-powered multi-hop reasoning with citation validation, confidence scoring |
| `src/retrieval/query_models.py` | 176 | ✅ Complete | 6 answer types, typed request/response models |

#### Extractors (8 files) — All Implemented ✅
- `structural_extractor.py`, `rule_based_extractor.py`, `definition_extractor.py`
- `obligation_extractor.py`, `concept_extractor.py`, `right_extractor.py`
- `cross_regulation_extractor.py`, `__init__.py`

#### Parsers (7 files) — All Implemented ✅
- `article_parser.py`, `recital_parser.py`, `annex_parser.py`
- `case_law_parser.py`, `guideline_parser.py`, `enforcement_parser.py`
- `base_parser.py`

#### Data Pipeline Scripts (8 scripts) — All Implemented ✅
| Script | Purpose | Status |
|--------|---------|--------|
| `01_parse_raw_data.py` | Parse raw legal text → JSON entities | ✅ |
| `02_load_structural_kg.py` | Load structural entities into Neo4j | ✅ |
| `02a_extract_structural_rels.py` | Extract structural relationships | ✅ |
| `02b_validate_graph_local.py` | Validate local graph without Neo4j | ✅ |
| `03_extract_semantic.py` | Extract semantic entities via LLM | ✅ |
| `03b_extract_obligations.py` | Extract obligations | ✅ |
| `03c_extract_cross_regulation.py` | Extract cross-regulation links | ✅ |
| `03d_validate_full_graph.py` | Validate full graph | ✅ |
| `03e_extract_concepts.py` | Extract legal concepts | ✅ |
| `03f_extract_rights.py` | Extract data subject rights | ✅ |
| `04_load_full_kg.py` | Load all data into Neo4j | ✅ |
| `05_load_vector_store.py` | Build vector embeddings | ✅ |
| `06_demo_query.py` | Demo query script | ✅ |
| `07_run_golden_tests.py` | Run golden test queries | ✅ |
| `08_coverage_report.py` | Coverage analysis report | ✅ |

#### Pre-Parsed Data — Exists ✅
- **`parsed_data/entities/`**: 10 JSON files (actors, ai_system_types, concepts, data_types, definitions, exemptions, obligations, penalties, rights, risk_categories)
- **`parsed_data/relationships/`**: 10 JSON files (cites, complements, concept_links, containment, defines, interprets, obligation_links, references, right_links, semantic_links)
- **`parsed_data/legal/`**: 7 JSON files (ai_act articles, chapters, recitals, annexes; gdpr articles, chapters, recitals)
- **`parsed_data/interpretive/`**: 3 JSON files (case_law, edpb_guidelines, enforcement_actions)
- **`chroma_data/`**: 7 pre-built vector store JSON files (articles, concepts, definitions, interpretive, obligations, recitals, rights)

#### Gaps / Issues
- **`raw_data/` directory is EMPTY** — The pipeline scripts (01_parse_raw_data.py) expect raw legal texts here. The actual raw data appears to be in `New_Data/` at the project root. Need to symlink or copy `New_Data/` → `core_2_knowledge_base/raw_data/` OR update the config path.
- **Vector store implementation mismatch**: `config.py` has `chroma_host`/`chroma_port` settings but `vector_store.py` is actually a custom JSON-backed store (comment says "ChromaDB incompatible with Python 3.14"). Config settings for ChromaDB are dead code.
- `src/validation/` directory has only `__init__.py` — validation logic might be inline in scripts instead.
- **Google API key required** for embeddings (text-embedding-004) and LLM reasoning (gemini-1.5-pro / gemini-2.0-flash)

---

### 2.3 Core 3 — Compliance Agent / Orchestrator (Port 8000)

**Purpose:** Multi-agent LangGraph workflow that receives AI system descriptions, classifies risk, audits GDPR compliance, queries Core 2 for legal research, generates compliance documents, and produces a final report.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 85 | ✅ Complete | Gemini + Anthropic keys, DB, Redis, module URLs, cost limits, CORS |
| `src/api/main.py` | 455 | ✅ Complete | Assessment CRUD, approval endpoints, statistics, health check |
| `src/agents/base.py` | 153 | ✅ Complete | Base class with LLM init (Gemini/Claude), cost tracking, audit logging |
| `src/agents/supervisor.py` | 552 | ✅ Complete | LangGraph StateGraph with 8 nodes, conditional edges, interrupt_before for human-in-loop, resume() |
| `src/agents/risk_classifier.py` | 398 | ✅ Complete | Article 5 prohibited patterns, Annex III high-risk categories, LLM capability extraction |
| `src/agents/technical_assessor.py` | 424 | ✅ Complete | 5 GDPR checklist items (Arts 5, 6, 9, 22, 32), data flow analysis, DPIA determination |
| `src/agents/legal_research.py` | 389 | ✅ Complete | GraphRAG API integration with retry, fallback to LLM, entity extraction, article ranking |
| `src/agents/documentation_generator.py` | 443 | ✅ Complete | DPIA, ROPA, Conformity Assessment, Transparency Notice generation via LLM |
| `src/state/compliance_state.py` | 234 | ✅ Complete | LangGraph TypedDict state with reducers (append, merge_dicts) |
| `src/control_plane/governance.py` | 294 | ✅ Complete | Rate limiter, per-agent policies, cost caps, authorization |
| `src/control_plane/approval_queue.py` | 291 | ✅ Complete | Human-in-loop approval with risk assessment, expiry, approve/reject |
| `src/database/models.py` | 137 | ✅ Complete | AssessmentModel with to/from state dict conversion |
| `src/database/repository.py` | 113 | ✅ Complete | Full CRUD + list + count operations |
| `src/database/session.py` | 56 | ✅ Complete | Async SQLAlchemy with asyncpg |
| `src/cache/redis_client.py` | 239 | ✅ Complete | Async Redis client for session state caching |
| `src/utils/cost_tracker.py` | 131 | ✅ Complete | Token counting with tiktoken, daily/session cost limits |
| `src/utils/error_handling.py` | 112 | ✅ Complete | Custom exceptions: AgentError, RateLimitError, CostLimitError, HumanApprovalRequired, GraphRAGError |
| `src/utils/logging.py` | 52 | ✅ Complete | structlog JSON logging |
| `src/templates/dpia_template.md` | — | ✅ Exists | DPIA Markdown template |
| `src/templates/conformity_assessment_template.md` | — | ✅ Exists | Conformity assessment template |

#### LangGraph Workflow Topology
```
classify_risk → check_human_review → [conditional]
                                      ├─ needs_review → await_approval (INTERRUPT) → assess_gdpr
                                      └─ proceed → assess_gdpr
assess_gdpr → research_legal → check_conflicts → generate_docs → synthesize → END
```
- **Interrupt support**: `interrupt_before=["await_approval"]` enables workflow pause/resume
- **Resume API**: `supervisor.resume(session_id, decision)` continues paused workflows

#### Gaps / Issues
- **`configs/` directory is EMPTY** — No YAML/JSON config files present. All config is via environment variables (which is fine, but the dir is dead).
- **`scripts/` directory is EMPTY** — No utility scripts (e.g., seed data, run assessment).
- **Cost tracker model pricing** is for OpenAI models (gpt-4o, gpt-4o-mini) but app uses **Gemini** models. The `estimate_cost()` falls back to `{"input": 0.01, "output": 0.03}` for unknown models, so it won't crash but costs will be inaccurate.
- **tiktoken** may not have Gemini tokenizer — it falls back to `cl100k_base`, which provides approximate but not exact token counts for Gemini.
- Several **artifact directories** exist with garbled names: `srcagents/`, `srcapi/`, `srccontrol_plane/`, `srcstate/`, `srctemplates/`, `srcutils/`, `testsintegration/`, `testsunit/`, `datagolden/` — these appear to be accidental copies/artifacts and should be cleaned up.

---

## 3. Data Pipeline Status

### Raw Data (New_Data/)
Comprehensive legal corpus is present at the project root:

| Category | Files | Status |
|----------|-------|--------|
| AI Act Chapters | 13 text files (chapters 1-13) | ✅ Present |
| AI Act Recitals | Multiple recital files | ✅ Present |
| AI Act Annexes | 1 text file | ✅ Present |
| GDPR Chapters | 11 text files (chapters 1-11) | ✅ Present |
| GDPR Recitals | Multiple recital files | ✅ Present |
| CJEU Case Law | 20+ case files + index | ✅ Present |
| EDPB Guidelines | 23+ guideline files + index | ✅ Present |
| Enforcement Actions | 17+ enforcement files + index | ✅ Present |

### Problem: `core_2_knowledge_base/raw_data/` is EMPTY
The pipeline scripts expect raw data at `core_2_knowledge_base/raw_data/` (or the path configured in `config.py` as `raw_data_dir`). The actual data is at `New_Data/` in the project root.

**Fix needed:** Either:
1. Copy/symlink `New_Data/*` → `core_2_knowledge_base/raw_data/`
2. Update `core_2_knowledge_base/src/config.py` → `raw_data_dir: Path = Path("../New_Data")`

### Pre-Processed Data — Already Built ✅
The parsed data and vector embeddings have already been generated and are available:
- `parsed_data/` — 30 JSON files across 4 subdirectories
- `chroma_data/` — 7 collection JSON files with pre-computed embeddings
- `golden_tests/test_queries.json` — 6 golden test queries

This means **scripts 01-05 have already been run successfully at some point**. Only Neo4j loading (scripts 02, 04) would need to be re-run against a fresh Neo4j instance.

---

## 4. Infrastructure & DevOps

### Docker Setup

| Component | File | Status |
|-----------|------|--------|
| Master docker-compose | `docker-compose.yml` | ✅ 182 lines, all 3 modules + PostgreSQL + Redis + Neo4j + Prometheus |
| Core 1 docker-compose | `core_1/docker-compose.yml` | ✅ Standalone with PostgreSQL + Prometheus |
| Core 2 docker-compose | `core_2_knowledge_base/docker-compose.yml` | ✅ Standalone with Neo4j |
| Core 3 docker-compose | `core_3/docker-compose.yml` | ✅ Standalone with PostgreSQL + Redis |
| Core 1 Dockerfile | `core_1/Dockerfile` | ✅ Multi-stage UV build |
| Core 2 Dockerfile | `core_2_knowledge_base/Dockerfile` | ✅ Multi-stage UV build, copies chroma_data + parsed_data |
| Core 3 Dockerfile | `core_3/Dockerfile` | ✅ Multi-stage UV build, copies golden test data |
| Pipeline script | `pipeline.ps1` | ✅ Unified lifecycle: start / stop / restart-orch / kill-ports |

### Environment Variables (.env)

| Variable | Required By | Status |
|----------|-------------|--------|
| `GEMINI_API_KEY` | Core 3 | ❌ Template placeholder |
| `GOOGLE_API_KEY` | Core 2 | ❌ Template placeholder |
| `ANTHROPIC_API_KEY` | Core 3 (optional) | ❌ Template placeholder |
| `NEO4J_PASSWORD` | Core 2 | ❌ Template placeholder |
| `SLACK_WEBHOOK_URL` | Core 1 (optional) | ❌ Template placeholder |

**All API keys need real values before the pipeline can run.**

### Services Required

| Service | Port | Required By | Docker Image |
|---------|------|-------------|--------------|
| PostgreSQL (Core 3) | 5432 | Core 3 Compliance Agent | postgres:15-alpine |
| PostgreSQL (Core 1) | 5433 | Core 1 Monitoring | postgres:15-alpine |
| Redis | 6379 | Core 3 session caching | redis:7-alpine |
| Neo4j | 7687 (bolt), 7474 (http) | Core 2 Graph Store | neo4j:5-community |
| Prometheus | 9091 | Core 1 metrics (optional) | prom/prometheus |

---

## 5. Testing Coverage

### Core 1 Tests
| File | Type | Status |
|------|------|--------|
| `tests/unit/test_compliance.py` | Unit | ✅ Exists |
| `tests/unit/test_monitoring.py` | Unit | ✅ Exists |
| `tests/unit/test_client.py` | Unit | ✅ Exists |
| `tests/integration/test_api.py` | Integration | ✅ Exists |

### Core 2 Tests
| File | Type | Status |
|------|------|--------|
| `tests/test_extractors.py` | Unit | ✅ Exists |
| `tests/test_retrieval.py` | Unit | ✅ Exists (VectorStore, QueryModels tested) |
| `tests/conftest.py` | Fixtures | ✅ Exists |

### Core 3 Tests
| File | Type | Status |
|------|------|--------|
| `tests/unit/test_risk_classifier.py` | Unit | ✅ 219 lines, well-structured |
| `tests/unit/test_technical_assessor.py` | Unit | ✅ Exists |
| `tests/unit/test_legal_research.py` | Unit | ✅ Exists |
| `tests/unit/test_documentation_generator.py` | Unit | ✅ Exists |
| `tests/unit/test_control_plane.py` | Unit | ✅ Exists |
| `tests/integration/test_api.py` | Integration | ✅ Exists |

### Cross-Module Tests
| File | Type | Status |
|------|------|--------|
| `tests/integration/test_cross_module.py` | Integration | ✅ 478 lines, mock-based (Core 3→2, Core 3→1, Core 2→1) |

### Test Gaps
- ❌ **No end-to-end tests** against live services
- ❌ **No load/performance tests**
- ❌ **Golden test runner** (`core_3/data/golden/test_cases.json` has 10+ test cases but no automated runner in Core 3)
- ⚠️ Cross-module tests use mocks — won't catch real integration issues
- ⚠️ No `conftest.py` in Core 1 or Core 3 test directories

---

## 6. Cross-Module Integration

### Core 3 → Core 2 (Legal Research Agent → GraphRAG API)

| Aspect | Status | Details |
|--------|--------|---------|
| HTTP client in Core 3 | ✅ | `legal_research.py` uses httpx with tenacity retry |
| Endpoint called | ✅ | `POST /api/v1/graph/traverse` and `POST /api/v1/hybrid/reason` |
| URL configuration | ✅ | `GRAPHRAG_API_URL` env var, defaults to `http://localhost:8001` |
| Fallback on failure | ✅ | Falls back to LLM-based research if GraphRAG unavailable |
| Request/response format match | ✅ | Core 3 sends `GraphTraverseRequest`-compatible JSON, Core 2 returns expected format |

### Core 3 → Core 1 (Compliance Agent → Monitoring API)

| Aspect | Status | Details |
|--------|--------|---------|
| Client SDK | ✅ | `core_1/src/client/monitoring_client.py` |
| URL configuration | ✅ | `MONITORING_API_URL` env var, defaults to `http://localhost:8002` |
| Integration in agents | ⚠️ Partial | Client SDK exists but Core 3 agents don't currently call `MonitoringClient` to report decisions |
| Data format | ✅ | `AgentDecision` and `GraphRAGQuery` models match Core 1's API models |

### Missing Integration
- **Core 3 agents do not actively report to Core 1.** The `MonitoringClient` exists but is not wired into the agent code. After each agent decision (risk classification, GDPR audit), Core 3 should call `monitor.track_agent_decision()`. This is planned but not yet implemented.

---

## 7. What's Left To Run the Full Pipeline

### Priority 1 — Blockers (Must Fix)

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 1 | **API keys not set** | All | Add real `GEMINI_API_KEY`, `GOOGLE_API_KEY` to `.env` |
| 2 | **`raw_data/` empty** | Core 2 | Symlink or copy `New_Data/` → `core_2_knowledge_base/raw_data/`; OR update config path |
| 3 | **Neo4j needs data loaded** | Core 2 | Run `04_load_full_kg.py` against a running Neo4j instance to populate the knowledge graph from parsed_data |
| 4 | **`uv.lock` files** | All | Run `uv lock` in each module directory to generate lock files (Dockerfiles reference `uv.lock*`) |
| 5 | **Database initialization** | Core 1, 3 | First startup creates tables via `create_all()`, but verify PostgreSQL is accessible |

### Priority 2 — Should Fix Before Demo

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 6 | **Cost tracker pricing** doesn't include Gemini models | Core 3 | Add `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-2.0-flash` to `MODEL_PRICING` dict |
| 7 | **Core 3 doesn't report to Core 1** | Cross-module | Wire `MonitoringClient` into supervisor/agents to report decisions and query metrics |
| 8 | **Artifact directories** exist | Core 3 | Delete `srcagents/`, `srcapi/`, `srccontrol_plane/`, `srcstate/`, `srctemplates/`, `srcutils/`, `testsintegration/`, `testsunit/`, `datagolden/` |
| 9 | **ChromaDB config is dead code** | Core 2 | Remove `chroma_host`/`chroma_port` from config or add a comment explaining they're unused |
| 10 | **`validation/` module empty** | Core 2 | Only has `__init__.py`; validation logic is in pipeline scripts |

### Priority 3 — Nice to Have

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 11 | Add Alembic migrations | Core 1, 3 | Replace `create_all()` with proper migration management |
| 12 | Add `conftest.py` to Core 1 & 3 test dirs | Core 1, 3 | Create shared fixtures |
| 13 | Add end-to-end test | Root tests/ | Test full flow: create assessment → verify all agents run → check monitoring received data |
| 14 | Add Grafana dashboards | Core 1 | Uncomment Grafana in docker-compose.yml, add pre-built dashboards |
| 15 | Golden test runner for Core 3 | Core 3 | Create script to run `data/golden/test_cases.json` against live API |
| 16 | `configs/` and `scripts/` dirs empty | Core 3 | Remove or populate |

---

## 8. Recommended Execution Order

To bring the full pipeline from current state to running:

```
Step 1:  Set real API keys in .env
            GEMINI_API_KEY=<your-key>
            GOOGLE_API_KEY=<your-key>  (can be same Gemini key)
            NEO4J_PASSWORD=<your-password>

Step 2:  Fix raw data path
            Copy or symlink New_Data/* → core_2_knowledge_base/raw_data/

Step 3:  Generate lock files
            cd core_1 && uv lock
            cd core_2_knowledge_base && uv lock
            cd core_3 && uv lock

Step 4:  Start infrastructure (Docker)
            docker-compose up -d neo4j compliance-db compliance-redis postgres prometheus

Step 5:  Load knowledge graph into Neo4j
            cd core_2_knowledge_base
            uv run python scripts/04_load_full_kg.py

Step 6:  Start all API services
            docker-compose up -d  (or use .\pipeline.ps1 -Action start -Mode docker)

Step 7:  Verify health endpoints
            curl http://localhost:8000/health  (Core 3)
            curl http://localhost:8001/health  (Core 2)
            curl http://localhost:8002/health  (Core 1)

Step 8:  Run a test assessment
            POST http://localhost:8000/api/v1/assessments
            {
              "system_description": "Facial recognition system for employee attendance...",
              "system_type": "facial_recognition",
              "deployment_context": "employee_monitoring",
              "company_name": "Test Corp"
            }

Step 9:  Run tests
            cd core_1 && uv run pytest
            cd core_2_knowledge_base && uv run pytest
            cd core_3 && uv run pytest
```

---

## Appendix: File Counts by Module

| Module | Source Files | Test Files | Config/Infra Files | Data Files |
|--------|-------------|------------|--------------------|-----------| 
| Core 1 | 12 .py files | 4 test files | Dockerfile, docker-compose, pyproject.toml, prometheus.yml | — |
| Core 2 | 20+ .py files | 3 test files | Dockerfile, docker-compose, pyproject.toml, MEMORY.md | 30+ parsed JSON, 7 vector JSON, 6 golden tests |
| Core 3 | 18 .py files, 2 .md templates | 6 test files | Dockerfile, docker-compose, pyproject.toml | 1 golden test JSON (10+ test cases) |
| Root | — | 1 integration test | docker-compose.yml, .env, start/stop scripts, CLAUDE.md, README.md | New_Data/ (80+ files) |

**Total estimated lines of application code:** ~7,500+  
**Total estimated lines of test code:** ~1,500+
