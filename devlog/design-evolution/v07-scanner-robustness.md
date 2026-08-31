---
version: "07"
title: Scanner robustness — measure recall first, then widen the signal
status: proposal
derives_from: v02-static-scanner-pivot.md
proposed_date: 2026-08-31
decided_date: null
implemented_in:
  - null
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - orchestrator/src/code_analyzer/scanners/       # the 6 scanners this hardens
  - orchestrator/src/code_analyzer/ingest.py       # builds a dep manifest nothing reads
  - orchestrator/src/code_analyzer/rules/          # the 10 rules whose recall is unmeasured
  - devlog/BUG_LOG.md DL-027                       # the false negative that motivated this
  - devlog/NORTHSTAR.md Part IV                    # the refuse-list this must respect
ai_guidance: |
  This is a forward-looking proposal grounded in external research (links
  inline). Read SYSTEM.md for what's actually built. Only treat this doc as
  current if status: implemented.
---

# v07 — Scanner robustness: measure recall first, then widen the signal

## 0. What this document is

DL-027 is the reason this exists. One traversal bug made every import-based
rule blind to `from X import Y` — the dominant modern Python import style —
and the scanner shipped confident, clean reports the whole time. A
face-recognition library whose name sits in AI-001's own pattern list scanned
as LIMITED_RISK. The fix was ten lines; the finding is that **nothing in this
project can currently notice when detection recall collapses.** The retrieval
side has METRICS.md, a golden set, and CI. The scanner — the actual product —
has no measured recall at all.

