# AlloyCode — Technical Reference

**Last updated:** 2026-04-13
**Covers:** Knowledge base schema · Rule catalog · Implementation status · Roadmap

---

## 1. Knowledge Base — the moat

The KG and vector store are the **rule corpus** for the scanner. Every detection rule (§3) maps to Articles / Obligations stored here. Do not throw this away — this is the single hardest thing in the repo to rebuild.

### 1.1 Current state (verified 2026-04-13)

| Store | Count | Notes |
|---|---|---|
| Neo4j nodes | **2,301** | Every node carries `Entity` super-label + one specialized label |
| Neo4j relationships | **4,423** | |
| Vector store docs | **2,198** | Custom JSON store (not ChromaDB — Python 3.14 compat; legacy folder name) |
| Vector collections | **7** | articles, obligations, recitals, definitions, concepts, rights, interpretive |
| Embedding model | `gemini-embedding-001` | 768-dim, cosine similarity |

### 1.2 Entity types (19)

| Label | Count | Label | Count |
|---|--:|---|--:|
| Obligation | 1,325 | AISystemType | 19 |
| Recital | 353 | Right | 19 |
| Article | 212 | Actor | 18 |
| Exemption | 96 | DataType | 17 |
| Definition | 90 | EnforcementAction | 15 |
| Concept | 47 | Annex | 13 |
| Chapter | 24 | Penalty | 6 |
| Guideline | 21 | RiskCategory | 4 |
| CaseLaw | 20 | Regulation | 2 |

### 1.3 Relationship types (top 13)

| Type | Count | Type | Count |
|---|--:|---|--:|
| REQUIRES | 1,008 | PART_OF | 270 |
| APPLIES_TO | 939 | PERMITS | 232 |
| CONTAINS | 602 | EXEMPTS | 96 |
| REFERENCES | 587 | DEFINES | 90 |
| INTERPRETS | 303 | CITES / PROHIBITS | 85 each |
| ENFORCES | 50 | COMPLEMENTS | 76 |

### 1.4 Raw data inventory (still on disk for rebuild)

89 files, 5.7 MB under [New_Data/](New_Data/):

| Category | Files | Entities |
|---|---|---|
| GDPR chapters | 11 `.txt` | 99 articles |
| GDPR recitals | 1 `.txt` | 173 recitals |
| EU AI Act chapters | 13 `.txt` | 113 articles |
| EU AI Act recitals | 1 `.txt` | ~180 recitals |
| EU AI Act annexes | 1 `.txt` | 13 annexes |
| CJEU case law | 17 `.txt` | 20 decisions |
| EDPB guidelines | 22 `.txt` | 22 guidelines |
| Enforcement actions | 18 `.txt` | 15 DPA decisions |

### 1.5 ID naming convention (unchanged)

| Pattern | Example | Meaning |
|---|---|---|
| `GDPR_ART_{N}` | `GDPR_ART_35` | GDPR Article |
| `AIACT_ART_{N}` | `AIACT_ART_14` | AI Act Article |
| `AIACT_ANNEX_{ROMAN}` | `AIACT_ANNEX_III` | AI Act Annex |
| `GDPR_DEF_{TERM}` | `GDPR_DEF_BIOMETRIC_DATA` | Definition |
| `OBL_{REG}_{NAME}` | `OBL_GDPR_LAWFUL_BASIS` | Obligation |
| `CJEU_C_{NUM}` | `CJEU_C_311_18` | Case law |
| `ENF_{NAME}` | `ENF_CLEARVIEW_AI` | Enforcement action |

### 1.6 Rebuild pipeline

Scripts in [knowledge_engine/scripts/](knowledge_engine/scripts/), run in order:

```
01_parse_raw_data.py            New_Data/*.txt → parsed_data/{legal,entities,interpretive}/*.json
02_load_structural_kg.py        → Regulation / Article / Annex nodes
02a_extract_structural_rels.py  → CONTAINS / REFERENCES edges
02b_validate_graph_local.py     → integrity check
03_extract_semantic.py          → concepts, principles
03b_extract_obligations.py      → 1,325 Obligation nodes
03c_extract_cross_regulation.py → GDPR ↔ AI Act bridges
03e_extract_concepts.py         → Concept nodes
03f_extract_rights.py           → Right nodes
03d_validate_full_graph.py      → validation
04_load_full_kg.py              → final state (2,301/4,423)
05_load_vector_store.py         → embeddings + JSON collections
07_run_golden_tests.py          → 6 golden queries
08_coverage_report.py           → coverage metrics
```

---

## 2. AI System Profile (the new orchestrator input)

