---
version: "04"
title: No human-in-the-loop approval gate (decision record)
status: implemented
derives_from: v02-static-scanner-pivot.md
proposed_date: 2026-04-13
decided_date: 2026-04-13
implemented_in:
  - 5210e51   # Restructure modules and update frontend/infrastructure (supervisor.py rewrite — removed HITL branch)
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - orchestrator/src/agents/supervisor.py            # the docstring + the linear graph that has no HITL node
  - orchestrator/src/agents/risk_classifier.py       # deterministic classifier (no LLM, no uncertainty score)
  - orchestrator/src/code_analyzer/rule_loader.py    # the YAML rule catalog the classifier consumes
  - devlog/design-evolution/v02-static-scanner-pivot.md  # the broader pivot this decision falls out of
  - 07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md §6.1        # the audit that required this doc to exist
ai_guidance: |
  This is a DECISION RECORD that codifies an already-shipped removal — the
  human-in-the-loop approval branch the pre-pivot supervisor had for Critical
  findings. The decision is in code (supervisor.py); this doc is the explicit
  rationale + the response to the obvious EU-AI-Act counter-argument. Read
  this before suggesting "we should add HITL back" — it's correctly-deferred,
  not absent-by-oversight (see NORTHSTAR.md Part IV).

  If you're answering an interview question or a recruiter follow-up, the
  three-sentence answer is in §3. The longer defence is in §4.
---

## 0. What this document is

A formal decision record for a removal that already shipped: AlloyCode's LangGraph supervisor has no human-in-the-loop approval gate. The pre-pivot system (the v01 free-text classifier) had a HITL pause for Critical findings; the static-scanner pivot (v02) decided that gate added no signal and removed it. This doc explains *why*, addresses the EU AI Act counter-argument it invites, and lists the conditions under which the decision would be revisited.

