# EU AI Knowledge Base - Project Memory

## Project Status: COMPLETE (100% — All 8 Phases)

### Final Numbers
| Metric | Count |
|--------|-------|
| Nodes (local graph) | 2,301 |
| Relationships | 4,431 |
| Entity Types | 17 |
| Relationship Types | 13 |
| Vector Documents | 2,132+ (7 collections) |
| Embedding Dimensions | 3,072 |
| COMPLEMENTS (cross-reg) | 84 edges, 5 interaction types |
| Cross-reg concept/right refs | 19 |
| Orphan Nodes | 0 |
| Connectivity | 100% |
| Avg rels/article | 19.1 |
| Unit Tests | 42 passing |
| Golden Tests | 6 test cases |
| Coverage Score | 100% (5/5 checks) |

## Phase Completion Summary

### Phase 0 — Data Audit
- Verified all 88 raw files across 8 categories
- Confirmed 8 delimiter patterns
- Caught guideline count error (21, not 22) and file count (88, not 89) before code was written

### Phase 1 — Parse Raw Data (`01_parse_raw_data.py`)
- 634 entities parsed from raw text files
- 99 GDPR articles + 113 AI Act articles
- 173 GDPR recitals + 180 AI Act recitals
- 13 AI Act annexes, 20 CJEU cases, 21 EDPB guidelines, 15 enforcement actions
- All 8 count checks PASS

### Phase 2 — Structural Knowledge Graph
- `02a_extract_structural_rels.py`: 1,792 structural relationships extracted
- `02b_validate_graph_local.py`: In-memory validation, 0 orphans, 660/660 connectivity
- `02_load_structural_kg.py`: Neo4j loading (Phase 2 only)
- Relationship types: CONTAINS (602), REFERENCES (566), INTERPRETS (303), PART_OF (236), CITES (85)

### Phase 3 — Semantic Entity Extraction
- `03_extract_semantic.py`: 154 rule-based entities
  - 90 definitions (24 GDPR + 66 AI Act, regex from Art 3/Art 4)
  - 18 actors (8 GDPR + 10 AI Act, hand-curated)
  - 17 data types (with PseudonymisedData correctly under PersonalData)
  - 4 risk categories (Prohibited, High, Limited, Minimal)
  - 19 AI system types (8 prohibited + 8 high-risk + 3 limited)
  - 6 penalty tiers (3 GDPR + 3 AI Act)
- `03b_extract_obligations.py`: 1,325 obligations + 96 exemptions
  - Obligation types: SHALL (707), CONDITION (300), MAY (232), MUST_NOT (85), MUST (1)
  - 53% duty bearer detection, 29% condition detection (rule-based only)
- `03c_extract_cross_regulation.py`: 84 COMPLEMENTS edges
  - REINFORCES (32), CO_TRIGGERS (26), CREATES_EXCEPTION (10), DELEGATES (10), CUMULATIVE (6)

### Phase 3e — Concept Extraction (`03e_extract_concepts.py`)
- 47 concepts across 4 categories:
  - GDPR principles (9): lawfulness, fairness, transparency, purpose limitation, data minimisation, accuracy, storage limitation, integrity/confidentiality, accountability
  - Processing operations (10): profiling, automated decisions, pseudonymisation, consent, legitimate interest, international transfer, data breach, joint controllership, DPbD, special category processing
  - Compliance concepts (13): DPIA, prior consultation, records of processing, breach notification, DPO, certification, codes of conduct, one-stop-shop, BCR, SCC, adequacy, supervisory cooperation, processor agreement
  - AI concepts (15): conformity assessment, risk management, human oversight, technical documentation, CE marking, regulatory sandbox, FRIA, data governance, transparency obligation, post-market monitoring, serious incident, record keeping, robustness, GPAI, systemic risk
- 316 relationships (300 APPLIES_TO + 16 REFERENCES cross-concept links)

### Phase 3f — Right Extraction (`03f_extract_rights.py`)
- 19 rights:
  - GDPR (15): transparent info, info (direct/indirect collection), access, rectification, erasure, restriction, notification, portability, object, automated decisions, lodge complaint, effective remedy (SA/controller), compensation
  - AI Act (4): explanation, complaint, effective remedy, AI system disclosure
- 41 relationships (38 APPLIES_TO + 3 REFERENCES cross-regulation links)

### Phase 3 Validation (`03d_validate_full_graph.py`)
- All 16 exit gate checks PASS (expanded from 14 to include Concept >= 40, Right >= 15)
- 2,301 nodes, 4,431 relationships, 0 orphans, 100% connectivity

### Phase 4 — Neo4j Loading (`04_load_full_kg.py`)
- Updated to load concepts + rights (10 entity file sources, up from 8)
- 2,235+ nodes loaded, 4,066+ relationships (COMPLEMENTS deduped by Neo4j)
- 0 orphans, all exit gates PASS
- Connection: `neo4j://127.0.0.1:7687`, user `neo4j`

