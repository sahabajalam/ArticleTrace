# Knowledge Base Construction Plan

## EU AI Regulatory Compliance Engine — Complete Build Specification

> **Date**: 2026-02-10
> **Author**: Lead Data Architect review
> **Scope**: Full knowledge graph + vector store construction from Data/

---

## 1. Raw Data Inventory

### What We Have (88 files, 5.7 MB total)

| Category | Files | Size | Format | Content |
|---|---|---|---|---|
| **GDPR Articles** | 11 chapter files | 193 KB | `=== ARTICLE N ===` delimited, paragraph-level | All 99 articles, full text with paragraphs |
| **GDPR Recitals** | 1 file | 153 KB | `=== RECITAL N ===` delimited | All 173 recitals |
| **EU AI Act Articles** | 13 chapter files | 293 KB | `=== ARTICLE N ===` delimited, paragraph-level | All 113 articles, full text |
| **EU AI Act Recitals** | 1 file | 225 KB | `=== RECITAL N ===` delimited | All 180 recitals |
| **EU AI Act Annexes** | 1 file | 46 KB | `=== ANNEX N ===` delimited | All 13 annexes (I–XIII) |
| **CJEU Case Law** | 20 individual + 1 compilation + 1 index | 191 KB | Structured fields per case | 20 landmark decisions |
| **EDPB Guidelines** | 21 individual + 1 compilation + 1 index | 4.3 MB | Full guideline text + structured headers | 21 key guidelines (19 GL + 2 WP) |
| **Enforcement Actions** | 15 individual + 1 compilation + 1 index | 139 KB | Structured fields per action | 15 major enforcement decisions |

### Data Format Patterns Observed

**Articles** (GDPR & AI Act):
```
Chapter N:
Name: <chapter_name>

=== ARTICLE N ===
Name: <article_title>                    # GDPR uses "Name:", AI Act uses "Title:"
Paragraph 1: <text>
Paragraph 2: <text>
(a) <sub-item>
(b) <sub-item>
```

**Recitals** (both regulations):
```
=== RECITAL N ===
<full recital text as single block>
```

**Annexes** (AI Act):
```
=== ANNEX N ===
Title: <annex_title>
<structured content — lists, sections, sub-items>
```

**Case Law**:
```
=== CASE: C-NNN/YY <name> ===
Full Name: <full case name>
Court: <court>
Decision Date: <YYYY-MM-DD>
Topic: <topic>
Provisions Interpreted: <comma-separated article refs>
Facts: <text>
Holding: <numbered points>
Key Legal Points: <bullet points>
Practical Impact: <bullet points>
AI Relevance: <bullet points>
```

**EDPB Guidelines**:
```
=== GUIDELINE: <reference> ===
Reference: <reference>
Topics: <comma-separated topics>
Tier: <tier classification>
--- PREAMBLE ---
<full guideline text with table of contents, sections, subsections>
```

**Enforcement Actions**:
```
=== ENFORCEMENT: <name> ===
Authority: <DPA name>
Target: <company>
Decision Date: <date>
Fine Amount: <EUR amount>
Fine Category: <GDPR tier>
Violations: <bullet list of GDPR articles>
Facts: <text>
Key Findings: <numbered points>
Corrective Measures: <bullet points>
AI Relevance: <bullet points>
```

---

## 2. The Fundamental Design Decision: KG-First Approach

**We build the knowledge graph to faithfully represent the regulatory domain FIRST, then design input adapters.**

### Rationale

The law defines the structure. The knowledge graph should mirror how EU AI Act and GDPR actually work — not how we think queries might look. This gives us:

1. **Completeness** — Every article, obligation, exemption, and cross-reference is captured regardless of whether we currently have a query for it
2. **Correctness** — The graph's structure follows the law's logic, not our assumptions
3. **Extensibility** — New regulations (AI Liability Directive, ePrivacy) and new input types (codebases, model cards) just need adapters, not schema redesign
4. **Answering the unknown** — The graph can answer questions we haven't thought of yet

### What "KG-First" Means in Practice

```
Phase 0: Data audit — verify raw data matches assumptions (integrity gate)
Phase 1: Parse raw text → structured JSON (ETL)
Phase 2: Build the legal knowledge graph (structural layer)
Phase 3: Extract semantic entities and relationships (semantic layer)
Phase 4: Build vector store over all text (retrieval layer)
Phase 5: Cross-link and validate (integrity layer)
```

> **Note**: SystemProfile → KG matching is an **application-layer concern** (Core 3 agent responsibility), not a KB construction task. It will be designed separately after the KB is validated.

---

## 3. Target Knowledge Graph Schema

### 3.1 Entity Types (19 types)

Extending the existing 14 to 19. Each entity becomes a Neo4j node with a type label.

```
EXISTING (keep as-is):
  Regulation          — GDPR, EU AI Act
  Article             — Individual articles with paragraph-level text
  Recital             — Interpretive context paragraphs
  Annex               — AI Act annexes (I–XIII)
  Definition          — Legal definitions from Art 4 (GDPR) and Art 3 (AI Act)
  Concept             — Abstract concepts (data minimisation, purpose limitation, etc.)
  Obligation          — Must/must-not/should requirements
  Right               — Data subject rights
  Penalty             — Fines and sanctions
  Authority           — Supervisory bodies (DPAs, AI Office, EDPB)
  Actor               — Controller, Processor, Provider, Deployer, Importer, etc.
  DataType            — Personal data, biometric data, health data, etc.
  AISystemType        — Facial recognition, credit scoring, CV screening, etc.
  RiskCategory        — Prohibited, High, Limited, Minimal

NEW (add):
  Exemption           — Specific exemption pathways with conditions
  CaseLaw             — CJEU decisions with holdings and provisions interpreted
  Guideline           — EDPB guidelines with interpretive content
  EnforcementAction   — DPA enforcement decisions with fines and violations
  Chapter             — Chapter-level grouping within a regulation
```

### 3.2 Relationship Types (25 types)

Extending the existing 18 to 25.

