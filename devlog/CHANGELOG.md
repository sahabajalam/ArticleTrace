---
title: ArticleTrace — Change Log
status: living
last_verified: 2026-06-19
companion_doc: devlog/SYSTEM.md
ai_guidance: |
  This is the LIVING change log — entries appended chronologically (newest
  first under the dated divider). Use it to recover the WHY behind any
  change. Each entry pairs with a section update in SYSTEM.md.
---

# ArticleTrace — Change Log

## Format

```
## YYYY-MM-DD — <short title>

**What:** <files / tables / modules / pages affected, concrete>
**Why:** <reason in one or two sentences>
**Impact on SYSTEM.md:** <section(s) updated; or "none — internal only">
**Refs:** <commit short hashes / migration numbers / PR refs if any>
```

---

## 2026-08-31 — Empty rule corpus can no longer pass as a clean scan (DL-035)

**What:** `orchestrator/src/code_analyzer/rule_loader.py` raises a new
`EmptyRuleCorpus` instead of returning `[]`; `scan.py` records `rules_loaded`
in the shared context and `profile.py` exposes it in `stats`; the scan detail
page shows **Rules loaded** as the first Coverage row, in red when zero or
missing; three regression tests in `tests/unit/test_scanner_gating.py`.

**Why:** An orchestrator started before the `04_AI_Governance_Scanner` →
`04_ArticleTrace` rename held the pre-rename `RULES_DIR`. `Path.glob()` on a
missing directory returns an empty iterator without raising, so `deepface`
scanned 152 files, matched zero rules, and reported MINIMAL_RISK / "No blocking
findings". A compliance scanner issuing a clean verdict because it loaded no
rules is the most dangerous output this system can produce, and nothing on
screen distinguished it from a genuine pass.

**Impact on SYSTEM.md:** Rule-loading section — `load_rules()` now has a
failure mode; `rules_loaded` added to the documented `stats` shape.

**Refs:** BUG_LOG entry 36 (DL-035)

---

## 2026-08-31 — documented eval commands made POSIX-first

**What:** `devlog/METRICS.md` §Reproducibility now leads with a macOS/Linux
invocation — `cd knowledge_engine && uv sync` then `./.venv/bin/python
scripts/NN_....py` — with the Windows `./.venv/Scripts/python.exe` form kept
alongside it as a labelled alternative rather than deleted. The `uv sync`
bootstrap is now explicit: there is a `uv.lock`, but a fresh clone has no
virtualenv at all, so the old text assumed a `.venv` that doesn't exist. Same
treatment for the §2 aside on running the full RAGAS metrics. Usage docstrings
updated to match in `knowledge_engine/scripts/07_run_golden_tests.py`,
`11_restore_from_jsonl.py`, `12_eval_three_mode.py` and
`13_eval_ragas_equivalent.py`. No script logic, golden-set entry, or recorded
metric value changed. `.github/workflows/golden-tests.yml` was checked and
needed no change — it runs `python scripts/...` against the `ubuntu-latest`
`setup-python` interpreter and never inherited the Windows path.

**Why:** Every documented route to reproducing the headline retrieval numbers
invoked `.venv/Scripts/python.exe`, which exists only on Windows. The project
now lives on macOS, so the reproducibility section could not be executed on
the machine that holds the project — making the numbers a claim rather than a
measurement, which is what NORTHSTAR Part I lever 2 exists to prevent.

**Verified:** the new §Reproducibility text was followed verbatim on macOS.
`uv sync` bootstrapped the environment; `./.venv/bin/python
scripts/07_run_golden_tests.py --dry-run` ran the full 25-query golden set
against the restored Aura instance and cleared the gate at **68% (17/25),
threshold 60%** — matching the recorded figure, no metric rewritten. The
`knowledge_engine` unit suite is green at **65 passed**.

**Note — `uv sync` and the test suite:** `pytest` sits in
`[project.optional-dependencies] dev`, so a bare `uv sync` *removes* it from an
existing venv. That is correct for the eval scripts (they need runtime deps
only, which is what §Reproducibility documents), but running the unit tests
needs `uv run --extra dev pytest tests/`. Recorded here rather than in
`METRICS.md`, which is scoped to reproducing metrics, not to test bootstrapping.

**Impact on SYSTEM.md:** none — documentation and invocation only.

**Refs:** issue #493173; proposal `devlog/design-evolution/v06-durable-kg-and-reproducible-eval.md` §2.4
(corrected in place — it wrongly listed the CI workflow among the Windows-path offenders; §2.4 now marked delivered,
the document stays `proposal` because §2.1 and §2.5 are outstanding).

---

## 2026-08-31 — keep-alive ping retired; weekly self-verifying KG backup in its place

**What:** Deleted `.github/workflows/keep-aura-alive.yml`. Added
`.github/workflows/backup-knowledge-graph.yml` — Monday 02:00 UTC plus
`workflow_dispatch`, runs `knowledge_engine/scripts/10_backup_to_jsonl.py` and
uploads `knowledge_engine/backups/` as a 90-day artifact
(`if-no-files-found: error`, uploaded only on success, so an artifact that
exists is one that passed the self-check). Dumps stay out of git;
`knowledge_engine/backups/` was already gitignored. Reworked
`10_backup_to_jsonl.py` around a new `verify_dump()`: after writing
`meta.json` the script re-reads both JSONL files off disk and fails unless the
complete-line counts equal `node_count` / `rel_count`, the last record parses
as JSON, and no file ends mid-write. The check runs on **every** invocation,
not only in CI, and `--verify <TS>` re-checks an existing dump. The
`from src.config import settings` import moved inside `run_backup()` so
verification needs no credentials. New `knowledge_engine/tests/
test_backup_verification.py` (16 tests) covers dropped lines, byte-level
truncation, count mismatch, emptied/missing/corrupt files and the CLI.

**Why:** Aura Free deletion is policy-based, not activity-based — a
`MATCH (n) RETURN count(n)` ping does not reset the 30-day timer. The ping was
added after the first deletion (DL-025), and the graph was destroyed a second
time anyway (`e8097dda`, found dormant 2026-08-31). DL-025's own follow-up
already said to retire it and schedule a backup; that was never actioned. A
workflow with a measured 0% success rate is deleted rather than disabled,
because a disabled-but-present workflow still looks like protection. The
verification exists because an unverified backup is the repo's dominant
failure class — a component reporting success while doing nothing (DL-003,
DL-019, DL-020, DL-023, DL-025). Implements
`design-evolution/v06-durable-kg-and-reproducible-eval.md` §2.3; the rest of
v06 is still `proposal`.

**Verified:** Full dump against the live instance produced
`20260831_144857` — 2,301 nodes / 4,423 rels / 1 vector index, self-check
passed, exit 0. `--verify` on the 102 MB `20260619_183622` dump passes. A copy
of that dump with 200 bytes chopped off `rels.jsonl` fails with all three
problems named (cut off mid-record; 4,421 lines vs 4,423, off by -2; last
record not valid JSON) and exit 1. `knowledge_engine/` suite: 65 passed.

**Impact on SYSTEM.md:** none — no architecture, schema or API change. §6
already links `.github/workflows/` generically rather than by file.

**Refs:** `devlog/BUG_LOG.md` DL-025; `devlog/DEPLOYMENT.md` lesson 26
(rewritten — it pointed at the deleted workflow); `devlog/NORTHSTAR.md` Part
III P0 item moved to `## Resolved`.

---

## 2026-08-31 — `.env` anchored to the repo root; credentials fail loudly at startup