The scanner's job is to produce this JSON artifact from a repo. Agents consume it instead of free-text.

```jsonc
{
  "scan_id": "scn_01H...",
  "repo": { "url": "...", "ref": "main", "commit": "abc123", "languages": ["python"] },
  "ai_components": [
    { "kind": "llm_sdk",        "evidence": [{"file": "src/chat.py", "line": 12, "import": "openai"}] },
    { "kind": "biometric_lib",  "evidence": [{"file": "src/verify.py", "line": 3, "import": "face_recognition"}] }
  ],
  "decision_surfaces": [
    { "endpoint": "POST /api/approve", "file": "src/api/approve.py", "line": 42,
      "calls_model": true, "has_human_review": false }
  ],
  "data_signals": {
    "pii_fields": ["email", "national_id"],
    "has_dpia_doc": false,
    "has_model_card": false,
    "has_data_card": false,
    "audit_logging": "partial"
  },
  "findings": [ /* see §3 */ ]
}
```

This is what every agent downstream reads.

---

## 3. Rule Catalog — Phase 1 MVP (10 rules)

Rules live in [orchestrator/src/code_analyzer/rules/](orchestrator/src/code_analyzer/rules/) as YAML (Semgrep-style; rule-as-data). Each maps to one or more KG obligations.

### 3.1 Rule definitions

| # | ID | Detects | Technique | Severity | Maps to |
|---|---|---|---|---|---|
| 1 | `AI-001` | Biometric / face / emotion recognition libs | Import scan: `face_recognition`, `deepface`, `mediapipe.solutions.face`, `dlib.get_frontal_face_detector`, `fer` | Critical | AIACT Art 5(1)(f,h) · Annex III §1 · GDPR Art 9 |
| 2 | `AI-002` | LLM / generative AI usage | Import scan: `openai`, `anthropic`, `google.generativeai`, `transformers`, `langchain`, `llama_index` | High | AIACT Art 50 · Art 52 |
| 3 | `AI-003` | User-facing AI decision endpoint | AST: FastAPI/Flask route returning model inference, no `human_review` / `approval` keyword in handler | High | AIACT Art 14 · GDPR Art 22 |
| 4 | `AI-004` | Missing transparency disclosure | File absence: no `model_card.md`, no `/disclose` endpoint, no "AI-generated" / "this is an AI" string in user-facing templates | Medium | AIACT Art 13 + 50 |
| 5 | `AI-005` | PII handling without DPIA marker | Regex/AST on schemas: fields matching `email\|ssn\|national_id\|biometric\|health`; no `dpia.md` / `DPIA.md` in repo root | High | GDPR Art 35 · Art 9 |
| 6 | `AI-006` | Training-data source opacity | File scan: `.csv` / `.parquet` / HuggingFace dataset refs in training scripts; no `data_card.md` / `DATASHEET.md` | Medium | AIACT Art 10 |
| 7 | `AI-007` | No logging / audit trail on AI decisions | AST: inference call not wrapped in `logger.*` / audit call within same function scope | Medium | AIACT Art 12 |
| 8 | `AI-008` | Social-scoring / behavioral-prediction keywords | Content scan in docstrings, README, identifiers: `social_score`, `trustworthiness`, `creditworthiness_by_behavior`, `predictive_policing` | Critical | AIACT Art 5(1)(c) |
| 9 | `AI-009` | Real-time biometric in public-space context | Co-occurrence: `AI-001` signal + keywords `cctv`, `public`, `street`, `realtime`, `live_stream` within 20 LOC or same file | Critical | AIACT Art 5(1)(h) |
| 10 | `AI-010` | No human-override mechanism for high-risk endpoint | AST: `AI-003` endpoint + no sibling `override` / `reject` / `appeal` route in same router | High | AIACT Art 14(4) |

### 3.2 Rule schema (YAML)

```yaml
# orchestrator/src/code_analyzer/rules/AI-001_biometric_libs.yml
id: AI-001
title: Biometric recognition library usage
severity: critical
technique: import_scan
languages: [python]
patterns:
  imports:
    - face_recognition
    - deepface
    - dlib.get_frontal_face_detector
    - mediapipe.solutions.face_detection
    - fer
maps_to:
  articles: [AIACT_ART_5, AIACT_ANNEX_III, GDPR_ART_9]
  obligation_anchors: [biometric_id, face_recognition, special_category_data]
confidence:
  base: 0.9
  dampeners:
    - { when: "file_matches: tests/|spec/", factor: 0.4 }  # test file → low confidence
    - { when: "import_unused: true", factor: 0.5 }
remediation: >
  Real-time remote biometric identification in publicly accessible spaces is
  prohibited by AI Act Art 5(1)(h) except for narrow law-enforcement carve-outs.
  If used in a closed / consented context, it remains a high-risk system under
  Annex III §1 and triggers GDPR Art 9 special-category requirements. Add a
  DPIA (GDPR Art 35) and a lawful basis under Art 9(2).
```