```
EXISTING (keep as-is):
  CONTAINS            — Regulation → Article, Regulation → Chapter
  PART_OF             — Article → Chapter, Paragraph → Article
  REFERENCES          — Article → Article (explicit cross-references)
  AMENDS              — Regulation → Regulation
  REPEALS             — Regulation → Regulation
  DEFINES             — Article → Definition
  REQUIRES            — Article → Obligation
  PROHIBITS           — Article → Practice/AISystemType
  PERMITS             — Article → Practice (with conditions)
  TRIGGERS            — Condition → Requirement
  EXEMPTS             — Exemption → Obligation
  APPLIES_TO          — Regulation/Article → Actor
  ENFORCED_BY         — Regulation → Authority
  RESPONSIBLE_FOR     — Actor → Obligation
  PROCESSES           — Actor → DataType
  PROTECTS            — Right → DataType/DataSubject
  REGULATED_BY        — DataType/AISystemType → Article
  CLASSIFIED_AS       — AISystem → RiskCategory
  MITIGATED_BY        — Risk → Measure

NEW (add):
  INTERPRETS          — Recital → Article, Guideline → Article, CaseLaw → Article
  HAS_EXCEPTION       — Article → Exemption (with conditions property)
  COMPLEMENTS         — Article → Article (cross-regulation). Required property: interaction_type ∈
                        {REINFORCES, CREATES_EXCEPTION, CO_TRIGGERS, CUMULATIVE, DELEGATES}
                        Example: Art 22 GDPR -[COMPLEMENTS {interaction_type: REINFORCES}]-> Art 14 AI Act
                        Example: Art 9 GDPR -[COMPLEMENTS {interaction_type: CREATES_EXCEPTION}]-> Art 10(5) AI Act
                        Example: Art 83 GDPR -[COMPLEMENTS {interaction_type: CUMULATIVE}]-> Art 99 AI Act
  SUPERSEDES          — Provision → Provision (when one overrides another)
  PENALISED_BY        — Violation → EnforcementAction
  CITES               — EnforcementAction → Article, CaseLaw → Article
```

### 3.3 Entity Property Specifications

#### Article Node (most important entity)
```json
{
  "id": "GDPR_ART_35",
  "type": "Article",
  "name": "Article 35",
  "title": "Data protection impact assessment",
  "regulation_id": "GDPR",
  "chapter": "Chapter 4",
  "article_number": "35",
  "full_text": "<complete article text>",
  "paragraphs": {
    "1": "<paragraph 1 text>",
    "2": "<paragraph 2 text>",
    "3": {
      "intro": "<intro text>",
      "a": "<sub-item a>",
      "b": "<sub-item b>"
    }
  },
  "modality": "MUST",
  "applies_to_actors": ["controller"],
  "cross_references": ["GDPR_ART_36", "GDPR_ART_9", "GDPR_ART_22"],
  "source_url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
  "source_version": "consolidated-2016-04-27",
  "loaded_at": "2026-02-10T00:00:00Z",
  "is_current": true,
  "superseded_by": null
}
```

#### Definition Node
```json
{
  "id": "GDPR_DEF_PERSONAL_DATA",
  "type": "Definition",
  "term": "personal data",
  "definition_text": "any information relating to an identified or identifiable natural person...",
  "regulation_id": "GDPR",
  "article_reference": "GDPR_ART_4_1",
  "synonyms": [],
  "examples": ["name", "identification number", "location data", "online identifier"]
}
```

#### CaseLaw Node
```json
{
  "id": "CJEU_C_311_18",
  "type": "CaseLaw",
  "case_number": "C-311/18",
  "case_name": "Schrems II",
  "full_name": "Data Protection Commissioner v Facebook Ireland Ltd and Maximillian Schrems",
  "court": "CJEU (Grand Chamber)",
  "decision_date": "2020-07-16",
  "topic": "International data transfers",
  "provisions_interpreted": ["GDPR_ART_44", "GDPR_ART_45", "GDPR_ART_46", "GDPR_ART_49"],
  "holding": "<numbered holding points>",
  "key_legal_points": ["<point 1>", "<point 2>"],
  "practical_impact": ["<impact 1>"],
  "ai_relevance": ["<relevance 1>"]
}
```

#### Obligation Node (extracted from article text)
```json
{
  "id": "OBL_GDPR_ART35_CONDUCT_DPIA",
  "type": "Obligation",
  "name": "Conduct DPIA before high-risk processing",
  "obligation_type": "MUST",
  "source_article": "GDPR_ART_35",
  "source_paragraph": "1",
  "source_text": "Where a type of processing...is likely to result in a high risk...the controller shall...carry out an assessment of the impact",
  "applies_to": ["controller"],
  "conditions": ["high_risk_processing", "new_technologies", "large_scale_special_category"],
  "deadline": "Before processing begins",
  "penalty_reference": "GDPR_ART_83_4_A"
}
```

#### Exemption Node (extracted from article text)
```json
{
  "id": "EXM_GDPR_ART9_2_A",
  "type": "Exemption",
  "name": "Explicit consent exemption for special category data",
  "source_article": "GDPR_ART_9",
  "source_paragraph": "2(a)",
  "exempts_from": "OBL_GDPR_ART9_PROHIBITION",
  "condition_text": "the data subject has given explicit consent to the processing of those personal data for one or more specified purposes",
  "conditions": ["explicit_consent", "specified_purpose"]
}
```

#### EnforcementAction Node
```json
{
  "id": "ENF_CLEARVIEW_AI",
  "type": "EnforcementAction",
  "name": "Clearview AI Biometric Fines",
  "authority": "Multiple DPAs: CNIL, Garante, ICO, HDPA, AP",
  "target": "Clearview AI Inc.",
  "decision_date": "2022-2024",
  "fine_amount_eur": 90500000,
  "violations": ["GDPR_ART_6_1", "GDPR_ART_9", "GDPR_ART_12", "GDPR_ART_15", "GDPR_ART_17"],
  "facts": "<summary>",
  "key_findings": ["<finding 1>"],
  "ai_relevance": ["<relevance 1>"]
}
```

---

## 4. Phase-by-Phase Construction Plan

### Phase 0: Data Audit (Integrity Gate)

**Goal**: Verify raw data matches all assumptions before writing any parser code.

**Method**: Manually inspect 1 representative file from each of the 8 data categories.

