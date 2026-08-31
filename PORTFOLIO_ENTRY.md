# Portfolio Entry — ArticleTrace Compliance Scanner

Field-by-field values for the portfolio website form, reflecting the
current (post-pivot) state of the project. Replaces the prior
"Smart Graph RAG" entry, which described the pre-pivot free-text
assessment system that has since been retired.

---

## ID (Slug)

```
articletrace-compliance-scanner
```

**Old:** `smart-graph-rag`.

The project pivoted from free-text RAG Q&A to static repo compliance
scanning. The slug should describe the actual product, not the
internal retrieval mechanism. ArticleTrace is the product name; "scanner"
is the verb. URL-safe, lowercase, hyphenated.

---

## Category

```
AI
```

Alternatives if the portfolio supports multi-category:
`Developer Tools`, `Compliance / Legal Tech`. Stick with AI as the
primary because the project's headline differentiator is *scanning AI
codebases* — security/compliance scanners exist for many domains, but
this one is AI-specific.

---

## Title

```
ArticleTrace: Static Scanner for EU AI Act & GDPR Compliance
```

**Old:** `Smart Graph RAG: Navigating the EU AI Act & GDPR`.

The old title led with "RAG" — that's now an internal implementation
detail, not the user-facing pitch. Reviewers don't open a project
because it uses RAG; they open it because it solves a concrete
problem. Lead with the problem (compliance), the action (static
scan), and the scope (EU AI Act + GDPR).

Under 70 characters so it doesn't truncate in card layouts.

---

## Short Description

```
Static analysis scanner that maps AI codebases to concrete EU AI Act
and GDPR obligations with file-and-line precision.
```

One sentence. The reviewer reads this in a card layout and decides
whether to click. Three things it must do:

1. Name the action (static analysis scanner).
2. Name the input + output (AI codebases → regulatory obligations).
3. Name the differentiator (file-and-line precision).

---

## Long Description

```
ArticleTrace is a static compliance scanner for AI codebases. Point it at
a GitHub repo and it returns a structured report of likely regulatory
violations — each finding linked to the exact file and line number,
mapped to the specific EU AI Act / GDPR articles the code triggers,
and accompanied by suggested remediation.

The system fills a gap in the AI-governance tooling landscape.
Existing tools either collect self-reported answers (Credo AI,
Holistic AI), audit runtime behavior with training-data access
(Fairlearn, AIF360), or validate LLM outputs (Guardrails AI). None
statically read AI application code against regulatory obligations.
ArticleTrace does.

Architecturally, scanning is deterministic and fast: AST analysis,
import detection, and file-pattern matching find facts in the code.
Those facts are then enriched against a 2,301-node knowledge graph
of EU AI Act and GDPR structure (articles, recitals, obligations,
definitions, case law) hosted in Neo4j with a native HNSW vector
index over 2,198 embedded obligations. A LangGraph multi-agent
workflow (Risk Classifier, Technical Assessor, Legal Research,
Documentation Generator) orchestrates the analysis; hybrid graph +
vector retrieval (Reciprocal Rank Fusion) finds the relevant
articles for each detected pattern. Gemini synthesizes the
human-readable narrative — LLMs are kept out of the detection hot
path so findings stay deterministic and explainable.
```

About 1,500 characters. If the portfolio caps at 1,000, drop the
landscape paragraph and keep the architecture paragraph.

---

## Tech Stack

```
Neo4j (graph + native vector index)
Gemini 2.5 Flash
gemini-embedding-001 (3072-dim)
LangGraph
FastAPI
Next.js 16
PostgreSQL (Supabase)
Redis
Docker
Cloud Run
Python uv
GitPython
```

**Removed from the old stack:**

- `ChromaDB` — migrated away first to a JSON-backed store, then
  Weaviate, finally consolidated into Neo4j's native vector index.
- `NetworkX` — graph operations now run as Cypher inside Neo4j; the
  in-memory graph library is no longer used.
- `LangChain` — replaced by LangGraph for the multi-agent workflow,
  which is the only orchestration surface that matters.
- `React Flow` — verify whether the frontend still renders the
  citation network this way; if no live visualization is shipped,
  drop it from the list. Don't list libraries the demo doesn't
  exercise.