**What:** Both services resolved `env_file=".env"` relative to the process
working directory, so anything launched from `knowledge_engine/` or
`orchestrator/` read no env file at all and silently fell back to field
defaults. Added `knowledge_engine/src/env.py` and `orchestrator/src/env.py`
(intentional duplicates — separate images, no shared package) exposing
`find_repo_root()` / `find_env_file()` / `ENV_FILE` / `require_credential()`,
all derived from `__file__` and anchored on the `.git` marker, so a stray
per-service `.env` can no longer shadow the root one. Both `config.py` modules
now use the absolute `ENV_FILE`; `orchestrator/src/config.py` also moved off the
deprecated inner `class Config` to `SettingsConfigDict`. Real environment
variables still outrank the file (Cloud Run depends on it). Missing credentials
now fail at startup with the variable name and the expected file:
`google_api_key` is validated on `Settings` (was defaulting to `""` and
surfacing as a Google 401 several frames away), `gemini_api_key` gains an
empty-string check alongside its existing `Field(...)`, and `NEO4J_PASSWORD` is
checked in `GraphStore.__init__` rather than on `Settings` so the module stays
importable in tests that never connect. New tests:
`knowledge_engine/tests/test_config.py` (14) and
`orchestrator/tests/unit/test_config.py` (10) cover CWD-independent resolution,
env-var-over-file precedence, and the named-variable failures.

**Why:** DL-025 step 2 — the root `.env` was updated while a stale
`knowledge_engine/.env` still pointed at a dead Neo4j instance, and the service
kept running against it. Same root cause as DL-005's confusing startup failure.

**Impact on SYSTEM.md:** none — configuration loading is internal and not
described there.

**Refs:** issue #815755; `knowledge_engine/src/{env,config}.py`,
`knowledge_engine/src/stores/graph_store.py`, `orchestrator/src/{env,config}.py`

---

## 2026-08-31 — Frontend rebuilt around the trace; 2,438 → 704 lines

**What:** Replaced the frontend with two screens built for one objective —
make the code→article trace inspectable, and be honest about coverage.

**Deleted as decoration:** `/knowledge` fetched nothing at all; it rendered
hardcoded constants (`TOTAL_NODES = 2301`) that would have kept reporting those
figures however the graph changed. `KnowledgeGraph.tsx` (405 lines, with a
`react-force-graph-2d` dependency) was never imported. `lib/markdown.ts` (165
lines) was never imported. `framer-motion`, `react-markdown` and `remark-gfm`
were installed and never used. Sidebar and topbar navigated three routes, two
of which now don't exist. **Runtime dependencies: 10 → 3** (`next`, `react`,
`react-dom`).

**Built:** `/` starts a scan and lists scans (absorbing `/scans/new`).
`/scans/{id}` shows risk posture, findings, and coverage. A finding expands to
its full chain — `file:line`, source excerpt, `└─▶` mapped articles rendered
readably (`AIACT_ART_5` → "AI Act Art. 5"), remediation — with confidence
always visible and the demotion reason shown when triage lowered it.

**Surfaces what the backend gained today and the old UI ignored entirely:**
`triage`, `dampened_triggers`, `llm_triage`, `manifest_scan` and
`source_read_errors` had zero references in the old code. The new Coverage
panel reports files scanned vs total, manifests read, triage status including
"not run" and the cost cap, and any unreadable source — so "no findings" is
distinguishable from "never looked", the failure mode behind DL-019, DL-020,
DL-027 and DL-028. An unreachable backend says so rather than rendering an
empty list that reads as "no scans".

**Verified** against the live deepface scan: 87 findings, `HIGH_RISK` with
`dampened_triggers: [AI-009]`, triage 40 reviewed / 25 demoted / 47 beyond cap,
three manifests read. Production build clean, TypeScript passing.

**Impact on SYSTEM.md:** §5 rewritten.

---

## 2026-08-31 — Rename follow-through: local directory, venvs, stale path claims

**What:** Completed the rename below the repository level. Local directory
`Portfolio/04_AI_Governance_Scanner` → `04_ArticleTrace` (keeps the siblings'
`NN_Name` convention). Both virtualenvs were rebuilt: uv writes absolute paths
into console-script shebangs, so `pytest` failed with `bad interpreter` the
moment the directory moved — `uv sync` regenerates them. Also updated the
Alloygraph project record, whose `repo_path` pointed at the old directory.

**A stale claim this surfaced.** SYSTEM.md §7 stated *"EU_AI_GDPR — repo
directory name only"*. That was already wrong before today: the directory had
been `04_AI_Governance_Scanner` for some time. The glossary row now says so
explicitly rather than quietly substituting the new name, since a doc that
silently corrects itself teaches nothing about how it drifted.

**Verified after the move:** 152 tests green, benchmark 9/9, git remote and
history intact, tree clean.

**Impact on SYSTEM.md:** §7 Glossary — EU_AI_GDPR row marked stale with the
reason; the naming paragraph no longer cites a directory name at all.

**Refs:** v08-naming.md.

---

## 2026-08-31 — Renamed AlloyCode → ArticleTrace

**What:** Third and final canonical name. Decision record:
[`design-evolution/v08-naming.md`](design-evolution/v08-naming.md). 36 files
updated, 130 live references; NORTHSTAR Part IV's rename refusal is recorded
as overridden once and then reinstated, now citing v08 so a fourth rename must
argue against evidence.

**Why AlloyCode failed:** three live collisions — `alloycode.com` is an
operating software consultancy trading under the exact name; Alloy is an
identity/AML fintech shipping "Agentic AI for KYC and Compliance" with a
trademark in the software class; and Alloy is MIT's formal specification
language used for code analysis. Worst possible position for a static analysis
tool about AI compliance.

**Why not AnnexIII (or AnnexScan/AnnexTrace):** the rule catalog makes 26
regulatory references and **exactly one is Annex III**. The most-referenced
provision is Art 5, and GDPR — roughly half the corpus — has no annexes. An
`Annex*` name would describe 1/26th of the product. `AnnexIII` also fails on
package ergonomics, has both domains taken, and could never rank against
EUR-Lex for its own name.

**Why ArticleTrace:** 25 of 26 references are Articles, the unit both
regulations share; "trace" names the actual differentiator (every finding
traceable from `file:line` to a cited Article) and is on-domain vocabulary via
AI Act Art 12; and it was verified free on PyPI, npm, GitHub, `.com` and
`.dev`.

**Compatibility kept:** `.alloycode.yml` lives in *users'* scanned repos, so it
is a public interface. The loader now accepts `.articletrace.yml` first and the
old name as fallback — renaming outright would have silently stopped honouring
existing suppression configs. Dated CHANGELOG/BUG_LOG entry bodies keep the old
name deliberately: they record what was true when written.

**Impact on SYSTEM.md:** naming paragraph and §7 Glossary — full lineage
Aegis → AlloyCode → ArticleTrace with the reason each was retired.

**Refs:** v08-naming.md; NORTHSTAR Part IV.

---

## 2026-08-31 — Open-source readiness pass

**What:** Prepared the repository for public release. `LICENSE` (Apache-2.0 —
patent grant and explicit contribution terms matter more than MIT's brevity for
a tool making regulatory claims), `NOTICE` separating code licensing from
redistributed EU content, [`CORPUS.md`](../CORPUS.md) documenting every
dataset's provenance and reuse terms, `.env.example`, a not-legal-advice
disclaimer, and a Quickstart a stranger can actually complete.

**Corpus licensing, researched not assumed.** EUR-Lex material (AI Act, GDPR)
is reusable under Commission Decision 2011/833/EU with CC BY 4.0 applied by the
Publications Office — attribution given and modifications indicated, as
required. **The EDPB's own terms could not be retrieved** (their legal-notice
URL 404s), so `parsed_data/interpretive/edpb_guidelines.json` is flagged in
CORPUS.md §3 as unverified, with two documented resolutions (verify, or exclude
— it is 56 of 2,198 documents and no golden test depends on it). Assuming the
general EU pattern applied would have been a guess about someone else's rights.