| Category | File to Inspect | Verify |
|---|---|---|
| GDPR Articles | `Data/gdpr_chapters/gdpr_chapter1.txt` | Delimiter `=== ARTICLE N ===`, "Name:" field, paragraph numbering |
| AI Act Articles | `Data/ai_act_chapters/ai_act_chapter1.txt` | Delimiter `=== ARTICLE N ===`, "Title:" field (not "Name:") |
| GDPR Recitals | `Data/gdpr_recitals/gdpr_recitals.txt` | Delimiter `=== RECITAL N ===`, single text block per recital |
| AI Act Recitals | `Data/ai_act_recitals/euai_recitals.txt` | Same delimiter pattern, count = 180 |
| AI Act Annexes | `Data/ai_act_annexes/ai_act_annexes.txt` | Delimiter `=== ANNEX N ===`, Roman numeral handling |
| Case Law | Any `Data/cjeu_case_law/C*.txt` | Delimiter `=== CASE: ===`, structured fields |
| Guidelines | Any `Data/edpb_guidelines/GL_*.txt` | Delimiter `=== GUIDELINE: ===`, Tier field |
| Enforcement | Any `Data/enforcement_actions/*.txt` | Delimiter `=== ENFORCEMENT: ===`, fine fields |

**Exit criteria**: All 8 delimiter patterns confirmed. All expected fields present. File counts match (11 GDPR chapter files, 13 AI Act chapter files, etc.). Any discrepancies documented and parser design updated.

---

### Phase 1: Parse Raw Text → Structured JSON (ETL Layer)

**Goal**: Convert all 89 raw text files into clean, validated JSON files.

**Script**: `core_2/scripts/parse_new_data.py`

#### 1.1 GDPR Article Parser
- **Input**: `Data/gdpr_chapters/gdpr_chapter*.txt` (11 files)
- **Delimiter**: `=== ARTICLE N ===`
- **Extract**: chapter name, article number, article name/title, each paragraph as separate field, sub-items `(a)`, `(b)`, etc.
- **Output**: `core_2/data/legal/gdpr_articles.json`
- **Expected**: 99 articles across 11 chapters
- **ID Convention**: `GDPR_ART_1` through `GDPR_ART_99`
- **Note**: GDPR uses "Name:" field; AI Act uses "Title:" field — parser must handle both

#### 1.2 EU AI Act Article Parser
- **Input**: `Data/ai_act_chapters/ai_act_chapter*.txt` (13 files)
- **Delimiter**: `=== ARTICLE N ===`
- **Extract**: Same structure as GDPR
- **Output**: `core_2/data/legal/eu_ai_act_articles.json`
- **Expected**: 113 articles across 13 chapters
- **ID Convention**: `AIACT_ART_1` through `AIACT_ART_113`

#### 1.3 GDPR Recital Parser
- **Input**: `Data/gdpr_recitals/gdpr_recitals.txt` (1 file, 153 KB)
- **Delimiter**: `=== RECITAL N ===`
- **Extract**: recital number, full text
- **Output**: `core_2/data/legal/gdpr_recitals.json`
- **Expected**: 173 recitals
- **ID Convention**: `GDPR_REC_1` through `GDPR_REC_173`

#### 1.4 EU AI Act Recital Parser
- **Input**: `Data/ai_act_recitals/euai_recitals.txt` (1 file, 225 KB)
- **Delimiter**: `=== RECITAL N ===`
- **Extract**: recital number, full text
- **Output**: `core_2/data/legal/ai_act_recitals.json`
- **Expected**: 180 recitals
- **ID Convention**: `AIACT_REC_1` through `AIACT_REC_180`

#### 1.5 EU AI Act Annex Parser
- **Input**: `Data/ai_act_annexes/ai_act_annexes.txt` (1 file, 46 KB)
- **Delimiter**: `=== ANNEX N ===` (Roman numerals in text, but delimited as I, II, III...)
- **Extract**: annex number, title, sections, sub-items
- **Output**: `core_2/data/legal/ai_act_annexes.json`
- **Expected**: 13 annexes (I–XIII)
- **ID Convention**: `AIACT_ANNEX_I` through `AIACT_ANNEX_XIII`

#### 1.6 CJEU Case Law Parser
- **Input**: `Data/cjeu_case_law/C*_*.txt` (20 individual files)
- **Delimiter**: `=== CASE: C-NNN/YY <name> ===`
- **Extract**: case_number, case_name, full_name, court, decision_date, topic, provisions_interpreted, facts, holding, key_legal_points, practical_impact, ai_relevance
- **Output**: `core_2/data/interpretive/case_law.json`
- **Expected**: 20 cases
- **ID Convention**: `CJEU_C_311_18` (case number with underscores)
- **Important**: Also parse `cjeu_case_law_detailed.txt` for any additional content not in individual files

#### 1.7 EDPB Guidelines Parser
- **Input**: `Data/edpb_guidelines/GL_*.txt` + `WP*.txt` (22 individual files)
- **Delimiter**: `=== GUIDELINE: <ref> ===`
- **Extract**: reference, title, topics, tier, full text (preserve section headings)
- **Output**: `core_2/data/interpretive/edpb_guidelines.json`
- **Expected**: 21 guidelines
- **ID Convention**: `EDPB_GL_05_2022` (reference number)
- **Special**: Guidelines are very large (up to 220KB each). For the vector store, split into sections. For the graph, keep metadata + section summaries.

#### 1.8 Enforcement Actions Parser
- **Input**: `Data/enforcement_actions/*.txt` (15 individual files)
- **Delimiter**: `=== ENFORCEMENT: <name> ===`
- **Extract**: authority, target, decision_date, fine_amount, fine_category, violations, facts, key_findings, corrective_measures, ai_relevance
- **Output**: `core_2/data/interpretive/enforcement_actions.json`
- **Expected**: 15 actions
- **ID Convention**: `ENF_CLEARVIEW_AI`, `ENF_META_TRANSFER`, etc.

#### Phase 1 Validation (EXIT GATE — do not proceed to Phase 2 until all pass)
- Count: Verify expected counts (99 GDPR articles, 113 AI Act articles, 173 GDPR recitals, 180 AI Act recitals, 13 annexes, 20 cases, 21 guidelines, 15 enforcement actions)
- Schema: All JSON files validate against Pydantic models
- Completeness: Spot-check 5 articles per regulation against raw text
- No data loss: Character count of `full_text` fields ≥ 95% of raw text
- Cross-references parsed: Every "Article N" mention in article text captured in `cross_references` field

---

### Phase 2: Build Structural Knowledge Graph (Neo4j)

**Goal**: Load all parsed entities + structural relationships into Neo4j.

**Script**: `core_2/scripts/load_knowledge_graph.py`

#### 2.1 Create Regulation Nodes (2)
```
(:Regulation {id: "GDPR", name: "General Data Protection Regulation", effective_date: "2018-05-25"})
(:Regulation {id: "EU_AI_ACT", name: "EU AI Act", effective_date: "2024-08-01"})
```

