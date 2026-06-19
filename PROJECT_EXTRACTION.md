# AlloyCode: Static Scanner for EU AI Act & GDPR Compliance

Static analysis scanner that maps AI codebases to concrete EU AI Act and GDPR obligations with file-and-line precision.

## What it does

Point AlloyCode at a public GitHub repo and it returns a structured compliance report. A deterministic scanner pass clones the repo, walks Python/JS/TS sources, and emits findings with file path, line number, code excerpt, severity, and the EU AI Act / GDPR articles each finding triggers. A LangGraph multi-agent layer (risk classifier, technical assessor, legal research, documentation generator) then enriches the findings with grounded narrative and scaffolds DPIA / ROPA / conformity documents.

For now it is a single-developer portfolio project — built to validate the architectural hypothesis that *code-grounded* compliance reporting beats free-text self-assessment for AI-governance tooling.

## Why I built it

The first version of this project was a free-text RAG Q&A bot — the user typed a description of their AI system into a textbox and five agents classified it. Three problems killed it: input was vibes, every demo looked the same, and there was no differentiator vs. any other LLM-wrapper project (see [`devlog/design-evolution/v02-static-scanner-pivot.md`](devlog/design-evolution/v02-static-scanner-pivot.md) §2).

The pivot to static scanning came from looking at the AI-governance landscape and noticing a gap: Credo AI / Holistic AI collect self-reported answers; Fairlearn / AIF360 audit runtime models with training-data access; Guardrails AI validates LLM outputs. **Nothing statically reads AI application code against regulatory obligations.** AlloyCode fills that gap.

## How it's built

- **Three live services**, two FastAPI backends + a Next.js frontend, wired through Docker Compose ([docker-compose.yml](docker-compose.yml))
- **Orchestrator** (Port 8004): scan API, code analyzer, LangGraph multi-agent workflow, Postgres + Redis ([orchestrator/src/](orchestrator/src/))
- **Knowledge engine** (Port 8001): Neo4j-backed regulatory graph with hybrid graph + vector retrieval ([knowledge_engine/src/retrieval/engine.py](knowledge_engine/src/retrieval/engine.py))
- **Frontend** (Port 3000): Next.js 16 + React 19 + Tailwind 4, with `react-force-graph-2d` for the citation network ([frontend/src/app/](frontend/src/app/))
- **Rules-as-data, Semgrep-style**: 10 YAML rule files in [orchestrator/src/code_analyzer/rules/](orchestrator/src/code_analyzer/rules/) loaded by [rule_loader.py](orchestrator/src/code_analyzer/rule_loader.py); adding a rule = adding a YAML file, no code change
- **Five scanner techniques**: import, AST, file-pattern, content, and co-occurrence ([orchestrator/src/code_analyzer/scanners/](orchestrator/src/code_analyzer/scanners/)). LLMs are kept out of the detection hot path so findings stay deterministic and explainable
- **Vector store consolidation**: migrated ChromaDB → JSON-backed store → Weaviate → Neo4j's native HNSW vector index, eliminating one external service (commit `661f990`)

## Impact / Scope

- 10 deterministic detection rules covering biometric libs, LLM usage, automated decision endpoints, transparency gaps, PII without DPIA, opaque training data, missing audit logs, prohibited practices, real-time biometric ID, and override gaps ([orchestrator/src/code_analyzer/rules/](orchestrator/src/code_analyzer/rules/))
- 5 scanner technique implementations, ~858 LOC total across [orchestrator/src/code_analyzer/scanners/](orchestrator/src/code_analyzer/scanners/) (`wc -l` on the scanners directory)
- 4 LangGraph agents: risk classifier, legal research, documentation generator, supervisor (~772 LOC across [orchestrator/src/agents/](orchestrator/src/agents/))
- 16 FastAPI route handlers across orchestrator + knowledge_engine (`grep -rE "@(app|router)\.(get|post|put|delete)"`)
- ~14,866 lines of project Python excluding venvs / vendor (`find ... -name "*.py" | xargs wc -l`)
- 99 test functions across 9 test files (`grep -rE "^\s*def test_" tests/`)
- [QUALITATIVE] Knowledge graph hosts ~2,301 nodes and 2,198 embedded obligations per [`devlog/SYSTEM.md`](devlog/SYSTEM.md) §2.1 — counts from prior runtime, not re-verified in this extraction
- [QUALITATIVE] Single-developer portfolio project; not yet shipped to other users
- [QUALITATIVE] Git history was rewritten during the recent restructure — current `git log` shows 4 squash commits, not the full development trail