**Untracked `legacy_prototypes/`** — 208 files, 14 MB of raw regulatory source.
It was listed in `.gitignore` (line 20) and NORTHSTAR records it as removed
"from repo surface", but it had been tracked the whole time: the same
tracked-despite-ignored class as `.env` and the `.pyc` files, from the same
commit lineage. Nothing reads it (scripts 02–05 build from `parsed_data/`;
only script 01 needs raw text), so removing it costs nothing and shrinks the
least-verified redistribution surface to zero.

**README corrected.** The Live-demo section advertised three Cloud Run URLs
including one promising "returns the live KG counts" — it returns
`neo4j: disconnected`. Replaced with an honest Status section. The clone URL
pointed at a repository name two renames stale. The new Quickstart documents
the previously-undocumented knowledge-graph build (scripts 02/04/09 + index
creation from the shipped `parsed_data/`), which is what makes self-hosting
possible at all; every file and script it references was verified to exist.

**Impact on SYSTEM.md:** none — packaging and documentation.

**Refs:** Commission Decision 2011/833/EU; CORPUS.md; 152 tests green,
benchmark 9/9.

---

## 2026-08-31 — v08 P1 retrieval arms: entity recall 25% → 62.5%, measured by ablation

**What:** Shipped both NORTHSTAR Part III P1 items and measured them
independently. **(1) Entity-name index** — a Neo4j full-text index over
`:Entity(name)` fused as a third RRF arm, with Lucene-reserved characters
stripped from the question (a stray `?` or `:` is a parser error, not a bad
match) and sub-3-character tokens dropped. **(2) Cross-regulation expansion** —
one `COMPLEMENTS` hop off the top vector hits. New ablation runner
[`14_eval_p1_arms.py`](../knowledge_engine/scripts/14_eval_p1_arms.py) scores
the golden set under baseline / name-only / complements-only / both.

**Result** (full table in [`METRICS.md`](METRICS.md) §6): entity recall@15
**25% → 62.5%**, pass rate **68% → 76%**, multi-hop **46% → 63%**, single-hop
**86% → 100%**, citation recall **unchanged at 81.8%**, out-of-scope correctly
unchanged. NORTHSTAR estimated ~46% entity and ~55% multi-hop; both exceeded.
The 9 recovered entities are exactly the short-label category nodes §4
predicted — including `PEN_AIACT_PROHIBITED`, which has no embedding at all
and was unreachable by vector search at any budget.

**COMPLEMENTS did not do what it was proposed for, and that is recorded rather
than glossed.** It was meant to close `GT_02` (7/8 → 8/8 citations); `GT_02`
still misses both citations in every configuration, and run alone COMPLEMENTS
changes no metric. It is kept for a different, measured reason: the name arm
displaces `GDPR_ART_22` out of top-15 on `GT_18` (citation 27/33 → 26/33), and
COMPLEMENTS restores it. The pair is strictly better than either alone — full
entity gain at zero citation cost. That justification is contingent on the
interaction, so the ablation must be re-run if the name arm is retuned.

**Impact on SYSTEM.md:** none yet — retrieval internals; §6 of METRICS.md
carries the detail. 77 knowledge_engine tests green (12 new).

**Refs:** METRICS.md §6; `golden_tests/p1_ablation_20260831.json`;
NORTHSTAR Resolved.

---

## 2026-08-31 — Credentials rotated; CI green for the first time

**What:** Owner rotated the exposed Gemini key and the Neo4j credentials.
Verified the rotation cryptographically rather than on trust — SHA-256 of each
current value compared against the published value recovered from the
pre-purge bundle: **all five differ**, and Alloygraph now holds a separate key
that is also not the exposed one. Tested both credentials live before storing
them (DL-017's lesson), then set `GOOGLE_API_KEY`, `NEO4J_URI`, `NEO4J_USER`,
`NEO4J_PASSWORD` as repo secrets, replacing three that dated from 2026-04-29
and pointed at an instance deleted twice over.

**Result: both workflows pass.**
- `Detection benchmark` — 9/9, no secrets required (v07 T0).
- `KE Golden Tests + 3-mode Eval` — first success on record. CI reproduces
  `METRICS.md` **exactly**: hybrid_rrf 27/33 (81.8%), vector_only 24/33
  (72.7%), graph_only 7/33 (21.2%), entity recall 6/24 / 10/24 / 0/24, pass
  rate 17/25 (68%).

That is the third independent reproduction of the headline retrieval numbers
— as recorded (pre-deletion), locally after the JSONL restore, and now on
GitHub runners against the restored Aura instance. The metric is no longer a
claim resting on one machine.

**Impact on SYSTEM.md:** none — credentials and CI configuration only.

**Refs:** runs 33422415468 (golden tests), 33421705215 (benchmark); DL-032,
DL-033.

---

## 2026-08-31 — Fix DL-033: the keyless benchmark required a key at import

**What:** The detection benchmark's first CI run failed with
`ValidationError: gemini_api_key Field required` before scanning anything.
`scan.py` imported `llm_ast_reviewer` at module scope, which imports
`src.config`, whose Settings requires a Gemini key — making the entire scanner
pipeline unimportable without one, including the `use_llm=False` path that
never calls an LLM. Made the import lazy (matching `finding_triage`), verified
against a real keyless clone, and added a regression test that asserts on
`scan.py`'s module-level source.

**Why it hid locally:** `.env` sits in the repo root, and v06 §2.2 had just
made config resolution find it from any working directory — so the local mask
was airtight. CI was the only environment that could see it.

**Impact on SYSTEM.md:** none — import-time only, no behaviour change.

**Refs:** BUG_LOG DL-033; run 33421479013.

---

## 2026-08-31 — CI triage: golden-tests red since before this session (DL-032)

**What:** Diagnosed the `KE Golden Tests + 3-mode Eval` failure. Pre-existing —
the 2026-08-30 scheduled run failed identically before any of this session's
work. Two gaps: `GOOGLE_API_KEY` was never added as a repo secret, and the
three `NEO4J_*` secrets date from 2026-04-29, predating **both** Aura
deletions, so they point at an instance that no longer resolves. Bumped
deprecated `actions/checkout@v4` / `upload-artifact@v4` / `cache@v4` to
v7/v7/v6 across all three workflows, and gave the detection benchmark a
push-to-main trigger so it gates direct pushes, not only PRs.

**Not done, deliberately:** installing the secrets. The Gemini key in `.env`
is the one that was published in git history; it must be rotated before being
stored anywhere. Owner action.

**Also settled — DL-025's open question.** `keep-aura-alive.yml` **succeeded**
on 2026-08-25, 08-27 and 08-29 and the instance was deleted regardless. Aura's
deletion is policy-based on idleness; a keep-alive query does not reset it.
The workflow was green while the database it protected was destroyed —
retroactive proof that v06 §2.3 was right to retire it for a verified backup.

**Impact on SYSTEM.md:** none — CI/config only.

**Refs:** BUG_LOG DL-032; runs 33316550844 (pre-existing failure), keep-alive
runs 2026-08-25/27/29.

---

## 2026-08-31 — Orchestrator test suite collects again (DL-031)

**What:** 5 of 7 orchestrator unit-test modules had failed collection since
commit `5210e51`, importing `src.state.compliance_state` and
`src.control_plane.approval_queue` — removed by the v02 static-scanner pivot
and the v04 HITL decision respectively. Only 22 tests ran; the rest were
invisible. Salvaged `test_control_plane.py` (15 governance tests still match
the live API; dropped only the `approval_queue` half), deleted the four that
test the v01 free-text classifier, and added
[`test_scan_state.py`](../orchestrator/tests/unit/test_scan_state.py) covering
what was worth keeping against the current API: state construction, the
deterministic compliance score, and the classification tiers T2's tests don't
reach. **`pytest tests/unit`: 74 passed, 0 collection errors.**

**Why:** Closes the last DL-027 follow-up. A suite that silently shrinks to
"whatever still imports" is why the pipeline critic could approve work whose
tests had never run.

**Impact on SYSTEM.md:** none — test-only.

**Refs:** BUG_LOG DL-031; v02 pivot, v04 HITL decision.

---

## 2026-08-31 — v07 T2 delivered: confidence-aware verdicts + LLM triage (judge, never detector)

**What:** **(1) Confidence-aware escalation** — a prohibited trigger sets
PROHIBITED only at finding confidence ≥ 0.5; test/example-dampened evidence
(×0.4 → ~0.36) lands in the new `RiskPosture.dampened_triggers` and caps at
HIGH_RISK with an explicit "capability present; verify deployment" reason.
Closes DL-027's open follow-up: deepface now classifies **HIGH_RISK with
dampened AI-009** instead of PROHIBITED-via-a-tests/-file (verified live). A
test pins the dampener↔threshold relationship. **(2) LLM finding triage**
([`finding_triage.py`](../orchestrator/src/code_analyzer/finding_triage.py),
IRIS-shaped per v07 §1.3): reviews ≤40 findings/scan, may CONFIRM or DEMOTE
(halve confidence + reasoned `finding.triage` annotation), structurally cannot
create/delete/boost — a hallucinated verdict can only quiet a scan, and
demotion below the T2.1 bar can defuse a dubious PROHIBITED but nothing the
LLM says can cause one. Fail-open with a receipt in `stats.llm_triage`
(ok/skipped/failed, reviewed/demoted/capped — the cap is loud). Live deepface
run: 40 reviewed, 25 demoted with stated reasons (`experiments/`,
`benchmarks/` directories — judgments path dampeners cannot make), 47
capped-out and reported.

**Why:** v07 §1.4 — capability evidence and deployment inference must not be
conflated by a trigger that ignores confidence; and the field's result (IRIS)
is LLM around the deterministic engine, not inside it.

**Benchmark unaffected** (deterministic path, 9/9); 50 orchestrator unit
tests green (9 new in test_t2_verdicts.py).

**Impact on SYSTEM.md:** §3.1 (triage in the scan flow), §3.2 (classifier
row: confidence-gated triggers, dampened_triggers).

**Refs:** v07 T2 delivery note; DL-027 follow-up #1 closed (the stale-test-
modules follow-up remains open).

