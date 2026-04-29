# TECHNICAL REFERENCE

**Consolidated from:** `01_PROJECT_PORTFOLIO.md`, `02_ARCHITECTURE_AND_INTEGRATION.md`, `03_KB_DESIGN_AND_CONSTRUCTION.md`, `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`
**Date:** 2026-02-24

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Neo4j Knowledge Graph Schema](#2-neo4j-knowledge-graph-schema)
3. [Retrieval Pipeline](#3-retrieval-pipeline)
4. [Agent Architecture (Core 3)](#4-agent-architecture-core-3)
5. [Cross-Module Integration](#5-cross-module-integration)
6. [Data Types & Risk Categories](#6-data-types--risk-categories)
7. [Cross-Regulation Mappings](#7-cross-regulation-mappings)
8. [EU AI Act Enforcement Timeline](#8-eu-ai-act-enforcement-timeline)
9. [Technology Stack](#9-technology-stack)
10. [Business Impact](#10-business-impact)

---

## 1. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│     CORE 3: Compliance Agent (Port 8000)                     │
│     • 5 AI Agents: Risk Classifier, GDPR Auditor, Legal      │
│       Research, Documentation Generator, Supervisor          │
│     • Uses LangGraph for workflow orchestration              │
└────────────┬─────────────────────────────────────────────────┘
             │ Queries knowledge graph for legal citations
             ▼
┌──────────────────────────────────────────────────────────────┐
│     CORE 2: GraphRAG Knowledge Engine (Port 8001)            │
│     • Neo4j Knowledge Graph (2,301 nodes, 4,431 rels)        │
│     • JSON-backed Vector Store (2,132+ docs, 7 collections)  │
│     • Hybrid Retrieval (RRF) + Multi-Hop Reasoning           │
└────────────┬─────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│     CORE 1: Monitoring & Governance (Port 8002)              │
│     • EU AI Act Article 14 compliance (human oversight)      │
│     • Bias detection (chi-square), drift detection (Evidently)│
│     • Prometheus metrics, Slack/email alerts                 │
└──────────────────────────────────────────────────────────────┘
```

### Portfolio Integration Context

```
Project 1 (Basic RAG) → Regulatory knowledge base
Project 3 (GraphRAG)  → Legal research engine     → Core 2
Project 4 (Multi-Agent) → Compliance automation   → Core 3
Project 2 (MLOps)     → Governance monitoring     → Core 1
```

---

## 2. Neo4j Knowledge Graph Schema

### 2.1 Entity Types (17 types — as built)

| Label | Description | Example ID |
|-------|-------------|------------|
| `Regulation` | Top-level framework | `GDPR`, `EU_AI_ACT` |
| `Chapter` | Chapter grouping | `GDPR_CHAPTER_4` |
| `Article` | Individual article | `GDPR_ART_35`, `AIACT_ART_6` |
| `Recital` | Interpretive recital | `GDPR_REC_71` |
| `Annex` | Technical annex | `AIACT_ANNEX_III` |
| `Definition` | Legal term | `GDPR_DEF_PERSONAL_DATA` |
| `Concept` | Abstract concept | `CONCEPT_DPIA` |
| `Right` | Data subject right | `RIGHT_ACCESS` |
| `Obligation` | Must/must-not requirement | `OBL_GDPR_LAWFUL_BASIS` |
| `Exemption` | Exception pathway | `EXM_GDPR_ART9_2_A` |
| `Actor` | Legal role | `ACTOR_CONTROLLER` |
| `DataType` | Data classification | `DT_BIOMETRIC` |
| `AISystemType` | AI risk classification | `AIST_FACIAL_RECOGNITION` |
| `RiskCategory` | Risk level | `RISK_HIGH` |
| `Penalty` | Fine/sanction tier | `PEN_GDPR_TIER2` |
| `CaseLaw` | CJEU decision | `CJEU_C_311_18` |
| `Guideline` | EDPB guideline | `EDPB_GL_05_2020` |
| `EnforcementAction` | DPA enforcement decision | `ENF_CLEARVIEW_AI` |

### 2.2 Relationship Types (13 types — as built)

| Type | Meaning | Example |
|------|---------|---------|
| `CONTAINS` | Parent → Child (structural) | `(GDPR)-[:CONTAINS]->(GDPR_ART_5)` |
| `PART_OF` | Child → Parent | — |
| `REFERENCES` | Cross-reference | `(AIACT_ART_6)-[:REFERENCES]->(AIACT_ANNEX_III)` |
| `DEFINES` | Definition provision | `(GDPR)-[:DEFINES]->(GDPR_DEF_PERSONAL_DATA)` |
| `REQUIRES` | Creates obligation | — |
| `PROHIBITS` | Forbids activity | `(AIACT_ART_5)-[:PROHIBITS]->(AIST_EMOTION_RECOG)` |
| `PERMITS` | Allows activity | — |
| `EXEMPTS` | Provides exception | — |
| `APPLIES_TO` | Affects which actors | — |
| `ENFORCES` | Authority enforces | — |
| `INTERPRETS` | Recital/Guideline → Article | `(GDPR_REC_71)-[:INTERPRETS]->(GDPR_ART_22)` |
| `CITES` | CaseLaw/Enforcement → Article | `(ENF_CLEARVIEW_AI)-[:CITES]->(GDPR_ART_9)` |
| `COMPLEMENTS` | Cross-regulation link | `(GDPR_ART_22)-[:COMPLEMENTS]->(AIACT_ART_14)` |

**COMPLEMENTS subtypes (5):** `REINFORCES`, `CO_TRIGGERS`, `CREATES_EXCEPTION`, `CUMULATIVE`, `DELEGATES`

### 2.3 Entity ID Naming Convention

| Pattern | Example | Meaning |
|---------|---------|---------|
| `GDPR_ART_{N}` | `GDPR_ART_35` | GDPR Article |
| `AIACT_ART_{N}` | `AIACT_ART_6` | AI Act Article |
| `GDPR_DEF_{TERM}` | `GDPR_DEF_BIOMETRIC_DATA` | GDPR Definition |
| `AIACT_DEF_{TERM}` | `AIACT_DEF_AI_SYSTEM` | AI Act Definition |
| `AIACT_ANNEX_{ROMAN}` | `AIACT_ANNEX_III` | AI Act Annex |
| `ANNEX_III_{N}` | `ANNEX_III_1` | Annex III Category |
| `OBL_GDPR_{NAME}` | `OBL_GDPR_LAWFUL_BASIS` | Obligation |
| `AUTH_{ACRONYM}` | `AUTH_EDPB` | Authority |
| `CJEU_C_{NUM}` | `CJEU_C_311_18` | Case Law |
| `ENF_{NAME}` | `ENF_CLEARVIEW_AI` | Enforcement Action |
| `RISK_{LEVEL}` | `RISK_PROHIBITED` | Risk Category |
| `AIST_{TYPE}` | `AIST_CHATBOT` | AI System Type |

### 2.4 Key Article Node Properties

```json
{
  "id": "GDPR_ART_35",
  "type": "Article",
  "title": "Data protection impact assessment",
  "regulation_id": "GDPR",
  "chapter": "Chapter 4",
  "article_number": "35",
  "full_text": "<complete article text>",
  "paragraphs": { "1": "...", "2": "...", "3": { "intro": "...", "a": "...", "b": "..." } },
  "modality": "MUST",
  "applies_to_actors": ["controller"],
  "cross_references": ["GDPR_ART_36", "GDPR_ART_9"]
}
```

### 2.5 Current Graph Statistics

| Metric | Count |
|--------|-------|
| Total Nodes | 2,301 |
| Total Relationships | 4,431 |
| Entity Types | 17 |
| Relationship Types | 13 |
| COMPLEMENTS (cross-reg) edges | 84 |
| Articles (GDPR + AI Act) | 212 |
| Recitals | 353 |
| Obligations | 1,325 |
| Exemptions | 96 |
| Definitions | 90 |
| Concepts | 47 |
| Rights | 19 |
| Avg relationships/article | 19.1 |
| Orphan nodes | 0 |
| Connectivity | 100% |

### 2.6 Key Cross-Regulation Relationships

```
(ANNEX_III_1)  -[:CO_TRIGGERS]-> (GDPR_ART_35)       -- Biometrics → DPIA
(GDPR_ART_22)  -[:COMPLEMENTS]-> (AIACT_ART_14)       -- ADM ↔ Human oversight
(AIACT_ART_14) -[:REFERENCES]->  (GDPR_ART_22)        -- Human oversight ↔ ADM
(AIACT_ART_5)  -[:PROHIBITS]->   (AIST_EMOTION_RECOG) -- Prohibited systems
(AIACT_ART_6)  -[:REFERENCES]->  (AIACT_ANNEX_III)    -- High-risk categories
(GDPR_ART_83)  -[:CUMULATIVE]->  (AIACT_ART_99)       -- Stacking fines
```

### 2.7 Example Graph Traversals

**"Does facial recognition require a DPIA?"**
```
facial_recognition → AIACT_DEF_BIOMETRIC_ID → ANNEX_III_1 → GDPR_ART_35 (via TRIGGERS)
                   → GDPR_ART_9 (via REGULATED_BY → GDPR_DEF_BIOMETRIC_DATA)
```

**"What AI practices are prohibited?"**
```
AIACT_ART_5 -[:PROHIBITS]→ [subliminal manipulation, social scoring,
                             real-time biometric in public, emotion recognition workplace, ...]
```

**"AI hiring system requirements"**
```
ANNEX_III_4 (Employment) → AIACT_ART_6 (High-risk) → GDPR_ART_22 (Automated decisions)
                         → AIACT_ART_14 (Human oversight) → AIACT_ART_43 (Conformity)
```

---

## 3. Retrieval Pipeline

### 3.1 Vector Store (JSON-backed, 7 collections)

| Collection | Content | Docs |
|------------|---------|------|
| `articles` | Article paragraphs (GDPR + AI Act) | 212 |
| `recitals` | Interpretive recitals | 353 |
| `obligations` | Extracted obligations | 1,421 |
| `definitions` | Legal definitions | 90 |
| `concepts` | Compliance concepts | 47 |
| `rights` | Data subject rights | 19 |
| `interpretive` | Case law + guidelines + enforcement | 56 |
| **Total** | | **2,132+** |

- **Embedding model:** `gemini-embedding-001` (3,072 dims)
- **Similarity:** Cosine
- **Note:** ChromaDB incompatible with Python 3.14 — custom JSON-backed store used

### 3.2 Hybrid Search (RRF Fusion)

```
Vector search → semantic similarity → ranked list A
Graph traversal → keyword/structural → ranked list B
RRF_score = Σ 1/(60 + rank_i)  for each list containing the entity
```

### 3.3 Multi-Hop Reasoning Pipeline

```
1. Vector search → seed entities (7 collections)
2. Graph traversal from seeds (N hops via Neo4j)
3. Build context from entities + paths
4. Gemini LLM synthesizes answer (gemini-2.0-flash)
5. Validate citations (anti-hallucination: all cited articles must appear in retrieval)
6. Score confidence: result count (30%) + fusion overlap (30%) + citation validity (40%)
```

**Rate limiting:** 4s delay between LLM calls (15 RPM free tier)

### 3.4 Query Types

| Type | Request Model | Use Case |
|------|--------------|----------|
| Compliance query | `ComplianceQueryRequest` | General compliance questions |
| Risk classification | `RiskClassificationRequest` | AI system risk tier |
| Obligation lookup | `ObligationLookupRequest` | "What must we do?" |
| Cross-regulation | `CrossRegulationRequest` | GDPR ↔ AI Act interaction |

**Answer templates (6):** `prohibition`, `obligation`, `conditional_permission`, `non_applicable`, `legal_uncertainty`, `general`

---

## 4. Agent Architecture (Core 3)

### 4.1 LangGraph Workflow

```
classify_risk → check_human_review → [conditional]
                                      ├─ needs_review → await_approval (INTERRUPT) → assess_gdpr
                                      └─ proceed → assess_gdpr
assess_gdpr → research_legal → check_conflicts → generate_docs → synthesize → END
```

Human review triggered when: classification = PROHIBITED, or HIGH_RISK with confidence < 80%, or conflicting agent outputs.

### 4.2 Agent Components

| Agent | File | Lines | Role |
|-------|------|-------|------|
| Supervisor | `supervisor.py` | 552 | LangGraph orchestrator, conflict detection, synthesis |
| Risk Classifier | `risk_classifier.py` | 398 | EU AI Act 4-tier classification (Art 5, Annex III) |
| Technical Assessor | `technical_assessor.py` | 424 | GDPR audit (Arts 5, 6, 9, 22, 32) |
| Legal Research | `legal_research.py` | 389 | Calls Core 2 GraphRAG API with retry/fallback |
| Documentation Generator | `documentation_generator.py` | 443 | DPIA, ROPA, Conformity Assessment, Transparency Notice |

### 4.3 Risk Classification Logic

| Category | Article | Trigger |
|----------|---------|---------|
| **PROHIBITED** | Article 5 | Social scoring, subliminal manipulation, real-time biometric in public, emotion detection in workplace/education |
| **HIGH_RISK** | Annex III | Biometrics, critical infrastructure, employment, education, credit scoring, law enforcement |
| **LIMITED_RISK** | Article 52 | Chatbots, deepfakes (transparency required) |
| **MINIMAL_RISK** | — | No specific obligations |

### 4.4 Assessment Sequence

```
User → Core 3: POST /api/v1/assessments
  Supervisor activates workflow
  Risk Classifier → classification + confidence
  Technical Assessor → GDPR violations
  Core 3 → Core 2: Legal research query (hybrid/reason endpoint)
    Core 2: Hybrid search (Neo4j + Vector) → Multi-hop reasoning
    Core 2 → Core 3: Citations + reasoning chains
  Documentation Generator → DPIA, ROPA, Conformity docs
  Supervisor → synthesizes final report
User receives: Complete compliance report + documents
```

### 4.5 SystemProfile Schema (input to KB queries)

```python
class SystemProfile(BaseModel):
    system_name: str
    capabilities: list[str]           # ["facial_recognition", "attendance_tracking"]
    data_types_processed: list[str]   # ["biometric", "employee_records"]
    special_category_data: list[str]
    deployment_context: str           # "workplace", "public_space"
    decision_types: list[str]
    autonomy_level: str               # "fully_automated", "human_in_loop"
    operator_role: str                # "provider", "deployer"
    cross_border_transfers: bool
```

**Field → KG mapping:**

| Field | Maps To | Relationship |
|-------|---------|-------------|
| `data_types_processed` | DataType nodes | → REGULATED_BY → Article |
| `capabilities` | AISystemType nodes | → CLASSIFIED_AS → RiskCategory |
| `deployment_context` | Annex III categories | → maps to HIGH_RISK |
| `operator_role` | Actor nodes | → RESPONSIBLE_FOR → Obligation |

---

## 5. Cross-Module Integration

### 5.1 Integration Points

| Integration | Mechanism | Endpoint | Data Flow |
|-------------|-----------|----------|-----------|
| Core 3 → Core 2 | HTTP (httpx + tenacity retry) | `POST /api/v1/hybrid/reason` | Legal queries → citation chains |
| Core 3 → Core 1 | MonitoringClient SDK | `POST /api/v1/monitoring/agent-decision` | Agent decisions → drift/bias monitoring |
| Core 2 → Core 1 | MonitoringClient SDK | `POST /api/v1/monitoring/graphrag-query` | Query metrics → performance monitoring |

**Note:** Core 3 → Core 1 integration exists (SDK in `core_1/src/client/monitoring_client.py`) but is not yet wired into Core 3 agents. See `PROJECT_ANALYSIS.md` Priority 2 item #7.

### 5.2 Integration Code Example

```python
# Core 3: Legal Research Agent calls Core 2
class LegalResearchAgent:
    async def research(self, query: str) -> dict:
        response = await httpx.post(
            f"{self.graphrag_url}/api/v1/hybrid/reason",
            json={"question": query}
        )
        return response.json()  # citations + reasoning chains
```

### 5.3 URL Configuration

| Env Var | Default | Used By |
|---------|---------|---------|
| `GRAPHRAG_API_URL` | `http://localhost:8001` | Core 3 Legal Research Agent |
| `MONITORING_API_URL` | `http://localhost:8002` | Core 3/2 MonitoringClient |

---

## 6. Data Types & Risk Categories

### DataType Hierarchy

```
DataType
├── PersonalData
│   ├── SpecialCategoryData
│   │   ├── BiometricData
│   │   ├── HealthData
│   │   ├── GeneticData
│   │   ├── RacialEthnicData
│   │   └── PoliticalOpinionData
│   └── RegularPersonalData
│       ├── ContactData
│       ├── LocationData
│       └── BehavioralData
└── NonPersonalData
    ├── AnonymisedData
    ├── AggregatedData
    └── PseudonymisedData (→ PersonalData by GDPR)
```

### RiskCategory Hierarchy

```
RiskCategory
├── PROHIBITED (Art 5)
│   ├── SubliminalManipulation
│   ├── SocialScoring (govt)
│   ├── RealTimeBiometricPublic
│   ├── EmotionRecognitionWorkplace
│   └── EmotionRecognitionEducation
├── HIGH_RISK (Annex III)
│   ├── BiometricIdentification
│   ├── CriticalInfrastructure
│   ├── Education/Training
│   ├── Employment/HR
│   ├── EssentialServices (credit, insurance)
│   ├── LawEnforcement
│   ├── MigrationAsylum
│   └── JusticeAdministration
├── LIMITED_RISK (Art 50)
│   ├── Chatbots
│   ├── EmotionRecognition (non-prohibited)
│   └── Deepfakes
└── MINIMAL_RISK (everything else)
```

### Knowledge Base Query Interface

| Consumer | Query | Expected Output |
|----------|-------|----------------|
| Risk Classifier Agent | System capabilities | `(AISystemType, RiskCategory, source Article)` tuples |
| Legal Research Agent | Legal question | Answer + cited entities + reasoning chain |
| Technical Assessor | GDPR obligations | Applicable articles + conditions |
| Documentation Generator | Obligation set | Organised obligations + citations for DPIA/ROPA |

---

## 7. Cross-Regulation Mappings

### GDPR ↔ AI Act Article Mappings

| GDPR | Relationship | AI Act | Rationale |
|------|-------------|--------|-----------|
| Art 5 (principles) | COMPLEMENTS | Art 10 (data governance) | AI data must follow GDPR principles |
| Art 9 (special categories) | COMPLEMENTS | Art 10(5) (bias detection) | Narrow exception for debiasing |
| Art 22 (automated decisions) | COMPLEMENTS | Art 14 (human oversight) | Both require human involvement |
| Art 25 (privacy by design) | COMPLEMENTS | Art 9 (risk management) | Both mandate built-in safeguards |
| Art 35 (DPIA) | COMPLEMENTS | Art 6 + Art 27 (risk + FRIA) | High-risk AI triggers DPIA |
| Art 13–14 (transparency) | COMPLEMENTS | Art 13 + Art 50 (transparency) | Both mandate informing individuals |
| Art 83 (admin fines) | CUMULATIVE_WITH | Art 99 (penalties) | Penalties can stack |

### Actor Mappings

| GDPR Actor | AI Act Actor | Relationship |
|------------|-------------|-------------|
| Controller | Provider / Deployer | MAY_BE |
| Processor | Provider | MAY_BE |
| Data Subject | Affected Person | EQUIVALENT |
| DPA | AI Office | COORDINATES_WITH |
| EDPB | AI Board | COORDINATES_WITH |

### Architectural Gaps (still relevant for KB improvements)

**GAP A: Articles treated as atomic units**
Articles stored as single entities — breaks for multi-clause articles (Art 6, Art 9, Art 22).
Fix: paragraph-level nodes with sub-item granularity.

**GAP B: Conditions & exceptions are implicit**
Conditions stored as flat lists, not navigable graph entities.
Fix: Exemption nodes with `HAS_EXCEPTION` relationships.

**GAP C: No negative knowledge**
System doesn't know when requirements DON'T apply (research exemptions, SME carve-outs).
Fix: Model exclusions as explicit graph paths.

**GAP D: Missing procedural workflows**
Static rules only — no decision trees or step-by-step compliance procedures.
Fix: Workflow nodes (DPIA procedure, conformity assessment steps).

---

## 8. EU AI Act Enforcement Timeline

| Date | Requirement |
|------|-------------|
| Feb 2, 2025 | Prohibited AI systems ban takes effect |
| Aug 2, 2025 | Governance structure requirements |
| Aug 2, 2026 | General-purpose AI (GPAI) model obligations |
| Aug 2, 2027 | High-risk AI system requirements (MAIN deadline) |

---

## 9. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| LLM | Gemini 2.0 Flash | Reasoning, classification |
| Embeddings | gemini-embedding-001 (3,072 dims) | Semantic search |
| Agent Framework | LangGraph + LangChain | Workflow orchestration |
| API | FastAPI | REST endpoints |
| Graph DB | Neo4j 5.x Community | Structural knowledge |
| Vector Store | JSON-backed (custom) | Semantic search (ChromaDB incompatible with Py 3.14) |
| Relational DB | PostgreSQL 15 | Audit logs, assessments |
| Cache | Redis 7 | Session state |
| Monitoring | Prometheus + Evidently | Metrics, drift |
| Rate Limiting | SlowAPI | 60 req/min |
| Package Manager | UV | Modern pip/poetry replacement |
| Linter | Ruff | Replaces flake8, isort, black |

**Gemini SDK note:** Use `google-genai` (`genai.Client()` API), NOT deprecated `google-generativeai`.

---

## 10. Business Impact

| Metric | Manual Process | With System | Improvement |
|--------|---------------|-------------|-------------|
| Assessment time | 40 hours | 6.5 hours | **84%** |
| Cost per assessment | £8,500 | £1,200 | **86%** |
| Annual savings (15/mo) | — | £1.3M | — |
| Fine prevention | Unknown | Up to €35M | Risk mitigation |
| Compliance detection time | Weeks | < 48 hours | Faster response |
| Legal research cost | £2,500/query | £0.08/query | 31,250× cheaper |

### Interview Pitch

> "I built an autonomous EU AI Act compliance platform that saves companies £1.3M/year by reducing assessment time from 40 hours to 6.5 hours. It uses a 5-agent LangGraph system where the Legal Research Agent makes real API calls to my GraphRAG system for multi-hop reasoning across 2,301 graph nodes covering EU AI Act and GDPR. The monitoring module tracks all agent decisions for EU AI Act Article 14 compliance and triggers alerts when quality degrades."