#### 2.2 Create Chapter Nodes
- GDPR: 11 chapters
- AI Act: 13 chapters
- Relationship: `(Regulation)-[:CONTAINS]->(Chapter)`

#### 2.3 Create Article Nodes (~212)
- GDPR: 99 articles with full paragraph-level text
- AI Act: 113 articles with full paragraph-level text
- Relationships:
  - `(Chapter)-[:CONTAINS]->(Article)`
  - `(Article)-[:PART_OF]->(Chapter)`

#### 2.4 Create Recital Nodes (~353)
- GDPR: 173 recitals
- AI Act: ~180 recitals
- Relationship: `(Regulation)-[:CONTAINS]->(Recital)`

#### 2.5 Create Annex Nodes (13)
- AI Act Annexes I–XIII
- Relationship: `(Regulation)-[:CONTAINS]->(Annex)`

#### 2.6 Create CaseLaw Nodes (20)
- All 20 CJEU cases with structured properties

#### 2.7 Create Guideline Nodes (22)
- All 22 EDPB guidelines with metadata

#### 2.8 Create EnforcementAction Nodes (15)
- All 15 enforcement actions with structured properties

#### 2.9 Create Structural Relationships

**Cross-references within articles** (parsed from text like "referred to in Article 36"):
- `(Article)-[:REFERENCES]->(Article)` with `{source_paragraph, target_paragraph}` properties
- Expected: ~400+ cross-references within GDPR, ~300+ within AI Act

**Article ↔ Recital links** (recitals reference specific articles):
- `(Recital)-[:INTERPRETS]->(Article)` with confidence score
- These must be extracted from recital text — recitals mention specific article numbers

**CaseLaw → Article links**:
- `(CaseLaw)-[:CITES]->(Article)` — directly from `provisions_interpreted` field
- `(CaseLaw)-[:INTERPRETS]->(Article)` — from the holding's legal interpretation

**Guideline → Article links**:
- `(Guideline)-[:INTERPRETS]->(Article)` — from guideline topics and article references
- Example: WP251 (profiling) → GDPR Art 22, Art 9, Art 35

**EnforcementAction → Article links**:
- `(EnforcementAction)-[:CITES]->(Article)` — directly from `violations` field
- Example: Clearview AI → GDPR Art 6(1), Art 9, Art 12, Art 15, Art 17

#### Phase 2 Validation (EXIT GATE — do not proceed to Phase 3 until all pass)
- Node counts match parsed data exactly
- Every Article has a PART_OF relationship to a Chapter
- Every Chapter has a CONTAINS relationship from a Regulation
- No orphan nodes (every node reachable from a Regulation root)
- Spot-check 10 cross-references against raw text
- Graph connectivity: `MATCH (n) WHERE NOT (n)--() RETURN count(n)` = 0

---

### Phase 3: Semantic Entity & Relationship Extraction

**Goal**: Extract Definitions, Concepts, Obligations, Rights, Exemptions, Actors, DataTypes, AISystemTypes, RiskCategories, Penalties from article text.

This is the hardest and most valuable phase. This is where the **document hierarchy becomes a knowledge graph**.

**Script**: `core_2/scripts/extract_semantic_entities.py`

#### 3.1 Definition Extraction (from Art 4 GDPR, Art 3 AI Act)

GDPR Art 4 contains 26 definitions. AI Act Art 3 contains 68+ definitions.

**Method**: Rule-based parsing (these are numbered lists in a known format)
```
(1) 'personal data' means <definition text>;
(2) 'processing' means <definition text>;
```

**Output**: ~94 Definition nodes
- Create `(Article)-[:DEFINES]->(Definition)` relationships
- Cross-link where both regulations define the same term (e.g., "biometric data" appears in both GDPR Art 4(14) and AI Act Art 3(34))

#### 3.2 Obligation Extraction (from all articles)

**Method**: LLM-assisted extraction with human-verifiable evidence

For every article, extract:
| Field | Source |
|---|---|
| obligation_type | Keyword: "shall" → MUST, "shall not" → MUST_NOT, "should" → SHOULD, "may" → MAY |
| who | The grammatical subject of the obligation clause |
| what | The action required or prohibited |
| conditions | "Where..." / "If..." / "In the case of..." clauses |
| source_text | Exact quote from article |

**CALIBRATION STEP** (before running full extraction):
- Manually extract obligations from 10 representative articles (5 GDPR, 5 AI Act) as gold standard
- Suggested calibration articles: GDPR Art 5, 6, 9, 22, 35; AI Act Art 5, 6, 9, 10, 14
- Run LLM extraction on these 10 articles, compare against gold standard
- Refine prompt until precision ≥ 90% and recall ≥ 85% against gold standard
- Only then run extraction across all 212 articles

**Heuristic pre-filter** (before LLM):
- Scan all article text for sentences containing "shall", "shall not", "must", "must not", "may", "should"
- GDPR uses "shall" ~500 times across 99 articles
- AI Act uses "shall" ~800 times across 113 articles
- Group by article → feed to LLM for structured extraction
- **Important**: "shall" is not always an obligation. Temporal clauses ("This Regulation shall apply from...") and delegation clauses ("Member States shall lay down...") must be filtered.

**LLM Prompt Per Article**:
```
You are a legal analyst. Extract ALL obligations from this article.
For each obligation, provide:
- obligation_type: MUST | MUST_NOT | SHOULD | MAY
- who: [actor(s) this applies to]
- what: [action required/prohibited]
- conditions: [when does this apply]
- source_quote: [exact text from the article]
- paragraph: [which paragraph]

Article text:
{article_full_text}
```

**Expected output**: ~800–1200 Obligation nodes
- `(Article)-[:REQUIRES]->(Obligation)` for MUST/SHOULD
- `(Article)-[:PROHIBITS]->(Obligation)` for MUST_NOT
- `(Article)-[:PERMITS]->(Obligation)` for MAY

**Validation**: Every Obligation node must have a `source_text` that appears verbatim in the source article. Automated check.

#### 3.3 Exemption Extraction

**Method**: LLM-assisted — scan for patterns like:
- "This prohibition does not apply where..."
- "The obligations referred to in paragraphs 1 and 2 shall not apply to..."
- "By derogation from..."
- "Paragraph N shall not apply where..."

