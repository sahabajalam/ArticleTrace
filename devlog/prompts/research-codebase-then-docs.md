---
title: Research the codebase first, then audit docs for gaps
slug: research-codebase-then-docs
scope: portable
status: active
tags:
  - research
  - methodology
  - documentation
  - onboarding
created: 2026-05-20
last_used: 2026-05-20
last_refined: 2026-05-20
origin_session: |
  Bootstrapping the living-docs system for the AlloyCode EU AI Act + GDPR
  compliance scanner. The repo had three disconnected piles of documentation
  (root-level ops docs, a `docs/` dir, and an unreferenced `gdpr context/`
  brainstorm dir). A naive "read all the docs first" pass would have produced
  a Frankenstein mental model mixing 2026-02 claims ("KB is 12% complete")
  with 2026-04 claims ("KB is 100% complete") without knowing which was
  current. The code-first ordering forced a ground-truth pass before being
  polluted by stale narrative. Result: drift points like the supervisor's
  HITL-removal-vs-docs-say-HITL-retained were caught explicitly.
see_also: []
---

# Research the codebase first, then audit docs for gaps

## When to use this

Reach for this when starting fresh on a project that has both code and accumulated documentation, and you suspect (or know) the docs may not perfectly reflect the code. The prompt structurally prevents the "read all the docs and confidently mix timeframes" failure mode by forcing a code-first ground-truth pass. Especially valuable before designing or refactoring documentation: you can't write a good `SYSTEM.md` from a Frankenstein understanding.

Not useful when the codebase is greenfield (no docs to compare) or when you already have a code-grounded mental model and just need to skim the docs.

## Required context to fill in

- `<PROJECT_DIR>` — absolute path to the project root being investigated (example: `d:\projects\my-app\`)
- `<EXTRA_BRAINSTORM_DIRS>` — non-standard documentation directories that hold raw notes / decisions / pre-pivot context the agent might otherwise miss (example: `gdpr context/`, `_notes/`, `_archive/`). Leave empty if the project doesn't have any.
- `<TARGET_METHODOLOGY>` — the playbook / methodology / structure you want to design toward, if any (example: `DOCS_PLAYBOOK.md`, `README structure for OSS release`, `internal RFC template`). Leave empty for pure exploration.

## The prompt

```
First read the codebase at <PROJECT_DIR> to understand the current project.

DO NOT read any document to understand the project. Read and analyse all the
code — source files, config, infrastructure, CI — to build a code-grounded
mental model of what the system IS right now.

Then, separately, read and analyse all the docs / READMEs / markdown files in
the project to understand what is documented and what the gaps are. Also read
every file in <EXTRA_BRAINSTORM_DIRS> (and any other notes / brainstorm /
archive directories you find) to understand the evolution of the project —
how it got to its current shape, what was tried and abandoned, what decisions
were made and why.

The ultimate goal is to <create methodology according to <TARGET_METHODOLOGY>
| design a documentation structure | produce a gap-analysis report>.

Output as a plan. Surface clarifying questions before finalising.
```

## Notes on what works

- **The explicit "DO NOT read docs first" instruction is load-bearing.** Without it, the agent reads docs and code in parallel and produces a synthesis that confidently asserts whichever source happened to be more recent or more emphatic. With it, the agent has to commit to a code-derived model first, then explicitly compare doc claims against that model — making drift visible.
- **Three explicit reading passes (code → docs → evolution) prevent skipping the messiest one.** Brainstorm / pre-pivot dirs are easy for an agent to skim past as "irrelevant." Calling them out by name forces engagement with the actual decision trail.
- **"Ultimate goal" framing channels the research.** Without a stated goal the agent will exhaustively summarise everything. With one, it triages by relevance to that goal.
- **"Output as a plan. Surface clarifying questions before finalising."** Pairs well with plan-mode runtimes (Claude Code's plan mode, Cursor's plan mode). The agent commits to research output before acting, and surfaces choices that would otherwise be guessed.
- **Watch for:** agents that try to combine the three passes for speed. Re-prompt them to keep the passes separate if you see code observations getting blended with doc claims in the first pass.

## Variations (optional)

- **Short version** — drop the `<EXTRA_BRAINSTORM_DIRS>` and `<TARGET_METHODOLOGY>` clauses. Just: *"First read the code; then audit the docs against what you found. Report the gaps."* Use this for quick onboarding to a small project.
- **Deep version** — add an explicit deliverable list at the end: *"Produce (1) a code-only summary, (2) a doc inventory with state-of-each, (3) a gap analysis, (4) a recommended target structure."* Use this when the next step is a major refactor.
- **Review version** — invert the framing: *"Read SYSTEM.md, then audit the code against it. Where do they disagree? The code wins; list the doc fixes."* Use this for periodic drift checks once a living-docs system is in place.

## History

- 2026-05-20: bootstrapping AlloyCode living-docs system (origin session). **Outcome:** caught at least one drift point (HITL approval removed from supervisor.py but still referenced in docs/README.md), produced a 4-phase methodology plan that survived user review with maximalist choices on every decision (distill+preserve archive, relocate operational docs, include v03, bootstrap prompt library) — implying the plan structure itself was sound.
