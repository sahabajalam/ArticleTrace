---
version: "02"
title: Static-scanner pivot — free-text input replaced by repo scanning
status: implemented
derives_from: v01-baseline.md
proposed_date: 2026-02-15
decided_date: 2026-02-15
implemented_in:
  - 5210e51   # "Restructure modules and update frontend/infrastructure"
  - 661f990   # "Migrate vector store to Neo4j; consolidate scripts and docs"
  - orchestrator/src/code_analyzer/  # entire subtree
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - docs/README.md
  - docs/REFERENCE.md
  - orchestrator/src/code_analyzer/scan.py
  - orchestrator/src/code_analyzer/scanners/__init__.py
  - orchestrator/src/agents/supervisor.py
  - PORTFOLIO_ENTRY.md
  - gdpr context/backup/improve_v1.md
ai_guidance: |
  This proposal SHIPPED. It is the single biggest design change in the project's
  history. The user-facing input mechanism, the supervisor graph topology, and
  the role of the LLM in the detection path all changed. Read SYSTEM.md for the
  current state; this file is the decision record for why.
---

## 0. What this document is

`v02` documents the project's pivot from a **free-text** "describe your AI system" classifier (the `v01` baseline) to a **static compliance scanner** that ingests real GitHub repos, detects AI-system patterns deterministically, and maps each finding to EU AI Act + GDPR obligations with `file:line` anchors.

The pivot was forced by three problems with the `v01` design (see Status section below). It was the right thing to do; the cost was throwing away the user-facing input UI and the entire HITL approval loop. The knowledge engine (`core_2` in `v01` terms) survives the pivot largely intact — its API is now consumed by a `LegalResearchAgent` instead of the free-text RiskClassifier.

---

## Status

- **State:** implemented.
- **Decision date:** 2026-02-15 (approximate — the doc trail in `docs/README.md` and `PORTFOLIO_ENTRY.md` shows the decision crystallized in mid-February; the implementation rolled in across multiple unstaged edits before the first git import).
- **Implementation:** commits `5210e51` (module restructure) and `661f990` (vector-store migration). The new `orchestrator/src/code_analyzer/` subtree didn't exist before this pivot.
- **Supersedes:** `v01-baseline.md` for the user-facing input mechanism (§2), the supervisor graph topology (§1), and the monitor module (§1 — now decommissioned).
- **Superseded by:** none.

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | **Keep the free-text classifier; iterate on prompts.** | The fundamental problem is that the input is vibes. No prompt-engineering fixes "the user is vague / wrong / dishonest." There is no ground truth to verify against. |
| 2 | **LLM-output validation (Guardrails AI shape).** | A real market category, but already owned by Guardrails AI and the LLM-validators ecosystem. No differentiation. Also: doesn't use the regulatory knowledge graph as a moat; the KG becomes incidental. |
| 3 | **Continuous runtime monitoring (Fairlearn / AIF360 shape).** | Requires access to the trained model and live training data. Out of scope for a static-analysis portfolio project, and the market is mature. |
| 4 | **Self-reported compliance questionnaires (Credo AI / Holistic AI shape).** | Identical input problem to `v01` — self-reports are vibes. No differentiation. |
| 5 | **Static scan of AI application code against regulatory obligations.** ✅ | The gap nobody else fills. The knowledge graph from `v01` becomes a *rule corpus*, not a Q&A bot. Every finding cites a `file:line` artifact the reviewer can open. Deterministic detection on the hot path; LLM only for the post-hoc narrative. |

## Consequences

- ✅ **Findings are ground-truth-able.** Every claim in the report cites a file and a line. A reviewer can disagree by opening the file, not by debating the LLM's confidence.
- ✅ **The knowledge graph becomes a moat.** It stops being "the thing the chatbot consults" and becomes "the thing the rules are written against." Every detection rule maps to one or more Article/Obligation IDs.
- ✅ **Demo differentiation.** Free-text demos all look the same (textbox + spinner + markdown). Repo scans produce concrete output the reviewer can compare with their own knowledge of the codebase being scanned.
- ✅ **LLMs leave the hot path.** Scan latency is bounded by AST parsing + Neo4j lookups, not by an LLM round-trip per finding. Cost-per-scan is bounded by repo size, not by prompt length.
- ⚠️ **Need a rule catalog.** The free-text version offloaded "what to ask" to the user; the scanner version requires us to enumerate "what to look for." Phase 1 ships 10 MVP rules; the full catalog is open-ended.
- ⚠️ **Loses the conversational demo.** Recruiters who liked the chatbot UX won't see one anymore. (Trade-off accepted — the conversational demo wasn't the differentiator anyway.)
- ⚠️ **Phase-1 language scope is Python-only.** AST scanners are Python-specific; multi-language support (tree-sitter beyond Python) is Phase-2 work.
- ❌ **HITL approval pause goes away.** Static findings are deterministic and auditable; nothing to pause on. The `core_3` supervisor graph collapses from a branched 5-agent flow with HITL pause to a linear 4-node graph (`classify_risk → research_legal → generate_narrative → synthesize`).
- ❌ **Monitor module (`core_1`) is decommissioned.** Drift/bias/Prometheus require continuous production traffic that no portfolio demo has. The signal-to-effort ratio collapsed; the module was removed.