**Expected output**: ~100–200 Exemption nodes
- `(Article)-[:HAS_EXCEPTION]->(Exemption)`
- `(Exemption)-[:EXEMPTS]->(Obligation)`

#### 3.4 Concept Extraction

**Method**: Combined rule-based + LLM

Key concepts to extract (non-exhaustive):
- Data protection principles: lawfulness, fairness, transparency, purpose limitation, data minimisation, accuracy, storage limitation, integrity/confidentiality, accountability
- Processing operations: collection, recording, storage, alteration, retrieval, consultation, use, disclosure, erasure, profiling, automated decision-making
- Compliance concepts: DPIA, conformity assessment, CE marking, risk management, human oversight, data governance, technical documentation
- Rights: right of access, right to rectification, right to erasure, right to restriction, data portability, right to object, right against automated decisions

**Expected output**: ~150–250 Concept nodes
- `(Concept)-[:REGULATED_BY]->(Article)`
- `(Concept)-[:RELATED_TO]->(Concept)` (synonyms, hierarchies)

#### 3.5 Actor Extraction

**Method**: Rule-based from definitions
- GDPR actors: controller, processor, data subject, DPO, supervisory authority, recipient, third party
- AI Act actors: provider, deployer, importer, distributor, product manufacturer, authorised representative, notified body, market surveillance authority, AI Office

**Expected output**: ~20 Actor nodes
- `(Article)-[:APPLIES_TO]->(Actor)`
- `(Actor)-[:RESPONSIBLE_FOR]->(Obligation)`

#### 3.6 DataType Hierarchy

**Method**: Rule-based from GDPR Art 4 definitions + Art 9 special categories + AI Act Art 3

```
DataType
├── PersonalData
│   ├── SpecialCategoryData
│   │   ├── BiometricData
│   │   ├── HealthData
│   │   ├── GeneticData
│   │   ├── RacialEthnicData
│   │   ├── PoliticalOpinions
│   │   ├── ReligiousBeliefs
│   │   ├── TradeUnionMembership
│   │   └── SexualOrientation
│   ├── PseudonymisedData          ← GDPR Recital 26 + Art 4(5): still personal data, GDPR fully applies
│   └── RegularPersonalData
│       ├── ContactData (name, email, phone)
│       ├── LocationData
│       ├── OnlineIdentifiers
│       ├── FinancialData
│       └── BehavioralData (profiling inputs)
└── NonPersonalData
    ├── AnonymisedData              ← Recital 26: truly anonymous = not personal data
    └── AggregatedData              ← Only non-personal if irreversibly aggregated
```

**Expected output**: ~25 DataType nodes
- `(DataType)-[:REGULATED_BY]->(Article)`
- `(DataType)-[:PARENT_OF]->(DataType)` for hierarchy

#### 3.7 AISystemType + RiskCategory Mapping

**Method**: Rule-based from Annex III + Art 5 + Art 52

```
RiskCategory
├── PROHIBITED (Art 5)
│   ├── SubliminalManipulation
│   ├── VulnerabilityExploitation
│   ├── SocialScoringByPublicAuthority
│   ├── RealTimeBiometricInPublicSpaces (except exemptions)
│   ├── EmotionRecognitionWorkplace
│   ├── EmotionRecognitionEducation
│   ├── UntargetedFacialScraping
│   └── BiometricCategorizationSensitive
├── HIGH_RISK (Annex III)
│   ├── BiometricIdentification (Annex III.1)
│   ├── CriticalInfrastructure (Annex III.2)
│   ├── EducationAssessment (Annex III.3)
│   ├── Employment (Annex III.4)
│   ├── EssentialServices (Annex III.5)
│   ├── LawEnforcement (Annex III.6)
│   ├── MigrationBorderControl (Annex III.7)
│   └── JusticeAndDemocracy (Annex III.8)
├── LIMITED_RISK (Art 50)
│   ├── Chatbots
│   ├── EmotionRecognition (non-prohibited contexts)
│   ├── DeepfakeGeneration
│   └── AIGeneratedContent
└── MINIMAL_RISK
    └── (everything else)
```

**Expected output**: ~40 nodes (AISystemType + RiskCategory)
- `(AISystemType)-[:CLASSIFIED_AS]->(RiskCategory)`
- `(RiskCategory)-[:REGULATED_BY]->(Article)`
- `(Annex)-[:DEFINES]->(RiskCategory)`

#### 3.8 Penalty Extraction

**Method**: Rule-based from GDPR Art 83 + AI Act Art 99

| Tier | Regulation | Max Fine | Articles |
|---|---|---|---|
| Tier 1 | GDPR Art 83(4) | €10M / 2% turnover | Art 8, 11, 25-39, 42-43 |
| Tier 2 | GDPR Art 83(5) | €20M / 4% turnover | Art 5-7, 9, 12-22, 44-49 |
| Tier 3 | GDPR Art 83(6) | €20M / 4% turnover | Non-compliance with DPA order |
| Prohibited AI | AI Act Art 99(3) | €35M / 7% turnover | Art 5 violations |
| High-Risk AI | AI Act Art 99(4) | €15M / 3% turnover | Art 6-49 violations |
| Info Provision | AI Act Art 99(5) | €7.5M / 1% turnover | Incorrect information |

**Expected output**: ~10 Penalty nodes
- `(Penalty)-[:APPLIED_TO]->(Obligation)`
- `(Article)-[:ENFORCED_BY]->(Penalty)`

#### 3.9 Cross-Regulation Links

**Critical relationships between GDPR and AI Act**:

| GDPR Article | Relationship | AI Act Article | Rationale |
|---|---|---|---|
| Art 5 (Principles) | COMPLEMENTS | Art 10 (Data governance) | AI data must follow GDPR principles |
| Art 9 (Special categories) | COMPLEMENTS | Art 10(5) (Bias detection) | AI Act allows processing special data for bias detection |
| Art 22 (Automated decisions) | COMPLEMENTS | Art 14 (Human oversight) | Both require human involvement in automated decisions |
| Art 25 (Privacy by design) | COMPLEMENTS | Art 9 (Risk management) | Both mandate built-in safeguards |
| Art 35 (DPIA) | COMPLEMENTS | Art 6+27 (Risk+Fundamental rights) | AI Act high-risk triggers GDPR DPIA |
| Art 13-14 (Transparency) | COMPLEMENTS | Art 13+50 (Transparency) | Both mandate informing individuals |
| Art 44-49 (Transfers) | COMPLEMENTS | Art 10 (Data governance) | AI training data transfers need safeguards |
| Art 30 (ROPA) | COMPLEMENTS | Art 11-12 (Technical docs) | Both require documentation |

