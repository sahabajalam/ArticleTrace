---
title: ArticleTrace — Journey
status: living
last_verified: 2026-05-20
source_of_truth: |
  Synthesized from devlog/history/00-history-and-decisions.md, PORTFOLIO_ENTRY.md,
  PROJECT_EXTRACTION.md, and the design-evolution stream. For the polished
  recruiter-facing form-field version, see PORTFOLIO_ENTRY.md at the project root.
ai_guidance: |
  This is the project's narrative for external readers — recruiters, friends,
  OSS visitors. Tells the story without the operational detail. If a fact here
  disagrees with SYSTEM.md, the code wins; bump this doc.
---

# ArticleTrace — the journey

## What it is

**ArticleTrace** is a static compliance scanner for AI codebases. Point it at a public GitHub repo; deterministic scanners detect AI-system patterns — biometric libraries, LLM SDKs, decision-making surfaces, missing model cards — and map each detection to specific EU AI Act and GDPR obligations from a 2,301-node regulatory knowledge graph. The output is a report of likely violations with `file:line` anchors and article citations. Every claim a reviewer can disagree with by opening the file.

Three services: a Next.js 16 frontend, a Python/FastAPI orchestrator (LangGraph supervisor + scanner pipeline), and a Python/FastAPI knowledge engine (Neo4j + hybrid retrieval). Cloud Run deployment.

## Why it exists

Two large regulatory frameworks — GDPR (in force since 2018) and the EU AI Act (effective 2024 with phased rollout) — interlock in ways that compliance teams find expensive to navigate. Industry estimates put a manual AI Act assessment at ~£8,500 and 40 hours per assessment; for a mid-size org doing 15 assessments a year that's ~£1.5M annually with high error variance. Existing AI-governance tools tackle adjacent problems — Credo AI and Holistic AI collect self-reported questionnaires; Fairlearn and AIF360 audit models at runtime; Guardrails AI validates LLM outputs. **Nobody statically scans AI application code against regulatory obligations.** That's the gap ArticleTrace fills.

## The pivot story

The project didn't start where it is now. The first version was a free-text conversational classifier: the user described their AI system in prose, a five-agent LangGraph workflow classified it against the EU AI Act, the system returned a markdown report. It shipped. It worked. It was wrong.

Three problems that no amount of prompt engineering could fix:
- Input was vibes — the user could be vague, wrong, or dishonest, and the classifier had no ground truth to push back against.
- Every demo looked identical (textbox + spinner + markdown), indistinguishable from any LLM-wrapper portfolio project.
- No defensible differentiation against established tools.

The reframe — static scan of real code from real repos — flipped the input from prose to ground-truth-able artifacts. Suddenly every finding cites a `file:line` a reviewer can audit. The knowledge graph stopped being "the thing the chatbot consults" and became "the thing the rules are written against." LLMs left the detection hot path entirely; they now write only the post-hoc narrative.

The decision to pivot is documented in [`design-evolution/v02-static-scanner-pivot.md`](design-evolution/v02-static-scanner-pivot.md), with the alternatives weighed and the trade-offs explicit. The biggest cost: throwing away the HITL approval pause and the entire monitoring service. The biggest gain: a defensible niche.

## The knowledge graph

The technical moat. 2,301 nodes / 4,423 relationships / 2,198 vector embeddings across 7 collections, paragraph-level granularity, cross-regulation edges connecting GDPR provisions to AI Act provisions ("facial recognition" → "biometric data" GDPR Art 9 → "remote biometric ID" AI Act Art 10). Built in-house because no third-party paragraph-granular KB exists. The construction arc — from a 12%-loaded skeleton that failed multi-hop reasoning ~88% of the time, to a fully-built corpus that backs deterministic rules — is documented in [`design-evolution/v03-kb-completion.md`](design-evolution/v03-kb-completion.md).

The graph is queryable through `POST /api/v1/hybrid/reason` on the knowledge engine, but you usually don't query it directly — the orchestrator's `LegalResearchAgent` does that for each scan, anchoring its query on detected code signals so the retrieval is grounded in real evidence rather than vibes.

## Where it stands

The current `devlog/SYSTEM.md` is the authoritative snapshot. As of May 2026:
- Phase 1 ships GitHub-public-repo URL scans, Python-only AST scanners, 10 MVP detection rules, ~30 mapped obligations from the KG, one-pass full-repo scan, web UI.
- Decommissioned: the monitoring module (no production traffic = no signal); the HITL approval pause (no classification uncertainty to gate on); the ChromaDB sidecar (consolidated into Neo4j's native vector index).
- Open work tracked in `design-evolution/`: Conditions/Exceptions as first-class graph nodes, authority weighting instead of numeric confidence, temporal logic for phased provisions, refresh pipeline for EDPB updates.

## What I learned building this

A handful of things worth carrying to the next project:

1. **Ship the wrong version first if you have to.** The free-text version was wrong but it forced the KG schema, the hybrid retrieval, and the LangGraph plumbing to be correct. Without that proving ground, the static-scanner reframe would have been guesswork.
2. **Static beats LLM in any hot path that has to be auditable.** LLMs write the narrative; deterministic scanners produce the evidence. Reviewers trust what they can open in their editor.
3. **A knowledge graph at paragraph granularity is more valuable than a knowledge graph at article granularity.** The difference between "GDPR Art 6 was retrieved" and "GDPR Art 6(1)(f) was retrieved" is the difference between a hallucination and a citation.
4. **Document the pivot, not just the destination.** The `design-evolution/v02` doc is the single most useful artifact in this repo for a reviewer trying to understand what kind of engineer built it.

## For external visitors

- **The product pitch:** [`PORTFOLIO_ENTRY.md`](../PORTFOLIO_ENTRY.md) — field-by-field portfolio-form values.
- **The deep-dive:** [`PROJECT_EXTRACTION.md`](../PROJECT_EXTRACTION.md) — resume bullets, story seeds, tech-stack rundown.
- **The current architecture:** [`SYSTEM.md`](SYSTEM.md) — code-audited, single source of truth.
- **How to run it:** [`DEPLOYMENT.md`](DEPLOYMENT.md) — local dev (UV+npm), Docker, Cloud Run.
- **Why it ended up like this:** this file + [`history/00-history-and-decisions.md`](history/00-history-and-decisions.md).