---

## 2026-08-31 — v07 T1 delivered: manifests, notebooks, string signals — 9/9 benchmark

**What:** The three T1 signal-widening items, each landed against a waiting
benchmark fixture that flipped XFAIL→XPASS→promoted. **(1) Manifest
cross-referencing** — `ImportScanner._manifest_pass` parses
requirements*.txt / pyproject.toml (PEP 621 + poetry) / package.json and
matches the same rule patterns with dist↔import normalisation
(face-recognition↔face_recognition, google-generativeai↔google.generativeai,
dlib↔dlib.get_frontal_face_detector); declared+imported boosts, declared-only
emits a 0.7×-dampened finding; parse failures surface in
`stats.manifest_scan.errors`. **(2) Notebook extraction** —
[`source_reader.py`](../orchestrator/src/code_analyzer/source_reader.py)
turns `.ipynb` code cells into a parseable stream (magics commented in place,
5 MB raw budget) consumed by Import/Ast/Content scanners; unreadable
notebooks land in `stats.source_read_errors`. **(3) String patterns** —
`strings:` on any rule, scanned in code files only; AI-002 gains HF
`from_pretrained` ids and hosted-LLM endpoints, catching shadow-AI raw-HTTP
usage with zero imports (new `raw_endpoint` fixture). Routing fixed so a
rule of one primary technique can carry auxiliary string evidence.

**Benchmark: 9/9 PASS, no xfails remain; `requests` and `flask` FP controls
stayed at zero through all three new signals.** Legitimate new visibility on
real repos: face_recognition's webcam notebook examples (AI-009) and its
declared `dlib` (declared-only AI-001). 41 orchestrator unit tests green
(12 new in test_t1_signals.py).

**Impact on SYSTEM.md:** §3.1 — detection signal sources, notebook handling,
coverage stats, benchmark pointer.

**Refs:** v07 T1 delivery note; corpus.json promotions (same-commit ground
truth cited per its _doc rule).

---

## 2026-08-31 — v07 T0 delivered: detection benchmark; first run caught three defects

**What:** Built the detection benchmark
([`orchestrator/detection_benchmark/`](../orchestrator/detection_benchmark/)):
`corpus.json` with 5 SHA-pinned public repos (deepface, face_recognition,
openai-quickstart, plus `requests` and `flask` as false-positive controls) and
3 local fixtures (`modern_sdk` guarding the DL-027 fix; `notebook_only` and
`manifest_only` as strict xfails encoding v07 gaps 1/3/4). Runner
([`run_detection_benchmark.py`](../orchestrator/scripts/run_detection_benchmark.py))
drives the real pipeline deterministically (`_scan_and_profile(use_llm=False)`
— new param), scores per-rule ground-truth expectations, reports coverage per
v06 §4, and fails on any miss, control-repo FP, or xpass. CI:
[`detection-benchmark.yml`](../.github/workflows/detection-benchmark.yml)
(PRs touching the scanner, weekly, no secrets).

**The first run caught three real defects (BUG_LOG DL-028/029/030):**
1. **DL-028** — `ingest` matched exclusions against *absolute* path segments,
   so a repo under any ancestor named `.cache`/`env`/`build`/`out` ingested
   **0 files** and reported MINIMAL_RISK with `errors: 0`. Now repo-relative.
2. **DL-029** — AI-004/AI-006 (missing model/data card) had **never emitted a
   finding**: the absent-marker `Evidence(file=".", line=0)` failed `ge=1`
   validation inside the fail-open per-scanner except. `Evidence.line` is now
   optional for repo-level facts; deepface/face_recognition/quickstart now
   correctly show both findings.
3. **DL-030** — AI-005 fired on the word "email" in a Flask docstring about
   URL generation. `ContentScanner` now honours the `requires_any_rule`
   precondition (mechanism already existed in FilePatternScanner) and AI-005
   requires AI-001/002/003 evidence first.

**Post-fix benchmark: 6/6 PASS, 2 XFAIL as pre-registered, 100% detection
pass rate.** 29 orchestrator unit tests green (12 import-scanner + 8 gating +
existing). Every defect is the same silent-degradation class the benchmark
was built to catch — it paid for itself before its first commit.

**Impact on SYSTEM.md:** none yet — scanner behaviour changes are
recall/precision fixes within documented architecture; v07 doc carries the
T0 delivery note.

**Refs:** v07 T0; BUG_LOG DL-028/029/030; `first_run.json` baseline.

---

## 2026-08-31 — v07 proposed: scanner robustness — measure recall first, then widen the signal