**Method**: LLM-assisted extraction with human review, validated against legal commentary.

**Expected output**: ~80–120 cross-regulation relationship edges (8 primary pairs expand to many paragraph-level edges, plus AI Act recitals referencing GDPR articles ~40+ times)

#### Phase 3 Validation
- Every Obligation has a `source_text` verifiable in the original article
- Every Definition links back to a specific paragraph
- Every cross-regulation link has a `rationale` property explaining why
- Run golden test queries (from `core_2/data/golden/test_queries.json`)

---

### Phase 4: Build Vector Store (ChromaDB)

**Goal**: Embed all textual content for semantic search. The vector store complements the graph — it finds relevant articles by meaning, the graph finds related articles by structure.

**Script**: `core_2/scripts/build_vector_store.py`

#### 4.1 Chunking Strategy

Different entity types need different chunking:

| Entity Type | Chunking Strategy | Estimated Chunks |
|---|---|---|
| **Articles** (GDPR+AI Act) | One chunk per paragraph (preserve article context in metadata) | ~1500 |
| **Recitals** | One chunk per recital (most are 1-3 paragraphs) | ~353 |
| **Annexes** | One chunk per section/sub-item | ~150 |
| **Case Law** | Separate chunks for: facts, holding, key_legal_points, practical_impact, ai_relevance | ~100 |
| **Guidelines** | One chunk per section heading (~10-30 sections per guideline) | ~400 |
| **Enforcement Actions** | Separate chunks for: facts, key_findings, corrective_measures, ai_relevance | ~60 |
| **Definitions** | One chunk per definition | ~94 |
| **Obligations** | One chunk per obligation (source_text) | ~800-1200 |
| **Concepts** | One chunk per concept description | ~200 |

**Total estimated chunks**: ~3,100–4,100

#### 4.2 Metadata Per Chunk

Every chunk in ChromaDB gets rich metadata for filtering:

```json
{
  "entity_id": "GDPR_ART_35",
  "entity_type": "Article",
  "regulation": "GDPR",
  "chapter": "Chapter 4",
  "article_number": "35",
  "paragraph": "1",
  "title": "Data protection impact assessment",
  "modality": "MUST",
  "actors": ["controller"],
  "data_types_mentioned": ["special_category"],
  "risk_relevance": "HIGH"
}
```

This metadata enables filtered vector search:
- "Find all GDPR obligations about biometric data" → filter: `regulation=GDPR, data_types_mentioned contains biometric`
- "Find all HIGH_RISK classification rules" → filter: `risk_relevance=HIGH`

#### 4.3 Embedding Model

Use `text-embedding-004` (Google, configured in existing stack) — 768 dimensions.

For each chunk:
1. Prepend a "search prefix" to improve retrieval quality:
   - Article chunks: `"EU regulation article: {title} — {text}"`
   - Case law chunks: `"Legal case holding: {case_name} — {text}"`
   - Obligation chunks: `"Compliance requirement: {who} must {what} — {source_text}"`

#### 4.4 Collection Structure

Create separate ChromaDB collections for different retrieval use cases:

| Collection | Content | Purpose |
|---|---|---|
| `articles` | Article paragraphs | Primary legal text search |
| `obligations` | Extracted obligations | "What must I do?" queries |
| `interpretive` | Recitals + Guidelines + Case law | "What does this mean?" queries |
| `enforcement` | Enforcement actions | "What happened to others?" queries |
| `definitions` | Legal definitions | Term lookup |

#### Phase 4 Validation
- Total chunk count matches expected
- Spot-check: query "biometric employee monitoring" retrieves Art 9, Art 35, Annex III.4, AI Act Art 14
- Spot-check: query "DPIA requirements" retrieves Art 35, WP248 guideline, Recital 84
- No empty embeddings, no duplicate chunks

---

### Phase 5: Cross-Link and Validate (Integrity Layer)

**Goal**: Ensure the KG and vector store are consistent, complete, and correct.

#### 5.1 Bidirectional Consistency Check
- Every entity in Neo4j has a corresponding chunk in ChromaDB
- Every chunk in ChromaDB has `entity_id` that exists in Neo4j
- No orphan nodes (every article connected to a chapter, every chapter to a regulation)

#### 5.2 Golden Query Test Suite

Expand `core_2/data/golden/test_queries.json` with expected answers:

```json
[
  {
    "query": "Is facial recognition for employee attendance HIGH_RISK under EU AI Act?",
    "expected_answer": "YES — HIGH_RISK",
    "expected_path": ["facial_recognition → BiometricData → Annex_III_1 → HIGH_RISK", "employee_attendance → Employment → Annex_III_4 → HIGH_RISK"],
    "expected_citations": ["AIACT_ART_6", "AIACT_ANNEX_III_1", "AIACT_ANNEX_III_4"],
    "expected_cross_reg": ["GDPR_ART_9"]
  },
  {
    "query": "Does processing health data with AI require a DPIA?",
    "expected_answer": "YES",
    "expected_path": ["HealthData → SpecialCategoryData → GDPR_ART_9 → GDPR_ART_35"],
    "expected_citations": ["GDPR_ART_35", "GDPR_ART_9", "GDPR_REC_91"]
  },
  {
    "query": "Can we train an AI model on scraped biometric images from social media?",
    "expected_answer": "NO — Prohibited",
    "expected_citations": ["AIACT_ART_5", "GDPR_ART_9", "ENF_CLEARVIEW_AI"],
    "expected_enforcement": "ENF_CLEARVIEW_AI"
  },
  {
    "query": "What are the transparency requirements for a chatbot?",
    "expected_answer": "Must disclose AI interaction",
    "expected_citations": ["AIACT_ART_50"],
    "expected_risk": "LIMITED_RISK"
  },
  {
    "query": "What penalty applies if we deploy prohibited AI?",
    "expected_answer": "Up to EUR 35M or 7% global turnover",
    "expected_citations": ["AIACT_ART_99_3", "AIACT_ART_5"]
  },
  {
    "query": "What are the combined requirements for a recruitment AI system?",
    "expected_answer": "HIGH_RISK classification + DPIA + human oversight + non-discrimination + transparency",
    "expected_citations": ["AIACT_ART_6", "AIACT_ANNEX_III_4", "AIACT_ART_14", "GDPR_ART_22", "GDPR_ART_35"],
    "expected_cross_reg": true
  }
]
```