This proposal is the result of researching how the field detects library/AI
usage in code (SAST engines, AI-BOM tooling, LLM-assisted static analysis)
and auditing our six scanners against it. The punchline is unfashionable:
**the highest-value work is not new detection capability, it is a detection
benchmark** — which happens to be exactly the precondition NORTHSTAR Part IV
already sets for expanding the scanner at all ("depth… beats breadth. Adding
rules without quantifying the existing ones is anti-pattern").

## Status

- **State:** `proposal`
- **Decided:** null
- **Implemented in:** null
- **Supersedes:** nothing. Refines the algorithmic core ratified in v02.

## 1. What the research says

### 1.1 Where AlloyCode sits in the SAST spectrum

The field brackets into syntactic pattern engines (Semgrep: tree-sitter ASTs,
YAML rules, ~10-second scans) and semantic engines (CodeQL: a relational
program database with real cross-function taint tracking, 30+ minute scans).
AlloyCode is architecturally a small Semgrep: tree-sitter, per-file matching,
no dataflow. Two numbers from that world matter here:

- On the OWASP Benchmark, CodeQL scores **74.4% F1 vs Semgrep's 69.4%** — the
  semantic engine buys surprisingly little at benchmark level.
- Semgrep's own Pro-vs-Community split is the bigger lesson: **72–75% detection
  (Pro, cross-function) vs 44–48% (Community, single-function)** on the same
  rules. Engine reach, not rule count, dominated — and they know this only
  because they measure detection rate continuously.

Implication: staying a fast syntactic engine is defensible (it is the v02
thesis), but only alongside a measured detection rate. Semgrep-CE-class recall
is a real possibility for us right now and we would not know.

### 1.2 How AI-BOM tooling detects AI components

The closest cousins to AlloyCode's detection problem are AI-BOM generators.
Cisco's open-source [aibom](https://github.com/cisco-ai-defense/aibom) is the
clearest architecture statement, and it is strikingly parallel to ours — a
deterministic tier, a cross-reference tier, an LLM tier — but with **six
signal sources** where we have one:

| Signal | Cisco aibom | AlloyCode today |
|---|---|---|
| Dependency manifests (pip/poetry/npm…) | ✓ | **built by `ingest()`, read by nothing** |
| Import statements | ✓ (LibCST for Python) | ✓ (tree-sitter; fixed in DL-027) |
| Inline string literals (model ids, endpoints) | ✓ | ✗ |
| Structural patterns (agent loops, pipelines) | ✓ | partial (decision-surface windows) |
| Environment variables | ✓ | ✗ |
| Container layers | ✓ | ✗ (out of scope for us) |

Their third tier uses an LLM to **confirm or reject every candidate** and
enrich it with registry-verified identifiers — unverified candidates are
filtered, not reported. Our LLM pass only *removes* (test/mock surfaces) and
never confirms or enriches.

### 1.3 LLM-assisted static analysis (the research frontier)

[IRIS (ICLR 2025)](https://arxiv.org/abs/2405.17238) is the reference result:
a neuro-symbolic pipeline where LLMs mine taint specifications and triage
alarms while CodeQL remains the detection engine. On CWE-Bench-Java it found
**55 vulnerabilities where CodeQL alone found 27**, while *reducing* the false
discovery rate by 5pp. Related work uses LLMs for
[path-feasibility triage](https://arxiv.org/pdf/2506.10322) of static alarms.

This refines, rather than contradicts, our "LLM out of the detection hot
path" thesis (NORTHSTAR Part V): the field's result is **LLM out of
*detection*, LLM in *specification and triage*** — mining patterns, judging
candidates, killing false positives — with every finding still anchored to
deterministic evidence.

### 1.4 The honest limit (and competitors' silence about it)

Surveying the EU-AI-Act scanner landscape ([comparison](https://airblackbox.ai/blog/eu-ai-act-compliance-tools-compared),
[ArkForge MCP scanner](https://github.com/ark-forge/mcp-eu-ai-act)):
open-source competitors are questionnaires, shallow pattern matchers, or
runtime hooks, and the comparison literature is notably silent on false
negatives. The one point of consensus: static analysis can see *which
capabilities the code has*, not *how the system is deployed* — and AI-Act
risk often turns on deployment. AI-001's remediation text already handles
this correctly ("in closed / consented contexts this remains high-risk…").
The DL-027 follow-up (a test-file hit escalating to PROHIBITED) is this
limit surfacing inside our own risk math: capability evidence and deployment
inference must not be conflated by a trigger that ignores confidence.

## 2. Gap analysis (verified against the code, 2026-08-31)

1. **Single-signal detection.** Only imports fire AI-001/AI-002.
   `ingest()` builds a dep manifest that no scanner reads (verified by grep) —
   a repo that declares `deepface` in requirements but imports it dynamically
   is invisible. SYSTEM.md even documents the manifest as a built artifact.
2. **No string-literal signal.** `AutoModel.from_pretrained("Salesforce/…")`,
   OpenAI/Anthropic endpoint URLs, HF model ids — all invisible unless an
   import also matched.
3. **File coverage.** `.py/.js/.ts` only. **No `.ipynb`** — a material share
   of real ML code lives in notebooks; a notebook-only repo scans clean.
4. **Dynamic imports** (`importlib`, `__import__`, lazy loaders) are
   invisible; manifests are the practical mitigation, see (1).
5. **Adjacency, not reachability.** AI-003/007/010 judge "endpoint lacks
   human review / audit / override" from a ±N-line window heuristic. No
   dataflow, so a review check one function away is a false positive and a
   decorator-wrapped one is a false negative.
6. **Confidence dies at the top.** Rules carry calibrated confidence with
   test-path dampeners, but the prohibited-trigger check ignores confidence
   entirely (DL-027 follow-up: PROHIBITED set by a `tests/` file).
7. **Zero detection benchmark.** No corpus, no recall number, no CI gate.
   Every one of DL-019, DL-020, DL-027 was a silent recall collapse that a
   measured benchmark would have caught on the day it shipped.

## 3. Proposal (tiered; each tier gated on the one before)

### T0 — The detection benchmark (do this first; ~a day)

A labelled corpus of 15–25 public repos with **pre-registered expected
findings** per repo — rule id, file, approximate line — scored like the
retrieval golden set: recall and precision per rule, in CI beside
`golden-tests.yml`. Seed set from repos already scanned and hand-verified
today: `serengil/deepface` (expect AI-001 ≥ N, component `deepface`),
`ageitgey/face_recognition`, `openai/openai-quickstart-python`,
`psf/requests` (expect **zero** — the false-positive control), plus a
notebook-only ML repo and a dynamic-import repo *expected to fail* (xfail),
which turns gaps (3) and (4) from unknowns into tracked, dated expectations.

This is C1 discipline applied to the scanner, and it satisfies the
refuse-list's own precondition for any expansion. **Nothing in T1+ lands
without a before/after benchmark delta.**

> **T0 delivered (2026-08-31, same day).** `orchestrator/detection_benchmark/`
> (corpus.json — 5 pinned repos + 3 fixtures, expectations authored from repo
> ground truth), `scripts/run_detection_benchmark.py` (deterministic
> `use_llm=False` path, strict xfail, coverage reported per §5), CI at
> `.github/workflows/detection-benchmark.yml`. **Its first run caught three
> real defects**: DL-028 (absolute-path exclusion → repos under `.cache`/`env`
> ancestors scan as 0 files), DL-029 (AI-004/AI-006 had *never* emitted — the
> absent-marker Evidence crashed validation inside a fail-open except), DL-030
> (AI-005 fired on "email" in a Flask docstring; now gated on
> `requires_any_rule`). Post-fix: 6/6 PASS, 2 XFAIL as registered, detection
> pass rate 100%. The rest of this proposal remains `proposal`.

### T1 — Widen the signal inside the existing six scanners

No new scanner types; these extend evidence sources of existing ones:

1. **Read the manifest** in `ImportScanner`: parse
   `requirements*.txt` / `pyproject.toml` / `package.json`, match the same
   rule patterns. Cross-reference per Cisco's Tier 2: *declared+imported* →
   confidence up; *declared-only* → medium-confidence finding ("dependency
   declared, usage not located"); *imported-only* → today's behaviour.
   Closes gaps (1) and most of (4).
2. **Notebook ingestion**: extract `.ipynb` code cells in `ingest()` and feed
   them through the existing scanners (cell → synthetic line mapping for
   evidence anchors). Closes gap (3) for Python's most AI-dense file type.
3. **Model-string patterns** in `ContentScanner`: HF org/model ids in
   `from_pretrained`/`pipeline()` calls, hosted-LLM endpoint URLs. Evidence
   stays `file:line` + excerpt, same as everything else. Closes gap (2).

### T2 — Fix confidence semantics; LLM as judge, not detector

1. **Confidence-aware verdict escalation**: a PROHIBITED trigger requires at
   least one hit at effective confidence ≥ threshold (i.e. not solely
   test/example-dampened evidence). Product decision flagged in DL-027 —
   needs an explicit call, then a rule.
2. **Extend the existing LLM pass from remove-only to confirm/enrich**
   (IRIS-shaped): for each candidate finding, the LLM judges "is this real
   use or vendored/dead/test code?" and may *lower* confidence or annotate —
   never raise, never create. Findings remain anchored to deterministic
   evidence, so Part V's "moat is the rule corpus" thesis is preserved; this
   is triage, not detection.

### T3 — Explicitly deferred (refuse-list aligned)

Dataflow/taint for AI-003/007/010 (CodeQL-class machinery; revisit only if
T0 shows those rules' precision is unacceptable), additional languages
(Java/Go), env-var and container signals, runtime hooks. Each waits for a
benchmark number proving the need.

## 4. What NOT to do (research-supported)

- **Don't add rules before T0.** Semgrep's CE/Pro split shows engine reach
  dominates rule count; our reach is unmeasured.
- **Don't put the LLM in detection.** IRIS's gain came from LLMs around a
  deterministic core. Our differentiation ("every finding traceable to a
  YAML rule, a code anchor, a regulatory article") survives only if that
  stays true.
- **Don't chase taint yet.** 30-minute scans kill the demo loop; the OWASP
  numbers say the payoff is smaller than intuition suggests; T0 will show
  whether window-heuristic precision is actually a problem.

## 5. Standing review question (inherited from v06 §4)

Every T1+ change answers before merging: *when this signal finds nothing,
can the caller distinguish "nothing exists" from "I stopped looking"?* —
manifest parse failures, unparseable notebooks, and string-scan skips must be
reported as coverage gaps in the profile, not swallowed. DL-027 lived for
months because the answer was no.