**What:** Researched how the field detects library/AI usage in code (Semgrep vs
CodeQL benchmark data, Cisco's aibom three-tier AI-BOM architecture, IRIS
neuro-symbolic LLM+CodeQL at ICLR 2025, the open-source EU-AI-Act scanner
landscape) and audited our six scanners against it. Verified gaps: detection is
single-signal (imports only — `ingest()` builds a dep manifest **no scanner
reads**), no string-literal/model-id signal, no `.ipynb` support, no dynamic
imports, window-heuristic adjacency instead of reachability for AI-003/007/010,
prohibited triggers ignore confidence, and **zero measured detection recall** —
the condition that let DL-027 ship clean reports while blind to `from X import
Y`. Proposal: [`design-evolution/v07-scanner-robustness.md`](design-evolution/v07-scanner-robustness.md)
— T0 a pre-registered detection benchmark corpus (the refuse-list's own
precondition for expansion), T1 manifest cross-referencing + notebook ingestion
+ model-string patterns inside the existing six scanners, T2 confidence-aware
PROHIBITED escalation + an IRIS-shaped LLM confirm/triage pass (never
detection), T3 explicitly deferred taint/languages.

**Why:** DL-027 proved one traversal bug can silently collapse recall across
every import rule. The retrieval side has METRICS.md and CI; the scanner — the
actual product — has no recall number at all.

**Impact on SYSTEM.md:** none — proposal only.

**Refs:** v07 doc (research links inline); BUG_LOG DL-019/DL-020/DL-027;
NORTHSTAR Part IV/V.

---

## 2026-08-31 — Knowledge graph restored (2nd Aura deletion); v06 proposed; BUG_LOG reformatted

**What:** Found the Neo4j Aura instance `e8097dda` hard-deleted — DNS no longer
resolves — after ~36 days dormant. This is the **second** free-tier idle deletion
(DL-025 was the first), and DL-025's own open follow-up predicted it: the
`keep-aura-alive.yml` ping was never diagnosed and never replaced with a
scheduled backup. Restored the full KG from the verified `20260619_183622` JSONL
dump into new instance `dab1e7ea` via
[`11_restore_from_jsonl.py`](../knowledge_engine/scripts/11_restore_from_jsonl.py):
**2,301/2,301 nodes, 4,423/4,423 relationships (0 skipped), 2,198 embeddings,
`entity_embedding` vector index recreated.** Added
[`design-evolution/v06-durable-kg-and-reproducible-eval.md`](design-evolution/v06-durable-kg-and-reproducible-eval.md)
(`status: proposal`) covering durability + reproducibility, and reformatted
[`BUG_LOG.md`](BUG_LOG.md) into the shape Alloygraph's devlog importer parses so
the 26 incidents load as queryable project memory (content preserved; verified
line-for-line).

**Why:** The KG is the project's moat and v03 delivered it without durability.
Restoring is a 4-minute chore only because DL-025 left a backup script behind —
without it this was a full rebuild. v06 exists to stop the third deletion from
being an incident.

**Acceptance run (v06 §2.5): PASSED, exactly.** Once a working Gemini
credential was in place, scripts 07 and 12 reproduced **every** recorded number
against the restored graph — hybrid_rrf citation recall@15 27/33 (81.8%),
vector 24/33 (72.7%), graph 7/33 (21.2%), pass rate 17/25 (68%), the same eight
failing queries, and identical per-category means. The restore is behaviourally
exact, not merely close. The HNSW non-determinism that moved the headline 12.5pp
on the old n=6 set moved it 0.0pp here, which is the n=25 expansion doing the job
`METRICS.md` §5 said it would. No headline number was changed.

**Was blocked (now resolved):** the acceptance run initially failed — — the
Gemini credential in `.env` returns `401 UNAUTHENTICATED`. Verified by testing
each key directly: `GEMINI_API_KEY` and `GOOGLE_API_KEY` are the *same* value
and both fail, while a known-good key on the same machine succeeds, so it is the
credential, not the client or the format. This is DL-017 recurring, and DL-017's
own lesson ("always test API keys independently") is what found it. Confirmed
`07_run_golden_tests.py` exits **1** on this failure, so CI would catch it — not
a silent failure.

**Impact on SYSTEM.md:** none yet — no code changed. §2.1's Aura instance ID is
now `dab1e7ea`; update when v06 lands.

**Refs:** `9243d37` (BUG_LOG reformat); backup `20260619_183622`; BUG_LOG
DL-017, DL-025.

---

## 2026-06-19 — Close RAG/eval gaps: expanded golden set + 3-mode comparison + RAGAS-equivalent + CI + ColPali scaffolding

**What:** Closed the two partial items from the post-audit completion tally. **(1) Golden set expanded 6 → 25 queries** ([`../knowledge_engine/golden_tests/test_queries.json`](../knowledge_engine/golden_tests/test_queries.json)): 7 single-hop / 11 multi-hop / 7 out-of-scope (matching the audit §4.3 split intent of 12/10/8 within the 25 cap). Authored against the real KG — every `expected_citations` ID verified to exist before authoring; uses Articles, Annexes, Concepts, Rights, RiskCategories, Penalties across both regulations. **(2) 3-mode comparison runner** ([`../knowledge_engine/scripts/12_eval_three_mode.py`](../knowledge_engine/scripts/12_eval_three_mode.py)) — runs vector_only / graph_only(vector-seeded) / hybrid_rrf on each query, reports per-mode + per-category breakdown, writes JSON artifact. **First run: hybrid 81.8% citation recall@15, vector 72.7%, graph 21.2%. Hybrid beats vector by 9pp — RRF validated.** **(3) RAGAS-equivalent metrics** ([`../knowledge_engine/scripts/13_eval_ragas_equivalent.py`](../knowledge_engine/scripts/13_eval_ragas_equivalent.py)) implemented directly against the existing Gemini client (no langchain/openai/pandas dep). Context relevance fully wired (375 judge calls, ~22 min); faithfulness + answer_relevance scaffolded but require ReasoningEngine and incur higher cost so gated to manual `--no-context-only` invocation. **First context-relevance run: 45.9% mean across 25 queries.** Notable signal: invented-constraint negative cases (GT_24 file-size, GT_25 HIPAA) hit 7% — system correctly recognises nonsense queries, *low context relevance is the right outcome there*. **(4) CI workflow** ([`../.github/workflows/golden-tests.yml`](../.github/workflows/golden-tests.yml)) — runs scripts 07 + 12 on every PR touching `knowledge_engine/`, weekly on main, manual-dispatch for the heavy script 13. **(5) ColPali multimodal scaffolding** at [`../knowledge_engine/src/multimodal/`](../knowledge_engine/src/multimodal/) — module compiles, interface fixed (indexer, MaxSim retriever, design rationale in [`v05-multimodal-colpali.md`](design-evolution/v05-multimodal-colpali.md) as `status: proposal`). `colpali-engine` deliberately not in deps; runtime import gated. Not built end-to-end — gated on GPU + Aura tier upgrade + 10-query multimodal benchmark + acceptance criteria in v05. Plus fixed real bug along the way: `gemini-2.0-flash` was deprecated 2026-06-19; updated 4 source-code references to `gemini-2.5-flash` (ReasoningEngine, ObligationExtractor, scripts 06 + 07). Updated [`METRICS.md`](METRICS.md) wholesale with new headline + 3-mode table + RAGAS-equivalent section + n=25 per-query breakdown + §4 entity-recall structural analysis + §5 HNSW non-determinism context. Updated [`../README.md`](../README.md) headline. Added new INTERVIEW_GUIDE Q11 ("how do you measure RAG quality?") + updated Q10 ("worst part") with the multimodal-honest framing. Updated cheat sheet of citable numbers.

**Why:** Direct execution of the two partial items from the 2026-06-19 completion tally ("Close RAG gap: ⚠️ partial; Close eval gap: ⚠️ partial"). The original Phase-3 plan (`01_AlloyCode.md` §4.2–4.3) named ColPali + RAGAS + 30-question golden as the gaps; this pass closes the eval half completely (n=25 quantified) and scaffolds the multimodal half with full design + acceptance criteria so the next session can build against a fixed interface. **The 81.8% citation recall headline is the strongest single quantified claim the project can make in a CV / screen / interview.** Per audit §3.3: production metrics > model metrics > framework fluency > academic credentials. Now we have a production-shape number with a reproducible script behind it.

