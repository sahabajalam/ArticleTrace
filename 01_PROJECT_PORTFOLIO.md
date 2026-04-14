# AlloyCode — Project Overview & System Architecture

**Last updated:** 2026-04-13
**Status:** Phase 1 (active) — pivoting from free-text assessment to static repo compliance scanning

---

## 1. What it is

AlloyCode is a **static compliance scanner for AI codebases** that maps detected code patterns to concrete EU AI Act and GDPR obligations. Point it at a GitHub repo; it returns a report of likely regulatory violations with **file:line anchors** and article citations.

Two entrypoints:

1. **Web UI** — paste a GitHub URL, run a one-shot scan, read the findings report.
2. **VS Code extension** (Phase 3) — scans on save / commit / schedule, surfaces findings as editor diagnostics.

---

## 2. Why this exists (and why the old direction was wrong)

**The old direction (shipped, now being retired):** user types a free-text description of their AI system into a form; five agents classify it against the EU AI Act. This had three fatal portfolio problems:

- Input is vibes — the user can be vague, wrong, or dishonest. The classifier has no ground truth.
- Every demo looks the same: a textbox, a loading spinner, a markdown report.
- No differentiator vs. any LLM-wrapper project.

**The new direction:** the input is **real code from a real repo**. Findings cite **real files and real lines**. The knowledge graph (2,301 nodes of EU AI Act + GDPR structure) becomes a **rule corpus**, not a research Q&A bot. Every claim in the report is grounded in an artifact the reviewer can open.

This is the gap in the AI-governance tooling landscape: Credo AI and Holistic AI collect self-reported answers; Fairlearn / AIF360 audit models at runtime with access to training data; Guardrails AI validates LLM outputs. **Nobody statically scans AI application code against regulatory obligations.**

---

## 3. Competitive landscape — what we borrow

Modern security / compliance scanners converged on a common shape. We borrow it directly.

| Tool | Pattern we borrow |
|---|---|
| Semgrep | Rule catalog as data (YAML), not hand-coded if/else |
| SonarQube | Confidence scoring + per-rule severity + suppressions via config |
| Snyk | Dependency / SBOM scanning; findings tied to fix suggestions |
| GitGuardian | Pre-commit and on-save delta scanning for low-friction UX |
| Trivy | Deterministic scanning first; LLMs only for narrative post-hoc |
| OpenSSF Scorecard | Repo hygiene signals that compose into a score |

**Core principle** shared across all of them: **LLMs are kept out of the detection hot path.** Static analysis is fast, cheap, explainable; LLMs are slow, expensive, and hallucinate. AlloyCode follows the same rule — deterministic scanners and KG lookups find the facts; Gemini only writes the human narrative at the end.

---

## 4. System architecture

Three live modules after the pivot (monitor is decommissioned).

```
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND (Next.js 16, Port 3000)                               │
│  Pages: /scan (new), /scans/[id], /knowledge, /approvals        │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTP fetch → localhost:8004
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (FastAPI, Port 8004)                              │
│  • code_analyzer/     — clone + scan + profile (NEW)            │
│  • agents/            — Risk Classifier, Technical Assessor,    │
│                         Legal Research, Doc Generator           │
│  • LangGraph workflow · Postgres · Redis · Gemini 2.5           │
└───────────────────────┬─────────────────────────────────────────┘
                        │ POST /api/v1/hybrid/reason
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE_ENGINE (FastAPI, Port 8001)                          │
│  • Neo4j: 2,301 nodes / 4,423 rels                              │
│  • Vector store: 2,198 docs across 7 JSON collections           │
│  • Hybrid retrieval (RRF) + multi-hop reasoning                 │
└─────────────────────────────────────────────────────────────────┘
```

**Decommissioned:** `monitor/` (was Port 8002). Drift/bias/Prometheus machinery provided no usable signal in a portfolio demo — see [02_TECHNICAL_REFERENCE.md](02_TECHNICAL_REFERENCE.md) §6 for the honest audit.

