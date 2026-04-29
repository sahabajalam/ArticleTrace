# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **EU AI Regulatory Compliance Engine** - a multi-agent compliance platform for EU AI Act and GDPR assessments. The system consists of three core modules that work together:

| Module | Purpose | Port | Key Tech |
|--------|---------|------|----------|
| **core_3** | Compliance Agent (orchestrator) | 8000 | LangGraph, FastAPI |
| **core_2** | GraphRAG Legal Research | 8001 | Neo4j, ChromaDB |
| **core_1** | Monitoring & Governance | 8002 | PostgreSQL, Prometheus, Evidently |

## Architecture

```
User → Core 3 (Compliance Agent) → orchestrates 5 agents:
       ├── Risk Classifier (EU AI Act classification)
       ├── Technical Assessor (GDPR auditing)
       ├── Legal Research Agent → calls Core 2 GraphRAG API
       ├── Documentation Generator (DPIA, ROPA, Conformity)
       └── Supervisor (LangGraph orchestrator)

       All agent decisions → reported to Core 1 (Monitoring)
```

**Key Integration**: Core 3's Legal Research Agent makes HTTP calls to Core 2's `/api/v1/hybrid/reason` endpoint for multi-hop legal reasoning. Core 1 monitors both systems for compliance violations and drift.

## Common Commands

### Starting Services

```powershell
# Start all modules (Docker - recommended)
docker-compose up -d

# Or start individually
cd core_3 && docker-compose up -d
cd core_2 && docker-compose up -d
cd core_1 && docker-compose up -d
```

### Local Development (without Docker)

```powershell
# Install dependencies for a module
cd core_3 && uv sync

# Run the API server
cd core_3 && uv run uvicorn src.api.main:app --reload --port 8000
cd core_2 && uv run uvicorn src.api.main:app --reload --port 8001
cd core_1 && uv run uvicorn src.api.main:app --reload --port 8002
```

### Testing

```powershell
# Run all tests for a module
cd core_3 && uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_risk_classifier.py -v
```

### Linting & Formatting

```powershell
# Check linting (ruff)
uv run ruff check src/

# Format code
uv run ruff format src/
```

### Using UV Scripts (core_3 only)

```powershell
cd core_3
uv run test     # pytest
uv run lint     # ruff check
uv run format   # ruff format
uv run serve    # uvicorn server
```

## Module Structure

### Core 3: Compliance Agent (main orchestrator)

```
core_3/src/
├── agents/
│   ├── supervisor.py         # LangGraph orchestrator
│   ├── risk_classifier.py    # EU AI Act classification
│   ├── technical_assessor.py # GDPR auditing
│   ├── legal_research.py     # Calls Core 2 GraphRAG
│   └── documentation_generator.py
├── api/main.py               # FastAPI endpoints
├── control_plane/
│   ├── governance.py         # Rate limits, cost caps
│   └── approval_queue.py     # Human-in-loop approvals
├── state/compliance_state.py # LangGraph shared state
└── templates/                # DPIA, Conformity templates
```

### Core 2: GraphRAG Legal Research

```
core_2/src/
├── graph/
│   ├── schema.py             # Neo4j entity types
│   └── extraction.py         # Entity extraction from legal text
├── stores/
│   ├── graph_store.py        # Neo4j operations
│   └── vector_store.py       # ChromaDB embeddings
├── retrieval/
│   ├── engine.py             # RRF hybrid retrieval
│   └── reasoning.py          # Multi-hop reasoning
└── api/main.py
```

### Core 1: Monitoring & Governance

```
core_1/src/
├── compliance/
│   ├── eu_ai_act.py          # Article 14 monitoring
│   └── gdpr.py               # Article 22 monitoring
├── monitoring/
│   ├── drift.py              # Evidently drift detection
│   └── bias.py               # Chi-square bias detection
├── alerting/alert_manager.py # Slack/email alerts
├── client/monitoring_client.py # Client SDK for other modules
└── api/main.py
```

## Key API Endpoints

### Core 3 (Port 8000)
- `POST /api/v1/assessments` - Start compliance assessment
- `GET /api/v1/assessments/{id}` - Get assessment results
- `GET /api/v1/approvals` - List pending human approvals
- `POST /api/v1/approvals/{id}/decide` - Approve/reject

### Core 2 (Port 8001)
- `POST /api/v1/vector/search` - Vector similarity search
- `POST /api/v1/graph/traverse` - Neo4j graph traversal
- `POST /api/v1/hybrid/search` - Combined RRF search
- `POST /api/v1/hybrid/reason` - Multi-hop reasoning (used by Core 3)

### Core 1 (Port 8002)
- `POST /api/v1/monitoring/agent-decision` - Track agent decisions
- `POST /api/v1/monitoring/graphrag-query` - Track GraphRAG queries
- `GET /api/v1/compliance/status` - Compliance dashboard
- `GET /api/v1/compliance/violations` - List violations

## Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here  # Optional fallback
NEO4J_PASSWORD=your-neo4j-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
```

## Technology Decisions

- **LangGraph** for multi-agent orchestration (state machines, conditional routing)
- **UV** as package manager (modern, fast replacement for pip/poetry)
- **Ruff** for linting (replaces flake8, isort, black)
- **Pydantic v2** for settings and data validation
- **Neo4j** for knowledge graph (legal relationships)
- **ChromaDB** for vector embeddings (semantic search)
- **Evidently** for ML drift detection
- **Prometheus** for time-series metrics

## Agent Classification Logic

Risk Classifier categorizes systems into:
- **PROHIBITED** (Article 5): Social scoring, subliminal manipulation, emotion detection in workplace/education
- **HIGH-RISK** (Annex III): Biometrics, critical infrastructure, employment, credit scoring
- **LIMITED-RISK** (Article 52): Chatbots, deepfakes (transparency required)
- **MINIMAL-RISK**: No specific obligations

Human review is triggered when:
- Classification = PROHIBITED
- Classification = HIGH_RISK with confidence < 80%
- Conflicting outputs between agents

## Development Workflow

- For changes spanning 4+ files, outline the plan and affected files before implementing
- When fixing bugs, write a failing test that reproduces the issue first, then fix until green
- After implementing a feature, list edge cases and potential failure modes that need test coverage
- Changes to agent logic (risk_classifier, technical_assessor) require updating the golden test cases in `data/golden/test_cases.json`
- Cross-module changes (e.g., modifying Core 2 API that Core 3 calls) require testing both modules together