#### 5.3 Relationship Density Analysis
- Target: Average ≥ 4 relationships per Article node
- Every Article with "shall" should have at least 1 Obligation extracted
- Every Annex III category should link to specific AISystemType examples
- Every enforcement action should cite ≥ 1 specific article

#### 5.4 Coverage Reports
- Generate a report: which GDPR articles have 0 obligations extracted? (indicates extraction failure, not truly an article without obligations)
- Which AI Act articles have 0 cross-references? (likely parsing issue)
- Which enforcement actions have no CITES relationships?

---

### Phase 6: Application Layer — SystemProfile Matching (OUT OF KB SCOPE)

> **This phase is NOT part of the KB construction project.** It belongs to Core 3 (Compliance Agent). Included here for reference only — do not build this as part of Phases 0-5.

**Goal**: Build the bridge from user input (codebase/docs/description) to KG traversal.

This phase is about defining the **standard intermediate representation** that all inputs get converted to, and how that representation maps to the KG.

#### 6.1 SystemProfile Schema

```python
class SystemProfile(BaseModel):
    """Standard representation of an AI system under evaluation."""
    
    # What the system does
    system_name: str
    system_description: str
    capabilities: list[str]           # ["facial_recognition", "attendance_tracking"]
    
    # What data it processes
    data_types_processed: list[str]   # ["biometric", "employee_records"]
    special_category_data: list[str]  # ["biometric", "health"]
    data_sources: list[str]           # ["camera_feed", "employee_database"]
    data_volume: str | None           # "large_scale" / "limited"
    
    # Who and where
    affected_persons: list[str]       # ["employees", "customers", "public"]
    deployment_context: str           # "workplace", "public_space", "online"
    deployment_geography: list[str]   # ["EU", "US", "global"]
    
    # How it makes decisions
    decision_types: list[str]         # ["access_control", "screening", "recommendation"]
    autonomy_level: str               # "fully_automated", "human_in_loop", "human_on_loop"
    human_oversight: bool
    
    # Who operates it
    operator_role: str                # "provider", "deployer", "both"
    
    # Technical
    technology: list[str]             # ["deep_learning", "computer_vision"]
    training_data_sources: list[str]  # ["proprietary", "scraped", "public_dataset"]
    cross_border_transfers: bool
```

#### 6.2 SystemProfile → KG Anchor Mapping

Each SystemProfile field maps to KG node types for traversal:

| SystemProfile Field | Maps To KG Node Type | Relationship Direction |
|---|---|---|
| `data_types_processed` | `DataType` | → REGULATED_BY → Article |
| `capabilities` | `AISystemType` | → CLASSIFIED_AS → RiskCategory |
| `decision_types` | `Concept` (automated decisions, profiling) | → TRIGGERS → Obligation |
| `affected_persons` | `Actor` (data subject types) | ← PROTECTS → Right |
| `deployment_context` | `Annex III` categories | → maps to HIGH_RISK |
| `human_oversight` | `Concept` (human oversight) | → Article 14 / Article 22 |
| `operator_role` | `Actor` (provider/deployer) | → RESPONSIBLE_FOR → Obligation |
| `cross_border_transfers` | `Concept` (international transfers) | → Chapter V GDPR |
| `training_data_sources: scraped` | `EnforcementAction` (Clearview) | precedent warning |

#### 6.3 Input Extractors

Build extractors that convert different input types to SystemProfile:

1. **Free text description** → LLM extraction → SystemProfile *(exists today, needs structuring)*
2. **Codebase analysis** → Static analysis + LLM → SystemProfile *(new)*
3. **Model card / docs** → Template parsing → SystemProfile *(new)*

#### 6.4 Compliance Traversal Algorithm

Given a SystemProfile, the system:

1. **Match anchors** — Find all KG nodes matching profile fields
2. **Traverse outward** — Follow relationships from anchors to discover all applicable:
   - Obligations (what MUST they do?)
   - Prohibitions (what MUST NOT they do?)
   - Rights (what rights do affected persons have?)
   - Exemptions (are there applicable exceptions?)
3. **Cross-regulate** — For each matched article, follow COMPLEMENTS edges to find requirements from the other regulation
4. **Cite precedents** — For each obligation, find enforcement actions and case law via CITES reverse edges
5. **Generate gap analysis** — Compare profile against obligations → list of compliance gaps
6. **Produce documents** — Use obligations + gaps to generate DPIA, ROPA, conformity assessment

---

## 5. Estimated Entity and Relationship Counts

| Category | Count |
|---|---|
| **Regulation nodes** | 2 |
| **Chapter nodes** | 24 |
| **Article nodes** | ~212 |
| **Recital nodes** | ~353 |
| **Annex nodes** | 13 |
| **Definition nodes** | ~94 |
| **Concept nodes** | ~200 |
| **Obligation nodes** | ~1,000 |
| **Exemption nodes** | ~150 |
| **Right nodes** | ~20 |
| **Penalty nodes** | ~10 |
| **Actor nodes** | ~20 |
| **DataType nodes** | ~25 |
| **AISystemType nodes** | ~30 |
| **RiskCategory nodes** | ~15 |
| **CaseLaw nodes** | 20 |
| **Guideline nodes** | 21 |
| **EnforcementAction nodes** | 15 |
| **TOTAL NODES** | **~2,225** |
| | |
| **Structural relationships** (CONTAINS, PART_OF) | ~650 |
| **Cross-reference relationships** (REFERENCES) | ~700 |
| **Semantic relationships** (REQUIRES, PROHIBITS, PERMITS, TRIGGERS, EXEMPTS) | ~1,500 |
| **Actor relationships** (APPLIES_TO, ENFORCED_BY, RESPONSIBLE_FOR) | ~300 |
| **Data/Risk relationships** (CLASSIFIED_AS, REGULATED_BY, PROCESSES) | ~200 |
| **Interpretive relationships** (INTERPRETS, CITES) | ~300 |
| **Cross-regulation relationships** (COMPLEMENTS) | ~80-120 |
| **TOTAL RELATIONSHIPS** | **~3,730-3,770** |
| | |
| **Vector store chunks** | **~3,500** |

---

## 6. Technology Stack & Storage

