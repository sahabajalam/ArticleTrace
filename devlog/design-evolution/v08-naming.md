---
version: "08"
title: Canonical name — AlloyCode → ArticleTrace
status: implemented
derives_from: v02-static-scanner-pivot.md
proposed_date: 2026-08-31
decided_date: 2026-08-31
implemented_in:
  - (this commit)
superseded_by: null
owner: Sahabaj Alam
source_of_truth:
  - orchestrator/src/code_analyzer/rules/    # the 26 regulatory references the name must describe
  - devlog/NORTHSTAR.md Part IV              # the refuse-list entry this overrides
ai_guidance: |
  This is a decision record, already implemented. The refusal to rename again
  STANDS — see §5. Argue against this document before proposing a fourth name.
---

# v08 — Canonical name: ArticleTrace

## 0. What this document is

The project has been renamed twice: *Aegis Compliance Engine* → *AlloyCode*
(2026-06-16) → *ArticleTrace* (2026-08-31). NORTHSTAR Part IV explicitly
refuses renaming, so this record exists to show the override was made on
evidence, and to make a fourth rename argue against something concrete rather
than restart the conversation.

## Status

- **State:** `implemented`
- **Decided:** 2026-08-31, by the owner, after research
- **Supersedes:** the naming decision recorded in CHANGELOG 2026-06-16

## 1. Why AlloyCode was wrong

Three collisions, found by research rather than intuition:

| Collision | Severity |
|---|---|
| **alloycode.com** — an operating software consultancy (Raleigh, NC) trading under the exact name | Exact match; the `.com` was unobtainable |
| **[Alloy](https://www.alloy.com/compliance)** — identity/AML fintech, 800+ financial institutions, ships "Agentic AI for KYC and Compliance"; registered trademark in the Scientific & Technological Services class | Direct semantic collision in the same market vocabulary |
| **[Alloy](https://dl.acm.org/doi/10.1145/3338843)** — MIT's formal specification language, whose Analyzer is used for software verification and code security analysis | Anyone in static analysis reads "Alloy" as this first |

Plus `alloy.app` (AI prototyping) and Alloy Software Inc (ITSM). For a static
analysis tool about AI compliance, sitting between the compliance fintech and
the code-analysis language is the worst available position.

## 2. Why not the obvious alternatives

**AnnexIII / AnnexScan / AnnexTrace** were all considered and rejected on one
measurement. The rule catalog makes **26 regulatory references, and exactly one
is Annex III**:

```
AIACT_ART_5 (prohibited practices) ×3   ← most-referenced
AIACT_ART_26                       ×3
GDPR   ART_9/22/6/35/30            ×7
AIACT  ART_11/12/13/14/27/50/52
AIACT_ANNEX_III                    ×1
```

An `Annex*` name describes 1/26th of the product. The flagship result — a
`PROHIBITED` verdict on a face-recognition library — comes from Art 5, not
Annex III. GDPR, roughly half the corpus, has no annexes at all.

`AnnexIII` additionally fails on ergonomics (`pip install annexiii` is
unpronounceable and unspellable — users will type `annex3`, `annexiii`,
`annex-iii`), on availability (`annexiii.com` and `annex3.com` both taken),
and on discoverability: searching "Annex III" returns EUR-Lex, so the project
could never rank for its own name. Naming a product exactly after a legal
provision also reads as semi-official, which sits badly beside a
not-legal-advice disclaimer.

## 3. Why ArticleTrace

**Grounded in the evidence:** 25 of 26 references are Articles, and Articles
are the unit both regulations share.

**Names the differentiator:** every finding is traceable from a `file:line`
anchor to a cited Article, via a YAML rule — as opposed to vibes-based LLM
classification (NORTHSTAR Part V). "Traceability" is also on-domain: AI Act
Art 12 is record-keeping and traceability.

**Available everywhere**, verified 2026-08-31: PyPI free, npm free, **zero**
GitHub repositories, `articletrace.com` and `articletrace.dev` both
unregistered.

## Alternatives considered

| # | Option | Why rejected |
|---|---|---|
| 1 | Keep **AlloyCode** | Three live collisions incl. an operating company at the exact domain |
| 2 | **AnnexIII** | Describes 1/26 of the catalog; roman numerals unusable in package/CLI names; domains taken; unrankable against EUR-Lex |
| 3 | **AnnexScan / AnnexTrace** | Same 1/26 grounding problem; "Scan" is a generic suffix shared with dozens of tools |
| 4 | **Obligo / Obligate** | Best conceptual fit (1,421 obligations span both regulations) but taken across PyPI, npm and `.com` |
| 5 | **ArticleTrace** ✓ | Matches 25/26 references, names the differentiator, fully available |

## Consequences

✅ **Unlocks** — a name that is searchable, unambiguous, and honestly describes
both regulations; clean package and domain namespaces.

⚠️ **Trade-offs** — a third rename costs continuity, and the repository was
public for roughly an hour under the old name (GitHub redirects the old URL).
Cloud Run services remain `aegis-*`; renaming them is still correctly deferred
(Part IV) since they are the *first* name and no inbound links depend on the
second.

❌ **Rules out** — nothing technical. The name appears in no data format, no
API contract, and no persisted record.

## 4. Compatibility kept deliberately

`.alloycode.yml` — the suppression file users place in **their own** scanned
repositories — is a public interface. `_load_suppressions` now accepts
`.articletrace.yml` first and `.alloycode.yml` as a fallback. Renaming it
outright would have silently stopped honouring existing configs: scans would
begin reporting suppressed findings with nothing to indicate why.

Dated entries in `CHANGELOG.md` and `BUG_LOG.md` keep the old name on purpose.
They record what was true when written; rewriting them would make the history
false. Only their document titles were updated.

## 5. This refusal stands

NORTHSTAR Part IV's refusal to rename is reinstated and now cites this
document. A fourth rename must argue against the evidence here — collision
research, the 26-reference measurement, and verified availability — not
against taste. Renaming again without new evidence of that kind is refused.