---

## 5. End-to-end data flow (one scan)

```
 [1] User pastes GitHub URL in /scan
        │
        ▼
 [2] Orchestrator: POST /api/v1/scans
        • Create scan_id, persist initial state, return 202
        • Background task picks up from here
        │
        ▼
 [3] code_analyzer.ingest
        • git clone --depth=1 → temp workspace
        • Detect language(s), framework(s), topology
        • Build file index + dep manifest (requirements.txt, pyproject, package.json)
        │
        ▼
 [4] code_analyzer.scan  ← 10 deterministic detection rules
        • Import-based scanners (biometric libs, LLM SDKs, …)
        • AST scanners (FastAPI/Flask routes, model-inference sites)
        • File-pattern scanners (model cards, DPIA docs, data cards)
        • Content scanners (prohibited-practice keywords)
        • Output: findings[] with {rule_id, file, line, excerpt, confidence}
        │
        ▼
 [5] code_analyzer.profile
        • Aggregate findings into "AI System Profile" JSON
        • Structured replacement for the old free-text description
        │
        ▼
 [6] Orchestrator LangGraph agents consume profile
        • Risk Classifier → EU AI Act tier (grounded in profile signals)
        • Technical Assessor → GDPR gap analysis
        • Legal Research → calls knowledge_engine with profile signals
        • Doc Generator → DPIA / ROPA / conformity scaffolds
        • (Human-in-loop approval retained for Critical severity)
        │
        ▼
 [7] Knowledge_engine.hybrid/reason
        • Vector search seeded on finding signal (e.g., "face_recognition lib")
        • Multi-hop graph traversal from matched Obligations
        • RRF fusion → Articles + Obligations + Recitals
        • Gemini synth → answer + citations (used for narrative only)
        │
        ▼
 [8] Report rendered at /scans/[id]
        • Each finding: file:line excerpt + severity + mapped articles
        •                         + suggested remediation + KG citations
        • Downloadable as JSON / markdown (PDF in Phase 2)
```

---

## 6. Integration contracts

**Frontend → Orchestrator**
```
POST /api/v1/scans              { repo_url, branch?, depth? }  → 202 { scan_id }
GET  /api/v1/scans/{id}         → scan state + findings
GET  /api/v1/scans              → list
GET  /api/v1/audit-log?scan_id  → per-scan event stream
POST /api/v1/approvals/{id}/decide  (unchanged — Critical findings pause for review)
```

**Orchestrator → Knowledge_engine**
```
POST /api/v1/hybrid/reason      { question, anchors[] }
  — anchors[] = detected signals (e.g., ["face_recognition", "biometric_id"])
  — forces retrieval to be grounded in observed code patterns, not prose embeddings
```

**Knowledge_engine internals** (unchanged)
```
/api/v1/vector/search · /api/v1/graph/traverse · /api/v1/hybrid/search · /api/v1/hybrid/reason
```

---

## 7. Scope of Phase 1 (what ships first)

| In | Out (for Phase 1) |
|---|---|
| GitHub public repo scan via URL | Private repo auth |
| Python-only scanners (AST + imports) | Tree-sitter / multi-language |
| 10 MVP detection rules | Full rule catalog |
| ~30 mapped obligations from KG | All 1,325 |
| One-pass full-repo scan | Delta scan / on-save |
| Web report UI | PDF export, VS Code extension |
| Orchestrator retains LangGraph + human-in-loop | Monitor module, drift/bias, Prometheus |

See [02_TECHNICAL_REFERENCE.md](02_TECHNICAL_REFERENCE.md) for the rule catalog, KG schema, implementation status, and full roadmap.

---

*Supersedes and merges the prior `01_PROJECT_PORTFOLIO.md` (multi-project portfolio pitch) and `02_ARCHITECTURE_AND_INTEGRATION.md` (pre-pivot architecture).*