**Impact on SYSTEM.md:** None — operational scripts + scaffolding only; architecture unchanged.

**Refs:** New files: `knowledge_engine/scripts/12_eval_three_mode.py`, `knowledge_engine/scripts/13_eval_ragas_equivalent.py`, `knowledge_engine/src/multimodal/__init__.py`, `knowledge_engine/src/multimodal/colpali_indexer.py`, `knowledge_engine/src/multimodal/multimodal_retrieval.py`, `devlog/design-evolution/v05-multimodal-colpali.md`, `.github/workflows/golden-tests.yml`. Modified: `knowledge_engine/golden_tests/test_queries.json` (6 → 25 queries), `knowledge_engine/src/retrieval/reasoning_engine.py` (model fix), `knowledge_engine/src/extractors/obligation_extractor.py` (model fix), `knowledge_engine/scripts/06_demo_query.py` (model fix), `knowledge_engine/scripts/07_run_golden_tests.py` (model fix), `devlog/METRICS.md` (wholesale update), `devlog/INTERVIEW_GUIDE.md` (new Q11 + updated Q10 + cheat sheet), `devlog/design-evolution/README.md` (v05 entry), `README.md` (headline). Eval artifacts (gitignored): `knowledge_engine/golden_tests/three_mode_results_20260619_*.json`, `ragas_equiv_20260619_*.json`. **Not done:** faithfulness + answer_relevance runs (scaffolded, not executed); ColPali end-to-end deploy (gated on GPU + PDFs + Aura tier).

---

## 2026-06-19 — Recover from Aura free-tier 30-day deletion (phantom-instance rescue)

**What:** Discovered the original Neo4j Aura instance `652f6242` had been auto-deleted by Neo4j after 30 days of inactivity (Aura free-tier policy). User created replacement `e8097dda` and updated root `.env`. Diagnostic queries against the old URI **still succeeded** because Aura's deletion is two-stage (account-removal → grace period → hard-purge) and the cluster hadn't purged yet. Wrote streaming backup script [`../knowledge_engine/scripts/10_backup_to_jsonl.py`](../knowledge_engine/scripts/10_backup_to_jsonl.py); dumped phantom instance to `~98 MB` of JSONL (`2,301 nodes / 4,423 rels / 1 vector index / 23 indexes / 1 constraint`). Wrote idempotent restore script [`../knowledge_engine/scripts/11_restore_from_jsonl.py`](../knowledge_engine/scripts/11_restore_from_jsonl.py) using property-based identity mapping (`:Entity(id)` unique constraint) — element IDs aren't portable across instances, but `id` properties are. Synced `knowledge_engine/.env` from root `.env` via PowerShell regex (KE config reads its own `.env`, not root). Ran restore: `2,301/2,301 nodes, 4,423/4,423 rels, 2,198 embeddings, 0 skipped, vector index entity_embedding recreated at 3072-dim cosine`. Updated `.gitignore` to exclude `knowledge_engine/backups/`.

**Verified behaviour change.** Reran golden tests on the restored instance: **citation recall@15 = 75% (6/8)**, down from 87.5% on the original. Same data, different HNSW build → `AIACT_ART_14` slipped past the top-15 cutoff for `GT_02`. This is HNSW non-determinism, not data loss — confirmed by direct query showing the node exists with correct properties + 3072-dim embedding. Updated [`METRICS.md`](METRICS.md) §5 with the analysis (HNSW non-determinism explained, both builds recorded, headline switched to 75% with the 75–87.5% range published — honest is better than cherry-picking). Updated [`../README.md`](../README.md) headline. Added [`BUG_LOG.md`](BUG_LOG.md) DL-025 with the full recovery story + the open follow-up to investigate why `keep-aura-alive.yml` didn't prevent the deletion (likely answer: Aura policy-based deletion, not activity-based — a `count(n)` ping doesn't reset the 30-day timer).

**Why:** Single most valuable artifact in the project is the 2,301-node regulatory KG; SYSTEM.md §2.1 explicitly calls it "the single hardest thing in the repo to rebuild" because re-running scripts `01 → 09` against raw text takes ~30 min + Gemini API spend. Recovery via JSONL dump completes in ~4 min and is exact-replica (same embeddings, no recomputation). The pair of scripts also gives a durable backup/restore path the project lacked entirely — important now that Aura free-tier is known to delete unilaterally.

**Impact on SYSTEM.md:** §2.1 Data layer — counts unchanged (still 2,301 / 4,423 / 2,198), but the active instance ID changed from `652f6242` → `e8097dda`. Added two new operational scripts to the KE pipeline. The METRICS.md headline number dropped from 87.5% to 75% with a published range; `last_verified` bumped on METRICS + BUG_LOG. SYSTEM `last_verified` unchanged (no architecture change — only an instance migration).

**Refs:** new scripts `knowledge_engine/scripts/10_backup_to_jsonl.py`, `knowledge_engine/scripts/11_restore_from_jsonl.py`. Modified `.gitignore`, `devlog/METRICS.md`, `devlog/BUG_LOG.md`, `devlog/CHANGELOG.md`, `README.md`. Backup data on disk (gitignored): `knowledge_engine/backups/20260619_183622_*.jsonl|.json`. **Not done:** push new Aura URI/password to GCP Secret Manager + restart Cloud Run services — KE on Cloud Run will silently break when `652f6242` hard-purges.

---

## 2026-06-16 — Remove dead Weaviate references from `pipeline.ps1`

**What:** Stripped all Weaviate references from [`../pipeline.ps1`](../pipeline.ps1): docstring synopsis + `.PARAMETER SkipInfra` block + the `[switch]$SkipInfra` param + all Show-Usage / examples / interactive-menu lines mentioning Weaviate or `-SkipInfra` + the stop-infra `docker compose stop weaviate` block + the start-mode Docker-for-Weaviate prereq check + the start-infra `docker compose up -d weaviate` block + the "Pipeline Ready" summary banner that listed Weaviate at localhost:8080. Replaced with a brief comment + a "Vector store: Neo4j Aura (remote, via NEO4J_URI in env)" banner line. Renumbered the interactive menu after dropping the now-meaningless `[5] stop-keep-infra` option. Smoke-tested via `pipeline.ps1 -Action help`.

**Why:** The system migrated Weaviate → Neo4j native HNSW in commit `661f990` (see [`design-evolution/v03-kb-completion.md`](design-evolution/v03-kb-completion.md) + [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md) Q5). `docker-compose.yml` already had zero Weaviate services, so `pipeline.ps1 -Action start` would silently no-op the `docker compose up -d weaviate` call (no such service) and then time out on `Wait-ForService -Port 8080`. The references were dead code that would *break* the local-dev start path if anyone tried to use `-SkipInfra=$false` — surfaced when the user opened the script and noticed the Weaviate mention.

**Impact on SYSTEM.md:** none — `pipeline.ps1` is a local-dev convenience script, not part of the architecture. The vector-store-is-Neo4j claim was already documented.

**Refs:** doc + script only; commit pending. The python-side dead twin `knowledge_engine/scripts/05_load_vector_store.py` (the original Weaviate loader, superseded by `09_load_vectors_to_neo4j.py`) is **not** touched in this pass — flagged as adjacent cleanup if desired.

---

## 2026-06-16 — Execute the NORTHSTAR punch list (7 of 7 items landed)