## Story seeds

1. **Architecture pivot — free-text RAG to static repo scanning.** The project shipped first as a free-text classifier: user pastes an AI-system description, five agents return a tier. Three failures forced the pivot — vague input, identikit demos, no differentiator. Rebuilt around static code analysis with file:line anchors so every claim in the report points to an artifact the reviewer can open. The knowledge graph went from research-Q&A bot to rule-and-citation corpus. Documented in [`devlog/design-evolution/v02-static-scanner-pivot.md`](devlog/design-evolution/v02-static-scanner-pivot.md) §2.

2. **Vector store consolidation — ChromaDB → JSON → Weaviate → Neo4j.** Started on ChromaDB, found the operational footprint disproportionate to the workload. Tried a JSON-backed store for portability, then Weaviate for proper vector search, then realised the regulatory data was already a graph in Neo4j and Neo4j 5.x ships a native HNSW vector index. Collapsed two stores into one (commit `661f990` "Migrate vector store to Neo4j; consolidate scripts and docs"). One fewer service to deploy, one consistent query surface for hybrid graph + vector retrieval.

3. **Decommissioning the monitor module.** The original architecture had a fourth service for drift / bias / Prometheus monitoring on port 8002. Without continuous production traffic it produced no usable signal — empty dashboards in the demo. Cut it entirely rather than ship dead code; orchestrator + knowledge_engine + frontend is the live surface. Documented in [`devlog/design-evolution/v02-static-scanner-pivot.md`](devlog/design-evolution/v02-static-scanner-pivot.md) §4.

## Resume bullets

- Built static compliance scanner mapping Python/JS/TS code to EU AI Act and GDPR articles with file:line anchors (orchestrator/src/code_analyzer/scan.py)
- Designed Semgrep-style rules-as-data layer: 10 YAML rule files loaded at runtime, adding a rule requires no code change (orchestrator/src/code_analyzer/rule_loader.py)
- Shipped 5 scanner techniques (import, AST, file-pattern, content, co-occurrence) covering biometric libs, LLM SDKs, decision endpoints, and transparency gaps
- Migrated vector store from ChromaDB through Weaviate to Neo4j native HNSW index, collapsing two services into one (commit 661f990)
- Wired LangGraph multi-agent workflow across risk classifier, legal research, technical assessor, and documentation generator (orchestrator/src/agents/)
- Built hybrid graph + vector retrieval with Reciprocal Rank Fusion over Neo4j-backed regulatory corpus (knowledge_engine/src/retrieval/engine.py)
- Cut runtime services from four to three by decommissioning the monitor module after it produced no usable signal in demos
- Pivoted product from free-text RAG Q&A to static code scanning after three failure modes: vague input, identikit demos, no differentiator
- [QUALITATIVE] Containerised the whole stack with docker-compose and a Cloud Run deploy script (gcp.ps1) for one-command stand-up

## Tech

Python 3.11, FastAPI, LangGraph, LangChain, Gemini 2.5 (google-generativeai + google-genai), Neo4j 5 (graph + native vector index), Postgres (asyncpg + SQLAlchemy), Redis, tree-sitter, GitPython, Pydantic, structlog, httpx, Next.js 16, React 19, TypeScript, Tailwind 4, framer-motion, react-force-graph-2d, react-markdown, Docker, Cloud Run, uv

## Domain

AI governance, Regulatory compliance (EU AI Act / GDPR), Static code analysis