It exists because the audit ([`../../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) §6.1) flagged it as one of the "inevitable follow-up questions" a candidate must be able to answer in an interview, and because the rationale was previously scattered across three places (a one-line docstring in supervisor.py, a passing mention in v02's Consequences section, a drift note in SYSTEM.md §3.2). One citable home, one explicit answer.

---

## Status

- **State:** implemented
- **Decision date:** 2026-04-13
- **Implementation:** commit `5210e51` — supervisor.py was rewritten as a 4-node linear graph (`classify_risk → research_legal → generate_narrative → synthesize → END`); no HITL node, no conditional branch, no `human_queue`.
- **Supersedes:** `v01-baseline.md §1` (the original supervisor had a HITL approval pause for Critical findings) and the now-archived `docs/README.md §5` claim that HITL was retained.
- **Superseded by:** none.

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | **Retain HITL on Critical findings** (the v01 design) | The trigger condition was classification uncertainty — LLM-produced category labels with confidence below a threshold. Post-pivot, categories come from a deterministic rule classifier (`risk_classifier.py`) with no uncertainty score, so no branch could be defined except a blanket "pause on every Critical finding," which adds latency without adding judgment. |
| 2 | **HITL gate after `research_legal`** (let a human approve the legal mapping) | The legal mapping is a Neo4j graph traversal grounded in `file:line` evidence. A human reviewer can verify it post-hoc from the citation list; pausing the pipeline to do so blocks the demo for no decision-quality gain. Closer to a tool the user runs *on* the output than a gate *inside* the pipeline. |
| 3 | **Optional HITL via config flag** (default off, on for production deployments) | Adds a code path and a configuration surface for a feature with zero current users. Violates [`../NORTHSTAR.md`](../NORTHSTAR.md) Part I (the single rule). Defer until a real deployment surfaces a real need. |

## Consequences

What removing HITL did:

- ✅ Pipeline runs end-to-end with no operator dependency — required for the live-demo target in [`../NORTHSTAR.md`](../NORTHSTAR.md) Part II. A scan completes in one round-trip.
- ✅ Deterministic, auditable output — every finding is traceable to a YAML rule and a `file:line` anchor; an external reviewer can verify the classification without re-running the system. This is what "ground-truth-able" means in the v02 thesis.
- ✅ No state-machine complexity (no `human_queue`, no resume tokens, no `SqliteSaver` checkpointing required for HITL replay).
- ⚠️ Removes a surface where a domain expert could override a borderline classification. The intended mitigation is the report itself — a Critical finding lists the rule hit, the matched code, the article citation, and the severity, and a downstream compliance officer can dispute any of those from the artifact.
- ⚠️ Loses an EU-AI-Act-aligned talking point ("human oversight"). See §4 for how to respond to that in interview.
- ❌ Rules out using AlloyCode as the *enforcement* layer in a production conformity workflow without a wrapping system that adds the gate externally. AlloyCode is a *reporting* tool, not a *blocking* tool.

---

## 1. The pre-pivot HITL design (what was removed)

The v01 supervisor was a five-agent graph where the `RiskClassifier` produced an EU AI Act category from free-text user input via an LLM call. Because LLM category outputs come with no calibrated confidence, the graph had a conditional branch: if the classifier's self-reported confidence was below a threshold (or the category was `HIGH_RISK` or `PROHIBITED`), the graph paused at a `human_approval` node, persisted state, and waited for an operator decision before continuing to legal research and documentation. This is the "approval gate" the pre-pivot `docs/README.md` described and the archived `gdpr context/` brainstorm trail explored at length.

## 2. The static-scanner pivot dissolved the gate's trigger

The v02 pivot replaced free-text input with a deterministic 6-scanner pipeline that produces an `AISystemProfile` from code. The `RiskClassifier` in the post-pivot system is a deterministic mapping over that profile:

- It scans `findings[].rule_id` for `prohibited_triggers` (currently `AI-008`, `AI-009`) → `PROHIBITED`.
- Otherwise, severity counts and weighted scores → `HIGH_RISK` / `LIMITED_RISK` / `MINIMAL_RISK`.

There is no LLM call. There is no confidence score. There is no uncertainty to gate on. The HITL branch literally had no trigger to fire on after the pivot, so it was removed rather than left dangling.

This is documented in `supervisor.py`'s top-of-file docstring:

> *No HITL branch: static scanners produce deterministic, auditable evidence, so there is no classification-uncertainty branch to pause on.*

## 3. The three-sentence answer (for interview use)

> The pre-pivot system used an LLM-based classifier whose categorical outputs had no calibrated confidence, so we added a HITL pause for Critical findings to let a human override low-confidence categorisations. When we pivoted to a static scanner with a deterministic rule classifier, the trigger condition for the pause disappeared — there's no uncertainty score to gate on. We chose to remove the branch rather than retain a pause that fires either always-on or never, because a pause that adds latency without adding judgment is anti-pattern. The mitigation is in the artifact: every finding is traceable to a YAML rule and a `file:line` anchor, so a downstream compliance officer can dispute or override any classification from the report itself — they just don't need to be *blocking* the pipeline to do it.

## 4. The EU AI Act counter-argument and the response

**The counter-argument:** EU AI Act Article 14 mandates "human oversight" for high-risk AI systems, and Recital 73 emphasises that oversight must allow the human to "decide not to use the high-risk AI system" or to "override or disregard" its output. A compliance-engineering tool that produces high-risk classifications without a human-in-the-loop checkpoint looks superficially out of step with the regulation it's mapping codebases against.

**The response:** Article 14 imposes the oversight obligation on the *operator of a high-risk AI system*. AlloyCode is not a high-risk AI system; it's a *static analysis tool* that produces a report. The unit of analysis Article 14 governs is the system being scanned, not the scanner. The scanner's job is to surface evidence; the operator's job (the compliance officer reviewing the report) is the oversight. AlloyCode's reports are designed to make that downstream oversight cheap: every finding has a code anchor, a rule, an article citation, and a severity, all of which a human can dispute from the artifact without needing to be inside the pipeline.

A useful analogue: `mypy` doesn't have a HITL approval gate. Its job is to surface evidence; the human reads the report and decides. Adding HITL to `mypy` would be a category error, and adding it to AlloyCode is the same category error one layer up.

If AlloyCode were ever positioned as an *enforcement* component (e.g., a CI gate that blocks merges on Critical findings), the equation would change — but blocking-mode is then the wrapping CI's responsibility (the GitHub Action calling AlloyCode would be the place to add the gate), not AlloyCode's.

## 5. What would change this decision

Re-add HITL if any of the following become true:

1. **A user surfaces a real need to override classifications inside the pipeline** rather than post-hoc on the report. (Today: zero users; the report-side workflow has not been exercised.)
2. **The classifier becomes non-deterministic** — e.g., a future scanner adds LLM-based pattern detection with confidence scores. Then a confidence-threshold gate becomes meaningful.
3. **The product is repositioned as an enforcement / CI-blocking tool** and the blocking gate is moved inside AlloyCode rather than its wrapping CI step. Adds a real "should this merge proceed?" decision the pipeline can pause on.

Until any of these fires, see [`../NORTHSTAR.md`](../NORTHSTAR.md) Part IV — "Skill-agents / sub-agent architecture inside the orchestrator." HITL falls in the same correctly-deferred bucket: not a bad idea, just not earning time given the current state.