**What:** Worked through the [`NORTHSTAR.md`](NORTHSTAR.md) Part III punch list end-to-end in a single session. (1) Cleaned repo cruft — deleted 10 empty path-with-spaces dirs in `orchestrator/`, deleted `frontend/ts_errors.txt` + 4 `scan_*.json` scratch dumps, added `legacy_prototypes/` to `.gitignore` and untracked it (preserves the raw EU AI Act / CJEU / EDPB source corpus on disk, removes it from repo surface). (2) Resolved tri-naming — **AlloyCode** is canonical; Aegis deprecated; updated DEPLOYMENT.md / BUG_LOG.md / gcp.ps1 (5 strings) / SYSTEM.md naming paragraph + glossary. (3) Wrote [`design-evolution/v04-hitl-decision.md`](design-evolution/v04-hitl-decision.md) — formal `status: implemented` decision record with the EU AI Act Article 14 counter-argument and the `mypy`-analogue response. (4) Created root [`../README.md`](../README.md) — tagline, Mermaid architecture diagram, headline-numbers table, live demo URLs, quickstart, where-to-go-next pointers, ATS-keyword coverage. (5) Wrote [`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md) — 10 line-by-line defence questions with three-sentence answers + follow-up traps + citable references. (6) Rewrote the upstream calibration deferral banner in `../../10Weeks/project_calibration/01_AlloyCode.md` — the original "sparse / empty README / no PORTFOLIO_ENTRY" rationale was factually wrong; replaced with a focus-discipline rationale + complete inventory. (7) Produced quantified retrieval metrics — ran `knowledge_engine/scripts/07_run_golden_tests.py --dry-run` against live Aura, captured in [`METRICS.md`](METRICS.md): **citation recall@15 = 87.5%** (7/8), entity recall@15 = 20% (2/10), pass rate = 3/6. (8) Verified deploy state — three Cloud Run services already live (frontend HTTP 200, KE healthy with 2,198 docs / 2,301 nodes confirmed, orchestrator degraded — Postgres unavailable, logged as new BUG_LOG DL-024). Moved all seven completed items into NORTHSTAR `## Resolved`; added five new follow-up targets (DB fix, Loom, cross-regulation expansion, entity-name index, golden-set expansion).

**Why:** Direct execution of [`../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) §6.1 ranked gap-fills + §7.3 sequencing for Project 1. The audit identified seven concrete, mostly-non-code deliverables (deploy / quantify / document) that, taken together, convert AlloyCode from "scripted-but-not-deployed and mislabelled as sparse" into a defensible front-line exhibit per the audit's §3.4 defensibility thesis and §5 levers. Running them all in one session locks in the depth-over-breadth posture before scope drifts. The new BUG_LOG entry (DL-024) was discovered as a side effect of verifying the deploy state — the audit had assumed the URL was "pending," but it has been live for some time and Postgres has degraded silently since the last touch.

**Impact on SYSTEM.md:** §3.2 drift note now cross-references v04; §7 Glossary entries for AlloyCode/Aegis/EU_AI_GDPR rewritten to mark Aegis deprecated and AlloyCode canonical; HITL glossary entry now cross-references v04. `last_verified` bumped to 2026-06-16.

**Refs:** doc-only + deploy verification. No code changed; no commits yet (file system only). New files: `README.md` (root), `devlog/INTERVIEW_GUIDE.md`, `devlog/METRICS.md`, `devlog/design-evolution/v04-hitl-decision.md`. Modified: `CLAUDE.md`, `devlog/SYSTEM.md`, `devlog/CHANGELOG.md`, `devlog/README.md`, `devlog/NORTHSTAR.md`, `devlog/BUG_LOG.md` (DL-024), `devlog/DEPLOYMENT.md`, `devlog/design-evolution/README.md`, `gcp.ps1`, `.gitignore`, `../../10Weeks/project_calibration/01_AlloyCode.md`. Deleted: 10 empty dirs in `orchestrator/`, `frontend/ts_errors.txt`, 4 `orchestrator/scan_*.json` files. Untracked from git (kept on disk): `legacy_prototypes/`.

---

## 2026-06-16 — Create NORTHSTAR.md from portfolio audit findings

**What:** Created [`NORTHSTAR.md`](NORTHSTAR.md) — the strategy / posture / refuse-list doc. Source: [`../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) (compiled 2026-06-16). The audit's §6.1 ranked gap-fills became Part III punch list; §3.4 + §5 produced the three-track single rule; §7.3 sequencing reframed the deferral; project-scope decisions (no fine-tuning, no MCP, no multi-language, etc.) became Part IV refuse list. Also updated [`../CLAUDE.md`](../CLAUDE.md) (NORTHSTAR is now present, dropped "currently absent" notes) and [`README.md`](README.md) (top-level docs section + mapping table reflect the live NORTHSTAR).
**Why:** A fresh audit landed naming concrete gaps for Project 1 (deploy demo, surface quantified eval numbers, clean cruft, resolve tri-naming, decide HITL story, populate root README, rewrite the upstream "sparse/deferred" rationale that the audit shows is factually wrong). Per [`../DOCS_PLAYBOOK.md`](../DOCS_PLAYBOOK.md) §8.4 the right home for "what to do next + what to refuse" is NORTHSTAR, not SYSTEM.md (which is past-tense code mirror) or a `vNN` proposal (which would imply architectural change — these are deploy/quantify/document fixes). Recording the punch list before executing it locks it against scope-creep and gives the next session a single citable list.
**Impact on SYSTEM.md:** none — strategic / meta-doc work only. No code changed.
**Refs:** doc-only; commit pending. Punch list to be worked through Phase-2; items move to NORTHSTAR `## Resolved` as they land.

---

## 2026-06-16 — Align devlog meta-docs with DOCS_PLAYBOOK v1.1 (NORTHSTAR added)

**What:** Updated [`../CLAUDE.md`](../CLAUDE.md) Part 1 (read order now lists NORTHSTAR as slot #2 with "currently absent" note) and Part 2 (added Step 6 — when/why to touch NORTHSTAR). Updated [`README.md`](README.md) top-level docs section and the doc-type mapping table (renumbered to match new 6-type model: #3 NORTHSTAR / #4 design-evolution / #5 history / #6 JOURNEY).
**Why:** [`../DOCS_PLAYBOOK.md`](../DOCS_PLAYBOOK.md) was refined from v1.0 (5 doc types) to v1.1 (6 doc types — adds NORTHSTAR.md as strategy/posture/refuse-list). The devlog's instantiation needed to mirror the new model so a fresh agent sees the same structure the playbook describes. NORTHSTAR.md itself is not yet created — populating it requires real strategic content (single rule, N-day targets, refuse list) the user has not yet defined.
**Impact on SYSTEM.md:** none — meta-doc / playbook alignment only.
**Refs:** doc-only; tracks playbook v1.1 (refined 2026-06-13 by Alloygraph adoption). No commit yet.

---

## 2026-05-20 — Adopt living-docs playbook

**What:** Created `CLAUDE.md` (root) + `devlog/` tree (`SYSTEM.md`, this `CHANGELOG.md`, `README.md`, `JOURNEY.md`, `design-evolution/v01-v03`, `history/00-01`, `prompts/`). Moved `DEPLOYMENT_GUIDE.md` → `devlog/DEPLOYMENT.md` and `DEVLOG.md` → `devlog/BUG_LOG.md`. Archived `gdpr context/` and `docs/archive/` into `devlog/history/01-research-arc.md` (preserved full text) + `devlog/history/00-history-and-decisions.md` (distilled narrative).
**Why:** Documentation was in three disconnected piles (root-level ops docs, `docs/` dir, `gdpr context/` brainstorm trail). A fresh AI agent couldn't tell current state from frozen state — `docs/MEMORY.md` said KB was "100% COMPLETE" while `gdpr context/main/04` said "12% complete," neither marked as which epoch. Applying [`../DOCS_PLAYBOOK.md`](../DOCS_PLAYBOOK.md) §11 bootstrap fixes the structural problem.
**Impact on SYSTEM.md:** Created from scratch (was missing); §1–§8 populated from direct code audit.
**Refs:** doc-only; commit pending.

---

## 2026-04-13 — Knowledge base build-out completed

**What:** Neo4j knowledge graph reached final state: 2,301 nodes, 4,423 (or 4,431 — sources disagree) relationships, 17 entity types, 13 relationship types, 2,198 vector documents across 7 collections, 84 cross-regulation `COMPLEMENTS` edges, 0 orphan nodes. Embeddings on `gemini-embedding-001` at 3072 dimensions. Sources: [`docs/MEMORY.md`](history/01-research-arc.md), [`docs/REFERENCE.md`](history/01-research-arc.md) §1.1.
**Why:** The Feb 2026 gap analysis (`gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`) showed the KB was only 12% complete — multi-hop reasoning was failing ~88% of test scenarios. Without a complete corpus, the "rule corpus, not Q&A bot" reframe from the static-scanner pivot doesn't land. Decision: complete in-house at paragraph granularity; no third-party paragraph-level KB exists.
**Impact on SYSTEM.md:** §2.1 Data layer — counts and schema. §3.3 Knowledge Engine — engines now operational against the full corpus.
**Refs:** doc-only (work pre-dates initial git import `2ccaadc`); design rationale captured in [`design-evolution/v03-kb-completion.md`](design-evolution/v03-kb-completion.md).

---

## 2026-04 — HITL approval pause removed from supervisor

**What:** `orchestrator/src/agents/supervisor.py` reduced to a linear graph: `classify_risk → research_legal → generate_narrative → synthesize → END`. The pre-pivot conditional branch that paused on `Critical` severity for human approval was removed. Docstring updated: *"No HITL branch: static scanners produce deterministic, auditable evidence, so there is no classification-uncertainty branch to pause on."*
**Why:** Static scanners produce ground-truth-able findings with `file:line` anchors — every claim is verifiable by opening the file. The HITL pause was inherited from the free-text era (where classification was vibes-based and needed human sanity-check). It became dead weight after the pivot.
**Impact on SYSTEM.md:** §3.2 Supervisor — node table reflects the 4-node linear graph; drift note added pointing at the now-archived `docs/README.md` which still mentioned HITL retention.
**Refs:** doc-only — the pivot landed across multiple unstaged edits; the doc trail is in [`docs/README.md`](history/01-research-arc.md) §5 (claims HITL retained — STALE) vs. [`orchestrator/src/agents/supervisor.py`](../orchestrator/src/agents/supervisor.py) (no HITL — CURRENT).

---

## 2026-Q1 — Migrate vector store to Neo4j; consolidate scripts and docs

**What:** Vector store moved from a custom JSON/ChromaDB hybrid into Neo4j's native vector index. One vector index (`entity_embedding`, 3072-dim, cosine) covers all 7 collections; queries filter by `n.collection`. Scripts in `pipeline.ps1` and `gcp.ps1` consolidated. Various docs reorganized under `docs/`.
**Why:** ChromaDB had Python 3.14 compatibility issues; running two storage backends added operational surface area without buying anything (Neo4j 5.x vector indexes are now first-class). Single backend = simpler health check, single backup story, fewer moving parts in Cloud Run.
**Impact on SYSTEM.md:** §2.1 Data layer — Neo4j-native vector index documented; §6 Deploy — single Neo4j env-var set replaces two storage configs.
**Refs:** commit `661f990` ("Migrate vector store to Neo4j; consolidate scripts and docs").

---

## 2026-Q1 — Restructure modules and update frontend/infrastructure

**What:** Major refactor of orchestrator module layout (introduces `code_analyzer/`, `agents/`, `database/`, `cache/`, `control_plane/` as top-level packages under `orchestrator/src/`). Frontend reorganized under Next.js App Router (`frontend/src/app/{scans,knowledge,page.tsx}`). Infrastructure files (Dockerfile per service, docker-compose.yml) updated.
**Why:** The static-scanner pivot needed a clean home for the new code_analyzer subsystem (scan.py, ingest.py, scanners/, rule_loader.py). Pre-existing layout mixed pre-pivot and post-pivot code; the refactor cleanly separated them.
**Impact on SYSTEM.md:** §3.1 Scan pipeline — newly documented; §5 Frontend — page paths updated.
**Refs:** commit `5210e51` ("Restructure modules and update frontend/infrastructure").

---

## 2026-Q1 — Static-scanner pivot (free-text → code scanner)

**What:** Project pivoted from a free-text "describe your AI system" classifier (5-agent LangGraph workflow over user prose) to a static compliance scanner over GitHub repos (deterministic detection + LLM narrative only). New subsystem: `orchestrator/src/code_analyzer/` (ingest, 6-scanner pipeline, profile builder). Pre-pivot architecture preserved in [`docs/archive/`](history/01-research-arc.md).
**Why:** Three fatal problems with the free-text approach: (1) input was vibes — classifier had no ground truth, (2) every demo looked identical (textbox + spinner + markdown), (3) no differentiator vs. any LLM-wrapper project. The static-scanner reframe ties every finding to `file:line` in real code; the knowledge graph becomes a rule corpus instead of a research Q&A bot. See [`design-evolution/v02-static-scanner-pivot.md`](design-evolution/v02-static-scanner-pivot.md) for the alternatives weighed and the consequences accepted.
**Impact on SYSTEM.md:** §1, §3.1, §3.2 fully rewritten; §3 added the scanner pipeline; §4.1 added `POST /api/v1/scans` and friends.
**Refs:** the orchestrator/code_analyzer/ subtree did not exist pre-pivot — see [`gdpr context/backup/improve_v1.md`](history/01-research-arc.md) (KB-design critique that pre-dated the pivot) and [`docs/README.md`](history/01-research-arc.md) §2 for the reasoning. Commits `5210e51` and `661f990` carry the bulk of the implementation.

---

## 2026-Q1 — Initial commit (project scaffold)

**What:** First git commit of the EU AI Compliance Engine. Includes the three-service Docker Compose layout, FastAPI scaffolding for orchestrator + knowledge engine, Next.js scaffolding for frontend, initial Neo4j schema definitions.
**Why:** Establish the repo as the consolidated home for what had been three notionally-separate projects (P1 Basic RAG / P3 GraphRAG Legal Engine / P4 Compliance Agent) — see [`history/01-research-arc.md`](history/01-research-arc.md) for the multi-project genesis.
**Impact on SYSTEM.md:** baseline.
**Refs:** commit `2ccaadc` ("Initial commit of EU AI Compliance Engine").

---

## Pre-existing operational bug log

The pre-existing `DEVLOG.md` has been moved to [`BUG_LOG.md`](BUG_LOG.md) and reframed as the **incident log** (companion to this CHANGELOG): 23 dated entries `DL-001` through `DL-023` covering operational fixes — uv/PowerShell issues, embedding model deprecations, CORS, Cloud Run port binding, git binary missing, secret corruption, etc. Format and contents are preserved; only the title and path changed.

Use this CHANGELOG for **intentional changes**. Use `BUG_LOG.md` for **incident-and-fix**.

---

## How to append a new entry

1. Add a new `## YYYY-MM-DD — <title>` block above the most recent dated entry (newest first).
2. Fill the four fields strictly: `What:` (concrete files / modules / pages), `Why:` (one or two sentences — this is the only prose field), `Impact on SYSTEM.md:` (sections updated, or `none — internal only`), `Refs:` (commit shorts, migrations, PR refs).
3. Bump `last_verified:` in this file's frontmatter.
4. Also update the section in `SYSTEM.md` that the change touches, and bump `last_verified:` there too.
