# `devlog/` — orientation map

Human-oriented index of what lives where. For agent-oriented read order, see [`../CLAUDE.md`](../CLAUDE.md).

This `devlog/` tree is the **living-docs system** for ArticleTrace, set up per [`../DOCS_PLAYBOOK.md`](../DOCS_PLAYBOOK.md). It's the structural fix for the common "AI agent reads ten stale docs and confidently mixes timeframes" failure.

---

## Top-level docs

- **[`SYSTEM.md`](SYSTEM.md)** — *Living snapshot.* What the system IS right now: architecture, modules, APIs, data layer, deploy targets. Single source of truth. If it disagrees with the code, the code wins; the doc gets fixed.
- **[`CHANGELOG.md`](CHANGELOG.md)** — *Reasoning trail.* Append-only log of intentional changes. Each entry: `What / Why / Impact on SYSTEM.md / Refs`. Pairs with `SYSTEM.md` — every meaningful code change updates both.
- **[`NORTHSTAR.md`](NORTHSTAR.md)** — *Strategy / posture / refuse-list.* The single rule (three tracks: defensibility, production metrics, live demo), N-day targets, the punch list, and the load-bearing **refuse list** of correctly-deferred ideas (fine-tuning, MCP, multi-language, skill-agents, …). Derived from the 2026-06-16 portfolio audit ([`../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md`](../07_MARKET_FIT_AND_PORTFOLIO_AUDIT.md) §6.1 + §7.3). Read this before suggesting new work.
- **[`JOURNEY.md`](JOURNEY.md)** — *Portfolio narrative.* ~600 words for external readers (recruiters, friends, OSS visitors). Tells the story of the pivot, the KB build, the static-scanner thesis.

## Operational docs

- **[`DEPLOYMENT.md`](DEPLOYMENT.md)** — *Accepted reference.* Local dev (UV+npm), Docker Compose, Cloud Run deploy. Cross-references the Mermaid diagram in `SYSTEM.md §6`.
- **[`BUG_LOG.md`](BUG_LOG.md)** — *Living incident log.* The pre-existing `DL-NNN` bug-fix entries. Format: per-incident, newest at top. Distinct from `CHANGELOG.md` (which records intentional changes) — this one records incidents and the fixes that landed.
- **[`METRICS.md`](METRICS.md)** — *Living retrieval metrics.* Quantified numbers from the golden-test runner: citation recall@15, entity recall@15, per-query breakdown. Pull headline numbers from here for CV / README / interview.
- **[`INTERVIEW_GUIDE.md`](INTERVIEW_GUIDE.md)** — *Living defence guide.* 10 line-by-line interview questions with three-sentence answers, follow-up traps, and citable references. Rehearsal material, not architecture reference.

## Design evolution

- **[`design-evolution/`](design-evolution/)** — *Versioned proposals.* RFCs that double as decision records. Read the highest-numbered `vNN-*.md` first. Each carries the dual RFC+ADR shape: `## Status` / `## Alternatives considered` / `## Consequences`. Current state:
  - `v01-baseline.md` — `accepted` — the original free-text RAG architecture (anchors the stream).
  - `v02-static-scanner-pivot.md` — `implemented` — the pivot to a static code scanner.
  - `v03-kb-completion.md` — `implemented` — the KB build-out from 12% to 100%.

## History

- **[`history/`](history/)** — *Frozen archive.* Two files, both `status: archived`:
  - `00-history-and-decisions.md` — distilled narrative (~1500 lines): origin story, project-pipeline realization, major decisions, the pivot, the KB arc.
  - `01-research-arc.md` — preserved primary sources concatenated under section dividers: 4 polished portfolio docs from `gdpr context/main/`, 15 raw brainstorms from `gdpr context/backup/`, 6 pre-pivot docs from the original `docs/archive/`.

  **Do not edit files in `history/`.** Frozen at `snapshot_date: 2026-05-20`. For current state, read `SYSTEM.md`.

## Prompt library

- **[`prompts/`](prompts/)** — *Companion system.* Refined, reusable prompts with frontmatter + status. See [`prompts/README.md`](prompts/README.md) for the save workflow.

---

## How this maps to `DOCS_PLAYBOOK.md`

| Playbook doc type | Path here |
|---|---|
| Entry point | [`../CLAUDE.md`](../CLAUDE.md) |
| #1 Living snapshot | [`SYSTEM.md`](SYSTEM.md) |
| #2 Change log | [`CHANGELOG.md`](CHANGELOG.md) |
| #3 Strategy / posture / refuse-list | [`NORTHSTAR.md`](NORTHSTAR.md) |
| #4 Forward proposals | [`design-evolution/`](design-evolution/) |
| #5 Historical archive | [`history/`](history/) |
| #6 Portfolio narrative | [`JOURNEY.md`](JOURNEY.md) |
| Companion: prompt library | [`prompts/`](prompts/) |

External-facing portfolio docs (`PORTFOLIO_ENTRY.md`, `PORTFOLIO_GUIDE.md`, `PROJECT_EXTRACTION.md`, `16-project-extraction-instructions.md`) and the `DOCS_PLAYBOOK.md` methodology file itself stay at the project root — they are external artifacts or reusable methodology, not living state.
