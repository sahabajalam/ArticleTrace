# EU AI Regulatory Knowledge Base — Standalone Project Context

## For Independent Development, Future Integration, and Portfolio Demonstration

> **Date**: 2026-02-10
> **Status**: Pre-build (design document)
> **Integration Target**: EU AI Regulatory Compliance Engine (3-core architecture)

---

## Table of Contents

1. [Why This Knowledge Base Exists](#1-why-this-knowledge-base-exists)
2. [What Problem It Solves](#2-what-problem-it-solves)
3. [How It Will Be Used](#3-how-it-will-be-used)
4. [Reusability Assessment of Existing core_2 Code](#4-reusability-assessment-of-existing-core_2-code)
5. [Standalone Project Scope](#5-standalone-project-scope)
6. [Raw Data Inventory](#6-raw-data-inventory)
7. [Knowledge Graph Design](#7-knowledge-graph-design)
8. [Vector Store Design](#8-vector-store-design)
9. [Query Interface Contract](#9-query-interface-contract)
10. [Integration Points](#10-integration-points)
11. [Build-First, Integrate-Later Strategy](#11-build-first-integrate-later-strategy)

---

## 1. Why This Knowledge Base Exists

### The Regulatory Problem

The EU has enacted two massive, interlocking legal frameworks that govern AI systems:

1. **General Data Protection Regulation (GDPR)** — Effective May 2018. Governs the processing of personal data. 99 articles, 173 recitals, enforced by ~30 national Data Protection Authorities across the EU.

2. **EU AI Act (Regulation 2024/1689)** — Effective August 2024 (tiered enforcement through 2027). The world's first comprehensive AI regulation. 113 articles, ~180 recitals, 13 annexes. Creates a risk-based classification system for AI systems with escalating requirements.

**The compliance challenge is three-dimensional:**

- **Volume**: ~212 articles, ~353 recitals, 13 annexes, plus guidelines, case law, and enforcement precedents — no human can hold this in their head.
- **Cross-regulation**: The AI Act explicitly builds on GDPR. A single AI system (e.g., facial recognition for employee attendance) triggers obligations from BOTH regulations simultaneously — different articles, different penalty tiers, different competent authorities.
- **Interpretive depth**: The raw articles are insufficient. Understanding what "high-risk" means requires reading Annex III. Understanding what a DPIA requires needs recital context plus EDPB guidelines. Understanding consequences requires enforcement precedents.

### Why a Knowledge Base (Not Just a Document Store)

A naive approach would be: dump all the legal text into a vector database, do RAG, call it a day.

That fails catastrophically for legal compliance because:

| What you need | What vector search gives you | What's missing |
|---|---|---|
| "What obligations apply to a provider of a high-risk AI system?" | Semantically similar text chunks | The STRUCTURAL chain: Art 6 → Annex III → Art 9-15 → Art 43 → Annex VII. A vector search returns fragments. A graph traversal returns the complete obligation chain. |
| "Can we process biometric data as part of AI training?" | Paragraphs mentioning biometric data | The CROSS-REGULATION logic: GDPR Art 9 says no (special category), but AI Act Art 10(5) creates a narrow exception for bias detection. You need to traverse across two legal frameworks. |
| "What happened to companies that deployed facial recognition without consent?" | Text about facial recognition | The PRECEDENT chain: Clearview AI was fined €90.5M by multiple DPAs → violations of specific GDPR articles → those same articles apply to your system. |
| "What is the definition of 'AI system' and does our product qualify?" | The definition text | The DEFINITIONAL chain: AI Act Art 3(1) defines "AI system" → Art 6 classifies risk → Annex III maps use cases → specific articles impose requirements per risk level. |

**The knowledge base must be a GRAPH, not a flat document store.** The graph captures relationships between legal provisions — containment, cross-reference, obligation, exemption, interpretation, enforcement. The vector store supplements the graph for semantic discovery (finding the right entry point when the user doesn't know specific article numbers).

### Portfolio Value

This is not just a compliance tool. It demonstrates:

- **Data engineering**: ETL pipeline parsing irregular legal text into structured entities
- **Knowledge graph design**: Domain-specific ontology for regulatory law
- **Semantic extraction**: LLM-assisted extraction of obligations, exemptions, conditions from natural language
- **Hybrid retrieval**: Graph traversal + vector search + Reciprocal Rank Fusion
- **Applied NLP**: Embedding strategies for legal text, chunking strategies for different entity types
- **System integration**: Clean API contract that multiple consumers can use

---

## 2. What Problem It Solves

### For the Compliance Engine (Integration Target)

The EU AI Regulatory Compliance Engine is a 3-module platform:

| Module | Role | What it needs from the KB |
|---|---|---|
| **Core 3 — Compliance Agent** | Orchestrates 5 LangGraph agents that classify risk, research law, check compliance, recommend actions, generate documents | **Primary consumer.** Agents query the KB to find applicable articles, obligations, exemptions, and precedents for a given AI system. |
| **Core 1 — Monitoring & Governance** | Tracks compliance decisions, monitors for drift, logs agent behavior | **Audit trail.** Needs to know which KB entities (articles, obligations) were cited in each compliance decision. |
| **Core 2 — GraphRAG Engine** | Currently hosts the graph/vector stores and retrieval logic | **Becomes the thin API wrapper** around the standalone KB once integrated. |

### For the End User

An AI developer or compliance officer describes their system ("We're building a facial recognition system for employee attendance at our Munich office, processes live camera feeds, uses deep learning, fully automated decisions about access").

The knowledge base enables the system to:

1. **Classify risk** — Traverse: facial recognition → BiometricIdentification → Annex III.1 → HIGH_RISK. Also: employee attendance → Employment → Annex III.4 → HIGH_RISK.
2. **Find all applicable obligations** — Traverse from HIGH_RISK classification through all requirement articles (Art 9–15, Art 43), plus GDPR DPIA requirement (Art 35), plus GDPR lawful basis (Art 6, Art 9).
3. **Check for prohibitions** — Traverse: real-time biometric → public space check → Art 5 prohibited practices. In this case, workplace is NOT public space, so not prohibited — but the KB captures this exemption path.
4. **Find exemptions** — "Can we process biometric data for this?" → GDPR Art 9(2)(a) explicit consent, or AI Act Art 10(5) bias detection. The KB captures both paths.
5. **Cite precedents** — "What happened to others?" → Clearview AI fined €90.5M for facial recognition without consent → specific article violations → those map to your system.
6. **Generate compliance documents** — DPIA, conformity assessment, ROPA entries — all require knowing which specific articles and obligations apply.

### What the KB Does NOT Do

- It does NOT make compliance decisions — that's the agent's job
- It does NOT store user data or system profiles — that's Core 1/Core 3's job
- It does NOT generate documents — that's the document agent's job
- It IS the authoritative source of regulatory knowledge that all other components query

Think of it as **the law library that the compliance lawyer consults** — complete, structured, navigable, but not the lawyer itself.

---

## 3. How It Will Be Used

### Query Patterns (Most Frequent → Least Frequent)

#### Pattern 1: Anchor → Traverse → Collect Obligations
```
Input: "What obligations apply to a HIGH_RISK AI system?"
Query: MATCH (rc:RiskCategory {name: "HIGH_RISK"})<-[:CLASSIFIED_AS]-(ast:AISystemType)
       MATCH (rc)-[:REGULATED_BY]->(art:Article)-[:REQUIRES]->(obl:Obligation)
       RETURN ast, art, obl
Output: List of all obligations with source articles, organized by actor (provider vs deployer)
```

#### Pattern 2: Data Type → Regulation → Requirements
```
Input: "We process biometric employee data"
Query: MATCH (dt:DataType {name: "BiometricData"})-[:REGULATED_BY]->(art:Article)
       MATCH (art)-[:REQUIRES|PROHIBITS]->(obl:Obligation)
       OPTIONAL MATCH (art)-[:HAS_EXCEPTION]->(exm:Exemption)
       RETURN art, obl, exm
Output: GDPR Art 9 prohibition + its exemptions + AI Act Art 10(5) bias exception
```

#### Pattern 3: System Description → Risk Classification
```
Input: "Facial recognition for employee attendance"
Query: MATCH (ast:AISystemType) WHERE ast.name CONTAINS "biometric" OR ast.name CONTAINS "facial"
       MATCH (ast)-[:CLASSIFIED_AS]->(rc:RiskCategory)
       MATCH (ast)-[:REGULATED_BY]->(art:Article)
       RETURN ast, rc, art
Output: HIGH_RISK (Annex III.1 + Annex III.4), with all relevant articles
```

#### Pattern 4: Cross-Regulation Requirements
```
Input: "What GDPR requirements ALSO apply when I'm already complying with AI Act?"
Query: MATCH (a1:Article {regulation_id: "EU_AI_ACT"})-[:COMPLEMENTS]->(a2:Article {regulation_id: "GDPR"})
       MATCH (a2)-[:REQUIRES]->(obl:Obligation)
       RETURN a1, a2, obl
Output: The complete GDPR overlay on top of AI Act compliance
```

#### Pattern 5: Penalty Lookup
```
Input: "What's the maximum fine for deploying prohibited AI?"
Query: MATCH (art:Article {id: "AIACT_ART_5"})-[:ENFORCED_BY]->(pen:Penalty)
       RETURN art, pen
Output: €35M or 7% global turnover (Art 99(3))
```

#### Pattern 6: Precedent Research
```
Input: "Has anyone been fined for what we're doing?"
Query: MATCH (enf:EnforcementAction)-[:CITES]->(art:Article)
       WHERE art.id IN [<list of articles applicable to user's system>]
       RETURN enf, art
Output: Relevant enforcement actions with fines, violations, and outcomes
```

#### Pattern 7: Semantic Search + Graph Expansion (Hybrid)
```
Input: Free-text query "transparency requirements for chatbots"  
Step 1 (Vector): Find top-5 semantically similar chunks → AIACT_ART_50, AIACT_REC_132, etc.
Step 2 (Graph): Expand from those anchors via graph traversal → related obligations, actors, penalties
Output: Complete answer with citations
```

### Consumers

| Consumer | How it queries | What it expects back |
|---|---|---|
| **Risk Classifier Agent** (Core 3) | Sends system capabilities → expects risk classification with evidence trail | List of (AISystemType, RiskCategory, source Article, Annex) tuples |
| **Legal Research Agent** (Core 3) | Sends legal query → expects authoritative answer with citations | Answer text + list of cited entities (articles, recitals, guidelines) |
| **Compliance Checker Agent** (Core 3) | Sends (system_profile, obligation_list) → expects gap analysis | List of (obligation, status: MET/UNMET/PARTIAL, evidence) |
| **Recommendation Agent** (Core 3) | Sends gaps → expects remediation guidance | Linked articles + guidelines + enforcement warnings |
| **Document Generator Agent** (Core 3) | Sends obligation set → expects structured content for DPIA/ROPA | Organized obligations, citations, recital context |
| **API Users** (direct) | REST API queries for legal research | Structured JSON with entities, relationships, citations |

---

## 4. Reusability Assessment of Existing core_2 Code

### The Honest Verdict: **Build Fresh, Borrow Ideas**

I audited every file in core_2/src/ and core_2/scripts/. Here's the file-by-file assessment:

#### ✅ REUSE — Worth Adapting (3 files)

| File | Lines | What's Good | What Needs Changing |
|---|---|---|---|
| **`config.py`** (50 LOC) | Clean Pydantic settings pattern | Change to standalone config (remove Core 2 API settings, add KB-specific settings). The pattern is good, the specific settings need updating. |
| **`retrieval/engine.py`** (303 LOC) | Solid RRF implementation. The `reciprocal_rank_fusion()` function is textbook-correct. Hybrid search pattern is sound. | Needs richer metadata handling. Current version only passes basic entity metadata. New version needs regulation_id, chapter, article_number, modality filters. |
| **`retrieval/reasoning.py`** (401 LOC) | Multi-hop reasoning pattern is architecturally correct. Seed → Expand → Reason → Cite workflow is right. | The LLM prompt is too generic. Needs domain-specific prompts for each query pattern. But the orchestration logic is reusable. |

#### ⚠️ PARTIAL — Structural Skeleton Only (3 files)

| File | Lines | What's Usable | What's Broken |
|---|---|---|---|
| **`graph/schema.py`** (165 LOC) | Entity/Relationship Pydantic models are well-structured. Enum pattern for types is correct. | **Missing 5 entity types** (Exemption, CaseLaw, Guideline, EnforcementAction, Chapter). Missing 6 relationship types. Need to add ~15 new fields across entity subclasses. About 60% needs rewriting. |
| **`stores/graph_store.py`** (368 LOC) | Neo4j connection management, session context manager, index creation, Cypher query patterns are all correct. | **Critical bug**: `_record_to_entity()` at line ~350 always returns base `Entity` class, dropping all subclass fields (full_text, article_number, obligations, etc.). Every entity comes back as a skeleton. This must be fixed. Also needs batch operations for loading 2000+ nodes. |
| **`stores/vector_store.py`** (302 LOC) | ChromaDB connection, embedding generation, basic search are fine. | **Missing**: multiple collections (current uses single "legal_entities" collection), rich metadata in chunks, search prefix strategy, filtered search by regulation/chapter/modality. The `_entity_to_text()` at line ~290 creates terrible embeddings: `"Type: Article\nName: Article 35\nDescription: DPIA"` — this will retrieve poorly. |

#### ❌ DO NOT REUSE — Rebuild From Scratch (4 files)

| File | Lines | Why Not |
|---|---|---|
| **`graph/extraction.py`** (443 LOC) | **Fundamentally wrong approach.** The `RuleBasedExtractor` uses simple regex to find articles in free text (`r"Article\s+(\d+[a-z]?)"`) — but our raw data already has articles delimited by `=== ARTICLE N ===`. We don't need regex to FIND articles, we need to PARSE already-delineated articles into structured entities. The `LLMExtractor` sends truncated text (8K chars) with a generic prompt and returns flat entities — no paragraph-level extraction, no obligation conditions, no cross-references. The `HybridExtractor` just merges both by ID — no quality comparison, no conflict resolution. |
| **`scripts/load_data.py`** (276 LOC) | **Wrong data format.** Loads from the existing tiny JSON files (14 GDPR articles, 11 AI Act articles — summaries, not full text). The `create_cross_regulation_relationships()` function hardcodes 7 relationships. We need a parser that handles 89 raw text files, extracts ~2,225 entities, and builds ~3,700 relationships. |
| **`scripts/evaluate.py`** | Not audited in detail, but depends on the tiny test dataset. Will need complete rewrite for the golden query test suite. |
| **`api/main.py`** (371 LOC) | This is the FastAPI wrapper. It's well-structured, but it's an API layer — not a KB construction concern. We build the KB first, then decide what API shape to expose. |

### Summary Decision Matrix

```
┌─────────────────────────┬──────────┬──────────────────────────────────────────┐
│ Component               │ Decision │ Rationale                                │
├─────────────────────────┼──────────┼──────────────────────────────────────────┤
│ Config pattern          │ BORROW   │ Good pattern, new settings               │
│ Schema (Pydantic)       │ REWRITE  │ Need 60% more entity types and fields    │
│ Graph store (Neo4j)     │ PARTIAL  │ Connection good, roundtrip broken        │
│ Vector store (Chroma)   │ PARTIAL  │ Connection good, embedding strategy bad  │
│ Retrieval engine (RRF)  │ BORROW   │ Algorithm correct, needs richer metadata │
│ Reasoning engine        │ BORROW   │ Pattern correct, needs domain prompts    │
│ Extraction pipeline     │ REBUILD  │ Completely wrong approach for our data   │
│ Data loading            │ REBUILD  │ Wrong data format, wrong scale           │
│ API layer               │ DEFER    │ Build KB first, API later                │
└─────────────────────────┴──────────┴──────────────────────────────────────────┘
```

### My Recommendation: Build Standalone, Then Replace core_2's Data Layer

**Build the KB as an independent project. When it's validated:**
1. Replace `core_2/src/graph/schema.py` with the new schema
2. Replace `core_2/src/stores/` with improved store implementations
3. Replace `core_2/data/` entirely with the new parsed data
4. Keep `core_2/src/retrieval/` as the retrieval layer, adapting to new schema
5. Keep `core_2/src/api/` as the API wrapper, adapting endpoints

This gives you:
- **A working KB you can test independently** (no Docker dependencies on Core 1/Core 3)
- **Clean integration** — swap the data layer, keep the service layer
- **No risk of breaking the existing system** during development

---

## 5. Standalone Project Scope

### What the Standalone KB Project Does

```
Raw legal text files (5.7 MB, 89 files)
        │
        ▼
   ┌─────────────────────────────────────────────────┐
   │              PARSING PIPELINE                    │
   │  Text → Structured JSON for all 8 data types    │
   └─────────────────────────┬───────────────────────┘
                             │
                             ▼
   ┌─────────────────────────────────────────────────┐
   │           SEMANTIC EXTRACTION PIPELINE           │
   │  Articles → Obligations, Exemptions, Concepts    │
   │  Cross-references → Relationship edges           │
   │  Definitions → Definition nodes                  │
   └─────────────────────────┬───────────────────────┘
                             │
                             ▼
   ┌─────────────────────────────────────────────────┐
   │              KNOWLEDGE GRAPH (Neo4j)             │
   │  ~2,225 nodes, ~3,700 relationships              │
   │  Legal provisions, obligations, exemptions,      │
   │  actors, data types, risk categories,             │
   │  case law, guidelines, enforcement actions       │
   └─────────────────────────┬───────────────────────┘
                             │
                             ▼
   ┌─────────────────────────────────────────────────┐
   │              VECTOR STORE (ChromaDB)              │
   │  ~3,500 chunks across 5 collections              │
   │  Rich metadata for filtered retrieval            │
   └─────────────────────────┬───────────────────────┘
                             │
                             ▼
   ┌─────────────────────────────────────────────────┐
   │           QUERY INTERFACE (API Contract)          │
   │  Hybrid retrieval, multi-hop reasoning,          │
   │  structured compliance queries                   │
   └─────────────────────────────────────────────────┘
```

### What the Standalone Project Does NOT Include

- No agent orchestration (that's Core 3)
- No monitoring/governance (that's Core 1)
- No user authentication or session management
- No DPIA/ROPA document generation (that's the agent layer)
- No codebase analysis or model card parsing (that's the input layer)

### Standalone Project Directory Structure

```
eu_ai_knowledge_base/
├── README.md
├── pyproject.toml
├── .env.example
├── docker-compose.yml              # Neo4j + ChromaDB only
│
├── raw_data/                       # Copy of Data/ (read-only source)
│   ├── gdpr_chapters/
│   ├── ai_act_chapters/
│   ├── ai_act_annexes/
│   ├── ai_act_recitals/
│   ├── gdpr_recitals/
│   ├── cjeu_case_law/
│   ├── edpb_guidelines/
│   └── enforcement_actions/
│
├── parsed_data/                    # Output of Phase 1
│   ├── legal/
│   │   ├── gdpr_articles.json
│   │   ├── eu_ai_act_articles.json
│   │   ├── gdpr_recitals.json
│   │   ├── ai_act_recitals.json
│   │   └── ai_act_annexes.json
│   ├── interpretive/
│   │   ├── case_law.json
│   │   ├── edpb_guidelines.json
│   │   └── enforcement_actions.json
│   └── entities/                   # Output of Phase 3
│       ├── definitions.json
│       ├── obligations.json
│       ├── exemptions.json
│       ├── concepts.json
│       ├── actors.json
│       ├── data_types.json
│       ├── ai_system_types.json
│       ├── risk_categories.json
│       └── penalties.json
│
├── src/
│   ├── __init__.py
│   ├── config.py                   # Standalone settings
│   │
│   ├── schema/                     # Pydantic models (ground truth)
│   │   ├── __init__.py
│   │   ├── entities.py             # All 19 entity types
│   │   ├── relationships.py        # All 25 relationship types
│   │   └── query_models.py         # Request/response models
│   │
│   ├── parsers/                    # Phase 1: Raw text → JSON
│   │   ├── __init__.py
│   │   ├── base_parser.py          # Shared delimiter parsing logic
│   │   ├── article_parser.py       # GDPR + AI Act articles
│   │   ├── recital_parser.py       # GDPR + AI Act recitals
│   │   ├── annex_parser.py         # AI Act annexes
│   │   ├── case_law_parser.py      # CJEU case law
│   │   ├── guideline_parser.py     # EDPB guidelines
│   │   └── enforcement_parser.py   # DPA enforcement actions
│   │
│   ├── extractors/                 # Phase 3: JSON → Semantic entities
│   │   ├── __init__.py
│   │   ├── definition_extractor.py      # Rule-based from Art 3/4
│   │   ├── obligation_extractor.py      # LLM-assisted from all articles
│   │   ├── exemption_extractor.py       # LLM-assisted from derogation clauses
│   │   ├── concept_extractor.py         # Combined rule + LLM
│   │   ├── cross_reference_extractor.py # Rule-based article citations
│   │   └── cross_regulation_linker.py   # GDPR ↔ AI Act COMPLEMENTS edges
│   │
│   ├── stores/                     # Database interaction layers
│   │   ├── __init__.py
│   │   ├── graph_store.py          # Neo4j (fixed roundtrip, batch ops)
│   │   └── vector_store.py         # ChromaDB (multi-collection, rich metadata)
│   │
│   ├── retrieval/                  # Query layer
│   │   ├── __init__.py
│   │   ├── hybrid_engine.py        # RRF-based hybrid retrieval
│   │   └── reasoning.py            # Multi-hop chain-of-thought
│   │
│   └── validation/                 # Phase 5: Quality assurance
│       ├── __init__.py
│       ├── golden_queries.py       # Golden test suite runner
│       ├── coverage_report.py      # Coverage analysis
│       └── integrity_check.py      # KG ↔ Vector store consistency
│
├── scripts/
│   ├── 01_parse_raw_data.py        # Run Phase 1
│   ├── 02_load_structural_kg.py    # Run Phase 2
│   ├── 03_extract_semantic.py      # Run Phase 3
│   ├── 04_build_vector_store.py    # Run Phase 4
│   ├── 05_validate.py              # Run Phase 5
│   └── run_all.py                  # Full pipeline
│
├── golden_tests/
│   └── test_queries.json           # Expected query → answer pairs
│
└── tests/
    ├── test_parsers.py
    ├── test_extractors.py
    ├── test_stores.py
    ├── test_retrieval.py
    └── test_golden.py
```

### Dependencies

```toml
[project]
name = "eu-ai-knowledge-base"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "neo4j>=5.15.0",
    "chromadb>=0.4.22",
    "google-generativeai>=0.5.0",   # Embeddings + LLM extraction
    "structlog>=24.1.0",
    "tenacity>=8.2.0",              # Retry logic for LLM calls
    "rich>=13.0.0",                 # Progress bars for pipeline
]
```

**No FastAPI, no LangChain, no LangGraph** — those are application-layer concerns.  
The standalone KB is a data engineering + knowledge engineering project.

---

## 6. Raw Data Inventory

### Data Available in Data/ (89 files, 5.7 MB)

| Category | Files | Size | Delimiter | Key Fields | Expected Entities |
|---|---|---|---|---|---|
| GDPR Articles | 11 chapter files | 193 KB | `=== ARTICLE N ===` | Name, Paragraphs, sub-items (a)(b) | 99 Article nodes |
| GDPR Recitals | 1 file | 153 KB | `=== RECITAL N ===` | Full text | 173 Recital nodes |
| AI Act Articles | 13 chapter files | 293 KB | `=== ARTICLE N ===` | Title, Paragraphs, sub-items | 113 Article nodes |
| AI Act Recitals | 1 file | 225 KB | `=== RECITAL N ===` | Full text | 180 Recital nodes |
| AI Act Annexes | 1 file | 46 KB | `=== ANNEX N ===` | Title, structured lists | 13 Annex nodes |
| CJEU Case Law | 20 + 1 compilation + 1 index | 191 KB | `=== CASE: C-NNN/YY ===` | Court, Date, Topic, Provisions, Holding, AI Relevance | 20 CaseLaw nodes |
| EDPB Guidelines | 20 + 1 compilation + 1 index | 4.3 MB | `=== GUIDELINE: ref ===` | Reference, Topics, Tier, Full text | 21 Guideline nodes |
| Enforcement Actions | 15 + 1 compilation + 1 index | 139 KB | `=== ENFORCEMENT: name ===` | Authority, Target, Fine Amount, Violations, AI Relevance | 15 EnforcementAction nodes |

### Data Quality Observations

**Strengths:**
- Consistent delimiter pattern (`=== TYPE: ID ===`) across ALL categories — single base parser possible
- Structured fields within each entry (key-value format)
- Paragraph-level granularity for articles (critical for precise citation)
- Case law and enforcement actions have "AI Relevance" fields — directly usable for cross-linking
- EDPB guidelines include tier classification (Tier 1 = binding authority)

**Weaknesses:**
- GDPR uses "Name:" for article titles; AI Act uses "Title:" — parser must handle both
- Annex structure is irregular (Annex I is a list of harmonisation legislation, Annex III is a categorized list, Annex IV is a document template) — per-annex parsing logic needed
- No explicit recital-to-article mappings in the data — must be extracted from recital text ("as referred to in Article...")
- Guidelines are massive (up to 220 KB each) — need section-level chunking for vector store
- No machine-readable cross-references — must parse "Article 14" mentions from text

---

## 7. Knowledge Graph Design

### 7.1 Ontology: Why These Entities and Not Others

Every entity type exists because it answers a specific question a compliance officer asks:

| Entity Type | Compliance Question It Answers | Example |
|---|---|---|
| **Regulation** | "Which law are we talking about?" | GDPR, EU AI Act |
| **Chapter** | "What section of the law?" | Chapter III: HIGH-RISK AI SYSTEMS |
| **Article** | "What does the law say exactly?" | Article 35: DPIA |
| **Recital** | "What did the legislator intend?" | Recital 91: DPIA for special categories |
| **Annex** | "What are the specific lists/criteria?" | Annex III: HIGH-RISK use cases |
| **Definition** | "What does this term legally mean?" | "AI system" means... |
| **Obligation** | "What MUST we do?" | "The provider SHALL establish a risk management system" |
| **Exemption** | "When does a requirement NOT apply?" | "The prohibition does not apply where..." |
| **Right** | "What rights do affected people have?" | Right to explanation under Art 22 GDPR |
| **Concept** | "What abstract principle is at stake?" | "Transparency", "Human oversight", "Data minimisation" |
| **Actor** | "Who has to do what?" | Provider, Deployer, Controller, DPO |
| **DataType** | "What kind of data triggers extra rules?" | Biometric data, health data, criminal records |
| **AISystemType** | "What category does our system fall into?" | Facial recognition, credit scoring, CV screening |
| **RiskCategory** | "What risk level applies?" | Prohibited, High, Limited, Minimal |
| **Penalty** | "What happens if we don't comply?" | €35M / 7% for prohibited AI (AI Act Art 99) |
| **Authority** | "Who enforces this?" | CNIL, ICO, AI Office |
| **CaseLaw** | "How have courts interpreted this?" | Schrems II (C-311/18): international transfers |
| **Guideline** | "What does the regulator's guidance say?" | WP248: DPIAs |
| **EnforcementAction** | "What happened to companies that violated?" | Clearview AI: €90.5M for biometric scraping |

### 7.2 Provenance Fields (All Entity Types)

Every entity node carries provenance metadata for versioning and auditability:

| Field | Type | Purpose |
|---|---|---|
| `source_url` | `str` | EUR-Lex or official source URL |
| `source_version` | `str` | Document version or consolidated date |
| `loaded_at` | `datetime` | When this entity was loaded into the KG |
| `is_current` | `bool` | Whether this is the latest version (default: True) |
| `superseded_by` | `str \| None` | ID of newer version if superseded |

These fields enable: tracking when EDPB guidelines are updated, marking overturned CJEU rulings, and rebuilding the KG from a known state.

### 7.3 Relationship Types (25)

| Relationship | From → To | Question It Answers |
|---|---|---|
| **CONTAINS** | Regulation → Chapter → Article | "What's inside this?" |
| **PART_OF** | Article → Chapter → Regulation | "What does this belong to?" |
| **REFERENCES** | Article → Article (same regulation) | "What else does this article point to?" |
| **AMENDS** | Regulation → Regulation | "What did this law change?" |
| **REPEALS** | Regulation → Regulation | "What did this law replace?" |
| **DEFINES** | Article → Definition | "Where is this term defined?" |
| **REQUIRES** | Article → Obligation (MUST/SHOULD) | "What does this article require?" |
| **PROHIBITS** | Article → Obligation (MUST_NOT) | "What does this article forbid?" |
| **PERMITS** | Article → Obligation (MAY) | "What does this article allow?" |
| **TRIGGERS** | Condition → Requirement | "When does this requirement activate?" |
| **EXEMPTS** | Exemption → Obligation | "What exception applies?" |
| **APPLIES_TO** | Article → Actor | "Who does this apply to?" |
| **ENFORCED_BY** | Article/Regulation → Authority/Penalty | "Who enforces it and what's the penalty?" |
| **RESPONSIBLE_FOR** | Actor → Obligation | "What must this actor do?" |
| **PROCESSES** | Actor → DataType | "What data does this actor handle?" |
| **PROTECTS** | Right → Person/DataType | "What does this right protect?" |
| **REGULATED_BY** | DataType/AISystemType → Article | "Which articles regulate this?" |
| **CLASSIFIED_AS** | AISystemType → RiskCategory | "What risk class is this?" |
| **MITIGATED_BY** | Risk → Measure | "How is this risk addressed?" |
| **INTERPRETS** | Recital/Guideline/CaseLaw → Article | "What interpretation exists?" |
| **HAS_EXCEPTION** | Article → Exemption | "Does this have exceptions?" |
| **COMPLEMENTS** | Article (Reg A) → Article (Reg B) | "What cross-regulation requirements exist?" Property: `interaction_type` ∈ {REINFORCES, CREATES_EXCEPTION, CO_TRIGGERS, CUMULATIVE, DELEGATES} |
| **SUPERSEDES** | Provision → Provision | "Which provision takes priority?" |
| **PENALISED_BY** | Violation → EnforcementAction | "What enforcement happened?" |
| **CITES** | EnforcementAction/CaseLaw → Article | "Which articles were invoked?" |

### 7.4 Expected Scale

| Metric | Count |
|---|---|
| Total nodes | ~2,225 |
| Total relationships | ~3,700 |
| Avg relationships per Article | ≥4 |
| Cross-regulation edges | ~80-120 |
| Vector store chunks | ~3,500 |

### 7.5 The Graph's Power: A Worked Example

**User says:** "We're building a CV screening AI that ranks job applicants."

**The traversal:**

```
1. Start: "CV screening" → match AISystemType: "Employment AI"
2. Traverse: Employment AI -[CLASSIFIED_AS]-> RiskCategory: HIGH_RISK (Annex III, category 4)
3. Traverse: HIGH_RISK -[REGULATED_BY]-> Article 6: Classification rules
4. Traverse: Article 6 -[REFERENCES]-> Annex III → Annex III.4: "Employment, workers management"
5. Traverse: HIGH_RISK -[REQUIRES]-> All obligation articles:
   - Art 9: Risk management system
   - Art 10: Data governance
   - Art 11: Technical documentation
   - Art 12: Record-keeping
   - Art 13: Transparency
   - Art 14: Human oversight
   - Art 15: Accuracy, robustness, cybersecurity
   - Art 43: Conformity assessment
6. Cross-regulate: Art 14 (Human oversight) -[COMPLEMENTS]-> GDPR Art 22 (Automated decisions)
7. Cross-regulate: Art 10 (Data governance) -[COMPLEMENTS]-> GDPR Art 5 (Data principles)
8. Cross-regulate: "employment decisions" → GDPR Art 9 special categories check
   - If screening considers gender, race, disability → Art 9 prohibition + exceptions
9. Precedent: GDPR Art 22 + automated employment decisions
   → CaseLaw: relevant CJEU rulings on profiling
   → Enforcement: Italian DPA fined Deliveroo for algorithmic discrimination
10. Penalties:
    - AI Act: €15M / 3% (Art 99(4)) for HIGH_RISK non-compliance
    - GDPR: €20M / 4% (Art 83(5)) for rights violations
```

**This gives the compliance agent everything it needs to produce a complete assessment — in one graph traversal.**

A vector-only approach would return scattered paragraphs about "employment" and "AI" and "screening" — requiring the LLM to stitch together the reasoning chain. The graph provides the chain.

---

## 8. Vector Store Design

### Why Both Graph AND Vector

| Scenario | Graph wins | Vector wins |
|---|---|---|
| "What obligations apply to HIGH_RISK AI?" | ✅ Direct traversal from RiskCategory | ❌ Would return random obligation fragments |
| "transparency requirements for chatbots" | ⚠️ Need to know to search AISystemType first | ✅ Semantic match to Art 50 even without knowing the article number |
| "What does 'legitimate interest' mean in context of AI training?" | ⚠️ Need exact term match | ✅ Finds GDPR Art 6(1)(f) + recitals + guidelines semantically |
| "Trace path from biometric data to penalties" | ✅ Multi-hop: BiometricData → Art 9 → Art 83 → Penalty | ❌ Cannot follow structural chains |

**They are complementary.** The vector store finds the entry point. The graph traces the reasoning chain.

### Collection Architecture

| Collection | Content | Chunks | Metadata | Use Case |
|---|---|---|---|---|
| `articles` | Article paragraphs | ~1,500 | regulation, chapter, article_num, title, modality, actors | Primary legal text search |
| `obligations` | Extracted obligations | ~1,000 | regulation, source_article, obligation_type, actors, conditions | "What must I do?" |
| `interpretive` | Recitals + Guidelines + Case law | ~750 | source_type, regulation, article_refs, topics | "What does this mean?" |
| `enforcement` | Enforcement actions | ~60 | authority, target, fine_amount, violations | "What happened to others?" |
| `definitions` | Legal definitions | ~94 | regulation, source_article, term | Term lookup |

### Embedding Strategy

Each entity type gets a specific **document prefix** to improve embedding quality, plus **query-time prefixes** for asymmetric search:

```python
# Document-side prefixes (applied during indexing)
DOCUMENT_PREFIXES = {
    "Article": "EU regulation article: {title} — {text}",
    "Obligation": "Legal compliance requirement: {who} {obligation_type} {what}. Source: {source_article}",
    "Recital": "Legislative interpretation context (Recital {number}): {text}",
    "CaseLaw": "Court ruling on {topic}: {case_name} ({case_number}). Holding: {text}",
    "Guideline": "Regulatory guidance on {topics}: {text}",
    "EnforcementAction": "Enforcement action against {target} by {authority}: {text}",
    "Definition": "Legal definition of '{term}': {definition_text}",
    "Exemption": "Legal exemption from {exempts_from}: {condition_text}",
}

# Query-side prefixes (applied at search time)
QUERY_PREFIXES = {
    "articles": "Find EU regulation about: {query}",
    "obligations": "Find compliance requirement for: {query}",
    "interpretive": "Find legal interpretation of: {query}",
    "enforcement": "Find enforcement precedent for: {query}",
    "definitions": "Find legal definition of: {query}",
}
```

### Chunking Rules

| Entity Type | Strategy | Max Chunk Size | Overlap |
|---|---|---|---|
| Articles | One chunk per paragraph | ~500 tokens | None (paragraph boundaries are natural) |
| Recitals | One chunk per recital | ~300 tokens | None |
| Annexes | One chunk per section/sub-item | ~400 tokens | None |
| Case law | Separate chunks for facts, holding, key_legal_points, practical_impact, ai_relevance | ~400 tokens each | None |
| Guidelines | One chunk per section heading | ~800 tokens | 50 token overlap (sections build on each other) |
| Enforcement | Separate chunks per field | ~400 tokens each | None |
| Obligations | One chunk per obligation | ~200 tokens | None |
| Definitions | One chunk per definition | ~150 tokens | None |

---

## 9. Query Interface Contract

The standalone KB exposes these query capabilities. These become the API contract when integrated into Core 2.

### 9.1 Graph Queries (Cypher-based)

```python
class GraphQueryRequest:
    """Structured graph traversal request."""
    start_entity_id: str | None = None      # Start from known entity
    start_entity_type: str | None = None     # OR start from entity type
    start_entity_name: str | None = None     # OR start from entity name
    relationship_types: list[str] | None     # Filter relationships
    max_hops: int = 3                        # Traversal depth
    target_entity_type: str | None = None    # What are we looking for
    regulation_filter: str | None = None     # GDPR, EU_AI_ACT, or both

class GraphQueryResponse:
    paths: list[GraphPath]                   # Graph traversal results
    entities: list[Entity]                   # Flattened unique entities
    total_paths: int
    execution_time_ms: float
```

### 9.2 Vector Queries (Semantic search)

```python
class VectorQueryRequest:
    query: str                               # Natural language query
    collection: str = "articles"             # Which collection
    top_k: int = 10
    filters: dict[str, Any] | None = None    # Metadata filters

class VectorQueryResponse:
    results: list[VectorResult]              # Ranked results with scores
    total_results: int
    execution_time_ms: float
```

### 9.3 Hybrid Queries (Graph + Vector + RRF)

```python
class HybridQueryRequest:
    query: str
    expand_graph: bool = True                # Expand vector results via graph
    expand_hops: int = 2
    collections: list[str] = ["articles"]    # Which vector collections
    top_k: int = 10

class HybridQueryResponse:
    results: list[HybridResult]              # RRF-fused results
    vector_hits: int
    graph_hits: int
    execution_time_ms: float
```

### 9.4 Compliance-Specific Queries (Built on top of graph + vector)

```python
class RiskClassificationRequest:
    system_capabilities: list[str]           # ["facial_recognition", "attendance"]
    data_types: list[str]                    # ["biometric", "employee"]
    deployment_context: str                  # "workplace"

class RiskClassificationResponse:
    risk_level: str                          # "HIGH_RISK"
    matched_categories: list[AnnexCategory]  # Annex III matches
    source_articles: list[Article]           # Art 6 + specific annexes
    confidence: float

class ObligationLookupRequest:
    risk_level: str
    actor_type: str                          # "provider" | "deployer"
    regulation: str | None                   # "GDPR" | "EU_AI_ACT" | None (both)

class ObligationLookupResponse:
    obligations: list[Obligation]
    source_articles: list[Article]
    exemptions: list[Exemption]              # Applicable exemptions
    penalties: list[Penalty]                 # What happens if you don't comply

class CrossRegulationRequest:
    ai_act_articles: list[str]               # Articles already identified
    
class CrossRegulationResponse:
    gdpr_overlay: list[ArticlePair]          # (AI Act article, GDPR article, rationale)
    additional_obligations: list[Obligation]  # GDPR obligations not in AI Act
```

---

## 10. Integration Points

### How the Standalone KB Becomes Part of the Compliance Engine

```
┌─────────────────────────────────────────────────────────┐
│                  Core 3: Compliance Agent                │
│  (LangGraph Agents)                                     │
│                                                         │
│  Risk Classifier → Legal Researcher → Compliance Check  │
│       │                    │                   │        │
│       └────────────────────┼───────────────────┘        │
│                            │                            │
│                     query via HTTP                       │
└────────────────────────────┼────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 Core 2: API Layer (FastAPI)              │
│                                                         │
│  /api/v1/classify-risk                                  │
│  /api/v1/obligations                                    │
│  /api/v1/hybrid/search                                  │
│  /api/v1/graph/traverse                                 │
│  /api/v1/cross-regulation                               │
│                                                         │
│        Uses the KB internally                           │
└────────────────────────────┼────────────────────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
          ┌──────────┐ ┌──────────┐ ┌─────────────┐
          │  Neo4j   │ │ ChromaDB │ │  KB Python   │
          │  (Graph) │ │ (Vector) │ │   Module     │
          └──────────┘ └──────────┘ └─────────────┘
           2,225 nodes  3,500 chunks  Schema + Query
           3,700 edges  5 collections  Logic
```

### Integration Steps (After KB is Built and Validated)

1. **Copy Schema**: `eu_ai_kb/src/schema/` → `core_2/src/graph/schema.py` (replace)
2. **Copy Stores**: `eu_ai_kb/src/stores/` → `core_2/src/stores/` (replace)
3. **Copy Parsed Data**: `eu_ai_kb/parsed_data/` → `core_2/data/` (replace)
4. **Adapt Retrieval**: Update `core_2/src/retrieval/engine.py` imports + add filtered collections
5. **Add New Endpoints**: Risk classification, obligation lookup, cross-regulation to `core_2/src/api/main.py`
6. **Load Data**: Run KB loading scripts against Core 2's Neo4j + ChromaDB instances
7. **Test**: Run golden query test suite through Core 2 API

### What Core 3 Agents Need to Change

| Current (Broken) | After Integration (Correct) |
|---|---|
| Risk classifier uses hardcoded `PROHIBITED_PATTERNS` list | Risk classifier calls `/api/v1/classify-risk` with system capabilities |
| Legal researcher does generic RAG over 25 articles | Legal researcher calls `/api/v1/hybrid/search` + `/api/v1/graph/traverse` over 2,225 nodes |
| Compliance checker compares against string patterns | Compliance checker calls `/api/v1/obligations` for specific obligation list + checks each |
| No cross-regulation awareness | Cross-regulation agent (or enhanced legal researcher) calls `/api/v1/cross-regulation` |
| No enforcement precedent lookup | Legal researcher includes enforcement collection in search |

---

## 11. Build-First, Integrate-Later Strategy

### Why Build Outside the Project

1. **No infrastructure dependency** — You can develop and test without running the full Docker stack (Core 1 + Core 2 + Core 3 + Neo4j + PostgreSQL + Redis + Prometheus)
2. **Faster iteration** — Change schema, re-run pipeline, validate. No API server restarts.
3. **Clean testing** — Unit test parsers, extractors, stores independently before integration
4. **No risk to existing code** — The current system keeps working while you build the replacement data layer
5. **Clear boundary** — Forces you to define a clean API contract (Section 9) that the integration must satisfy

### Development Workflow

```
Week 1-2: Phase 1 (Parsing) + Phase 2 (Structural KG)
  ├── All parsers written and tested
  ├── All 89 files parsed to JSON
  ├── Structural graph loaded (Regulation → Chapter → Article → Recital)
  └── Validate: node counts, relationship counts, spot-checks

Week 2-3: Phase 3 (Semantic Extraction)
  ├── Definition extraction (rule-based, Art 3 + Art 4)
  ├── Obligation extraction (LLM-assisted, all articles)
  ├── Exemption extraction (LLM-assisted, derogation clauses)
  ├── Cross-reference extraction (rule-based, "Article N" mentions)
  ├── Cross-regulation linking (LLM-assisted with human review)
  └── Validate: obligation counts, source_text verification

Week 3: Phase 4 (Vector Store) + Phase 5 (Validation)
  ├── Chunking pipeline for all entity types
  ├── Embedding generation with search prefixes
  ├── 5 collections populated
  ├── Golden query test suite (≥20 queries with expected answers)
  ├── Coverage reports
  └── KG ↔ Vector store consistency check

Week 4: Integration
  ├── Swap data layer in Core 2
  ├── Update API endpoints
  ├── Update Core 3 agents to use new API
  └── End-to-end test: system description → compliance report
```

### Success Criteria

**The KB is done when:**

1. ✅ All 89 raw text files are parsed with zero data loss
2. ✅ ~2,225 nodes and ~3,700 relationships loaded in Neo4j
3. ✅ ~3,500 chunks across 5 collections in ChromaDB
4. ✅ Every obligation has a verifiable `source_text` from the original article
5. ✅ Golden query test suite passes (≥80% of queries return expected answers)
6. ✅ Coverage report shows ≥95% of articles have at least 1 obligation or cross-reference
7. ✅ Cross-regulation links cover all 8 known GDPR ↔ AI Act intersections
8. ✅ Enforcement actions correctly link to the specific articles violated
9. ✅ Risk classification traversal correctly maps Annex III categories to HIGH_RISK for all 8 use-case areas

**The integration is done when:**

1. ✅ Core 3's risk classifier produces correct results using the KB (not hardcoded patterns)
2. ✅ Core 3's legal researcher returns cited, multi-source answers
3. ✅ End-to-end: "facial recognition for employees" → complete compliance report with GDPR + AI Act obligations, risk classification, enforcement warnings, and remediation steps

---

> **This document is the complete context needed to build the EU AI Regulatory Knowledge Base as an independent project.** It contains the why, the what, the how, and the integration path — everything a developer needs to start building without knowing the rest of the codebase.