### 3.3 Confidence & suppressions

- Each finding carries a **confidence score 0.0–1.0** (base × dampeners).
- Suppressions via `.alloycode.yml` at repo root (pattern copied from Semgrep):
  ```yaml
  suppress:
    - rule: AI-001
      path: "tests/**"
    - rule: AI-002
      reason: "Internal tool, no user-facing transparency obligation"
      expires: 2026-12-31
  ```

### 3.4 Scanner architecture

```
orchestrator/src/code_analyzer/
├── __init__.py
├── ingest.py              # shallow clone, language detect, file index
├── profile.py             # aggregate findings -> AI System Profile
├── rules/                 # rule definitions (YAML)
│   ├── AI-001_biometric_libs.yml
│   └── ... (10 total)
├── scanners/
│   ├── base.py            # Scanner ABC, loads rules, emits findings
│   ├── import_scanner.py  # ast.Import / ast.ImportFrom walks
│   ├── ast_scanner.py     # AST pattern matching (routes, inference calls)
│   ├── file_pattern.py    # presence/absence of marker files
│   └── content_scanner.py # regex on docstrings, README, identifiers
└── mapper.py              # finding -> KG obligation via knowledge_engine
```

Folded into orchestrator (not a separate service) — fewer moving parts for a portfolio project. Extract later if it grows.

---

## 4. Orchestrator — revised agent contract

Each agent now consumes the **AI System Profile** (§2) instead of free-text.

| Agent | Before | After |
|---|---|---|
| Risk Classifier | "user typed a description" → LLM guesses tier | Reads `ai_components` + `decision_surfaces` → deterministic tier bands → LLM refines |
| Technical Assessor | Free-text GDPR gap analysis | Walks `data_signals` + detected PII fields → KG lookup for each gap |
| Legal Research | Generic `question` to knowledge_engine | `anchors[]` grounded in profile signals → focused RRF retrieval |
| Doc Generator | Writes DPIA / ROPA from scratch | Fills DPIA template with actual evidence (file:line) from profile |
| Supervisor | LangGraph orchestration | **Unchanged** — same state machine, richer state |

The LangGraph state machine in [orchestrator/src/agents/supervisor.py](orchestrator/src/agents/supervisor.py) and the human-in-loop approval queue ([orchestrator/src/control_plane/approval_queue.py](orchestrator/src/control_plane/approval_queue.py)) are retained. Only the input contract changes.

---

## 5. API surface — after Phase 1

### 5.1 Orchestrator (Port 8004)

| Endpoint | Method | Purpose | Status |
|---|---|---|---|
| `/api/v1/scans` | POST | Submit repo URL for scan | **NEW** |
| `/api/v1/scans` | GET | List scans | **NEW** |
| `/api/v1/scans/{id}` | GET | Scan state + findings report | **NEW** |
| `/api/v1/scans/{id}/profile` | GET | Raw AI System Profile JSON | **NEW** |
| `/api/v1/scans/{id}/findings` | GET | Flat findings list | **NEW** |
| `/api/v1/approvals` / `/approvals/{id}/decide` | GET/POST | Human-in-loop (retained) | Kept |
| `/api/v1/audit-log` | GET | Event stream per scan | Kept |
| `/api/v1/assessments*` | — | Old free-text endpoints | **DEPRECATED — removed** |