**Order matters.** The first three items are the technical
differentiators (graph DB + native vectors, modern Gemini, multi-agent
LangGraph). Put those first; infrastructure (Docker, Cloud Run) goes
last.

---

## Key Features

```
1. Static AST + import scanning of GitHub repos against 10
   deterministic compliance rules.
2. File:line anchors with EU AI Act and GDPR article citations for
   every finding.
3. 2,301-node knowledge graph + 2,198 embedded obligations with
   hybrid graph + vector retrieval (RRF fusion).
4. LangGraph multi-agent workflow: risk classification, technical
   assessment, legal research, documentation generation.
5. Human-in-the-loop approval for Critical findings; downloadable
   JSON / markdown reports.
6. Generates DPIA / ROPA / conformity scaffolds tied to detected
   violations.
```

Each feature is one line and starts with a noun (the user-visible
capability), not the framework. "Static AST scanning" not
"using LibCST and tree-sitter." Reviewers want to know what the
product does, not what it imports.

---

## Image URL

```
/assets/project_card/ArticleTrace-Compliance-Scanner.png
```

You need a new image. The old one (`Smart Graph RAG.png.png`) is
outdated and the double `.png.png` extension reads as careless.
Three good candidate compositions:

1. **Architecture diagram** — three-tier box drawing showing
   frontend → orchestrator → knowledge_engine → Neo4j, with arrows
   labeled `POST /api/v1/scans` and `POST /api/v1/hybrid/search`.
   Same shape as the diagram in [`devlog/SYSTEM.md`](devlog/SYSTEM.md) §1.
   Shows technical depth.
2. **Scan result UI screenshot** — the report page with a real
   finding: `frontend_api/src/face_client.ts:10 — import * as faceapi
   from "@vladmandic/face-api"` mapped to `AI Act Art 5(1)(h)`. Shows
   the product working.
3. **Knowledge graph visualization** — the 2,301-node citation graph
   rendered (e.g. via Neo4j Browser or the frontend's `/knowledge`
   page if it exists). Shows the data scale.

Pick one. (2) is the strongest because it shows the actual deliverable
— a finding with a citation. (1) shows architectural sophistication.
(3) is visually impressive but doesn't tell the story by itself.

Aspect ratio matches whatever the portfolio site expects (commonly
16:9 or 4:3, around 1200×675 or 1200×900). PNG with transparency only
if the portfolio has a non-white background.

---

## GitHub URL

```
https://github.com/sahabajalam/gdpr
```

**Old:** `https://github.com/sahabajalam/eu-ai-gdpr-rag`.

The old URL doesn't match the actual remote (verified via
`git remote -v`). Update to the live repo. Before the portfolio entry
goes live, run a checklist on the repo:

- README at the root opens with what the project does in one
  paragraph (you have [`devlog/SYSTEM.md`](devlog/SYSTEM.md) — consider
  symlinking or copying its top section into the root README so
  GitHub's project page shows it).
- A live `main` branch builds without errors.
- License file present (MIT or Apache 2 are conventional).
- No leaked `.env` files or credentials in history (already verified
  — `.env` is in `.gitignore`).

---

## Demo URL

```
(pending Cloud Run deploy)
```

The old `https://euaigdpr.web.app/` was Firebase Hosting — that domain
may still resolve to a stale build of the old free-text UI.

The new deploy will land at a Cloud Run URL like
`https://aegis-frontend-<hash>.europe-west1.run.app` (or whatever the
custom domain ends up being). Until `./gcp.ps1 -Action deploy`
finishes on the `gdpreuai` project, leave this field blank rather
than point to the old Firebase URL — a stale demo is worse than no
demo for portfolio review.

If the deploy isn't ready in time, two interim options:

1. Replace Demo URL with a 60-second screen-recording walkthrough
   (Loom / YouTube unlisted) showing a real scan from URL paste to
   findings report.
2. Hide the Demo URL field entirely and let GitHub URL carry the
   reviewer.

---

## Update sequence (do this in order)

1. **Replace the image asset** in `/assets/project_card/`. Delete the
   old `Smart Graph RAG Navigating the EU AI Act GDPR.png.png`.
2. **Update slug, title, descriptions** before tech stack — they're
   the most visible.
3. **Update GitHub URL** to the real remote.
4. **Defer Demo URL** until deploy is green; come back to it.
5. **Tech stack and features** can update last; they're internal
   accuracy, not the headline.