### Phase 5 — Vector Store (`05_load_vector_store.py`)
- Updated to 7 collections (added concepts + rights)
- 2,132+ documents embedded with `gemini-embedding-001` (3,072 dimensions)
- Collections: articles (212), recitals (353), interpretive (56), definitions (90), obligations (1,421), concepts (47), rights (19)
- JSON-backed vector store (ChromaDB incompatible with Python 3.14)
- Exit gates updated: concepts >= 40, rights >= 15

### Retrieval Engine (`src/retrieval/engine.py`)
- Graph RAG with Reciprocal Rank Fusion (RRF, k=60)
- Dual path: Vector search (semantic) + Graph traversal (structural)
- Searches across all 7 vector collections
- Cross-regulation results verified (GDPR Art 22 + AI Act Art 14, GDPR Art 83 + AI Act Art 99)

### Reasoning Engine (`src/retrieval/reasoning_engine.py`)
- LLM synthesis layer wrapping RetrievalEngine
- Pipeline: retrieve -> classify intent -> build context -> Gemini synthesis -> validate citations -> score confidence
- Intent classification: prohibition, obligation, right, cross_regulation, risk_classification, exemption, general
- Anti-hallucination guardrail: validates all cited articles appear in retrieval results
- Confidence scoring: based on result count (30%), fusion overlap (30%), citation validity (40%)
- Rate limiting: 4s delay (15 RPM free tier)

### Query Models (`src/retrieval/query_models.py`)
- 4 typed request/response pairs:
  - `ComplianceQueryRequest/Response` — general compliance questions
  - `RiskClassificationRequest/Response` — AI system risk classification
  - `ObligationLookupRequest/Response` — obligation/exemption/penalty lookup
  - `CrossRegulationRequest/Response` — GDPR/AI Act interaction analysis
- 6 answer templates: prohibition, obligation, conditional_permission, non_applicable, legal_uncertainty, general
- Pydantic models with Citation, ReasoningStep, ConfidenceLevel

### Golden Tests (`scripts/07_run_golden_tests.py`)
- 6 test cases in `golden_tests/test_queries.json`:
  1. Prohibited AI (social scoring) — expects AIACT_ART_5, RISK_PROHIBITED
  2. Cross-regulation obligations (automated decisions) — expects GDPR_ART_22, AIACT_ART_14
  3. Data subject rights (access) — expects GDPR_ART_15, RIGHT_ACCESS
  4. DPIA+FRIA co-triggering — expects GDPR_ART_35, AIACT_ART_27
  5. Transparency (chatbot) — expects AIACT_ART_50, AIST_CHATBOT
  6. Household exemption — expects GDPR_ART_2
- Validates: retrieval coverage (citations + entities) and answer type matching

### Unit Tests (`tests/`)
- 42 tests passing across 3 test files:
  - `test_extractors.py` (20 tests): ConceptExtractor (7), RightExtractor (7), DefinitionExtractor (2), ObligationExtractor (4)
  - `test_retrieval.py` (22 tests): VectorStore (7), QueryModels (4), ReasoningEngine (11)
- Fixtures in `conftest.py`: sample articles, mock vector store, sample retrieval results

### Coverage Report (`scripts/08_coverage_report.py`)
- 5 checks, all passing (100% score):
  1. 0 orphan nodes
  2. <50% articles with zero obligations (only 2/212)
  3. 84+ COMPLEMENTS edges
  4. 47 concepts (>= 40)
  5. 19 rights (>= 15)
- Reports: entity type distribution, zero-obligation articles, below-average articles, cross-reg coverage

## Architecture

### Entity Types (17)
Regulation, Chapter, Article, Recital, Annex, Definition, Concept, Right, Actor, DataType, RiskCategory, AISystemType, Penalty, Obligation, Exemption, CaseLaw, Guideline, EnforcementAction

### Relationship Types (13)
CONTAINS, PART_OF, REFERENCES, DEFINES, REQUIRES, PROHIBITS, PERMITS, EXEMPTS, APPLIES_TO, ENFORCES, INTERPRETS, CITES, COMPLEMENTS

### COMPLEMENTS Interaction Types (5)
REINFORCES, CO_TRIGGERS, CREATES_EXCEPTION, CUMULATIVE, DELEGATES

## Environment
- **Python**: `C:\Users\SAB\AppData\Local\Python\bin\python3.exe` (3.14.0)
- **Neo4j**: `neo4j://127.0.0.1:7687` (Community 5 with APOC)
- **Gemini SDK**: `google-genai` (new SDK, NOT deprecated `google-generativeai`)
- **Embedding model**: `gemini-embedding-001` (NOT `text-embedding-004`)
- **LLM model**: `gemini-2.0-flash`
- **Vector store**: JSON-backed (ChromaDB incompatible with Python 3.14)
- **Windows console**: ASCII only — no Unicode arrows/checkmarks in print()