### 5.2 Knowledge_engine (Port 8001) — unchanged

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/vector/search` | POST | Semantic top-K |
| `/api/v1/graph/traverse` | POST | Multi-hop Cypher |
| `/api/v1/hybrid/search` | POST | RRF fusion |
| `/api/v1/hybrid/reason` | POST | Fusion + LLM synth (accepts new `anchors[]` param) |
| `/health` | GET | Health + node/doc counts |

---

## 6. Honest audit — why `monitor/` was removed

The pre-pivot audit rated `monitor/` at 85% complete. On honest re-review, for a **portfolio project**, it added weight without signal:

| Claim | Reality |
|---|---|
| Drift detection | Needs continuous traffic to show anything. Run 6 golden tests once → flat lines forever. |
| Bias detection | Chi-square on protected attributes requires a dataset with protected attributes. We didn't have one. |
| Article 14 compliance check | One rule: `if risk=="HIGH_RISK" and not human_reviewed: flag`. The orchestrator already enforces this at the workflow level. |
| Prometheus metrics | Collected but nothing consumed them. No Grafana wired. |
| Monitored "all systems" | Monitored only the orchestrator's own agents — circular. |

**What was removed:**
- `monitor/` service from [docker-compose.yml](docker-compose.yml)
- Entries in [start-all-modules.ps1](start-all-modules.ps1) / `stop-all-modules.ps1`
- `/monitoring` page from frontend + sidebar link
- Port 8002 is no longer in use
- The one useful idea — a per-scan audit log — lives in the orchestrator (`/api/v1/audit-log`)

Freed ~1,500 LOC, 2 Docker services (monitor + monitoring-postgres), and simplified the deploy story.

---

## 7. Implementation status (post-pivot snapshot)

| Component | Status | Notes |
|---|---|---|
| knowledge_engine (2,301 nodes) | ✅ Complete | No changes needed |
| Neo4j Aura instance | ⚠️ Live | Auto-pauses after 3 days on free tier; resumes on demand |
| Orchestrator LangGraph core | ✅ Kept | Input contract being reshaped |
| Orchestrator `code_analyzer/` module | ⬜ **Phase 1 — to build** | Scanner, rules, profile |
| 10 MVP detection rules | ⬜ **Phase 1 — to build** | Python-only AST/import/file-pattern |
| Finding → KG obligation mapper | ⬜ **Phase 1 — to build** | Uses `/hybrid/reason` with anchors |
| Frontend `/scan` page | ⬜ **Phase 1 — to build** | URL input → progress → findings |
| Frontend `/scans/[id]` report | ⬜ **Phase 1 — to build** | file:line anchored findings, article citations |
| Frontend `/knowledge` page | ✅ Kept | Force-directed KG explorer — demoable as-is |
| Old `/assessments/*` pages | 🗑️ To remove | Replaced by `/scans/*` |
| `monitor/` module + `/monitoring` page | ✅ Removed | See §6 |
| Tree-sitter / multi-language scanner | ⬜ Phase 2 | Python-first keeps Phase 1 small |
| VS Code extension | ⬜ Phase 3 | Depends on stable scan API |
| PDF report export | ⬜ Phase 2 | Markdown → weasyprint |
| Delta / on-save scan API | ⬜ Phase 2 | Prereq for VS Code extension |

---

## 8. Roadmap

### Phase 1 — Prove the thesis (current)

Goal: demoable end-to-end scan of a real public Python AI repo producing file:line findings mapped to KG articles.

- [ ] Scaffold `orchestrator/src/code_analyzer/`
- [ ] Ingest: `git clone --depth=1`, language detect, file index
- [ ] Implement 10 rules as YAML + 4 scanners (import, AST, file-pattern, content)
- [ ] Profile aggregator → `AISystemProfile` schema
- [ ] Mapper: findings → obligations via knowledge_engine `/hybrid/reason`
- [ ] Reshape agents to consume profile (not free-text)
- [ ] Frontend `/scan` + `/scans/[id]` pages
- [x] Delete `monitor/` module + `/monitoring` page
- [ ] Delete old `/assessments/*` pages
- [ ] Golden test: scan a known-violating fixture repo → assert expected findings

### Phase 2 — Make it good

- Expand to ~50 rules across tree-sitter (JS/TS/Go/Java)
- Full obligation catalog mapping (~1,325 obligations)
- LLM-generated narrative in report (post-detection)
- SBOM / dependency graph scanning (catch transitive AI usage)
- Scan history + diff view (what changed since last scan)
- PDF export

### Phase 3 — VS Code extension

- Delta scans on save / commit
- Diagnostics in Problems panel with file:line + article reference
- Code lens: "Run full compliance scan"
- Authentication for private repos
- Publish to VS Code Marketplace

---

## 9. Key risks (called out honestly)

| Risk | Mitigation |
|---|---|
| **False positives** — `import face_recognition` in a test file is noise | Dampener rules; `.alloycode.yml` suppressions; confidence score |
| **Signal → obligation mapping is soft** | KG provides grounded citations; every finding links to the Article; reviewer can judge fit |
| **Python-only limits demo repos** | Phase 1 scope accepted; tree-sitter in Phase 2 |
| **Neo4j Aura free tier auto-pauses** | Not worth fixing for a portfolio; resume on demand takes 30s |
| **LLM cost if narrative is per-finding** | Narrative is per-scan, not per-finding; batched single Gemini call |

---

*Supersedes and merges the prior `03_KB_DESIGN_AND_CONSTRUCTION.md` (KG schema) and `04_IMPLEMENTATION_AUDIT.md` (pre-pivot audit).*