---

## 1. New architecture

Three services become two-and-a-half:

| Pre-pivot (v01) | Post-pivot (this v02) |
|---|---|
| `core_3` Compliance Agent (port 8000) | `orchestrator` (port 8004) — name and port changed; absorbs the `code_analyzer` subsystem. |
| `core_2` GraphRAG (port 8001) | `knowledge_engine` (port 8001) — renamed, internals unchanged. |
| `core_1` Monitoring (port 8002) | **decommissioned.** |

See [`../SYSTEM.md`](../SYSTEM.md) §1 for the current container diagram.

## 2. New input contract

```
POST /api/v1/scans              { repo_url, ref?: "main" }  →  202 { scan_id }
GET  /api/v1/scans/{id}         →  scan state + findings
GET  /api/v1/scans/{id}/findings  →  flat findings list
GET  /api/v1/scans/{id}/report  →  synthesized ScanReport
```

The body is a GitHub URL, not prose. Findings carry `{rule_id, file, line, excerpt, severity, confidence}`. The synthesized report includes the LLM-written narrative *and* the underlying structured findings, so the reviewer can read the prose or audit the evidence at will.

## 3. New detection pipeline ([`orchestrator/src/code_analyzer/scan.py`](../../orchestrator/src/code_analyzer/scan.py))

Strict scanner order (order matters — later scanners read shared state populated by earlier ones):

1. **`ImportScanner`** — module/library imports (e.g., `face_recognition`, `openai`, `anthropic`).
2. **`AstScanner`** — collects "decision surfaces" (function defs that look like model-inference call sites or decisioning code).
3. **LLM enrichment pass** — `review_decision_surfaces()` drops test/mock surfaces. Fail-open: if the LLM call fails, all surfaces are kept with regex verdicts.
4. **`AstRulesScanner`** — applies AST rules against the LLM-cleaned surfaces.
5. **`ContentScanner`** — content-based detection (PII fields, prohibited keywords).
6. **`FilePatternScanner`** — file-presence detection (model cards, DPIA docs, data cards).
7. **`CooccurrenceScanner`** — rules that need multiple of the above to fire together.

Phase-1 scope: 10 MVP rules; full catalog open-ended. Rules are loaded from data files via `rule_loader.load_rules()` — no hand-coded if/else.

## 4. New supervisor topology ([`orchestrator/src/agents/supervisor.py`](../../orchestrator/src/agents/supervisor.py))

```
classify_risk  →  research_legal  →  generate_narrative  →  synthesize  →  END
```

Linear. No HITL branch. The supervisor docstring explicitly notes: *"static scanners produce deterministic, auditable evidence, so there is no classification-uncertainty branch to pause on."*

- `classify_risk` — `RiskClassifierAgent`, deterministic, no LLM. Prohibited triggers: rule IDs `AI-008`, `AI-009`.
- `research_legal` — `LegalResearchAgent`, calls `POST /api/v1/hybrid/reason` on the knowledge engine.
- `generate_narrative` — `DocumentationGeneratorAgent`, Gemini synthesis, post-hoc only.
- `synthesize` — inline supervisor step, merges everything into the final `ScanReport`.

## 5. Borrowed patterns from the static-analysis ecosystem

The pivot adopts a shape that converged across modern static / compliance scanners:

| Tool | Pattern borrowed |
|---|---|
| Semgrep | Rule catalog as data (YAML / JSON), not hand-coded if/else. |
| SonarQube | Confidence scoring + per-rule severity + suppressions. |
| Snyk | Findings tied to fix suggestions. |
| GitGuardian | (Phase 3) pre-commit / on-save delta scanning for low-friction UX. |
| Trivy | Deterministic scanning first; LLMs only for narrative post-hoc. |

Core principle shared across all of them: **LLMs are kept out of the detection hot path.** ArticleTrace follows the same rule.

## 6. What's preserved from v01

- The knowledge graph schema (entity-aligned IDs, paragraph-level granularity, cross-regulation edges).
- The hybrid retrieval engine in the knowledge service (vector + graph + RRF + LLM synthesis).
- The LangGraph supervisor pattern (just with fewer nodes and no HITL).
- The Postgres + Redis backing on the orchestrator.

What changed is the input modality and the role of the LLM. The substrate — knowledge graph + multi-agent orchestration — is the same.

---

*This is the single most important design change in the project's history. Every later decision is downstream of this one.*