| Component | Technology | Purpose |
|---|---|---|
| **Knowledge Graph** | Neo4j 5.x (existing) | Structural + semantic relationships, multi-hop traversal |
| **Vector Store** | ChromaDB (existing) | Semantic search over legal text |
| **Embedding Model** | Google text-embedding-004 (existing) | 768-dim embeddings |
| **LLM for Extraction** | Gemini 1.5 Pro (existing) | Obligation/concept extraction in Phase 3 |
| **Parsing Scripts** | Python (existing project structure) | ETL pipeline |
| **Validation** | pytest + golden queries | Automated correctness checks |

No new technology needed. The existing stack is correct for this task.

---

## 7. Execution Order and Dependencies

```
Phase 0 (Data Audit)    ← No dependencies, MUST complete before any coding
    ↓
Phase 1 (Parse)         ← Depends on Phase 0 confirming data format assumptions
    ↓
Phase 2 (Structural KG) ← Depends on Phase 1 JSON output
    ↓
Phase 3 (Semantic KG)   ← Depends on Phase 2 (needs article nodes to attach to)
    ↓                      Can partially parallelize with Phase 4
Phase 4 (Vector Store)  ← Depends on Phase 1 + Phase 3 (obligations need embedding too)
    ↓
Phase 5 (Validate)      ← Depends on Phases 2, 3, 4
```

### Estimated Effort

| Phase | Effort | Notes |
|---|---|---|
| Phase 0: Data Audit | 0.5 day | Manual inspection, non-negotiable gate |
| Phase 1: Parsing | 2-3 days | Rule-based, well-structured input |
| Phase 2: Structural KG | 1-2 days | Straightforward loading |
| Phase 3: Semantic extraction | 7-10 days | LLM-assisted, requires calibration + 2 rounds of prompt refinement. First pass produces ~30% noise. |
| Phase 4: Vector store | 1-2 days | Chunking + embedding |
| Phase 5: Validation | 2-3 days | Golden queries, coverage reports |
| **Total** | **~14-21 days** | Phase 3 is the critical path |

---

## 8. Risk Mitigation

| Risk | Mitigation |
|---|---|
| LLM hallucination in obligation extraction | Every obligation must have verifiable `source_text` from the original article. Automated check. |
| Missing cross-references | Parse explicit references first (rule-based), use LLM only for implicit connections |
| EDPB guidelines are very large (up to 220KB) | Store metadata+sections in graph, full text in vector store only |
| Definition conflicts between regulations | Surface both definitions, mark with `regulation_id`, let retrieval return both |
| Annex structure is irregular | Custom parser per annex format (Annex III is a numbered list, Annex IV is a document template, etc.) |
| Schema migration from existing data | Phase 2 replaces all existing data files. Git history preserves originals. |

---

## 9. File Structure After Completion

```
core_2/
├── data/
│   ├── legal/
│   │   ├── gdpr_articles.json          # 99 articles (REPLACED)
│   │   ├── eu_ai_act_articles.json     # 113 articles (REPLACED)
│   │   ├── gdpr_recitals.json          # 173 recitals (NEW)
│   │   ├── ai_act_recitals.json        # ~180 recitals (NEW)
│   │   └── ai_act_annexes.json         # 13 annexes (NEW)
│   ├── interpretive/
│   │   ├── case_law.json               # 20 cases (REPLACED)
│   │   ├── edpb_guidelines.json        # 21 guidelines (REPLACED)
│   │   └── enforcement_actions.json    # 15 actions (REPLACED)
│   ├── entities/
│   │   ├── definitions.json            # ~94 definitions (NEW)
│   │   ├── concepts.json               # ~200 concepts (NEW)
│   │   ├── obligations.json            # ~1000 obligations (NEW)
│   │   ├── exemptions.json             # ~150 exemptions (NEW)
│   │   ├── rights.json                 # ~20 rights (NEW)
│   │   ├── actors.json                 # ~20 actors (NEW)
│   │   ├── data_types.json             # ~25 data types (NEW)
│   │   ├── ai_system_types.json        # ~30 system types (NEW)
│   │   ├── risk_categories.json        # ~15 risk categories (NEW)
│   │   └── penalties.json              # ~10 penalties (NEW)
│   ├── relationships/
│   │   ├── structural.json             # CONTAINS, PART_OF (NEW)
│   │   ├── cross_references.json       # REFERENCES (NEW)
│   │   ├── semantic.json               # REQUIRES, PROHIBITS, etc. (NEW)
│   │   └── cross_regulation.json       # COMPLEMENTS (NEW)
│   └── golden/
│       └── test_queries.json           # Expanded golden tests (MODIFIED)
├── scripts/
│   ├── parse_new_data.py               # Phase 1 parser (NEW)
│   ├── load_knowledge_graph.py         # Phase 2 loader (NEW/MODIFIED)
│   ├── extract_semantic_entities.py    # Phase 3 extractor (NEW)
│   └── build_vector_store.py           # Phase 4 embedder (NEW)
└── src/
    └── graph/
        └── schema.py                   # Updated with new entity/relationship types (MODIFIED)
```

---

## 10. Why Not Other Storage Options?

**Should we add a third store beyond Neo4j + ChromaDB?**

No. Here's the reasoning:

| Considered | Decision | Why |
|---|---|---|
| **PostgreSQL for entities** | NO | The entities ARE the graph nodes. Duplicating them in Postgres adds sync complexity and provides no benefit. The relational models in Core 1 are correctly scoped to operational data (decision logs, violations). |
| **Elasticsearch** | NO | ChromaDB handles semantic search. We don't need full-text search — we need SEMANTIC search over legal text. Elasticsearch would be redundant. |
| **Second graph DB (e.g., Amazon Neptune)** | NO | Neo4j is the correct choice for legal knowledge. Multi-hop traversal, Cypher query language, property graph model — all fit perfectly. |
| **Document store (MongoDB)** | NO | JSON files on disk + Neo4j nodes are sufficient. We don't need a document store for 89 source files. |
| **Redis for KG caching** | MAYBE LATER | Could cache frequent traversal results. Not needed in initial build. Core 3 already has Redis for session state. |

**The two-store architecture (Neo4j for structure + ChromaDB for semantics) is the correct design for this use case.** The key insight: the graph answers "what's connected?" and the vectors answer "what's similar?" — you need both for legal compliance, but you don't need a third.

---

> **Next step**: Begin Phase 1 — implement `parse_new_data.py` to convert all raw text files into structured JSON.