## Directory Structure
```
eu_ai_knowledge_base/
  src/
    config.py                    # Pydantic Settings (.env)
    schema/
      entities.py                # 19 entity types, Provenance mixin, entity_from_dict()
      relationships.py           # 25 rel types, InteractionType enum
    parsers/
      base_parser.py             # Shared delimiter parsing
      article_parser.py          # GDPR + AI Act articles
      recital_parser.py          # Recital compilations
      annex_parser.py            # AI Act annexes
      case_law_parser.py         # CJEU case law
      guideline_parser.py        # EDPB guidelines
      enforcement_parser.py      # DPA enforcement actions
    extractors/
      structural_extractor.py    # CONTAINS, REFERENCES, INTERPRETS, CITES
      definition_extractor.py    # Regex from Art 3/Art 4
      rule_based_extractor.py    # Actors, DataTypes, RiskCats, AITypes, Penalties
      obligation_extractor.py    # Obligations + Exemptions (hybrid)
      cross_regulation_extractor.py  # 84 COMPLEMENTS edges
      concept_extractor.py       # 47 concepts (4 categories, keyword matching)
      right_extractor.py         # 19 rights (GDPR + AI Act, cross-reg links)
    stores/
      graph_store.py             # Neo4j CRUD with batch ops
      vector_store.py            # JSON-backed vector store (7 collections)
    retrieval/
      engine.py                  # Graph RAG with RRF fusion
      reasoning_engine.py        # LLM synthesis, intent classification, citation validation
      query_models.py            # 4 request/response pairs, 6 answer templates
  scripts/
    01_parse_raw_data.py         # Phase 1: Parse -> parsed_data/
    02a_extract_structural_rels.py
    02b_validate_graph_local.py  # In-memory validation (no Neo4j)
    02_load_structural_kg.py     # Phase 2: Load structural into Neo4j
    03_extract_semantic.py       # Phase 3a: Rule-based entities
    03b_extract_obligations.py   # Phase 3b: Obligations + Exemptions
    03c_extract_cross_regulation.py  # Phase 3c: COMPLEMENTS
    03d_validate_full_graph.py   # Phase 3: Full validation (16 checks)
    03e_extract_concepts.py      # Phase 3e: 47 concepts
    03f_extract_rights.py        # Phase 3f: 19 rights
    04_load_full_kg.py           # Phase 4: Load everything into Neo4j
    05_load_vector_store.py      # Phase 5: Embed + load vector store (7 collections)
    06_demo_query.py             # Demo: Graph RAG queries (--reason for LLM mode)
    07_run_golden_tests.py       # Golden query test suite (6 cases)
    08_coverage_report.py        # Coverage report (5 checks)
  tests/
    conftest.py                  # Fixtures: sample articles, mock stores
    test_extractors.py           # 20 tests: concept, right, definition, obligation
    test_retrieval.py            # 22 tests: vector store, query models, reasoning engine
  golden_tests/
    test_queries.json            # 6 golden test cases with expected outputs
  parsed_data/
    legal/                       # Articles, recitals, chapters, annexes
    interpretive/                # Case law, guidelines, enforcement
    entities/                    # Definitions, actors, obligations, concepts, rights, etc.
    relationships/               # All relationship JSON files
  chroma_data/                   # Vector store (JSON files, 7 collections)
```

## Known Issues & Gotchas
1. **Modality detection**: First-match "shall not" before "shall" gives wrong results — use frequency-based detection
2. **Paragraphs format**: `article["paragraphs"]` is `dict[str, str|dict]` keyed by para number, NOT a list
3. **Gemini SDK**: `google-generativeai` deprecated, use `google-genai` with `genai.Client()` API
4. **Embedding model**: `gemini-embedding-001` (NOT `text-embedding-004` which 404s on new SDK)
5. **Definition extraction**: 90/94 defs (24/26 GDPR, 66/68 AI Act) — 4 missing use non-standard formatting
6. **Neo4j COMPLEMENTS dedup**: 84 JSON edges -> 76 in Neo4j (bidirectional pairs with same props collapsed)
7. **Orphan node fixes**: CaseLaw (Directive 95/46/EC pattern), Guidelines (scan 20000 chars not 5000), Enforcement (raw text fallback)
8. **ChromaDB**: Incompatible with Python 3.14 (pydantic v1 issue) — use JSON-backed store
9. **Windows console**: `UnicodeEncodeError` with arrows/checkmarks — use ASCII only

## Pipeline Run Order
```bash
# Parse & Extract
python scripts/01_parse_raw_data.py
python scripts/02a_extract_structural_rels.py
python scripts/02b_validate_graph_local.py
python scripts/03_extract_semantic.py
python scripts/03b_extract_obligations.py
python scripts/03c_extract_cross_regulation.py
python scripts/03e_extract_concepts.py
python scripts/03f_extract_rights.py
python scripts/03d_validate_full_graph.py

# Load
python scripts/04_load_full_kg.py --clear
python scripts/05_load_vector_store.py --clear

# Query & Test
python scripts/06_demo_query.py              # Retrieval only
python scripts/06_demo_query.py --reason     # Full reasoning with LLM
python scripts/07_run_golden_tests.py        # Golden test suite
python scripts/08_coverage_report.py         # Coverage report

# Unit tests
python -m pytest tests/ -v                   # 42 tests
```
