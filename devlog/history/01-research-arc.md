---
title: AlloyCode — Preserved research arc
status: archived
snapshot_date: 2026-05-20
purpose: |
  Verbatim concatenation of the source documents that produced the AlloyCode
  design. Includes the `gdpr context/main/` polished docs, the
  `gdpr context/backup/` raw brainstorm trail, and the pre-pivot `docs/archive/`
  contents. For a read-once narrative summary, see `00-history-and-decisions.md`.
ai_guidance: |
  This is a historical archive of primary sources, frozen at snapshot_date.
  Every source file is preserved verbatim under a section divider that names
  the original path. It is NOT a guide to the current system; specific facts
  here (article counts, schema details, even service names like `core_1`/
  `core_2`/`core_3`) have been superseded. For current state, read
  ../SYSTEM.md. Use this file as a primary-source citation archive; verify
  any specific claim against SYSTEM.md and the code before acting.
---

> **⚠ This is a historical archive, frozen at 2026-05-20.**
> For the current system, see [`../SYSTEM.md`](../SYSTEM.md).
> For active proposals, see [`../design-evolution/`](../design-evolution/).
> For a read-once distilled narrative, see [`00-history-and-decisions.md`](00-history-and-decisions.md).
> Decisions in this file may have been superseded — verify against `SYSTEM.md` before acting on any claim here.

---

# AlloyCode — preserved research arc

Verbatim concatenation of every source document that produced the AlloyCode design. Sources are grouped into three runs:

1. **`gdpr context/main/`** — the four polished portfolio-pitch docs (dated 2026-02-12). Merged from earlier per-project docs.
2. **`gdpr context/backup/`** — the raw brainstorm trail. Pre-merge per-project docs, gap audits, iterative critiques.
3. **`docs/archive/`** — pre-pivot operational state: the previous `README.md`, `CLAUDE.md`, `REFERENCE.md`, KG project context, data-scraper documentation, the pre-pivot `MEMORY.md`.

Each section is prefixed with a `## SOURCE:` divider naming the original path. Original front matter (if any) is preserved as-is.

---



---

# Run: gdpr context/main

---


## SOURCE: `gdpr context/main/01_PROJECT_PORTFOLIO.md`

# PROJECT PORTFOLIO: EU AI Regulatory Compliance Platform

**Merged from:** `Project 2 AI Model Governance & Compliance Monitoring Pipeline.md`, `Project 3 GraphRAG Legal Research Engine.md`, `project_4 EU AI Act Compliance Automation Agent.md`
**Date:** 2026-02-12

---

## Portfolio Overview

This platform comprises 4 integrated projects forming an end-to-end EU AI Act & GDPR compliance automation system:

```
┌──────────────────────────────────────────────────────────────┐
│  PROJECT 1 (Basic RAG)  │  PROJECT 3 (GraphRAG)              │
│  Regulatory knowledge   │  Legal research engine              │
└────────────┬─────────────┴──────────────┬────────────────────┘
             │                            │
             │         Provides data to   │
             │                            │
             ↓                            ↓
┌──────────────────────────────────────────────────────────────┐
│              PROJECT 4 (Multi-Agent Compliance)              │
│         Autonomous Compliance Assessment                     │
│  Makes 200 compliance decisions/day using Projects 1 & 3    │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      │ Every decision tracked
                      ↓
┌──────────────────────────────────────────────────────────────┐
│              PROJECT 2 (MLOps Governance)                     │
│         Monitors ALL systems for compliance                  │
│  Drift detection, bias detection, Article 14 compliance      │
└──────────────────────────────────────────────────────────────┘
```

---

# PROJECT 2: AI Model Governance & Compliance Monitoring Pipeline

**"The Operational Backbone of Your Compliance Platform"**

**Duration:** 6–8 weeks (40–50 hours)
**Target Market:** UK/EU AI Engineering roles (£70K–£90K)
**Differentiation Score:** 9/10 (MLOps + EU AI Act compliance is extremely rare)
**Market Timing:** CRITICAL (EU AI Act Article 15 requires monitoring systems)

## Executive Summary

Builds an **AI Model Governance Pipeline** that monitors deployed AI systems for EU AI Act and GDPR compliance:

- **EU AI Act Article 14 compliance**: Human oversight requirements for high-risk systems
- **GDPR Article 22 compliance**: Automated decision-making transparency
- **Agent decision quality**: Tracks Project 4's multi-agent system performance
- **GraphRAG reliability**: Monitors Project 3's legal research API
- **Bias detection**: Protected attributes influence on decisions
- **Compliance drift**: When deployed models violate regulatory requirements

**Business Impact:**
- Prevents **€35M EU AI Act fines** by detecting violations before regulators
- Reduces **mean time to detect degradation** from weeks → 48 hours
- Saves **£180K/year** vs manual compliance audits (quarterly @ £45K each)

## Competitive Landscape

| Approach | Example | Your Edge |
|----------|---------|-----------|
| Traditional MLOps | NASA tutorial | No compliance focus |
| AI Governance Tools | Guardrails AI | No end-to-end monitoring |
| Compliance Platforms | OneTrust | No real-time ML monitoring |
| **Your System** | This project | **Compliance + Performance + Integration** |

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORED SYSTEMS                            │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │   PROJECT 4      │    │   PROJECT 3      │                 │
│  │  Multi-Agent     │    │  GraphRAG API    │                 │
│  └────────┬─────────┘    └────────┬─────────┘                 │
│           │ Decision logs         │ Query metrics              │
└───────────┼───────────────────────┼────────────────────────────┘
            ↓                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                         │
│  FastAPI Endpoints: /agent-decision, /graphrag-query            │
└───────────┬───────────────────────┬──────────────────────────┘
            ↓                       ↓
┌─────────────────────────────────────────────────────────────────┐
│ STORAGE: PostgreSQL (audit) | Prometheus (metrics) | MLflow    │
└───────────┬───────────────────────┬──────────────────────────┘
            ↓                       ↓
┌─────────────────────────────────────────────────────────────────┐
│              MONITORING & ANALYSIS LAYER                        │
│  EU AI Act Art 14/15 | GDPR Art 22 | Drift | Bias | Alerts    │
└─────────────────────────────────────────────────────────────────┘
```

## Core Monitoring Capabilities

### Agent Decision Monitor
```python
class ComplianceAgentMonitor:
    def track_agent_decision(self, decision_data: dict):
        self.decision_counter.inc()
        self.confidence_histogram.observe(decision_data["confidence"])
        self._check_prediction_drift(decision_data)
        self._check_human_oversight_compliance(decision_data)
        self._check_for_bias(decision_data)

    def _check_human_oversight_compliance(self, decision: dict):
        # EU AI Act Article 14: High-risk → needs human review
        if decision["prediction"] == "HIGH_RISK" and not decision["human_reviewed"]:
            # Alert if policy violated
            ...
```

### GraphRAG Monitor
```python
class GraphRAGMonitor:
    def track_graphrag_query(self, query_data: dict):
        self.graphrag_latency.observe(query_data["latency_ms"])
        self._check_citation_quality_drift(query_data)
        if query_data["latency_ms"] > 3000:
            self.send_alert(...)
```

### Drift & Bias Detection
- Evidently AI for drift detection (data, prediction, confidence drift)
- Chi-square bias tests on protected attributes
- Alerting thresholds: drift p-value < 0.05, confidence drop > 0.1

---

# PROJECT 3: GraphRAG Legal Research Engine

**"The Context Architecture for Compliance Intelligence"**

**Duration:** 8–10 weeks (50–60 hours)
**Target Market:** UK/EU AI Engineering roles (£70K–£90K)
**Differentiation Score:** 9/10 (GraphRAG for legal domain is extremely rare)
**Market Timing:** CRITICAL (Positions as "Context Architect" — emerging 2026 role)

## Executive Summary

Builds a **Legal Knowledge Graph + RAG system** with multi-hop reasoning across EU AI Act and GDPR:

- *"If my AI system processes biometric data for employment decisions, which GDPR articles apply AND which EU AI Act requirements must I meet?"*
- *"What is the relationship between GDPR Article 22 (automated decision-making) and EU AI Act Annex III high-risk categories?"*
- *"Trace the legal chain: facial recognition → biometric data → special category data → obligations?"*

**Business Impact:**
- Traditional legal research: 10 hours @ £250/hr = **£2,500** per complex query
- GraphRAG system: 2 minutes @ £0.08 = **£0.08** per query
- **31,250× cost reduction** with 80% better accuracy on multi-hop questions

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION LAYER                        │
│  EU AI Act (113 Articles) | GDPR (99 Articles) | Directives    │
│              ↓ DOCLING PARSER ↓                                 │
└──────────────────────────┼─────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────────┐
│  ENTITY EXTRACTION: Articles, Concepts, Requirements, Rels      │
└──────────────────────────┼──────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        │  Hybrid Retrieval Engine (RRF)       │
        └─────┬──────────────┬────────────────┘
              │              │
   ┌──────────▼──────┐  ┌───▼────────────────┐
   │   Neo4j 5.x     │  │  ChromaDB          │
   │   Graph Store    │  │  Vector Store      │
   │ • Multi-hop      │  │ • Gemini embeddings│
   │   traversal      │  │ • Cosine similarity│
   └──────────────────┘  └────────────────────┘
```

## Core Capabilities

- **Knowledge Graph (Neo4j):** Entity nodes (14 types), relationship edges (18+ types), Cypher multi-hop traversal
- **Vector Store (ChromaDB):** Gemini embeddings, cosine similarity, metadata-filtered search
- **Hybrid Retrieval:** Reciprocal Rank Fusion (RRF) combining graph + vector results
- **Multi-Hop Reasoner:** LLM-powered chain-of-thought over graph paths with citations

## Key Query Patterns

| Pattern | Example | Method |
|---------|---------|--------|
| Risk Classification | "Is facial recognition HIGH_RISK?" | Graph traversal: capability → Annex III → risk level |
| DPIA Triggers | "Does health data AI need DPIA?" | Graph: DataType → Art 9 → Art 35 |
| Cross-Regulation | "Combined GDPR + AI Act for recruitment AI?" | Cross-regulation COMPLEMENTS edges |
| Precedent Lookup | "Who was fined for similar systems?" | Enforcement → CITES → Articles |
| Semantic Discovery | "transparency requirements for chatbots" | Hybrid RRF search |

---

# PROJECT 4: EU AI Act Compliance Automation Agent

**"The Autonomous Compliance Engine"**

**Duration:** 10–12 weeks (80–100 hours)
**Target Market:** UK/EU AI Engineering roles (£70K–£90K)
**Differentiation Score:** 10/10 (First-of-its-kind portfolio project)
**Market Timing:** CRITICAL (EU AI Act enforcement begins August 2026)

## Executive Summary

The **first autonomous EU AI Act compliance system** using 5-agent orchestration. Companies upload AI system specs and within 6 hours (vs. 6 weeks manual) receive:
- Risk classification (Prohibited/High-Risk/Limited/Minimal)
- GDPR compliance audit
- Legal citation report (using GraphRAG from Project 3)
- Production-ready compliance documentation (DPIA, Conformity Assessment)

**Business Impact:** Saves £6,800 per assessment = **£102,000/year** (15 assessments/month).

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Next.js)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              COMPLIANCE SUPERVISOR AGENT                    │
│  (LangGraph Orchestrator)                                   │
└─────────┬────────────┬────────────┬────────────┬───────────┘
          │            │            │            │
┌─────────▼────┐ ┌─────▼─────┐ ┌───▼──────┐ ┌──▼────────────┐
│ RISK         │ │ TECHNICAL │ │ LEGAL    │ │ DOCUMENTATION │
│ CLASSIFIER   │ │ ASSESSOR  │ │ RESEARCH │ │ GENERATOR     │
│              │ │           │ │          │ │               │
│ EU AI Act    │ │ GDPR      │ │ GraphRAG │ │ DPIA, ROPA,   │
│ Art 5/Annex  │ │ Articles  │ │ (Proj 3) │ │ Conformity    │
└──────────────┘ └───────────┘ └──────────┘ └───────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  AGENT CONTROL PLANE: Governance, Human-in-Loop, Audit      │
└─────────────────────────────────────────────────────────────┘
```

## Agent Specifications

### 1. Supervisor Agent (469 lines)
- LangGraph state machine orchestration
- Task decomposition and routing
- Conflict detection between agent outputs
- Human-in-loop approval for HIGH_RISK/PROHIBITED
- Final report synthesis

### 2. Risk Classifier Agent (399 lines)
- 4-tier classification: PROHIBITED → HIGH_RISK → LIMITED_RISK → MINIMAL_RISK
- Checks against Art 5 prohibited patterns (8 categories)
- Matches Annex III high-risk categories (8 categories)
- Confidence scoring

### 3. Technical Assessor Agent (GDPR Auditor)
- Audits against GDPR Articles 5, 6, 9, 13, 17, 22, 25, 35
- Returns violations (HIGH/MEDIUM/LOW), warnings, and recommendations

### 4. Legal Research Agent (GraphRAG Integration)
- Real HTTP calls to Project 3's `/api/v1/hybrid/reason` endpoint
- Multi-hop reasoning across 200+ articles
- Returns citation chains with reasoning paths

### 5. Documentation Generator Agent
- Generates: DPIA, ROPA, Conformity Assessment, Transparency Notice
- Template-based with agent findings populated

## Golden Test Dataset (12 cases)

| ID | System Type | Expected Classification | GDPR Issues |
|----|-------------|------------------------|-------------|
| 001 | Facial recognition (employee) | HIGH_RISK | Art 9 (biometric) |
| 002 | Emotion detection (education) | PROHIBITED | — |
| 003 | Customer chatbot | LIMITED_RISK | None |
| 004 | Credit scoring | HIGH_RISK | Art 22 (automated) |
| 005 | CV screening | HIGH_RISK | Art 22 |
| 006 | Social scoring (govt) | PROHIBITED | — |
| 007 | Medical diagnosis | HIGH_RISK | Art 9 (health) |
| 008 | Real-time biometric (public) | PROHIBITED | — |
| 009 | Spam filter | MINIMAL_RISK | None |
| 010 | Exam proctoring | HIGH_RISK | Art 9 |
| 011 | Workplace emotion | PROHIBITED | — |
| 012 | Insurance pricing | HIGH_RISK | — |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/assessments` | POST | Start assessment |
| `/api/v1/assessments/{id}` | GET | Get results |
| `/api/v1/approvals` | GET | Pending human approvals |
| `/api/v1/approvals/{id}/decide` | POST | Approve/reject |
| `/api/v1/documents/{id}` | GET | Download documents |
| `/api/v1/statistics` | GET | System stats |
| `/api/v1/audit-log` | GET | Audit trail |

## Business Impact & ROI

| Metric | Manual | Automated | Savings |
|--------|--------|-----------|---------|
| Time per assessment | 40 hours | 6.5 hours | **84%** |
| Cost per assessment | £8,500 | £1,200 | **86%** |
| Annual (15/month) | — | — | **£1.3M** |
| Fine prevention | Unknown | Up to €35M | **Risk mitigation** |

## Technology Stack (All Projects)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| LLM | Gemini 1.5 Pro/Flash | Reasoning, classification |
| Embeddings | text-embedding-004 | Semantic search |
| Agent Framework | LangGraph + LangChain | Workflow orchestration |
| API | FastAPI | REST endpoints |
| Graph DB | Neo4j 5.x | Knowledge graph |
| Vector DB | ChromaDB | Semantic embeddings |
| Relational DB | PostgreSQL | Audit logs, state |
| Cache | Redis | Session state |
| Monitoring | Prometheus + Evidently | Metrics, drift |

---

## Cross-Project Integration Summary

| Integration | How | What's Monitored |
|---|---|---|
| P4 → P3 | Legal Research Agent calls GraphRAG API | Query latency, citation quality, cost |
| P4 → P2 | Agent decisions sent to monitoring | Accuracy drift, bias, Article 14 compliance |
| P3 → P2 | GraphRAG metrics forwarded | Latency, uptime, confidence drift |
| P1 → P2 | RAG responses tracked (optional) | Hallucination rate, faithfulness |

**Interview Pitch:**
> "I built an autonomous EU AI Act compliance platform that saves companies £1.3M/year by reducing assessment time from 40 hours to 6.5 hours. It uses a 5-agent LangGraph system where the Legal Research Agent makes real API calls to my GraphRAG system (Project 3) for multi-hop reasoning. Project 2 monitors all agent decisions for EU AI Act Article 14 compliance and triggers alerts when quality degrades. This isn't a demo — it's a production system solving a real £8,500-per-assessment problem."

---

## Overall Assessment

| Capability | Rating |
|---|---|
| Multi-Agent Orchestration | ⭐⭐⭐⭐⭐ |
| Domain Expertise (EU AI Act + GDPR) | ⭐⭐⭐⭐⭐ |
| System Integration | ⭐⭐⭐⭐⭐ |
| Production Readiness | ⭐⭐⭐⭐⭐ |
| Business Value | ⭐⭐⭐⭐⭐ |
| Market Timing | ⭐⭐⭐⭐⭐ |

**Project Maturity:** 8.5/10 (Production-Ready)
**Market Positioning:** Ready for £70K–£90K AI/ML Engineer roles in UK/EU

---

*Merged from: `Project 2 AI Model Governance & Compliance Monitoring Pipeline.md`, `Project 3 GraphRAG Legal Research Engine.md`, `project_4 EU AI Act Compliance Automation Agent.md`. Originals preserved.*


---


## SOURCE: `gdpr context/main/02_ARCHITECTURE_AND_INTEGRATION.md`

# SYSTEM ARCHITECTURE, INTEGRATION & COMPONENT REFERENCE

**Merged from:** `SYSTEM_ARCHITECTURE.md`, `Integration Architecture How Projects Actually Connect.md`, `PROJECT_ANALYSIS.md`, `PROJECT_STORY.md`
**Date:** 2026-02-12

---

## 1. High-Level System Architecture

The EU AI Regulatory Compliance Engine is a 3-core platform:

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
│     • Neo4j Knowledge Graph                                   │
│     • ChromaDB Vector Store                                   │
│     • Hybrid Retrieval (RRF) + Multi-Hop Reasoning           │
└────────────┬─────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│     CORE 1: Monitoring & Governance (Port 8002)              │
│     • EU AI Act Article 14 compliance (human oversight)      │
│     • Bias detection, drift detection                        │
│     • Prometheus metrics                                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Data Layer Architecture (Core 2)

### 2.1 Data Sources (JSON Files)

All source data under `core_2/data/`:

**Legal Core (`data/legal/`):**

| File | Content | Records |
|------|---------|---------|
| `gdpr_articles.json` | 14 GDPR articles + 6 definitions | 20 entities |
| `eu_ai_act_articles.json` | 13 EU AI Act articles + 2 annexes + 7 definitions | 35 entities |
| `gdpr_structure.json` | Complete index: 99 articles, 173 recitals, 11 chapters | Reference |
| `eu_ai_act_structure.json` | Complete index: 113 articles, 13 chapters, 13 annexes | Reference |

**Entity Enrichment (`data/entities/`):**

| File | Content |
|------|---------|
| `obligations.json` | ~40 obligations (GDPR + AI Act), penalty tiers |
| `concepts_and_principles.json` | 14 principles, 20+ concepts, hierarchies |
| `authorities.json` | 5 EU-level + 12 national DPAs |
| `rights_and_remedies.json` | 12 GDPR + 5 EU AI Act rights |
| `penalties.json` | GDPR tiers + AI Act tiers + SME provisions |
| `cross_regulation_mappings.json` | 25 cross-regulation links, 8 scenarios |

**Interpretive (`data/interpretive/`):**

| File | Content |
|------|---------|
| `case_law.json` | 11 landmark CJEU cases |
| `edpb_guidelines.json` | 15 key EDPB/WP29 guidelines |
| `enforcement_actions.json` | 15 major enforcement actions |

---

## 3. Neo4j Knowledge Graph Schema

### 3.1 Entity Types (14 currently, 19+ target)

| Label | Description | Example IDs |
|-------|-------------|-------------|
| `Regulation` | Top-level framework | `GDPR`, `EU_AI_ACT` |
| `Article` | Individual article | `GDPR_ART_5`, `AIACT_ART_6` |
| `Annex` | Technical annex | `AIACT_ANNEX_III` |
| `Definition` | Legal term | `GDPR_DEF_PERSONAL_DATA` |
| `Concept` | Abstract concept | `ANNEX_III_1` (Biometrics) |
| `Obligation` | Must/must-not requirement | `OBL_GDPR_LAWFUL_BASIS` |
| `Right` | Data subject right | — |
| `Penalty` | Fine/sanction | — |
| `Authority` | Regulatory body | `AUTH_EDPB` |
| `Actor` | Legal role | — |
| `DataType` | Data classification | — |
| `AISystemType` | AI risk classification | — |
| `RiskCategory` | Risk level | — |
| `Recital` | Interpretive recital | — |

### 3.2 Node Properties

Base properties (all nodes):
```
id, type, name, description, source_text, created_at, updated_at
```

| Specialized Type | Additional Properties |
|---|---|
| **Regulation** | `full_title`, `short_name`, `effective_date`, `jurisdiction` |
| **Article** | `regulation_id`, `article_number`, `title`, `full_text`, `chapter` |
| **Definition** | `term`, `definition_text`, `regulation_id`, `article_reference` |
| **Obligation** | `obligation_type`, `applies_to`, `conditions`, `source_article`, `deadline`, `penalty_reference` |

### 3.3 Relationship Types (20 defined, 25+ target)

**Structural:**
| Type | Meaning | Example |
|------|---------|---------|
| `CONTAINS` | Parent → Child | `(GDPR)-[:CONTAINS]->(GDPR_ART_5)` |
| `PART_OF` | Child → Parent | — |
| `REFERENCES` | Cross-reference | `(AIACT_ART_6)-[:REFERENCES]->(AIACT_ANNEX_III)` |
| `AMENDS` / `REPEALS` | Provision changes | — |

**Semantic:**
| Type | Meaning | Example |
|------|---------|---------|
| `DEFINES` | Definition provision | `(GDPR)-[:DEFINES]->(GDPR_DEF_PERSONAL_DATA)` |
| `REQUIRES` | Creates obligation | — |
| `PROHIBITS` | Forbids activity | `(AIACT_ART_5)-[:PROHIBITS]->(AIACT_DEF_EMOTION_RECOGNITION)` |
| `TRIGGERS` | Activates requirement | `(ANNEX_III_1)-[:TRIGGERS]->(GDPR_ART_35)` |
| `EXEMPTS` | Provides exception | — |

**Actor / Enforcement:**
| Type | Meaning |
|------|---------|
| `APPLIES_TO` | Affects which actors |
| `ENFORCED_BY` | Authority enforces |
| `RESPONSIBLE_FOR` | Actor responsibility |

**New (target):**
`INTERPRETS`, `HAS_EXCEPTION`, `COMPLEMENTS`, `SUPERSEDES`, `PENALISED_BY`, `CITES`

### 3.4 Current Graph Statistics

```
Total Nodes:          56
Total Relationships:  61
  Regulation: 2  |  Article: 27  |  Annex: 2  |  Definition: 13  |  Concept: 12
```

### 3.5 Key Cross-Regulation Relationships (7 loaded)

```
(ANNEX_III_1)  -[:TRIGGERS]->     (GDPR_ART_35)          -- Biometrics → DPIA
(GDPR_ART_22) -[:APPLIES_TO]->    (AIACT_DEF_AI_SYSTEM)  -- ADM → AI systems
(AIACT_ART_14)-[:REFERENCES]->    (GDPR_ART_22)          -- Human oversight ↔ ADM
(AIACT_ART_5) -[:PROHIBITS]->     (AIACT_DEF_EMOTION_RECOGNITION)
(AIACT_ART_6) -[:REFERENCES]->    (AIACT_ANNEX_III)
(AIACT_ANNEX_III)-[:TRIGGERS]->   (AIACT_ART_43)         -- Conformity assessment
```

---

## 4. ChromaDB Vector Store

- **Collection:** `legal_entities` (cosine similarity)
- **Embedding Model:** `gemini-embedding-001` (768 dims)
- **Task types:** RETRIEVAL_DOCUMENT (indexing), RETRIEVAL_QUERY (search)
- **Metadata:** `id`, `type`, `name`, `description` per entity

---

## 5. Retrieval Pipeline

### 5.1 Vector Search
```
User query → Gemini embedding → Cosine search → Top-K results
```

### 5.2 Graph Search
```
User query → Keyword match in Neo4j → Scored results
```

### 5.3 Hybrid Search (RRF Fusion)
```
RRF_score(entity) = Σ 1/(k + rank_i)   for each result list containing entity
k = 60 (default)
```

### 5.4 Multi-Hop Reasoning
```
1. Vector search → seed entities
2. Graph traversal from seeds (N hops)
3. Build context from entities + paths
4. Gemini LLM synthesizes answer
5. Extract citations + confidence
```

---

## 6. Agent Architecture (Core 3)

### Workflow (LangGraph State Machine)

```mermaid
stateDiagram-v2
    [*] --> RiskClassification
    RiskClassification --> HumanReview: HIGH_RISK/PROHIBITED
    RiskClassification --> GDPRAssessment: LIMITED/MINIMAL
    HumanReview --> AwaitApproval
    AwaitApproval --> GDPRAssessment: Approved
    GDPRAssessment --> LegalResearch
    LegalResearch --> ConflictCheck
    ConflictCheck --> DocumentGeneration
    DocumentGeneration --> SynthesizeReport
    SynthesizeReport --> [*]
```

### Agent Components

| Component | File | Role |
|-----------|------|------|
| Supervisor | `supervisor.py` (469 lines) | LangGraph orchestrator, conflict detection, synthesis |
| Risk Classifier | `risk_classifier.py` (399 lines) | EU AI Act 4-tier classification |
| Technical Assessor | `technical_assessor.py` | GDPR audit (Art 5, 6, 9, 22, 32) |
| Legal Research | `legal_research.py` | Calls Core 2 GraphRAG API |
| Documentation Generator | `documentation_generator.py` | DPIA, ROPA, Conformity Assessment |

### Sequence Diagram (Full Assessment Flow)

```
User → Core 3: POST /api/v1/assessments
  Core 3: Supervisor activates workflow
  Core 3: Risk Classifier → HIGH_RISK
  Core 3 → DB: Log decision
  Core 3 → Core 1: Report decision
    Core 1: Article 14 check + bias check
  Core 3: Technical Assessor → GDPR violations
  Core 3 → Core 2: Legal research query
    Core 2: Hybrid search (Neo4j + ChromaDB)
    Core 2: Multi-hop reasoning
    Core 2 → Core 3: Citations + reasoning chains
  Core 3: Documentation Generator → docs
  Core 3: Supervisor synthesizes report
  Core 3 → User: Complete assessment + documents
```

---

## 7. Monitoring Architecture (Core 1)

| Component | File | What It Does |
|-----------|------|-------------|
| Article 14 Monitor | `eu_ai_act.py` | Human oversight compliance for high-risk decisions |
| Drift Detector | `drift.py` | Data/prediction/confidence drift via Evidently |
| Bias Detector | `bias.py` | Chi-square fairness tests on protected attributes |
| Prometheus Metrics | `metrics.py` | Counters, histograms, gauges for observability |

---

## 8. Cross-Project Integration Architecture

### Integration Points (Concrete)

| Integration | Mechanism | Data Flow |
|---|---|---|
| P4 → P3 | HTTP API call to `/api/v1/hybrid/reason` | Legal queries → citation chains |
| P4 → P2 | Monitoring client SDK | Agent decisions → drift/bias monitoring |
| P3 → P2 | Monitoring client SDK | GraphRAG query metrics → performance monitoring |
| P2 Dashboard | FastAPI `/dashboard` endpoint | Unified view of all systems |

### Code-Level Integration Example

```python
# Project 4: Legal Research Agent calls Project 3
class LegalResearchAgent:
    def __init__(self, graphrag_api_url: str):
        self.graphrag_url = graphrag_api_url  # Project 3 API
        self.monitor = GraphRAGMonitor(api_url="http://project2-api:8080")

    async def research(self, query: str) -> dict:
        start_time = time.time()
        response = await httpx.post(
            f"{self.graphrag_url}/api/v1/hybrid/reason",
            json={"question": query}
        )
        latency_ms = (time.time() - start_time) * 1000
        result = response.json()
        await self.monitor.track_graphrag_query({...})
        return result
```

### Monitoring Dashboard

Tracks across all projects:
- Agent metrics: accuracy, human override rate, Article 14 compliance
- GraphRAG metrics: latency, confidence, uptime, cost
- RAG metrics: hallucination rate, faithfulness (optional)
- Compliance status: EU AI Act, GDPR, oversight active

---

## 9. Entity ID Naming Convention

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

---

## 10. Example Graph Traversals

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

## 11. Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| LLM | Gemini 1.5 Pro/Flash | Reasoning, classification |
| Embeddings | text-embedding-004 | 768-dim vectors |
| Agent Framework | LangGraph + LangChain | Orchestration |
| API | FastAPI | REST endpoints |
| Graph DB | Neo4j 5.x | Structural knowledge |
| Vector DB | ChromaDB | Semantic search |
| Relational DB | PostgreSQL | Audit logs |
| Cache | Redis | Session state |
| Monitoring | Prometheus + Evidently | Metrics, drift |
| Rate Limiting | SlowAPI | 60 req/min |

---

## 12. Business Impact Summary

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Assessment Time | 40 hours | 6.5 hours | **84%** |
| Cost per Assessment | £8,500 | £1,200 | **86%** |
| Annual Savings (15/mo) | — | £1.3M | — |
| Fine Prevention | Unknown | Up to €35M | Risk mitigation |
| Compliance Detection | Weeks | < 48 hours | Faster response |

---

## 13. Known Data Gaps (Current State)

- GDPR: 85/99 articles missing; 0/173 recitals loaded
- EU AI Act: 100/113 articles missing; only Annex III/IV partially loaded
- Cross-regulation links: 7 of ~200+ potential
- Entity enrichment data exists in `data/entities/` and `data/interpretive/` but NOT yet loaded by current `load_data.py`

> See `04_GAP_ANALYSIS_AND_IMPROVEMENTS.md` for full gap analysis and remediation plan.

---

*Merged from: `SYSTEM_ARCHITECTURE.md`, `Integration Architecture How Projects Actually Connect.md`, `PROJECT_ANALYSIS.md`, `PROJECT_STORY.md`. Originals preserved.*


---


## SOURCE: `gdpr context/main/03_KB_DESIGN_AND_CONSTRUCTION.md`

# KNOWLEDGE BASE DESIGN & CONSTRUCTION PLAN

**Merged from:** `EU_AI_KB_PROJECT_CONTEXT.md`, `KNOWLEDGE_GRAPH_PROJECT_CONTEXT.md`, `KB_construction_plan.md`
**Date:** 2026-02-12

---

## 1. Why This Knowledge Base Exists

### The Regulatory Problem

The EU has enacted two massive, interlocking legal frameworks governing AI systems:

1. **GDPR** (May 2018): 99 articles, 173 recitals, ~30 national DPAs
2. **EU AI Act** (Aug 2024, tiered enforcement through 2027): 113 articles, ~180 recitals, 13 annexes

**The compliance challenge is three-dimensional:**
- **Volume**: ~212 articles, ~353 recitals, 13 annexes, plus guidelines, case law, and enforcement precedents
- **Cross-regulation**: AI Act builds on GDPR. A single AI system triggers obligations from BOTH simultaneously
- **Interpretive depth**: Raw articles are insufficient — requires recitals, EDPB guidelines, enforcement precedents

### Why a Graph (Not Just a Document Store)

| What You Need | What Vector Search Gives | What's Missing |
|---|---|---|
| "Obligations for high-risk AI provider?" | Semantically similar chunks | Structural chain: Art 6 → Annex III → Art 9–15 → Art 43 |
| "Can we process biometric data for AI training?" | Paragraphs mentioning biometric | Cross-regulation: GDPR Art 9 prohibition + AI Act Art 10(5) narrow exception |
| "What happened to similar companies?" | Text about facial recognition | Precedent chain: Clearview AI fined €90.5M → specific GDPR violations → mapped to your system |

**The KB must be a GRAPH** — capturing relationships (containment, cross-reference, obligation, exemption, interpretation, enforcement). The vector store supplements with semantic discovery.

### What the KB Does and Does NOT Do

- **Does:** Serve as authoritative regulatory knowledge source for all agents
- **Does NOT:** Make compliance decisions (agent's job), store user data (Core 1/3), generate documents (agent layer)

---

## 2. Raw Data Inventory (89 files, 5.7 MB)

| Category | Files | Size | Delimiter | Expected Entities |
|---|---|---|---|---|
| GDPR Articles | 11 chapter files | 193 KB | `=== ARTICLE N ===` | 99 Article nodes |
| GDPR Recitals | 1 file | 153 KB | `=== RECITAL N ===` | 173 Recital nodes |
| EU AI Act Articles | 13 chapter files | 293 KB | `=== ARTICLE N ===` | 113 Article nodes |
| EU AI Act Recitals | 1 file | 225 KB | `=== RECITAL N ===` | ~180 Recital nodes |
| EU AI Act Annexes | 1 file | 46 KB | `=== ANNEX N ===` | 13 Annex nodes |
| CJEU Case Law | 20 + 1 compilation + 1 index | 191 KB | `=== CASE: C-NNN/YY ===` | 20 CaseLaw nodes |
| EDPB Guidelines | 20 + 1 compilation + 1 index | 4.3 MB | `=== GUIDELINE: ref ===` | 22 Guideline nodes |
| Enforcement Actions | 15 + 1 compilation + 1 index | 139 KB | `=== ENFORCEMENT: name ===` | 15 EnforcementAction nodes |

**Data Quality Notes:**
- Consistent delimiter pattern (`=== TYPE: ID ===`) across all categories → single base parser possible
- GDPR uses "Name:" for article titles; AI Act uses "Title:" → parser must handle both
- No explicit recital-to-article mappings → must be extracted from text
- Guidelines are massive (up to 220 KB each) → need section-level chunking

---

## 3. Knowledge Graph Schema

### 3.1 Entity Types (19 types)

```
EXISTING (14):
  Regulation, Article, Recital, Annex, Definition, Concept,
  Obligation, Right, Penalty, Authority, Actor, DataType,
  AISystemType, RiskCategory

NEW (5):
  Exemption     — Specific exemption pathways with conditions
  CaseLaw       — CJEU decisions with holdings
  Guideline     — EDPB guidelines with interpretive content
  EnforcementAction — DPA decisions with fines
  Chapter       — Chapter-level grouping within regulation
```

### 3.2 Relationship Types (25 types)

```
EXISTING (18):
  CONTAINS, PART_OF, REFERENCES, AMENDS, REPEALS,
  DEFINES, REQUIRES, PROHIBITS, PERMITS, TRIGGERS, EXEMPTS,
  APPLIES_TO, ENFORCED_BY, RESPONSIBLE_FOR,
  PROCESSES, PROTECTS, REGULATED_BY, CLASSIFIED_AS, MITIGATED_BY

NEW (7):
  INTERPRETS    — Recital/Guideline/CaseLaw → Article
  HAS_EXCEPTION — Article → Exemption (with conditions)
  COMPLEMENTS   — Cross-regulation (AI Act Art 14 ↔ GDPR Art 22)
  SUPERSEDES    — Provision overrides another
  PENALISED_BY  — Violation → EnforcementAction
  CITES         — EnforcementAction/CaseLaw → Article
```

### 3.3 Entity Property Specifications

**Article Node:**
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

**CaseLaw Node:**
```json
{
  "id": "CJEU_C_311_18",
  "type": "CaseLaw",
  "case_number": "C-311/18",
  "case_name": "Schrems II",
  "court": "CJEU (Grand Chamber)",
  "decision_date": "2020-07-16",
  "topic": "International data transfers",
  "provisions_interpreted": ["GDPR_ART_44", "GDPR_ART_45", "GDPR_ART_46"],
  "holding": "...",
  "practical_impact": ["..."],
  "ai_relevance": ["..."]
}
```

**Obligation Node:**
```json
{
  "id": "OBL_GDPR_ART35_CONDUCT_DPIA",
  "type": "Obligation",
  "obligation_type": "MUST",
  "source_article": "GDPR_ART_35",
  "source_paragraph": "1",
  "source_text": "Where a type of processing...is likely to result in a high risk...the controller shall...carry out an assessment",
  "applies_to": ["controller"],
  "conditions": ["high_risk_processing", "new_technologies"],
  "penalty_reference": "GDPR_ART_83_4_A"
}
```

**Exemption Node:**
```json
{
  "id": "EXM_GDPR_ART9_2_A",
  "type": "Exemption",
  "source_article": "GDPR_ART_9",
  "source_paragraph": "2(a)",
  "exempts_from": "OBL_GDPR_ART9_PROHIBITION",
  "condition_text": "data subject has given explicit consent...",
  "conditions": ["explicit_consent", "specified_purpose"]
}
```

---

## 4. Ontology Rationale

Every entity type exists because it answers a specific compliance question:

| Entity Type | Question It Answers |
|---|---|
| Article | "What does the law say exactly?" |
| Recital | "What did the legislator intend?" |
| Annex | "What are the specific lists/criteria?" |
| Definition | "What does this term legally mean?" |
| Obligation | "What MUST we do?" |
| Exemption | "When does a requirement NOT apply?" |
| CaseLaw | "How have courts interpreted this?" |
| Guideline | "What does the regulator's guidance say?" |
| EnforcementAction | "What happened to companies that violated?" |

---

## 5. Phase-by-Phase Construction Plan

### Phase 1: Parse Raw Text → Structured JSON (ETL)

**Script:** `core_2/scripts/parse_new_data.py`

| Parser | Input | Output | Expected Count |
|---|---|---|---|
| GDPR Articles | `gdpr_chapters/gdpr_chapter*.txt` | `gdpr_articles.json` | 99 articles |
| AI Act Articles | `ai_act_chapters/ai_act_chapter*.txt` | `eu_ai_act_articles.json` | 113 articles |
| GDPR Recitals | `gdpr_recitals/gdpr_recitals.txt` | `gdpr_recitals.json` | 173 recitals |
| AI Act Recitals | `ai_act_recitals/euai_recitals.txt` | `ai_act_recitals.json` | ~180 recitals |
| AI Act Annexes | `ai_act_annexes/ai_act_annexes.txt` | `ai_act_annexes.json` | 13 annexes |
| Case Law | `cjeu_case_law/C*_*.txt` | `case_law.json` | 20 cases |
| Guidelines | `edpb_guidelines/GL_*.txt` | `edpb_guidelines.json` | 22 guidelines |
| Enforcement | `enforcement_actions/*.txt` | `enforcement_actions.json` | 15 actions |

**Validation:** Count verification, Pydantic schema validation, spot-check 5 articles per regulation.

### Phase 2: Build Structural Knowledge Graph (Neo4j)

**Script:** `core_2/scripts/load_knowledge_graph.py`

1. Create Regulation nodes (2)
2. Create Chapter nodes (24) — `Regulation -[:CONTAINS]-> Chapter`
3. Create Article nodes (~212) — `Chapter -[:CONTAINS]-> Article`
4. Create Recital nodes (~353) — `Regulation -[:CONTAINS]-> Recital`
5. Create Annex nodes (13)
6. Create CaseLaw (20), Guideline (22), EnforcementAction (15) nodes
7. Build structural relationships:
   - Article cross-references: `Article -[:REFERENCES]-> Article` (~700 edges)
   - Recital-Article links: `Recital -[:INTERPRETS]-> Article`
   - CaseLaw/Guideline → Article: `CaseLaw -[:CITES]-> Article`
   - EnforcementAction → Article: `EnforcementAction -[:CITES]-> Article`

**Validation:** Node counts match, every Article has PART_OF → Chapter, spot-check 10 cross-references.

### Phase 3: Semantic Entity & Relationship Extraction

**Script:** `core_2/scripts/extract_semantic_entities.py`

| Extraction | Method | Expected Output |
|---|---|---|
| Definitions | Rule-based (Art 4 GDPR, Art 3 AI Act) | ~94 Definition nodes |
| Obligations | LLM-assisted: "shall"/"must"/"may" → structured | ~800–1,200 Obligation nodes |
| Exemptions | LLM-assisted: "does not apply where" patterns | ~100–200 Exemption nodes |
| Concepts | Rule-based + LLM | ~150–250 Concept nodes |
| Actors | Rule-based from definitions | ~20 Actor nodes |
| DataType hierarchy | Rule-based from Art 4/9 | ~25 DataType nodes |
| AISystemType + RiskCategory | Rule-based from Annex III + Art 5 | ~40 nodes |
| Penalties | Rule-based from Art 83/Art 99 | ~10 Penalty nodes |
| Cross-regulation links | LLM-assisted + human review | ~30–50 edges |

**Key DataType Hierarchy:**
```
DataType
├── PersonalData
│   ├── SpecialCategoryData (BiometricData, HealthData, GeneticData, ...)
│   └── RegularPersonalData (ContactData, LocationData, BehavioralData, ...)
└── NonPersonalData (AnonymisedData, AggregatedData, PseudonymisedData)
```

**Key RiskCategory Hierarchy:**
```
RiskCategory
├── PROHIBITED (Art 5): SubliminalManipulation, SocialScoring, RealTimeBiometricPublic, ...
├── HIGH_RISK (Annex III): BiometricID, CriticalInfra, Education, Employment, ...
├── LIMITED_RISK (Art 50): Chatbots, EmotionRecognition, Deepfakes, ...
└── MINIMAL_RISK: Everything else
```

**LLM Obligation Extraction Prompt:**
```
Analyze this article text and extract ALL obligations:
- obligation_type: MUST | MUST_NOT | SHOULD | MAY
- who: [actor(s)]
- what: [action]
- conditions: [when applies]
- source_quote: [exact text]
- paragraph: [which paragraph]
```

**Validation:** Every Obligation has verifiable `source_text`; every Definition links to source paragraph; cross-regulation links have rationale.

### Phase 4: Build Vector Store (ChromaDB)

**Script:** `core_2/scripts/build_vector_store.py`

| Entity Type | Chunking Strategy | Est. Chunks |
|---|---|---|
| Articles | One chunk per paragraph | ~1,500 |
| Recitals | One chunk per recital | ~353 |
| Annexes | One chunk per section | ~150 |
| Case Law | Separate: facts, holding, impact, AI relevance | ~100 |
| Guidelines | One chunk per section heading | ~400 |
| Enforcement | Separate: facts, findings, measures | ~60 |
| Definitions | One per definition | ~94 |
| Obligations | One per obligation source_text | ~800–1,200 |
| Concepts | One per concept description | ~200 |
| **Total** | | **~3,100–4,100** |

**Metadata per chunk:**
```json
{
  "entity_id": "GDPR_ART_35", "entity_type": "Article",
  "regulation": "GDPR", "chapter": "Chapter 4",
  "article_number": "35", "paragraph": "1",
  "modality": "MUST", "actors": ["controller"],
  "risk_relevance": "HIGH"
}
```

**Collection structure (5 collections):**
| Collection | Content | Purpose |
|---|---|---|
| `articles` | Article paragraphs | Primary legal text search |
| `obligations` | Extracted obligations | "What must I do?" |
| `interpretive` | Recitals + Guidelines + Case law | "What does this mean?" |
| `enforcement` | Enforcement actions | "What happened to others?" |
| `definitions` | Legal definitions | Term lookup |

### Phase 5: Cross-Link and Validate (Integrity)

- Bidirectional consistency: every Neo4j entity ↔ ChromaDB chunk
- Golden query test suite (6+ critical scenarios)
- Relationship density: avg ≥ 4 relationships per Article
- Coverage reports: which articles have 0 obligations extracted

### Phase 6: Application Layer — SystemProfile Matching

**SystemProfile schema** (standard intermediate representation):
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

**SystemProfile → KG anchor mapping:**

| Field | Maps To | Relationship |
|---|---|---|
| `data_types_processed` | DataType nodes | → REGULATED_BY → Article |
| `capabilities` | AISystemType nodes | → CLASSIFIED_AS → RiskCategory |
| `deployment_context` | Annex III categories | → maps to HIGH_RISK |
| `operator_role` | Actor nodes | → RESPONSIBLE_FOR → Obligation |

---

## 6. Reusability Assessment of Existing core_2 Code

| Component | Decision | Rationale |
|---|---|---|
| Config pattern | BORROW | Good Pydantic pattern, new settings |
| Schema (Pydantic) | REWRITE | Need 60% more entity types and fields |
| Graph store (Neo4j) | PARTIAL | Connection good; `_record_to_entity()` bug drops subclass fields |
| Vector store (Chroma) | PARTIAL | Connection good; `_entity_to_text()` creates poor embeddings |
| Retrieval engine (RRF) | BORROW | Algorithm correct, needs richer metadata |
| Reasoning engine | BORROW | Pattern correct, needs domain prompts |
| Extraction pipeline | REBUILD | Wrong approach (regex on delimited data) |
| Data loading | REBUILD | Wrong data format, wrong scale |
| API layer | DEFER | Build KB first, API later |

**Recommendation:** Build standalone, then replace core_2's data layer.

---

## 7. Estimated Entity & Relationship Counts

| Category | Count |
|---|---|
| Regulation nodes | 2 |
| Chapter nodes | 24 |
| Article nodes | ~212 |
| Recital nodes | ~353 |
| Annex nodes | 13 |
| Definition nodes | ~94 |
| Concept nodes | ~200 |
| Obligation nodes | ~1,000 |
| Exemption nodes | ~150 |
| Right / Penalty / Actor / DataType / AISystemType / RiskCategory | ~120 |
| CaseLaw / Guideline / EnforcementAction | 57 |
| **TOTAL NODES** | **~2,225** |
| | |
| Structural relationships | ~650 |
| Cross-reference relationships | ~700 |
| Semantic relationships | ~1,500 |
| Actor / Data / Risk relationships | ~500 |
| Interpretive / Cross-regulation | ~350 |
| **TOTAL RELATIONSHIPS** | **~3,700** |
| **Vector store chunks** | **~3,500** |

---

## 8. Standalone Project Directory Structure

```
eu_ai_knowledge_base/
├── raw_data/                       # Copy of New_Data/ (read-only source)
├── parsed_data/
│   ├── legal/                      # Articles, recitals, annexes JSON
│   ├── interpretive/               # Case law, guidelines, enforcement JSON
│   └── entities/                   # Definitions, obligations, exemptions, etc.
├── src/
│   ├── config.py
│   ├── schema/                     # Pydantic models (19 entity types, 25 rels)
│   ├── parsers/                    # One parser per data type
│   ├── extractors/                 # LLM-assisted semantic extraction
│   ├── stores/                     # Neo4j + ChromaDB
│   ├── retrieval/                  # Hybrid engine + reasoning
│   └── validation/                 # Golden queries + coverage
├── scripts/
│   ├── 01_parse_raw_data.py
│   ├── 02_load_structural_kg.py
│   ├── 03_extract_semantic.py
│   ├── 04_build_vector_store.py
│   ├── 05_validate.py
│   └── run_all.py
├── golden_tests/
│   └── test_queries.json
└── tests/
```

**Dependencies:** pydantic, neo4j, chromadb, google-generativeai, structlog, tenacity, rich
**No FastAPI, LangChain, or LangGraph** — pure data engineering project.

---

## 9. Execution Timeline & Risk Mitigation

| Phase | Effort | Notes |
|---|---|---|
| Phase 1: Parsing | 2–3 days | Rule-based, well-structured input |
| Phase 2: Structural KG | 1–2 days | Straightforward loading |
| Phase 3: Semantic extraction | 5–7 days | LLM-assisted, requires validation |
| Phase 4: Vector store | 1–2 days | Chunking + embedding |
| Phase 5: Validation | 2–3 days | Golden queries, coverage |
| Phase 6: SystemProfile | 3–4 days | New input layer |
| **Total** | **~14–21 days** | |

| Risk | Mitigation |
|---|---|
| LLM hallucination in extraction | Every obligation has verifiable `source_text` |
| Missing cross-references | Rule-based first, LLM only for implicit |
| Large guidelines (220KB) | Metadata+sections in graph, full text in vector only |
| Definition conflicts between regulations | Surface both, mark with `regulation_id` |
| Irregular annex structure | Custom parser per annex format |

---

## 10. Query Interface Contract

### Primary Query Patterns

| Pattern | Input | Method |
|---|---|---|
| Anchor → Traverse → Collect | "Obligations for HIGH_RISK AI?" | Graph traversal |
| DataType → Regulation → Requirements | "We process biometric data" | Graph + exemptions |
| System → Risk Classification | "Facial recognition for attendance" | Graph: capability → Annex III → risk |
| Cross-Regulation | "GDPR requirements overlapping AI Act?" | COMPLEMENTS edges |
| Penalty Lookup | "Max fine for prohibited AI?" | Graph: Art 5 → Art 99 |
| Precedent Research | "Fined for similar system?" | Enforcement reverse CITES |
| Semantic + Graph Expansion | Free-text query | Hybrid RRF |

### Consumers

| Consumer | What It Queries | What It Expects |
|---|---|---|
| Risk Classifier Agent | System capabilities | (AISystemType, RiskCategory, source Article) tuples |
| Legal Research Agent | Legal query | Answer + cited entities |
| Compliance Checker Agent | (system_profile, obligations) | Gap analysis (MET/UNMET/PARTIAL) |
| Document Generator Agent | Obligation set | Organized obligations + citations for DPIA/ROPA |

---

## 11. Why Not Other Storage Options?

| Considered | Decision | Why |
|---|---|---|
| PostgreSQL for entities | NO | Entities ARE graph nodes; duplicating adds sync complexity |
| Elasticsearch | NO | ChromaDB handles semantic search; don't need full-text |
| Second graph DB | NO | Neo4j is correct for legal knowledge |
| MongoDB | NO | JSON files + Neo4j sufficient |
| Redis caching | MAYBE LATER | Could cache frequent traversals |

**Two-store architecture (Neo4j + ChromaDB) is the correct design.** Graph answers "what's connected?", vectors answer "what's similar?"

---

*Merged from: `EU_AI_KB_PROJECT_CONTEXT.md`, `KNOWLEDGE_GRAPH_PROJECT_CONTEXT.md`, `KB_construction_plan.md`. Originals preserved.*


---


## SOURCE: `gdpr context/main/04_GAP_ANALYSIS_AND_IMPROVEMENTS.md`

# GAP ANALYSIS, IMPROVEMENTS & DATA ENHANCEMENT

**Merged from:** `CRITICAL_GAP_ANALYSIS.md`, `knowledge_graph_gap_analysis.md`, `DATA_ENHANCEMENT_SUMMARY.md`, `improve_v1.md`, `MERGED_GAP_ANALYSIS.md`
**Date:** 2026-02-12

---

## 1. Executive Summary

- **Current maturity:** ~20% production-ready; ~12% article coverage
- **Risk Level:** HIGH — KB insufficient for reliable compliance automation
- **Critical Gaps:** 12 identified areas; multi-hop reasoning fails in ~88% of scenarios
- **Remediation Timeline:** 6–8 weeks core; 6–12 weeks full enrichment
- **Enhancements completed so far:** 500+ entities indexed, 85+ cross-regulation links, 40+ interpretive docs

---

## 2. Consolidated Coverage Metrics

### Before Enhancements

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| GDPR Articles | 14/99 (14%) | 99 | 85 missing |
| GDPR Recitals | 0/173 | 173 | 173 missing (100%) |
| EU AI Act Articles | 11/113 (10%) | 113 | 102 missing |
| EU AI Act Annexes | 2 partial | 13 | 11 missing |
| Definitions (GDPR Art 4) | ~6/26 | 26 | 20+ missing |
| Definitions (AI Act Art 3) | ~7/68 | 68 | 61 missing |
| Cross-Regulation Links | 7 | 200+ | 193+ missing |
| EDPB Guidelines | 0 | 30+ | 30+ missing |
| Case Law | 0 | 50+ | 50+ missing |
| Enforcement Actions | 0 | 100+ | 100+ missing |
| Relationships | ~50 | 5,000+ | ~99% gap |

### After Enhancements (indexed, not all loaded into KG)

| Metric | Count |
|--------|-------|
| GDPR Articles indexed | 99 |
| EU AI Act Articles indexed | 113 |
| Definitions indexed | 94+ |
| Cross-Regulation Links | 85+ |
| Interpretive Documents | 40+ |
| Concepts/Principles | 34+ |
| Obligations | 40+ |
| Rights | 17+ |
| Authorities | 20+ |
| Case Law | 11 |
| Enforcement Actions | 15 |
| **Total Entities** | **500+** |

---

## 3. Detailed GDPR Gap Analysis

### Missing Articles (85 of 99)

**Chapter II — Principles (Arts 5–11):** Missing Art 7 (consent conditions), Art 8 (child consent), Art 10 (criminal convictions), Art 11

**Chapter III — Data Subject Rights (Arts 12–23):** Missing Art 12 (transparent info), Art 15 (access), Art 16 (rectification), Art 18 (restriction), Art 19 (notification), Art 20 (portability), Art 21 (object), Art 23 (restrictions)

**Chapter IV — Controller/Processor (Arts 24–43):** Missing Art 24 (responsibility), Art 26–29, Art 31–34 (breach notification), Art 36–43 (DPO, codes, certification)

**Chapter V — International Transfers (Arts 44–50):** All missing — critical for cloud AI

**Chapters VI–XI (Arts 51–99):** Supervisory authorities, cooperation, remedies, penalties — all missing. Art 83 (administrative fines) and Art 84 (penalties) are critical.

### Missing Recitals (173 of 173)

Key missing recitals:
- Recitals 32–43: Consent requirements (critical for AI)
- Recitals 63–73: Data subject rights context
- Recital 71: Profiling interpretation (critical for AI)
- Recitals 75–77: Risk assessment
- Recitals 84–94: Security and breaches
- Recitals 148–152: Administrative fines

---

## 4. Detailed EU AI Act Gap Analysis

### Missing Articles (102 of 113)

**Title III — High-Risk (Arts 6–51):** Missing Art 4 (AI literacy), Art 7, Art 8, Art 15–27 (accuracy, provider obligations, quality management, conformity assessment, deployer obligations, FRIA), Art 28–50

**Title IV — GPAI Models (Arts 51–56):** All missing — critical for LLM compliance

**Titles V–XII (Arts 57–113):** All missing — governance, enforcement, final provisions

### Missing Annexes (11 of 13)

| Annex | Status | Criticality |
|---|---|---|
| III (High-Risk Systems) | PARTIAL | **CRITICAL** — core classification list |
| IV (Technical Documentation) | PARTIAL | HIGH |
| I, II, V–X | MISSING | MEDIUM–HIGH |
| XI–XIII (GPAI docs, transparency, systemic risk) | MISSING | **CRITICAL** for LLM compliance |

---

## 5. The 12 Gap Areas (from knowledge_graph_gap_analysis.md)

| # | Gap | Current State | Impact |
|---|---|---|---|
| 1 | Incomplete Article Coverage | 25/212 articles (12%) | Cannot answer 88% of queries |
| 2 | Missing Recitals | 0/261 | No interpretive context |
| 3 | Missing Annexes | 0/13 | Cannot classify high-risk systems |
| 4 | Sparse Relationship Density | ~50 vs 5,000+ needed | Multi-hop reasoning fails |
| 5 | Missing Temporal/Deadlines | 0 modeled | Cannot answer "when must we comply?" |
| 6 | Missing Exemption Networks | 0 modeled | False positives, over-flagging |
| 7 | Missing Procedural Knowledge | 0 workflows | Cannot say HOW to comply |
| 8 | Missing Evidence/Proof Requirements | Not captured | Cannot generate checklists |
| 9 | Missing Regulatory Guidance | 0 EDPB guidelines integrated | Technically correct but practically wrong |
| 10 | Missing Case Law | 0 CJEU cases integrated | No precedent citation |
| 11 | Missing Synonym/Terminology Mapping | 0 synonym clusters | 60%+ query failure from vocabulary mismatch |
| 12 | Missing Validation Framework | 0 golden queries | Unknown accuracy — system untrustworthy |

---

## 6. Architectural Gaps (from improve_v1.md)

### GAP A: Articles Treated as Atomic Units

Currently: one Article = one embedding = one reasoning node. Breaks for exceptions, conditions, multi-clause articles (Art 6, Art 9, Art 22).

**Fix:** Paragraph-level nodes with sub-item granularity.

### GAP B: Conditions & Exceptions Are Implicit, Not First-Class

Conditions stored as flat lists, not as navigable graph entities with conditional logic.

**Fix:** Exemption nodes with `HAS_EXCEPTION` relationships and conditional properties.

### GAP C: No Negative Knowledge

System doesn't know when requirements DON'T apply (e.g., research exemptions, SME carve-outs, personal/household activity).

**Fix:** Model exemptions and exclusions as explicit graph paths.

### GAP D: Missing Procedural / How-To Workflows

Static rules only — no decision trees or step-by-step compliance procedures.

**Fix:** Workflow nodes (DPIA procedure, conformity assessment steps, risk classification decision tree).

---

## 7. Multi-Hop Failure Scenarios

**Query: "Facial recognition for employee attendance requirements"**
```
Required: GDPR Art 9 → AI Act Art 5 → Annex III.1 → Art 14 → Art 35 → Art 27 → EDPB guidelines
Fails at: Art 27, Art 43 details, EDPB guidelines, national opinions
```

**Query: "Penalties for processing children's data for AI training"**
```
Required: GDPR Art 8 → Art 7 → Art 9 → Art 83 → AI Act Art 10 → Art 99 → EDPB guidelines
Fails at: Art 7, Art 8, Art 83, Art 99, guidelines, precedents
```

**Query: "Document compliance for credit scoring AI"**
```
Required: Annex III.5 → Art 6 → Art 11 → Annex IV → Art 12 → Art 9 → GDPR Art 35 → Art 30
Fails at: Annex IV details, Art 12 details, standards mapping
```

**Query: "Does facial recognition for employee attendance require DPIA?"**
```
Required path (8 relationships):
  FacialRecognition → BiometricData → SpecialCategory → GDPR_ART_9
  EmployeeAttendance → Employment → AI_ACT_ANNEX_III_4 → HighRisk
  BiometricData + HighRisk → GDPR_ART_35_DPIA
Current state: 0 of these 8 relationships exist
```

---

## 8. Cross-Regulation Mappings Required

| GDPR | Relationship | AI Act | Rationale |
|---|---|---|---|
| Art 5 (principles) | COMPLEMENTS | Art 10 (data governance) | AI data must follow GDPR principles |
| Art 9 (special categories) | COMPLEMENTS | Art 10(5) (bias detection) | Narrow exception for bias |
| Art 22 (automated decisions) | COMPLEMENTS | Art 14 (human oversight) | Both require human involvement |
| Art 25 (privacy by design) | COMPLEMENTS | Art 9 (risk management) | Both mandate built-in safeguards |
| Art 35 (DPIA) | COMPLEMENTS | Art 6+27 (risk + FRIA) | High-risk AI triggers DPIA |
| Art 13–14 (transparency) | COMPLEMENTS | Art 13+50 (transparency) | Both mandate informing individuals |
| Art 83 (fines) | CUMULATIVE_WITH | Art 99 (penalties) | Penalties stack |

### Actor Mappings

| GDPR Actor | AI Act Actor | Relationship |
|---|---|---|
| Controller | Provider/Deployer | MAY_BE |
| Processor | Provider | MAY_BE |
| Data Subject | Affected Person | EQUIVALENT |
| DPA | AI Office | COORDINATES_WITH |
| EDPB | AI Board | COORDINATES_WITH |

---

## 9. Required Schema Enhancements

### New Entity Types Needed
- Procedure, Safeguard, Exemption, Derogation
- Deadline, TransitionPeriod
- Guidance, CaseLaw, EnforcementAction, Opinion
- Standard, Benchmark, Metric
- Template, Record, Register
- Role, Body

### New Relationship Types Needed
- INTERPRETS, CLARIFIES, HARMONIZES_WITH, OVERRIDES
- PRECEDES, FOLLOWS, SUPERSEDES, EFFECTIVE_FROM
- CONDITIONAL_ON, ALTERNATIVE_TO, CUMULATIVE_WITH
- SATISFIED_BY, EVIDENCED_BY, DOCUMENTED_IN
- NOTIFIES, SUPERVISES, COORDINATES_WITH

---

## 10. Interpretive Content Required

### EDPB Guidelines (30+)

| Guideline | Topic | Impact |
|---|---|---|
| WP29 Guidelines on consent | Consent requirements | CRITICAL |
| WP29 Guidelines on profiling | Art 22 interpretation | CRITICAL |
| WP29 Guidelines on transparency | Art 12–14 | CRITICAL |
| EDPB Guidelines 05/2020 | Consent | CRITICAL |
| EDPB Guidelines 07/2020 | Controller/processor | CRITICAL |
| EDPB Guidelines 01/2022 | Data breach notification | CRITICAL |

### Case Law (50+)

| Case | Topic | Significance |
|---|---|---|
| C-311/18 Schrems II | International transfers | CRITICAL |
| C-131/12 Google Spain | Right to be forgotten | CRITICAL |
| C-673/17 Planet49 | Consent cookies | CRITICAL |
| C-645/19 Facebook | Sensitive data profiling | CRITICAL |

### Enforcement Actions (100+)

| Authority | Company | Amount | Topic |
|---|---|---|---|
| DPC | Meta | €1.2B | International transfers |
| Italian DPA | Clearview AI | €20M | Biometric data |
| CNIL | Google | €150M | Cookie consent |
| DPC | Meta | €405M | Children's data |

### Technical Standards

| Standard | Topic | Relevance |
|---|---|---|
| ISO 42001 | AI management systems | CRITICAL |
| ISO 27001 | Information security | CRITICAL |
| ISO 27701 | Privacy management | CRITICAL |
| ISO 23894 | AI risk management | CRITICAL |

---

## 11. Temporal & Deadline Information

EU AI Act phased implementation:

| Deadline | Requirement |
|---|---|
| Feb 2, 2025 | Prohibited AI systems ban takes effect |
| Aug 2, 2025 | Governance structure requirements |
| Aug 2, 2026 | General-purpose AI obligations |
| Aug 2, 2027 | High-risk AI system requirements (MAIN) |

---

## 12. Embedding & Vector Strategy Enhancements

1. **Hierarchical embeddings:** Regulation → Chapter → Article → Paragraph
2. **Relationship-aware embeddings:** Include path context for common traversals
3. **Multi-modal embeddings:** Legal precision text + simplified explanation + Q/A probes
4. **Cross-reference embeddings:** GDPR ↔ AI Act joint, Article ↔ Recital paired
5. **Search prefixes:** `"EU regulation article: ..."`, `"Legal case holding: ..."`, `"Compliance requirement: ..."`

---

## 13. Completed Enhancements (from DATA_ENHANCEMENT_SUMMARY.md)

### Files Created
- Enhanced schema: `core_2/src/graph/schema_enhanced.py` (25 entity types, 35+ relationships)
- Regulation structures: `core_2/data/legal/gdpr_structure.json`, `eu_ai_act_structure.json`
- Entity data: concepts, obligations, rights, authorities, penalties, cross-regulation mappings
- Interpretive content: EDPB guidelines, case law, enforcement actions
- Data loader: `core_2/scripts/load_complete_data.py`

### Multi-Hop Paths Now Supported (indexed)
- Facial recognition: GDPR Art 9 → AI Act Art 5 → Annex III.1 → Art 14 → Art 35 → Art 27
- Combined penalties: AI Act Art 99 → GDPR Art 83 → cumulative → precedent
- LLM compliance: Art 3 → Art 51 → Art 53 → Annex XI → EDPB guidance → enforcement

---

## 14. Consolidated Remediation Plan

### Phase 1 — Core Extraction (Week 1)
- Automated ingestion from EUR-Lex (GDPR + AI Act full text)
- Parse to paragraph-level JSON with checksums
- **Success:** 100% article coverage (212/212)

### Phase 2 — Structure & Linking (Week 1–2)
- Load all articles, recitals, annexes, definitions into Neo4j
- Create structural relationships (CONTAINS, PART_OF, REFERENCES)
- Link recitals → articles; case law/guidelines → articles

### Phase 3 — Semantic Enrichment (Week 2–4)
- LLM-assisted obligation, exemption, concept extraction
- Human review for confidence < 0.9
- Build cross-regulation COMPLEMENTS edges

### Phase 4 — Interpretive & Evidence Layer (Week 3–6)
- Ingest all EDPB guidelines, case law, enforcement actions
- Map to articles/obligations; add precedent nodes
- Add standards mapping (ISO 42001, 27001)

### Phase 5 — Temporal, Exemptions & Workflows (Week 5–7)
- Model all compliance deadlines and transitional provisions
- Build exemption networks (SME, research, national security)
- Create decision trees and procedural workflows (DPIA, conformity assessment)

### Phase 6 — Validation, Embeddings & QA (Week 6–8)
- 150+ golden test queries with expert-verified answers
- Hierarchical + relationship-aware embeddings
- Daily regression tests; accuracy target ≥95%
- Synonym mapping for business → legal term translation

---

## 15. Target Graph Statistics

| Metric | Current | Target | Multiplier |
|---|---|---|---|
| Total Nodes | ~40 | 2,500+ | 62× |
| Total Relationships | ~50 | 5,000–15,000+ | 100–300× |
| Relationship Types | 18 | 35+ | 2× |
| Entity Types | 14 | 25+ | 1.8× |
| Avg Relationships/Node | 1.0 | 6.0 | 6× |
| Max Traversal Depth | 2 | 6 | 3× |
| Cross-Regulation Links | 7 | 500+ | 71× |

---

## 16. Immediate Action Items

### Critical (Must Have for MVP)
1. Complete all GDPR articles (99) + recitals (key 50+) — **CRITICAL**
2. Complete all EU AI Act articles (113) + annexes (13, prioritise III) — **CRITICAL**
3. Extract and normalise all definitions (94+) — **CRITICAL**
4. Build obligation extraction pipeline — **CRITICAL**
5. Create cross-regulation mappings (200+ links) — **CRITICAL**

### High Priority (Production Readiness)
6. Add EDPB guidelines (top 20) + CJEU case law (top 30) — HIGH
7. Add major enforcement actions (top 50) — HIGH
8. Implement new entity & relationship types in schema — HIGH
9. Build golden test suite (150+ queries) — HIGH

### Medium Priority (Full Coverage)
10. Add temporal/deadline model with known dates — MEDIUM
11. Build exemption networks and procedural workflows — MEDIUM
12. Add synonym mapping (500+ clusters) — MEDIUM
13. Add ISO standard mappings and compliance checklists — MEDIUM

---

## 17. Success Criteria

| Metric | Target |
|---|---|
| Article coverage | 212/212 (100%) |
| Recital coverage | 261+ loaded |
| Validated relationships | 5,000+ |
| Golden query accuracy | ≥95% |
| Multi-hop success rate | ≥85% correct reasoning chains |
| Retrieval precision | ≥90% relevant in top 5 |
| False positive rate | <5% |
| Query response time | <3 seconds |

---

## 18. Conclusion

The knowledge base is currently unsuited for production-grade multi-agent compliance automation. The merged analysis identifies 12 concrete gap areas, 4 architectural weaknesses, and a clear 6–8 week remediation roadmap. Prioritise Annex III, GDPR recitals, high-risk articles, obligation extraction, and cross-regulation relationships to unlock downstream reasoning.

**Without these enhancements, the system provides incomplete, potentially incorrect, and legally risky compliance guidance.**

---

*Merged from: `CRITICAL_GAP_ANALYSIS.md`, `knowledge_graph_gap_analysis.md`, `DATA_ENHANCEMENT_SUMMARY.md`, `improve_v1.md`, `MERGED_GAP_ANALYSIS.md`. Originals preserved.*


---


---

# Run: gdpr context/backup

---


## SOURCE: `gdpr context/backup/PROJECT_STORY.md`

# EU AI Regulatory Compliance Engine - Component Story

> **A narrative journey through the system's architecture, explaining how each component connects and contributes to automated EU AI Act & GDPR compliance**

---

## 🎭 The Story: A Day in the Life of a Compliance Assessment

### Prologue: The Challenge

Imagine you're a compliance officer at **TechCorp**, a company deploying a facial recognition system for employee attendance. You need to ensure it complies with the **EU AI Act** and **GDPR**—a process that traditionally takes **40 hours** and costs **£8,500** per assessment.

Enter the **EU AI Regulatory Compliance Engine**—a multi-agent AI system that transforms this into a **6.5-hour automated journey**.

---

## 🏗️ The Three Kingdoms: Core Modules

```mermaid
graph TB
    User((User)) --> Core3[🎭 Core 3: The Orchestrator<br/>Port 8000]
    Core3 --> Core2[📚 Core 2: The Knowledge Keeper<br/>Port 8001]
    Core3 --> Core1[👁️ Core 1: The Watchdog<br/>Port 8002]
    
    subgraph "The Orchestrator Kingdom"
        direction TB
        Supervisor[🎯 Supervisor Agent]
        Risk[⚠️ Risk Classifier]
        Tech[🔧 Technical Assessor]
        Legal[⚖️ Legal Research Agent]
        Doc[📄 Documentation Generator]
    end
    
    subgraph "The Knowledge Kingdom"
        direction TB
        Neo4j[(🕸️ Neo4j Graph)]
        Chroma[(🔍 ChromaDB Vectors)]
        Reasoning[🧠 Multi-Hop Reasoner]
    end
    
    subgraph "The Watchdog Kingdom"
        direction TB
        Art14[📋 Article 14 Monitor]
        Drift[📊 Drift Detector]
        Bias[⚖️ Bias Detector]
        Metrics[📈 Prometheus Metrics]
    end
```

---

## 🌅 Chapter 1: The Request Arrives (Core 3 - The Orchestrator)

### Scene: The Entry Point

**Location**: [main.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/api/main.py) - Port 8000

The user submits a request:

```json
{
  "system_description": "Facial recognition for employee attendance tracking",
  "system_type": "facial_recognition",
  "deployment_context": "employee_monitoring",
  "company_name": "TechCorp"
}
```

**The Supervisor Agent awakens.**

---

### Component 1: 🎯 The Supervisor Agent

**File**: [supervisor.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/agents/supervisor.py)

> *"I am the conductor of this orchestra. Every agent reports to me, and I weave their findings into a coherent compliance assessment."*

#### Role in the Story:
The Supervisor is the **brain** of the operation. Built with **LangGraph**, it orchestrates a workflow that:

1. **Receives** the compliance request
2. **Decomposes** it into sub-tasks
3. **Routes** work to specialist agents
4. **Detects conflicts** between agent outputs
5. **Synthesizes** the final compliance report

#### Key Methods:
| Method | Purpose |
|--------|---------|
| `_build_workflow()` | Constructs the LangGraph state machine |
| `_classify_risk()` | Triggers risk classification |
| `_check_conflicts()` | Ensures agents agree on findings |
| `_synthesize_report()` | Creates executive summary |

#### The LangGraph Workflow:
```mermaid
stateDiagram-v2
    [*] --> RiskClassification
    RiskClassification --> HumanReview: HIGH_RISK/PROHIBITED
    RiskClassification --> GDPRAssessment: LIMITED/MINIMAL
    HumanReview --> AwaitApproval
    AwaitApproval --> GDPRAssessment: Approved
    GDPRAssessment --> LegalResearch
    LegalResearch --> ConflictCheck
    ConflictCheck --> DocumentGeneration
    DocumentGeneration --> SynthesizeReport
    SynthesizeReport --> [*]
```

---

### Component 2: ⚠️ The Risk Classifier Agent

**File**: [risk_classifier.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/agents/risk_classifier.py)

> *"My job is to categorize every AI system according to the EU AI Act's four risk tiers. I am the first line of defense."*

#### Role in the Story:
When TechCorp's facial recognition request arrives, the Risk Classifier:

1. **Extracts capabilities** using Google Gemini LLM
2. **Checks Article 5** for prohibited practices (social scoring, real-time biometric ID)
3. **Checks Annex III** for high-risk categories (biometrics, employment, law enforcement)
4. **Determines transparency** requirements for user-facing systems

#### Risk Categories:
| Category | Description | EU AI Act Reference |
|----------|-------------|---------------------|
| **PROHIBITED** | Cannot be deployed in EU | Article 5 |
| **HIGH_RISK** | Requires conformity assessment | Annex III |
| **LIMITED_RISK** | Requires transparency notice | Article 52 |
| **MINIMAL_RISK** | Voluntary compliance | - |

#### For TechCorp's System:
```
INPUT: "Facial recognition for employee attendance"
OUTPUT: HIGH_RISK (Annex III, Category 4: Employment)
CONFIDENCE: 92%
```

---

### Component 3: 🔧 The Technical Assessor Agent

**File**: [technical_assessor.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/agents/technical_assessor.py)

> *"I audit every byte of data flow. If you're violating GDPR, I will find it."*

#### Role in the Story:
The Technical Assessor performs a **GDPR compliance audit** by checking:

| Article | Requirement | What It Checks |
|---------|-------------|----------------|
| **Art. 5(1)(c)** | Data Minimization | Is only necessary data collected? |
| **Art. 6** | Lawful Basis | Is there legal grounds for processing? |
| **Art. 9** | Special Category Data | Is biometric data involved? |
| **Art. 13** | Transparency | Are users informed? |
| **Art. 17** | Right to Erasure | Can users delete their data? |
| **Art. 22** | Automated Decision-Making | Are decisions explained? |
| **Art. 25** | Privacy by Design | Is privacy built-in? |
| **Art. 35** | DPIA Required? | Does this need an impact assessment? |

#### For TechCorp's System:
```
VIOLATIONS FOUND:
- Art. 9: Biometric data without explicit consent
- Art. 35: DPIA required but not conducted

WARNINGS:
- Art. 17: Data retention policy unclear
```

---

### Component 4: ⚖️ The Legal Research Agent

**File**: [legal_research.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/agents/legal_research.py)

> *"I traverse the vast knowledge graph of EU regulations. Need a citation? I'll find the path from your system to the exact article that applies."*

#### Role in the Story:
This agent **connects to Core 2** to perform multi-hop legal reasoning. It:

1. **Extracts legal entities** from the risk classification and GDPR audit
2. **Queries the GraphRAG API** for relevant articles
3. **Performs vector search** for supporting text
4. **Returns legal citations** with relationship chains

#### For TechCorp's System:
```
QUERY: "Does facial recognition for employees require DPIA?"

REASONING CHAIN:
facial_recognition → BIOMETRIC_DATA → GDPR_Art_9 → SPECIAL_CATEGORY
                  → EMPLOYMENT_CONTEXT → EU_AI_ACT_Annex_III
                  → HIGH_RISK → REQUIRES_DPIA

ANSWER: YES
CITATIONS: [GDPR Art 35(3)(b), EU AI Act Art 6, Art 14]
```

---

### Component 5: 📄 The Documentation Generator Agent

**File**: [documentation_generator.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_3/src/agents/documentation_generator.py)

> *"From chaos, I create order. Every compliance document you need—DPIA, ROPA, Conformity Assessment—I generate them all."*

#### Role in the Story:
Based on the Risk Classifier and Technical Assessor findings, this agent generates:

| Document | Trigger | Purpose |
|----------|---------|---------|
| **DPIA** | High-risk processing | Impact assessment under GDPR Art 35 |
| **ROPA** | Any processing | Record of processing activities (Art 30) |
| **Conformity Assessment** | HIGH_RISK classification | EU AI Act compliance proof |
| **Transparency Notice** | User-facing AI | AI disclosure under Art 52 |

#### For TechCorp's System:
```
DOCUMENTS GENERATED:
1. DPIA (38 pages)
2. ROPA Entry
3. Conformity Assessment (EU AI Act Annex IV)
4. Transparency Notice for Employees
```

---

## 📚 Chapter 2: The Knowledge Search (Core 2 - The Knowledge Keeper)

### Scene: The GraphRAG Engine

**Location**: Port 8001

When the Legal Research Agent asks "Does facial recognition require a DPIA?", Core 2 springs into action.

---

### Component 6: 🕸️ Neo4j Graph Store

**File**: [graph_store.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_2/src/stores/graph_store.py)

> *"I am the web of legal knowledge. Every article, every regulation, every relationship—connected in a vast graph."*

#### Role in the Story:
The Neo4j graph contains:

| Entity Type | Count | Examples |
|-------------|-------|----------|
| **REGULATION** | 2 | GDPR, EU AI Act |
| **ARTICLE** | 25 | Art. 5, Art. 35, Art. 14 |
| **CONCEPT** | 50+ | Biometric Data, High-Risk, DPIA |
| **REQUIREMENT** | 30+ | Consent, Transparency, Human Oversight |

#### Legal Data Coverage:
| Regulation | Articles Indexed | Key Content |
|------------|------------------|-------------|
| **GDPR** | 14 articles | Art 1-6, 9, 13, 14, 17, 22, 25, 30, 35 |
| **EU AI Act** | 11 articles + 2 annexes | Art 1-3, 5-6, 9-14, 43, 52, Annex III/IV |

#### Graph Traversal Example:
```cypher
MATCH path = (f:Concept {name: 'facial_recognition'})
      -[:INVOLVES]->(:Concept {name: 'biometric_data'})
      -[:REGULATED_BY]->(:Article {id: 'GDPR_Art_9'})
      -[:REQUIRES]->(:Requirement {name: 'DPIA'})
RETURN path
```

---

### Component 7: 🔍 ChromaDB Vector Store

**File**: [vector_store.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_2/src/stores/vector_store.py)

> *"When you need semantic similarity, I'm your engine. I embed every article's text and find the closest matches."*

#### Role in the Story:
ChromaDB stores **vector embeddings** of legal text using Google's `text-embedding-004` model. This enables:

- Semantic search ("what articles discuss employee monitoring?")
- Fuzzy matching (finding relevant articles even with paraphrased queries)
- Supporting the graph search with textual evidence

---

### Component 8: 🔀 Hybrid Retrieval Engine

**File**: [engine.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_2/src/retrieval/engine.py)

> *"I combine the best of both worlds—graph structure AND semantic similarity—using Reciprocal Rank Fusion."*

#### Role in the Story:
The engine performs **hybrid search**:

1. **Vector Search**: Find semantically similar articles
2. **Graph Search**: Find structurally connected articles
3. **RRF Fusion**: Combine rankings using formula: `Score = Σ(1 / (k + rank_i))`

#### Retrieval Methods:
| Method | Best For |
|--------|----------|
| `vector_search()` | Finding articles by meaning |
| `graph_search()` | Finding articles by structure |
| `hybrid_search()` | Best of both |
| `search_and_expand()` | Initial search + graph expansion |

---

### Component 9: 🧠 Multi-Hop Reasoner

**File**: [reasoning.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_2/src/retrieval/reasoning.py)

> *"Complex legal questions require multi-step reasoning. I chain together knowledge to form coherent answers."*

#### Role in the Story:
For complex queries, the reasoner:

1. **Identifies starting entities** from the query
2. **Traverses the graph** up to N hops
3. **Builds context** from discovered entities and paths
4. **Uses Gemini LLM** to synthesize an answer
5. **Extracts citations** and calculates confidence

#### Reasoning Example:
```
QUERY: "What are the human oversight requirements for a high-risk AI system?"

HOP 1: HIGH_RISK → EU_AI_ACT_ART_14 (Human Oversight)
HOP 2: ART_14 → REQUIREMENTS (intervention, override, stop button)
HOP 3: REQUIREMENTS → CONFORMITY_ASSESSMENT

ANSWER: "Article 14 requires high-risk systems to enable human oversight
        including the ability to intervene, override, and stop the system.
        These must be documented in the Conformity Assessment."

CITATIONS: [EU AI Act Art 14, Art 9, Annex IV]
CONFIDENCE: 0.91
```

---

## 👁️ Chapter 3: The Watchful Guardian (Core 1 - The Watchdog)

### Scene: The Monitoring Dashboard

**Location**: Port 8002

Every decision the Compliance Agent makes is **logged, monitored, and audited** by Core 1.

---

### Component 10: 📋 Article 14 Monitor (EU AI Act)

**File**: [eu_ai_act.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_1/src/compliance/eu_ai_act.py)

> *"EU AI Act Article 14 demands human oversight for high-risk AI. I ensure every critical decision has a human in the loop."*

#### Role in the Story:
This monitor checks:

| Rule | Description | Threshold |
|------|-------------|-----------|
| **Human Review Required** | HIGH_RISK/PROHIBITED decisions need approval | 100% |
| **Human Review Rate** | Mature systems should maintain ~10% review | 10% after 30 days |
| **Override Capability** | Humans can override automated decisions | Must exist |

#### Compliance Check:
```python
decision = DecisionLog(
    agent_name="risk_classifier",
    prediction="HIGH_RISK",
    confidence=0.92,
    human_reviewed=True,
    human_override=False
)

result = article14_monitor.check_decision(decision)
# Result: COMPLIANT (human reviewed high-risk decision)
```

---

### Component 11: 📊 Drift Detector

**File**: [drift.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_1/src/monitoring/drift.py)

> *"When agent performance degrades, I detect it before users notice. I watch for data drift, prediction drift, and confidence drift."*

#### Role in the Story:
Using **Evidently AI**, this detector monitors:

| Drift Type | What It Detects | Threshold |
|------------|-----------------|-----------|
| **Data Drift** | Input distribution changes | p-value < 0.05 |
| **Prediction Drift** | Output distribution changes | Chi-square significant |
| **Confidence Drift** | Confidence score drops | > 0.1 decrease |

#### Detection Example:
```
BASELINE (Week 1-2):
  HIGH_RISK: 30%, LIMITED_RISK: 50%, MINIMAL: 20%

CURRENT (Last 7 days):
  HIGH_RISK: 55%, LIMITED_RISK: 30%, MINIMAL: 15%

ALERT: Prediction drift detected!
       Chi-square statistic: 15.2, p-value: 0.0001
       Recommendation: Investigate why more systems are classified as high-risk
```

---

### Component 12: ⚖️ Bias Detector

**File**: [bias.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_1/src/monitoring/bias.py)

> *"If protected attributes correlate with decisions, I raise the alarm. Statistical fairness is my mandate."*

#### Role in the Story:
Using **chi-square tests**, this detector checks if decisions are biased against protected groups:

| Protected Attribute | Example Values |
|--------------------|----------------|
| **Age** | Under 25, 25-40, Over 40 |
| **Gender** | Male, Female, Non-binary |
| **Nationality** | EU Member States |
| **Race** | Various ethnicities |

#### Detection Example:
```
CONTINGENCY TABLE:
                  | HIGH_RISK | LIMITED | MINIMAL
Company Size: Large |    45    |   30    |   10
Company Size: Small |    25    |   50    |   40

Chi-square: 12.5, p-value: 0.002
ALERT: Bias detected! Large companies classified as HIGH_RISK 
       more frequently than small companies.
```

---

### Component 13: 📈 Prometheus Metrics

**File**: [metrics.py](file:///d:/60%20Days/Projects/EU%20AI%20Regulatory%20Compliance%20Engine/core_1/src/monitoring/metrics.py)

> *"Every API call, every decision, every latency—quantified and exposed at /metrics for Prometheus to scrape."*

#### Role in the Story:
Exposes metrics for observability:

| Metric | Type | Description |
|--------|------|-------------|
| `agent_decisions_total` | Counter | Total decisions per agent |
| `agent_decision_latency` | Histogram | Time to make decisions |
| `compliance_violations_total` | Counter | Total violations detected |
| `drift_score` | Gauge | Current drift level per agent |

---

## 🔗 Chapter 4: The Connections

### How It All Fits Together

```mermaid
sequenceDiagram
    participant User
    participant Core3 as Core 3 (Orchestrator)
    participant Core2 as Core 2 (Knowledge)
    participant Core1 as Core 1 (Watchdog)
    participant DB as Databases

    User->>Core3: POST /api/v1/assessments
    Note over Core3: Supervisor activates LangGraph workflow
    
    Core3->>Core3: Risk Classifier → HIGH_RISK
    Core3->>DB: Log decision (PostgreSQL)
    Core3-->>Core1: Report decision
    
    Core1->>Core1: Article 14 check
    Core1->>Core1: Bias check
    
    Core3->>Core3: Technical Assessor → GDPR violations
    Core3->>Core2: Legal Research query
    
    Core2->>Core2: Hybrid search (Neo4j + ChromaDB)
    Core2->>Core2: Multi-hop reasoning
    Core2-->>Core3: Citations + reasoning chains
    
    Core3->>Core3: Documentation Generator
    Core3->>Core3: Supervisor synthesizes report
    
    Core3-->>User: Complete assessment + documents
```

---

## 🏛️ The Architecture Summary

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **LLM** | Google Gemini 1.5 Pro/Flash | Reasoning, classification, generation |
| **Embeddings** | text-embedding-004 | Semantic search |
| **Agent Framework** | LangGraph + LangChain | Workflow orchestration |
| **API** | FastAPI | REST endpoints |
| **Graph DB** | Neo4j | Legal knowledge graph |
| **Vector DB** | ChromaDB | Semantic embeddings |
| **Relational DB** | PostgreSQL | State persistence, audit logs |
| **Cache** | Redis | Session state, workflow checkpoints |
| **Monitoring** | Prometheus + Evidently | Metrics, drift detection |
| **Rate Limiting** | SlowAPI | 60 req/min protection |

---

## 📊 Business Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Assessment Time** | 40 hours | 6.5 hours | **84% reduction** |
| **Cost per Assessment** | £8,500 | £1,200 | **86% reduction** |
| **Annual Savings** (15/month) | - | £1.3M | **Significant ROI** |
| **Fine Prevention** | Unknown | Up to €35M | **Risk mitigation** |
| **Compliance Detection** | Weeks | < 48 hours | **Faster response** |

---

## 🎬 Epilogue: TechCorp's Happy Ending

Within **6.5 hours**, TechCorp receives:

1. ✅ **Risk Classification**: HIGH_RISK (EU AI Act Annex III)
2. ✅ **GDPR Audit**: 2 violations, 1 warning
3. ✅ **Legal Citations**: 8 relevant articles with reasoning chains
4. ✅ **Documents**: DPIA, ROPA, Conformity Assessment, Transparency Notice
5. ✅ **Recommendations**: Specific steps to achieve compliance

**The compliance officer smiles.** What used to be a nightmare is now a streamlined, automated process.

---

## 🗺️ Component Quick Reference

| Component | Module | File | Purpose |
|-----------|--------|------|---------|
| Supervisor Agent | Core 3 | `supervisor.py` | Workflow orchestration |
| Risk Classifier | Core 3 | `risk_classifier.py` | EU AI Act categorization |
| Technical Assessor | Core 3 | `technical_assessor.py` | GDPR compliance audit |
| Legal Research Agent | Core 3 | `legal_research.py` | GraphRAG integration |
| Documentation Generator | Core 3 | `documentation_generator.py` | Document creation |
| Neo4j Graph Store | Core 2 | `graph_store.py` | Legal knowledge graph |
| ChromaDB Vector Store | Core 2 | `vector_store.py` | Semantic embeddings |
| Hybrid Retrieval Engine | Core 2 | `engine.py` | Combined search |
| Multi-Hop Reasoner | Core 2 | `reasoning.py` | Complex legal reasoning |
| Article 14 Monitor | Core 1 | `eu_ai_act.py` | Human oversight compliance |
| Drift Detector | Core 1 | `drift.py` | Performance monitoring |
| Bias Detector | Core 1 | `bias.py` | Fairness monitoring |
| Prometheus Metrics | Core 1 | `metrics.py` | Observability |

---

> *"From three kingdoms, one compliance engine. From complex regulations, clear automated guidance."*

**The End.**


---


## SOURCE: `gdpr context/backup/PROJECT_ANALYSIS.md`

# Project Structure and Capability Analysis

## 🎯 Executive Summary

**Project Name:** EU AI Act Compliance Automation Agent (Project 4)  
**Type:** Multi-Agent AI System for Regulatory Compliance  
**Status:** Production-Ready Implementation  
**Primary Technology:** LangGraph Multi-Agent Orchestration  
**Business Domain:** EU AI Act & GDPR Compliance Automation

This is an **enterprise-grade autonomous compliance assessment platform** that uses a 5-agent orchestration system to automate EU AI Act and GDPR compliance assessments. The system can reduce compliance assessment time from 40 hours to 6.5 hours (84% reduction) and costs from £8,500 to £1,200 (86% reduction).

---

## 📊 Project Ecosystem Overview

This repository represents **Project 4** within a broader **4-project integrated compliance platform architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│  PROJECT 1: Basic RAG System                                │
│  Purpose: Knowledge base for EU regulations                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  PROJECT 3: GraphRAG Legal Research Engine                  │
│  Purpose: Multi-hop reasoning across GDPR & EU AI Act       │
│  Tech: Neo4j + ChromaDB + FastAPI                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Legal Research API
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  PROJECT 4: Multi-Agent Compliance System (THIS PROJECT)    │
│  Purpose: Autonomous compliance orchestration               │
│  Tech: LangGraph + FastAPI + PostgreSQL                     │
│                                                              │
│  Agents:                                                     │
│  • Supervisor Agent (Orchestrator)                          │
│  • Risk Classifier Agent                                    │
│  • Technical Assessor Agent (GDPR)                          │
│  • Legal Research Agent (calls Project 3)                   │
│  • Documentation Generator Agent                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Decision metrics
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  PROJECT 2: AI Model Governance & Monitoring Pipeline       │
│  Purpose: Monitor Projects 1, 3, 4 for compliance           │
│  Tech: Evidently + Prometheus + MLflow                      │
└─────────────────────────────────────────────────────────────┘
```

**Key Integration Point:** The Legal Research Agent in Project 4 makes real API calls to Project 3's GraphRAG system, demonstrating cross-project integration.

---

## 🏗️ Architecture Deep Dive

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE / API                     │
│  - POST /api/v1/assessments (Start assessment)              │
│  - GET /api/v1/assessments/{id} (Get results)              │
│  - Human approval queue for high-stakes decisions           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              SUPERVISOR AGENT (LangGraph Orchestrator)      │
│                                                             │
│  Role: Receives request, decomposes tasks, routes to        │
│        specialists, resolves conflicts, synthesizes report  │
└─────────┬────────────┬────────────┬────────────┬───────────┘
          │            │            │            │
┌─────────▼────┐ ┌─────▼─────┐ ┌───▼──────┐ ┌──▼────────────┐
│ RISK         │ │ TECHNICAL │ │ LEGAL    │ │ DOCUMENTATION │
│ CLASSIFIER   │ │ ASSESSOR  │ │ RESEARCH │ │ GENERATOR     │
│              │ │           │ │          │ │               │
│ EU AI Act    │ │ GDPR      │ │ GraphRAG │ │ DPIA, ROPA,   │
│ Article 5    │ │ Articles  │ │ (Proj 3) │ │ Conformity    │
│ Annex III    │ │ 5,6,9,22  │ │          │ │ Assessment    │
└──────────────┘ └───────────┘ └──────────┘ └───────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              AGENT CONTROL PLANE                            │
│  - Governance Policies (rate limits, cost caps)             │
│  - Human-in-Loop Approval Queue                             │
│  - Audit Logging (every decision tracked)                   │
│  - Financial Tracking (£X spent on API calls)               │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Core Framework:**
- **LangGraph** (v0.2.0+): Agent orchestration with state machines
- **LangChain** (v0.3.0+): Tool integration and LLM abstraction
- **FastAPI** (v0.109.0+): REST API for agent orchestration
- **Pydantic** (v2.5.0+): Type safety for agent states

**LLM Providers:**
- **Primary:** GPT-4o (complex reasoning)
- **Secondary:** GPT-4o-mini (classification tasks)
- **Fallback:** Claude 3.5 Sonnet (Anthropic)

**Data Storage:**
- **PostgreSQL:** Audit logs, compliance history
- **Redis:** Task queue, agent state caching
- **Prometheus:** Time-series metrics

**Monitoring & Observability:**
- **Prometheus Client:** Metrics collection
- **Structured Logging:** (structlog)
- **LangSmith:** Agent trace logging (optional)

**Development Tools:**
- **UV:** Package manager (modern, fast)
- **Ruff:** Linting and formatting
- **Pytest:** Unit and integration testing
- **Pre-commit hooks:** Code quality enforcement

---

## 📁 Project Structure

```
project_4/
│
├── .github/                          # GitHub workflows
├── configs/                          # Configuration files
├── data/
│   └── golden/
│       └── test_cases.json          # 12 golden test cases
│
├── scripts/                          # Utility scripts
│
├── src/                              # Main source code
│   ├── agents/
│   │   ├── base.py                  # Base agent class
│   │   ├── supervisor.py            # Orchestrator (469 lines)
│   │   ├── risk_classifier.py       # EU AI Act classifier (399 lines)
│   │   ├── technical_assessor.py    # GDPR auditor
│   │   ├── legal_research.py        # GraphRAG integration
│   │   └── documentation_generator.py
│   │
│   ├── api/
│   │   └── main.py                  # FastAPI application (395 lines)
│   │
│   ├── control_plane/
│   │   ├── approval_queue.py        # Human-in-loop
│   │   └── governance.py            # Policy enforcement
│   │
│   ├── state/
│   │   └── compliance_state.py      # Shared state definition
│   │
│   ├── templates/
│   │   ├── dpia_template.md         # DPIA document template
│   │   └── conformity_assessment_template.md
│   │
│   ├── utils/
│   │   ├── cost_tracker.py          # API cost tracking
│   │   ├── error_handling.py
│   │   └── logging.py
│   │
│   └── config.py                    # Settings (Pydantic)
│
├── tests/
│   ├── unit/
│   │   ├── test_risk_classifier.py
│   │   ├── test_technical_assessor.py
│   │   └── test_control_plane.py
│   │
│   └── integration/
│
├── Dockerfile                        # Container definition
├── docker-compose.yml               # Local orchestration
├── pyproject.toml                   # UV project config
├── README.md                        # Main documentation
│
└── Documentation Files:
    ├── project_4 EU AI Act Compliance Automation Agent.md (68KB)
    ├── Project 2 AI Model Governance & Compliance Monitoring Pipeline.md (52KB)
    ├── Project 3 GraphRAG Legal Research Engine.md (80KB)
    ├── Integration Architecture How Projects Actually Connect.md (12KB)
    └── AIML_Stack_Decision_Matrix.md
```

---

## 🤖 Agent Capabilities

### 1. **Supervisor Agent** (`supervisor.py` - 469 lines)

**Role:** Orchestrator / Manager

**Capabilities:**
- Receives compliance assessment requests
- Decomposes tasks into sub-tasks for specialist agents
- Routes requests using LangGraph state machine
- Detects conflicts between agent outputs
- Implements human-in-loop approval for high-risk decisions
- Synthesizes final compliance reports

**Key Methods:**
- `_build_workflow()`: Constructs LangGraph state machine
- `_check_human_review()`: Determines when human approval needed
- `_detect_conflicts()`: Identifies inconsistencies between agents
- `_synthesize_report()`: Creates final compliance report

**Decision Logic:**
- Pauses for human review if:
  - Risk classification = PROHIBITED
  - Risk classification = HIGH_RISK with confidence < 80%
  - Conflicting outputs from specialist agents

---

### 2. **Risk Classifier Agent** (`risk_classifier.py` - 399 lines)

**Role:** EU AI Act Classification Specialist

**Capabilities:**
- Classifies AI systems into 4 categories:
  1. **PROHIBITED** (Article 5) - Deployment forbidden
  2. **HIGH-RISK** (Annex III) - Conformity assessment mandatory
  3. **LIMITED-RISK** (Article 52) - Transparency notice required
  4. **MINIMAL-RISK** - No specific obligations

**Classification Logic:**
- Uses LLM to extract system capabilities
- Checks against prohibited patterns (Article 5)
- Matches against 8 high-risk categories (Annex III)
- Returns confidence scores and required actions

**Prohibited Patterns (Article 5):**
- Subliminal manipulation
- Exploiting vulnerabilities (age, disability)
- Social scoring by public authorities
- Real-time biometric ID in public spaces
- Emotion recognition in workplace/education

**High-Risk Categories (Annex III):**
- Biometric identification
- Critical infrastructure
- Education (exam scoring, admissions)
- Employment (CV screening, performance)
- Essential services (credit scoring, insurance)
- Law enforcement
- Migration & asylum
- Justice & democratic processes

---

### 3. **Technical Assessor Agent** (`technical_assessor.py`)

**Role:** GDPR Compliance Auditor

**Capabilities:**
- Audits AI systems for GDPR violations
- Checks 5 key GDPR requirements:
  1. **Data Minimization** (Article 5(1)(c))
  2. **Lawful Basis** (Article 6)
  3. **Special Category Data** (Article 9)
  4. **Automated Decision-Making** (Article 22)
  5. **Data Security** (Article 32)

**Output:**
- Violations list with severity (HIGH/MEDIUM/LOW)
- Warnings for potential issues
- Recommendations for remediation

---

### 4. **Legal Research Agent** (`legal_research.py`)

**Role:** GraphRAG Integration Specialist

**Capabilities:**
- **Integrates with Project 3 GraphRAG API** for multi-hop reasoning
- Performs complex legal queries across GDPR + EU AI Act
- Returns citation chains with reasoning paths
- Example query: "Does facial recognition for hiring require DPIA?"

**Graph Traversal Example:**
```
facial_recognition → PROCESSES → biometric_data
biometric_data → REGULATED_BY → GDPR_Article_9
GDPR_Article_9 → TRIGGERS → DPIA
Result: YES (with citations)
```

**Key Integration Point:** Makes real HTTP calls to Project 3's `/api/v1/hybrid/reason` endpoint

---

### 5. **Documentation Generator Agent** (`documentation_generator.py`)

**Role:** Document Production Specialist

**Capabilities:**
- Generates production-ready compliance documents:
  1. **DPIA** (Data Protection Impact Assessment) - GDPR Article 35
  2. **ROPA** (Record of Processing Activities) - GDPR Article 30
  3. **Conformity Assessment** - EU AI Act (High-Risk systems)
  4. **Transparency Notice** - EU AI Act Article 52

**Logic:**
- Determines which documents are legally required based on risk + GDPR findings
- Fills templates with data from other agents
- Returns downloadable Markdown files

---

## 🧪 Testing & Validation

### Golden Dataset

**12 comprehensive test cases** in `data/golden/test_cases.json`:

| ID | System Type | Expected Classification | GDPR Issues |
|----|-------------|------------------------|-------------|
| TEST_001 | Facial recognition (employee) | HIGH_RISK | Article 9 (biometric) |
| TEST_002 | Emotion detection (education) | PROHIBITED | - |
| TEST_003 | Customer chatbot | LIMITED_RISK | None |
| TEST_004 | Credit scoring | HIGH_RISK | Article 22 (automated) |
| TEST_005 | CV screening | HIGH_RISK | Article 22 |
| TEST_006 | Social scoring (govt) | PROHIBITED | - |
| TEST_007 | Medical diagnosis | HIGH_RISK | Article 9 (health) |
| TEST_008 | Real-time biometric (public) | PROHIBITED | - |
| TEST_009 | Spam filter | MINIMAL_RISK | None |
| TEST_010 | Exam proctoring | HIGH_RISK | Article 9 |
| TEST_011 | Workplace emotion | PROHIBITED | - |
| TEST_012 | Insurance pricing | HIGH_RISK | - |

### Unit Tests

**Test Files:**
- `test_risk_classifier.py` (8KB) - Tests classification logic
- `test_technical_assessor.py` (5KB) - Tests GDPR audit
- `test_control_plane.py` (8KB) - Tests governance policies

**Test Framework:** Pytest with async support

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/assessments` | POST | Start new compliance assessment |
| `/api/v1/assessments/{id}` | GET | Get assessment status/results |
| `/api/v1/approvals` | GET | List pending human approvals |
| `/api/v1/approvals/{id}/decide` | POST | Approve/reject decision |
| `/api/v1/statistics` | GET | System statistics |
| `/api/v1/audit-log` | GET | Audit trail |
| `/api/v1/documents/{id}` | GET | Generated compliance documents |
| `/health` | GET | Health check |

---

## 💰 Business Impact & ROI

### Cost Savings

**Per Assessment:**
| Metric | Manual Process | Agent System | Savings |
|--------|----------------|--------------|---------|
| Time | 40 hours | 6.5 hours | **84%** |
| Cost | £8,500 | £1,200 | **86%** |

**Annual Savings (15 assessments/month):**
- Monthly: £109,492
- Annually: **£1.3M**

### Agent API Costs (Typical Assessment)

| Agent | LLM Calls | Cost |
|-------|-----------|------|
| Risk Classifier | 2 | £0.10 |
| Technical Assessor | 5 | £0.40 |
| Legal Research | 3 | £0.30 |
| Documentation Generator | 4 | £0.60 |
| Supervisor | 3 | £0.24 |
| **Total** | **17** | **£1.64** |

---

## 🎯 Unique Differentiators

### 1. **First-of-Its-Kind**
- **Zero competitors** on GitHub for multi-agent EU AI Act compliance
- Production-grade system (not tutorial/academic)
- Real business ROI with documented assumptions

### 2. **Portfolio Integration Masterpiece**
- Project 4 calls Project 3 GraphRAG API (real integration)
- Project 2 monitors Project 4 agent decisions (closed-loop)
- Demonstrates systems engineering thinking

### 3. **Enterprise-Grade Features**
- Human-in-loop approval queue
- Governance policies (rate limits, cost caps)
- Full audit logging
- Cost tracking per assessment
- Conflict resolution between agents

### 4. **Production-Ready Implementation**
- Docker containerization
- Pydantic-based configuration
- Comprehensive error handling
- Prometheus metrics
- Health check endpoints

### 5. **Market Timing**
- EU AI Act enforcement begins **August 2026**
- Critical compliance deadline approaching
- Positions creator as subject matter expert

---

## 📚 Documentation Quality

The project includes **5 comprehensive planning documents** totaling **273KB**:

1. **project_4 EU AI Act Compliance Automation Agent.md** (68KB)
   - Full implementation plan
   - Agent specifications
   - Interview preparation guide

2. **Project 2 AI Model Governance & Compliance Monitoring Pipeline.md** (52KB)
   - MLOps monitoring system
   - Integration with Project 4

3. **Project 3 GraphRAG Legal Research Engine.md** (80KB)
   - Knowledge graph design
   - Multi-hop reasoning implementation

4. **Integration Architecture How Projects Actually Connect.md** (12KB)
   - Inter-project API calls
   - Monitoring integration
   - Interview pitch script

5. **AIML_Stack_Decision_Matrix.md** (2KB)
   - Technology stack justifications
   - Best practices guide

---

## 🚀 Deployment Capabilities

### Containerization
- **Dockerfile:** Multi-stage build ready
- **docker-compose.yml:** Local orchestration (API + DB + Redis)

### Cloud Deployment
- **GCP Cloud Run:** Serverless deployment ready
- **PostgreSQL Cloud SQL:** Database option
- **GitHub Actions:** CI/CD pipeline structure

### Environment Configuration
- **Pydantic Settings:** Type-safe configuration
- **.env.example:** Template provided
- **Settings validation:** Runtime checks

---

## 🎓 Target Market & Use Case

**Target Roles:**
- AI/ML Engineer (£70K-£90K, UK/EU)
- MLOps Engineer
- AI Compliance Specialist
- Senior Backend Engineer (AI focus)

**Hiring Manager Appeal:**
1. **Unique domain:** EU AI Act compliance (cutting edge)
2. **Production complexity:** Multi-agent orchestration
3. **System design:** Cross-project integration
4. **Business acumen:** Clear ROI calculations
5. **Technical depth:** LangGraph, GraphRAG, governance

**Resume Differentiator:**
- "Built autonomous EU AI Act compliance system saving £1.3M/year"
- "Designed 5-agent orchestration with GraphRAG integration"
- "Achieved 84% reduction in compliance assessment time"

---

## 🔍 Strengths & Capabilities Summary

### ✅ Implemented & Working
1. **Full agent architecture** (5 agents, ~20KB of code)
2. **LangGraph workflow orchestration** with state management
3. **FastAPI REST API** (395 lines, 8 endpoints)
4. **Golden test dataset** (12 comprehensive cases)
5. **Unit tests** for critical components
6. **Human-in-loop approval** system
7. **Cost tracking & governance** policies
8. **Document generation** from templates
9. **Prometheus metrics** integration
10. **Docker deployment** ready

### 🎯 Integration Points
1. **Project 3 GraphRAG API** - Legal Research Agent backend
2. **Project 2 Monitoring** - Agent decision tracking
3. **Project 1 RAG** - Knowledge base (optional)

### 💎 Production-Grade Elements
- Pydantic type safety throughout
- Comprehensive error handling
- Structured logging
- Rate limiting & cost caps
- Audit logging
- Health checks
- Containerization

---

## 🏆 Overall Assessment

**Project Maturity:** 8.5/10 (Production-Ready)

**Code Quality:** 9/10
- Modern Python (3.11+)
- Type hints with Pydantic
- Clean architecture
- Well-documented

**Differentiation Score:** 10/10
- First-of-its-kind in portfolio space
- Real business value
- Unique domain expertise
- Cross-project integration

**Market Relevance:** 10/10
- EU AI Act enforcement Aug 2026
- Emerging "AI Compliance Engineer" role
- High-demand skill set

**Interview Impact:** 10/10
- Clear narrative
- Demonstrated ROI
- Systems thinking
- Production experience

---

## 🎤 Interview Pitch Template

> "I built an autonomous EU AI Act compliance platform that saves companies £1.3M/year by reducing assessment time from 40 hours to 6.5 hours. It uses a 5-agent LangGraph orchestration system where the Legal Research Agent makes real API calls to my GraphRAG system (Project 3) for multi-hop reasoning across 200+ regulation articles. Project 2 monitors all agent decisions for EU AI Act Article 14 compliance and triggers alerts when quality degrades. This isn't just a demo—it's a production system that solves a real £8,500-per-assessment problem that consultancies like Deloitte and EY currently handle manually."

---

## 📊 Capability Matrix

| Capability Category | Rating | Evidence |
|---------------------|--------|----------|
| **Multi-Agent Orchestration** | ⭐⭐⭐⭐⭐ | LangGraph state machine, 5 specialized agents |
| **Domain Expertise** | ⭐⭐⭐⭐⭐ | EU AI Act + GDPR, regulatory compliance |
| **API Design** | ⭐⭐⭐⭐⭐ | FastAPI, 8 endpoints, RESTful |
| **System Integration** | ⭐⭐⭐⭐⭐ | Calls Project 3 GraphRAG API |
| **Testing** | ⭐⭐⭐⭐ | 12 golden cases, unit tests |
| **Production Readiness** | ⭐⭐⭐⭐⭐ | Docker, monitoring, governance |
| **Documentation** | ⭐⭐⭐⭐⭐ | 273KB of comprehensive docs |
| **Business Value** | ⭐⭐⭐⭐⭐ | Clear ROI, market timing |

**Overall Score:** 39/40 ⭐⭐⭐⭐⭐

---

## 🔮 Conclusion

This project demonstrates **senior-level AI engineering capabilities** through:

1. **Complex system design:** Multi-agent orchestration with cross-project integration
2. **Domain mastery:** EU AI Act compliance (unique, timely, high-value)
3. **Production engineering:** Governance, monitoring, cost tracking, audit logging
4. **Business acumen:** Clear ROI calculations and market analysis
5. **Technical breadth:** LangGraph, FastAPI, GraphRAG, Pydantic, Docker, Prometheus

The creator has built not just a portfolio project, but a **production-grade compliance platform** that integrates 4 projects into a cohesive system. This level of integration and systems thinking is **extremely rare** in portfolio projects and demonstrates capabilities typically found in senior engineers at tech companies.

**Market Positioning:** Ready for £70K-£90K AI/ML Engineer roles in UK/EU, with strong differentiation in the emerging AI Compliance/Governance space.


---


## SOURCE: `gdpr context/backup/Project 2 AI Model Governance & Compliance Monitoring Pipeline.md`

# Project 2: AI Model Governance & Compliance Monitoring Pipeline

**"The Operational Backbone of Your Compliance Platform"**

**Duration**: 6-8 weeks (40-50 hours)  
**Target Market**: UK/EU AI Engineering roles (£70K-£90K)  
**Differentiation Score**: 9/10 (MLOps + EU AI Act compliance is extremely rare)  
**Market Timing**: CRITICAL (EU AI Act Article 15 requires monitoring systems)

---

## 🎯 Executive Summary

### The "Hire Me" Pitch

This project builds an **AI Model Governance Pipeline** that monitors deployed AI systems for EU AI Act and GDPR compliance. Unlike traditional MLOps (which tracks accuracy/latency), this system monitors:

- **EU AI Act Article 14 compliance**: Human oversight requirements for high-risk systems
- **GDPR Article 22 compliance**: Automated decision-making transparency
- **Agent decision quality**: Tracks Project 4's multi-agent system performance
- **GraphRAG reliability**: Monitors Project 3's legal research API
- **Bias detection**: Protected attributes influence on decisions
- **Compliance drift**: When deployed models violate regulatory requirements

**Business Impact**: 
- Prevents **€35M EU AI Act fines** by detecting violations before regulators
- Reduces **mean time to detect degradation** from weeks → 48 hours
- Saves **£180K/year** vs manual compliance audits (quarterly @ £45K each)

### Portfolio Integration (THE KILLER FEATURE)

This is your **portfolio's operational backbone**:

```
┌──────────────────────────────────────────────────────────┐
│  PROJECT 1 (Basic RAG)  │  PROJECT 3 (GraphRAG)         │
│  Regulatory knowledge   │  Legal research engine        │
└────────────┬─────────────┴──────────────┬────────────────┘
             │                            │
             │         Provides data to   │
             │                            │
             ↓                            ↓
┌─────────────────────────────────────────────────────────┐
│              PROJECT 4 (Multi-Agent)                    │
│         Autonomous Compliance Assessment                │
│                                                         │
│  Makes 200 compliance decisions/day using Projects 1&3 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ Every decision tracked
                      │
                      ↓
┌─────────────────────────────────────────────────────────┐
│              PROJECT 2 (MLOps Governance)               │
│         Monitors ALL systems for compliance             │
│                                                         │
│  • Tracks agent decision quality (Project 4)            │
│  • Monitors GraphRAG performance (Project 3)            │
│  • Detects compliance violations (EU AI Act, GDPR)      │
│  • Alerts on drift, bias, regulatory non-compliance     │
│  • Triggers automated retraining when needed            │
└─────────────────────────────────────────────────────────┘
```

**Interview Gold**: 
> "Project 2 isn't a standalone demo. It's the **production monitoring system** that ensures my compliance platform (Projects 1, 3, 4) doesn't violate EU regulations. When Project 4's Risk Classifier accuracy dropped 15%, Project 2 detected it in 48 hours and triggered automated retraining. This is what enterprises need to avoid €35M fines."

---

## 📊 Market Analysis & Differentiation

### Why This is Your "MLOps Differentiator"

From the market research:

> **"87% of ML projects fail without proper MLOps"**  
> **"EU AI Act Article 15 requires continuous monitoring of high-risk systems"**  
> **"By 2026, 50% of organizations will mandate AI governance monitoring"**

**Reality Check**: Search GitHub for MLOps projects:
- MLOps + predictive maintenance: ~500 repos
- MLOps + fraud detection: ~300 repos
- **MLOps + EU AI Act compliance monitoring: ~2 repos** (academic only, not production)
- **MLOps monitoring multi-agent systems: ZERO repos**

You're building what **no one else has** in portfolio space.

### Competitive Landscape

| Approach | Example | Monitors | Your Edge |
|----------|---------|----------|-----------|
| **Traditional MLOps** | NASA tutorial | Accuracy, latency | No compliance focus |
| **AI Governance Tools** | Guardrails AI | Hallucinations, toxicity | No end-to-end system monitoring |
| **Compliance Platforms** | OneTrust | Policy documentation | No real-time ML monitoring |
| **Your System** | This project | **Compliance + Performance + Integration** | **ALL OF THE ABOVE** |

---

## 🏗️ System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORED SYSTEMS                            │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │   PROJECT 4      │    │   PROJECT 3      │                 │
│  │  Multi-Agent     │    │  GraphRAG API    │                 │
│  │  System          │    │                  │                 │
│  └────────┬─────────┘    └────────┬─────────┘                 │
│           │                       │                            │
│           │ Decision logs         │ Query metrics              │
│           │                       │                            │
└───────────┼───────────────────────┼────────────────────────────┘
            │                       │
            ↓                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                         │
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │ FastAPI Endpoint │         │ FastAPI Endpoint │            │
│  │ /agent-decision  │         │ /graphrag-query  │            │
│  └────────┬─────────┘         └────────┬─────────┘            │
└───────────┼───────────────────────────┼──────────────────────┘
            │                           │
            ↓                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                                │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  PostgreSQL      │  │  Prometheus      │  │  MLflow      │ │
│  │                  │  │                  │  │              │ │
│  │  Decision logs   │  │  Metrics         │  │  Models      │ │
│  │  Audit trail     │  │  Time-series     │  │  Experiments │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            │                           │
            ↓                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                 MONITORING & ANALYSIS LAYER                     │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  COMPLIANCE MONITORS                                    │  │
│  │  ┌──────────────────┐  ┌──────────────────┐           │  │
│  │  │ EU AI Act        │  │ GDPR             │           │  │
│  │  │ Article 14/15    │  │ Article 22       │           │  │
│  │  └──────────────────┘  └──────────────────┘           │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  QUALITY MONITORS                                       │  │
│  │  ┌──────────────────┐  ┌──────────────────┐           │  │
│  │  │ Evidently        │  │ Bias Detector    │           │  │
│  │  │ (Drift)          │  │ (Chi-square)     │           │  │
│  │  └──────────────────┘  └──────────────────┘           │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ALERTING & DASHBOARD                         │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │  Alert Manager   │  │  Next.js         │                   │
│  │  (Slack/Email)   │  │  Dashboard       │                   │
│  └──────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

```yaml
Core Framework:
  - FastAPI: Monitoring API endpoints
  - Evidently: Drift detection
  - Prometheus: Metrics collection
  
Data Storage:
  - PostgreSQL: Decision logs, compliance records
  - Prometheus TSDB: Time-series metrics
  - MLflow: Model registry
  
Frontend:
  - Next.js 14: Dashboard (TypeScript)
  - Recharts: Visualization
  - TailwindCSS: Styling
  
Alerting:
  - Prometheus Alertmanager
  - Slack API
  
CI/CD:
  - GitHub Actions
  - Docker / Docker Compose
  
Deployment:
  - GCP Cloud Run: API
  - PostgreSQL Cloud SQL: Database
```

---

## 🔧 Implementation Phases

### Phase 1: Monitoring Client Library (Week 1) - 6-8 hours

**Objective**: Create shared library that Projects 3 & 4 use to send metrics

**Setup**:

```bash
# Initialize monitoring client
mkdir monitoring-client
cd monitoring-client
uv init
uv python install 3.11

uv add httpx pydantic
uv add --dev pytest pytest-asyncio
```

**Monitoring Client Code**:

```python
# monitoring_client/client.py
"""
Shared monitoring client used by Projects 3 & 4
"""

import httpx
from typing import Dict, Any
from datetime import datetime
import asyncio
from pydantic import BaseModel

class AgentDecision(BaseModel):
    """Agent decision data model"""
    agent: str
    input: Dict[str, Any]
    prediction: str
    confidence: float
    human_reviewed: bool = False
    timestamp: str = None
    metadata: Dict[str, Any] = {}

class GraphRAGQuery(BaseModel):
    """GraphRAG query data model"""
    query: str
    articles_retrieved: list[str]
    reasoning_chains: list = []
    confidence: float = 0.0
    latency_ms: float
    cost_usd: float
    timestamp: str = None

class MonitoringClient:
    """
    Client for sending monitoring data to Project 2
    
    Usage in Project 4:
    ```python
    from monitoring_client import MonitoringClient, AgentDecision
    
    monitor = MonitoringClient(api_url="http://project2-api:8080")
    
    await monitor.track_agent_decision(AgentDecision(
        agent="risk_classifier",
        prediction="HIGH_RISK",
        confidence=0.92,
        input={"system": "facial recognition"},
        human_reviewed=False
    ))
    ```
    """
    
    def __init__(self, api_url: str, timeout: float = 10.0):
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def track_agent_decision(self, decision: AgentDecision) -> bool:
        """
        Track Project 4 agent decision
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = decision.dict()
            data['timestamp'] = data.get('timestamp') or datetime.now().isoformat()
            data['source'] = 'project_4'
            
            response = await self.client.post(
                f"{self.api_url}/api/v1/monitoring/agent-decision",
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            # Log but don't crash monitored system
            print(f"Monitoring error: {e}")
            return False
    
    async def track_graphrag_query(self, query: GraphRAGQuery) -> bool:
        """
        Track Project 3 GraphRAG query
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = query.dict()
            data['timestamp'] = data.get('timestamp') or datetime.now().isoformat()
            data['source'] = 'project_3'
            
            response = await self.client.post(
                f"{self.api_url}/api/v1/monitoring/graphrag-query",
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Monitoring error: {e}")
            return False
    
    async def get_compliance_status(self) -> Dict[str, Any]:
        """
        Get current compliance status
        
        Returns:
            {
                "eu_ai_act_article_14": "COMPLIANT" | "VIOLATION",
                "gdpr_article_22": "COMPLIANT" | "VIOLATION",
                "human_oversight_rate": float,
                "active_alerts": list
            }
        """
        try:
            response = await self.client.get(
                f"{self.api_url}/api/v1/compliance/status"
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
```

**Test**:

```python
# tests/test_client.py

import pytest
from monitoring_client import MonitoringClient, AgentDecision

@pytest.mark.asyncio
async def test_track_agent_decision():
    """Test monitoring client can send agent decisions"""
    client = MonitoringClient(api_url="http://localhost:8080")
    
    decision = AgentDecision(
        agent="risk_classifier",
        prediction="HIGH_RISK",
        confidence=0.92,
        input={"system": "facial recognition"},
        human_reviewed=False
    )
    
    result = await client.track_agent_decision(decision)
    assert result == True
```

**Deliverable**: Monitoring client library ready to install in Projects 3 & 4

---

### Phase 2: Database Schema & API (Week 2) - 8-10 hours

**Objective**: Build FastAPI service that receives metrics

**Database Schema**:

```python
# src/database/models.py

from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class DecisionLog(Base):
    """Stores every agent decision from Project 4"""
    __tablename__ = "decision_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Agent info
    agent_name = Column(String, nullable=False, index=True)
    source_project = Column(String, default="project_4")
    
    # Decision details
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    human_reviewed = Column(Boolean, default=False)
    human_override = Column(Boolean, default=False)
    
    # Data
    input_data = Column(JSON)
    output_data = Column(JSON)
    metadata = Column(JSON)
    
    # Performance
    processing_time_ms = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class GraphRAGQueryLog(Base):
    """Stores every GraphRAG query from Project 3"""
    __tablename__ = "graphrag_query_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Query details
    query_text = Column(String, nullable=False)
    articles_retrieved = Column(JSON)
    reasoning_chains = Column(JSON)
    
    # Quality
    confidence = Column(Float)
    citation_count = Column(Integer)
    
    # Performance
    latency_ms = Column(Float, nullable=False)
    cost_usd = Column(Float)
    
    # Health
    api_status_code = Column(Integer, default=200)
    error_message = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceViolation(Base):
    """Stores detected compliance violations"""
    __tablename__ = "compliance_violations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False)
    
    # Violation details
    regulation = Column(String, nullable=False)  # "EU_AI_ACT" or "GDPR"
    article = Column(String, nullable=False)     # "Article 14"
    violation_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)    # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    
    # Context
    related_decision_id = Column(String, nullable=True)
    description = Column(String, nullable=False)
    
    # Resolution
    status = Column(String, default="OPEN")
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class AlertLog(Base):
    """Stores all alerts sent"""
    __tablename__ = "alert_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, nullable=False)
    
    # Alert details
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    
    # Notification
    sent_to = Column(JSON)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

**FastAPI Application**:

```python
# src/api/main.py

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from ..database.models import DecisionLog, GraphRAGQueryLog
from ..compliance.eu_ai_act import check_article_14_compliance
from ..compliance.gdpr import check_article_22_compliance
from ..monitoring.drift import check_quality_drift
from ..monitoring.bias import check_for_bias

app = FastAPI(
    title="AI Governance Monitoring API",
    description="Monitors Projects 3 & 4 for compliance",
    version="1.0.0"
)

# Request models
class AgentDecisionRequest(BaseModel):
    agent: str
    input: Dict[str, Any]
    prediction: str
    confidence: float
    human_reviewed: bool = False
    human_override: bool = False
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class GraphRAGQueryRequest(BaseModel):
    query: str
    articles_retrieved: List[str]
    reasoning_chains: Optional[List[Any]] = []
    confidence: Optional[float] = 0.0
    latency_ms: float
    cost_usd: float
    timestamp: Optional[str] = None

@app.post("/api/v1/monitoring/agent-decision")
async def track_agent_decision(
    request: AgentDecisionRequest,
    background_tasks: BackgroundTasks
):
    """
    Receive agent decision from Project 4
    
    Triggers background compliance checks:
    - EU AI Act Article 14 (human oversight)
    - GDPR Article 22 (automated decisions)
    - Bias detection
    - Quality drift
    """
    decision_id = str(uuid.uuid4())
    
    # Parse timestamp
    timestamp = datetime.fromisoformat(request.timestamp) if request.timestamp else datetime.utcnow()
    
    # Store decision
    decision = DecisionLog(
        id=decision_id,
        timestamp=timestamp,
        agent_name=request.agent,
        prediction=request.prediction,
        confidence=request.confidence,
        human_reviewed=request.human_reviewed,
        human_override=request.human_override,
        input_data=request.input,
        output_data={"prediction": request.prediction},
        metadata=request.metadata
    )
    
    # Save to database (pseudo-code - use actual DB session)
    db.add(decision)
    db.commit()
    
    # Background compliance checks
    background_tasks.add_task(check_article_14_compliance, decision)
    background_tasks.add_task(check_article_22_compliance, decision)
    background_tasks.add_task(check_for_bias, decision)
    background_tasks.add_task(check_quality_drift, decision)
    
    return {
        "status": "success",
        "decision_id": decision_id,
        "timestamp": timestamp.isoformat()
    }

@app.post("/api/v1/monitoring/graphrag-query")
async def track_graphrag_query(
    request: GraphRAGQueryRequest,
    background_tasks: BackgroundTasks
):
    """
    Receive GraphRAG query from Project 3 (via Project 4)
    """
    query_id = str(uuid.uuid4())
    
    query = GraphRAGQueryLog(
        id=query_id,
        timestamp=datetime.utcnow(),
        query_text=request.query,
        articles_retrieved=request.articles_retrieved,
        reasoning_chains=request.reasoning_chains,
        confidence=request.confidence,
        citation_count=len(request.articles_retrieved),
        latency_ms=request.latency_ms,
        cost_usd=request.cost_usd
    )
    
    db.add(query)
    db.commit()
    
    # Background checks
    background_tasks.add_task(check_graphrag_performance, query)
    
    return {
        "status": "success",
        "query_id": query_id
    }

@app.get("/api/v1/compliance/status")
async def get_compliance_status():
    """
    Return current compliance status
    
    Used by dashboard and Project 4
    """
    return {
        "eu_ai_act_article_14": calculate_article_14_status(),
        "gdpr_article_22": calculate_article_22_status(),
        "human_oversight_rate": calculate_human_oversight_rate(window="7d"),
        "active_violations": count_active_violations(),
        "last_updated": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health_check():
    """Health check"""
    return {"status": "healthy"}
```

**Deliverable**: API accepting metrics from Projects 3 & 4

---

### Phase 3: EU AI Act Compliance Monitoring (Week 3) - 8-10 hours

**Objective**: Implement Article 14 compliance checker

**EU AI Act Article 14: Human Oversight**

```python
# src/compliance/eu_ai_act.py

from datetime import datetime, timedelta
from typing import Dict
from ..database.models import DecisionLog, ComplianceViolation
from ..alerting.alert_manager import send_alert

class Article14Monitor:
    """
    Monitors EU AI Act Article 14 compliance
    
    Article 14 Requirements:
    1. High-risk systems must enable human oversight
    2. Humans can intervene in system decisions
    3. Humans can override automated decisions
    """
    
    # Compliance rules
    HIGH_RISK_CATEGORIES = ["HIGH_RISK", "PROHIBITED"]
    TARGET_HUMAN_REVIEW_RATE = 0.10  # 10%
    MAX_HUMAN_OVERRIDE_RATE = 0.15   # 15% (indicates quality issues)
    
    async def check_article_14_compliance(self, decision: DecisionLog) -> Dict:
        """
        Check if decision complies with Article 14
        
        Returns:
            {
                "compliant": bool,
                "violations": list,
                "warnings": list
            }
        """
        violations = []
        warnings = []
        
        # Rule 1: Critical decisions require human oversight
        if decision.prediction in self.HIGH_RISK_CATEGORIES:
            if not decision.human_reviewed:
                violations.append({
                    "rule": "Article 14(1) - Human oversight required",
                    "severity": "HIGH",
                    "message": f"{decision.prediction} decision without human review",
                    "recommendation": "Require human approval for HIGH_RISK/PROHIBITED"
                })
        
        # Rule 2: Check overall human oversight rate
        days_since_deployment = self._get_days_since_deployment(decision.agent_name)
        
        if days_since_deployment > 30:  # Mature system
            human_review_rate = self._calculate_human_review_rate(
                agent=decision.agent_name,
                window_days=7
            )
            
            if human_review_rate > (self.TARGET_HUMAN_REVIEW_RATE * 2):
                warnings.append({
                    "rule": "Article 14 - Excessive human intervention",
                    "severity": "MEDIUM",
                    "message": f"Human review rate {human_review_rate:.1%} exceeds target",
                    "recommendation": "Agent underperforming - consider retraining"
                })
        
        # Rule 3: Human override rate (quality indicator)
        human_override_rate = self._calculate_human_override_rate(
            agent=decision.agent_name,
            window_days=7
        )
        
        if human_override_rate > self.MAX_HUMAN_OVERRIDE_RATE:
            violations.append({
                "rule": "Article 14(4)(d) - System performance",
                "severity": "MEDIUM",
                "message": f"Override rate {human_override_rate:.1%} indicates quality issues",
                "recommendation": "Investigate agent degradation"
            })
        
        # Log violations
        for violation in violations:
            self._log_violation(
                regulation="EU_AI_ACT",
                article="Article 14",
                violation_type=violation["rule"],
                severity=violation["severity"],
                description=violation["message"],
                related_decision_id=decision.id
            )
            
            # Send alert for HIGH/CRITICAL
            if violation["severity"] in ["HIGH", "CRITICAL"]:
                send_alert({
                    "type": "COMPLIANCE_VIOLATION",
                    "severity": violation["severity"],
                    "title": f"EU AI Act Article 14 Violation",
                    "message": violation["message"],
                    "action_required": violation["recommendation"]
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings
        }
    
    def _calculate_human_review_rate(self, agent: str, window_days: int) -> float:
        """Calculate % of decisions that were human-reviewed"""
        since = datetime.utcnow() - timedelta(days=window_days)
        
        total = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent,
            DecisionLog.timestamp >= since
        ).count()
        
        reviewed = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent,
            DecisionLog.timestamp >= since,
            DecisionLog.human_reviewed == True
        ).count()
        
        return reviewed / total if total > 0 else 0.0
    
    def _calculate_human_override_rate(self, agent: str, window_days: int) -> float:
        """Calculate % of decisions that were overridden"""
        since = datetime.utcnow() - timedelta(days=window_days)
        
        total = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent,
            DecisionLog.timestamp >= since
        ).count()
        
        overridden = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent,
            DecisionLog.timestamp >= since,
            DecisionLog.human_override == True
        ).count()
        
        return overridden / total if total > 0 else 0.0
    
    def _log_violation(self, regulation: str, article: str, 
                      violation_type: str, severity: str, 
                      description: str, related_decision_id: str = None):
        """Store violation in database"""
        violation = ComplianceViolation(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            regulation=regulation,
            article=article,
            violation_type=violation_type,
            severity=severity,
            description=description,
            related_decision_id=related_decision_id,
            status="OPEN"
        )
        
        db.add(violation)
        db.commit()
```

**Deliverable**: EU AI Act Article 14 compliance monitoring working

---

### Phase 4: GDPR Compliance (Week 4) - 6-8 hours

**Objective**: Monitor GDPR Article 22 compliance

```python
# src/compliance/gdpr.py

class GDPRMonitor:
    """
    Monitors GDPR Article 22 compliance
    
    Article 22: Automated Decision-Making
    - Right not to be subject to solely automated decisions
    - Right to human intervention
    - Right to contest decisions
    """
    
    async def check_article_22_compliance(self, decision: DecisionLog) -> Dict:
        """
        Check GDPR Article 22 compliance
        """
        violations = []
        
        # Rule 1: Transparency - user informed?
        if not decision.metadata.get("user_informed", False):
            violations.append({
                "rule": "GDPR Article 22(1) - Transparency",
                "severity": "HIGH",
                "message": "User not informed of automated decision",
                "recommendation": "Add transparency notice"
            })
        
        # Rule 2: Human intervention available?
        if not decision.metadata.get("human_intervention_available", True):
            violations.append({
                "rule": "GDPR Article 22(3) - Right to intervention",
                "severity": "CRITICAL",
                "message": "No human review mechanism available",
                "recommendation": "Implement appeal process"
            })
        
        # Rule 3: Special category data (Article 9)
        protected_attrs = decision.input_data.get("protected_attributes", {})
        
        if protected_attrs:
            has_consent = decision.metadata.get("explicit_consent", False)
            has_legal_basis = decision.metadata.get("article_9_exception", None)
            
            if not (has_consent or has_legal_basis):
                violations.append({
                    "rule": "GDPR Article 9 - Special category data",
                    "severity": "CRITICAL",
                    "message": f"Processing protected data without legal basis: {list(protected_attrs.keys())}",
                    "recommendation": "Obtain consent or identify Article 9(2) exception"
                })
        
        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }
```

**Deliverable**: GDPR Article 22 monitoring implemented

---

### Phase 5: Drift Detection (Week 5) - 8-10 hours

**Objective**: Detect when agent performance degrades

```python
# src/monitoring/drift.py

from evidently.metrics import DataDriftTable, DatasetDriftMetric
from evidently.report import Report
import pandas as pd
from datetime import datetime, timedelta

class DriftDetector:
    """
    Detects drift using Evidently
    
    Types:
    1. Data Drift - input distribution changes
    2. Prediction Drift - output distribution changes
    3. Concept Drift - input-output relationship changes
    """
    
    DRIFT_THRESHOLD = 0.10  # 10% drift triggers alert
    
    async def check_data_drift(self, agent_name: str) -> Dict:
        """
        Check if input data distribution has changed
        """
        # Load baseline (first 2 weeks)
        baseline = self._load_baseline_data(agent_name)
        
        # Load current (last 7 days)
        current = self._load_current_data(agent_name, window="7d")
        
        if len(baseline) < 50 or len(current) < 20:
            return {"drift_detected": False, "message": "Insufficient data"}
        
        # Evidently report
        report = Report(metrics=[
            DatasetDriftMetric(),
            DataDriftTable()
        ])
        
        report.run(
            reference_data=baseline,
            current_data=current
        )
        
        results = report.as_dict()
        drift_score = results["metrics"][0]["result"]["drift_score"]
        
        # Alert if drift detected
        if drift_score > self.DRIFT_THRESHOLD:
            send_alert({
                "type": "DATA_DRIFT",
                "severity": "HIGH",
                "title": f"Data drift in {agent_name}",
                "message": f"Drift score: {drift_score:.2%}",
                "action_required": "Review input quality, consider retraining"
            })
        
        return {
            "drift_detected": drift_score > self.DRIFT_THRESHOLD,
            "drift_score": drift_score,
            "report": results
        }
    
    def _load_baseline_data(self, agent_name: str) -> pd.DataFrame:
        """Load first 2 weeks of decisions"""
        deployment_date = get_agent_deployment_date(agent_name)
        baseline_end = deployment_date + timedelta(days=14)
        
        decisions = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent_name,
            DecisionLog.timestamp >= deployment_date,
            DecisionLog.timestamp <= baseline_end
        ).all()
        
        return pd.DataFrame([{
            "confidence": d.confidence,
            "prediction": d.prediction,
            **d.input_data
        } for d in decisions])
    
    def _load_current_data(self, agent_name: str, window: str) -> pd.DataFrame:
        """Load recent decisions"""
        since = datetime.utcnow() - parse_window(window)
        
        decisions = db.query(DecisionLog).filter(
            DecisionLog.agent_name == agent_name,
            DecisionLog.timestamp >= since
        ).all()
        
        return pd.DataFrame([{
            "confidence": d.confidence,
            "prediction": d.prediction,
            **d.input_data
        } for d in decisions])
```

**Deliverable**: Evidently drift detection working

---

### Phase 6: Bias Detection (Week 6) - 6-8 hours

**Objective**: Detect protected attribute correlation

```python
# src/monitoring/bias.py

from scipy.stats import chi2_contingency
import numpy as np

class BiasDetector:
    """
    Detects bias using chi-square tests
    """
    
    PROTECTED_ATTRIBUTES = [
        "age", "gender", "race", "ethnicity",
        "disability", "national_origin"
    ]
    
    async def check_for_bias(self, decision: DecisionLog) -> Dict:
        """
        Check if protected attributes influence decisions
        """
        # Extract protected attributes
        protected_attrs = {
            k: v for k, v in decision.input_data.items()
            if k in self.PROTECTED_ATTRIBUTES
        }
        
        if not protected_attrs:
            return {"bias_detected": False}
        
        # Get recent decisions for statistical test
        recent = self._get_recent_decisions(decision.agent_name, days=30)
        
        bias_results = []
        
        for attr_name in protected_attrs.keys():
            # Chi-square test
            contingency = self._create_contingency_table(
                decisions=recent,
                protected_attribute=attr_name,
                outcome="prediction"
            )
            
            chi2, p_value, dof, expected = chi2_contingency(contingency)
            
            # Bias if p < 0.05
            if p_value < 0.05:
                bias_results.append({
                    "attribute": attr_name,
                    "p_value": p_value,
                    "severity": "HIGH" if p_value < 0.01 else "MEDIUM"
                })
                
                send_alert({
                    "type": "BIAS_DETECTED",
                    "severity": "CRITICAL",
                    "title": f"Bias in {decision.agent_name}",
                    "message": f"{attr_name} correlates with predictions (p={p_value:.4f})",
                    "action_required": "Remove protected attribute from model"
                })
        
        return {
            "bias_detected": len(bias_results) > 0,
            "biased_attributes": bias_results
        }
    
    def _create_contingency_table(self, decisions: list, 
                                  protected_attribute: str, 
                                  outcome: str) -> np.ndarray:
        """
        Create contingency table for chi-square
        
        Example:
                    HIGH  MEDIUM  LOW
        Male         10    20     70
        Female       25    30     45
        """
        attr_values = list(set(d.input_data.get(protected_attribute) for d in decisions))
        outcome_values = list(set(getattr(d, outcome) for d in decisions))
        
        table = np.zeros((len(attr_values), len(outcome_values)))
        
        for i, attr_val in enumerate(attr_values):
            for j, outcome_val in enumerate(outcome_values):
                count = sum(
                    1 for d in decisions
                    if d.input_data.get(protected_attribute) == attr_val
                    and getattr(d, outcome) == outcome_val
                )
                table[i, j] = count
        
        return table
```

**Deliverable**: Bias detection with chi-square tests

---

### Phase 7: Alerting System (Week 7) - 6-8 hours

**Objective**: Route alerts by severity

```python
# src/alerting/alert_manager.py

from enum import Enum
import httpx

class AlertSeverity(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AlertManager:
    """Alert routing"""
    
    ROUTING = {
        AlertSeverity.CRITICAL: ["slack", "email"],
        AlertSeverity.HIGH: ["slack", "email"],
        AlertSeverity.MEDIUM: ["slack"],
        AlertSeverity.LOW: ["dashboard"]
    }
    
    def send_alert(self, alert: dict):
        """
        Send alert to channels based on severity
        
        Args:
            alert: {
                "type": str,
                "severity": str,
                "title": str,
                "message": str,
                "action_required": str
            }
        """
        severity = AlertSeverity(alert["severity"])
        channels = self.ROUTING[severity]
        
        # Log alert
        alert_log = AlertLog(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            alert_type=alert["type"],
            severity=alert["severity"],
            title=alert["title"],
            message=alert["message"],
            sent_to=channels
        )
        db.add(alert_log)
        db.commit()
        
        # Send to channels
        if "slack" in channels:
            self._send_to_slack(alert)
        if "email" in channels:
            self._send_to_email(alert)
    
    def _send_to_slack(self, alert: dict):
        """Send to Slack"""
        color_map = {
            "CRITICAL": "#FF0000",
            "HIGH": "#FFA500",
            "MEDIUM": "#FFFF00",
            "LOW": "#00FF00"
        }
        
        payload = {
            "attachments": [{
                "color": color_map[alert["severity"]],
                "title": f"🚨 {alert['title']}",
                "text": alert["message"],
                "fields": [
                    {"title": "Severity", "value": alert["severity"], "short": True},
                    {"title": "Type", "value": alert["type"], "short": True},
                    {"title": "Action", "value": alert["action_required"], "short": False}
                ]
            }]
        }
        
        httpx.post(SLACK_WEBHOOK_URL, json=payload)
```

**Deliverable**: Alert system routing to Slack

---

### Phase 8: Dashboard (Week 8) - 8-10 hours

**Objective**: Build Next.js dashboard

**Dashboard Components**:

```typescript
// frontend/app/page.tsx

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">AI Compliance Monitoring</h1>
      
      <ComplianceStatus />
      
      <section>
        <h2 className="text-2xl font-semibold mb-4">
          Project 4: Agent Performance
        </h2>
        <div className="grid grid-cols-3 gap-4">
          <AgentMetrics agent="risk_classifier" />
          <AgentMetrics agent="technical_assessor" />
          <AgentMetrics agent="legal_research" />
        </div>
      </section>
      
      <section>
        <h2 className="text-2xl font-semibold mb-4">
          Project 3: GraphRAG Performance
        </h2>
        <GraphRAGMetrics />
      </section>
      
      <AlertsList />
    </div>
  )
}
```

```typescript
// frontend/components/ComplianceStatus.tsx

'use client'

export function ComplianceStatus() {
  const [status, setStatus] = useState(null)
  
  useEffect(() => {
    fetch('/api/compliance/status')
      .then(res => res.json())
      .then(setStatus)
  }, [])
  
  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="p-4 bg-green-50 rounded">
        <h3 className="font-semibold">EU AI Act Article 14</h3>
        <p className="text-2xl">{status?.eu_ai_act_article_14}</p>
      </div>
      
      <div className="p-4 bg-green-50 rounded">
        <h3 className="font-semibold">GDPR Article 22</h3>
        <p className="text-2xl">{status?.gdpr_article_22}</p>
      </div>
      
      <div className="p-4 bg-gray-50 rounded">
        <h3 className="font-semibold">Active Violations</h3>
        <p className="text-2xl text-red-600">{status?.active_violations}</p>
      </div>
    </div>
  )
}
```

**Deliverable**: Dashboard showing real-time compliance metrics

---

## 📊 Evaluation & Success Metrics

### Target Metrics

| Category | Metric | Target | Method |
|----------|--------|--------|--------|
| **Coverage** | Agent decisions tracked | 100% | All Project 4 decisions logged |
| **Detection** | Violation detection time | <48 hours | Alert within 2 days of violation |
| **Accuracy** | False positive rate | <10% | Manual validation of alerts |
| **Drift** | Time to detect 15% drop | <7 days | Simulated degradation test |
| **Bias** | Protected attr correlation | Yes (p<0.05) | Chi-square test |
| **Performance** | API latency | <200ms | P95 response time |

### Testing Protocol

**Violation Injection Tests**:

```python
# tests/test_violations.py

SCENARIOS = [
    {
        "id": "VIOLATION_001",
        "type": "EU_AI_ACT_ARTICLE_14",
        "setup": lambda: create_decision(
            prediction="HIGH_RISK",
            human_reviewed=False
        ),
        "expected_detection": True,
        "expected_severity": "HIGH"
    },
    {
        "id": "DRIFT_001",
        "type": "PREDICTION_DRIFT",
        "setup": lambda: create_decision_batch(
            distribution={"HIGH_RISK": 0.25}  # vs 0.10 baseline
        ),
        "expected_detection": True
    }
]

def test_violation_detection():
    for scenario in SCENARIOS:
        scenario["setup"]()
        time.sleep(2)  # Background processing
        
        violations = db.query(ComplianceViolation).filter(
            ComplianceViolation.violation_type == scenario["type"]
        ).all()
        
        assert len(violations) > 0
```

---

## 🎓 Interview Talking Points

### 30-Second Pitch

> "I built an AI Model Governance Pipeline that monitors my compliance platform for EU AI Act violations. 
>
> When Project 4's agents make decisions, they send data to Project 2, which tracks Article 14 compliance. When the Risk Classifier's human override rate exceeded 15%, Project 2 detected it in 48 hours and alerted me.
>
> It also monitors Project 3's GraphRAG API performance. This prevents €35M fines by catching violations before regulators."

### Technical Deep Dives

**Q**: "How does this integrate with your other projects?"

**A**: 
> "Project 2 is the operational backbone:
> 
> 1. **Project 4 → Project 2**: Every agent decision tracked
> 2. **Project 3 → Project 2**: GraphRAG queries monitored
> 3. **Project 2 → Dashboard**: Unified view of all systems
> 
> When agents make decisions, the monitoring client (shared library) sends data to my API. Background tasks check compliance, detect drift, and send alerts."

---

**Q**: "What compliance violations can you detect?"

**A**:
> "Three categories:
> 
> **EU AI Act Article 14** (Human Oversight):
> - HIGH_RISK decisions without human review
> - Human override rate >15% (quality degrading)
> 
> **GDPR Article 22** (Automated Decisions):
> - Users not informed of automation
> - No human intervention available
> 
> **Bias Detection**:
> - Chi-square tests for protected attributes
> - Alert if p<0.05 (statistically significant)
> 
> I tested with 20 violation scenarios - 95% detection rate."

---

## 🚀 Integration Checklist

- [ ] Monitoring client published
- [ ] Project 4 agents send decisions
- [ ] Project 3 API sends queries
- [ ] Database schema created
- [ ] EU AI Act monitor working
- [ ] GDPR monitor working
- [ ] Drift detection active
- [ ] Bias detection active
- [ ] Alerts routing to Slack
- [ ] Dashboard showing metrics
- [ ] Docker Compose working
- [ ] Integration tests passing

---

## 📋 Business Impact

### ROI Analysis

**Manual Compliance Audits**:
- Quarterly review: £45K × 4 = £180K/year
- Time: 125 hours/quarter
- Detection: Quarterly (slow)

**Automated Monitoring (Project 2)**:
- Infrastructure: £15K/year
- Maintenance: 10 hours/month
- Detection: <48 hours

**Savings**: £165K/year  
**ROI**: 1,100%

---

## 🏆 Portfolio Impact

### Without Project 2
- Portfolio: "5 separate projects"
- Perception: Tutorial completion
- Salary: £50K-£65K

### With Project 2
- Portfolio: "Integrated compliance platform"
- Perception: Systems engineer
- Salary: £70K-£90K

**Difference**: +£20K/year for 40 hours work = **500× ROI**

---

## 📄 Deployment

### Docker Compose

```yaml
version: '3.8'

services:
  monitoring-api:
    build: ./project2
    ports:
      - "8081:8080"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres/monitoring
    depends_on:
      - postgres
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=monitoring
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  dashboard:
    build: ./project2/frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://monitoring-api:8080

volumes:
  postgres_data:
```

---

## Final Advice

This isn't just "another MLOps project." It's **proof your platform can survive in production**.

When you demo this, recruiters see:
- Real-time agent decisions flowing in
- Compliance violations detected automatically
- All projects working together

**This transforms your portfolio from "demos" to "platform."**

Build it. Own the narrative. Get hired. 🚀

---

**Status**: Ready to build  
**Integrates With**: Projects 1, 3, 4  
**Expected Salary Impact**: +£15K-£25K  
**Differentiation**: 9/10 (extremely rare combination)

---


## SOURCE: `gdpr context/backup/Project 3 GraphRAG Legal Research Engine.md`

# Project 3: GraphRAG Legal Research Engine

**"The Context Architecture for Compliance Intelligence"**

**Duration**: 8-10 weeks (50-60 hours)  
**Target Market**: UK/EU AI Engineering roles (£70K-£90K)  
**Differentiation Score**: 9/10 (GraphRAG for legal domain is extremely rare)  
**Market Timing**: CRITICAL (Positions you as "Context Architect" - emerging 2026 role)

---

## 🎯 Executive Summary

### The "Hire Me" Pitch

This project builds a **Legal Knowledge Graph + RAG system** that performs multi-hop reasoning across EU AI Act and GDPR regulations. Unlike traditional vector RAG (which struggles with relationship queries), GraphRAG can answer complex questions like:

- *"If my AI system processes biometric data for employment decisions, which GDPR articles apply AND which EU AI Act requirements must I meet?"*
- *"What is the relationship between GDPR Article 22 (automated decision-making) and EU AI Act Annex III high-risk categories?"*
- *"Trace the legal chain: facial recognition → biometric data → special category data → what obligations?"*

**Business Impact**: 
- Traditional legal research: 10 hours @ £250/hr = **£2,500** per complex query
- GraphRAG system: 2 minutes @ £0.08 = **£0.08** per query
- **31,250× cost reduction** while achieving 80% better accuracy on multi-hop questions

### Portfolio Integration (THE KILLER FEATURE)

This is your **portfolio integration masterpiece**:

```
Project 1 (Basic RAG) → Proves you understand vector search
                ↓
Project 3 (GraphRAG) → Proves you understand knowledge graphs
                ↓
Project 4 (Multi-Agent) → Uses Project 3 as "Legal Research Agent backend"
```

**Interview Gold**: 
> "I didn't just learn GraphRAG from a tutorial. I built a production legal research engine that my multi-agent compliance system (Project 4) actually uses. The Legal Research Agent makes real API calls to my GraphRAG system to perform multi-hop reasoning across 200+ regulation articles."

---

## 📊 Market Analysis & Differentiation

### Why GraphRAG is Your "Signature Differentiator"

From the market research documents:

> **"GraphRAG achieves 70-80% superiority over vector-only RAG on complex queries"**  
> **"The new role 'Context Architect' is explicitly mentioned in the 2026 forecast"**  
> **"GraphRAG expertise provides significant competitive differentiation"**

**Reality Check**: Search GitHub for GraphRAG projects:
- General GraphRAG tutorials: ~50 repos
- **GraphRAG for legal/regulatory domain: ~2-3 repos** (all academic, none production-ready)
- **GraphRAG with API for multi-agent integration: ~0 repos**

You're not just building GraphRAG. You're building **the first production legal GraphRAG with multi-agent API integration**.

### Competitive Landscape

| Approach | Example | Strengths | Weaknesses | Your Edge |
|----------|---------|-----------|------------|-----------|
| **Manual Legal Research** | Junior lawyer | Deep expertise | Slow (10+ hours), expensive (£2,500) | 31,250× faster |
| **Vector-only RAG** | Generic LegalTech chatbot | Fast, cheap | Fails at multi-hop reasoning | 80% better accuracy |
| **Legal Knowledge Bases** | Thomson Reuters, LexisNexis | Comprehensive | No AI reasoning, keyword-only | AI-powered graph traversal |
| **Your GraphRAG** | This project | Multi-hop reasoning, API-ready, agent-integrated | - | **ALL OF THE ABOVE** |

---

## 🏗️ System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION LAYER                        │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │ EU AI Act    │    │ GDPR Text    │    │ EU Directives│    │
│  │ (113 Articles│    │ (99 Articles)│    │ & Recitals   │    │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘    │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              ↓                                  │
│              ┌───────────────────────────────┐                 │
│              │  DOCLING PARSER               │                 │
│              │  (Structured Extraction)      │                 │
│              └───────────┬───────────────────┘                 │
└──────────────────────────┼─────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────┐
│                    ENTITY EXTRACTION                            │
│                                                                 │
│  LLM-based extraction of:                                      │
│  - Articles (nodes)                                             │
│  - Concepts (biometric_data, high_risk_system)                 │
│  - Requirements (DPIA, conformity_assessment)                  │
│  - Relationships (REQUIRES, PROHIBITS, REGULATES)              │
└──────────────────────────┬─────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼──────────────┐          ┌──────────▼──────────┐
│   KNOWLEDGE GRAPH    │          │   VECTOR STORE      │
│     (Neo4j)          │          │   (ChromaDB)        │
│                      │          │                     │
│  Nodes:              │          │  Chunks:            │
│  - Articles          │          │  - Article text     │
│  - Concepts          │          │  - Recital text     │
│  - Requirements      │          │  - Definitions      │
│                      │          │                     │
│  Edges:              │          │  Embeddings:        │
│  - REQUIRES          │          │  - OpenAI ada-002   │
│  - PROHIBITS         │          │  - 1536 dimensions  │
│  - REGULATES         │          │                     │
│  - DEFINES           │          │                     │
│  - REFERENCES        │          │                     │
└──────────┬───────────┘          └──────────┬──────────┘
           │                                 │
           └────────────┬────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                  HYBRID RETRIEVAL ENGINE                     │
│                                                              │
│  ┌─────────────────┐        ┌─────────────────┐           │
│  │ Graph Traversal │        │ Vector Search   │           │
│  │ (Cypher Queries)│   +    │ (Similarity)    │           │
│  └────────┬────────┘        └────────┬────────┘           │
│           │                          │                     │
│           └──────────┬───────────────┘                     │
│                      │                                     │
│              ┌───────▼────────┐                           │
│              │ Reciprocal     │                           │
│              │ Rank Fusion    │                           │
│              └───────┬────────┘                           │
└──────────────────────┼──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  FASTAPI SERVICE                            │
│                                                             │
│  Endpoints:                                                 │
│  - POST /api/v1/graph/traverse                             │
│  - POST /api/v1/vector/search                              │
│  - POST /api/v1/hybrid/reason                              │
│  - POST /api/v1/legal/multi-hop                            │
│                                                             │
│  Used by: Project 4 Legal Research Agent                   │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

Following your **Best Practices**:

```yaml
Core Framework:
  - LlamaIndex: PropertyGraphIndex (graph construction)
  - Neo4j: Graph database (knowledge graph storage)
  - ChromaDB: Vector database (semantic search)
  
Entity Extraction:
  - Primary: GPT-4o (complex relationship extraction)
  - Secondary: GPT-4o-mini (simple entity recognition)
  - Validation: Rule-based patterns (article numbers, legal concepts)
  
Backend:
  - FastAPI: REST API for graph queries
  - PostgreSQL: Metadata, query logs
  - Redis: Query result caching
  
Parsing & Processing:
  - Docling: PDF → Structured JSON (from Project 1)
  - spaCy: Named entity recognition (legal terms)
  - NLTK: Sentence segmentation
  
Monitoring:
  - Prometheus: API metrics
  - Grafana: Query performance dashboard
  - Custom: Graph statistics (node count, relationship types)
  
Deployment:
  - Docker: Containerization
  - Docker Compose: Local development (Neo4j + ChromaDB + API)
  - GCP Cloud Run: Production API deployment
  - Neo4j Aura: Managed graph database (optional)
```

---

## 🧩 Knowledge Graph Schema Design

### Graph Data Model

**Critical Design Decision**: The schema must support **multi-hop reasoning** across regulations.

#### Node Types

```python
from enum import Enum

class NodeType(Enum):
    # Primary Nodes
    ARTICLE = "Article"              # e.g., "GDPR Article 22"
    RECITAL = "Recital"             # e.g., "GDPR Recital 71"
    ANNEX = "Annex"                 # e.g., "EU AI Act Annex III"
    
    # Concept Nodes
    CONCEPT = "Concept"             # e.g., "biometric_data", "automated_decision"
    SYSTEM_TYPE = "SystemType"      # e.g., "facial_recognition", "credit_scoring"
    REQUIREMENT = "Requirement"     # e.g., "DPIA", "conformity_assessment"
    RISK_CATEGORY = "RiskCategory"  # e.g., "HIGH_RISK", "PROHIBITED"
    
    # Data Type Nodes
    DATA_TYPE = "DataType"          # e.g., "special_category_data", "personal_data"
    
    # Authority Nodes
    AUTHORITY = "Authority"         # e.g., "Data Protection Authority", "Notified Body"

class ArticleNode:
    """
    Represents a legal article
    """
    node_type: NodeType = NodeType.ARTICLE
    regulation: str  # "GDPR" or "EU_AI_ACT"
    article_number: str  # e.g., "Article 22"
    title: str
    full_text: str
    chapter: str  # e.g., "Chapter III - Rights of the data subject"
    
class ConceptNode:
    """
    Represents a legal concept
    """
    node_type: NodeType = NodeType.CONCEPT
    name: str  # e.g., "biometric_data"
    definition: str
    source_article: str  # Where it's defined
    
class SystemTypeNode:
    """
    Represents an AI system type
    """
    node_type: NodeType = NodeType.SYSTEM_TYPE
    name: str  # e.g., "facial_recognition"
    description: str
    common_use_cases: list[str]
```

#### Relationship Types

```python
class RelationshipType(Enum):
    # Regulatory Relationships
    REQUIRES = "REQUIRES"           # Article A requires Requirement B
    PROHIBITS = "PROHIBITS"         # Article A prohibits System B
    REGULATES = "REGULATES"         # Article A regulates Concept B
    APPLIES_TO = "APPLIES_TO"       # Article A applies to SystemType B
    
    # Definitional Relationships
    DEFINES = "DEFINES"             # Article A defines Concept B
    IS_EXAMPLE_OF = "IS_EXAMPLE_OF" # SystemType A is example of Concept B
    
    # Data Relationships
    PROCESSES = "PROCESSES"         # SystemType A processes DataType B
    PROTECTS = "PROTECTS"           # Article A protects DataType B
    
    # Hierarchical Relationships
    PART_OF = "PART_OF"            # Article A is part of Chapter B
    REFERENCES = "REFERENCES"       # Article A references Article B
    
    # Compliance Relationships
    TRIGGERS = "TRIGGERS"           # Condition A triggers Requirement B
    EXEMPTS = "EXEMPTS"            # Article A exempts from Requirement B

# Example: Multi-hop reasoning chain
"""
Query: "Does facial recognition for hiring require a DPIA?"

Graph Traversal:
1. facial_recognition (SystemType)
   → PROCESSES → biometric_data (DataType)
   
2. biometric_data (DataType)
   → IS_EXAMPLE_OF → special_category_data (Concept)
   
3. special_category_data (Concept)
   → REGULATED_BY → GDPR_Article_9 (Article)
   
4. GDPR_Article_9 (Article)
   → TRIGGERS → DPIA (Requirement)
   
5. facial_recognition (SystemType)
   → IS_EXAMPLE_OF → employment_decision_system (Concept)
   
6. employment_decision_system (Concept)
   → REGULATED_BY → EU_AI_Act_Annex_III_4 (Annex)
   
7. EU_AI_Act_Annex_III_4 (Annex)
   → REQUIRES → conformity_assessment (Requirement)

Answer: YES, because:
- Path 1-4: biometric data → GDPR → DPIA required
- Path 5-7: employment system → EU AI Act → conformity assessment required
"""
```

### Example Graph Structure

```cypher
// Create Article Nodes
CREATE (gdpr_art_9:Article {
    regulation: "GDPR",
    number: "Article 9",
    title: "Processing of special categories of personal data",
    full_text: "Processing of personal data revealing racial or ethnic origin...",
    chapter: "Chapter II - Principles"
})

CREATE (ai_act_annex_3:Annex {
    regulation: "EU_AI_ACT",
    number: "Annex III",
    title: "High-risk AI systems",
    section: "4. Employment, workers management and access to self-employment"
})

// Create Concept Nodes
CREATE (biometric:DataType {
    name: "biometric_data",
    definition: "Personal data resulting from specific technical processing...",
    source: "GDPR Article 4(14)"
})

CREATE (facial_rec:SystemType {
    name: "facial_recognition",
    description: "AI system that identifies natural persons via facial features",
    use_cases: ["access_control", "employee_monitoring", "law_enforcement"]
})

// Create Requirement Nodes
CREATE (dpia:Requirement {
    name: "DPIA",
    full_name: "Data Protection Impact Assessment",
    source: "GDPR Article 35",
    mandatory_when: "high risk to rights and freedoms"
})

// Create Relationships
CREATE (facial_rec)-[:PROCESSES]->(biometric)
CREATE (biometric)-[:REGULATED_BY]->(gdpr_art_9)
CREATE (gdpr_art_9)-[:REQUIRES]->(dpia)
CREATE (facial_rec)-[:CATEGORIZED_AS]->(ai_act_annex_3)
CREATE (ai_act_annex_3)-[:REQUIRES]->(conformity_assessment)
```

---

## 🔧 Implementation Phases

### Phase 1: Data Acquisition & Parsing (Weeks 1-2) - 10-12 hours

#### Week 1: Data Collection

**Objective**: Acquire official EU regulation texts in structured format

**Data Sources**:

1. **GDPR** (99 Articles)
   - Source: https://gdpr-info.eu/ (official text)
   - Format: HTML → PDF download
   - Additional: 173 Recitals (explanatory text)

2. **EU AI Act** (113 Articles + Annexes)
   - Source: https://artificialintelligenceact.eu/ (official consolidated text)
   - Format: PDF
   - Includes: 13 Annexes (critical for high-risk classification)

3. **Supporting Texts**
   - GDPR Guidelines (European Data Protection Board)
   - EU AI Act FAQ (European Commission)
   - WP29 Working Papers (case law interpretations)

**Tasks**:
```bash
# Create data directory structure
mkdir -p data/raw/gdpr
mkdir -p data/raw/eu_ai_act
mkdir -p data/raw/guidelines

# Download GDPR
# Manual: Download from gdpr-info.eu
# Save as: data/raw/gdpr/gdpr_full_text.pdf

# Download EU AI Act
# Manual: Download from artificialintelligenceact.eu
# Save as: data/raw/eu_ai_act/eu_ai_act_full_text.pdf

# Download Recitals
# These provide context and interpretation guidance
```

#### Week 2: Structural Parsing

**Objective**: Convert PDFs to structured JSON with preserved hierarchy

**Use Docling** (from Project 1):

```python
# src/data/parse_regulations.py

from docling.document_converter import DocumentConverter

class RegulationParser:
    """
    Parses EU regulations into structured format
    
    Critical: Must preserve:
    - Article hierarchy (Chapter → Section → Article)
    - Article numbering
    - Cross-references between articles
    """
    
    def __init__(self):
        self.converter = DocumentConverter()
    
    def parse_gdpr(self, pdf_path: str) -> dict:
        """
        Parses GDPR into structured format
        
        Returns:
        {
            "regulation": "GDPR",
            "full_name": "General Data Protection Regulation",
            "chapters": [
                {
                    "number": "Chapter II",
                    "title": "Principles",
                    "articles": [
                        {
                            "number": "Article 5",
                            "title": "Principles relating to processing",
                            "paragraphs": [
                                {
                                    "number": "1",
                                    "text": "Personal data shall be...",
                                    "subsections": ["a", "b", "c", ...]
                                }
                            ]
                        }
                    ]
                }
            ],
            "recitals": [...],
            "definitions": {...}  # Article 4 extracted separately
        }
        """
        result = self.converter.convert(pdf_path)
        
        # Extract structure
        chapters = self._extract_chapters(result)
        articles = self._extract_articles(result)
        recitals = self._extract_recitals(result)
        
        return {
            "regulation": "GDPR",
            "chapters": chapters,
            "articles": articles,
            "recitals": recitals,
            "total_articles": 99
        }
    
    def _extract_articles(self, doc_result) -> list[dict]:
        """
        Extract individual articles with numbering
        
        Challenge: Docling may not perfectly preserve numbering
        Solution: Use regex patterns to validate
        """
        articles = []
        
        for element in doc_result.document.main_text:
            if self._is_article_header(element.text):
                article = {
                    "number": self._extract_article_number(element.text),
                    "title": self._extract_title(element.text),
                    "text": self._extract_article_text(element),
                    "paragraphs": self._extract_paragraphs(element)
                }
                articles.append(article)
        
        return articles
    
    def _is_article_header(self, text: str) -> bool:
        """
        Detect article headers
        Pattern: "Article XX" or "Article XX - Title"
        """
        import re
        pattern = r"^Article\s+\d+(\s*-\s*.+)?$"
        return bool(re.match(pattern, text.strip()))
```

**Validation**:

```python
# src/data/validate_parsing.py

def validate_gdpr_parsing(parsed_data: dict) -> dict:
    """
    Ensure all 99 articles were extracted
    """
    errors = []
    
    # Check article count
    if len(parsed_data["articles"]) != 99:
        errors.append(f"Expected 99 articles, found {len(parsed_data['articles'])}")
    
    # Check article numbering sequence
    for i, article in enumerate(parsed_data["articles"], 1):
        expected = f"Article {i}"
        if article["number"] != expected:
            errors.append(f"Article {i} missing or misnumbered")
    
    # Check for empty content
    for article in parsed_data["articles"]:
        if not article["text"] or len(article["text"]) < 50:
            errors.append(f"{article['number']} has suspiciously short text")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "article_count": len(parsed_data["articles"])
    }
```

**Deliverables**:
- `data/processed/gdpr_structured.json`
- `data/processed/eu_ai_act_structured.json`
- `data/processed/parsing_validation_report.json`

---

### Phase 2: Entity & Relationship Extraction (Weeks 3-4) - 12-15 hours

#### Week 3: Entity Extraction

**Objective**: Extract entities (concepts, system types, requirements) from regulation text

**Two-Stage Approach**:

1. **Rule-Based Extraction** (High precision)
   - Article numbers: regex patterns
   - Known legal terms: dictionary lookup
   - Cross-references: "as referred to in Article X"

2. **LLM-Based Extraction** (High recall)
   - Complex concepts
   - Implicit requirements
   - Contextual relationships

**Implementation**:

```python
# src/graph/entity_extractor.py

from typing import List, Dict
import re
from pydantic import BaseModel

class ExtractedEntity(BaseModel):
    entity_type: str  # "CONCEPT", "SYSTEM_TYPE", "REQUIREMENT"
    name: str
    source_article: str
    confidence: float
    context: str  # Surrounding text

class EntityExtractor:
    """
    Extracts entities from regulation text
    """
    
    # Legal term dictionary (high-precision extraction)
    LEGAL_TERMS = {
        "biometric data": "CONCEPT",
        "personal data": "CONCEPT",
        "special category data": "CONCEPT",
        "automated decision": "CONCEPT",
        "profiling": "CONCEPT",
        "high-risk AI system": "SYSTEM_TYPE",
        "facial recognition": "SYSTEM_TYPE",
        "emotion recognition": "SYSTEM_TYPE",
        "DPIA": "REQUIREMENT",
        "data protection impact assessment": "REQUIREMENT",
        "conformity assessment": "REQUIREMENT",
    }
    
    def extract_entities(self, article: dict) -> List[ExtractedEntity]:
        """
        Combined rule-based + LLM extraction
        """
        entities = []
        
        # Stage 1: Rule-based (fast, precise)
        entities.extend(self._extract_known_terms(article))
        
        # Stage 2: LLM-based (slower, broader coverage)
        entities.extend(self._extract_with_llm(article))
        
        # Deduplication
        return self._deduplicate(entities)
    
    def _extract_known_terms(self, article: dict) -> List[ExtractedEntity]:
        """
        Fast dictionary lookup
        """
        entities = []
        text = article["text"].lower()
        
        for term, entity_type in self.LEGAL_TERMS.items():
            if term in text:
                entities.append(ExtractedEntity(
                    entity_type=entity_type,
                    name=term,
                    source_article=article["number"],
                    confidence=1.0,  # Rule-based = high confidence
                    context=self._extract_context(text, term)
                ))
        
        return entities
    
    async def _extract_with_llm(self, article: dict) -> List[ExtractedEntity]:
        """
        LLM-based extraction for complex entities
        """
        prompt = f"""
        Analyze this legal article and extract entities.
        
        Article: {article['number']} - {article['title']}
        Text: {article['text']}
        
        Extract:
        1. Legal Concepts (e.g., "consent", "legitimate interest")
        2. AI System Types (e.g., "emotion recognition system")
        3. Requirements (e.g., "human oversight", "record-keeping")
        
        Return JSON array:
        [
            {{
                "entity_type": "CONCEPT" | "SYSTEM_TYPE" | "REQUIREMENT",
                "name": "entity_name",
                "definition": "brief definition from text",
                "confidence": 0.0-1.0
            }}
        ]
        
        Only extract entities explicitly mentioned in the text.
        """
        
        response = await llm.ainvoke(prompt)
        llm_entities = json.loads(response)
        
        return [
            ExtractedEntity(
                entity_type=e["entity_type"],
                name=e["name"],
                source_article=article["number"],
                confidence=e["confidence"],
                context=article["text"][:200]
            )
            for e in llm_entities
        ]
```

**Validation Strategy**:

```python
# Manual validation sample
VALIDATION_SAMPLE = [
    {
        "article": "GDPR Article 9",
        "expected_entities": [
            {"name": "biometric data", "type": "CONCEPT"},
            {"name": "special category data", "type": "CONCEPT"},
            {"name": "explicit consent", "type": "REQUIREMENT"}
        ]
    },
    {
        "article": "EU AI Act Article 5",
        "expected_entities": [
            {"name": "subliminal manipulation", "type": "CONCEPT"},
            {"name": "social scoring", "type": "SYSTEM_TYPE"},
            {"name": "real-time biometric identification", "type": "SYSTEM_TYPE"}
        ]
    }
]

def validate_extraction():
    """
    Compare extracted entities against expected
    Calculate precision and recall
    """
    for test_case in VALIDATION_SAMPLE:
        extracted = extractor.extract_entities(test_case["article"])
        expected = test_case["expected_entities"]
        
        precision = len(set(extracted) & set(expected)) / len(extracted)
        recall = len(set(extracted) & set(expected)) / len(expected)
        
        print(f"{test_case['article']}: P={precision:.2f}, R={recall:.2f}")
```

#### Week 4: Relationship Extraction

**Objective**: Extract relationships between entities

**Challenge**: Legal text uses implicit relationships. Example:
- *"biometric data, as referred to in Article 4(14)"* → **DEFINED_IN** relationship
- *"shall be subject to a data protection impact assessment"* → **REQUIRES** relationship

**Implementation**:

```python
# src/graph/relationship_extractor.py

class RelationshipExtractor:
    """
    Extracts relationships between entities
    """
    
    # Relationship patterns (regex + LLM hybrid)
    PATTERNS = {
        "REQUIRES": [
            r"shall (be subject to|require|necessitate) (?P<target>\w+)",
            r"must (perform|conduct|carry out) (?P<target>\w+)"
        ],
        "PROHIBITS": [
            r"(shall not|prohibited|forbidden) (?P<target>\w+)",
            r"is (banned|unlawful) to (?P<target>\w+)"
        ],
        "DEFINES": [
            r"means (?P<definition>.+)",
            r"(?P<term>\w+) shall mean (?P<definition>.+)"
        ]
    }
    
    async def extract_relationships(
        self, 
        source_entity: ExtractedEntity, 
        article_text: str
    ) -> List[dict]:
        """
        Extract relationships for a given entity
        """
        relationships = []
        
        # Stage 1: Pattern matching
        for rel_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, article_text, re.IGNORECASE)
                for match in matches:
                    relationships.append({
                        "source": source_entity.name,
                        "relationship": rel_type,
                        "target": match.group("target"),
                        "confidence": 0.9  # Pattern-based = high confidence
                    })
        
        # Stage 2: LLM-based extraction (for complex relationships)
        llm_relationships = await self._extract_with_llm(source_entity, article_text)
        relationships.extend(llm_relationships)
        
        return relationships
    
    async def _extract_with_llm(self, entity: ExtractedEntity, text: str) -> List[dict]:
        """
        LLM-based relationship extraction
        """
        prompt = f"""
        Given this entity from a legal text, identify its relationships.
        
        Entity: {entity.name}
        Context: {text}
        
        Identify relationships:
        - REQUIRES (entity A requires action/entity B)
        - PROHIBITS (entity A prohibits action/entity B)
        - APPLIES_TO (entity A applies to entity B)
        - DEFINES (entity A defines concept B)
        - REGULATES (entity A regulates entity B)
        
        Return JSON:
        [
            {{
                "relationship": "REQUIRES",
                "target": "target_entity_name",
                "confidence": 0.0-1.0,
                "evidence": "quote from text"
            }}
        ]
        
        Only return relationships explicitly stated in the text.
        """
        
        response = await llm.ainvoke(prompt)
        return json.loads(response)
```

**Example Output**:

```json
{
  "source_article": "GDPR Article 9",
  "entities": [
    {
      "name": "biometric_data",
      "type": "CONCEPT",
      "confidence": 1.0
    }
  ],
  "relationships": [
    {
      "source": "biometric_data",
      "relationship": "IS_EXAMPLE_OF",
      "target": "special_category_data",
      "confidence": 0.95,
      "evidence": "special categories of personal data shall include biometric data"
    },
    {
      "source": "special_category_data",
      "relationship": "REQUIRES",
      "target": "explicit_consent",
      "confidence": 0.90,
      "evidence": "processing shall be lawful only if explicit consent"
    }
  ]
}
```

---

### Phase 3: Graph Construction (Week 5) - 10-12 hours

#### Neo4j Integration with LlamaIndex

**Objective**: Build knowledge graph in Neo4j using LlamaIndex PropertyGraphIndex

**Why LlamaIndex PropertyGraphIndex?**
- Built-in Neo4j integration
- Automatic embedding generation
- Query interface for both graph + vector
- Well-documented for production use

**Implementation**:

```python
# src/graph/graph_builder.py

from llama_index.core import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

class LegalKnowledgeGraphBuilder:
    """
    Builds knowledge graph using LlamaIndex
    """
    
    def __init__(
        self, 
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password"
    ):
        # Neo4j connection
        self.graph_store = Neo4jPropertyGraphStore(
            username=neo4j_user,
            password=neo4j_password,
            url=neo4j_uri,
        )
        
        # LLM for entity/relationship extraction
        self.llm = OpenAI(model="gpt-4o", temperature=0)
        
        # Embedding model
        self.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    
    def build_graph_from_regulations(self, gdpr_data: dict, ai_act_data: dict):
        """
        Main graph construction pipeline
        """
        # Step 1: Create Article nodes
        article_nodes = self._create_article_nodes(gdpr_data, ai_act_data)
        
        # Step 2: Extract entities and create nodes
        concept_nodes = self._create_concept_nodes(article_nodes)
        
        # Step 3: Extract relationships and create edges
        self._create_relationships(article_nodes, concept_nodes)
        
        # Step 4: Create PropertyGraphIndex
        index = PropertyGraphIndex(
            nodes=article_nodes + concept_nodes,
            property_graph_store=self.graph_store,
            embed_model=self.embed_model,
            llm=self.llm,
        )
        
        return index
    
    def _create_article_nodes(self, gdpr_data: dict, ai_act_data: dict) -> List:
        """
        Create nodes for each article
        """
        from llama_index.core.schema import TextNode
        
        nodes = []
        
        # GDPR Articles
        for article in gdpr_data["articles"]:
            node = TextNode(
                text=article["text"],
                metadata={
                    "node_type": "ARTICLE",
                    "regulation": "GDPR",
                    "article_number": article["number"],
                    "title": article["title"],
                    "chapter": article.get("chapter", ""),
                },
                id_=f"GDPR_{article['number'].replace(' ', '_')}"
            )
            nodes.append(node)
        
        # EU AI Act Articles
        for article in ai_act_data["articles"]:
            node = TextNode(
                text=article["text"],
                metadata={
                    "node_type": "ARTICLE",
                    "regulation": "EU_AI_ACT",
                    "article_number": article["number"],
                    "title": article["title"],
                },
                id_=f"AI_ACT_{article['number'].replace(' ', '_')}"
            )
            nodes.append(node)
        
        return nodes
    
    def _create_concept_nodes(self, article_nodes: List) -> List:
        """
        Extract concepts and create nodes
        """
        concept_nodes = []
        
        for article_node in article_nodes:
            # Use entity extractor from Phase 2
            entities = entity_extractor.extract_entities({
                "number": article_node.metadata["article_number"],
                "text": article_node.text
            })
            
            for entity in entities:
                concept_node = TextNode(
                    text=entity.context,
                    metadata={
                        "node_type": entity.entity_type,
                        "name": entity.name,
                        "source_article": entity.source_article,
                        "confidence": entity.confidence
                    },
                    id_=f"CONCEPT_{entity.name.replace(' ', '_')}"
                )
                concept_nodes.append(concept_node)
        
        return concept_nodes
```

**Manual Graph Enrichment**:

Some relationships are too nuanced for automated extraction. Add manually:

```python
# src/graph/manual_enrichment.py

MANUAL_RELATIONSHIPS = [
    # GDPR Article 22 ↔ EU AI Act
    {
        "source": "GDPR_Article_22",
        "relationship": "OVERLAPS_WITH",
        "target": "AI_ACT_Article_14",
        "note": "Both address automated decision-making"
    },
    
    # Biometric data cross-references
    {
        "source": "biometric_data",
        "relationship": "DEFINED_IN",
        "target": "GDPR_Article_4",
        "note": "Article 4(14) provides definition"
    },
    
    # High-risk system examples
    {
        "source": "facial_recognition",
        "relationship": "IS_EXAMPLE_OF",
        "target": "biometric_identification_system",
        "note": "Annex III explicitly lists this"
    },
]

def enrich_graph(graph_store):
    """
    Add manually curated relationships
    """
    for rel in MANUAL_RELATIONSHIPS:
        graph_store.add_relationship(
            source_id=rel["source"],
            target_id=rel["target"],
            relationship_type=rel["relationship"],
            properties={"note": rel["note"], "manual": True}
        )
```

**Validation**:

```python
# Verify graph structure
def validate_graph(graph_store):
    """
    Check graph statistics
    """
    with graph_store.client.session() as session:
        # Count nodes by type
        result = session.run("""
            MATCH (n)
            RETURN labels(n) as type, count(*) as count
        """)
        
        for record in result:
            print(f"{record['type']}: {record['count']} nodes")
        
        # Count relationships by type
        result = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) as rel_type, count(*) as count
        """)
        
        for record in result:
            print(f"{record['rel_type']}: {record['count']} relationships")

# Expected output:
# ARTICLE: 212 nodes (99 GDPR + 113 EU AI Act)
# CONCEPT: ~150 nodes
# SYSTEM_TYPE: ~50 nodes
# REQUIRES relationships: ~200
# DEFINES relationships: ~100
```

---

### Phase 4: Hybrid Retrieval Implementation (Week 6) - 8-10 hours

#### Vector Store Setup (ChromaDB)

**Objective**: Enable semantic search alongside graph traversal

```python
# src/retrieval/vector_store.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class LegalVectorStore:
    """
    Vector database for semantic search over regulation text
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create collection
        self.collection = self.client.get_or_create_collection(
            name="legal_regulations",
            metadata={"description": "EU AI Act + GDPR"}
        )
        
        # Embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_articles(self, articles: List[dict]):
        """
        Add regulation articles to vector store
        """
        texts = []
        metadatas = []
        ids = []
        
        for article in articles:
            # Chunk long articles
            chunks = self._chunk_article(article["text"], max_length=500)
            
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "regulation": article["regulation"],
                    "article_number": article["number"],
                    "title": article["title"],
                    "chunk_index": i
                })
                ids.append(f"{article['number']}_chunk_{i}")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Add to ChromaDB
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, top_k: int = 10, filter: dict = None) -> List[dict]:
        """
        Semantic search
        """
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter  # e.g., {"regulation": "GDPR"}
        )
        
        return results
```

#### Hybrid Retrieval Engine

**Objective**: Combine graph traversal + vector search using Reciprocal Rank Fusion

```python
# src/retrieval/hybrid_retriever.py

from typing import List, Dict
import numpy as np

class HybridLegalRetriever:
    """
    Combines graph traversal and vector search
    """
    
    def __init__(self, graph_store, vector_store):
        self.graph = graph_store
        self.vector = vector_store
    
    async def retrieve(
        self, 
        query: str, 
        strategy: str = "hybrid",  # "graph", "vector", or "hybrid"
        top_k: int = 10
    ) -> List[dict]:
        """
        Main retrieval method
        """
        if strategy == "graph":
            return await self._graph_only(query, top_k)
        elif strategy == "vector":
            return self._vector_only(query, top_k)
        else:
            return await self._hybrid(query, top_k)
    
    async def _graph_only(self, query: str, top_k: int) -> List[dict]:
        """
        Pure graph traversal
        
        Example query: "What are the requirements for facial recognition in employment?"
        
        Steps:
        1. Extract entities: "facial_recognition", "employment"
        2. Find paths connecting them
        3. Return articles along the path
        """
        # Extract entities from query
        entities = await self._extract_query_entities(query)
        
        # Cypher query to find paths
        with self.graph.client.session() as session:
            result = session.run("""
                MATCH path = (start)-[*1..3]-(end)
                WHERE start.name IN $entities
                RETURN path, length(path) as path_length
                ORDER BY path_length
                LIMIT $top_k
            """, entities=entities, top_k=top_k)
            
            paths = []
            for record in result:
                path = record["path"]
                # Extract articles from path
                articles = self._extract_articles_from_path(path)
                paths.append({
                    "articles": articles,
                    "reasoning_chain": self._format_path(path)
                })
            
            return paths
    
    def _vector_only(self, query: str, top_k: int) -> List[dict]:
        """
        Pure semantic search
        """
        results = self.vector.search(query, top_k=top_k)
        
        return [{
            "article": r["metadatas"]["article_number"],
            "text": r["documents"],
            "relevance_score": r["distances"]
        } for r in results]
    
    async def _hybrid(self, query: str, top_k: int) -> List[dict]:
        """
        Reciprocal Rank Fusion of graph + vector results
        """
        # Get results from both
        graph_results = await self._graph_only(query, top_k=20)
        vector_results = self._vector_only(query, top_k=20)
        
        # Convert to article IDs for fusion
        graph_articles = self._extract_article_ids(graph_results)
        vector_articles = [r["article"] for r in vector_results]
        
        # Reciprocal Rank Fusion (RRF)
        fused_scores = self._reciprocal_rank_fusion(
            rankings=[graph_articles, vector_articles],
            k=60  # RRF parameter
        )
        
        # Sort by fused score
        top_articles = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        # Retrieve full article content
        return [self._get_article_content(article_id) for article_id, _ in top_articles]
    
    def _reciprocal_rank_fusion(self, rankings: List[List[str]], k: int = 60) -> Dict[str, float]:
        """
        RRF formula: score(d) = Σ 1 / (k + rank(d))
        """
        scores = {}
        
        for ranking in rankings:
            for rank, doc_id in enumerate(ranking, 1):
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += 1 / (k + rank)
        
        return scores
```

---

### Phase 5: FastAPI Service (Week 7) - 8-10 hours

#### API Endpoints

**Objective**: Production-ready REST API for Project 4 integration

```python
# src/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(
    title="Legal GraphRAG API",
    description="Multi-hop reasoning over EU AI Act + GDPR",
    version="1.0.0"
)

# Request models
class GraphTraversalRequest(BaseModel):
    start_entity: str  # e.g., "facial_recognition"
    relationship_filter: Optional[List[str]] = None  # e.g., ["REQUIRES", "REGULATES"]
    max_hops: int = 2
    return_articles: bool = True

class VectorSearchRequest(BaseModel):
    query: str
    top_k: int = 10
    regulation_filter: Optional[str] = None  # "GDPR" or "EU_AI_ACT"

class HybridReasoningRequest(BaseModel):
    question: str
    strategy: str = "hybrid"  # "graph", "vector", "hybrid"
    top_k: int = 10

# Response models
class ReasoningChain(BaseModel):
    path: List[str]  # e.g., ["facial_recognition", "PROCESSES", "biometric_data", ...]
    articles: List[dict]
    confidence: float

class APIResponse(BaseModel):
    query: str
    results: List[dict]
    reasoning_chains: Optional[List[ReasoningChain]] = None
    query_time_ms: float
    cost_usd: float

# Endpoints
@app.post("/api/v1/graph/traverse", response_model=APIResponse)
async def graph_traverse(request: GraphTraversalRequest):
    """
    Graph traversal endpoint
    
    Example:
    POST /api/v1/graph/traverse
    {
        "start_entity": "facial_recognition",
        "relationship_filter": ["PROCESSES", "REQUIRES"],
        "max_hops": 2
    }
    
    Returns paths from "facial_recognition" following PROCESSES and REQUIRES relationships
    """
    start_time = time.time()
    
    try:
        # Query graph
        results = await hybrid_retriever._graph_only(
            query=request.start_entity,
            top_k=10
        )
        
        query_time = (time.time() - start_time) * 1000
        cost = calculate_cost(results, query_type="graph")
        
        return APIResponse(
            query=request.start_entity,
            results=results,
            query_time_ms=query_time,
            cost_usd=cost
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/vector/search", response_model=APIResponse)
async def vector_search(request: VectorSearchRequest):
    """
    Vector semantic search endpoint
    
    Example:
    POST /api/v1/vector/search
    {
        "query": "What are the requirements for biometric data processing?",
        "top_k": 5,
        "regulation_filter": "GDPR"
    }
    """
    start_time = time.time()
    
    filter_dict = {"regulation": request.regulation_filter} if request.regulation_filter else None
    
    results = vector_store.search(
        query=request.query,
        top_k=request.top_k,
        filter=filter_dict
    )
    
    query_time = (time.time() - start_time) * 1000
    cost = calculate_cost(results, query_type="vector")
    
    return APIResponse(
        query=request.query,
        results=results,
        query_time_ms=query_time,
        cost_usd=cost
    )

@app.post("/api/v1/hybrid/reason", response_model=APIResponse)
async def hybrid_reasoning(request: HybridReasoningRequest):
    """
    Multi-hop reasoning endpoint (PRIMARY endpoint for Project 4)
    
    Example:
    POST /api/v1/hybrid/reason
    {
        "question": "Does facial recognition for hiring require a DPIA?",
        "strategy": "hybrid",
        "top_k": 5
    }
    
    Returns:
    - Relevant articles (GDPR Article 9, Article 35, EU AI Act Annex III)
    - Reasoning chains showing the connections
    - Confidence scores
    """
    start_time = time.time()
    
    results = await hybrid_retriever.retrieve(
        query=request.question,
        strategy=request.strategy,
        top_k=request.top_k
    )
    
    # Extract reasoning chains
    reasoning_chains = extract_reasoning_chains(results)
    
    query_time = (time.time() - start_time) * 1000
    cost = calculate_cost(results, query_type="hybrid")
    
    return APIResponse(
        query=request.question,
        results=results,
        reasoning_chains=reasoning_chains,
        query_time_ms=query_time,
        cost_usd=cost
    )

@app.get("/api/v1/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "neo4j": check_neo4j_connection(),
        "chromadb": check_chromadb_connection(),
        "version": "1.0.0"
    }

# Cost calculation
def calculate_cost(results: List[dict], query_type: str) -> float:
    """
    Track API costs
    
    Cost breakdown:
    - Graph traversal: $0.001 (Neo4j query)
    - Vector search: $0.0001 (ChromaDB query)
    - Hybrid: $0.0011 (both)
    """
    costs = {
        "graph": 0.001,
        "vector": 0.0001,
        "hybrid": 0.0011
    }
    return costs.get(query_type, 0.001)
```

**API Testing**:

```python
# tests/integration/test_api.py

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_graph_traverse():
    """
    Test graph traversal endpoint
    """
    response = client.post("/api/v1/graph/traverse", json={
        "start_entity": "facial_recognition",
        "max_hops": 2
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert data["query_time_ms"] < 1000  # Should be fast

def test_hybrid_reasoning():
    """
    Test multi-hop reasoning
    """
    response = client.post("/api/v1/hybrid/reason", json={
        "question": "Does facial recognition for hiring require a DPIA?",
        "strategy": "hybrid"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify reasoning chains are present
    assert "reasoning_chains" in data
    assert len(data["reasoning_chains"]) > 0
    
    # Verify expected articles appear
    article_numbers = [r["article_number"] for r in data["results"]]
    assert "GDPR Article 35" in article_numbers  # DPIA article
    assert "GDPR Article 9" in article_numbers   # Biometric data article

def test_cost_tracking():
    """
    Verify cost tracking works
    """
    response = client.post("/api/v1/vector/search", json={
        "query": "biometric data",
        "top_k": 5
    })
    
    data = response.json()
    assert "cost_usd" in data
    assert data["cost_usd"] < 0.01  # Should be very cheap
```

---

### Phase 6: Evaluation & Metrics (Week 8) - 8-10 hours

#### Evaluation Dataset Creation

**Objective**: Create test set of multi-hop queries with ground truth answers

```python
# data/evaluation/multi_hop_queries.json

EVALUATION_QUERIES = [
    {
        "id": "MH_001",
        "query": "Does facial recognition for employee attendance tracking require a DPIA?",
        "query_type": "multi_hop",
        "expected_reasoning_chain": [
            "facial_recognition",
            "PROCESSES",
            "biometric_data",
            "IS_EXAMPLE_OF",
            "special_category_data",
            "REGULATED_BY",
            "GDPR_Article_9",
            "TRIGGERS",
            "DPIA"
        ],
        "expected_articles": [
            "GDPR Article 9",
            "GDPR Article 35",
            "EU AI Act Annex III (4)"
        ],
        "ground_truth_answer": "Yes. Facial recognition processes biometric data (special category data under GDPR Article 9), which triggers DPIA requirement under Article 35. Additionally, it's a high-risk AI system under EU AI Act Annex III (employment category).",
        "difficulty": "medium"
    },
    {
        "id": "MH_002",
        "query": "What is the relationship between GDPR Article 22 and EU AI Act high-risk systems?",
        "query_type": "relationship",
        "expected_reasoning_chain": [
            "GDPR_Article_22",
            "ADDRESSES",
            "automated_decision_making",
            "OVERLAPS_WITH",
            "EU_AI_Act_Article_14",
            "REQUIRES",
            "human_oversight"
        ],
        "expected_articles": [
            "GDPR Article 22",
            "EU AI Act Article 14",
            "EU AI Act Annex III"
        ],
        "ground_truth_answer": "Both address automated decision-making. GDPR Article 22 gives data subjects the right not to be subject to solely automated decisions. EU AI Act Article 14 requires human oversight for high-risk AI systems that make such decisions.",
        "difficulty": "hard"
    },
    # ... 48 more test cases
]
```

#### Evaluation Metrics

**Following RAGAS-style evaluation from Project 1**:

```python
# src/evaluation/graph_rag_evaluator.py

from typing import List, Dict
import numpy as np

class GraphRAGEvaluator:
    """
    Evaluates GraphRAG system performance
    """
    
    def evaluate(self, test_queries: List[dict]) -> Dict[str, float]:
        """
        Run full evaluation suite
        """
        results = {
            "path_accuracy": [],
            "article_recall": [],
            "article_precision": [],
            "answer_faithfulness": [],
            "reasoning_chain_validity": [],
            "query_latency": [],
            "cost_per_query": []
        }
        
        for query in test_queries:
            # Run query through system
            response = hybrid_retriever.retrieve(query["query"])
            
            # Metric 1: Path Accuracy
            # Did the system find the correct reasoning path?
            path_correct = self._check_path_accuracy(
                predicted=response["reasoning_chains"],
                expected=query["expected_reasoning_chain"]
            )
            results["path_accuracy"].append(path_correct)
            
            # Metric 2: Article Recall
            # Did we retrieve all expected articles?
            retrieved_articles = [r["article_number"] for r in response["results"]]
            expected_articles = query["expected_articles"]
            recall = len(set(retrieved_articles) & set(expected_articles)) / len(expected_articles)
            results["article_recall"].append(recall)
            
            # Metric 3: Article Precision
            # Are retrieved articles relevant?
            precision = len(set(retrieved_articles) & set(expected_articles)) / len(retrieved_articles)
            results["article_precision"].append(precision)
            
            # Metric 4: Answer Faithfulness (using LLM as judge)
            faithfulness = self._check_faithfulness(
                answer=response["answer"],
                context=response["results"],
                ground_truth=query["ground_truth_answer"]
            )
            results["answer_faithfulness"].append(faithfulness)
            
            # Performance metrics
            results["query_latency"].append(response["query_time_ms"])
            results["cost_per_query"].append(response["cost_usd"])
        
        # Aggregate results
        return {
            "path_accuracy": np.mean(results["path_accuracy"]),
            "article_recall": np.mean(results["article_recall"]),
            "article_precision": np.mean(results["article_precision"]),
            "answer_faithfulness": np.mean(results["answer_faithfulness"]),
            "avg_query_latency_ms": np.mean(results["query_latency"]),
            "avg_cost_per_query_usd": np.mean(results["cost_per_query"]),
            "total_queries": len(test_queries)
        }
    
    def _check_path_accuracy(self, predicted: List[str], expected: List[str]) -> float:
        """
        Check if predicted reasoning path matches expected
        
        Allows for:
        - Extra intermediate nodes (not penalized)
        - Different path to same answer (partial credit)
        """
        # Exact match
        if predicted == expected:
            return 1.0
        
        # Partial match (key nodes present)
        key_nodes = [n for n in expected if n.isupper()]  # Article nodes
        predicted_nodes = [n for n in predicted if n.isupper()]
        
        overlap = len(set(key_nodes) & set(predicted_nodes))
        return overlap / len(key_nodes)
    
    async def _check_faithfulness(self, answer: str, context: List[dict], ground_truth: str) -> float:
        """
        Use LLM to verify answer is faithful to retrieved context
        """
        prompt = f"""
        Evaluate if this answer is faithful to the legal context.
        
        Context (Retrieved Articles):
        {context}
        
        Generated Answer:
        {answer}
        
        Ground Truth:
        {ground_truth}
        
        Rate faithfulness 0.0-1.0:
        - 1.0: Answer fully grounded in context, matches ground truth
        - 0.5: Partially correct, some hallucinations
        - 0.0: Answer contradicts context or is completely wrong
        
        Return only the score as a number.
        """
        
        response = await llm.ainvoke(prompt)
        return float(response.strip())
```

#### Target Metrics

| Metric | Target | Stretch Goal | Minimum Viable |
|--------|--------|--------------|----------------|
| **Path Accuracy** | >80% | >90% | >70% |
| **Article Recall** | >85% | >92% | >80% |
| **Article Precision** | >80% | >88% | >75% |
| **Answer Faithfulness** | >85% | >90% | >80% |
| **Avg Query Latency** | <2000ms | <1500ms | <3000ms |
| **Cost per Query** | <£0.10 | <£0.05 | <£0.15 |

**Why These Metrics Matter for Interviews**:

> **Interviewer**: "How do you know your GraphRAG is better than vector-only RAG?"
> 
> **Your Answer**: "I tested both on 50 multi-hop queries. Vector RAG achieved 45% path accuracy - it could find individual articles but couldn't connect them. My GraphRAG achieved 82% path accuracy by traversing relationships. On the query 'Does facial recognition for hiring require a DPIA?', vector RAG returned GDPR Article 9 but missed the connection to Article 35. GraphRAG followed the path: facial_recognition → biometric_data → special_category_data → DPIA_required, citing both articles."

---

### Phase 7: Optimization & Deployment (Week 9-10) - 10-12 hours

#### Week 9: Performance Optimization

**Objective**: Reduce query latency and cost

**Optimization 1: Query Caching**

```python
# src/retrieval/cache.py

import redis
import hashlib
import json

class QueryCache:
    """
    Cache frequent queries to reduce Neo4j/ChromaDB load
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url)
        self.ttl = 3600  # 1 hour cache
    
    def get(self, query: str, strategy: str) -> Optional[dict]:
        """
        Retrieve cached result
        """
        cache_key = self._generate_key(query, strategy)
        cached = self.redis_client.get(cache_key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def set(self, query: str, strategy: str, result: dict):
        """
        Cache query result
        """
        cache_key = self._generate_key(query, strategy)
        self.redis_client.setex(
            cache_key,
            self.ttl,
            json.dumps(result)
        )
    
    def _generate_key(self, query: str, strategy: str) -> str:
        """
        Generate cache key from query
        """
        content = f"{query}:{strategy}"
        return f"graphrag:{hashlib.md5(content.encode()).hexdigest()}"

# Integration with retriever
class CachedHybridRetriever(HybridLegalRetriever):
    """
    Retriever with caching
    """
    
    def __init__(self, graph_store, vector_store, cache: QueryCache):
        super().__init__(graph_store, vector_store)
        self.cache = cache
    
    async def retrieve(self, query: str, strategy: str = "hybrid", top_k: int = 10) -> List[dict]:
        # Check cache first
        cached_result = self.cache.get(query, strategy)
        if cached_result:
            return cached_result
        
        # Not cached - query normally
        result = await super().retrieve(query, strategy, top_k)
        
        # Cache for future
        self.cache.set(query, strategy, result)
        
        return result
```

**Optimization 2: Precomputed Paths**

For common query patterns, precompute frequent paths:

```python
# src/graph/path_precomputation.py

COMMON_PATHS = [
    # Biometric data → DPIA
    {
        "pattern": "biometric_data → DPIA",
        "cypher": """
            MATCH path = (bio:Concept {name: 'biometric_data'})
                -[*1..3]->
                (dpia:Requirement {name: 'DPIA'})
            RETURN path
        """,
        "precompute": True
    },
    # Facial recognition → High-risk
    {
        "pattern": "facial_recognition → high_risk",
        "cypher": """
            MATCH path = (fr:SystemType {name: 'facial_recognition'})
                -[*1..2]->
                (hr:RiskCategory {name: 'HIGH_RISK'})
            RETURN path
        """,
        "precompute": True
    }
]

def precompute_common_paths(graph_store):
    """
    Run during deployment to precompute frequent paths
    """
    for pattern in COMMON_PATHS:
        if pattern["precompute"]:
            with graph_store.client.session() as session:
                result = session.run(pattern["cypher"])
                # Store in cache
                paths = [record["path"] for record in result]
                cache.set(f"precomputed:{pattern['pattern']}", paths)
```

**Optimization 3: Batch Processing**

For Project 4 integration, support batch queries:

```python
@app.post("/api/v1/batch/reason")
async def batch_reasoning(requests: List[HybridReasoningRequest]):
    """
    Process multiple queries in parallel
    
    Used by Project 4 when agent needs to check multiple systems
    """
    import asyncio
    
    tasks = [
        hybrid_retriever.retrieve(req.question, req.strategy, req.top_k)
        for req in requests
    ]
    
    results = await asyncio.gather(*tasks)
    
    return {
        "batch_size": len(requests),
        "results": results,
        "total_cost_usd": sum(r["cost_usd"] for r in results)
    }
```

#### Week 10: Deployment

**Docker Compose Setup**:

```yaml
# docker-compose.yml

version: '3.8'

services:
  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.14
    environment:
      - NEO4J_AUTH=neo4j/password
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
    ports:
      - "7474:7474"  # Browser UI
      - "7687:7687"  # Bolt protocol
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
  
  # ChromaDB Vector Database
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
  
  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  # FastAPI Service
  api:
    build: .
    depends_on:
      - neo4j
      - chromadb
      - redis
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
      - CHROMA_HOST=chromadb
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8080

volumes:
  neo4j_data:
  neo4j_logs:
  chroma_data:
  redis_data:
```

**Dockerfile**:

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY data/ ./data/

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8080

# Run API
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deployment to GCP Cloud Run**:

```bash
# Build and push Docker image
docker build -t gcr.io/YOUR_PROJECT/legal-graphrag:latest .
docker push gcr.io/YOUR_PROJECT/legal-graphrag:latest

# Deploy to Cloud Run
gcloud run deploy legal-graphrag \
  --image gcr.io/YOUR_PROJECT/legal-graphrag:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars NEO4J_URI=YOUR_NEO4J_URI,OPENAI_API_KEY=YOUR_KEY \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300

# Get deployed URL
gcloud run services describe legal-graphrag --region europe-west1 --format='value(status.url)'
# Output: https://legal-graphrag-xxxxx-ew.a.run.app
```

---

## 📄 Documentation & Demo (Week 10 cont.) - 4-6 hours

### README.md Template

```markdown
# Legal GraphRAG: Multi-Hop Reasoning Engine for EU AI Act & GDPR

**The first production knowledge graph for legal compliance research**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.14-blue.svg)](https://neo4j.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

This project implements a **GraphRAG system** that performs multi-hop reasoning across EU AI Act and GDPR regulations. Unlike traditional vector RAG (which fails at relationship queries), GraphRAG can answer complex questions by traversing knowledge graph relationships.

### Business Impact
- **31,250× cost reduction**: £2,500 manual research → £0.08 automated query
- **80% better accuracy** on multi-hop questions vs vector-only RAG
- **Powers Project 4**: Legal Research Agent backend for autonomous compliance system

---

## 🏗️ Architecture

[Insert architecture diagram]

### Key Components

1. **Knowledge Graph (Neo4j)**: 212 article nodes, 500+ relationships
2. **Vector Store (ChromaDB)**: Semantic search over regulation text
3. **Hybrid Retrieval**: Reciprocal Rank Fusion of graph + vector results
4. **FastAPI Service**: Production-ready REST API

---

## 🚀 Quick Start

```bash
# Start infrastructure
docker-compose up -d

# Build knowledge graph
uv run python scripts/build_graph.py

# Start API
uv run uvicorn src.api.main:app --reload --port 8080

# Test query
curl -X POST http://localhost:8080/api/v1/hybrid/reason \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Does facial recognition for hiring require a DPIA?",
    "strategy": "hybrid"
  }'
```

---

## 📊 Evaluation Results

Tested on 50 multi-hop legal queries:

| Metric | Score | Target |
|--------|-------|--------|
| Path Accuracy | 82% | >80% ✅ |
| Article Recall | 87% | >85% ✅ |
| Article Precision | 83% | >80% ✅ |
| Answer Faithfulness | 86% | >85% ✅ |
| Avg Query Latency | 1,850ms | <2000ms ✅ |
| Cost per Query | £0.08 | <£0.10 ✅ |

**Comparison**:
- Vector-only RAG: 45% path accuracy (fails at multi-hop)
- Manual legal research: £2,500 per query, 10 hours
- **GraphRAG: 82% path accuracy, £0.08 per query, 2 seconds** ✅

---

## 🎓 Interview Talking Points

### 30-Second Pitch
> "I built a legal knowledge graph that performs multi-hop reasoning across EU AI Act and GDPR. It powers the Legal Research Agent in my compliance automation system (Project 4). When asked 'Does facial recognition for hiring require a DPIA?', it traverses: facial_recognition → biometric_data → special_category_data → DPIA_required, citing GDPR Articles 9 and 35. It's 31,250× cheaper than manual legal research and 80% more accurate than vector-only RAG."

### Technical Deep Dive
- **Graph Schema**: "I designed a multi-layered schema with Article nodes, Concept nodes, and typed relationships (REQUIRES, PROHIBITS, REGULATES). This enables Cypher queries like 'Find all requirements triggered by biometric data processing'."
- **Hybrid Retrieval**: "I combine graph traversal (for relationship reasoning) with vector search (for semantic similarity) using Reciprocal Rank Fusion. Graph-only gives 70% recall, vector-only gives 80%, but hybrid achieves 87%."
- **Portfolio Integration**: "Project 4's Legal Research Agent makes real API calls to this GraphRAG system. It's not a demo - it's production infrastructure."

---

## 📜 License

MIT License

---

**Status**: ✅ Production Ready | API live at :8080 | Integrated with Project 4
```

### Demo Video Script (3-4 minutes)

```
[0:00-0:20] Hook
"Vector RAG is everywhere. But it fails at one critical task: multi-hop reasoning. Let me show you the difference."

[0:20-1:00] The Problem
Screen: Show vector RAG query "Does facial recognition for hiring require a DPIA?"
Result: Returns GDPR Article 9 (biometric data) but misses Article 35 (DPIA)
Narration: "Vector search finds keywords but can't connect the dots."

[1:00-2:30] The Solution
Screen: Neo4j Browser showing knowledge graph visualization
Highlight path: facial_recognition → PROCESSES → biometric_data → IS_EXAMPLE_OF → special_category_data → TRIGGERS → DPIA
Narration: "My GraphRAG system traverses relationships. It understands that facial recognition PROCESSES biometric data, which IS an EXAMPLE OF special category data, which TRIGGERS a DPIA requirement."

[2:30-3:00] Live Demo
Screen: Postman making API call to /api/v1/hybrid/reason
Show JSON response with reasoning chains
Narration: "This powers my compliance automation system. When the Legal Research Agent needs legal citations, it calls this API."

[3:00-3:30] Results
Screen: Evaluation metrics table
Narration: "82% path accuracy, 87% article recall. Tested on 50 real legal queries. Compare that to 45% for vector-only RAG."

[3:30-4:00] Impact
Screen: Cost comparison (£2,500 manual → £0.08 GraphRAG)
Narration: "This is production infrastructure, not a toy demo. It's deployed on GCP Cloud Run and integrated into my multi-agent compliance platform."
```

---

## 🎯 Success Criteria Checklist

### Technical Excellence
- [ ] Knowledge graph contains 200+ article nodes
- [ ] 500+ relationships extracted and validated
- [ ] Multi-hop queries successfully traverse 2-3 hops
- [ ] API handles concurrent requests without errors
- [ ] Integration with Project 4 tested and working

### Evaluation
- [ ] Path accuracy >80% on golden dataset
- [ ] Article recall >85%
- [ ] Query latency <2 seconds (P95)
- [ ] Cost per query <£0.10

### Production Readiness
- [ ] Docker Compose setup works locally
- [ ] Deployed to cloud with public URL
- [ ] Error handling for Neo4j/ChromaDB failures
- [ ] Query caching reduces latency by 60%
- [ ] Monitoring dashboard shows graph statistics

### Portfolio Integration
- [ ] Project 4 Legal Research Agent successfully calls this API
- [ ] Demo video shows end-to-end integration
- [ ] Documentation explains how projects connect

### Interview Readiness
- [ ] Can explain graph schema on whiteboard
- [ ] Can defend GraphRAG vs vector RAG tradeoffs
- [ ] Have prepared "failure mode" answers (what if Neo4j is down?)
- [ ] Can demonstrate live system during interview

---

## 🚨 Common Pitfalls & Mitigations

### Pitfall 1: "Entity extraction is too noisy"

**Symptom**: LLM extracts 1000+ entities, many irrelevant

**Mitigation**:
- Use two-stage extraction (rule-based first, LLM second)
- Set confidence threshold (only keep entities with >0.7 confidence)
- Manual validation of top 100 entities
- Iteratively refine LLM prompt with negative examples

### Pitfall 2: "Graph queries are too slow"

**Symptom**: Cypher queries take >5 seconds

**Mitigation**:
- Add indexes on frequently queried properties: `CREATE INDEX ON :Article(article_number)`
- Limit max hops to 3 (longer paths rarely useful)
- Use query caching (Redis)
- Precompute common paths during deployment

### Pitfall 3: "Neo4j learning curve"

**Symptom**: Stuck on Cypher syntax

**Mitigation**:
- Start with LlamaIndex PropertyGraphIndex (abstracts Cypher)
- Use Neo4j Browser to visualize queries
- Copy patterns from Neo4j docs
- Join Neo4j Community Slack for help

### Pitfall 4: "Can't prove it's better than vector RAG"

**Symptom**: No quantitative comparison

**Mitigation**:
- Build same test set for both systems
- Run side-by-side evaluation
- Create comparison table in README
- Include in demo video

### Pitfall 5: "Integration with Project 4 breaks"

**Symptom**: API calls fail from Project 4 agents

**Mitigation**:
- Add comprehensive API tests
- Implement retry logic with exponential backoff
- Add fallback to vector-only if graph fails
- Test early (Week 7, not Week 10)

---

## 📚 Resources & References

### Essential Reading
- [Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)
- [LlamaIndex PropertyGraphIndex](https://docs.llamaindex.ai/en/stable/examples/property_graph/)
- [Microsoft GraphRAG Paper](https://arxiv.org/abs/2404.16130)
- [Reciprocal Rank Fusion](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)

### Tools
- [Neo4j Browser](http://localhost:7474) - Graph visualization
- [Neo4j Bloom](https://neo4j.com/product/bloom/) - Visual exploration (optional paid)
- [Cypher Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/current/)

---

## 🏆 Final Advice

### What Makes This Project "Interview Gold"

**1. Rare Skill**: GraphRAG expertise is extremely rare in 2026. Most candidates only know vector RAG.

**2. Portfolio Integration**: This isn't standalone - it's the backend for Project 4. That's engineering maturity.

**3. Business Impact**: You can cite 31,250× cost reduction and 80% accuracy improvement with data to back it up.

**4. Technical Depth**: Knowledge graphs, Cypher queries, hybrid retrieval, RRF - you're demonstrating advanced information retrieval skills.

**5. Production Thinking**: API design, caching, error handling, deployment - this is production-grade infrastructure.

### The "Killer Demo" Strategy

**Don't say**: "I built a knowledge graph"  
**Say**: "I built the legal research engine that my compliance automation platform uses to perform multi-hop reasoning across 200+ regulation articles"

**Don't show**: Neo4j Browser with nodes  
**Show**: Live API call from Project 4 agent getting multi-hop reasoning chains

**Don't explain**: Graph database concepts  
**Explain**: "When the Legal Research Agent asks 'Does facial recognition require a DPIA?', it calls my GraphRAG API which traverses: facial_recognition → biometric_data → DPIA_required, returning cited articles in 2 seconds for £0.08 vs £2,500 manual research"

---

## 🎯 Integration with Project 4

### How Projects Connect

```python
# In Project 4: src/agents/legal_research_agent.py

class LegalResearchAgent:
    """
    Calls Project 3 GraphRAG API for legal citations
    """
    
    def __init__(self, graphrag_api_url: str):
        # Points to your deployed GraphRAG API
        self.graphrag_url = graphrag_api_url  # e.g., "https://legal-graphrag-xxx.run.app"
    
    async def research(self, query: str) -> dict:
        """
        Query knowledge graph for legal citations
        """
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.graphrag_url}/api/v1/hybrid/reason",
                json={
                    "question": query,
                    "strategy": "hybrid",
                    "top_k": 5
                },
                timeout=30.0
            )
            
            result = response.json()
            
            return {
                "relevant_articles": result["results"],
                "reasoning_chains": result["reasoning_chains"],
                "confidence": self._calculate_confidence(result),
                "cost_usd": result["cost_usd"]
            }
```

### Testing Integration

```python
# tests/integration/test_project_integration.py

async def test_project4_calls_project3():
    """
    Verify Project 4 can call Project 3 API
    """
    # Start Project 3 API locally
    graphrag_url = "http://localhost:8080"
    
    # Project 4 agent
    agent = LegalResearchAgent(graphrag_api_url=graphrag_url)
    
    # Test query
    result = await agent.research(
        "Does facial recognition for hiring require a DPIA?"
    )
    
    # Verify response
    assert "relevant_articles" in result
    assert len(result["relevant_articles"]) > 0
    assert "GDPR Article 35" in str(result["relevant_articles"])
    assert result["cost_usd"] < 0.50  # Should be cheap
```

---

## 📈 Expected Outcomes

### Market Positioning

**Before**: "AI Engineer with RAG skills" (£50K-£65K)  
**After**: "Context Architect / GraphRAG Specialist" (£70K-£90K)

**Why**: GraphRAG expertise is rare, high-value, and aligns with emerging "Context Architect" role from 2026 forecast.

### Competitive Edge

When interviewer asks: "What differentiates you from other candidates?"

**Your Answer**:
> "I didn't just learn RAG from a tutorial. I built a production legal knowledge graph that my autonomous compliance system actually uses. While other candidates show toy demos, I show integrated infrastructure. The Legal Research Agent in my Project 4 makes real API calls to my GraphRAG system (Project 3), performing multi-hop reasoning across EU regulations. It's tested on 50 real queries, deployed on GCP, and achieves 82% path accuracy - 80% better than vector-only approaches."

---

**Project Difficulty**: 🔴 Advanced  
**Market Relevance**: 🔴 CRITICAL (Context Architect role emerging)  
**Differentiation Score**: 9/10 (Very rare skill)  
**Estimated Time**: 50-60 hours (8-10 weeks @ 6-8 hrs/week)  
**Expected Salary Impact**: +£10K-£15K (enables "Context Architect" positioning)

---

**Document Version**: 1.0  
**Created**: January 2026  
**Purpose**: Complete implementation plan for Project 3 GraphRAG  
**Status**: Ready to build  
**Integrates With**: Project 4 (Legal Research Agent backend)

Go build the knowledge infrastructure of the future. 🚀

---


## SOURCE: `gdpr context/backup/project_4 EU AI Act Compliance Automation Agent.md`

# Project 4: EU AI Act Compliance Automation Agent

**"The Autonomous Compliance Engine"**

**Duration**: 10-12 weeks (80-100 hours)  
**Target Market**: UK/EU AI Engineering roles (£70K-£90K)  
**Differentiation Score**: 10/10 (First-of-its-kind portfolio project)  
**Market Timing**: CRITICAL (EU AI Act enforcement begins August 2026)

---

## 🎯 Executive Summary

### The "Hire Me" Pitch

This project builds the **first autonomous EU AI Act compliance system** using a 5-agent orchestration architecture. Companies upload their AI system specifications, and within 6 hours (vs. 6 weeks manual), receive:

- Risk classification (Prohibited/High-Risk/Limited/Minimal)
- GDPR compliance audit
- Legal citation report (using GraphRAG from Project 3)
- Production-ready compliance documentation (DPIA, Conformity Assessment)

**Business Impact**: Saves £6,800 per compliance assessment = **£102,000/year** for a consultancy handling 15 assessments/month.

### Portfolio Synergy

This is your **portfolio integration masterpiece**:

```
Project 1 (RAG) → Knowledge Base for EU regulations
                     ↓
Project 3 (GraphRAG) → Legal Research Agent backend
                     ↓
Project 4 (Multi-Agent) → Autonomous compliance orchestration
```

**Interview Gold**: "I didn't just build 4 separate projects. I built a **compliance platform** where each project is a module in an integrated system."

---

## 📊 Market Analysis & Differentiation

### Why This Project is a "Recruiter Magnet"

| Standard Portfolio Project | Your Project |
|---------------------------|--------------|
| Generic "customer support chatbot" (1000+ on GitHub) | EU AI Act compliance agent (ZERO on GitHub) |
| No business domain | Regulatory compliance (high-stakes, high-value) |
| Standalone demo | Integrates 3 of your portfolio projects |
| "It works on my laptop" | Production-grade with governance, cost tracking, human-in-loop |
| No clear ROI | £102K/year savings with documented assumptions |

### Competitive Landscape (as of Jan 2026)

**Search Query**: "EU AI Act compliance automation"

**Results**:
- 🏢 **Manual Consultancies**: Deloitte, EY, PwC (£8K per assessment, 4-6 weeks)
- 📋 **Compliance Checklists**: Static PDF guides (no automation)
- 🤖 **Your System**: Autonomous multi-agent orchestration (**FIRST**)

**Your Edge**: You're building the tool these consultancies will BUY in 2027.

---

## 🏗️ System Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Next.js)                 │
│  - Upload AI System Specs                                   │
│  - View Real-Time Agent Workflow                            │
│  - Approve/Reject High-Stakes Decisions                     │
│  - Download Compliance Reports                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              COMPLIANCE SUPERVISOR AGENT                    │
│  (LangGraph Orchestrator)                                   │
│                                                             │
│  Role: Receives compliance request, decomposes into tasks, │
│        routes to specialist agents, synthesizes final report│
└─────────┬────────────┬────────────┬────────────┬───────────┘
          │            │            │            │
┌─────────▼────┐ ┌─────▼─────┐ ┌───▼──────┐ ┌──▼────────────┐
│ RISK         │ │ TECHNICAL │ │ LEGAL    │ │ DOCUMENTATION │
│ CLASSIFIER   │ │ ASSESSOR  │ │ RESEARCH │ │ GENERATOR     │
│ AGENT        │ │ AGENT     │ │ AGENT    │ │ AGENT         │
│              │ │           │ │          │ │               │
│ Determines   │ │ Audits for│ │ Queries  │ │ Generates     │
│ if system is │ │ GDPR      │ │ YOUR     │ │ DPIA, ROPAs,  │
│ Prohibited/  │ │ violations│ │ GraphRAG │ │ Conformity    │
│ High-Risk    │ │           │ │ (Proj 3) │ │ Assessments   │
└──────────────┘ └───────────┘ └──────────┘ └───────────────┘
          │            │            │            │
          └────────────┴────────────┴────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              AGENT CONTROL PLANE                            │
│  - Governance Policies (rate limits, cost caps)             │
│  - Human-in-Loop Approval Queue                             │
│  - Audit Logging (every decision tracked)                   │
│  - Financial Tracking (£X spent on API calls)               │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

Following your **Best Practices** guidelines:

```yaml
Core Framework:
  - LangGraph: Agent orchestration (state machines)
  - LangChain: Tool integration
  - Pydantic: Type safety for agent states
  
LLM Providers:
  - Primary: GPT-4o (complex reasoning for Supervisor)
  - Secondary: GPT-4o-mini (simple classification tasks)
  - Fallback: Claude 3.5 Sonnet (for GDPR analysis)
  
Backend:
  - FastAPI: REST API for agent orchestration
  - PostgreSQL: Audit logs, compliance history
  - Redis: Task queue, agent state caching
  
Frontend:
  - Next.js 14 (TypeScript)
  - TailwindCSS: Professional UI
  - Shadcn/ui: Component library
  
Integration:
  - Project 3 GraphRAG API: Legal research queries
  - Project 1 RAG system: Regulation retrieval (optional)
  
Monitoring:
  - LangSmith: Agent trace logging (if using LangChain)
  - Prometheus: API metrics
  - Custom Dashboard: Agent performance, cost tracking
  
Deployment:
  - Docker: Containerization
  - GCP Cloud Run: Serverless deployment
  - GitHub Actions: CI/CD
```

---

## 🤖 Agent Specifications

### Agent 1: Compliance Supervisor Agent

**Role**: Orchestrator / Manager

**Responsibility**: 
- Receives compliance assessment request
- Decomposes into sub-tasks
- Routes to specialist agents
- Resolves conflicts between agents
- Synthesizes final compliance report

**LangGraph State Machine**:

```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph

class ComplianceState(TypedDict):
    """
    Shared state across all agents
    """
    # Input
    system_description: str
    system_type: str  # e.g., "facial_recognition", "chatbot", "credit_scoring"
    deployment_context: str  # e.g., "employee_monitoring", "customer_service"
    
    # Agent Outputs
    risk_classification: dict  # From Risk Classifier Agent
    gdpr_audit: dict           # From Technical Assessor Agent
    legal_citations: dict      # From Legal Research Agent
    compliance_docs: dict      # From Documentation Agent
    
    # Control Flow
    current_step: str
    requires_human_review: bool
    human_decision: str | None
    
    # Metadata
    confidence_scores: dict[str, float]
    cost_tracking: dict[str, float]
    audit_log: list[dict]

class SupervisorAgent:
    """
    The 'manager' that orchestrates specialist agents
    """
    
    def __init__(self):
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(ComplianceState)
        
        # Step 1: Risk Classification
        workflow.add_node("classify_risk", self._route_to_risk_classifier)
        
        # Step 2: Parallel Assessment (GDPR + Legal Research)
        workflow.add_node("assess_gdpr", self._route_to_technical_assessor)
        workflow.add_node("research_legal", self._route_to_legal_agent)
        
        # Step 3: Human Checkpoint (if high-risk)
        workflow.add_conditional_edges(
            "classify_risk",
            self._check_human_review_needed,
            {
                "needs_review": "await_approval",
                "auto_proceed": "parallel_assessment"
            }
        )
        
        # Step 4: Generate Documentation
        workflow.add_node("generate_docs", self._route_to_doc_generator)
        
        # Step 5: Synthesize Report
        workflow.add_node("synthesize", self._create_final_report)
        
        workflow.set_entry_point("classify_risk")
        
        return workflow.compile()
    
    def _check_human_review_needed(self, state: ComplianceState) -> Literal["needs_review", "auto_proceed"]:
        """
        Decision logic: When to pause for human approval
        """
        risk = state["risk_classification"]
        
        # Rule 1: Prohibited systems ALWAYS require human review
        if risk["category"] == "PROHIBITED":
            state["requires_human_review"] = True
            return "needs_review"
        
        # Rule 2: High-risk with low confidence
        if risk["category"] == "HIGH_RISK" and risk["confidence"] < 0.80:
            state["requires_human_review"] = True
            return "needs_review"
        
        # Rule 3: Conflicting agent outputs
        if self._detect_conflicts(state):
            state["requires_human_review"] = True
            return "needs_review"
        
        return "auto_proceed"
```

**Tools**: 
- Task router
- Conflict resolver
- Report synthesizer

**Success Criteria**:
- ✅ Correctly routes 100% of test cases to appropriate agents
- ✅ Detects conflicts (e.g., Risk Classifier says "High-Risk" but Technical Assessor finds "No GDPR violations")
- ✅ Pauses for human review when confidence < 80%

---

### Agent 2: Risk Classifier Agent

**Role**: Specialist

**Responsibility**: 
Determine if AI system falls into:
1. **Prohibited** (EU AI Act Article 5) - Cannot be deployed
2. **High-Risk** (Annex III) - Requires conformity assessment
3. **Limited Risk** (Article 52) - Transparency obligations only
4. **Minimal Risk** - No special requirements

**Decision Logic**:

```python
class RiskClassifierAgent:
    """
    Implements EU AI Act classification logic
    """
    
    # EU AI Act Article 5: Prohibited AI Practices
    PROHIBITED_PATTERNS = [
        "subliminal manipulation",
        "exploit vulnerabilities (age, disability)",
        "social scoring by public authorities",
        "real-time remote biometric identification (public spaces)",
        "predictive policing (individual risk assessment)",
        "emotion recognition (workplace, education)"
    ]
    
    # Annex III: High-Risk AI Systems
    HIGH_RISK_CATEGORIES = {
        "biometric_identification": ["facial_recognition", "gait_analysis"],
        "critical_infrastructure": ["traffic_management", "water_supply"],
        "education": ["exam_scoring", "admission_decisions"],
        "employment": ["cv_screening", "performance_evaluation"],
        "essential_services": ["credit_scoring", "insurance_pricing"],
        "law_enforcement": ["crime_prediction", "evidence_evaluation"],
        "migration": ["visa_decision", "asylum_assessment"],
        "justice": ["case_prioritization", "sentence_recommendation"]
    }
    
    async def classify(self, system_description: str, context: str) -> dict:
        """
        Step 1: Check for prohibited patterns
        Step 2: Check for high-risk categories
        Step 3: Determine transparency requirements
        """
        
        # Use LLM to extract system capabilities
        capabilities = await self._extract_capabilities(system_description)
        
        # Check PROHIBITED
        for pattern in self.PROHIBITED_PATTERNS:
            if self._matches_pattern(capabilities, pattern):
                return {
                    "category": "PROHIBITED",
                    "article": "Article 5",
                    "reason": f"System involves {pattern}",
                    "confidence": 0.95,
                    "action": "DEPLOYMENT_FORBIDDEN"
                }
        
        # Check HIGH-RISK
        for category, examples in self.HIGH_RISK_CATEGORIES.items():
            if self._matches_category(capabilities, category):
                return {
                    "category": "HIGH_RISK",
                    "annex": "Annex III",
                    "subcategory": category,
                    "confidence": 0.88,
                    "requirements": [
                        "Conformity assessment required",
                        "CE marking mandatory",
                        "Registration in EU database",
                        "Human oversight required"
                    ]
                }
        
        # Check LIMITED RISK (transparency)
        if self._is_user_facing(context):
            return {
                "category": "LIMITED_RISK",
                "article": "Article 52",
                "requirements": ["Transparency notice (users informed it's AI)"]
            }
        
        # Default: MINIMAL RISK
        return {
            "category": "MINIMAL_RISK",
            "requirements": ["No specific legal obligations"]
        }
    
    async def _extract_capabilities(self, description: str) -> dict:
        """
        Use LLM to parse system description into structured capabilities
        """
        prompt = f"""
        Analyze this AI system description and extract key capabilities:
        
        Description: {description}
        
        Return JSON with:
        - primary_function (e.g., "facial_recognition")
        - data_types (e.g., ["biometric", "behavioral"])
        - decision_impact (e.g., "hiring_decision")
        - deployment_context (e.g., "public_space")
        """
        
        response = await self.llm.ainvoke(prompt)
        return parse_json(response)
```

**Tools**:
- EU AI Act Article 5 checker (prohibited practices)
- Annex III matcher (high-risk categories)
- Confidence scorer

**Edge Cases to Handle**:
- User uploads vague description → Agent asks clarifying questions
- System spans multiple categories → Returns primary + secondary classifications
- Borderline cases → Flags for human review

**Test Cases** (Golden Dataset):

```python
TEST_CASES = [
    {
        "description": "Facial recognition for employee attendance tracking",
        "expected": "HIGH_RISK",  # Employment category
        "expected_annex": "Annex III (4) - Employment"
    },
    {
        "description": "Emotion detection for student engagement in online classes",
        "expected": "PROHIBITED",  # Article 5(1)(f) - Emotion recognition in education
    },
    {
        "description": "Chatbot for customer service (clearly disclosed as AI)",
        "expected": "LIMITED_RISK",  # Article 52 - Transparency
    },
    {
        "description": "Credit scoring for loan approval",
        "expected": "HIGH_RISK",  # Annex III (5) - Essential services
    }
]
```

---

### Agent 3: Technical Assessor Agent

**Role**: Specialist (GDPR Auditor)

**Responsibility**:
Audit AI system for GDPR compliance:
1. **Data Minimization** (Article 5(1)(c))
2. **Lawful Basis** (Article 6)
3. **Special Category Data** (Article 9)
4. **Automated Decision-Making** (Article 22)
5. **Data Security** (Article 32)

**Audit Checklist**:

```python
class TechnicalAssessorAgent:
    """
    GDPR compliance auditor
    """
    
    GDPR_CHECKLIST = {
        "data_minimization": {
            "article": "Article 5(1)(c)",
            "questions": [
                "Does system collect only necessary data?",
                "Is data retention period defined?",
                "Are unused data fields deleted?"
            ]
        },
        "lawful_basis": {
            "article": "Article 6",
            "questions": [
                "What is the lawful basis? (consent, contract, legal obligation, vital interests, public task, legitimate interests)",
                "If consent: Is it freely given, specific, informed, unambiguous?",
                "If legitimate interests: Has balancing test been performed?"
            ]
        },
        "special_category_data": {
            "article": "Article 9",
            "questions": [
                "Does system process biometric data?",
                "Does system process health data?",
                "Is there an Article 9(2) exception? (explicit consent, vital interests, etc.)"
            ]
        },
        "automated_decisions": {
            "article": "Article 22",
            "questions": [
                "Are decisions solely automated?",
                "Do decisions produce legal/similarly significant effects?",
                "Is there meaningful human involvement?",
                "Can individuals request human review?"
            ]
        }
    }
    
    async def audit(self, system_description: str, data_flows: dict) -> dict:
        """
        Run GDPR compliance check
        """
        violations = []
        warnings = []
        
        # Check each GDPR requirement
        for requirement, details in self.GDPR_CHECKLIST.items():
            result = await self._check_requirement(
                system_description,
                data_flows,
                details
            )
            
            if result["status"] == "VIOLATION":
                violations.append({
                    "article": details["article"],
                    "issue": result["issue"],
                    "severity": "HIGH"
                })
            elif result["status"] == "WARNING":
                warnings.append({
                    "article": details["article"],
                    "issue": result["issue"],
                    "severity": "MEDIUM"
                })
        
        return {
            "gdpr_compliant": len(violations) == 0,
            "violations": violations,
            "warnings": warnings,
            "recommendations": self._generate_recommendations(violations, warnings)
        }
    
    async def _check_requirement(self, description: str, data_flows: dict, requirement: dict) -> dict:
        """
        Use LLM to evaluate compliance with specific GDPR article
        """
        prompt = f"""
        You are a GDPR compliance auditor.
        
        System: {description}
        Data Flows: {data_flows}
        
        Evaluate compliance with {requirement['article']}:
        Questions to answer:
        {requirement['questions']}
        
        Return JSON:
        {{
            "status": "COMPLIANT" | "WARNING" | "VIOLATION",
            "issue": "Description of problem (if any)",
            "evidence": "Quote from system description"
        }}
        """
        
        response = await self.llm.ainvoke(prompt)
        return parse_json(response)
```

**Tools**:
- GDPR Article matcher
- Data flow analyzer
- Special category data detector

**Integration with Risk Classifier**:

If Risk Classifier says "HIGH-RISK", Technical Assessor must additionally check:
- Article 10 (Data Quality - high-risk systems need training data documentation)
- Article 14 (Human Oversight - high-risk systems need human intervention capability)

---

### Agent 4: Legal Research Agent ⭐ **INTEGRATES PROJECT 3**

**Role**: Specialist (Knowledge Graph Query)

**Responsibility**:
- Query your **GraphRAG system** (Project 3) for relevant legal articles
- Perform multi-hop reasoning across GDPR + EU AI Act
- Generate citation report with confidence scores

**Architecture**:

```python
class LegalResearchAgent:
    """
    Queries Project 3 GraphRAG for legal citations
    
    This is where your portfolio INTEGRATION happens!
    """
    
    def __init__(self, graphrag_api_url: str):
        # This points to your Project 3 API endpoint
        self.graphrag_client = GraphRAGClient(api_url=graphrag_api_url)
    
    async def research(self, query: str, risk_category: str) -> dict:
        """
        Step 1: Entity extraction from query
        Step 2: Graph traversal for relevant articles
        Step 3: Vector search for supporting text
        Step 4: Synthesize citations
        """
        
        # Extract legal entities
        entities = await self._extract_legal_entities(query)
        # e.g., ["facial_recognition", "GDPR_Article_6", "biometric_data"]
        
        # Call YOUR GraphRAG API (Project 3)
        graph_results = await self.graphrag_client.traverse(
            start_entities=entities,
            relationship_types=["REGULATES", "REQUIRES", "PROHIBITS"],
            max_hops=2  # Multi-hop reasoning
        )
        
        # Vector search for supporting context
        vector_results = await self.graphrag_client.vector_search(
            query=query,
            top_k=5,
            filter_regulation=["GDPR", "EU_AI_ACT"]
        )
        
        # Synthesize findings
        return {
            "relevant_articles": self._rank_articles(graph_results, vector_results),
            "relationship_chains": graph_results["paths"],
            "citations": self._format_citations(graph_results),
            "confidence": self._calculate_confidence(graph_results)
        }
    
    def _rank_articles(self, graph: dict, vector: dict) -> list[dict]:
        """
        Combine graph + vector results, rank by relevance
        """
        articles = []
        
        # From graph: Articles connected by relationships
        for path in graph["paths"]:
            for node in path["nodes"]:
                if node["type"] == "ARTICLE":
                    articles.append({
                        "regulation": node["regulation"],  # "GDPR" or "EU_AI_ACT"
                        "article_number": node["number"],  # e.g., "Article 22"
                        "title": node["title"],
                        "relevance_score": path["weight"],
                        "relationship": path["relationship"]  # e.g., "PROHIBITS"
                    })
        
        # From vector: Articles with high semantic similarity
        for result in vector["results"]:
            articles.append({
                "regulation": result["metadata"]["regulation"],
                "article_number": result["metadata"]["article"],
                "text_snippet": result["text"][:200],
                "similarity_score": result["score"]
            })
        
        # Deduplicate and rank
        return self._merge_and_rank(articles)
```

**Example Query Flow**:

**Input**: "Company wants to use facial recognition for employee attendance"

**Step 1**: Extract entities
- `facial_recognition` (system type)
- `employee_monitoring` (context)
- `biometric_data` (data type)

**Step 2**: Graph traversal (YOUR PROJECT 3)
```cypher
MATCH (sys:SystemType {name: 'facial_recognition'})
      -[:REGULATED_BY]->(art:Article)
      -[:REQUIRES]->(req:Requirement)
RETURN sys, art, req
```

**Results**:
- EU AI Act Annex III (4) → Employment → HIGH-RISK
- GDPR Article 9 → Biometric Data → Special Category
- GDPR Article 22 → Automated Decision → Human Oversight Required

**Step 3**: Vector search for supporting text
- "Biometric data for the purpose of uniquely identifying a natural person" (GDPR Recital 51)
- "AI systems used in employment for recruitment or selection" (EU AI Act Annex III)

**Output**:
```json
{
  "relevant_articles": [
    {
      "regulation": "EU_AI_ACT",
      "article": "Annex III (4)",
      "title": "High-risk AI systems - Employment",
      "reasoning": "System is used for attendance tracking → employment decisions",
      "confidence": 0.95
    },
    {
      "regulation": "GDPR",
      "article": "Article 9",
      "title": "Processing of special categories of data",
      "reasoning": "Facial recognition processes biometric data",
      "confidence": 0.98
    }
  ],
  "multi_hop_chain": [
    "facial_recognition → PROCESSES → biometric_data",
    "biometric_data → GOVERNED_BY → GDPR_Article_9",
    "GDPR_Article_9 → REQUIRES → explicit_consent OR legal_basis_exception"
  ]
}
```

**Tools**:
- Your Project 3 GraphRAG API (Neo4j + ChromaDB)
- LLM for query expansion
- Citation formatter

**Success Criteria**:
- ✅ Successfully queries Project 3 API
- ✅ Returns multi-hop reasoning chains
- ✅ Cites EXACT article numbers (no hallucinations)
- ✅ Handles API failures gracefully (fallback to vector-only search)

---

### Agent 5: Documentation Generator Agent

**Role**: Specialist (Document Production)

**Responsibility**:
Generate required compliance documents:
1. **DPIA** (Data Protection Impact Assessment) - GDPR Article 35
2. **ROPA** (Record of Processing Activities) - GDPR Article 30
3. **Conformity Assessment** - EU AI Act (High-Risk systems)
4. **Transparency Notice** - EU AI Act Article 52

**Document Templates**:

```python
class DocumentationGeneratorAgent:
    """
    Generates production-ready compliance documents
    """
    
    TEMPLATES = {
        "DPIA": "templates/dpia_template.md",
        "ROPA": "templates/ropa_template.md",
        "CONFORMITY_ASSESSMENT": "templates/conformity_assessment.md",
        "TRANSPARENCY_NOTICE": "templates/transparency_notice.md"
    }
    
    async def generate(self, state: ComplianceState) -> dict:
        """
        Step 1: Determine which documents are required
        Step 2: Fill templates with agent outputs
        Step 3: Return downloadable files
        """
        
        required_docs = self._determine_requirements(
            risk=state["risk_classification"],
            gdpr=state["gdpr_audit"]
        )
        
        documents = {}
        
        for doc_type in required_docs:
            template = self._load_template(doc_type)
            
            # Fill template with data from other agents
            filled = await self._fill_template(
                template=template,
                data={
                    "system_description": state["system_description"],
                    "risk_classification": state["risk_classification"],
                    "gdpr_audit": state["gdpr_audit"],
                    "legal_citations": state["legal_citations"]
                }
            )
            
            documents[doc_type] = {
                "content": filled,
                "format": "markdown",
                "filename": f"{doc_type}_{timestamp}.md"
            }
        
        return documents
    
    def _determine_requirements(self, risk: dict, gdpr: dict) -> list[str]:
        """
        Business logic: Which documents are legally required?
        """
        required = []
        
        # GDPR Article 35: DPIA required if "high risk to rights and freedoms"
        if gdpr.get("processes_special_category_data"):
            required.append("DPIA")
        
        if risk["category"] in ["HIGH_RISK", "PROHIBITED"]:
            required.append("DPIA")
        
        # GDPR Article 30: ROPA always required (unless <250 employees exemption)
        required.append("ROPA")
        
        # EU AI Act: Conformity Assessment for high-risk systems
        if risk["category"] == "HIGH_RISK":
            required.append("CONFORMITY_ASSESSMENT")
        
        # EU AI Act Article 52: Transparency for user-facing AI
        if risk["category"] == "LIMITED_RISK":
            required.append("TRANSPARENCY_NOTICE")
        
        return required
    
    async def _fill_template(self, template: str, data: dict) -> str:
        """
        Use LLM to fill template sections with compliance data
        """
        prompt = f"""
        You are a legal documentation specialist.
        
        Template: {template}
        
        Fill in the following sections using the compliance data:
        
        System Description: {data['system_description']}
        Risk Classification: {data['risk_classification']}
        GDPR Audit Results: {data['gdpr_audit']}
        Legal Citations: {data['legal_citations']}
        
        Rules:
        - Use formal legal language
        - Cite specific articles (e.g., "pursuant to GDPR Article 35(1)")
        - Include all required fields from template
        - No placeholder text (e.g., no "[INSERT X]")
        
        Return the completed document in Markdown format.
        """
        
        response = await self.llm.ainvoke(prompt)
        return response
```

**Example DPIA Template** (Partial):

```markdown
# Data Protection Impact Assessment (DPIA)
**Pursuant to GDPR Article 35**

## 1. Description of Processing Operation

**System Name**: [Filled by agent from state]
**Purpose**: [Filled by agent]
**Legal Basis**: [Filled from GDPR audit]

## 2. Necessity and Proportionality Assessment

**Is the processing necessary?**: [Agent evaluates]
**Could a less intrusive method achieve the same goal?**: [Agent suggests alternatives]

## 3. Risks to Data Subjects

**Identified Risks**:
- [From GDPR audit violations]
- [From risk classification]

**Likelihood**: [Agent estimates: High/Medium/Low]
**Severity**: [Agent estimates]

## 4. Measures to Address Risks

**Technical Measures**:
- [From technical assessor recommendations]

**Organizational Measures**:
- [Agent suggests: staff training, access controls]

## 5. Consultation with Data Protection Officer

**Recommendation**: [If high risk, agent flags: "DPO consultation MANDATORY"]

## 6. Conclusion

**DPIA Outcome**: Processing [CAN/CANNOT] proceed subject to implementation of measures.

---

**Document Generated**: [Timestamp]
**Generated by**: EU AI Act Compliance Agent v1.0
**Legal Citations**: 
- GDPR Article 35 (Data Protection Impact Assessments)
- [Additional citations from Legal Research Agent]
```

**Tools**:
- Template engine (Jinja2 or similar)
- LLM for narrative generation
- PDF converter (for official submission)

---

## 🛡️ Agent Control Plane (Governance Layer)

### Overview

The Control Plane is the **"HR department for AI workers"**. It enforces policies, tracks costs, and ensures agents don't go rogue.

**Critical for 2026**: By 2026, no enterprise deploys agents without governance. This is THE differentiator.

### Control Plane Features

```python
from pydantic import BaseModel
from enum import Enum

class AgentPermissionLevel(Enum):
    READ_ONLY = "read"
    WRITE_ALLOWED = "write"
    REQUIRES_APPROVAL = "approval"

class GovernancePolicy(BaseModel):
    """
    Policy for each agent
    """
    agent_name: str
    max_api_calls_per_hour: int
    max_spend_per_action_usd: float
    permission_level: AgentPermissionLevel
    requires_human_approval_if: list[str]  # Conditions
    
    class Config:
        frozen = True  # Immutable policies

class AgentControlPlane:
    """
    Central governance system
    """
    
    # Policies for each agent
    POLICIES = {
        "risk_classifier": GovernancePolicy(
            agent_name="risk_classifier",
            max_api_calls_per_hour=50,
            max_spend_per_action_usd=0.10,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=["classification == PROHIBITED"]
        ),
        "legal_research": GovernancePolicy(
            agent_name="legal_research",
            max_api_calls_per_hour=100,  # Calls Project 3 GraphRAG
            max_spend_per_action_usd=0.50,
            permission_level=AgentPermissionLevel.READ_ONLY,
            requires_human_approval_if=["confidence < 0.75"]
        ),
        "technical_assessor": GovernancePolicy(
            agent_name="technical_assessor",
            max_api_calls_per_hour=30,
            max_spend_per_action_usd=0.15,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=["violations_detected > 0"]
        ),
        "documentation_generator": GovernancePolicy(
            agent_name="documentation_generator",
            max_api_calls_per_hour=20,
            max_spend_per_action_usd=1.00,  # Document generation is expensive
            permission_level=AgentPermissionLevel.REQUIRES_APPROVAL,
            requires_human_approval_if=["always"]  # Always review docs before delivery
        )
    }
    
    def __init__(self):
        self.audit_log = []
        self.rate_limiter = RateLimiter()
        self.cost_tracker = CostTracker()
    
    async def authorize_action(self, agent_name: str, action: dict, cost_estimate: float) -> dict:
        """
        Before ANY agent takes an action, it calls this method
        
        Returns:
        {
            "authorized": bool,
            "reason": str,
            "requires_approval": bool
        }
        """
        policy = self.POLICIES[agent_name]
        
        # Check 1: Rate limit
        if not self.rate_limiter.check(agent_name, policy.max_api_calls_per_hour):
            return {
                "authorized": False,
                "reason": f"Rate limit exceeded ({policy.max_api_calls_per_hour}/hour)",
                "requires_approval": False
            }
        
        # Check 2: Cost limit
        if cost_estimate > policy.max_spend_per_action_usd:
            return {
                "authorized": False,
                "reason": f"Cost ${cost_estimate:.2f} exceeds limit ${policy.max_spend_per_action_usd}",
                "requires_approval": True  # Can override with approval
            }
        
        # Check 3: Approval conditions
        for condition in policy.requires_human_approval_if:
            if self._evaluate_condition(condition, action):
                return {
                    "authorized": False,
                    "reason": f"Approval required: {condition}",
                    "requires_approval": True
                }
        
        # All checks passed
        self.rate_limiter.increment(agent_name)
        self.cost_tracker.add(agent_name, cost_estimate)
        
        return {"authorized": True}
    
    def log_decision(self, agent_name: str, action: dict, outcome: dict):
        """
        Every agent action is logged for audit trail
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "outcome": outcome,
            "cost_usd": outcome.get("cost", 0),
            "duration_seconds": outcome.get("duration", 0)
        }
        
        self.audit_log.append(log_entry)
        
        # Persist to database
        db.save_audit_log(log_entry)
    
    def get_agent_statistics(self) -> dict:
        """
        Dashboard metrics
        """
        return {
            "total_actions": len(self.audit_log),
            "total_cost_usd": self.cost_tracker.total(),
            "actions_by_agent": self._count_by_agent(),
            "approval_rate": self._calculate_approval_rate(),
            "average_cost_per_action": self.cost_tracker.average()
        }
```

### Human-in-Loop Approval Queue

**When Agent Pauses for Approval:**

```python
class ApprovalQueue:
    """
    Manages high-stakes decisions awaiting human review
    """
    
    async def request_approval(self, agent_name: str, action: dict, state: ComplianceState) -> dict:
        """
        Sends approval request to human reviewer
        """
        approval_request = {
            "id": str(uuid4()),
            "agent": agent_name,
            "action": action,
            "context": {
                "system_description": state["system_description"],
                "agent_reasoning": action.get("reasoning"),
                "confidence_score": action.get("confidence")
            },
            "risk_level": self._assess_risk_level(action),
            "timestamp": datetime.now(),
            "status": "PENDING"
        }
        
        # Store in database
        db.save_approval_request(approval_request)
        
        # Notify human via Slack/Email
        await self._send_notification(approval_request)
        
        # Wait for decision (with timeout)
        decision = await self._wait_for_decision(
            approval_id=approval_request["id"],
            timeout_seconds=3600  # 1 hour
        )
        
        return decision
    
    async def _send_notification(self, request: dict):
        """
        Send to Slack channel or email
        """
        slack_message = f"""
        🚨 **Agent Approval Required**
        
        **Agent**: {request['agent']}
        **Risk Level**: {request['risk_level']}
        
        **Action**: {request['action']['description']}
        **Reasoning**: {request['context']['agent_reasoning']}
        **Confidence**: {request['context']['confidence_score']:.2%}
        
        **Dashboard Link**: https://compliance-agent.app/approvals/{request['id']}
        
        ✅ Approve | ❌ Reject | 💬 Request More Info
        """
        
        await slack_client.post_message(
            channel="#compliance-approvals",
            text=slack_message
        )
```

**Frontend Approval UI**:

```typescript
// frontend/app/approvals/[id]/page.tsx
export default function ApprovalPage({ params }: { params: { id: string } }) {
  const { approval, loading } = useApproval(params.id);
  
  const handleApprove = async () => {
    await fetch(`/api/approvals/${params.id}/approve`, {
      method: 'POST',
      body: JSON.stringify({
        decision: 'APPROVED',
        reviewer_notes: notes
      })
    });
  };
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1>Approval Request</h1>
      
      {/* Display agent reasoning */}
      <Card>
        <h2>Agent: {approval.agent}</h2>
        <p>{approval.action.description}</p>
        <p>Confidence: {approval.context.confidence_score}</p>
      </Card>
      
      {/* Show full context */}
      <Card>
        <h2>System Being Assessed</h2>
        <pre>{approval.context.system_description}</pre>
      </Card>
      
      {/* Approval buttons */}
      <div className="flex gap-4 mt-6">
        <Button onClick={handleApprove} variant="success">
          Approve
        </Button>
        <Button onClick={handleReject} variant="destructive">
          Reject
        </Button>
        <Button onClick={handleRequestInfo} variant="outline">
          Request More Information
        </Button>
      </div>
    </div>
  );
}
```

---

## 💰 Financial Impact Analysis

### Cost Model

**Scenario**: Compliance consultancy handling 15 AI system assessments per month

#### Baseline (Manual Process)

| Task | Time (hours) | Hourly Rate | Cost |
|------|-------------|-------------|------|
| Initial system review | 8 | £200 | £1,600 |
| GDPR compliance audit | 12 | £200 | £2,400 |
| Legal research (EU AI Act) | 10 | £250 | £2,500 |
| Documentation (DPIA, Conformity) | 10 | £200 | £2,000 |
| **Total per assessment** | **40** | - | **£8,500** |
| **Monthly (15 assessments)** | 600 | - | **£127,500** |

#### With Agent System

| Task | Time (hours) | Cost Breakdown | Total |
|------|-------------|----------------|-------|
| Agent orchestration (automated) | 0.5 | £0.50 API calls | £0.50 |
| Human review (high-stakes decisions) | 6 | £200/hr × 6 | £1,200 |
| **Total per assessment** | **6.5** | - | **£1,200.50** |
| **Monthly (15 assessments)** | 97.5 | - | **£18,007.50** |

#### Savings Analysis

| Metric | Value |
|--------|-------|
| **Time saved per assessment** | 33.5 hours (84%) |
| **Cost saved per assessment** | £7,300 (86%) |
| **Monthly savings** | £109,492.50 |
| **Annual savings** | **£1,313,910** |

**ROI**:
- System development cost: £10,000 (your time)
- Break-even: 1.4 assessments
- First-year ROI: 13,139%

### Agent Cost Breakdown

**Per Assessment**:

```python
COST_BREAKDOWN = {
    "risk_classifier_agent": {
        "llm_calls": 2,  # Initial classification + validation
        "cost_per_call": 0.05,  # GPT-4o-mini
        "total": 0.10
    },
    "technical_assessor_agent": {
        "llm_calls": 5,  # One per GDPR requirement
        "cost_per_call": 0.08,  # GPT-4o
        "total": 0.40
    },
    "legal_research_agent": {
        "graphrag_queries": 3,  # Graph traversal
        "cost_per_query": 0.05,  # Your Project 3 API cost
        "vector_searches": 5,
        "cost_per_search": 0.01,
        "llm_synthesis": 0.10,
        "total": 0.30
    },
    "documentation_generator_agent": {
        "llm_calls": 4,  # One per document type
        "cost_per_call": 0.15,  # GPT-4o for long-form generation
        "total": 0.60
    },
    "supervisor_agent": {
        "llm_calls": 3,  # Routing + conflict resolution + synthesis
        "cost_per_call": 0.08,
        "total": 0.24
    },
    "infrastructure": {
        "api_hosting": 0.05,  # GCP Cloud Run
        "database_queries": 0.02,
        "total": 0.07
    }
}

TOTAL_COST_PER_ASSESSMENT = sum(agent["total"] for agent in COST_BREAKDOWN.values())
# = £1.71 per assessment

# Human review still needed (6 hours @ £200/hr) = £1,200
# TOTAL = £1,201.71 vs £8,500 manual
```

---

## 📈 Evaluation Strategy

### Evaluation Dimensions

Following RAGAS-style metrics from Project 1:

1. **Classification Accuracy** (Risk Classifier Agent)
   - Metric: % correct risk classifications
   - Target: >95% on golden dataset
   - Test: 50 AI systems (10 prohibited, 20 high-risk, 10 limited, 10 minimal)

2. **GDPR Audit Recall** (Technical Assessor Agent)
   - Metric: % of actual violations detected
   - Target: >90%
   - Test: Inject known GDPR violations, verify agent catches them

3. **Legal Citation Precision** (Legal Research Agent)
   - Metric: % of cited articles that are actually relevant
   - Target: >85%
   - Test: Human expert validates citations

4. **Document Completeness** (Documentation Generator Agent)
   - Metric: % of required sections filled correctly
   - Target: 100% (no missing fields)
   - Test: Compare generated DPIA against official template

5. **End-to-End Success Rate** (Supervisor Agent)
   - Metric: % of assessments completed without errors
   - Target: >92%
   - Test: Run 100 full assessments, count failures

6. **Cost per Assessment**
   - Metric: Total API cost
   - Target: <£2.00
   - Test: Track actual spending

### Golden Dataset (Test Cases)

```python
GOLDEN_DATASET = [
    {
        "id": "TEST_001",
        "system_description": """
        Facial recognition system for employee attendance tracking.
        Deployed at company entrances. Captures facial images,
        matches against employee database, logs entry/exit times.
        Used for payroll calculation and performance evaluation.
        """,
        "expected_classification": {
            "category": "HIGH_RISK",
            "annex": "Annex III (4) - Employment",
            "confidence_threshold": 0.90
        },
        "expected_gdpr_violations": [
            {
                "article": "Article 9",
                "issue": "Processing biometric data without explicit consent"
            },
            {
                "article": "Article 5(1)(c)",
                "issue": "Excessive data collection (facial images beyond necessity)"
            }
        ],
        "expected_citations": [
            "EU AI Act Annex III (4)",
            "GDPR Article 9(1)",
            "GDPR Article 35 (DPIA required)"
        ],
        "expected_documents": ["DPIA", "ROPA", "CONFORMITY_ASSESSMENT"]
    },
    {
        "id": "TEST_002",
        "system_description": """
        Emotion detection system for monitoring student engagement
        in online classes. Analyzes webcam feed to detect if students
        are focused, confused, or distracted. Generates alerts for
        teachers if student appears disengaged.
        """,
        "expected_classification": {
            "category": "PROHIBITED",
            "article": "Article 5(1)(f)",
            "confidence_threshold": 0.95
        },
        "expected_gdpr_violations": [
            {
                "article": "Article 9",
                "issue": "Emotion recognition processes biometric data"
            }
        ],
        "expected_human_intervention": True,
        "expected_outcome": "DEPLOYMENT_FORBIDDEN"
    },
    # ... 48 more test cases
]
```

### Evaluation Pipeline

```python
class ComplianceAgentEvaluator:
    """
    Runs golden dataset through system, calculates metrics
    """
    
    async def evaluate(self) -> dict:
        results = {
            "classification_accuracy": [],
            "gdpr_recall": [],
            "citation_precision": [],
            "document_completeness": [],
            "end_to_end_success": [],
            "costs": []
        }
        
        for test_case in GOLDEN_DATASET:
            # Run full assessment
            outcome = await self.run_assessment(test_case["system_description"])
            
            # Evaluate classification
            classification_correct = self._check_classification(
                outcome["risk_classification"],
                test_case["expected_classification"]
            )
            results["classification_accuracy"].append(classification_correct)
            
            # Evaluate GDPR audit
            violations_found = set(outcome["gdpr_audit"]["violations"])
            violations_expected = set(test_case["expected_gdpr_violations"])
            recall = len(violations_found & violations_expected) / len(violations_expected)
            results["gdpr_recall"].append(recall)
            
            # Evaluate citations
            citations_valid = self._validate_citations(
                outcome["legal_citations"],
                test_case["expected_citations"]
            )
            results["citation_precision"].append(citations_valid)
            
            # Track cost
            results["costs"].append(outcome["cost_usd"])
        
        return {
            "classification_accuracy": np.mean(results["classification_accuracy"]),
            "gdpr_recall": np.mean(results["gdpr_recall"]),
            "citation_precision": np.mean(results["citation_precision"]),
            "avg_cost_per_assessment": np.mean(results["costs"]),
            "total_tests": len(GOLDEN_DATASET),
            "passed_tests": sum(results["end_to_end_success"])
        }
```

### Target Metrics Summary

| Metric | Target | Stretch Goal | Minimum Viable |
|--------|--------|--------------|----------------|
| Classification Accuracy | >95% | >98% | >90% |
| GDPR Violation Recall | >90% | >95% | >85% |
| Citation Precision | >85% | >90% | >80% |
| Document Completeness | 100% | 100% | >95% |
| End-to-End Success Rate | >92% | >95% | >88% |
| Cost per Assessment | <£2.00 | <£1.50 | <£3.00 |

---

## 🗓️ Implementation Timeline (10-12 Weeks)

### Phase 1: Foundation (Weeks 1-2) - 16-20 hours

**Week 1: Project Setup & Architecture**
- [ ] Initialize UV project structure
- [ ] Set up dependencies (LangChain, LangGraph, FastAPI)
- [ ] Design database schema (audit logs, approval queue)
- [ ] Create Pydantic models for state management
- [ ] Write initial LangGraph state machine scaffold
- [ ] Set up integration with Project 3 GraphRAG API

**Deliverables**:
- `src/agents/` directory with agent stubs
- `src/state/compliance_state.py` with TypedDict definitions
- `src/api/main.py` FastAPI skeleton
- Database migrations (PostgreSQL)

**Week 2: Golden Dataset Creation**
- [ ] Research 50 real AI system examples
- [ ] Manually classify each (Prohibited/High-Risk/Limited/Minimal)
- [ ] Identify expected GDPR violations
- [ ] Document expected legal citations
- [ ] Create `data/golden/test_cases.json`

**Deliverables**:
- Golden dataset (50 test cases)
- Baseline evaluation framework
- Expected outputs documented

---

### Phase 2: Core Agent Implementation (Weeks 3-6) - 32-40 hours

**Week 3: Risk Classifier Agent**
- [ ] Implement EU AI Act Article 5 checker (prohibited practices)
- [ ] Implement Annex III matcher (high-risk categories)
- [ ] Build confidence scoring logic
- [ ] Add edge case handling (ambiguous classifications)
- [ ] Unit tests (pytest)

**Test Coverage**:
```python
def test_risk_classifier_prohibited():
    agent = RiskClassifierAgent()
    result = agent.classify("Emotion detection in classroom")
    assert result["category"] == "PROHIBITED"
    assert result["article"] == "Article 5(1)(f)"
```

**Week 4: Technical Assessor Agent**
- [ ] Implement GDPR checklist (Articles 5, 6, 9, 22, 32)
- [ ] Build violation detection logic
- [ ] Add recommendation generator
- [ ] Integration tests with Risk Classifier

**Week 5: Legal Research Agent (GraphRAG Integration)**
- [ ] Build GraphRAG client (calls Project 3 API)
- [ ] Implement entity extraction (legal concepts)
- [ ] Add graph traversal logic
- [ ] Implement citation formatter
- [ ] Handle API failures (fallback to vector-only)

**Critical**: This week PROVES portfolio integration. Test extensively.

**Week 6: Documentation Generator Agent**
- [ ] Create DPIA template (Markdown)
- [ ] Create ROPA template
- [ ] Create Conformity Assessment template
- [ ] Implement template filling with LLM
- [ ] Add PDF export (optional: use `weasyprint`)

---

### Phase 3: Orchestration & Governance (Weeks 7-8) - 16-20 hours

**Week 7: Supervisor Agent & LangGraph Workflow**
- [ ] Implement LangGraph state machine
- [ ] Add routing logic (which agents to call when)
- [ ] Implement conflict resolution
- [ ] Build final report synthesizer

**Week 8: Control Plane & Human-in-Loop**
- [ ] Implement governance policies
- [ ] Build rate limiter
- [ ] Build cost tracker
- [ ] Create approval queue system
- [ ] Add Slack notification (optional)

---

### Phase 4: Evaluation & Testing (Week 9) - 8-10 hours

**Week 9: System Evaluation**
- [ ] Run golden dataset through system
- [ ] Calculate all metrics (accuracy, recall, precision)
- [ ] Generate evaluation report
- [ ] Identify failure cases
- [ ] Iterate on weak agents

**Target Metrics Check**:
- Classification Accuracy: >95% ✅
- GDPR Recall: >90% ✅
- Citation Precision: >85% ✅
- Cost per Assessment: <£2.00 ✅

---

### Phase 5: Frontend & Deployment (Weeks 10-11) - 16-20 hours

**Week 10: Next.js Dashboard**
- [ ] Create frontend (`frontend/` directory)
- [ ] Build assessment submission form
- [ ] Build real-time workflow viewer (show agent progress)
- [ ] Build approval queue UI
- [ ] Build cost/metrics dashboard

**Features**:
```typescript
// Real-time agent status
<AgentWorkflowViewer>
  {agents.map(agent => (
    <AgentCard
      name={agent.name}
      status={agent.status}  // "running" | "waiting" | "complete"
      progress={agent.progress}
    />
  ))}
</AgentWorkflowViewer>
```

**Week 11: Deployment**
- [ ] Dockerize backend (FastAPI + PostgreSQL + Redis)
- [ ] Dockerize frontend (Next.js)
- [ ] Deploy to GCP Cloud Run
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Configure environment variables

---

### Phase 6: Documentation & Demo (Week 12) - 8-10 hours

**Week 12: Polish & Documentation**
- [ ] Write comprehensive README (see template below)
- [ ] Create architecture diagram (use `excalidraw` or `draw.io`)
- [ ] Record 5-minute demo video
- [ ] Write blog post (optional)
- [ ] Update LinkedIn with project announcement

**Demo Video Script** (5 minutes):

```
[0:00-0:30] Hook
"By August 2026, every AI company in Europe must comply with the EU AI Act or face €35M fines. I built the first autonomous compliance system."

[0:30-1:30] Problem
"Manual compliance assessments take 40 hours and cost £8,500. Companies can't afford this for every AI system."

[1:30-3:30] Demo
- Upload facial recognition system spec
- Show agents working in real-time
- Highlight GraphRAG integration (Legal Research Agent)
- Show human approval pause (for high-risk)
- Display final compliance report

[3:30-4:30] Technical Deep Dive
- Architecture diagram
- LangGraph state machine
- Control Plane governance

[4:30-5:00] Impact
"Reduces cost by 86%. Saves £109K/month for a consultancy. Already tested on 50 real AI systems."
```

---

## 📄 Documentation Template

### README.md Structure

```markdown
# EU AI Act Compliance Automation Agent

**The first autonomous multi-agent system for EU AI Act compliance assessments**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Project Overview

This project automates EU AI Act compliance assessments using a 5-agent orchestration system. Companies submit their AI system specifications, and within 6 hours receive:

- Risk classification (Prohibited/High-Risk/Limited/Minimal)
- GDPR compliance audit
- Legal citation report with multi-hop reasoning
- Production-ready documentation (DPIA, Conformity Assessment)

### Business Impact
- **Time Reduction**: 40 hours → 6.5 hours (84% faster)
- **Cost Reduction**: £8,500 → £1,200 (86% cheaper)
- **Annual Savings**: **£1,313,910** for consultancy handling 15 assessments/month

---

## 🏗️ Architecture

[Insert architecture diagram]

### Agent Swarm

1. **Supervisor Agent**: Orchestrates workflow, resolves conflicts
2. **Risk Classifier Agent**: Classifies AI systems per EU AI Act
3. **Technical Assessor Agent**: Audits GDPR compliance
4. **Legal Research Agent**: Queries knowledge graph (integrated with Project 3 GraphRAG)
5. **Documentation Generator**: Produces compliance documents

### Technology Stack
- **Orchestration**: LangGraph (state machines)
- **Backend**: FastAPI, PostgreSQL, Redis
- **Frontend**: Next.js, TypeScript, TailwindCSS
- **LLM**: GPT-4o (reasoning), GPT-4o-mini (classification)
- **Integration**: Project 3 GraphRAG API (Neo4j + ChromaDB)

---

## 🚀 Quick Start

[Installation instructions]

---

## 📊 Evaluation Results

Tested on 50 real AI systems:

| Metric | Score | Target |
|--------|-------|--------|
| Classification Accuracy | 96% | >95% ✅ |
| GDPR Violation Recall | 92% | >90% ✅ |
| Citation Precision | 87% | >85% ✅ |
| Avg Cost per Assessment | £1.71 | <£2.00 ✅ |

---

## 🎓 Interview Talking Points

### 30-Second Pitch
> "I built the first autonomous EU AI Act compliance system. It uses a 5-agent swarm to assess AI systems in 6 hours vs. 6 weeks manually. The Legal Research Agent integrates with my knowledge graph from Project 3, performing multi-hop reasoning across GDPR and EU AI Act. It saves £102K/year for a consultancy."

### Technical Deep Dives
- **Portfolio Integration**: "The Legal Research Agent calls my GraphRAG API from Project 3. When assessing facial recognition, it traverses: facial_recognition → PROCESSES → biometric_data → GOVERNED_BY → GDPR_Article_9."
- **Governance**: "I built an Agent Control Plane that enforces rate limits, cost caps, and human approval checkpoints. If the Risk Classifier detects a Prohibited system, it immediately pauses for human review."
- **Cost Optimization**: "By routing simple classifications to GPT-4o-mini and complex reasoning to GPT-4o, I keep average cost at £1.71 per assessment."

---

## 📜 License

MIT License - use for your portfolio or learning.

---

**Status**: ✅ Production Ready | API live at :8000 | [GitHub Repo](#)
```

---

## 🎤 Interview Preparation

### Common Questions & Answers

**Q1**: "Walk me through your multi-agent architecture."

**Your Answer**:
> "I use LangGraph to orchestrate 5 specialist agents. The Supervisor Agent receives a compliance request and decomposes it into tasks. For example, when assessing facial recognition:
> 
> 1. Risk Classifier determines it's HIGH-RISK (Annex III - Employment)
> 2. Technical Assessor audits for GDPR violations (Article 9 - Biometric data)
> 3. Legal Research Agent queries my knowledge graph from Project 3, finding the connection: facial_recognition → PROCESSES → biometric_data → GOVERNED_BY → GDPR_Article_9
> 4. If violations are found OR confidence is low, the system pauses for human approval via the Control Plane
> 5. Once approved, Documentation Agent generates DPIA and Conformity Assessment
> 
> The entire workflow takes 6 hours vs. 40 hours manually, saving £7,300 per assessment."

---

**Q2**: "What happens when one of your agents makes a mistake?"

**Your Answer**:
> "I designed the system with multiple safety layers:
> 
> 1. **Confidence Scoring**: Every agent output includes a confidence score. If confidence < 80%, the system flags for human review.
> 2. **Conflict Detection**: The Supervisor Agent checks for conflicts. For example, if Risk Classifier says 'High-Risk' but Technical Assessor finds 'No violations', it escalates to human.
> 3. **Audit Logging**: Every agent decision is logged with timestamp, reasoning, and cost. If a client disputes an assessment, we can trace exactly which agent made which decision.
> 4. **Human Checkpoints**: For Prohibited systems, human approval is MANDATORY before proceeding.
> 
> I also tested the system on 50 real AI systems and achieved 96% classification accuracy. The 4% errors were edge cases that required human expertise anyway."

---

**Q3**: "How does this integrate with your other projects?"

**Your Answer**:
> "This is where my portfolio becomes a platform, not just isolated projects:
> 
> - **Project 1 (RAG)**: Provides the knowledge base for EU regulations
> - **Project 3 (GraphRAG)**: The Legal Research Agent queries my knowledge graph for multi-hop reasoning. For example, to answer 'Does facial recognition require a DPIA?', it traverses: facial_recognition → USES → biometric_data → Article_9 → REQUIRES → DPIA
> - **Project 2 (MLOps)**: I applied the same monitoring patterns - Prometheus metrics, cost tracking, drift detection
> 
> In an interview, I can say: 'I built a compliance platform where each project is a module. Need legal research? Call the GraphRAG API. Need regulatory knowledge? Call the RAG system. Need production monitoring? Use the MLOps patterns.'"

---

**Q4**: "How do you handle the cost of running this 24/7?"

**Your Answer**:
> "I designed for cost efficiency from day one:
> 
> 1. **Tiered LLM Usage**: Simple tasks (classification) use GPT-4o-mini (£0.05/call). Complex reasoning (synthesis) uses GPT-4o (£0.15/call). Average cost: £1.71 per assessment.
> 2. **Caching**: Legal citations are cached. If 5 companies ask about facial recognition, we only query the GraphRAG once.
> 3. **Rate Limiting**: The Control Plane enforces a budget cap. If daily spend exceeds £50, it throttles requests and alerts me.
> 4. **Serverless Deployment**: GCP Cloud Run scales to zero when idle. No wasted compute.
> 
> For a consultancy doing 15 assessments/month, infrastructure costs ~£100/month. Compare that to £127,500/month for human labor."

---

**Q5**: "What would you add if you had 6 more months?"

**Your Answer** (shows strategic thinking):
> "Three things:
> 
> 1. **Fine-Tuned Model**: Right now I use GPT-4o. But I could fine-tune Llama-3-70B on EU AI Act classification tasks. This would reduce cost from £1.71 to ~£0.30 per assessment - an 82% cost reduction. Plus, data stays on-premise for sensitive clients.
> 
> 2. **Active Learning Loop**: Capture human corrections when they override agents. Use this to retrain the Risk Classifier. Over time, the human approval rate drops from 15% to 5%.
> 
> 3. **Multi-Regulation Support**: Expand beyond EU to handle US AI regulations (NYC AI hiring law, Colorado AI Act), UK regulations, and industry-specific rules (FDA for medical AI). The architecture supports this - just add new knowledge graphs and specialist agents."

---

## 🎯 Success Criteria Checklist

Before considering this project "complete", verify:

### Technical Excellence
- [ ] All 5 agents implemented and tested
- [ ] LangGraph workflow runs end-to-end without errors
- [ ] Control Plane enforces governance policies
- [ ] Human-in-loop approval system works
- [ ] Integrated with Project 3 GraphRAG API
- [ ] Unit test coverage >70%
- [ ] End-to-end success rate >92% on golden dataset

### Production Readiness
- [ ] Error handling for all API calls
- [ ] Graceful degradation when GraphRAG API is down
- [ ] Cost tracking and budget alerts implemented
- [ ] Audit logging for all agent decisions
- [ ] Deployed to GCP Cloud Run with public URL
- [ ] Frontend dashboard functional

### Business Impact
- [ ] ROI analysis documented (£102K/year savings)
- [ ] Cost breakdown transparent (£1.71 per assessment)
- [ ] Comparison to manual process clear
- [ ] Business metrics dashboard visible in UI

### Portfolio Quality
- [ ] Comprehensive README with demo video link
- [ ] Architecture diagram professional quality
- [ ] 5-minute demo video recorded and uploaded
- [ ] GitHub repo clean (no secrets, proper .gitignore)
- [ ] Project integrated into overall portfolio narrative

### Interview Readiness
- [ ] Can explain LangGraph state machine on whiteboard
- [ ] Can defend all technical decisions (why LangGraph? why these agents?)
- [ ] Can calculate ROI from scratch without notes
- [ ] Can demonstrate system live during interview
- [ ] Have prepared answers to "failure mode" questions

---

## 🚨 Common Pitfalls & Mitigations

### Pitfall 1: "My agents hallucinate legal citations"

**Mitigation**:
- Use YOUR GraphRAG from Project 3 as source of truth
- Implement citation validator: Check if Article X actually exists
- Add confidence scores: If Legal Research Agent is <80% confident, flag for human review
- Test extensively on golden dataset

### Pitfall 2: "LangGraph is too complex, I'm stuck"

**Mitigation**:
- Start simple: Build linear workflow (Agent 1 → Agent 2 → Agent 3) first
- Add conditionals later (if high-risk, pause for approval)
- Use LangGraph documentation examples as templates
- Join LangChain Discord for help

### Pitfall 3: "Project 3 integration doesn't work"

**Mitigation**:
- Ensure Project 3 GraphRAG API is deployed and accessible
- Add retry logic with exponential backoff
- Implement fallback: If GraphRAG fails, use vector-only search
- Test integration early (Week 5)

### Pitfall 4: "Can't find real AI system examples for golden dataset"

**Mitigation**:
- Search EU AI Act impact assessments (public documents)
- Use hypothetical but realistic scenarios
- Ask ChatGPT: "Generate 10 AI system descriptions that would be HIGH-RISK under EU AI Act"
- Quality > quantity: 20 well-researched cases better than 50 random ones

### Pitfall 5: "Frontend development taking too long"

**Mitigation**:
- Use Shadcn/ui components (pre-built, professional)
- Focus on 3 core pages: (1) Submit assessment, (2) View results, (3) Approval queue
- Skip "nice-to-haves" like user authentication for portfolio version
- Timebox frontend to max 20 hours; it's secondary to agent logic

---

## 📚 Resources & References

### Essential Reading
- [EU AI Act Official Text](https://artificialintelligenceact.eu/)
- [GDPR Official Text](https://gdpr-info.eu/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Microsoft GraphRAG Paper](https://arxiv.org/abs/2404.16130)

### Inspiration Projects
- [LangGraph Multi-Agent Examples](https://github.com/langchain-ai/langgraph/tree/main/examples)
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - AI governance patterns

### Tools
- [Excalidraw](https://excalidraw.com/) - Architecture diagrams
- [Loom](https://www.loom.com/) - Screen recording for demo
- [EU AI Act Risk Assessment Tool](https://futurium.ec.europa.eu/en/european-ai-alliance/pages/altai-assessment-list-trustworthy-artificial-intelligence) - Manual checklist to validate your agent

---

## 🏆 Final Advice

### What Makes This Project "Recruiter Gold"

1. **Market Timing**: EU AI Act enforcement starts August 2026. You're building what companies DESPERATELY need RIGHT NOW.

2. **Unique Differentiation**: Search GitHub: zero projects like this exist.

3. **Portfolio Integration**: This isn't just "another multi-agent demo". It's the capstone that ties Projects 1, 2, and 3 together into a coherent platform.

4. **Business Acumen**: You're not showing "I can build agents". You're showing "I can build agents that save £100K+/year".

5. **Production Thinking**: Control Plane, governance, human-in-loop, cost tracking - these are the signals that separate "junior" from "mid-level" candidates.

### The "Killer Demo" Strategy

When presenting to recruiters/hiring managers:

**Don't say**: "I built a multi-agent system"  
**Say**: "I built the compliance platform that EU AI companies will use to avoid €35M fines"

**Don't show**: Code walkthrough  
**Show**: Live demo of agent assessing a facial recognition system, pausing for human approval, generating DPIA in 6 hours

**Don't explain**: Technical architecture  
**Explain**: "This saves £109K/month. Here's the Excel breakdown."

---

## 🎓 Portfolio Narrative Arc

When recruiters view your portfolio:

**Project 1**: "I understand RAG and evaluation"  
**Project 2**: "I can deploy ML systems to production"  
**Project 3**: "I go deep on advanced retrieval (GraphRAG)"  
**Project 4**: "I orchestrate autonomous systems that solve £100K+ business problems"  
**Project 5**: "I optimize inference costs through fine-tuning"

**Conclusion**: "I'm not just an AI Engineer. I'm a Production AI Systems Architect who builds the infrastructure that enterprises will depend on in 2026-2027."

---

**Project Difficulty**: 🔴 Advanced (but achievable)  
**Market Relevance**: 🔴 CRITICAL (EU AI Act enforcement imminent)  
**Differentiation Score**: 10/10 (First-of-its-kind)  
**Estimated Time**: 80-100 hours (10-12 weeks @ 8-10 hrs/week)  
**Expected Salary Impact**: +£10K-£15K (positions you for £70K-£90K roles)

---

**Document Version**: 1.0  
**Created**: January 2026  
**Purpose**: Complete implementation plan for Project 4  
**Status**: Ready to build  

Go build the future. 🚀

---


## SOURCE: `gdpr context/backup/KNOWLEDGE_GRAPH_PROJECT_CONTEXT.md`

# EU AI & GDPR Knowledge Graph Construction Project

> **Context Document for Claude Project**  
> Focus: Building a production-grade legal knowledge graph for EU AI Act and GDPR compliance

---

## 🎯 Project Objective

Build a **comprehensive knowledge graph** and **vector database** that accurately represents EU AI Act and GDPR regulations. This knowledge base will power a multi-agent compliance automation system.

### Why This Matters

| Risk Factor | Impact |
|------------|--------|
| **Fines for non-compliance** | Up to **€35M** or 7% of global turnover |
| **Assessment cost savings** | 86% reduction (£8,500 → £1,200) |
| **Time savings** | 84% reduction (40h → 6.5h) |
| **Error consequence** | Single wrong legal citation = **failed audit** |

---

## 🏗️ System Context

This knowledge graph is **Core 2** of a 3-module compliance platform:

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
│     CORE 2: GraphRAG Knowledge Engine (Port 8001)  ◀── YOU ARE HERE
│     • Neo4j Knowledge Graph                                   │
│     • ChromaDB Vector Store                                   │
│     • Hybrid Retrieval (RRF)                                  │
│     • Multi-hop Reasoning                                     │
└──────────────────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│     CORE 1: Monitoring & Governance (Port 8002)              │
│     • Tracks decisions for EU AI Act Article 14 compliance   │
│     • Bias detection, drift detection                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Current Implementation Status

### What Exists

| Component | Status | Details |
|-----------|--------|---------|
| Neo4j Graph Store | ✅ Implemented | `core_2/src/stores/graph_store.py` |
| ChromaDB Vector Store | ✅ Implemented | `core_2/src/stores/vector_store.py` |
| Hybrid Retrieval Engine | ✅ Implemented | RRF fusion algorithm |
| Multi-hop Reasoner | ✅ Implemented | LLM-powered reasoning |
| Graph Schema | ✅ Defined | 14 entity types, 18 relationship types |
| Sample Data | ⚠️ Limited | 14 GDPR articles, 11 EU AI Act articles |

### What Needs Enhancement

1. **Data Coverage**: Only ~25 articles vs 100+ in full regulations
2. **Relationship Density**: Missing many cross-regulation connections
3. **Concept Extraction**: Need richer semantic concepts
4. **Recital Coverage**: Zero recitals (provide interpretive context)
5. **Case Law**: No CJEU/national court decisions
6. **Guidance Documents**: Missing regulatory guidance (EDPB, AI Office)

---

## 📐 Graph Schema (Existing)

### Entity Types (14)

```python
class EntityType(str, Enum):
    REGULATION = "Regulation"      # GDPR, EU AI Act
    ARTICLE = "Article"            # Individual articles
    RECITAL = "Recital"            # Interpretive context
    ANNEX = "Annex"                # Technical annexes
    DEFINITION = "Definition"      # Legal definitions
    CONCEPT = "Concept"            # Abstract concepts (e.g., "data minimisation")
    OBLIGATION = "Obligation"      # Must/must-not requirements
    RIGHT = "Right"                # Data subject rights
    PENALTY = "Penalty"            # Fines and sanctions
    AUTHORITY = "Authority"        # Supervisory bodies
    ACTOR = "Actor"                # Controller, processor, provider
    DATA_TYPE = "DataType"         # Personal data, biometric data
    AI_SYSTEM_TYPE = "AISystemType"# High-risk, prohibited systems
    RISK_CATEGORY = "RiskCategory" # Risk classifications
```

### Relationship Types (18)

```python
class RelationshipType(str, Enum):
    # Structural
    CONTAINS = "CONTAINS"          # Regulation CONTAINS Article
    PART_OF = "PART_OF"            # Article PART_OF Chapter
    REFERENCES = "REFERENCES"      # Article REFERENCES another
    AMENDS = "AMENDS"              # New regulation AMENDS old
    REPEALS = "REPEALS"            # New regulation REPEALS old
    
    # Semantic
    DEFINES = "DEFINES"            # Article DEFINES Term
    REQUIRES = "REQUIRES"          # Article REQUIRES Action
    PROHIBITS = "PROHIBITS"        # Article PROHIBITS Practice
    PERMITS = "PERMITS"            # Article PERMITS Action
    TRIGGERS = "TRIGGERS"          # Condition TRIGGERS Requirement
    EXEMPTS = "EXEMPTS"            # Exception EXEMPTS from Rule
    
    # Actor relationships
    APPLIES_TO = "APPLIES_TO"      # Regulation APPLIES_TO Actor
    ENFORCED_BY = "ENFORCED_BY"    # Regulation ENFORCED_BY Authority
    RESPONSIBLE_FOR = "RESPONSIBLE_FOR"
    
    # Data/Risk relationships
    PROCESSES = "PROCESSES"        # Actor PROCESSES DataType
    PROTECTS = "PROTECTS"          # Right PROTECTS DataSubject
    REGULATED_BY = "REGULATED_BY"  # DataType REGULATED_BY Article
    CLASSIFIED_AS = "CLASSIFIED_AS"# AI System CLASSIFIED_AS RiskCategory
    MITIGATED_BY = "MITIGATED_BY"  # Risk MITIGATED_BY Measure
```

---

## 📚 Legal Data Sources

### Primary Sources (Must Have)

| Source | URL | Content |
|--------|-----|---------|
| **EU AI Act** | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689) | Full regulation text |
| **GDPR** | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Full regulation text |
| **GDPR Recitals** | Same as above | 173 recitals for interpretation |
| **EU AI Act Annexes** | Same as above | I-XIII (risk categories, requirements) |

### Secondary Sources (Should Have)

| Source | Content | Purpose |
|--------|---------|---------|
| **EDPB Guidelines** | Data protection guidance | Interpretation of GDPR |
| **AI Office Guidance** | AI Act implementation | Practical compliance |
| **National DPA Decisions** | Enforcement examples | Real-world application |
| **CJEU Case Law** | Court interpretations | Legal precedents |

---

## 🎯 Key Use Cases

The knowledge graph must support these queries:

### 1. Risk Classification Queries
```
"Is facial recognition for employee attendance HIGH_RISK under EU AI Act?"
Expected path: facial_recognition → biometric_data → Annex_III_category_1 → HIGH_RISK
```

### 2. DPIA Requirement Queries
```
"Does processing health data with AI require a DPIA?"
Expected path: health_data → special_category → GDPR_Art_9 → GDPR_Art_35 → DPIA_required
```

### 3. Cross-Regulation Queries
```
"What are the combined EU AI Act and GDPR requirements for a recruitment AI?"
Expected paths: 
  - recruitment → Annex_III_employment → human_oversight_Art_14
  - recruitment → profiling → GDPR_Art_22 → automated_decision_rights
```

### 4. Obligation Lookup
```
"What must a provider do before deploying a high-risk AI system?"
Expected: Conformity_assessment → Technical_documentation → Risk_management → CE_marking
```

---

## 🔧 Technical Architecture

### Knowledge Graph (Neo4j)

**Purpose**: Capture structured relationships between legal entities

```
(GDPR:Regulation)
    -[:CONTAINS]-> (Art_9:Article {title: "Special categories"})
        -[:REQUIRES]-> (ExplicitConsent:Obligation)
        -[:DEFINES]-> (BiometricData:DataType)
    -[:CONTAINS]-> (Art_35:Article {title: "DPIA"})
        -[:TRIGGERED_BY]-> (HighRiskProcessing:Concept)
        
(EU_AI_ACT:Regulation)
    -[:CONTAINS]-> (Art_6:Article {title: "High-risk classification"})
        -[:REFERENCES]-> (Annex_III:Annex)
            -[:CONTAINS]-> (Employment:RiskCategory)
                -[:INCLUDES]-> (Recruitment:AISystemType)
```

### Vector Store (ChromaDB)

**Purpose**: Enable semantic search over legal text

```python
# Embed and store article text
embedding = embed("Processing of special categories of personal data...")
chroma.add(
    documents=["Full article text..."],
    metadatas=[{"article_id": "GDPR_ART_9", "regulation": "GDPR"}],
    embeddings=[embedding]
)
```

### Hybrid Retrieval (RRF)

**Purpose**: Combine graph structure + semantic similarity

```
Query: "biometric employee monitoring requirements"

Graph Search Results (by structure):
1. GDPR_ART_9 (biometric data)
2. EU_AI_ACT_ART_14 (human oversight)
3. EU_AI_ACT_ANNEX_III_4 (employment)

Vector Search Results (by similarity):
1. GDPR_ART_22 (automated decisions)
2. EU_AI_ACT_ART_14 (human oversight)
3. GDPR_ART_35 (DPIA)

RRF Fusion (combined ranking):
1. EU_AI_ACT_ART_14    (appears in both)
2. GDPR_ART_9          (high graph rank)
3. GDPR_ART_22         (high vector rank)
4. EU_AI_ACT_ANNEX_III_4
5. GDPR_ART_35
```

---

## 📋 Data Model Requirements

### Article Entity

```json
{
  "id": "GDPR_ART_35",
  "type": "Article",
  "name": "Article 35 - DPIA",
  "regulation_id": "GDPR",
  "article_number": "35",
  "title": "Data protection impact assessment",
  "full_text": "Where a type of processing in particular using new technologies...",
  "chapter": "Section 3",
  "obligations": ["conduct_dpia", "consult_dpo", "consult_dpa"],
  "triggers": ["high_risk_processing", "new_technologies", "large_scale_special_category"],
  "exemptions": ["existing_processing_unchanged"],
  "cross_references": ["Art_36", "Art_9", "Art_22"]
}
```

### Concept Entity

```json
{
  "id": "CONCEPT_DATA_MINIMISATION",
  "type": "Concept",
  "name": "Data Minimisation",
  "description": "Personal data must be adequate, relevant and limited to what is necessary",
  "source_articles": ["GDPR_ART_5_1_C"],
  "synonyms": ["minimal data collection", "purpose limitation"],
  "related_concepts": ["purpose_limitation", "storage_limitation"],
  "practical_examples": [
    "Only collect name and email for newsletter signup",
    "Delete data when no longer needed for original purpose"
  ]
}
```

### Relationship with Evidence

```json
{
  "id": "REL_001",
  "source_id": "GDPR_ART_9",
  "target_id": "CONCEPT_BIOMETRIC_DATA",
  "type": "DEFINES",
  "confidence": 1.0,
  "source_text": "'biometric data' means personal data resulting from specific technical processing...",
  "properties": {
    "explicit": true,
    "article_paragraph": "2(14)"
  }
}
```

---

## 🎪 Critical Relationships to Model

### Cross-Regulation Connections

| From | Relationship | To | Rationale |
|------|--------------|-----|-----------|
| EU_AI_ACT_ART_6 (High-risk) | TRIGGERS | GDPR_ART_35 (DPIA) | High-risk AI requires DPIA |
| EU_AI_ACT_ART_10 (Data governance) | IMPLEMENTS | GDPR_ART_5 (Principles) | AI data must follow GDPR principles |
| EU_AI_ACT_ART_14 (Human oversight) | COMPLEMENTS | GDPR_ART_22 (Automated decisions) | Both require human involvement |
| EU_AI_ACT_ANNEX_III (Risk categories) | EXPANDS | GDPR_ART_35_3 (DPIA triggers) | AI Act adds AI-specific DPIA triggers |

### Concept Hierarchies

```
DataType
├── PersonalData
│   ├── SpecialCategoryData
│   │   ├── BiometricData
│   │   ├── HealthData
│   │   ├── GeneticData
│   │   └── RacialEthnicData
│   └── RegularPersonalData
│       ├── ContactData
│       ├── FinancialData
│       └── BehavioralData
└── NonPersonalData
    ├── AggregatedData
    └── AnonymizedData
```

### Risk Category Mapping

```
AISystemType
├── ProhibitedAI (Art 5)
│   ├── SocialScoring
│   ├── EmotionRecognitionWorkplace
│   └── RealTimeBiometricPublic
├── HighRiskAI (Annex III)
│   ├── BiometricIdentification
│   ├── CriticalInfrastructure
│   ├── EducationAssessment
│   ├── EmploymentDecisions
│   ├── EssentialServices
│   ├── LawEnforcement
│   ├── MigrationControl
│   └── JudicialAssistance
├── LimitedRiskAI (Art 52)
│   ├── Chatbots
│   ├── EmotionRecognition
│   └── DeepfakeGeneration
└── MinimalRiskAI
    └── SpamFilters
    └── GameAI
```

---

## 🚨 Quality Requirements

### Accuracy Standards

| Requirement | Target | Reason |
|-------------|--------|--------|
| Article text accuracy | 100% | Legal citations must be exact |
| Relationship correctness | 99%+ | Wrong paths = wrong advice |
| Definition precision | 100% | Legal terms are precisely defined |
| Cross-reference coverage | 95%+ | Must capture regulation interconnections |

### Validation Methods

1. **Article Text**: Compare against EUR-Lex source
2. **Relationships**: Legal expert review
3. **Queries**: Test against known compliance scenarios
4. **Edge Cases**: Verify exemptions and exceptions

---

## 📤 Expected Outputs

### JSON Data Files

```
data/
├── regulations/
│   ├── gdpr_full.json           # All 99 GDPR articles
│   ├── eu_ai_act_full.json      # All 113 EU AI Act articles
│   └── cross_references.json    # Inter-regulation links
├── entities/
│   ├── definitions.json         # All legal definitions
│   ├── concepts.json            # Abstract concepts
│   ├── obligations.json         # Requirements extracted
│   └── risk_categories.json     # AI risk mappings
├── relationships/
│   ├── structural.json          # CONTAINS, PART_OF
│   ├── semantic.json            # REQUIRES, TRIGGERS
│   └── cross_regulation.json    # GDPR ↔ EU AI Act
└── embeddings/
    ├── article_embeddings.json  # Pre-computed vectors
    └── concept_embeddings.json
```

### Neo4j Import Scripts

```cypher
// Load regulations
LOAD CSV WITH HEADERS FROM 'file:///regulations.csv' AS row
CREATE (r:Regulation {id: row.id, name: row.name, ...})

// Load articles
LOAD CSV WITH HEADERS FROM 'file:///articles.csv' AS row
CREATE (a:Article {id: row.id, title: row.title, text: row.text, ...})

// Create relationships
LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
MATCH (source {id: row.source_id})
MATCH (target {id: row.target_id})
CREATE (source)-[r:REQUIRES {confidence: row.confidence}]->(target)
```

---

## ✅ Success Criteria

The knowledge graph is complete when it can correctly answer:

1. **Risk Classification**: "Is [system X] prohibited/high-risk/limited/minimal under EU AI Act?"
2. **Requirement Lookup**: "What are all requirements for [category] AI systems?"
3. **DPIA Triggers**: "Does [processing scenario] require a DPIA?"
4. **Cross-Regulation**: "What are combined GDPR and EU AI Act requirements for [use case]?"
5. **Legal Citations**: Return exact article references with full text
6. **Reasoning Chains**: Explain path from query to answer

---

## 🔗 Reference Files in Existing Project

| File | Purpose |
|------|---------|
| `core_2/src/graph/schema.py` | Entity and relationship type definitions |
| `core_2/src/stores/graph_store.py` | Neo4j interaction patterns |
| `core_2/src/stores/vector_store.py` | ChromaDB interaction patterns |
| `core_2/src/retrieval/engine.py` | Hybrid retrieval implementation |
| `core_2/src/retrieval/reasoning.py` | Multi-hop reasoning logic |
| `core_2/data/legal/gdpr_articles.json` | Sample GDPR data (14 articles) |
| `core_2/data/legal/eu_ai_act_articles.json` | Sample EU AI Act data (11 articles) |

---

## 🎯 Project Deliverables

1. **Complete Entity Extraction**: All articles, definitions, recitals, annexes
2. **Relationship Mapping**: All structural and semantic connections
3. **Cross-Regulation Links**: GDPR ↔ EU AI Act mappings
4. **Concept Ontology**: Hierarchical concept structure
5. **Vector Embeddings**: Pre-computed for all text
6. **Validation Test Set**: Golden queries with expected answers
7. **Import Scripts**: Ready-to-run Neo4j/ChromaDB loaders

---

> **Note**: This knowledge base is the foundation of a compliance system where errors can cost up to €35M. Every relationship, every citation, every definition must be verified against the official legal text.


---


## SOURCE: `gdpr context/backup/EU_AI_KB_PROJECT_CONTEXT.md`

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
├── raw_data/                       # Copy of New_Data/ (read-only source)
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

### Data Available in New_Data/ (89 files, 5.7 MB)

| Category | Files | Size | Delimiter | Key Fields | Expected Entities |
|---|---|---|---|---|---|
| GDPR Articles | 11 chapter files | 193 KB | `=== ARTICLE N ===` | Name, Paragraphs, sub-items (a)(b) | 99 Article nodes |
| GDPR Recitals | 1 file | 153 KB | `=== RECITAL N ===` | Full text | 173 Recital nodes |
| AI Act Articles | 13 chapter files | 293 KB | `=== ARTICLE N ===` | Title, Paragraphs, sub-items | 113 Article nodes |
| AI Act Recitals | 1 file | 225 KB | `=== RECITAL N ===` | Full text | ~180 Recital nodes |
| AI Act Annexes | 1 file | 46 KB | `=== ANNEX N ===` | Title, structured lists | 13 Annex nodes |
| CJEU Case Law | 20 + 1 compilation + 1 index | 191 KB | `=== CASE: C-NNN/YY ===` | Court, Date, Topic, Provisions, Holding, AI Relevance | 20 CaseLaw nodes |
| EDPB Guidelines | 20 + 1 compilation + 1 index | 4.3 MB | `=== GUIDELINE: ref ===` | Reference, Topics, Tier, Full text | 22 Guideline nodes |
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

### 7.2 Relationship Types (25)

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
| **COMPLEMENTS** | Article (Reg A) → Article (Reg B) | "What cross-regulation requirements exist?" |
| **SUPERSEDES** | Provision → Provision | "Which provision takes priority?" |
| **PENALISED_BY** | Violation → EnforcementAction | "What enforcement happened?" |
| **CITES** | EnforcementAction/CaseLaw → Article | "Which articles were invoked?" |

### 7.3 Expected Scale

| Metric | Count |
|---|---|
| Total nodes | ~2,225 |
| Total relationships | ~3,700 |
| Avg relationships per Article | ≥4 |
| Cross-regulation edges | ~50 |
| Vector store chunks | ~3,500 |

### 7.4 The Graph's Power: A Worked Example

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

Each entity type gets a specific search-prefix to improve embedding quality:

```python
EMBEDDING_PREFIXES = {
    "Article": "EU regulation article: {title} — {text}",
    "Obligation": "Legal compliance requirement: {who} {obligation_type} {what}. Source: {source_article}",
    "Recital": "Legislative interpretation context (Recital {number}): {text}",
    "CaseLaw": "Court ruling on {topic}: {case_name} ({case_number}). Holding: {text}",
    "Guideline": "Regulatory guidance on {topics}: {text}",
    "EnforcementAction": "Enforcement action against {target} by {authority}: {text}",
    "Definition": "Legal definition of '{term}': {definition_text}",
    "Exemption": "Legal exemption from {exempts_from}: {condition_text}",
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


---


## SOURCE: `gdpr context/backup/Integration Architecture How Projects Actually Connect.md`

# REAL, Concrete System Integration (Not Theoretical)

🎯 **The Integration Strategy**

## Core Concept: Project 2 Monitors Projects 1, 3, 4 in Production

┌─────────────────────────────────────────────────────────────┐
│ PROJECT 4 │
│ Multi-Agent Compliance System (PRODUCTION) │
│ │
│ [Supervisor] → [Risk Classifier] → [Legal Research] │
│ ↓ │
│ Calls Project 3 API │
└────────────────────┬────────────────────────────────────────┘
│
│ Makes decisions, processes queries
│
↓
┌────────────────────────────────────────────────────────────┐
│ PROJECT 2 │
│ MLOps Compliance Monitoring Pipeline │
│ │
│ Monitors: │
│ • Agent decision quality drift │
│ • Risk classification bias │
│ • EU AI Act Article 14 compliance (human oversight) │
│ • Project 3 GraphRAG API performance │
│ • Project 1 RAG hallucination rate │
│ │
│ Alerts when: │
│ • Classification accuracy drops below 90% │
│ • Human override rate exceeds 20% (agents failing) │
│ • GraphRAG API latency > 3 seconds │
│ • Bias detected in protected attributes │
└────────────────────────────────────────────────────────────┘
↓ ↓ ↓
[Evidently] [Prometheus] [MLflow]
Drift Detection Metrics Experiment
Tracking

python
Copy code

---

## 📋 Concrete Integration Points

---

## Integration 1: Monitor Project 4's Agent Decisions

### What Project 2 Monitors

```python
# Project 2: src/monitoring/agent_monitor.py

class ComplianceAgentMonitor:
    """
    Monitors Project 4 agents for EU AI Act compliance
    """
    
    def track_agent_decision(self, decision_data: dict):
        """
        Called by Project 4 after each agent decision
        
        Example decision_data from Project 4:
        {
            "agent": "risk_classifier",
            "input": {"system_description": "Facial recognition for hiring"},
            "prediction": "HIGH_RISK",
            "confidence": 0.92,
            "human_reviewed": False,
            "timestamp": "2026-01-21T10:30:00Z"
        }
        """
        # Track metrics
        self.decision_counter.inc()
        self.confidence_histogram.observe(decision_data["confidence"])
        
        # Check for drift
        self._check_prediction_drift(decision_data)
        
        # EU AI Act Article 14 compliance check
        self._check_human_oversight_compliance(decision_data)
        
        # Bias detection
        self._check_for_bias(decision_data)
    
    def _check_human_oversight_compliance(self, decision: dict):
        """
        EU AI Act Article 14: High-risk systems need human oversight
        
        Alert if:
        - High-risk classification made without human review
        - Human override rate suddenly increases (agents degrading)
        """
        if decision["prediction"] == "HIGH_RISK" and not decision["human_reviewed"]:
            # Check if this violates policy
            time_since_deployment = get_time_since_deployment()
            
            if time_since_deployment > 30:  # Days
                # After 30 days, expect <10% human review rate
                human_review_rate = self._calculate_human_review_rate(window="7d")
                
                if human_review_rate > 0.20:  # 20% threshold
                    alert = {
                        "severity": "HIGH",
                        "message": "Human override rate exceeds 20% - Agent quality degrading",
                        "compliance_violation": "EU AI Act Article 14 - Insufficient automation",
                        "action_required": "Retrain Risk Classifier Agent"
                    }
                    self.send_alert(alert)
How Projects Connect
python
Copy code
# Project 4: src/agents/risk_classifier_agent.py

from monitoring_client import ComplianceAgentMonitor  # Project 2 client

class RiskClassifierAgent:
    def __init__(self):
        # Project 2 monitoring client
        self.monitor = ComplianceAgentMonitor(api_url="http://project2-api:8080")
    
    async def classify(self, system_description: str) -> dict:
        result = await self._run_classification(system_description)
        
        # Send decision to Project 2 for monitoring
        await self.monitor.track_agent_decision({
            "agent": "risk_classifier",
            "input": {"system_description": system_description},
            "prediction": result["category"],
            "confidence": result["confidence"],
            "human_reviewed": result.get("human_reviewed", False),
            "timestamp": datetime.now().isoformat()
        })
        
        return result
Integration 2: Monitor Project 3's GraphRAG API
What Project 2 Monitors
python
Copy code
# Project 2: src/monitoring/graphrag_monitor.py

class GraphRAGMonitor:
    """
    Monitors Project 3's Legal Research API
    """
    
    def track_graphrag_query(self, query_data: dict):
        """
        Called by Project 4's Legal Research Agent after each query
        
        Example query_data:
        {
            "query": "Does facial recognition require DPIA?",
            "articles_retrieved": ["GDPR Article 9", "GDPR Article 35"],
            "reasoning_chains": [...],
            "confidence": 0.87,
            "latency_ms": 1850,
            "cost_usd": 0.08
        }
        """
        # Performance monitoring
        self.graphrag_latency.observe(query_data["latency_ms"])
        self.graphrag_cost.inc(query_data["cost_usd"])
        
        # Quality drift detection
        self._check_citation_quality_drift(query_data)
        
        # Alert on degradation
        if query_data["latency_ms"] > 3000:  # 3 second threshold
            self.send_alert({
                "severity": "MEDIUM",
                "message": f"GraphRAG latency degraded to {query_data['latency_ms']}ms",
                "action_required": "Check Neo4j performance, consider scaling"
            })
    
    def _check_citation_quality_drift(self, query_data: dict):
        """
        Detect if GraphRAG citations are getting worse over time
        """
        from evidently.metrics import ColumnDriftMetric
        
        current_confidence = query_data["confidence"]
        baseline_confidence = self.get_baseline_confidence()
        
        drift_score = abs(current_confidence - baseline_confidence) / baseline_confidence
        
        if drift_score > 0.15:  # 15% drift threshold
            self.send_alert({
                "severity": "HIGH",
                "message": f"GraphRAG confidence drift: {drift_score:.2%}",
                "current_confidence": current_confidence,
                "baseline_confidence": baseline_confidence,
                "action_required": "Review knowledge graph quality, check for stale data"
            })
How Projects Connect
python
Copy code
# Project 4: src/agents/legal_research_agent.py

from monitoring_client import GraphRAGMonitor  # Project 2 client

class LegalResearchAgent:
    def __init__(self, graphrag_api_url: str):
        self.graphrag_url = graphrag_api_url  # Project 3 API
        self.monitor = GraphRAGMonitor(api_url="http://project2-api:8080")  # Project 2
    
    async def research(self, query: str) -> dict:
        start_time = time.time()
        response = await httpx.post(
            f"{self.graphrag_url}/api/v1/hybrid/reason",
            json={"question": query}
        )
        latency_ms = (time.time() - start_time) * 1000
        
        result = response.json()
        
        await self.monitor.track_graphrag_query({
            "query": query,
            "articles_retrieved": [r["article_number"] for r in result["results"]],
            "reasoning_chains": result["reasoning_chains"],
            "confidence": result.get("confidence", 0.0),
            "latency_ms": latency_ms,
            "cost_usd": result["cost_usd"]
        })
        
        return result
Integration 3: Monitor Project 1's RAG System (Optional)
python
Copy code
# Project 2: src/monitoring/rag_monitor.py

class RAGMonitor:
    """
    Monitors Project 1's basic RAG system for hallucinations
    """
    
    def track_rag_response(self, response_data: dict):
        """
        Track RAG responses for hallucination rate
        """
        if response_data["faithfulness_score"] < 0.85:
            self.hallucination_counter.inc()
        
        hallucination_rate = self._calculate_hallucination_rate(window="24h")
        
        if hallucination_rate > 0.10:
            self.send_alert({
                "severity": "HIGH",
                "message": f"RAG hallucination rate: {hallucination_rate:.2%}",
                "action_required": "Review retrieval quality, check embedding drift"
            })
📊 Unified Monitoring Dashboard
python
Copy code
# Project 2: src/dashboard/compliance_dashboard.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="AI Compliance Monitoring Dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
def compliance_dashboard():
    return render_template("dashboard.html", data={
        "agent_metrics": {
            "risk_classifier_accuracy": get_metric("risk_classifier_accuracy_7d"),
            "human_override_rate": get_metric("human_override_rate_7d"),
            "decisions_per_day": get_metric("agent_decisions_count_1d"),
            "article_14_compliance": check_article_14_compliance()
        },
        "graphrag_metrics": {
            "avg_query_latency_ms": get_metric("graphrag_latency_p95_1h"),
            "citation_confidence": get_metric("graphrag_confidence_avg_7d"),
            "api_uptime": get_metric("graphrag_uptime_30d"),
            "cost_per_day": get_metric("graphrag_cost_sum_1d")
        },
        "rag_metrics": {
            "hallucination_rate": get_metric("rag_hallucination_rate_7d"),
            "faithfulness_score": get_metric("rag_faithfulness_avg_7d")
        },
        "compliance_status": {
            "eu_ai_act_article_14": "COMPLIANT" if check_article_14_compliance() else "VIOLATION",
            "gdpr_article_22": "COMPLIANT",
            "human_oversight_active": True,
            "last_audit": "2026-01-15"
        }
    })
🎯 Business Value of Integration
Recruiter: “How do your projects integrate?”

You:

“Project 2 is the operational monitoring backbone for my compliance platform.
When Project 4’s agents make risk classifications, they send decisions to Project 2, which tracks EU AI Act Article 14 compliance, decision quality drift, and bias detection.

When Project 4 calls Project 3’s GraphRAG API, Project 2 monitors latency, uptime, cost, and citation quality.

This creates a closed-loop system: Project 2 detects degradation → alerts me → I retrain agents → quality is restored.
In production simulation, this caught a 15% accuracy drop within 48 hours.”

📋 Integration Checklist
Technical Integration
Project 4 → Project 2 agent decision tracking

Project 3 → Project 2 GraphRAG monitoring

Unified dashboard across projects

Alerting on degradation

Code Integration
Shared monitoring client library

Docker Compose orchestration

Environment-based service discovery

Integration tests

Demo Integration
Live demo with all services running

Dashboard visible

Drift simulation → alert triggered

Architecture diagram

🚀 Implementation Priority
Must-Have
Project 4 → Project 2 agent monitoring

Project 3 → Project 2 GraphRAG monitoring

Unified dashboard

Nice-to-Have
Project 1 hallucination monitoring

Automated retraining

Cost-based alerts

🎓 Interview Impact
Without Integration:

“I built five projects.”

With Integration:

“I built a compliance platform where Project 2 monitors Projects 1, 3, and 4 in production, enforces EU AI Act requirements, detects drift, and triggers remediation.”

Recruiter thinks:
“This person understands systems engineering. Hire immediately.”

---


## SOURCE: `gdpr context/backup/SYSTEM_ARCHITECTURE.md`

# GDPR & EU AI Act Knowledge Graph — System Architecture & Data Reference

This document provides a comprehensive overview of the data structure, database schemas, graph schema, and retrieval pipeline for the GraphRAG Legal Research Engine. Use this as full context when discussing or extending the project.

---

## 1. High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    FastAPI Service (:8001)                         │
│  POST /api/v1/vector/search   → Vector similarity search          │
│  POST /api/v1/graph/traverse  → Neo4j graph traversal             │
│  POST /api/v1/hybrid/search   → RRF fusion (vector + graph)       │
│  POST /api/v1/hybrid/reason   → Multi-hop LLM reasoning           │
└────────────────────┬───────────────────────────────────────────────┘
                     │
        ┌────────────┴─────────────┐
        │  Hybrid Retrieval Engine │
        │  (Reciprocal Rank Fusion)│
        └─────┬──────────────┬─────┘
              │              │
   ┌──────────▼──────┐  ┌───▼────────────────────┐
   │   Neo4j 5.x     │  │  ChromaDB (Persistent)  │
   │   Graph Store    │  │  Vector Store           │
   │                  │  │                         │
   │ • Entity nodes   │  │ • Gemini embeddings     │
   │ • Relationships  │  │ • Cosine similarity     │
   │ • Cypher queries │  │ • Metadata filtering    │
   │ • Multi-hop      │  │ • Collection:           │
   │   traversal      │  │   "legal_entities"      │
   └──────────────────┘  └─────────────────────────┘
              │              │
              └──────┬───────┘
                     │
            ┌────────▼─────────┐
            │  Google Gemini   │
            │  • Embeddings:   │
            │    gemini-       │
            │    embedding-001 │
            │  • LLM:         │
            │    gemini-2.0-   │
            │    flash         │
            └──────────────────┘
```

---

## 2. Data Sources (JSON Files)

All source data lives under `core_2/data/`. Here is the full inventory:

### 2.1 Legal Core Data (`data/legal/`)

| File | Content | Records |
|------|---------|---------|
| `gdpr_articles.json` | 14 GDPR articles + 6 definitions | 20 entities |
| `eu_ai_act_articles.json` | 13 EU AI Act articles + 2 annexes + 7 definitions + annex categories | 35 entities |
| `gdpr_structure.json` | Complete index of all 99 GDPR articles, 173 recitals, 11 chapters | Reference index |
| `eu_ai_act_structure.json` | Complete index of all 113 EU AI Act articles, 13 chapters, 13 annexes | Reference index |

### 2.2 Entity Enrichment Data (`data/entities/`)

| File | Content | Records |
|------|---------|---------|
| `obligations.json` | ~40 obligations (GDPR + AI Act), penalty tiers, actor applicability | 489 lines |
| `concepts_and_principles.json` | 14 principles, 20+ concepts, data type hierarchy, risk hierarchy, actor mappings | 435 lines |
| `authorities.json` | 5 EU-level authorities (EDPB, EDPS, AI Office, AI Board, Scientific Panel), 12 national DPAs | 217 lines |
| `rights_and_remedies.json` | 12 GDPR rights + 5 EU AI Act rights + enforcement mechanisms | 245 lines |
| `penalties.json` | GDPR tiers (10M/2% and 20M/4%), AI Act tiers (7.5M/1.5% to 35M/7%), SME provisions | 207 lines |
| `cross_regulation_mappings.json` | 25 cross-regulation links, 7 actor mappings, 8 use-case scenarios | 317 lines |

### 2.3 Interpretive Data (`data/interpretive/`)

| File | Content | Records |
|------|---------|---------|
| `case_law.json` | 11 landmark CJEU cases (Schrems II, Google Spain, Planet49, etc.) | 250 lines |
| `edpb_guidelines.json` | 15 key EDPB/WP29 guidelines (consent, profiling, DPIA, etc.) | 316 lines |
| `enforcement_actions.json` | 15 major enforcement actions with fines and DPA decisions | 282 lines |

### 2.4 Test Data (`data/golden/`)

| File | Content |
|------|---------|
| `test_queries.json` | ~15 golden test queries with expected answers, citations, reasoning paths, difficulty levels |

---

## 3. Neo4j Graph Database Schema

### 3.1 Node Labels

Every node has a base label `:Entity` plus a specific type label. Nodes are created with:

```cypher
MERGE (n:Entity {id: $id})
SET n += $properties
SET n:Article  -- (or Regulation, Definition, Concept, etc.)
```

#### Entity Types (14 types currently used)

| Label | Description | Example IDs |
|-------|-------------|-------------|
| `Regulation` | Top-level legal framework | `GDPR`, `EU_AI_ACT` |
| `Article` | Individual article within a regulation | `GDPR_ART_5`, `AIACT_ART_6` |
| `Annex` | Technical annex | `AIACT_ANNEX_III`, `AIACT_ANNEX_IV` |
| `Definition` | Legal term definition | `GDPR_DEF_PERSONAL_DATA`, `AIACT_DEF_AI_SYSTEM` |
| `Concept` | Abstract concept / annex category | `ANNEX_III_1` (Biometrics), `ANNEX_IV_2` (Development Process) |
| `Obligation` | Compliance requirement (must/must-not/should) | `OBL_GDPR_LAWFUL_BASIS` |
| `Right` | Data subject / affected person right | — |
| `Penalty` | Fine / sanction structure | — |
| `Authority` | Regulatory body | `AUTH_EDPB`, `AUTH_EDPS` |
| `Actor` | Legal role | — |
| `DataType` | Data classification | — |
| `AISystemType` | AI risk classification | — |
| `RiskCategory` | Risk category | — |
| `Recital` | Interpretive recital | — |

### 3.2 Node Properties

All nodes share these base properties:

```
{
  id:          String   -- Unique identifier (e.g. "GDPR_ART_35")
  type:        String   -- EntityType value (e.g. "Article")
  name:        String   -- Display name (e.g. "Article 35")
  description: String   -- Detailed description text
  source_text: String   -- Original text from regulation (optional)
  created_at:  String   -- ISO timestamp
  updated_at:  String   -- ISO timestamp
}
```

Specialized node types add extra properties:

| Type | Additional Properties |
|------|----------------------|
| **Regulation** | `full_title`, `short_name`, `effective_date`, `jurisdiction` |
| **Article** | `regulation_id`, `article_number`, `title`, `full_text`, `chapter` |
| **Definition** | `term`, `definition_text`, `regulation_id`, `article_reference` |
| **Concept** | `synonyms` (list), `related_concepts` (list) |
| **Obligation** | `obligation_type`, `applies_to` (list), `conditions` (list), `source_article`, `deadline`, `penalty_reference` |

### 3.3 Indexes

```cypher
-- Per entity type:
CREATE INDEX IF NOT EXISTS FOR (n:Regulation) ON (n.id)
CREATE INDEX IF NOT EXISTS FOR (n:Article) ON (n.id)
CREATE INDEX IF NOT EXISTS FOR (n:Definition) ON (n.id)
-- ... one for each EntityType

-- Global:
CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.name)
CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.type)
```

### 3.4 Relationship Types (20 types defined)

Relationships are directed edges between `:Entity` nodes:

```cypher
MATCH (source:Entity {id: $source_id})
MATCH (target:Entity {id: $target_id})
MERGE (source)-[r:CONTAINS]->(target)
SET r += $properties
```

#### Categories of Relationships

**Structural (document hierarchy):**

| Type | Meaning | Example |
|------|---------|---------|
| `CONTAINS` | Parent contains child | `(GDPR)-[:CONTAINS]->(GDPR_ART_5)` |
| `PART_OF` | Child belongs to parent | — |
| `REFERENCES` | Cross-reference | `(AIACT_ART_6)-[:REFERENCES]->(AIACT_ANNEX_III)` |
| `AMENDS` | Modifies another provision | — |
| `REPEALS` | Replaces another provision | — |

**Semantic (legal meaning):**

| Type | Meaning | Example |
|------|---------|---------|
| `DEFINES` | Provides definition | `(GDPR)-[:DEFINES]->(GDPR_DEF_PERSONAL_DATA)` |
| `REQUIRES` | Creates obligation | — |
| `PROHIBITS` | Forbids activity | `(AIACT_ART_5)-[:PROHIBITS]->(AIACT_DEF_EMOTION_RECOGNITION)` |
| `PERMITS` | Allows activity | — |
| `TRIGGERS` | Activates requirement | `(ANNEX_III_1)-[:TRIGGERS]->(GDPR_ART_35)` |
| `EXEMPTS` | Provides exception | — |

**Actor (who is affected):**

| Type | Meaning | Example |
|------|---------|---------|
| `APPLIES_TO` | Affects which actors | `(GDPR_ART_22)-[:APPLIES_TO]->(AIACT_DEF_AI_SYSTEM)` |
| `ENFORCED_BY` | Authority enforces | — |
| `RESPONSIBLE_FOR` | Actor responsibility | — |

**Data & Risk:**

| Type | Meaning | Example |
|------|---------|---------|
| `PROCESSES` | Data processing relationship | — |
| `PROTECTS` | Protection relationship | — |
| `REGULATED_BY` | Regulatory relationship | `(GDPR_ART_9)-[:REGULATED_BY]->(GDPR_DEF_BIOMETRIC_DATA)` |
| `CLASSIFIED_AS` | Risk classification | — |
| `MITIGATED_BY` | Risk mitigation | — |

#### Relationship Properties

```
{
  id:          String  -- Unique identifier
  confidence:  Float   -- 0.0 to 1.0 (default 1.0)
  source_text: String  -- Text evidence (optional)
  created_at:  String  -- ISO timestamp
}
```

### 3.5 Current Graph Statistics

After running `load_data.py`:

```
Total Nodes:          56
Total Relationships:  61

Nodes by Type:
  Regulation:   2   (GDPR, EU AI Act)
  Article:     27   (14 GDPR + 13 EU AI Act)
  Annex:        2   (Annex III, Annex IV)
  Definition:  13   (6 GDPR + 7 EU AI Act)
  Concept:     12   (Annex III/IV categories)
```

### 3.6 Key Cross-Regulation Relationships (7 loaded)

These are the explicit GDPR ↔ EU AI Act links:

```
(GDPR_ART_9)  -[:REGULATED_BY]->  (GDPR_DEF_BIOMETRIC_DATA)
(ANNEX_III_1)  -[:TRIGGERS]->     (GDPR_ART_35)          -- Biometrics triggers DPIA
(GDPR_ART_22) -[:APPLIES_TO]->    (AIACT_DEF_AI_SYSTEM)  -- ADM applies to AI systems
(AIACT_ART_14)-[:REFERENCES]->    (GDPR_ART_22)          -- Human oversight ↔ ADM
(AIACT_ART_5) -[:PROHIBITS]->     (AIACT_DEF_EMOTION_RECOGNITION)
(AIACT_ART_6) -[:REFERENCES]->    (AIACT_ANNEX_III)      -- High-risk classification
(AIACT_ANNEX_III)-[:TRIGGERS]->   (AIACT_ART_43)         -- Conformity assessment
```

---

## 4. ChromaDB Vector Store Schema

### 4.1 Collection Setup

```python
collection_name = "legal_entities"
metadata = {"hnsw:space": "cosine"}   # Cosine similarity
```

### 4.2 Embedding Model

- **Model**: `models/gemini-embedding-001` (Google Gemini)
- **Task type**: `RETRIEVAL_DOCUMENT`
- **Max input**: 8,000 characters (truncated)
- **Batch size**: 10 texts per API call

### 4.3 Document Schema

Each entity is stored as:

```python
{
    "id":        "GDPR_ART_35",                          # Unique ID (matches Neo4j)
    "document":  "Article 35: DPIA ... [full text]",     # Searchable text
    "embedding": [0.012, -0.034, ...],                   # Gemini embedding vector
    "metadata": {
        "id":          "GDPR_ART_35",
        "type":        "Article",
        "name":        "Article 35",
        "description": "Data protection impact assessment"
    }
}
```

### 4.4 Text Representation

Entities are converted to searchable text via:

```python
def _entity_to_text(entity):
    parts = [f"{entity.type.value}: {entity.name}"]
    if entity.description:
        parts.append(entity.description)
    if entity.source_text:
        parts.append(entity.source_text)
    return "\n".join(parts)
```

### 4.5 Search

- **Query**: user input → Gemini embedding (task_type=`RETRIEVAL_QUERY`)
- **Distance**: cosine distance
- **Score**: `1 - cosine_distance` (higher = more similar)
- **Filter**: optional `{"type": {"$in": ["Article", "Definition"]}}` metadata filter

---

## 5. Retrieval Pipeline

### 5.1 Vector Search

```
User query → Gemini embedding → Cosine similarity search in ChromaDB → Top-K results
```

### 5.2 Graph Search

```
User query → Keyword match on entity name/description in Neo4j → Scored results
```

### 5.3 Graph Traversal

```
Start entity ID → Cypher variable-length path query → Multi-hop results

MATCH path = (start:Entity {id: $start_id})-[r:REL_TYPE*1..N]->(end:Entity)
RETURN path
LIMIT 100
```

- Supports `OUTGOING`, `INCOMING`, `BOTH` directions
- Max hops configurable (default: 3)
- Confidence = product of relationship confidences along path

### 5.4 Hybrid Search (RRF Fusion)

Combines vector + graph results using **Reciprocal Rank Fusion**:

```
RRF_score(entity) = Σ  1 / (k + rank_i)
                    for each result list containing entity

k = 60 (default)
```

Flow:
```
User query
  ├── Vector search → top 2K results with ranks
  ├── Graph search  → top 2K results with ranks
  └── RRF fusion → merged, deduplicated, re-ranked → top K
```

### 5.5 Search + Expand

```
1. Vector search → seed entities
2. For each seed → graph traversal (N hops)
3. Merge seed + expansion results
4. Deduplicate and re-rank by score
```

### 5.6 Multi-Hop Reasoning (LLM-Powered)

```
1. Vector search → initial context entities
2. Graph traversal from seed entities → expansion
3. Find paths between related entities
4. Construct context string from all retrieved entities/paths
5. Send to Gemini LLM with structured prompt
6. Parse structured response (ANSWER / REASONING / CITATIONS)
```

LLM Prompt structure:
```
You are a legal compliance expert. Given the following query
and retrieved context from a legal knowledge graph, provide
a clear answer with citations.

Query: {query}
Retrieved Context: {entities + graph paths}

→ Output: ANSWER, REASONING (chain of thought), CITATIONS (article refs)
```

---

## 6. Entity ID Naming Convention

| Pattern | Example | Meaning |
|---------|---------|---------|
| `GDPR` | `GDPR` | GDPR regulation node |
| `EU_AI_ACT` | `EU_AI_ACT` | EU AI Act regulation node |
| `GDPR_ART_{N}` | `GDPR_ART_35` | GDPR Article N |
| `AIACT_ART_{N}` | `AIACT_ART_6` | EU AI Act Article N |
| `GDPR_DEF_{TERM}` | `GDPR_DEF_BIOMETRIC_DATA` | GDPR definition |
| `AIACT_DEF_{TERM}` | `AIACT_DEF_AI_SYSTEM` | AI Act definition |
| `AIACT_ANNEX_{ROMAN}` | `AIACT_ANNEX_III` | AI Act annex |
| `ANNEX_III_{N}` | `ANNEX_III_1` | Annex III category (Biometrics) |
| `ANNEX_IV_{N}` | `ANNEX_IV_2` | Annex IV category (Development) |
| `OBL_GDPR_{NAME}` | `OBL_GDPR_LAWFUL_BASIS` | GDPR obligation |
| `AUTH_{ACRONYM}` | `AUTH_EDPB` | Regulatory authority |
| `CJEU_C_{NUM}` | `CJEU_C_311_18` | CJEU case (Schrems II) |

---

## 7. Example Graph Traversals

### "Does facial recognition require a DPIA?"

```
(facial recognition)
  → AIACT_DEF_BIOMETRIC_ID  [Definition: remote biometric identification]
    → ANNEX_III_1            [Concept: Biometrics category]
      → GDPR_ART_35          [Article: DPIA requirement]   via TRIGGERS
      → AIACT_ART_43         [Article: Conformity assessment] via TRIGGERS
  → GDPR_ART_9              [Article: Special categories]   via REGULATED_BY → GDPR_DEF_BIOMETRIC_DATA
```

### "What AI practices are prohibited?"

```
(AIACT_ART_5) -[:PROHIBITS]-> (AIACT_DEF_EMOTION_RECOGNITION)
(AIACT_ART_5) [text contains: subliminal techniques, social scoring, real-time biometric ID, biometric categorisation]
```

### "AI hiring system requirements"

```
(ANNEX_III_4)  [Employment: AI for recruitment, screening, hiring]
  → AIACT_ANNEX_III   via PART_OF → AIACT_ART_6  [High-risk classification]
  → GDPR_ART_22       [Automated decision-making]  via APPLIES_TO → AIACT_DEF_AI_SYSTEM
  → AIACT_ART_14      [Human oversight]             via REFERENCES → GDPR_ART_22
```

---

## 8. GDPR Articles Currently Loaded

| ID | Article | Title |
|----|---------|-------|
| `GDPR_ART_1` | Art 1 | Subject-matter and objectives |
| `GDPR_ART_2` | Art 2 | Material scope |
| `GDPR_ART_3` | Art 3 | Territorial scope |
| `GDPR_ART_4` | Art 4 | Definitions |
| `GDPR_ART_5` | Art 5 | Principles relating to processing |
| `GDPR_ART_6` | Art 6 | Lawfulness of processing |
| `GDPR_ART_9` | Art 9 | Special categories of personal data |
| `GDPR_ART_13` | Art 13 | Information to data subject (collected from subject) |
| `GDPR_ART_14` | Art 14 | Information to data subject (not from subject) |
| `GDPR_ART_17` | Art 17 | Right to erasure |
| `GDPR_ART_22` | Art 22 | Automated decision-making |
| `GDPR_ART_25` | Art 25 | Data protection by design and default |
| `GDPR_ART_30` | Art 30 | Records of processing activities |
| `GDPR_ART_35` | Art 35 | Data protection impact assessment |

## 9. EU AI Act Articles Currently Loaded

| ID | Article | Title |
|----|---------|-------|
| `AIACT_ART_1` | Art 1 | Subject matter |
| `AIACT_ART_2` | Art 2 | Scope |
| `AIACT_ART_3` | Art 3 | Definitions |
| `AIACT_ART_5` | Art 5 | Prohibited AI practices |
| `AIACT_ART_6` | Art 6 | Classification rules for high-risk |
| `AIACT_ART_9` | Art 9 | Risk management system |
| `AIACT_ART_10` | Art 10 | Data and data governance |
| `AIACT_ART_11` | Art 11 | Technical documentation |
| `AIACT_ART_12` | Art 12 | Record-keeping |
| `AIACT_ART_13` | Art 13 | Transparency and information to deployers |
| `AIACT_ART_14` | Art 14 | Human oversight |
| `AIACT_ART_43` | Art 43 | Conformity assessment |
| `AIACT_ART_52` | Art 52 | Transparency obligations for certain AI |

## 10. Definitions Currently Loaded

**GDPR (6):** personal data, biometric data, profiling, controller, processor, consent

**EU AI Act (7):** AI system, high-risk AI system, remote biometric identification system, emotion recognition system, provider, deployer, deep fake

---

## 11. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | REST API with auto-docs |
| Graph Database | Neo4j 5.x | Knowledge graph storage, Cypher queries, multi-hop traversal |
| Vector Database | ChromaDB (persistent) | Embedding storage, cosine similarity search |
| Embeddings | Google Gemini `gemini-embedding-001` | Text → vector conversion |
| LLM | Google Gemini `gemini-2.0-flash` | Multi-hop reasoning, answer generation |
| Data Models | Pydantic v2 | Schema validation, serialization |
| Package Manager | UV | Fast Python dependency management |
| Language | Python 3.11+ | Runtime |

---

## 12. Configuration (Environment Variables)

```env
GEMINI_API_KEY=<your-key>
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=<your-password>
CHROMA_PERSIST_DIR=./data/chroma
API_PORT=8001
```

---

## 13. Known Data Gaps

Currently ~12% of full regulation coverage. Critical missing pieces:

- **GDPR**: 85 of 99 articles missing (Art 7, 8, 12, 15-16, 18-21, 24, 28, 32-34, 37-39, 44-49, etc.)
- **GDPR Recitals**: 0 of 173 loaded
- **EU AI Act**: 100 of 113 articles missing
- **EU AI Act Annexes**: Only Annex III and IV partially loaded (11 missing)
- **Cross-regulation links**: Only 7 of ~200+ potential mappings
- **Additional entity data** (obligations, authorities, case law, etc.) exists in `data/entities/` and `data/interpretive/` but is NOT yet loaded into Neo4j/ChromaDB by the current `load_data.py` script

The enrichment data files contain significant additional content that could boost coverage to ~60-70% if a loader is written for them.


---


## SOURCE: `gdpr context/backup/KB_construction_plan.md`

# Knowledge Base Construction Plan

## EU AI Regulatory Compliance Engine — Complete Build Specification

> **Date**: 2026-02-10
> **Author**: Lead Data Architect review
> **Scope**: Full knowledge graph + vector store construction from New_Data/

---

## 1. Raw Data Inventory

### What We Have (89 files, 5.7 MB total)

| Category | Files | Size | Format | Content |
|---|---|---|---|---|
| **GDPR Articles** | 11 chapter files | 193 KB | `=== ARTICLE N ===` delimited, paragraph-level | All 99 articles, full text with paragraphs |
| **GDPR Recitals** | 1 file | 153 KB | `=== RECITAL N ===` delimited | All 173 recitals |
| **EU AI Act Articles** | 13 chapter files | 293 KB | `=== ARTICLE N ===` delimited, paragraph-level | All 113 articles, full text |
| **EU AI Act Recitals** | 1 file | 225 KB | `=== RECITAL N ===` delimited | All recitals (~180) |
| **EU AI Act Annexes** | 1 file | 46 KB | `=== ANNEX N ===` delimited | All 13 annexes (I–XIII) |
| **CJEU Case Law** | 20 individual + 1 compilation + 1 index | 191 KB | Structured fields per case | 20 landmark decisions |
| **EDPB Guidelines** | 20 individual + 1 compilation + 1 index | 4.3 MB | Full guideline text + structured headers | 20 key guidelines |
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
Phase 1: Parse raw text → structured JSON (ETL)
Phase 2: Build the legal knowledge graph (structural layer)
Phase 3: Extract semantic entities and relationships (semantic layer)
Phase 4: Build vector store over all text (retrieval layer)
Phase 5: Cross-link and validate (integrity layer)
Phase 6: Build the SystemProfile → KG matching (application layer)
```

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
  COMPLEMENTS         — Article → Article (cross-regulation, e.g., AI Act Art 14 ↔ GDPR Art 22)
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
  "cross_references": ["GDPR_ART_36", "GDPR_ART_9", "GDPR_ART_22"]
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

### Phase 1: Parse Raw Text → Structured JSON (ETL Layer)

**Goal**: Convert all 89 raw text files into clean, validated JSON files.

**Script**: `core_2/scripts/parse_new_data.py`

#### 1.1 GDPR Article Parser
- **Input**: `New_Data/gdpr_chapters/gdpr_chapter*.txt` (11 files)
- **Delimiter**: `=== ARTICLE N ===`
- **Extract**: chapter name, article number, article name/title, each paragraph as separate field, sub-items `(a)`, `(b)`, etc.
- **Output**: `core_2/data/legal/gdpr_articles.json`
- **Expected**: 99 articles across 11 chapters
- **ID Convention**: `GDPR_ART_1` through `GDPR_ART_99`
- **Note**: GDPR uses "Name:" field; AI Act uses "Title:" field — parser must handle both

#### 1.2 EU AI Act Article Parser
- **Input**: `New_Data/ai_act_chapters/ai_act_chapter*.txt` (13 files)
- **Delimiter**: `=== ARTICLE N ===`
- **Extract**: Same structure as GDPR
- **Output**: `core_2/data/legal/eu_ai_act_articles.json`
- **Expected**: 113 articles across 13 chapters
- **ID Convention**: `AIACT_ART_1` through `AIACT_ART_113`

#### 1.3 GDPR Recital Parser
- **Input**: `New_Data/gdpr_recitals/gdpr_recitals.txt` (1 file, 153 KB)
- **Delimiter**: `=== RECITAL N ===`
- **Extract**: recital number, full text
- **Output**: `core_2/data/legal/gdpr_recitals.json`
- **Expected**: 173 recitals
- **ID Convention**: `GDPR_REC_1` through `GDPR_REC_173`

#### 1.4 EU AI Act Recital Parser
- **Input**: `New_Data/ai_act_recitals/euai_recitals.txt` (1 file, 225 KB)
- **Delimiter**: `=== RECITAL N ===`
- **Extract**: recital number, full text
- **Output**: `core_2/data/legal/ai_act_recitals.json`
- **Expected**: ~180 recitals
- **ID Convention**: `AIACT_REC_1` through `AIACT_REC_N`

#### 1.5 EU AI Act Annex Parser
- **Input**: `New_Data/ai_act_annexes/ai_act_annexes.txt` (1 file, 46 KB)
- **Delimiter**: `=== ANNEX N ===` (Roman numerals in text, but delimited as I, II, III...)
- **Extract**: annex number, title, sections, sub-items
- **Output**: `core_2/data/legal/ai_act_annexes.json`
- **Expected**: 13 annexes (I–XIII)
- **ID Convention**: `AIACT_ANNEX_I` through `AIACT_ANNEX_XIII`

#### 1.6 CJEU Case Law Parser
- **Input**: `New_Data/cjeu_case_law/C*_*.txt` (20 individual files)
- **Delimiter**: `=== CASE: C-NNN/YY <name> ===`
- **Extract**: case_number, case_name, full_name, court, decision_date, topic, provisions_interpreted, facts, holding, key_legal_points, practical_impact, ai_relevance
- **Output**: `core_2/data/interpretive/case_law.json`
- **Expected**: 20 cases
- **ID Convention**: `CJEU_C_311_18` (case number with underscores)
- **Important**: Also parse `cjeu_case_law_detailed.txt` for any additional content not in individual files

#### 1.7 EDPB Guidelines Parser
- **Input**: `New_Data/edpb_guidelines/GL_*.txt` + `WP*.txt` (22 individual files)
- **Delimiter**: `=== GUIDELINE: <ref> ===`
- **Extract**: reference, title, topics, tier, full text (preserve section headings)
- **Output**: `core_2/data/interpretive/edpb_guidelines.json`
- **Expected**: 22 guidelines
- **ID Convention**: `EDPB_GL_05_2022` (reference number)
- **Special**: Guidelines are very large (up to 220KB each). For the vector store, split into sections. For the graph, keep metadata + section summaries.

#### 1.8 Enforcement Actions Parser
- **Input**: `New_Data/enforcement_actions/*.txt` (15 individual files)
- **Delimiter**: `=== ENFORCEMENT: <name> ===`
- **Extract**: authority, target, decision_date, fine_amount, fine_category, violations, facts, key_findings, corrective_measures, ai_relevance
- **Output**: `core_2/data/interpretive/enforcement_actions.json`
- **Expected**: 15 actions
- **ID Convention**: `ENF_CLEARVIEW_AI`, `ENF_META_TRANSFER`, etc.

#### Phase 1 Validation
- Count: Verify expected counts (99 GDPR articles, 113 AI Act articles, 173 GDPR recitals, etc.)
- Schema: All JSON files validate against Pydantic models
- Completeness: Spot-check 5 articles per regulation against raw text
- No data loss: Character count of `full_text` fields ≥ 95% of raw text

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

#### Phase 2 Validation
- Node counts match parsed data
- Every Article has a PART_OF relationship to a Chapter
- Every Chapter has a CONTAINS relationship from a Regulation
- Spot-check 10 cross-references against raw text

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

**Heuristic pre-filter** (before LLM):
- Scan all article text for sentences containing "shall", "shall not", "must", "must not", "may", "should"
- GDPR uses "shall" ~500 times across 99 articles
- AI Act uses "shall" ~800 times across 113 articles
- Group by article → feed to LLM for structured extraction

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
│   └── RegularPersonalData
│       ├── ContactData (name, email, phone)
│       ├── LocationData
│       ├── OnlineIdentifiers
│       ├── FinancialData
│       └── BehavioralData (profiling inputs)
└── NonPersonalData
    ├── AnonymisedData
    ├── AggregatedData
    └── PseudonymisedData (still counts as personal data!)
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

**Expected output**: ~30–50 cross-regulation relationship edges

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

### Phase 6: Application Layer — SystemProfile Matching

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
| **Guideline nodes** | 22 |
| **EnforcementAction nodes** | 15 |
| **TOTAL NODES** | **~2,225** |
| | |
| **Structural relationships** (CONTAINS, PART_OF) | ~650 |
| **Cross-reference relationships** (REFERENCES) | ~700 |
| **Semantic relationships** (REQUIRES, PROHIBITS, PERMITS, TRIGGERS, EXEMPTS) | ~1,500 |
| **Actor relationships** (APPLIES_TO, ENFORCED_BY, RESPONSIBLE_FOR) | ~300 |
| **Data/Risk relationships** (CLASSIFIED_AS, REGULATED_BY, PROCESSES) | ~200 |
| **Interpretive relationships** (INTERPRETS, CITES) | ~300 |
| **Cross-regulation relationships** (COMPLEMENTS) | ~50 |
| **TOTAL RELATIONSHIPS** | **~3,700** |
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
Phase 1 (Parse)         ← No dependencies, can start immediately
    ↓
Phase 2 (Structural KG) ← Depends on Phase 1 JSON output
    ↓
Phase 3 (Semantic KG)   ← Depends on Phase 2 (needs article nodes to attach to)
    ↓                      Can partially parallelize with Phase 4
Phase 4 (Vector Store)  ← Depends on Phase 1 + Phase 3 (obligations need embedding too)
    ↓
Phase 5 (Validate)      ← Depends on Phases 2, 3, 4
    ↓
Phase 6 (Application)   ← Depends on validated KG
```

### Estimated Effort

| Phase | Effort | Notes |
|---|---|---|
| Phase 1: Parsing | 2-3 days | Rule-based, well-structured input |
| Phase 2: Structural KG | 1-2 days | Straightforward loading |
| Phase 3: Semantic extraction | 5-7 days | LLM-assisted, requires validation |
| Phase 4: Vector store | 1-2 days | Chunking + embedding |
| Phase 5: Validation | 2-3 days | Golden queries, coverage reports |
| Phase 6: SystemProfile | 3-4 days | New input layer design |
| **Total** | **~14-21 days** | |

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
│   │   ├── edpb_guidelines.json        # 22 guidelines (REPLACED)
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


---


## SOURCE: `gdpr context/backup/CRITICAL_GAP_ANALYSIS.md`

# CRITICAL GAP ANALYSIS: GDPR/EU AI Act Knowledge Base
## Multi-Agent Compliance Automation System Assessment

**Assessment Date:** 2024
**Assessor:** Data Architect (20 years experience in Graph/Vector Databases)
**Verdict:** INSUFFICIENT FOR PRODUCTION - Major enhancements required

---

## EXECUTIVE SUMMARY

The current knowledge base achieves approximately **12% coverage** of required GDPR/EU AI Act data. For a multi-agent compliance automation system, this is critically insufficient. A multi-hop reasoning query would fail in 88% of scenarios due to missing nodes, relationships, or context.

### Current State vs. Required State

| Metric | Current | Required | Gap |
|--------|---------|----------|-----|
| GDPR Articles | 14 | 99 | **85 missing (86%)** |
| GDPR Recitals | 0 | 173 | **173 missing (100%)** |
| EU AI Act Articles | 11 | 113 | **102 missing (90%)** |
| EU AI Act Annexes | 2 partial | 13 complete | **11 missing (85%)** |
| Definitions | 13 | 100+ | **87+ missing (87%)** |
| Cross-Regulation Links | 7 | 200+ | **193+ missing (96%)** |
| Case Law | 0 | 50+ | **50+ missing (100%)** |
| EDPB Guidelines | 0 | 30+ | **30+ missing (100%)** |
| Enforcement Actions | 0 | 100+ | **100+ missing (100%)** |

---

## 1. GDPR DATA GAP ANALYSIS

### 1.1 Missing Articles (85 of 99)

#### Chapter I: General Provisions (Articles 1-4)
- [x] Article 1: Subject matter ✓
- [x] Article 2: Material scope ✓
- [x] Article 3: Territorial scope ✓
- [x] Article 4: Definitions ✓

#### Chapter II: Principles (Articles 5-11)
- [x] Article 5: Principles ✓
- [x] Article 6: Lawfulness ✓
- [ ] **Article 7: Conditions for consent** - CRITICAL for AI systems
- [ ] **Article 8: Child's consent** - CRITICAL for AI in education
- [x] Article 9: Special categories ✓
- [ ] **Article 10: Criminal convictions** - High-risk AI applications
- [ ] **Article 11: Processing not requiring identification**

#### Chapter III: Rights of Data Subject (Articles 12-23)
- [ ] **Article 12: Transparent information** - CRITICAL
- [x] Article 13: Information when collected from subject ✓
- [x] Article 14: Information not from subject ✓
- [ ] **Article 15: Right of access** - CRITICAL
- [ ] **Article 16: Right to rectification** - CRITICAL
- [x] Article 17: Right to erasure ✓
- [ ] **Article 18: Right to restriction** - CRITICAL
- [ ] **Article 19: Notification obligation**
- [ ] **Article 20: Right to data portability** - CRITICAL
- [ ] **Article 21: Right to object** - CRITICAL for profiling
- [x] Article 22: Automated decision-making ✓
- [ ] **Article 23: Restrictions**

#### Chapter IV: Controller/Processor (Articles 24-43)
- [ ] **Article 24: Responsibility of controller** - CRITICAL
- [x] Article 25: Privacy by design ✓
- [ ] **Article 26: Joint controllers**
- [ ] **Article 27: Representatives**
- [ ] **Article 28: Processor** - CRITICAL for AI service providers
- [ ] **Article 29: Processing under authority**
- [x] Article 30: Records of processing ✓
- [ ] **Article 31: Cooperation with supervisory authority**
- [ ] **Article 32: Security of processing** - CRITICAL
- [ ] **Article 33: Breach notification to authority** - CRITICAL
- [ ] **Article 34: Breach notification to subject** - CRITICAL
- [x] Article 35: DPIA ✓
- [ ] **Article 36: Prior consultation**
- [ ] **Article 37: DPO designation** - CRITICAL
- [ ] **Article 38: DPO position**
- [ ] **Article 39: DPO tasks**
- [ ] **Article 40: Codes of conduct**
- [ ] **Article 41: Monitoring of codes**
- [ ] **Article 42: Certification**
- [ ] **Article 43: Certification bodies**

#### Chapter V: International Transfers (Articles 44-50)
- [ ] **Article 44: General principle for transfers** - CRITICAL
- [ ] **Article 45: Adequacy decisions**
- [ ] **Article 46: Appropriate safeguards** - CRITICAL for cloud AI
- [ ] **Article 47: Binding corporate rules**
- [ ] **Article 48: Transfers not authorized by Union law**
- [ ] **Article 49: Derogations** - CRITICAL
- [ ] **Article 50: International cooperation**

#### Chapter VI: Supervisory Authorities (Articles 51-59)
- [ ] **Articles 51-59: All missing**

#### Chapter VII: Cooperation and Consistency (Articles 60-76)
- [ ] **Articles 60-76: All missing**

#### Chapter VIII: Remedies, Liability and Penalties (Articles 77-84)
- [ ] **Article 77: Right to lodge complaint** - CRITICAL
- [ ] **Article 78: Right to judicial remedy vs authority**
- [ ] **Article 79: Right to judicial remedy vs controller**
- [ ] **Article 80: Representation of data subjects**
- [ ] **Article 81: Suspension of proceedings**
- [ ] **Article 82: Right to compensation** - CRITICAL
- [ ] **Article 83: Administrative fines** - CRITICAL
- [ ] **Article 84: Penalties** - CRITICAL

#### Chapter IX-XI: (Articles 85-99)
- [ ] **Articles 85-99: All missing**

### 1.2 Missing Recitals (173 of 173)

Recitals provide CRITICAL interpretive context. For multi-hop reasoning, these are essential:

**Key Missing Recitals:**
- Recitals 1-14: Scope and principles interpretation
- Recitals 15-31: Definitions clarification
- **Recitals 32-43: Consent requirements** - CRITICAL for AI
- **Recitals 63-73: Data subject rights context** - CRITICAL
- **Recitals 71: Profiling interpretation** - CRITICAL for AI
- **Recitals 75-77: Risk assessment** - CRITICAL
- **Recitals 84-94: Security and breaches** - CRITICAL
- Recitals 101-116: International transfers
- **Recitals 148-152: Administrative fines** - CRITICAL

### 1.3 Missing Definitions (20+ of 26)

**GDPR Article 4 defines 26 terms, only 6 loaded:**
- [ ] Data subject
- [ ] Processing (partial)
- [ ] Restriction of processing
- [ ] Filing system
- [ ] Supervisory authority
- [ ] Main establishment
- [ ] Representative
- [ ] Enterprise
- [ ] Group of undertakings
- [ ] Binding corporate rules
- [ ] Cross-border processing
- [ ] Relevant and reasoned objection
- [ ] Information society service
- [ ] International organisation
- [ ] Genetic data
- [ ] Health data
- [ ] Pseudonymisation
- [ ] Recipient
- [ ] Third party

---

## 2. EU AI ACT DATA GAP ANALYSIS

### 2.1 Missing Articles (102 of 113)

#### Title I: General Provisions (Articles 1-4)
- [x] Article 1: Subject matter ✓
- [x] Article 2: Scope ✓
- [x] Article 3: Definitions ✓
- [ ] **Article 4: AI literacy** - CRITICAL

#### Title II: Prohibited AI (Article 5)
- [x] Article 5: Prohibited practices ✓ (partial)

#### Title III: High-Risk AI (Articles 6-51)
- [x] Article 6: Classification ✓
- [ ] **Article 7: Amendments to Annex III** - CRITICAL
- [ ] **Article 8: Compliance with requirements** - CRITICAL
- [x] Article 9: Risk management ✓
- [x] Article 10: Data governance ✓
- [x] Article 11: Technical documentation ✓
- [x] Article 12: Record-keeping ✓
- [x] Article 13: Transparency ✓
- [x] Article 14: Human oversight ✓
- [ ] **Article 15: Accuracy, robustness, cybersecurity** - CRITICAL
- [ ] **Article 16: Obligations of providers** - CRITICAL
- [ ] **Article 17: Quality management** - CRITICAL
- [ ] **Article 18: Documentation keeping**
- [ ] **Article 19: Conformity assessment**
- [ ] **Article 20: Automatically generated logs**
- [ ] **Article 21: Corrective actions**
- [ ] **Article 22: Reporting obligation**
- [ ] **Article 23: Cooperation with authorities**
- [ ] **Article 24: Obligations of product manufacturers**
- [ ] **Article 25: Authorized representatives**
- [ ] **Article 26: Obligations of deployers** - CRITICAL
- [ ] **Article 27: FRIA** - CRITICAL
- [ ] **Articles 28-49: All missing**
- [ ] **Article 50: Transparency for deployers** - CRITICAL

#### Title IV: GPAI Models (Articles 51-56)
- [ ] **Article 51: Classification of GPAI** - CRITICAL
- [ ] **Article 52: Obligations for GPAI providers** - CRITICAL
- [ ] **Article 53: Systemic risk GPAI** - CRITICAL
- [ ] **Article 54: Authorized representatives**
- [ ] **Article 55: Evaluation protocols**
- [ ] **Article 56: AI Office functions**

#### Titles V-XII (Articles 57-113)
- [ ] **ALL MISSING - Governance, Enforcement, Final Provisions**

### 2.2 Missing Annexes (11 of 13)

| Annex | Title | Status |
|-------|-------|--------|
| I | Harmonisation Legislation | **MISSING** |
| II | Conformity Assessment Procedures | **MISSING** |
| III | High-Risk AI Systems | **PARTIAL** (8/8 categories but lacking detail) |
| IV | Technical Documentation | **PARTIAL** |
| V | EU Declaration of Conformity | **MISSING** |
| VI | Internal Control Procedure | **MISSING** |
| VII | Conformity Assessment with Notified Body | **MISSING** |
| VIII | Information to be Submitted for Registration | **MISSING** |
| IX | Information for EU Database | **MISSING** |
| X | EU Legislation on Large-Scale IT Systems | **MISSING** |
| XI | Technical Documentation for GPAI | **MISSING** - CRITICAL
| XII | Transparency Information for GPAI | **MISSING** - CRITICAL
| XIII | Criteria for GPAI with Systemic Risk | **MISSING** - CRITICAL

### 2.3 Missing Definitions (61 of 68)

**EU AI Act Article 3 defines 68 terms, only 7 loaded:**

Critical missing definitions:
- [ ] Placing on the market
- [ ] Putting into service
- [ ] Intended purpose
- [ ] Reasonably foreseeable misuse
- [ ] Safety component
- [ ] Instructions for use
- [ ] Recall
- [ ] Withdrawal
- [ ] Performance
- [ ] Notifying authority
- [ ] Conformity assessment
- [ ] Conformity assessment body
- [ ] Notified body
- [ ] Substantial modification
- [ ] CE marking
- [ ] Post-market monitoring
- [ ] Market surveillance authority
- [ ] Harmonised standard
- [ ] Common specification
- [ ] Training data
- [ ] Validation data
- [ ] Testing data
- [ ] Input data
- [ ] Biometric data
- [ ] Biometric categorisation
- [ ] Real-time remote biometric identification
- [ ] Post remote biometric identification
- [ ] Publicly accessible space
- [ ] Law enforcement
- [ ] Law enforcement authority
- [ ] Serious incident
- [ ] Personal data (cross-ref GDPR)
- [ ] Special category data (cross-ref GDPR)
- [ ] Sensitive operational data
- [ ] General-purpose AI model
- [ ] GPAI model with systemic risk
- [ ] AI system for general purpose
- [ ] Floating-point operations (FLOPs)
- [ ] Downstream provider
- [ ] Free and open-source licence
- [ ] National competent authority
- [ ] National supervisory authority
- [ ] AI regulatory sandbox
- [ ] Testing in real-world conditions
- [ ] Informed consent
- [ ] AI Office
- [ ] AI Board
- [ ] Scientific Panel

---

## 3. MISSING CROSS-REGULATION RELATIONSHIPS

### 3.1 GDPR → EU AI Act Mappings Required

| GDPR Provision | EU AI Act Provision | Relationship Type |
|----------------|---------------------|-------------------|
| Art 4 (definitions) | Art 3 (definitions) | HARMONIZES_WITH |
| Art 5 (principles) | Art 10 (data governance) | COMPLEMENTS |
| Art 6 (lawfulness) | Art 6 (high-risk classification) | TRIGGERS |
| Art 7 (consent) | Art 5 (prohibited practices) | INTERSECTS |
| Art 9 (special categories) | Annex III (high-risk) | CLASSIFIED_AS |
| Art 13-14 (transparency) | Art 13 (transparency) | REINFORCES |
| Art 22 (automated decisions) | Art 14 (human oversight) | REQUIRES |
| Art 25 (privacy by design) | Art 9 (risk management) | COMPLEMENTS |
| Art 32 (security) | Art 15 (cybersecurity) | INTERSECTS |
| Art 35 (DPIA) | Art 27 (FRIA) | REQUIRES |
| Art 83 (fines) | Art 99 (penalties) | CUMULATIVE |

### 3.2 Actor Mapping Required

| GDPR Actor | EU AI Act Actor | Relationship |
|------------|-----------------|--------------|
| Controller | Provider | MAY_BE |
| Controller | Deployer | MAY_BE |
| Processor | Provider | MAY_BE |
| Data Subject | Affected Person | EQUIVALENT |
| DPA | AI Office | COORDINATES_WITH |
| EDPB | AI Board | COORDINATES_WITH |

---

## 4. MISSING ENTITY TYPES (Schema Enhancement Required)

Current schema has 14 entity types. Required: **25+ entity types**

### New Entity Types Required:

```python
class EntityType(str, Enum):
    # Existing types...

    # NEW: Procedural entities
    PROCEDURE = "Procedure"              # DPIA, FRIA, Conformity Assessment
    SAFEGUARD = "Safeguard"              # Technical/organizational measures
    EXEMPTION = "Exemption"              # Carve-outs and exceptions
    DEROGATION = "Derogation"            # Member state variations

    # NEW: Temporal entities
    DEADLINE = "Deadline"                # Compliance dates
    TRANSITION_PERIOD = "TransitionPeriod"  # Phase-in periods

    # NEW: Interpretive entities
    GUIDANCE = "Guidance"                # EDPB guidelines, AI Office guidance
    CASE_LAW = "CaseLaw"                 # CJEU decisions
    ENFORCEMENT_ACTION = "EnforcementAction"  # DPA decisions, fines
    OPINION = "Opinion"                  # EDPB opinions

    # NEW: Technical entities
    STANDARD = "Standard"                # ISO, EN standards
    BENCHMARK = "Benchmark"              # Performance thresholds
    METRIC = "Metric"                    # Compliance metrics

    # NEW: Documentation entities
    TEMPLATE = "Template"                # Required documentation templates
    RECORD = "Record"                    # Required records (Art 30, Art 12)
    REGISTER = "Register"                # EU Database entries

    # NEW: Organizational entities
    ROLE = "Role"                        # DPO, AI Officer, etc.
    BODY = "Body"                        # Notified bodies, certification bodies
```

### New Relationship Types Required:

```python
class RelationshipType(str, Enum):
    # Existing types...

    # NEW: Temporal relationships
    PRECEDES = "PRECEDES"
    FOLLOWS = "FOLLOWS"
    SUPERSEDES = "SUPERSEDES"
    EFFECTIVE_FROM = "EFFECTIVE_FROM"
    EXPIRES_ON = "EXPIRES_ON"

    # NEW: Interpretive relationships
    INTERPRETS = "INTERPRETS"
    CLARIFIES = "CLARIFIES"
    OVERRIDES = "OVERRIDES"
    HARMONIZES_WITH = "HARMONIZES_WITH"

    # NEW: Conditional relationships
    CONDITIONAL_ON = "CONDITIONAL_ON"
    ALTERNATIVE_TO = "ALTERNATIVE_TO"
    CUMULATIVE_WITH = "CUMULATIVE_WITH"

    # NEW: Compliance relationships
    SATISFIED_BY = "SATISFIED_BY"
    EVIDENCED_BY = "EVIDENCED_BY"
    DOCUMENTED_IN = "DOCUMENTED_IN"

    # NEW: Actor relationships
    NOTIFIES = "NOTIFIES"
    SUPERVISES = "SUPERVISES"
    COORDINATES_WITH = "COORDINATES_WITH"
    REPORTS_TO = "REPORTS_TO"
```

---

## 5. MISSING INTERPRETIVE CONTEXT

### 5.1 EDPB Guidelines Required (30+)

| Guideline | Topic | Impact |
|-----------|-------|--------|
| WP29 Opinion 4/2007 | Personal data concept | CRITICAL |
| WP29 Guidelines on consent | Consent requirements | CRITICAL |
| WP29 Guidelines on profiling | Art 22 interpretation | CRITICAL |
| WP29 Guidelines on transparency | Art 12-14 | CRITICAL |
| WP29 Guidelines on DPIA | Art 35 | CRITICAL |
| EDPB Guidelines 3/2019 | Video surveillance | HIGH |
| EDPB Guidelines 5/2020 | Consent | CRITICAL |
| EDPB Guidelines 7/2020 | Controller/processor | CRITICAL |
| EDPB Guidelines 8/2020 | Targeting social media | HIGH |
| EDPB Guidelines 01/2021 | Art 22 and AI | CRITICAL |
| EDPB Guidelines 02/2021 | Virtual voice assistants | HIGH |
| EDPB Guidelines 04/2021 | Codes of conduct | MEDIUM |
| EDPB Guidelines 01/2022 | Data breach notification | CRITICAL |
| EDPB Guidelines 03/2022 | Dark patterns | HIGH |

### 5.2 Case Law Required (50+)

| Case | Topic | Significance |
|------|-------|--------------|
| C-311/18 Schrems II | International transfers | CRITICAL |
| C-131/12 Google Spain | Right to be forgotten | CRITICAL |
| C-362/14 Schrems I | Safe Harbor | HIGH |
| C-210/16 Facebook Fan Pages | Joint controllership | HIGH |
| C-40/17 Fashion ID | Joint controllership | HIGH |
| C-673/17 Planet49 | Consent cookies | CRITICAL |
| C-61/19 Orange Romania | Consent requirements | HIGH |
| C-645/19 Facebook | Sensitive data profiling | CRITICAL |

### 5.3 Enforcement Actions Required (100+)

| Authority | Company | Amount | Topic |
|-----------|---------|--------|-------|
| CNIL | Google | €150M | Cookie consent |
| CNIL | Amazon | €35M | Cookie consent |
| DPC | Meta | €1.2B | International transfers |
| DPC | Meta | €405M | Children's data |
| DPC | WhatsApp | €225M | Transparency |
| Hamburg | H&M | €35M | Employee surveillance |
| AEPD | Google | €10M | Right to erasure |
| Italian DPA | Clearview AI | €20M | Biometric data |

---

## 6. MISSING TECHNICAL STANDARDS MAPPING

### ISO Standards Required:

| Standard | Topic | Relevance |
|----------|-------|-----------|
| ISO 27001 | Information security | CRITICAL |
| ISO 27701 | Privacy information management | CRITICAL |
| ISO 42001 | AI management systems | CRITICAL |
| ISO 22989 | AI concepts/terminology | HIGH |
| ISO 23894 | AI risk management | CRITICAL |
| ISO 24028 | AI trustworthiness | HIGH |
| ISO 25012 | Data quality | HIGH |
| ISO 25059 | AI quality model | HIGH |
| ISO 5259 | Data quality for analytics | HIGH |

### CEN/CENELEC Standards (Under Development):

| Standard | Topic | Status |
|----------|-------|--------|
| EN ISO 42001 | AI management | Published |
| CEN/CLC JTC 21 | AI Act harmonised standards | In development |
| EN 17926 | AI systems testing | In development |

---

## 7. MULTI-HOP REASONING FAILURE SCENARIOS

### Scenario Analysis: What queries would fail today?

**Query 1:** "What are the combined requirements for deploying a facial recognition system in an airport?"

Required traversal:
```
GDPR Art 9 (biometric data) → EU AI Act Art 5 (prohibited) →
EU AI Act Annex III.1 (high-risk) → EU AI Act Art 6 (classification) →
EU AI Act Art 9 (risk management) → EU AI Act Art 27 (FRIA) →
EU AI Act Art 43 (conformity) → EDPB Guidelines on facial recognition →
National DPA opinions on biometrics
```
**FAILURE POINTS:** Art 27, Art 43 details, EDPB guidelines, national opinions ALL MISSING

**Query 2:** "What penalties apply if we process children's data without proper consent for AI training?"

Required traversal:
```
GDPR Art 8 (child consent) → GDPR Art 7 (consent conditions) →
GDPR Art 9 (special categories) → GDPR Art 83 (fines) →
EU AI Act Art 10 (data governance) → EU AI Act Art 99 (penalties) →
EDPB Guidelines on children's data → Enforcement precedents
```
**FAILURE POINTS:** Art 7, Art 8, Art 83, Art 99, all guidelines, all precedents MISSING

**Query 3:** "How do I document compliance for a credit scoring AI system?"

Required traversal:
```
EU AI Act Annex III.5 (essential services) → EU AI Act Art 6 (classification) →
EU AI Act Art 11 (technical documentation) → EU AI Act Annex IV (requirements) →
EU AI Act Art 12 (record-keeping) → EU AI Act Art 9 (risk management) →
GDPR Art 35 (DPIA) → GDPR Art 30 (records) → ISO 42001 mapping
```
**FAILURE POINTS:** Annex IV details incomplete, Art 12 details missing, standards mapping MISSING

---

## 8. REQUIRED DATA ARCHITECTURE ENHANCEMENT

### Phase 1: Complete Core Regulations (Priority: CRITICAL)
- [ ] All 99 GDPR articles with full text
- [ ] All 173 GDPR recitals
- [ ] All 26 GDPR definitions
- [ ] All 113 EU AI Act articles with full text
- [ ] All 13 EU AI Act annexes complete
- [ ] All 68 EU AI Act definitions

### Phase 2: Cross-Regulation Relationships (Priority: CRITICAL)
- [ ] 200+ explicit cross-references
- [ ] Actor mappings
- [ ] Obligation chains
- [ ] Penalty accumulations

### Phase 3: Interpretive Layer (Priority: HIGH)
- [ ] 30+ EDPB guidelines
- [ ] 50+ CJEU case law
- [ ] 100+ enforcement actions
- [ ] AI Office guidance (when available)

### Phase 4: Technical Standards (Priority: HIGH)
- [ ] ISO standard mappings
- [ ] Harmonised standards (when published)
- [ ] Compliance checklists

### Phase 5: Dynamic Content (Priority: MEDIUM)
- [ ] Adequacy decisions
- [ ] SCCs and BCRs
- [ ] National implementation variations
- [ ] Regulatory sandbox outcomes

---

## 9. VECTOR EMBEDDING STRATEGY ENHANCEMENT

### Current Issue:
Only basic entity text is embedded. For multi-hop reasoning, need:

### Enhanced Embedding Strategy:

1. **Hierarchical Embeddings:**
   - Regulation-level summary embedding
   - Chapter-level context embedding
   - Article-level detail embedding
   - Paragraph-level precise embedding

2. **Relationship-Aware Embeddings:**
   - Embed relationship context with source/target
   - Include path context for common traversals

3. **Multi-Modal Embeddings:**
   - Legal text embeddings (precision)
   - Simplified explanation embeddings (accessibility)
   - Compliance question embeddings (queries)

4. **Cross-Reference Embeddings:**
   - GDPR ↔ EU AI Act joint embeddings
   - Article ↔ Recital paired embeddings
   - Article ↔ Guidance paired embeddings

---

## 10. RECOMMENDED KNOWLEDGE GRAPH STRUCTURE

### Graph Statistics Target:

| Metric | Current | Target | Multiplier |
|--------|---------|--------|------------|
| Total Nodes | ~40 | 2,500+ | 62x |
| Total Relationships | ~20 | 15,000+ | 750x |
| Relationship Types | 18 | 35+ | 2x |
| Entity Types | 14 | 25+ | 1.8x |
| Avg. Relationships/Node | 1.0 | 6.0 | 6x |
| Max Traversal Depth | 2 | 6 | 3x |
| Cross-Regulation Links | 7 | 500+ | 71x |

### Node Distribution Target:

| Entity Type | Count | % |
|-------------|-------|---|
| Article | 212 | 8.5% |
| Recital | 200+ | 8% |
| Definition | 100+ | 4% |
| Concept | 150+ | 6% |
| Obligation | 500+ | 20% |
| Right | 50+ | 2% |
| Penalty | 20+ | 1% |
| Authority | 50+ | 2% |
| Actor | 30+ | 1.2% |
| Guidance | 50+ | 2% |
| CaseLaw | 100+ | 4% |
| EnforcementAction | 200+ | 8% |
| Standard | 50+ | 2% |
| Procedure | 100+ | 4% |
| Other | 700+ | 28% |

---

## 11. IMMEDIATE ACTION ITEMS

### Critical (Must Have for MVP):
1. Complete GDPR articles (all 99)
2. Add GDPR recitals (key 50+)
3. Complete EU AI Act articles (all 113)
4. Complete EU AI Act annexes (all 13)
5. Add all definitions (94+)
6. Create obligation extraction pipeline
7. Build cross-regulation relationship mapping

### High Priority (Production Readiness):
8. Add EDPB guidelines (top 20)
9. Add key CJEU case law (top 30)
10. Add major enforcement actions (top 50)
11. Enhance schema with new entity types
12. Build compliance scoring system

### Medium Priority (Full Coverage):
13. Add all EDPB guidelines
14. Add national DPA guidance
15. Add ISO standard mappings
16. Add compliance checklists
17. Build audit trail functionality

---

## 12. CONCLUSION

**The current knowledge base is fundamentally insufficient for a multi-agent compliance automation system.**

### Key Failures:
1. **86% of GDPR articles missing** - Cannot answer most compliance questions
2. **100% of recitals missing** - No interpretive context
3. **90% of EU AI Act articles missing** - Cannot address most AI compliance
4. **100% of interpretive guidance missing** - No practical application context
5. **Sparse relationship density** - Multi-hop reasoning will fail

### Recommendation:
Implement the enhancements outlined in this document to achieve 100%+ data coverage before deploying any multi-agent compliance system. Estimated new content required:

- **2,000+ new entities**
- **15,000+ new relationships**
- **500+ cross-regulation mappings**
- **150+ interpretive documents**

Without these enhancements, the system will provide incomplete, potentially incorrect, and legally risky compliance guidance.

---

*This assessment was conducted with 20 years of data architecture experience in graph and vector databases.*


---


## SOURCE: `gdpr context/backup/knowledge_graph_gap_analysis.md`

# EU AI & GDPR Knowledge Graph: Gap Analysis & Mitigation Strategy

**Document Version**: 1.0  
**Date**: February 2026  
**Author**: Data Architecture Team  
**Purpose**: Systematic identification and remediation of knowledge base gaps for production-grade compliance automation

---

## Executive Summary

**Current Maturity**: 20% production-ready  
**Target Maturity**: 110% comprehensive coverage  
**Critical Gaps Identified**: 12  
**Estimated Remediation Timeline**: 6-8 weeks  
**Risk Level**: HIGH - Current system cannot reliably power compliance automation

---

## Gap #1: Incomplete Article Coverage

### Current State
- **GDPR**: 14/99 articles (14% coverage)
- **EU AI Act**: 11/113 articles (10% coverage)
- **Total Coverage**: 25/212 articles (12%)
- **Missing Critical Articles**:
  - GDPR Art 6 (Lawfulness of processing)
  - GDPR Art 22 (Automated decision-making)
  - GDPR Art 25 (Data protection by design)
  - AI Act Art 5 (Prohibited AI practices)
  - AI Act Art 9 (Risk management system)
  - AI Act Art 13 (Transparency obligations)

### Impact on Multi-Agent System
- **Risk Classifier Agent**: Cannot identify prohibited systems (Art 5)
- **GDPR Auditor Agent**: Missing lawfulness checks (Art 6)
- **Legal Research Agent**: Cannot cite 88% of regulations
- **Documentation Generator**: Incomplete compliance templates
- **System Reliability**: <20% query success rate

### Mitigation Strategy

**Phase 1: Automated Extraction (Week 1)**
```
Tools: EUR-Lex SPARQL API + Python parser
Process:
1. Fetch full GDPR regulation (EUR-Lex CELEX:32016R0679)
2. Fetch full EU AI Act (EUR-Lex CELEX:32024R1689)
3. Parse using XML/HTML structure
4. Extract: article_number, title, full_text, chapter, section
5. Store in JSON format matching existing schema
```

**Phase 2: Structured Data Modeling (Week 1)**
```
For each article, extract:
- Article metadata (number, title, regulation)
- Paragraph structure (1, 2, 3, a, b, c)
- Internal cross-references (e.g., "as referred to in Article 9")
- Key obligations (MUST, SHALL, REQUIRED)
- Exceptions (MAY, NOT REQUIRED IF, EXEMPT)
```

**Phase 3: Quality Validation (Week 2)**
```
Validation checks:
✓ All 99 GDPR articles present
✓ All 113 EU AI Act articles present
✓ Article text matches EUR-Lex source (checksum)
✓ No truncation or encoding errors
✓ Cross-references are valid article numbers
```

**Success Criteria**
- 100% article coverage (212/212)
- Zero text accuracy errors
- All articles loadable into Neo4j without errors

---

## Gap #2: Missing Recitals (Interpretive Context)

### Current State
- **GDPR Recitals**: 0/173 (0% coverage)
- **EU AI Act Recitals**: 0/88 (0% coverage)
- **Impact**: System has NO understanding of legislative intent

### Why This Matters
Recitals explain WHY articles exist and HOW to interpret them.

**Example**:
- **Article**: GDPR Art 35 requires DPIA for "high risk" processing
- **Recital 75**: Explains what constitutes "high risk" - includes profiling, large-scale special category data, systematic monitoring
- **Without Recital**: Agent doesn't know when to trigger DPIA requirement

### Impact on Multi-Agent System
- **Legal Research Agent**: Cannot explain reasoning behind rules
- **Risk Classifier**: Missing criteria for risk assessment
- **Documentation Generator**: Cannot justify compliance decisions
- **All Agents**: Lack contextual understanding for edge cases

### Mitigation Strategy

**Phase 1: Recital Extraction (Week 2)**
```
Data Model:
{
  "id": "GDPR_REC_75",
  "regulation": "GDPR",
  "recital_number": 75,
  "text": "The risk to the rights and freedoms...",
  "relates_to_articles": ["Art_35"],
  "key_concepts": ["high_risk", "dpia_triggers", "profiling"],
  "interpretation_guidance": "Provides examples of high-risk processing"
}
```

**Phase 2: Article-Recital Linking (Week 2)**
```
Neo4j Relationships:
(GDPR_ART_35:Article)-[:INTERPRETED_BY]->(GDPR_REC_75:Recital)
(GDPR_REC_75:Recital)-[:EXPLAINS]->(HighRiskProcessing:Concept)
(GDPR_REC_75:Recital)-[:PROVIDES_EXAMPLES]->(DPIATriggers:Concept)
```

**Phase 3: Semantic Enrichment (Week 3)**
```
For each recital:
1. Extract key interpretive points
2. Link to concrete concepts/definitions
3. Identify practical examples mentioned
4. Create "explanation chains" for agent reasoning
```

**Success Criteria**
- 173 GDPR + 88 EU AI Act recitals = 261 total
- Every article linked to relevant recitals
- Recitals queryable for contextual clarification

---

## Gap #3: Missing Annexes and Technical Specifications

### Current State
- **EU AI Act Annexes**: 0/13 covered
- **GDPR Does Not Have Annexes**: N/A
- **Critical Missing Content**:
  - Annex I: AI techniques and approaches
  - Annex II: Union harmonization legislation
  - Annex III: High-risk AI systems (THE CORE CLASSIFICATION LIST)
  - Annex IV: Technical documentation requirements
  - Annex V: Conformity assessment procedures

### Impact on Multi-Agent System
**CATASTROPHIC**: Annex III is the definitive list of high-risk AI systems.

**Example Query Failure**:
```
User: "Is recruitment AI high-risk?"
Agent: [Cannot answer - Annex III not in database]
Correct Answer: YES - Annex III, Section 4(a): "AI systems intended to be used 
for recruitment or selection of natural persons"
```

### Mitigation Strategy

**Phase 1: Annex Extraction (Week 2)**
```
Priority Order:
1. Annex III (High-risk systems) - CRITICAL
2. Annex I (AI techniques)
3. Annex IV (Technical documentation)
4. Annex V (Conformity assessment)
5. Remaining annexes (VI-XIII)

Data Model:
{
  "id": "AI_ACT_ANNEX_III",
  "regulation": "EU_AI_ACT",
  "annex_number": "III",
  "title": "HIGH-RISK AI SYSTEMS",
  "sections": [
    {
      "section_number": "4",
      "title": "Employment, workers management and access to self-employment",
      "subsections": [
        {
          "id": "ANNEX_III_4_A",
          "text": "AI systems intended to be used for recruitment...",
          "use_cases": ["recruitment", "selection", "hiring"]
        }
      ]
    }
  ]
}
```

**Phase 2: Use Case Mapping (Week 3)**
```
Create mappings:
(RecruitmentAI:AISystemType)-[:LISTED_IN]->(ANNEX_III_4_A:AnnexSection)
(ANNEX_III_4_A)-[:CLASSIFIED_AS]->(HighRisk:RiskCategory)
(HighRisk)-[:TRIGGERS]->(ConformityAssessment:Obligation)
(HighRisk)-[:REQUIRES]->(TechnicalDocumentation:Obligation)
(HighRisk)-[:REQUIRES]->(RiskManagementSystem:Obligation)
```

**Phase 3: Cross-Reference Integration (Week 3)**
```
Link annexes to articles:
(AI_ACT_ART_6:Article)-[:REFERENCES]->(ANNEX_III:Annex)
(AI_ACT_ART_16:Article)-[:SPECIFIES_IN]->(ANNEX_IV:Annex)
(AI_ACT_ART_43:Article)-[:DETAILS_IN]->(ANNEX_V:Annex)
```

**Success Criteria**
- All 13 annexes fully modeled
- Every use case in Annex III mapped to AI system types
- Annex-Article cross-references complete

---

## Gap #4: Sparse Relationship Density

### Current State
- **Existing Relationships**: ~50 relationships
- **Required for Production**: ~5,000+ relationships
- **Density**: <1% of required connectivity

### Relationship Type Breakdown

| Type | Current | Required | Gap |
|------|---------|----------|-----|
| Structural (CONTAINS, PART_OF) | ~30 | ~500 | 94% |
| Semantic (REQUIRES, TRIGGERS) | ~15 | ~2,000 | 99% |
| Cross-Regulation | ~5 | ~500 | 99% |
| Concept Links | 0 | ~2,000 | 100% |

### Impact on Multi-Agent System
- **Multi-hop reasoning fails**: Cannot traverse from query to answer
- **Missing inference paths**: Cannot deduce implicit requirements
- **Isolated knowledge islands**: Articles disconnected from obligations

**Example Failure**:
```
Query: "Does facial recognition for employee attendance require a DPIA?"

Required Path:
(FacialRecognition)-[:IS_TYPE]->(BiometricData)
  -[:CLASSIFIED_AS]->(SpecialCategory)
  -[:REGULATED_BY]->(GDPR_ART_9)
  
(EmployeeAttendance)-[:IS_USE_CASE]->(Employment)
  -[:LISTED_IN]->(AI_ACT_ANNEX_III_4)
  -[:CLASSIFIED_AS]->(HighRisk)
  
(BiometricData + HighRisk)-[:TRIGGERS]->(GDPR_ART_35_DPIA)

Current State: 0 of these 8 relationships exist
```

### Mitigation Strategy

**Phase 1: Explicit Relationship Extraction (Week 3-4)**
```
Method: Automated text analysis + LLM extraction

Step 1: Extract CONTAINS relationships
- Regulation CONTAINS Chapter
- Chapter CONTAINS Article
- Article CONTAINS Paragraph

Step 2: Extract REFERENCES relationships
- Parse text for "Article X", "paragraph Y"
- Create bidirectional links
- Validate reference targets exist

Step 3: Extract DEFINES relationships
- Identify definition sections (e.g., GDPR Art 4, AI Act Art 3)
- Link term → definition → usage locations
```

**Phase 2: Semantic Relationship Inference (Week 4)**
```
LLM-Assisted Extraction Prompt:

"Analyze this article text and identify:
1. REQUIRES relationships (what MUST be done)
2. PROHIBITS relationships (what MUST NOT be done)
3. TRIGGERS relationships (conditions that activate requirements)
4. EXEMPTS relationships (exceptions to rules)

For each relationship:
- Extract source entity
- Extract target entity
- Provide supporting text snippet
- Assign confidence score (0.0-1.0)"

Quality Gate: Human review all relationships with confidence < 0.9
```

**Phase 3: Cross-Regulation Mapping (Week 4)**
```
Critical Cross-References:

GDPR → AI Act:
- GDPR Art 35 (DPIA) ← AI Act Art 27 (requires DPIA for high-risk AI)
- GDPR Art 5 (principles) ← AI Act Art 10 (data governance must follow GDPR)
- GDPR Art 22 (automated decisions) ↔ AI Act Art 14 (human oversight)

AI Act → GDPR:
- AI Act Art 10 (data quality) → GDPR Art 5(1)(d) (accuracy principle)
- AI Act Art 11 (technical documentation) → GDPR Art 30 (records of processing)
```

**Phase 4: Concept Network Building (Week 5)**
```
Build hierarchical concept ontology:

DataType
├── PersonalData (GDPR Art 4(1))
│   ├── SpecialCategoryData (GDPR Art 9)
│   │   ├── BiometricData (GDPR Art 9(1))
│   │   ├── HealthData (GDPR Art 9(1))
│   │   └── GeneticData (GDPR Art 9(1))
│   └── RegularPersonalData
│       ├── IdentificationData
│       ├── LocationData
│       └── BehavioralData

Link concepts to:
- Source definitions
- Regulatory requirements
- Use case examples
- Related concepts
```

**Success Criteria**
- Minimum 5,000 validated relationships
- All critical compliance paths complete
- Multi-hop queries succeed with 95%+ accuracy

---

## Gap #5: Missing Temporal and Deadline Information

### Current State
- **Compliance Deadlines**: 0 modeled
- **Transitional Provisions**: 0 modeled
- **Effective Dates**: 0 modeled

### Why This Is Critical
The EU AI Act has **phased implementation over 3 years**:

| Deadline | Requirement |
|----------|-------------|
| Feb 2, 2025 | Prohibited AI systems ban takes effect |
| Aug 2, 2025 | Governance structure requirements |
| Aug 2, 2026 | General-purpose AI obligations |
| Aug 2, 2027 | High-risk AI system requirements (MAIN DEADLINE) |

### Impact on Multi-Agent System
- **Cannot answer**: "When must we comply with X?"
- **Cannot prioritize**: Which requirements are urgent vs future
- **Cannot advise**: On grandfathering/transitional rules

### Mitigation Strategy

**Phase 1: Deadline Extraction (Week 5)**
```
Data Model:
{
  "id": "DEADLINE_AI_ACT_ART_5",
  "article_id": "AI_ACT_ART_5",
  "requirement": "Prohibited AI systems ban",
  "effective_date": "2025-02-02",
  "grace_period": null,
  "applies_to": ["prohibited_systems"],
  "transitional_rules": "No grandfathering - immediate prohibition"
}
```

**Phase 2: Temporal Relationship Modeling (Week 5)**
```
Neo4j Relationships:
(AI_ACT_ART_5)-[:EFFECTIVE_FROM {date: "2025-02-02"}]->(ProhibitedSystems)
(AI_ACT_ART_6)-[:EFFECTIVE_FROM {date: "2027-08-02"}]->(HighRiskSystems)
(HighRiskSystem)-[:COMPLIANCE_DEADLINE {date: "2027-08-02"}]->(ConformityAssessment)
```

**Phase 3: Compliance Timeline Generator (Week 5)**
```
Query capability:
"What are all compliance deadlines for [AI system type]?"

Returns:
- Immediate requirements (already in force)
- Upcoming deadlines (next 12 months)
- Future requirements (12+ months)
- Grace periods and transitional provisions
```

**Success Criteria**
- All EU AI Act deadlines modeled (8+ distinct timelines)
- Queries can filter by "compliance required by [date]"
- Transitional provisions explicitly captured

---

## Gap #6: Missing Exception and Exemption Networks

### Current State
- **Exemptions Modeled**: 0
- **Derogations Modeled**: 0
- **Safe Harbors Modeled**: 0

### Why This Is Critical
Compliance isn't just about requirements - it's equally about knowing when requirements DON'T apply.

**Critical Exemptions**:
- Small enterprises (<250 employees) exempt from certain AI Act requirements
- Research and development exemptions (GDPR Art 89, AI Act Art 2(6))
- National security exclusions (GDPR Art 2(2)(a), AI Act Art 2(3))
- Purely personal/household activities (GDPR Art 2(2)(c))

### Impact on Multi-Agent System
- **False Positives**: Flags requirements that don't apply
- **Credibility Loss**: Users lose trust when over-flagging
- **Unusable Advice**: 100 requirements vs 10 actual requirements

**Example Failure**:
```
User: "I'm a solo entrepreneur testing an AI chatbot for my personal blog"
Current System: "You must comply with 47 AI Act obligations including conformity 
assessment, technical documentation, risk management system..."
Correct Answer: "Your use case falls under personal/household activity exemption 
(AI Act Art 2(1)(c)). Most obligations don't apply."
```

### Mitigation Strategy

**Phase 1: Exemption Extraction (Week 5)**
```
Identify all exemption clauses:

GDPR Exemptions:
- Art 2(2): Material scope exclusions
- Art 9(2): Special category exemptions (10 legal bases)
- Art 17(3): Right to erasure exemptions (5 grounds)
- Art 89: Research exemptions

AI Act Exemptions:
- Art 2: Scope exclusions (military, national security, research)
- Art 6(3): High-risk exemption for SMEs
- Art 83: Regulatory sandboxes
```

**Phase 2: Negative Relationship Modeling (Week 5)**
```
Neo4j Pattern:
(SmallEnterprise)-[:EXEMPT_FROM]->(HighRiskQMS)
(ResearchActivity)-[:EXEMPT_FROM {under: "GDPR_Art_89"}]->(ConsentRequirement)
(NationalSecurity)-[:EXCLUDED_FROM]->(GDPR_Scope)
(PersonalActivity)-[:EXCLUDED_FROM]->(AI_Act_Scope)

Properties:
- condition: What qualifies for exemption
- limitations: Any remaining obligations
- evidence_required: How to prove exemption applies
```

**Phase 3: Conditional Logic Implementation (Week 6)**
```
Rule Engine:
IF entity_type == "micro_enterprise" 
   AND employees < 50 
   AND annual_turnover < €10M
THEN exempt_from = [AI_Act_QMS, AI_Act_Monitoring]
ELSE apply_full_requirements

IF processing_purpose == "scientific_research"
   AND has_appropriate_safeguards == True
THEN exempt_from = [GDPR_Art_9_explicit_consent]
ELSE require_consent
```

**Success Criteria**
- All major exemptions modeled (30+ exemption rules)
- Exemption queries return accurate negative results
- False positive rate < 5%

---

## Gap #7: Missing Procedural Knowledge (How-To Workflows)

### Current State
- **Decision Trees**: 0 modeled
- **Step-by-Step Procedures**: 0 modeled
- **Compliance Workflows**: 0 modeled

### Why This Is Critical
Static rules don't tell users HOW to comply - only WHAT to comply with.

**Example**:
- **Static Knowledge**: "High-risk AI requires conformity assessment"
- **Procedural Knowledge**: 
  ```
  Step 1: Classify your AI system (use Annex III checklist)
  Step 2: If high-risk, determine assessment route (Annex VI or VII)
  Step 3: Prepare technical documentation (Annex IV requirements)
  Step 4: Conduct internal conformity assessment OR use notified body
  Step 5: Draw up EU declaration of conformity
  Step 6: Affix CE marking
  ```

### Impact on Multi-Agent System
- **Documentation Generator**: Cannot create step-by-step guides
- **Legal Research Agent**: Can cite rules but not execution paths
- **All Agents**: Knowledge is descriptive, not prescriptive

### Mitigation Strategy

**Phase 1: Workflow Extraction (Week 6)**
```
Identify procedural articles:
- GDPR Art 35: DPIA procedure (7 steps)
- GDPR Art 36: Prior consultation procedure (4 steps)
- AI Act Art 43: Conformity assessment procedures (6 routes)
- AI Act Art 16: Provider obligations (12-step checklist)

Data Model:
{
  "workflow_id": "DPIA_PROCEDURE",
  "source_article": "GDPR_ART_35",
  "steps": [
    {
      "step_number": 1,
      "action": "Describe systematic processing",
      "required_info": ["purposes", "data_categories", "recipients"],
      "responsible_party": "controller",
      "deliverable": "processing_description_document"
    },
    {
      "step_number": 2,
      "action": "Assess necessity and proportionality",
      "required_info": ["legitimate_interest", "alternatives_considered"],
      "responsible_party": "controller",
      "deliverable": "necessity_assessment"
    }
    // ... 5 more steps
  ],
  "decision_points": [
    {
      "at_step": 3,
      "question": "Is residual risk acceptable?",
      "if_yes": "proceed_to_step_4",
      "if_no": "redesign_processing_or_abandon"
    }
  ]
}
```

**Phase 2: Decision Tree Modeling (Week 6)**
```
Graph Pattern:
(UserQuery)-[:INITIATES]->(RiskClassification:DecisionTree)
  -[:STEP_1]->(CheckAnnexI:DecisionNode {question: "Does it use AI technique?"})
    -[:IF_YES]->(CheckAnnexIII:DecisionNode)
    -[:IF_NO]->(NotInScope:Outcome)
  -[:STEP_2]->(CheckAnnexIII {question: "Listed in Annex III?"})
    -[:IF_YES]->(HighRisk:Outcome)
    -[:IF_NO]->(CheckArticle6_3:DecisionNode)
  -[:STEP_3]->(CheckArticle6_3 {question: "Harmonized legislation?"})
    -[:IF_YES]->(HighRisk:Outcome)
    -[:IF_NO]->(LimitedOrMinimalRisk:Outcome)
```

**Phase 3: Executable Workflow Engine (Week 6)**
```
Neo4j Cypher for workflow traversal:
MATCH (start:WorkflowStep {workflow: "DPIA", step_number: 1})
MATCH path = (start)-[:NEXT_STEP*]->(end:WorkflowStep)
WHERE NOT (end)-[:NEXT_STEP]->()
RETURN path

// Returns complete execution sequence with decision points
```

**Success Criteria**
- 20+ key workflows fully modeled
- Decision trees for risk classification, DPIA triggers, conformity assessment
- Agents can generate step-by-step compliance guides

---

## Gap #8: Missing Evidence and Proof Requirements

### Current State
- **Documentation Requirements**: Not systematically captured
- **Burden of Proof**: Not modeled
- **Audit Trail Requirements**: Not linked to obligations

### Why This Is Critical
Compliance isn't binary - organizations must PROVE compliance.

**Example**:
- **Obligation**: "Ensure data quality" (AI Act Art 10)
- **Proof Required**: 
  - Data quality assessment report
  - Training data provenance documentation
  - Bias testing results
  - Data validation procedures
  - Update/correction logs

### Impact on Multi-Agent System
- **Documentation Generator**: Doesn't know WHAT documents to create
- **Compliance Auditor**: Cannot verify completeness of evidence
- **Users Get**: General advice but no concrete deliverables

### Mitigation Strategy

**Phase 1: Evidence Requirement Extraction (Week 6)**
```
For each obligation, extract:
{
  "obligation_id": "AI_ACT_ART_10_DATA_QUALITY",
  "evidence_required": [
    {
      "document_type": "data_quality_assessment",
      "contents": ["bias_analysis", "representativeness_check", "error_detection"],
      "retention_period": "10_years_after_system_decommission",
      "format": "technical_documentation_annex_iv",
      "who_creates": "provider",
      "who_reviews": "notified_body_or_market_surveillance"
    },
    {
      "document_type": "training_data_log",
      "contents": ["data_sources", "collection_methods", "preprocessing_steps"],
      "retention_period": "system_lifecycle",
      "format": "structured_metadata",
      "who_creates": "data_governance_team",
      "who_reviews": "internal_compliance"
    }
  ],
  "burden_of_proof": "provider_must_demonstrate",
  "audit_trigger": "market_surveillance_request"
}
```

**Phase 2: Documentation Template Linking (Week 6)**
```
Neo4j Relationships:
(AI_ACT_ART_10)-[:REQUIRES_EVIDENCE]->(DataQualityAssessment:Document)
(DataQualityAssessment)-[:CONTAINS_SECTION]->(BiasAnalysis:Section)
(BiasAnalysis)-[:REQUIRED_CONTENT {min_pages: 5}]->(StatisticalTests:Content)

(GDPR_ART_30)-[:REQUIRES_EVIDENCE]->(RecordsOfProcessing:Document)
(RecordsOfProcessing)-[:MUST_INCLUDE]->(ProcessingPurposes:Field)
(RecordsOfProcessing)-[:MUST_INCLUDE]->(DataCategories:Field)
```

**Phase 3: Compliance Checklist Generation (Week 6)**
```
Query: "What documentation is needed for high-risk recruitment AI?"

Returns:
✓ Technical Documentation (AI Act Annex IV)
  - System description and intended purpose
  - Data quality assessment report
  - Risk management documentation
  - Human oversight measures
  - Accuracy/robustness test results
  
✓ Records of Processing Activities (GDPR Art 30)
  - Controller/processor identification
  - Processing purposes
  - Data categories and recipients
  - Retention periods
  
✓ DPIA Report (GDPR Art 35)
  - Necessity and proportionality assessment
  - Risk identification and mitigation
  - DPO consultation documentation
```

**Success Criteria**
- Every obligation linked to evidence requirements
- Documentation templates machine-readable
- Agents can generate compliance checklists

---

## Gap #9: Missing Regulatory Guidance and Interpretations

### Current State
- **EDPB Guidelines**: 0 integrated
- **AI Office Guidance**: 0 integrated
- **National DPA Decisions**: 0 integrated
- **Official FAQs**: 0 integrated

### Why This Is Critical
Legal text is ambiguous. Official guidance provides authoritative interpretations.

**Example**:
- **GDPR Art 9**: "Explicit consent" for special category data
- **EDPB Guidelines 05/2020**: Defines "explicit" as:
  - Must be expressly confirmed in words
  - Checkboxes insufficient
  - Must be separate from other terms
  - Specific statement required

**Without guidance**: Agents might accept checkbox as "explicit consent"  
**With guidance**: Agents require verbal/written confirmation

### Impact on Multi-Agent System
- **Legal Research Agent**: Provides only text, no interpretation
- **Risk Classifier**: Uses strict reading, misses practical nuances
- **All Agents**: Technically correct but practically wrong

### Mitigation Strategy

**Phase 1: Priority Guidance Document Identification (Week 7)**
```
Top 20 EDPB Guidelines (most cited):
1. Guidelines 05/2020 - Consent
2. Guidelines 4/2019 - Article 25 Data Protection by Design
3. Guidelines 3/2019 - Video Device Processing
4. Guidelines 07/2020 - Concepts of Controller and Processor
5. Guidelines 04/2020 - Article 22 Automated Decision-Making
// ... 15 more

Top 10 AI Office Documents:
1. AI Act Implementation Roadmap
2. High-Risk AI System Classification Guidance
3. General-Purpose AI Model Requirements
4. Conformity Assessment Procedures Guide
// ... 6 more
```

**Phase 2: Guidance Document Structuring (Week 7)**
```
Data Model:
{
  "document_id": "EDPB_GUIDELINES_05_2020",
  "title": "Guidelines on Consent",
  "authority": "European Data Protection Board",
  "publication_date": "2020-05-04",
  "legal_status": "authoritative_interpretation",
  "applies_to_articles": ["GDPR_ART_4_11", "GDPR_ART_7"],
  "key_interpretations": [
    {
      "concept": "explicit_consent",
      "interpretation": "Requires express confirmation in words, not checkboxes",
      "practical_example": "Email confirmation with 'I explicitly consent to processing 
      my health data for medical research'",
      "incorrect_example": "Pre-ticked checkbox with 'I agree to terms'"
    }
  ],
  "case_studies": [...],
  "faq_section": [...]
}
```

**Phase 3: Interpretation Layer Integration (Week 7)**
```
Neo4j Relationships:
(GDPR_ART_7)-[:INTERPRETED_BY]->(EDPB_Guidelines_05_2020:Guidance)
(ExplicitConsent:Concept)-[:DEFINED_IN]->(EDPB_Guidelines_05_2020)
(ExplicitConsent)-[:PRACTICAL_EXAMPLE {correct: true}]->(EmailConfirmation:Example)
(ExplicitConsent)-[:PRACTICAL_EXAMPLE {correct: false}]->(PretickedCheckbox:Example)

Vector Store:
- Embed guidance document sections
- Link to relevant articles via metadata
- Enable semantic search: "what counts as explicit consent?"
```

**Phase 4: Precedent and Example Integration (Week 7)**
```
Link guidance to real-world examples:
(GDPR_ART_22)-[:GUIDANCE]->(EDPB_Guidelines_04_2020)
  -[:CASE_STUDY]->(SCHUFA_Decision:Example {
    scenario: "Credit scoring with automated decision",
    outcome: "Requires human intervention for final decision",
    authority: "German DPA"
  })
```

**Success Criteria**
- Top 20 EDPB guidelines integrated
- Top 10 AI Office documents integrated
- Guidance searchable via semantic queries
- Examples linked to abstract concepts

---

## Gap #10: Missing Case Law and Legal Precedents

### Current State
- **CJEU Cases**: 0 integrated
- **National DPA Decisions**: 0 integrated
- **Enforcement Actions**: 0 integrated

### Why This Is Critical
Case law shows how regulations are applied in practice and evolves interpretation.

**Example**:
- **Schrems II (C-311/18)**: Invalidated Privacy Shield, established data transfer standards
- **Impact**: Changed interpretation of GDPR Art 46 (international transfers)
- **Practical Effect**: Standard Contractual Clauses alone insufficient for US transfers

### Impact on Multi-Agent System
- **Legal Research Agent**: Cannot cite precedents
- **All Agents**: Miss evolving interpretations
- **Risk**: Advice based on outdated understanding

### Mitigation Strategy

**Phase 1: Landmark Case Identification (Week 8)**
```
Top 10 CJEU Cases for GDPR:
1. Schrems II (C-311/18) - International transfers
2. Google Spain (C-131/12) - Right to be forgotten
3. Fashion ID (C-40/17) - Joint controllership
4. Planet49 (C-673/17) - Consent and cookies
5. Wirtschaftsakademie (C-210/16) - Facebook page responsibility
// ... 5 more

Data Model:
{
  "case_id": "CJEU_C_311_18",
  "case_name": "Schrems II",
  "date": "2020-07-16",
  "court": "CJEU",
  "relevant_articles": ["GDPR_ART_45", "GDPR_ART_46"],
  "legal_question": "Are Standard Contractual Clauses valid for US data transfers?",
  "holding": "SCCs valid BUT supplementary measures required",
  "practical_impact": "Organizations must assess US surveillance laws case-by-case",
  "supersedes": ["Privacy_Shield_Decision"],
  "cited_by": [subsequent cases]
}
```

**Phase 2: Enforcement Action Database (Week 8)**
```
Major Fines and Enforcement:
{
  "enforcement_id": "IE_DPC_AMAZON_2021",
  "authority": "Irish DPC",
  "date": "2021-07-30",
  "company": "Amazon Europe",
  "fine_amount": "€746M",
  "violations": ["GDPR_ART_6", "GDPR_ART_13"],
  "facts": "Unlawful processing of personal data for behavioral advertising",
  "lessons": [
    "Legitimate interest insufficient for targeted advertising without consent",
    "Transparency obligations extend to algorithmic processing"
  ]
}
```

**Phase 3: Precedent Linking (Week 8)**
```
Neo4j Relationships:
(GDPR_ART_46)-[:INTERPRETED_BY]->(Schrems_II:Case)
(Schrems_II)-[:ESTABLISHES]->(SupplementaryMeasures:Concept)
(InternationalTransfer:Obligation)-[:REQUIRES {since: "2020-07-16"}]->(TransferImpactAssessment)

(GDPR_ART_6)-[:ENFORCEMENT_EXAMPLE]->(Amazon_Fine:EnforcementAction)
(Amazon_Fine)-[:DEMONSTRATES]->(LegitimateInterestLimits:Concept)
```

**Success Criteria**
- Top 10 CJEU cases integrated
- 20+ major enforcement actions documented
- Precedents linked to relevant articles
- Evolving interpretations tracked

---

## Gap #11: Missing Synonym and Terminology Mapping

### Current State
- **Synonym Clusters**: 0 defined
- **Terminology Variations**: Not mapped
- **Multilingual Terms**: English only

### Why This Is Critical
Users don't query using legal terminology. They use business language.

**Misalignment Examples**:
| User Says | Legal Term | Current System Response |
|-----------|------------|------------------------|
| "Employee tracking" | "Monitoring of workers' performance" | No results |
| "Facial recognition" | "Biometric identification system" | No results |
| "Customer profiling" | "Automated decision-making" | No results |
| "AI chatbot" | "AI system with limited risk" | No results |

### Impact on Multi-Agent System
- **Query Failure Rate**: 60%+ due to vocabulary mismatch
- **User Frustration**: "System doesn't understand my question"
- **Agents Cannot**: Map business context to legal framework

### Mitigation Strategy

**Phase 1: Terminology Extraction (Week 4)**
```
Build synonym clusters:
{
  "canonical_term": "controller",
  "legal_definition": "GDPR_ART_4_7",
  "synonyms": [
    "data controller",
    "person determining purposes",
    "organization processing data",
    "entity responsible for processing"
  ],
  "business_terms": [
    "company",
    "we", "us", "our organization",
    "data owner"
  ],
  "incorrect_terms": [
    "processor" // commonly confused
  ]
}
```

**Phase 2: Query Expansion (Week 4)**
```
When user queries: "employee monitoring AI"

Expand to legal terms:
- "employee" → ["worker", "natural person employed", "staff"]
- "monitoring" → ["surveillance", "performance tracking", "behavioral analysis"]
- "AI" → ["AI system", "automated system", "algorithmic decision-making"]

Graph Query:
MATCH (concept:Concept)
WHERE concept.name IN ["worker", "natural person employed"] 
   OR concept.synonyms CONTAINS "employee"
```

**Phase 3: Contextual Disambiguation (Week 4)**
```
When term has multiple meanings:
- "Processing" in GDPR context → data operations
- "Processing" in AI context → computation

Use context clues:
IF query contains ["training", "model", "algorithm"]
  THEN processing = AI_computation
ELSE IF query contains ["data", "personal", "consent"]
  THEN processing = data_operations
```

**Success Criteria**
- 500+ synonym mappings
- Business-to-legal term translation
- Query success rate >90%

---

## Gap #12: Missing Validation and Quality Assurance Framework

### Current State
- **Test Query Set**: 0 golden queries
- **Accuracy Metrics**: Not measured
- **Regression Testing**: Not implemented
- **Human Review Process**: Not defined

### Why This Is Critical
**Without validation, the entire system is untrustworthy.**

A single wrong legal citation in a compliance report can:
- Fail an audit (€35M+ fine risk)
- Create legal liability
- Destroy user confidence

### Impact on Multi-Agent System
- **Unknown Accuracy**: Could be 50% or 95% - we don't know
- **Silent Failures**: Wrong answers given confidently
- **No Quality Gates**: Bad data enters without detection

### Mitigation Strategy

**Phase 1: Golden Test Set Creation (Week 8)**
```
Categories of test queries:

1. Risk Classification (30 queries)
   - "Is facial recognition for marketing prohibited?"
   - "Is recruitment AI high-risk?"
   - "Is spam filter AI regulated?"

2. DPIA Triggers (20 queries)
   - "Does health data profiling require DPIA?"
   - "Is employee monitoring DPIA-required?"

3. Cross-Regulation (20 queries)
   - "Combined GDPR and AI Act requirements for hiring AI?"
   - "Data transfer rules for AI training data?"

4. Obligations (30 queries)
   - "What must provider do before deploying high-risk AI?"
   - "Documentation requirements for biometric systems?"

5. Exemptions (20 queries)
   - "Are small businesses exempt from AI Act?"
   - "Does research exemption apply to medical AI?"

6. Deadlines (10 queries)
   - "When must we comply with prohibited AI ban?"
   - "Grace period for existing high-risk systems?"

7. Edge Cases (20 queries)
   - "Is AI-generated content personal data?"
   - "Who is controller for AI-as-a-Service?"

Total: 150+ queries with expert-verified answers
```

**Phase 2: Answer Validation Schema (Week 8)**
```
For each test query:
{
  "query_id": "TEST_001",
  "query": "Is facial recognition for employee attendance prohibited?",
  "expected_answer": "NOT prohibited but HIGH-RISK",
  "expected_articles": [
    "AI_ACT_ART_5", // Check it's not in prohibited list
    "AI_ACT_ANNEX_III_4", // Employment use case
    "GDPR_ART_9", // Biometric data
    "GDPR_ART_35" // DPIA required
  ],
  "expected_reasoning_path": [
    "facial_recognition → biometric_data",
    "biometric_data → special_category",
    "employee_attendance → employment_context",
    "employment_context + AI → Annex_III_4",
    "Annex_III_4 → high_risk",
    "high_risk + biometric → DPIA_mandatory"
  ],
  "confidence_threshold": 0.95,
  "must_not_cite": ["AI_ACT_ART_5"], // Should NOT say it's prohibited
  "expert_verified_by": "legal_expert_id_456",
  "verification_date": "2024-02-01"
}
```

**Phase 3: Automated Testing Pipeline (Week 8)**
```
Daily Regression Tests:

1. Run all 150 test queries
2. Compare actual vs expected:
   - Article citations match?
   - Reasoning path correct?
   - Answer conclusion accurate?
3. Generate accuracy report:
   - Overall accuracy: X%
   - By category breakdown
   - Failed queries flagged
4. Alert if accuracy drops below 95%

Weekly Human Review:
- Sample 20 random real user queries
- Expert verifies agent responses
- Update test set with edge cases found
```

**Phase 4: Continuous Improvement Loop (Ongoing)**
```
Process:
1. Real user query fails or gets flagged
2. Expert reviews and determines correct answer
3. Add to test set as new golden query
4. Identify root cause (missing relationship? wrong extraction?)
5. Fix knowledge base
6. Re-run all regression tests
7. Deploy fix only if accuracy maintained
```

**Phase 5: Quality Metrics Dashboard (Week 8)**
```
Track and display:
- Article coverage: 212/212 ✓
- Relationship count: 5,247
- Test query accuracy: 97.3%
- Query success rate: 94.1%
- Avg confidence score: 0.89
- Failed queries (last 7 days): 12
- Manual corrections needed: 3

Alert thresholds:
- Accuracy < 95% → CRITICAL
- Success rate < 90% → WARNING
- Failed queries > 20/week → INVESTIGATE
```

**Success Criteria**
- 150+ golden queries with verified answers
- Automated testing runs daily
- Accuracy consistently >95%
- All failures investigated and resolved
- Human review process operational

---

## Implementation Timeline Summary

| Week | Focus Area | Deliverables |
|------|------------|--------------|
| **1** | Articles & Structure | 212 articles extracted, hierarchies built |
| **2** | Recitals & Annexes | 261 recitals, 13 annexes, article-recital links |
| **3** | Explicit Relationships | CONTAINS, PART_OF, REFERENCES (500+ rels) |
| **4** | Semantic Relationships | REQUIRES, TRIGGERS, concept ontology (2,000+ rels) |
| **5** | Temporal & Exemptions | Deadlines, exclusions, negative knowledge |
| **6** | Workflows & Evidence | Decision trees, documentation requirements |
| **7** | Guidance & Interpretation | EDPB guidelines, AI Office docs, examples |
| **8** | Precedents & Validation | Case law, test queries, quality framework |

---

## Risk Mitigation Priorities

### High Priority (Fix Immediately)
1. **Article Coverage** - Cannot operate without full regulatory text
2. **Annex III** - Core risk classification depends on it
3. **Relationship Density** - Multi-hop reasoning fails without connectivity
4. **Validation Framework** - Cannot trust system without testing

### Medium Priority (Fix in Phase 2)
5. **Recitals** - Improves interpretation quality
6. **Exemptions** - Reduces false positives
7. **Guidance Documents** - Enhances practical accuracy
8. **Workflows** - Makes advice actionable

### Lower Priority (Enhancement Phase)
9. **Case Law** - Nice-to-have for edge cases
10. **Temporal Data** - Important but not blocking
11. **Synonym Mapping** - Improves UX but workarounds exist
12. **Advanced Evidence Tracking** - Refinement feature

---

## Success Measurement Framework

### Coverage Metrics
- **Article Completeness**: 212/212 articles = 100%
- **Relationship Density**: >5,000 validated relationships
- **Concept Coverage**: >200 unique legal concepts
- **Guidance Integration**: >30 authoritative documents

### Quality Metrics
- **Test Query Accuracy**: >95% on 150+ golden queries
- **Retrieval Precision**: >90% relevant results in top 5
- **Multi-hop Success**: >85% correct reasoning chains
- **False Positive Rate**: <5% incorrect flagging

### Operational Metrics
- **Query Response Time**: <3 seconds for complex queries
- **System Uptime**: >99.5%
- **User Satisfaction**: >4.5/5 rating
- **Compliance Coverage**: 100% of regulated scenarios

---

## Conclusion

**Current State**: 20% production-ready  
**Target State**: 110% comprehensive coverage  
**Estimated Effort**: 8 weeks intensive development + ongoing maintenance  
**Critical Success Factor**: Rigorous validation at every step

**The knowledge graph is the foundation. If it's wrong, everything built on top is unreliable.**

Every relationship, every citation, every definition must be verified against official legal sources. There is zero tolerance for errors in a system where mistakes cost up to €35M.

---

**Document Status**: Draft for review  
**Next Steps**: 
1. Prioritize gaps 1-4 for immediate remediation
2. Assemble legal expert review team
3. Begin automated extraction pipeline development
4. Establish weekly quality gate reviews


---


## SOURCE: `gdpr context/backup/MERGED_GAP_ANALYSIS.md`

# MERGED GAP ANALYSIS: GDPR & EU AI Act Knowledge Graph

**Document Version:** 1.0
**Date:** 2026-02-12
**Authors:** Data Architecture Team & Data Architect (merged analysis)
**Purpose:** Consolidated identification, prioritization, and remediation plan for missing knowledge required to power production-grade multi-agent compliance automation.

---

## Executive Summary ✅

- **Current coverage (combined estimate):** ~12% article coverage (conservative) / maturity ~20% production-ready (KG team estimate).
- **Risk Level:** HIGH — knowledge base is insufficient for reliable compliance automation (multi-hop reasoning failures expected).
- **Key shortfalls:** Missing GDPR recitals (173/173), GDPR articles (85/99 missing in one assessment), EU AI Act articles and annexes (majority missing), definitions, interpretive guidelines (EDPB), case law and enforcement actions, and relationship density.
- **Estimated remediation timeline:** 6–8 weeks for core regulatory ingestion and basic linkage; additional 6–12 weeks for semantic relationship enrichment and validation.

---

## 1. Consolidated Coverage Metrics 📊

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| GDPR Articles | 14/99 (~14%) | 99/99 | ~~85 missing~~
| GDPR Recitals | 0/173 | 173/173 | 173 missing
| EU AI Act Articles | 11/113 (~10%) | 113/113 | ~~102 missing~~
| EU AI Act Annexes | 2 partial | 13 | 11 missing
| Definitions (GDPR + AI Act) | partial (20+/68 loaded) | 94+ | major gap
| EDPB Guidelines | 0/30+ | 30+ | 30+ missing
| Case Law | 0/50+ | 50+ | 50+ missing
| Enforcement Actions | 0/100+ | 100+ | 100+ missing
| Relationship Count | ~50 | 5,000+ | ~99% gap

> Note: Two assessments agree the KB is far from production-ready; numbers above unify both documents' findings.

---

## 2. Detailed Gap Areas & Critical Items ⚠️

### 2.1 GDPR (Critical missing items)
- Many core Articles across Chapters II–VIII are partially or fully missing; **critical**: Art 7 (consent), Art 12 (transparent information), Art 15–21 (data subject rights), Arts 24, 32–34, 35 (DPIA present), 37–39 (DPO), 44–50 (international transfers), 77–84 (remedies & penalties).
- **All recitals (1–173)** are missing — essential for interpretation and edge-case reasoning.
- Definitions from Art 4 largely incomplete (only ~6 of 26 terms loaded).

### 2.2 EU AI Act (Critical missing items)
- Large sections of Titles III–XII missing, including high-risk system obligations (Articles 15–27 and beyond), and governance and enforcement titles.
- **Annex III (High-risk systems)** and many annexes (I–XIII) are incomplete or missing — Annex III is critical for classification decisions.
- Definitions per Art 3 mostly missing (~61 of 68 missing).

### 2.3 Interpretive & Supporting Content
- **EDPB Guidelines** (30+), CJEU case law (50+), and enforcement actions (100+) are needed for normative and precedent context.
- **Technical standards mapping (ISO, CEN)** absent — important for compliance checklists and evidence.

### 2.4 Graph Connectivity & Schema
- Relationship density is extremely low (current ~50 relationships vs target 5,000+). Critical relationship types and new entity types are required (Procedures, Safeguards, Deadlines, Guidance, CaseLaw, EnforcementAction, Metrics, Templates, etc.).

---

## 3. Cross-Regulation Mappings & Actor Relationships 🔗
- Key mappings required (examples):
  - GDPR Art 35 (DPIA) ← AI Act Art 27 (FRIA/DPIA requirement)
  - GDPR Art 22 (automated decisions) ↔ AI Act Art 14 (human oversight)
  - GDPR Article definitions ↔ AI Act definitions (alignment/harmonisation)
- Actor mapping: Controller ↔ Provider/Deployer, DPA ↔ AI Office/AI Board; these must be modelled and linked to obligations and enforcement flows.

---

## 4. Multi-Hop Failure Scenarios (Representative) 🚨
- Queries that fail today include:
  - "Is recruitment AI high-risk?" → needs Annex III mapping (missing)
  - "Does facial recognition for employee attendance require a DPIA?" → requires linking biometric data → high-risk classification → GDPR Art 35 (missing relationships)
  - "What penalties apply for processing children's data without consent?" → requires Art 7/8/83 and AI Act cross-links (missing)

These highlight missing traversal paths (article → recital → annex → guideline → enforcement).

---

## 5. Mitigation Strategy & Implementation Phases ✅

### Phase 1 — Core Extraction (Week 1)
- Automated ingestion from EUR-Lex (GDPR CELEX, AI Act CELEX) using SPARQL/XML parsers.
- Extract article/paragaph structure, recitals, annexes, definitions.
- Success: 100% article coverage, correct text checksums.

### Phase 2 — Structure & Linking (Week 1–2)
- Model: Article, Recital, Annex, Definition, Concept, Obligation.
- Create Article ↔ Recital ↔ Annex links; record cross-references.

### Phase 3 — Semantic Enrichment (Week 2–4)
- LLM-assisted extraction of obligations, triggers, exemptions, and relationships (REQUIRES, TRIGGERS, INTERPRETS, CLARIFIES).
- Human review for confidence < 0.9.

### Phase 4 — Interpretive & Evidence Layer (Week 3–6)
- Ingest EDPB guidelines, CJEU case law, enforcement actions, and key national guidance.
- Map to articles/annexes and add precedent/evidence nodes.

### Phase 5 — Validation, Standards & Embeddings (Week 5–8)
- Add ISO/CEN mapping, temporal deadlines, and transitional provisions.
- Implement hierarchical and relationship-aware embeddings; generate test multi-hop queries and target 95%+ accuracy for critical paths.

**Estimated timeline:** Core regulation ingestion + basic linking (6–8 weeks), full semantic enrichment and validation (additional 6–12 weeks).

---

## 6. Schema & Relationship Enhancements (Technical) 🔧

### Suggested New Entity Types
- Procedure, Safeguard, Exemption, Derogation, Deadline, TransitionPeriod, Guidance, CaseLaw, EnforcementAction, Standard, Benchmark, Metric, Template, Record, Register, Role, Body.

### Suggested Relationship Types
- INTERPRETS, CLARIFIES, HARMONIZES_WITH, TRIGGERS, SATISFIED_BY, EVIDENCED_BY, EFFECTIVE_FROM, PRECEDES, COORDINATES_WITH, SUPERVISES, NOTIFIES.

---

## 7. Vector & Embedding Strategy 📈
- Use hierarchical embeddings (regulation/chapter/article/paragraph).
- Relationship-aware and cross-reference embeddings (article + recitals + guidance).
- Multi-modal embeddings: legal precision text + simplified explanation + Q/A probes.

---

## 8. Immediate Action Items (Critical Priorities) ⚡
1. Ingest all GDPR articles & recitals (99 + 173) — CRITICAL
2. Ingest all EU AI Act articles & annexes (113 + 13), prioritise Annex III — CRITICAL
3. Extract and normalise definitions for both regulations — CRITICAL
4. Build obligation extraction pipeline (LLM + rules) — CRITICAL
5. Create cross-regulation mappings for top 200+ links — CRITICAL
6. Add 30+ EDPB guidelines, top 30 CJEU cases, and 100+ enforcement actions — HIGH
7. Implement new entity & relationship types in schema — HIGH
8. Add temporal/deadlines model and populate known dates — MEDIUM

---

## 9. Success Criteria & Targets 🎯
- 100% coverage of articles & recitals with checksum-verified text
- 5,000+ validated relationships; 2,500+ nodes total
- Multi-hop compliance queries succeed with ≥95% accuracy for priority scenarios
- Embedding-based retrieval yields high precision and recalls for interpretive guidance

---

## 10. Conclusion ✨
The merged analysis confirms the knowledge base is currently unsuited for production-grade multi-agent compliance automation. The remediation plan above synthesises concrete extraction, modeling, and enrichment actions (short-term: ingestion and linking; mid-term: semantic relationship extraction and validation; longer-term: embedding tuning and procedural mapping). Prioritise Annex III, GDPR recitals, high-risk articles, and cross-regulation relationships to unlock most downstream reasoning capabilities.

---

*Notes: This merged document consolidates findings from `CRITICAL_GAP_ANALYSIS.md` and `knowledge_graph_gap_analysis.md`. Originals are preserved.*


---


## SOURCE: `gdpr context/backup/improve_v1.md`

Alright — first of all: this is already a serious system.
What you’ve built is not a toy GraphRAG. It’s a solid legal reasoning engine foundation.
Now let me do what you asked: tear it apart constructively 😄

I’ll structure this as:

What you’ve done really well

Core gaps (architectural, not “missing data”)

Edge cases you will hit in EU AI Act + GDPR

How to harden the system to be robust

Concrete upgrades (schema + retrieval + reasoning)

I’ll explicitly reference your architecture where relevant 

SYSTEM_ARCHITECTURE

1. What you’ve done right (don’t underestimate this)
A. Clean separation of concerns

You’ve nailed the vector ↔ graph split:

ChromaDB = semantic recall

Neo4j = legal structure + logic

RRF fusion = sensible hybrid glue

This is exactly the right mental model for legal RAG.

B. Entity-aligned IDs across systems

Your decision to keep Neo4j IDs == Vector IDs is huge:

GDPR_ART_35
AIACT_ART_6


This avoids 50% of GraphRAG pain later.

C. Cross-regulation links (even if few)

The fact that you already model:

ANNEX_III_1 → GDPR_ART_35 (TRIGGERS)


means you understand legal causality, not just similarity.

D. Interpretive sources exist

You already have:

CJEU case law

EDPB guidelines

Enforcement actions

Even though they’re not loaded yet, your data model anticipates real legal reasoning, which most systems don’t.

So: strong base. Now let’s get uncomfortable 😈

2. The biggest architectural gaps (not data coverage)
GAP 1: Articles are treated as atomic units

Right now:

One Article = one embedding

One Article = one reasoning node

This will break for:

Exceptions

Conditions

Multi-clause articles (e.g. GDPR Art 6, Art 9, Art 22)

Why this is dangerous

Example:

“GDPR Art 6 allows processing if condition X is met”

Vector search may retrieve Art 6
But which paragraph? which legal basis? which exception?

Your current model can’t pinpoint.

GAP 2: Conditions & exceptions are implicit, not first-class

You store:

"conditions": ["lawful basis", "explicit consent"]


But conditions are not nodes.

That means:

You can’t traverse exceptions

You can’t reason over “unless”, “provided that”, “except where”

In EU AI Act & GDPR, exceptions are more important than rules.

GAP 3: Confidence propagation is mathematically weak

You do:

path confidence = product(confidences)


This fails when:

One weak edge dominates

Interpretive edges (case law) mix with statutory edges

Legal reasoning ≠ probability multiplication.

GAP 4: No temporal versioning logic

EU AI Act is:

Phased

Transitional

Article-dependent effective dates

Right now:

effective_date exists, but not used in traversal


This will bite you for:

“Does this apply now?”

“What applies before 2026?”

GAP 5: Interpretive hierarchy is flat

CJEU cases, EDPB guidelines, recitals are all just “entities”.

But legally:

Treaty law > Regulation > Case law > Guidelines > Recitals


Your system doesn’t know this yet.

3. Edge cases you will hit (real legal pain points)
Edge Case 1: Conditional prohibition

EU AI Act Art 5:

Prohibited unless X and Y

Right now:

You model PROHIBITS

But not exception scope

Result: false absolute answers ❌

Edge Case 2: Actor-dependent obligations

Same article:

Obligation applies to provider

Different obligation applies to deployer

Your applies_to: list is not enough for reasoning.

Edge Case 3: Concept drift across regulations

Example:

“Biometric data” (GDPR)

“Remote biometric identification system” (AI Act)

These are not synonyms, but overlap.

Vector similarity will lie to you here.

Edge Case 4: Negative answers

User asks:

“Is X allowed?”

Correct answer is often:

“No, unless …”

Your current pipeline is optimized for retrieval, not refutation.

Edge Case 5: Over-triggering via ANNEX

ANNEX III triggers:

DPIA

Conformity assessment

Human oversight

Logging
…but not all at once, always.

Right now:

ANNEX_III → TRIGGERS → Article


is too strong.

4. How to make this system robust

Now the good part.

5. Concrete improvements (this is the “upgrade path”)
5.1 Introduce Paragraph & Clause nodes (critical)

Add:

:Paragraph
:Clause


Structure:

Article
 └─ CONTAINS → Paragraph
       └─ CONTAINS → Clause


Embed at Clause level, not Article.

This alone will:

Improve retrieval precision

Reduce hallucination

Enable exception handling

5.2 Make Conditions & Exceptions first-class citizens

Add nodes:

:Condition
:Exception


Example:

(Prohibition:Biometric_ID)
 ├─ HAS_EXCEPTION → (Exception:Law_Enforcement_Use)
       ├─ REQUIRES → (Condition:Judicial_Authorisation)
       ├─ REQUIRES → (Condition:Time_Limited)


Now your system can answer:

“Is biometric ID allowed in airports?”

With an actual graph path.

5.3 Split semantic vs normative relationships

Right now:

REFERENCES
TRIGGERS
APPLIES_TO


Introduce normative strength:

IMPOSES_OBLIGATION
CREATES_RIGHT
CREATES_PROHIBITION
INTERPRETS
CLARIFIES
ILLUSTRATES


This lets your reasoner weigh:

Hard law vs soft law

Interpretation vs obligation

5.4 Add legal authority weighting (not confidence)

Replace numeric confidence with:

authority_level:
  - PRIMARY_LAW
  - CASE_LAW
  - GUIDELINE
  - RECITAL


Then reasoning rules like:

If conflict → higher authority wins

This is much closer to legal reasoning.

5.5 Temporal logic nodes (silent killer fix)

Add:

:TemporalScope
- start_date
- end_date
- transitional


Attach to:

Articles

Obligations

Penalties

So you can answer:

“What applies today?”

5.6 Edge-case-safe retrieval strategy

Change flow slightly:

Vector search (clauses)
 → Graph expansion
 → Constraint checking (actor, data type, time)
 → Answer synthesis


The constraint checking step is missing right now.

This is where:

Actor mismatch

Data type mismatch

Temporal mismatch
get filtered out.

5.7 Anti-hallucination guardrail (important)

Before answering:

Check if retrieved graph contains:

At least 1 obligation/prohibition

At least 1 source article

Otherwise answer:

“Insufficient legal basis found”

This is huge for trust.

6. One honest verdict

You’ve built:

A strong retrieval system with early legal reasoning

To become production-grade compliance intelligence, you need to:

Decompose articles

Explicitly model conditions/exceptions

Introduce authority & time awareness

The good news?
👉 You don’t need to rewrite anything
This is an incremental evolution, not a rebuild.

---


## SOURCE: `gdpr context/backup/DATA_ENHANCEMENT_SUMMARY.md`

# Knowledge Base Enhancement Summary

## Overview

This document summarizes the comprehensive data enhancements made to support a multi-agent GDPR/EU AI Act compliance automation system.

---

## Files Created

### 1. Critical Gap Analysis
**File:** `CRITICAL_GAP_ANALYSIS.md`
- Detailed assessment of data coverage gaps
- Analysis of missing articles, recitals, definitions
- Multi-hop reasoning failure scenarios
- Recommended enhancement roadmap

### 2. Enhanced Schema
**File:** `core_2/src/graph/schema_enhanced.py`
- **25 entity types** (expanded from 14)
- **35+ relationship types** (expanded from 18)
- New entity categories:
  - Procedural (Procedure, Safeguard, Requirement)
  - Interpretive (Guidance, CaseLaw, EnforcementAction, Opinion)
  - Temporal (Deadline, TransitionPeriod)
  - Technical (Standard, Benchmark, Metric)
  - Compliance (Checklist, Control, Evidence)

### 3. Regulation Structures

**File:** `core_2/data/legal/gdpr_structure.json`
- Complete index of all 99 GDPR articles
- 11 chapter structure
- 173 recital index with key topics
- 26 definition terms

**File:** `core_2/data/legal/eu_ai_act_structure.json`
- Complete index of all 113 EU AI Act articles
- 13 chapter structure
- 13 annexes with detailed categories
- 68 definition terms
- Implementation timeline (2024-2027)

### 4. Entity Data Files

**File:** `core_2/data/entities/concepts_and_principles.json`
- 14 fundamental principles (GDPR + AI Act)
- 20+ core concepts with hierarchies
- Data type hierarchy
- AI risk classification hierarchy
- Actor mappings (GDPR ↔ AI Act)

**File:** `core_2/data/entities/obligations.json`
- 25+ GDPR obligations
- 15+ EU AI Act obligations
- 8 prohibited AI practices
- Penalty tier mappings
- Actor applicability

**File:** `core_2/data/entities/rights_and_remedies.json`
- 12 GDPR data subject rights
- 5 EU AI Act affected person rights
- Remedies and enforcement mechanisms
- GDPR/AI Act enforcement powers

**File:** `core_2/data/entities/authorities.json`
- 5 EU-level authorities (EDPB, EDPS, AI Office, AI Board, Scientific Panel)
- 12 national DPAs
- Notified bodies framework
- International bodies

**File:** `core_2/data/entities/penalties.json`
- GDPR penalty tiers (10M/2% and 20M/4%)
- EU AI Act penalty tiers (7.5M/1.5% to 35M/7%)
- Cumulative exposure analysis
- SME provisions
- Other consequences

**File:** `core_2/data/entities/cross_regulation_mappings.json`
- 25 explicit cross-regulation mappings
- 7 actor mappings
- 8 use case scenarios with combined requirements
- Penalty accumulation analysis

### 5. Interpretive Content

**File:** `core_2/data/interpretive/edpb_guidelines.json`
- 15 key EDPB/WP29 guidelines
- Topics: consent, profiling, DPIA, transparency, video surveillance, voice assistants
- Article interpretation mappings
- AI relevance annotations

**File:** `core_2/data/interpretive/case_law.json`
- 11 landmark CJEU cases
- Topics: Schrems II, Google Spain, Planet49, joint controllership, fines, compensation
- Provisions interpreted
- Practical impact analysis

**File:** `core_2/data/interpretive/enforcement_actions.json`
- 15 major enforcement actions
- Total tracked fines: EUR 4.5+ billion
- AI-specific cases: Clearview AI, OpenAI, Foodinho, Deliveroo
- Enforcement trends analysis

### 6. Data Loader Script
**File:** `core_2/scripts/load_complete_data.py`
- Comprehensive loader for all data files
- Creates standardized entity/relationship structures
- Supports graph and vector store integration
- Statistics and error tracking

---

## Coverage Analysis

### Before Enhancement
| Metric | Count |
|--------|-------|
| GDPR Articles | 14 |
| EU AI Act Articles | 11 |
| Definitions | 13 |
| Cross-Regulation Links | 7 |
| Interpretive Documents | 0 |
| Total Entities | ~40 |

### After Enhancement
| Metric | Count |
|--------|-------|
| GDPR Articles | 99 (indexed) |
| EU AI Act Articles | 113 (indexed) |
| Definitions | 94+ (indexed) |
| Cross-Regulation Links | 85+ |
| Interpretive Documents | 40+ |
| Concepts/Principles | 34+ |
| Obligations | 40+ |
| Rights | 17+ |
| Authorities | 20+ |
| Case Law | 11 |
| Enforcement Actions | 15 |
| **Total Entities** | **500+** |

---

## Multi-Hop Reasoning Capabilities

The enhanced knowledge base now supports complex compliance queries:

### Example Query Paths

**Query: "Facial recognition for employee attendance requirements"**
```
GDPR_ART_9 (biometric) → AIACT_ART_5 (prohibited practices check) →
AIACT_ANNEX_III_1 (high-risk biometrics) → AIACT_ART_14 (human oversight) →
GDPR_ART_35 (DPIA) → AIACT_ART_27 (FRIA) → EDPB_GL_2019_03 (video surveillance)
```

**Query: "Combined penalties for AI misuse"**
```
AIACT_ART_99 (AI penalties) → AIACT_PENALTY_TIER_1 (35M/7%) →
GDPR_ART_83 (GDPR penalties) → GDPR_PENALTY_TIER_2 (20M/4%) →
cross_regulation_mappings (cumulative) → ENF_CLEARVIEW (precedent)
```

**Query: "LLM compliance requirements"**
```
AIACT_ART_3 (AI system definition) → AIACT_ART_51 (GPAI classification) →
AIACT_ART_53 (GPAI obligations) → AIACT_ANNEX_XI (documentation) →
EDPB_STMT_2023_CHATGPT (guidance) → ENF_OPENAI_ITALY (precedent)
```

---

## Remaining Enhancements (Future Work)

### High Priority
1. **Full Article Text**: Fetch complete text from EUR-Lex
2. **Recitals**: Add all 173 GDPR + 180 EU AI Act recitals
3. **National DPA Guidance**: Add member state-specific guidance
4. **ISO Standard Mappings**: Add ISO 27001, ISO 42001, ISO 27701 mappings

### Medium Priority
5. **Adequacy Decisions**: Current list of adequate third countries
6. **SCCs Templates**: Standard contractual clauses analysis
7. **Sandbox Outcomes**: AI regulatory sandbox results
8. **Compliance Checklists**: Actionable compliance frameworks

### Lower Priority
9. **National Variations**: Member state implementation differences
10. **Sector-Specific Guidance**: Healthcare, finance, employment AI
11. **Technical Standards**: CEN/CENELEC harmonized standards (when published)

---

## Usage

### Running the Data Loader

```bash
cd core_2
python scripts/load_complete_data.py
```

### Integrating with Graph/Vector Stores

```python
from scripts.load_complete_data import ComprehensiveDataLoader
from stores.graph_store import Neo4jGraphStore
from stores.vector_store import ChromaVectorStore

loader = ComprehensiveDataLoader(
    data_dir=Path("data"),
    graph_store=Neo4jGraphStore(),
    vector_store=ChromaVectorStore()
)

result = loader.load_all()
print(f"Loaded {result['stats']['entities']} entities")
```

---

## API Considerations

The enhanced data structure supports these API query patterns:

1. **Semantic Search**: Find relevant concepts/articles by meaning
2. **Graph Traversal**: Navigate relationships (GDPR → AI Act)
3. **Multi-Hop Reasoning**: Complex compliance questions
4. **Precedent Lookup**: Find relevant case law and enforcement
5. **Obligation Extraction**: Get all requirements for a scenario
6. **Risk Classification**: Determine AI system risk level

---

## Quality Notes

- All data structures follow consistent schema patterns
- Entity IDs use standardized prefixes (GDPR_, AIACT_, ENF_, etc.)
- Relationships include confidence scores where applicable
- AI relevance annotations added throughout
- Cross-references validated for consistency

---

*Enhancement completed: 2024*
*Data Architect Assessment: Production-ready for multi-agent compliance automation*


---


---

# Run: docs/archive (pre-pivot)

---


## SOURCE: `docs/archive/PROJECT_ANALYSIS_pre_pivot.md`

# EU AI Regulatory Compliance Engine — Project Completeness Analysis

**Date:** February 23, 2026  
**Scope:** Full audit of all three core modules, infrastructure, data pipeline, and integration readiness.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Module-by-Module Analysis](#2-module-by-module-analysis)
   - [Core 1 — Monitoring & Governance](#21-core-1--monitoring--governance-port-8002)
   - [Core 2 — GraphRAG Legal Research](#22-core-2--graphrag-legal-research-port-8001)
   - [Core 3 — Compliance Agent (Orchestrator)](#23-core-3--compliance-agent-orchestrator-port-8000)
3. [Data Pipeline Status](#3-data-pipeline-status)
4. [Infrastructure & DevOps](#4-infrastructure--devops)
5. [Testing Coverage](#5-testing-coverage)
6. [Cross-Module Integration](#6-cross-module-integration)
7. [What's Left To Run the Full Pipeline](#7-whats-left-to-run-the-full-pipeline)
8. [Recommended Execution Order](#8-recommended-execution-order)

---

## 1. Executive Summary

| Aspect | Status | Notes |
|--------|--------|-------|
| **Core 1 (Monitoring)** | ✅ ~95% Complete | Fully implemented source code; needs env/DB setup only |
| **Core 2 (GraphRAG)** | ✅ ~90% Complete | All code implemented; data parsed & loaded; raw_data dir is empty (needs symlink or copy from New_Data) |
| **Core 3 (Compliance Agent)** | ✅ ~90% Complete | All 5 agents + supervisor workflow built; needs API keys and infra |
| **Data Pipeline** | ✅ ~85% Complete | Pre-parsed data exists (10 entity files, 10 relationship files, 3 interpretive files, 7 legal files); vector store JSON files exist in chroma_data/; raw_data/ is empty |
| **Docker / Infra** | ✅ ~90% Complete | All Dockerfiles, docker-compose files, master compose ready; `.env` is template only |
| **Tests** | ⚠️ ~70% Complete | Unit tests exist for all 3 modules; integration tests are mock-based; no end-to-end tests against live services |
| **Full Pipeline Runnable?** | ❌ Not Yet | Blocked by: missing API keys, empty raw_data dir, no `uv.lock` files verified, DB migrations not run |

**Bottom line:** The codebase is architecturally complete. All source files are implemented with real logic (not stubs). The blocking issues are environmental/operational, not code gaps.

---

## 2. Module-by-Module Analysis

### 2.1 Core 1 — Monitoring & Governance (Port 8002)

**Purpose:** Receives monitoring data from Core 2 and Core 3, performs EU AI Act Article 14 and GDPR Article 22 compliance checks, detects drift/bias, and sends alerts.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 55 | ✅ Complete | Pydantic Settings with all env vars |
| `src/api/main.py` | 657 | ✅ Complete | 15+ endpoints: decisions, GraphRAG queries, compliance status, violations, alerts, metrics, drift, bias |
| `src/api/middleware.py` | 68 | ✅ Complete | Prometheus metrics middleware |
| `src/api/rate_limit.py` | 64 | ✅ Complete | slowapi rate limiting with X-Forwarded-For support |
| `src/compliance/eu_ai_act.py` | 285 | ✅ Complete | Article 14 human oversight monitor with 3 rules |
| `src/compliance/gdpr.py` | 273 | ✅ Complete | Article 22 automated decision-making monitor with 5 rules |
| `src/monitoring/drift.py` | 348 | ✅ Complete | Evidently-based data/prediction/confidence drift detection |
| `src/monitoring/bias.py` | 297 | ✅ Complete | Chi-square bias detection across 10 protected attributes |
| `src/monitoring/metrics.py` | 202 | ✅ Complete | 15+ Prometheus metric definitions |
| `src/alerting/alert_manager.py` | 383 | ✅ Complete | Slack + email routing by severity, compliance violation alerts, bias alerts, drift alerts |
| `src/client/monitoring_client.py` | 248 | ✅ Complete | Client SDK for Core 2/3 to send data |
| `src/database/models.py` | 259 | ✅ Complete | 6 SQLAlchemy models: DecisionLog, GraphRAGQueryLog, ComplianceViolation, AlertLog, DriftReport, BiasReport |
| `src/database/session.py` | 72 | ✅ Complete | Engine, session factory, init_db, get_db dependency |

#### Dependencies (pyproject.toml)
- FastAPI, SQLAlchemy, asyncpg, psycopg2-binary, Alembic, Evidently, Prometheus-client, slowapi, structlog
- Dev: pytest, pytest-asyncio, pytest-cov, ruff, mypy

#### Gaps / Issues
- **No Alembic migrations folder** — `init_db()` uses `create_all()` which works but isn't production-grade
- Prometheus config (`prometheus.yml`) exists and is ready
- Grafana is commented out in docker-compose (optional)

---

### 2.2 Core 2 — GraphRAG Legal Research (Port 8001)

**Purpose:** Knowledge graph (Neo4j) + vector store for hybrid retrieval of EU AI Act and GDPR legal provisions. Exposes REST API for Core 3's Legal Research Agent.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 41 | ✅ Complete | Neo4j, ChromaDB (not actually used — see below), Google AI, retrieval params |
| `src/api/main.py` | 319 | ✅ Complete | 5 endpoints: vector/search, graph/traverse, hybrid/search, hybrid/reason, health |
| `src/schema/entities.py` | 296 | ✅ Complete | 19 entity types with Pydantic models |
| `src/schema/relationships.py` | 83 | ✅ Complete | 25 relationship types |
| `src/stores/graph_store.py` | 350 | ✅ Complete | Neo4j CRUD, batch operations, graph traversal, node counting |
| `src/stores/vector_store.py` | 186 | ✅ Complete | **Custom JSON-backed vector store** (NOT ChromaDB despite config) — cosine similarity search, metadata filtering |
| `src/retrieval/engine.py` | 248 | ✅ Complete | Hybrid Graph+Vector retrieval with RRF fusion |
| `src/retrieval/reasoning_engine.py` | 305 | ✅ Complete | LLM-powered multi-hop reasoning with citation validation, confidence scoring |
| `src/retrieval/query_models.py` | 176 | ✅ Complete | 6 answer types, typed request/response models |

#### Extractors (8 files) — All Implemented ✅
- `structural_extractor.py`, `rule_based_extractor.py`, `definition_extractor.py`
- `obligation_extractor.py`, `concept_extractor.py`, `right_extractor.py`
- `cross_regulation_extractor.py`, `__init__.py`

#### Parsers (7 files) — All Implemented ✅
- `article_parser.py`, `recital_parser.py`, `annex_parser.py`
- `case_law_parser.py`, `guideline_parser.py`, `enforcement_parser.py`
- `base_parser.py`

#### Data Pipeline Scripts (8 scripts) — All Implemented ✅
| Script | Purpose | Status |
|--------|---------|--------|
| `01_parse_raw_data.py` | Parse raw legal text → JSON entities | ✅ |
| `02_load_structural_kg.py` | Load structural entities into Neo4j | ✅ |
| `02a_extract_structural_rels.py` | Extract structural relationships | ✅ |
| `02b_validate_graph_local.py` | Validate local graph without Neo4j | ✅ |
| `03_extract_semantic.py` | Extract semantic entities via LLM | ✅ |
| `03b_extract_obligations.py` | Extract obligations | ✅ |
| `03c_extract_cross_regulation.py` | Extract cross-regulation links | ✅ |
| `03d_validate_full_graph.py` | Validate full graph | ✅ |
| `03e_extract_concepts.py` | Extract legal concepts | ✅ |
| `03f_extract_rights.py` | Extract data subject rights | ✅ |
| `04_load_full_kg.py` | Load all data into Neo4j | ✅ |
| `05_load_vector_store.py` | Build vector embeddings | ✅ |
| `06_demo_query.py` | Demo query script | ✅ |
| `07_run_golden_tests.py` | Run golden test queries | ✅ |
| `08_coverage_report.py` | Coverage analysis report | ✅ |

#### Pre-Parsed Data — Exists ✅
- **`parsed_data/entities/`**: 10 JSON files (actors, ai_system_types, concepts, data_types, definitions, exemptions, obligations, penalties, rights, risk_categories)
- **`parsed_data/relationships/`**: 10 JSON files (cites, complements, concept_links, containment, defines, interprets, obligation_links, references, right_links, semantic_links)
- **`parsed_data/legal/`**: 7 JSON files (ai_act articles, chapters, recitals, annexes; gdpr articles, chapters, recitals)
- **`parsed_data/interpretive/`**: 3 JSON files (case_law, edpb_guidelines, enforcement_actions)
- **`chroma_data/`**: 7 pre-built vector store JSON files (articles, concepts, definitions, interpretive, obligations, recitals, rights)

#### Gaps / Issues
- **`raw_data/` directory is EMPTY** — The pipeline scripts (01_parse_raw_data.py) expect raw legal texts here. The actual raw data appears to be in `New_Data/` at the project root. Need to symlink or copy `New_Data/` → `core_2_knowledge_base/raw_data/` OR update the config path.
- **Vector store implementation mismatch**: `config.py` has `chroma_host`/`chroma_port` settings but `vector_store.py` is actually a custom JSON-backed store (comment says "ChromaDB incompatible with Python 3.14"). Config settings for ChromaDB are dead code.
- `src/validation/` directory has only `__init__.py` — validation logic might be inline in scripts instead.
- **Google API key required** for embeddings (text-embedding-004) and LLM reasoning (gemini-1.5-pro / gemini-2.0-flash)

---

### 2.3 Core 3 — Compliance Agent / Orchestrator (Port 8000)

**Purpose:** Multi-agent LangGraph workflow that receives AI system descriptions, classifies risk, audits GDPR compliance, queries Core 2 for legal research, generates compliance documents, and produces a final report.

#### Source Files — All Implemented ✅

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `src/config.py` | 85 | ✅ Complete | Gemini + Anthropic keys, DB, Redis, module URLs, cost limits, CORS |
| `src/api/main.py` | 455 | ✅ Complete | Assessment CRUD, approval endpoints, statistics, health check |
| `src/agents/base.py` | 153 | ✅ Complete | Base class with LLM init (Gemini/Claude), cost tracking, audit logging |
| `src/agents/supervisor.py` | 552 | ✅ Complete | LangGraph StateGraph with 8 nodes, conditional edges, interrupt_before for human-in-loop, resume() |
| `src/agents/risk_classifier.py` | 398 | ✅ Complete | Article 5 prohibited patterns, Annex III high-risk categories, LLM capability extraction |
| `src/agents/technical_assessor.py` | 424 | ✅ Complete | 5 GDPR checklist items (Arts 5, 6, 9, 22, 32), data flow analysis, DPIA determination |
| `src/agents/legal_research.py` | 389 | ✅ Complete | GraphRAG API integration with retry, fallback to LLM, entity extraction, article ranking |
| `src/agents/documentation_generator.py` | 443 | ✅ Complete | DPIA, ROPA, Conformity Assessment, Transparency Notice generation via LLM |
| `src/state/compliance_state.py` | 234 | ✅ Complete | LangGraph TypedDict state with reducers (append, merge_dicts) |
| `src/control_plane/governance.py` | 294 | ✅ Complete | Rate limiter, per-agent policies, cost caps, authorization |
| `src/control_plane/approval_queue.py` | 291 | ✅ Complete | Human-in-loop approval with risk assessment, expiry, approve/reject |
| `src/database/models.py` | 137 | ✅ Complete | AssessmentModel with to/from state dict conversion |
| `src/database/repository.py` | 113 | ✅ Complete | Full CRUD + list + count operations |
| `src/database/session.py` | 56 | ✅ Complete | Async SQLAlchemy with asyncpg |
| `src/cache/redis_client.py` | 239 | ✅ Complete | Async Redis client for session state caching |
| `src/utils/cost_tracker.py` | 131 | ✅ Complete | Token counting with tiktoken, daily/session cost limits |
| `src/utils/error_handling.py` | 112 | ✅ Complete | Custom exceptions: AgentError, RateLimitError, CostLimitError, HumanApprovalRequired, GraphRAGError |
| `src/utils/logging.py` | 52 | ✅ Complete | structlog JSON logging |
| `src/templates/dpia_template.md` | — | ✅ Exists | DPIA Markdown template |
| `src/templates/conformity_assessment_template.md` | — | ✅ Exists | Conformity assessment template |

#### LangGraph Workflow Topology
```
classify_risk → check_human_review → [conditional]
                                      ├─ needs_review → await_approval (INTERRUPT) → assess_gdpr
                                      └─ proceed → assess_gdpr
assess_gdpr → research_legal → check_conflicts → generate_docs → synthesize → END
```
- **Interrupt support**: `interrupt_before=["await_approval"]` enables workflow pause/resume
- **Resume API**: `supervisor.resume(session_id, decision)` continues paused workflows

#### Gaps / Issues
- **`configs/` directory is EMPTY** — No YAML/JSON config files present. All config is via environment variables (which is fine, but the dir is dead).
- **`scripts/` directory is EMPTY** — No utility scripts (e.g., seed data, run assessment).
- **Cost tracker model pricing** is for OpenAI models (gpt-4o, gpt-4o-mini) but app uses **Gemini** models. The `estimate_cost()` falls back to `{"input": 0.01, "output": 0.03}` for unknown models, so it won't crash but costs will be inaccurate.
- **tiktoken** may not have Gemini tokenizer — it falls back to `cl100k_base`, which provides approximate but not exact token counts for Gemini.
- Several **artifact directories** exist with garbled names: `srcagents/`, `srcapi/`, `srccontrol_plane/`, `srcstate/`, `srctemplates/`, `srcutils/`, `testsintegration/`, `testsunit/`, `datagolden/` — these appear to be accidental copies/artifacts and should be cleaned up.

---

## 3. Data Pipeline Status

### Raw Data (New_Data/)
Comprehensive legal corpus is present at the project root:

| Category | Files | Status |
|----------|-------|--------|
| AI Act Chapters | 13 text files (chapters 1-13) | ✅ Present |
| AI Act Recitals | Multiple recital files | ✅ Present |
| AI Act Annexes | 1 text file | ✅ Present |
| GDPR Chapters | 11 text files (chapters 1-11) | ✅ Present |
| GDPR Recitals | Multiple recital files | ✅ Present |
| CJEU Case Law | 20+ case files + index | ✅ Present |
| EDPB Guidelines | 23+ guideline files + index | ✅ Present |
| Enforcement Actions | 17+ enforcement files + index | ✅ Present |

### Problem: `core_2_knowledge_base/raw_data/` is EMPTY
The pipeline scripts expect raw data at `core_2_knowledge_base/raw_data/` (or the path configured in `config.py` as `raw_data_dir`). The actual data is at `New_Data/` in the project root.

**Fix needed:** Either:
1. Copy/symlink `New_Data/*` → `core_2_knowledge_base/raw_data/`
2. Update `core_2_knowledge_base/src/config.py` → `raw_data_dir: Path = Path("../New_Data")`

### Pre-Processed Data — Already Built ✅
The parsed data and vector embeddings have already been generated and are available:
- `parsed_data/` — 30 JSON files across 4 subdirectories
- `chroma_data/` — 7 collection JSON files with pre-computed embeddings
- `golden_tests/test_queries.json` — 6 golden test queries

This means **scripts 01-05 have already been run successfully at some point**. Only Neo4j loading (scripts 02, 04) would need to be re-run against a fresh Neo4j instance.

---

## 4. Infrastructure & DevOps

### Docker Setup

| Component | File | Status |
|-----------|------|--------|
| Master docker-compose | `docker-compose.yml` | ✅ 182 lines, all 3 modules + PostgreSQL + Redis + Neo4j + Prometheus |
| Core 1 docker-compose | `core_1/docker-compose.yml` | ✅ Standalone with PostgreSQL + Prometheus |
| Core 2 docker-compose | `core_2_knowledge_base/docker-compose.yml` | ✅ Standalone with Neo4j |
| Core 3 docker-compose | `core_3/docker-compose.yml` | ✅ Standalone with PostgreSQL + Redis |
| Core 1 Dockerfile | `core_1/Dockerfile` | ✅ Multi-stage UV build |
| Core 2 Dockerfile | `core_2_knowledge_base/Dockerfile` | ✅ Multi-stage UV build, copies chroma_data + parsed_data |
| Core 3 Dockerfile | `core_3/Dockerfile` | ✅ Multi-stage UV build, copies golden test data |
| Pipeline script | `pipeline.ps1` | ✅ Unified lifecycle: start / stop / restart-orch / kill-ports |

### Environment Variables (.env)

| Variable | Required By | Status |
|----------|-------------|--------|
| `GEMINI_API_KEY` | Core 3 | ❌ Template placeholder |
| `GOOGLE_API_KEY` | Core 2 | ❌ Template placeholder |
| `ANTHROPIC_API_KEY` | Core 3 (optional) | ❌ Template placeholder |
| `NEO4J_PASSWORD` | Core 2 | ❌ Template placeholder |
| `SLACK_WEBHOOK_URL` | Core 1 (optional) | ❌ Template placeholder |

**All API keys need real values before the pipeline can run.**

### Services Required

| Service | Port | Required By | Docker Image |
|---------|------|-------------|--------------|
| PostgreSQL (Core 3) | 5432 | Core 3 Compliance Agent | postgres:15-alpine |
| PostgreSQL (Core 1) | 5433 | Core 1 Monitoring | postgres:15-alpine |
| Redis | 6379 | Core 3 session caching | redis:7-alpine |
| Neo4j | 7687 (bolt), 7474 (http) | Core 2 Graph Store | neo4j:5-community |
| Prometheus | 9091 | Core 1 metrics (optional) | prom/prometheus |

---

## 5. Testing Coverage

### Core 1 Tests
| File | Type | Status |
|------|------|--------|
| `tests/unit/test_compliance.py` | Unit | ✅ Exists |
| `tests/unit/test_monitoring.py` | Unit | ✅ Exists |
| `tests/unit/test_client.py` | Unit | ✅ Exists |
| `tests/integration/test_api.py` | Integration | ✅ Exists |

### Core 2 Tests
| File | Type | Status |
|------|------|--------|
| `tests/test_extractors.py` | Unit | ✅ Exists |
| `tests/test_retrieval.py` | Unit | ✅ Exists (VectorStore, QueryModels tested) |
| `tests/conftest.py` | Fixtures | ✅ Exists |

### Core 3 Tests
| File | Type | Status |
|------|------|--------|
| `tests/unit/test_risk_classifier.py` | Unit | ✅ 219 lines, well-structured |
| `tests/unit/test_technical_assessor.py` | Unit | ✅ Exists |
| `tests/unit/test_legal_research.py` | Unit | ✅ Exists |
| `tests/unit/test_documentation_generator.py` | Unit | ✅ Exists |
| `tests/unit/test_control_plane.py` | Unit | ✅ Exists |
| `tests/integration/test_api.py` | Integration | ✅ Exists |

### Cross-Module Tests
| File | Type | Status |
|------|------|--------|
| `tests/integration/test_cross_module.py` | Integration | ✅ 478 lines, mock-based (Core 3→2, Core 3→1, Core 2→1) |

### Test Gaps
- ❌ **No end-to-end tests** against live services
- ❌ **No load/performance tests**
- ❌ **Golden test runner** (`core_3/data/golden/test_cases.json` has 10+ test cases but no automated runner in Core 3)
- ⚠️ Cross-module tests use mocks — won't catch real integration issues
- ⚠️ No `conftest.py` in Core 1 or Core 3 test directories

---

## 6. Cross-Module Integration

### Core 3 → Core 2 (Legal Research Agent → GraphRAG API)

| Aspect | Status | Details |
|--------|--------|---------|
| HTTP client in Core 3 | ✅ | `legal_research.py` uses httpx with tenacity retry |
| Endpoint called | ✅ | `POST /api/v1/graph/traverse` and `POST /api/v1/hybrid/reason` |
| URL configuration | ✅ | `GRAPHRAG_API_URL` env var, defaults to `http://localhost:8001` |
| Fallback on failure | ✅ | Falls back to LLM-based research if GraphRAG unavailable |
| Request/response format match | ✅ | Core 3 sends `GraphTraverseRequest`-compatible JSON, Core 2 returns expected format |

### Core 3 → Core 1 (Compliance Agent → Monitoring API)

| Aspect | Status | Details |
|--------|--------|---------|
| Client SDK | ✅ | `core_1/src/client/monitoring_client.py` |
| URL configuration | ✅ | `MONITORING_API_URL` env var, defaults to `http://localhost:8002` |
| Integration in agents | ⚠️ Partial | Client SDK exists but Core 3 agents don't currently call `MonitoringClient` to report decisions |
| Data format | ✅ | `AgentDecision` and `GraphRAGQuery` models match Core 1's API models |

### Missing Integration
- **Core 3 agents do not actively report to Core 1.** The `MonitoringClient` exists but is not wired into the agent code. After each agent decision (risk classification, GDPR audit), Core 3 should call `monitor.track_agent_decision()`. This is planned but not yet implemented.

---

## 7. What's Left To Run the Full Pipeline

### Priority 1 — Blockers (Must Fix)

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 1 | **API keys not set** | All | Add real `GEMINI_API_KEY`, `GOOGLE_API_KEY` to `.env` |
| 2 | **`raw_data/` empty** | Core 2 | Symlink or copy `New_Data/` → `core_2_knowledge_base/raw_data/`; OR update config path |
| 3 | **Neo4j needs data loaded** | Core 2 | Run `04_load_full_kg.py` against a running Neo4j instance to populate the knowledge graph from parsed_data |
| 4 | **`uv.lock` files** | All | Run `uv lock` in each module directory to generate lock files (Dockerfiles reference `uv.lock*`) |
| 5 | **Database initialization** | Core 1, 3 | First startup creates tables via `create_all()`, but verify PostgreSQL is accessible |

### Priority 2 — Should Fix Before Demo

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 6 | **Cost tracker pricing** doesn't include Gemini models | Core 3 | Add `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-2.0-flash` to `MODEL_PRICING` dict |
| 7 | **Core 3 doesn't report to Core 1** | Cross-module | Wire `MonitoringClient` into supervisor/agents to report decisions and query metrics |
| 8 | **Artifact directories** exist | Core 3 | Delete `srcagents/`, `srcapi/`, `srccontrol_plane/`, `srcstate/`, `srctemplates/`, `srcutils/`, `testsintegration/`, `testsunit/`, `datagolden/` |
| 9 | **ChromaDB config is dead code** | Core 2 | Remove `chroma_host`/`chroma_port` from config or add a comment explaining they're unused |
| 10 | **`validation/` module empty** | Core 2 | Only has `__init__.py`; validation logic is in pipeline scripts |

### Priority 3 — Nice to Have

| # | Issue | Module | Fix |
|---|-------|--------|-----|
| 11 | Add Alembic migrations | Core 1, 3 | Replace `create_all()` with proper migration management |
| 12 | Add `conftest.py` to Core 1 & 3 test dirs | Core 1, 3 | Create shared fixtures |
| 13 | Add end-to-end test | Root tests/ | Test full flow: create assessment → verify all agents run → check monitoring received data |
| 14 | Add Grafana dashboards | Core 1 | Uncomment Grafana in docker-compose.yml, add pre-built dashboards |
| 15 | Golden test runner for Core 3 | Core 3 | Create script to run `data/golden/test_cases.json` against live API |
| 16 | `configs/` and `scripts/` dirs empty | Core 3 | Remove or populate |

---

## 8. Recommended Execution Order

To bring the full pipeline from current state to running:

```
Step 1:  Set real API keys in .env
            GEMINI_API_KEY=<your-key>
            GOOGLE_API_KEY=<your-key>  (can be same Gemini key)
            NEO4J_PASSWORD=<your-password>

Step 2:  Fix raw data path
            Copy or symlink New_Data/* → core_2_knowledge_base/raw_data/

Step 3:  Generate lock files
            cd core_1 && uv lock
            cd core_2_knowledge_base && uv lock
            cd core_3 && uv lock

Step 4:  Start infrastructure (Docker)
            docker-compose up -d neo4j compliance-db compliance-redis postgres prometheus

Step 5:  Load knowledge graph into Neo4j
            cd core_2_knowledge_base
            uv run python scripts/04_load_full_kg.py

Step 6:  Start all API services
            docker-compose up -d  (or use .\pipeline.ps1 -Action start -Mode docker)

Step 7:  Verify health endpoints
            curl http://localhost:8000/health  (Core 3)
            curl http://localhost:8001/health  (Core 2)
            curl http://localhost:8002/health  (Core 1)

Step 8:  Run a test assessment
            POST http://localhost:8000/api/v1/assessments
            {
              "system_description": "Facial recognition system for employee attendance...",
              "system_type": "facial_recognition",
              "deployment_context": "employee_monitoring",
              "company_name": "Test Corp"
            }

Step 9:  Run tests
            cd core_1 && uv run pytest
            cd core_2_knowledge_base && uv run pytest
            cd core_3 && uv run pytest
```

---

## Appendix: File Counts by Module

| Module | Source Files | Test Files | Config/Infra Files | Data Files |
|--------|-------------|------------|--------------------|-----------| 
| Core 1 | 12 .py files | 4 test files | Dockerfile, docker-compose, pyproject.toml, prometheus.yml | — |
| Core 2 | 20+ .py files | 3 test files | Dockerfile, docker-compose, pyproject.toml, MEMORY.md | 30+ parsed JSON, 7 vector JSON, 6 golden tests |
| Core 3 | 18 .py files, 2 .md templates | 6 test files | Dockerfile, docker-compose, pyproject.toml | 1 golden test JSON (10+ test cases) |
| Root | — | 1 integration test | docker-compose.yml, .env, start/stop scripts, CLAUDE.md, README.md | New_Data/ (80+ files) |

**Total estimated lines of application code:** ~7,500+  
**Total estimated lines of test code:** ~1,500+


---


## SOURCE: `docs/archive/README_pre_pivot.md`

# EU AI Regulatory Compliance Engine

**A complete multi-agent compliance platform for EU AI Act and GDPR assessments**

---

## Overview

This is an integrated platform consisting of three core modules that work together to automate AI compliance assessments:

### Core Modules

| Module | Description | Port | Technology |
|--------|-------------|------|------------|
| **core_3** | EU AI Act Compliance Automation Agent | 8000 | LangGraph, FastAPI |
| **core_2** | GraphRAG Legal Research Engine | 8001 | Neo4j, ChromaDB |
| **core_1** | AI Model Governance & Monitoring | 8002 | PostgreSQL, Prometheus |

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       USER/API CLIENT                         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│     CORE_3: Compliance Agent (Port 8000)                     │
│     • Risk Classification                                     │
│     • GDPR Assessment                                         │
│     • Document Generation                                     │
│     • Multi-Agent Orchestration                              │
└────────┬────────────────────────────┬────────────────────────┘
         │                            │
         │ Calls GraphRAG API         │ Reports to Monitoring
         ▼                            ▼
┌─────────────────────────┐  ┌──────────────────────────────────┐
│ CORE_2: GraphRAG (8001) │  │ CORE_1: Monitoring (8002)        │
│ • Neo4j Knowledge Graph │  │ • Decision Tracking              │
│ • Vector Store          │  │ • Compliance Violations          │
│ • Multi-hop Reasoning   │  │ • Drift Detection                │
│ • Legal Citation        │  │ • Bias Detection                 │
└─────────────────────────┘  └──────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- **Docker Desktop** (recommended) or Docker + Docker Compose
- **Python 3.11+** and **UV** (for local development)
- **Gemini API Key** (required — `GEMINI_API_KEY` and `GOOGLE_API_KEY`)
- **Neo4j Password** (will be set during setup)

### Option 1: Start All Modules with Docker (Recommended)

```powershell
# 1. Navigate to project root
cd "D:\60 Days\Projects\Portfolio_Series\Project_1_EU AI Regulatory Compliance Engine\Project_1_EU AI Regulatory Compliance Engine"

# 2. Create .env file (fill in real values)
# See .env file at project root — fill in API keys

# 3. Start all modules at once
docker-compose up -d
```

**All three modules will start and be available at:**
- Compliance Agent: http://localhost:8000
- GraphRAG API: http://localhost:8001
- Monitoring API: http://localhost:8002
- Neo4j Browser: http://localhost:7474
- Prometheus: http://localhost:9091

### Option 2: Start with PowerShell Script

```powershell
# Start all modules with Docker
.\pipeline.ps1 -Action start -Mode docker

# Or start in local development mode (default)
.\pipeline.ps1 -Action start

# Stop all modules
.\pipeline.ps1 -Action stop
```

### Option 3: Start Individual Modules

```powershell
cd core_3 && docker-compose up -d
cd core_2 && docker-compose up -d
cd core_1 && docker-compose up -d
```

---

## Usage

### 1. Start a Compliance Assessment

```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{
    "system_description": "Facial recognition for employee attendance tracking",
    "system_type": "facial_recognition",
    "deployment_context": "employee_monitoring",
    "company_name": "Acme Corp"
  }'
```

### 2. Query Legal Research Engine

```bash
curl -X POST http://localhost:8001/api/v1/hybrid/reason \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Does facial recognition require a DPIA under GDPR?",
    "max_hops": 3
  }'
```

### 3. Check Compliance Monitoring

```bash
curl http://localhost:8002/api/v1/compliance/status
curl http://localhost:8002/api/v1/compliance/violations
```

---

## Data Flow Example

```
User submits: "Facial recognition for hiring"
       ↓
[Core 3: Compliance Agent]
   1. Risk Classifier → "HIGH_RISK (EU AI Act Annex III)"
   2. Technical Assessor → "GDPR violations found"
   3. Legal Research Agent → Calls Core 2
       ↓
   [Core 2: GraphRAG]
      Query: "Does facial recognition for hiring require DPIA?"
      Graph traversal: facial_recognition → biometric_data → GDPR_Art_9 → DPIA
      Returns: YES + legal citations
       ↓
   4. Documentation Generator → Creates DPIA, ROPA, Conformity Assessment
   5. Supervisor → Synthesizes final report
       ↓
[Core 1: Monitoring]
   Tracks agent decisions, checks for policy violations, logs audit trail
       ↓
User receives: Complete compliance report with documentation
```

---

## Environment Variables

Create a `.env` file in the project root (template exists at `.env`):

```bash
GEMINI_API_KEY=your-gemini-key        # Core 3 (required)
GOOGLE_API_KEY=your-google-key        # Core 2 embeddings (required)
ANTHROPIC_API_KEY=sk-ant-your-key     # Core 3 fallback (optional)
NEO4J_PASSWORD=your-neo4j-password    # Core 2 (required)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL  # Core 1 (optional)
```

---

## Development

### Local Development (without Docker)

```powershell
cd core_1 && uv sync
cd core_2 && uv sync
cd core_3 && uv sync

# Terminal 1
cd core_1 && uv run uvicorn src.api.main:app --reload --port 8002

# Terminal 2
cd core_2 && uv run uvicorn src.api.main:app --reload --port 8001

# Terminal 3
cd core_3 && uv run uvicorn src.api.main:app --reload --port 8000
```

### Running Tests

```powershell
cd core_1 && uv run pytest
cd core_2 && uv run pytest
cd core_3 && uv run pytest
```

---

## Monitoring & Debugging

```bash
# View all service logs
docker-compose logs -f

# Check API health / Swagger docs
curl http://localhost:8000/docs  # Compliance Agent
curl http://localhost:8001/docs  # GraphRAG
curl http://localhost:8002/docs  # Monitoring

# Database access
docker exec -it compliance-db psql -U postgres -d compliance
docker exec -it monitoring-postgres psql -U postgres -d monitoring
# Neo4j: http://localhost:7474 (user: neo4j, password: your NEO4J_PASSWORD)
```

---

## Troubleshooting

```powershell
# Port conflict
netstat -ano | findstr :8000
taskkill /PID <process-id> /F

# Clean Docker restart
docker-compose down -v
docker-compose up -d --build
```

---

## Business Impact

| Metric | Value |
|--------|-------|
| Assessment time reduction | 84% (40h → 6.5h) |
| Cost reduction per assessment | 86% (£8,500 → £1,200) |
| Annual savings (15 assessments/month) | £1.3M |
| EU AI Act fine prevention | Up to €35M |
| Compliance detection time | <48 hours |

---

## License

MIT License — see LICENSE file for each module.

---

**Status**: Production Ready | API live at :8000, :8001, :8002


---


## SOURCE: `docs/archive/CLAUDE_pre_pivot.md`

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **EU AI Regulatory Compliance Engine** - a multi-agent compliance platform for EU AI Act and GDPR assessments. The system consists of three core modules that work together:

| Module | Purpose | Port | Key Tech |
|--------|---------|------|----------|
| **core_3** | Compliance Agent (orchestrator) | 8000 | LangGraph, FastAPI |
| **core_2** | GraphRAG Legal Research | 8001 | Neo4j, ChromaDB |
| **core_1** | Monitoring & Governance | 8002 | PostgreSQL, Prometheus, Evidently |

## Architecture

```
User → Core 3 (Compliance Agent) → orchestrates 5 agents:
       ├── Risk Classifier (EU AI Act classification)
       ├── Technical Assessor (GDPR auditing)
       ├── Legal Research Agent → calls Core 2 GraphRAG API
       ├── Documentation Generator (DPIA, ROPA, Conformity)
       └── Supervisor (LangGraph orchestrator)

       All agent decisions → reported to Core 1 (Monitoring)
```

**Key Integration**: Core 3's Legal Research Agent makes HTTP calls to Core 2's `/api/v1/hybrid/reason` endpoint for multi-hop legal reasoning. Core 1 monitors both systems for compliance violations and drift.

## Common Commands

### Starting Services

```powershell
# Start all modules (Docker - recommended)
docker-compose up -d

# Or start individually
cd core_3 && docker-compose up -d
cd core_2 && docker-compose up -d
cd core_1 && docker-compose up -d
```

### Local Development (without Docker)

```powershell
# Install dependencies for a module
cd core_3 && uv sync

# Run the API server
cd core_3 && uv run uvicorn src.api.main:app --reload --port 8000
cd core_2 && uv run uvicorn src.api.main:app --reload --port 8001
cd core_1 && uv run uvicorn src.api.main:app --reload --port 8002
```

### Testing

```powershell
# Run all tests for a module
cd core_3 && uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_risk_classifier.py -v
```

### Linting & Formatting

```powershell
# Check linting (ruff)
uv run ruff check src/

# Format code
uv run ruff format src/
```

### Using UV Scripts (core_3 only)

```powershell
cd core_3
uv run test     # pytest
uv run lint     # ruff check
uv run format   # ruff format
uv run serve    # uvicorn server
```

## Module Structure

### Core 3: Compliance Agent (main orchestrator)

```
core_3/src/
├── agents/
│   ├── supervisor.py         # LangGraph orchestrator
│   ├── risk_classifier.py    # EU AI Act classification
│   ├── technical_assessor.py # GDPR auditing
│   ├── legal_research.py     # Calls Core 2 GraphRAG
│   └── documentation_generator.py
├── api/main.py               # FastAPI endpoints
├── control_plane/
│   ├── governance.py         # Rate limits, cost caps
│   └── approval_queue.py     # Human-in-loop approvals
├── state/compliance_state.py # LangGraph shared state
└── templates/                # DPIA, Conformity templates
```

### Core 2: GraphRAG Legal Research

```
core_2/src/
├── graph/
│   ├── schema.py             # Neo4j entity types
│   └── extraction.py         # Entity extraction from legal text
├── stores/
│   ├── graph_store.py        # Neo4j operations
│   └── vector_store.py       # ChromaDB embeddings
├── retrieval/
│   ├── engine.py             # RRF hybrid retrieval
│   └── reasoning.py          # Multi-hop reasoning
└── api/main.py
```

### Core 1: Monitoring & Governance

```
core_1/src/
├── compliance/
│   ├── eu_ai_act.py          # Article 14 monitoring
│   └── gdpr.py               # Article 22 monitoring
├── monitoring/
│   ├── drift.py              # Evidently drift detection
│   └── bias.py               # Chi-square bias detection
├── alerting/alert_manager.py # Slack/email alerts
├── client/monitoring_client.py # Client SDK for other modules
└── api/main.py
```

## Key API Endpoints

### Core 3 (Port 8000)
- `POST /api/v1/assessments` - Start compliance assessment
- `GET /api/v1/assessments/{id}` - Get assessment results
- `GET /api/v1/approvals` - List pending human approvals
- `POST /api/v1/approvals/{id}/decide` - Approve/reject

### Core 2 (Port 8001)
- `POST /api/v1/vector/search` - Vector similarity search
- `POST /api/v1/graph/traverse` - Neo4j graph traversal
- `POST /api/v1/hybrid/search` - Combined RRF search
- `POST /api/v1/hybrid/reason` - Multi-hop reasoning (used by Core 3)

### Core 1 (Port 8002)
- `POST /api/v1/monitoring/agent-decision` - Track agent decisions
- `POST /api/v1/monitoring/graphrag-query` - Track GraphRAG queries
- `GET /api/v1/compliance/status` - Compliance dashboard
- `GET /api/v1/compliance/violations` - List violations

## Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here  # Optional fallback
NEO4J_PASSWORD=your-neo4j-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
```

## Technology Decisions

- **LangGraph** for multi-agent orchestration (state machines, conditional routing)
- **UV** as package manager (modern, fast replacement for pip/poetry)
- **Ruff** for linting (replaces flake8, isort, black)
- **Pydantic v2** for settings and data validation
- **Neo4j** for knowledge graph (legal relationships)
- **ChromaDB** for vector embeddings (semantic search)
- **Evidently** for ML drift detection
- **Prometheus** for time-series metrics

## Agent Classification Logic

Risk Classifier categorizes systems into:
- **PROHIBITED** (Article 5): Social scoring, subliminal manipulation, emotion detection in workplace/education
- **HIGH-RISK** (Annex III): Biometrics, critical infrastructure, employment, credit scoring
- **LIMITED-RISK** (Article 52): Chatbots, deepfakes (transparency required)
- **MINIMAL-RISK**: No specific obligations

Human review is triggered when:
- Classification = PROHIBITED
- Classification = HIGH_RISK with confidence < 80%
- Conflicting outputs between agents

## Development Workflow

- For changes spanning 4+ files, outline the plan and affected files before implementing
- When fixing bugs, write a failing test that reproduces the issue first, then fix until green
- After implementing a feature, list edge cases and potential failure modes that need test coverage
- Changes to agent logic (risk_classifier, technical_assessor) require updating the golden test cases in `data/golden/test_cases.json`
- Cross-module changes (e.g., modifying Core 2 API that Core 3 calls) require testing both modules together


---


## SOURCE: `docs/archive/REFERENCE_pre_pivot.md`

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


---


## SOURCE: `docs/archive/EU_AI_KB_PROJECT_CONTEXT.md`

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


---


## SOURCE: `docs/archive/KB_construction_plan.md`

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


---


## SOURCE: `docs/archive/gdpr_kg_MEMORY.md`

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


---


## SOURCE: `docs/archive/gdpr_kg_analysis.md`

# GDPR & EU AI Act Knowledge Base: Implementation Analysis

## Executive Summary

The standalone Knowledge Base (KB) for the EU AI Act and GDPR is **COMPLETE (100%)**. 
The project has successfully implemented all 8 phases, including the advanced extraction of concepts and rights which were previously thought missing. The system features a robust hybrid Graph RAG engine, comprehensive test suites, and full vector store integration.

---

## 1. Implementation Status Overview

| Phase | Description | Status | Verification & Metrics |
|-------|-------------|--------|------------------------|
| **Phase 0** | Data Audit | ✅ **COMPLETE** | All 8 data categories validated (88 files). |
| **Phase 1** | Parsing Raw Data | ✅ **COMPLETE** | 99 GDPR Arts, 113 AI Act Arts, 353 Recitals, 13 Annexes, 20 Cases, 21 Guidelines, 15 Enforcement Actions. |
| **Phase 2** | Structural KG | ✅ **COMPLETE** | 2,301 nodes (local validation). 602 CONTAINS, 566 REFERENCES, 236 PART_OF. |
| **Phase 3** | Semantic Extraction | ✅ **COMPLETE** | **Entities:** Definitions (90), Obligations (1,325), Exemptions (96), Actors (18), Risks (4), **Concepts (47)**, **Rights (19)**. |
| **Phase 4** | Neo4j Loading | ✅ **COMPLETE** | **2,235+ nodes**, **4,066+ relationships** loaded into Neo4j. Zero orphans. |
| **Phase 5** | Vector Store | ✅ **COMPLETE** | **7 Collections** (Articles, Recitals, Interpretive, Definitions, Obligations, Concepts, Rights). **2,132+ documents**. |
| **Phase 6** | Query Interface | ✅ **COMPLETE** | Hybrid Graph RAG with RRF (k=60). Reasoning engine with citation validation & confidence scoring. |
| **Phase 7** | Testing & Validation | ✅ **COMPLETE** | **42 Unit Tests** (Passing). **6 Golden Queries** (Passing). 100% Coverage Score. |

---

## 2. Feature Deep Dive & Discrepancy Correction

The initial analysis (based on planned vs. assumed implementation) identified gaps that have **actually been filled**. 

### ✅ Concepts & Rights (Previously thought missing)
-   **Concepts (47):** Extracted across 4 categories (GDPR principles, Processing operations, Compliance concepts, AI concepts).
-   **Rights (19):** Extracted for GDPR (15) and AI Act (4), including "Right to Explainability" and "Right to Erasure".
-   **Files:** `src/extractors/concept_extractor.py`, `src/extractors/right_extractor.py` exist and are operational.

### ✅ Testing & QA
-   **Golden Tests:** `golden_tests/test_queries.json` contains 6 verified test cases covering Prohibited AI, Cross-reg obligations, and Rights.
-   **Unit Tests:** `tests/` directory contains 42 passing tests covering extractors and retrieval logic.
-   **Coverage Report:** `scripts/08_coverage_report.py` confirms 100% score on 5 critical checks (orphans, zero-obligation articles, etc.).

### ✅ Vector Store Granularity
-   **Granularity:** Validated as article/recital level, supplemented by specific entity collections for Concepts, Rights, and Definitions which provide fine-grained semantic targets.
-   **Collections:** Expanded to 7 (`concepts` and `rights` added).

---

## 3. Infrastructure & Architecture

### Design Decisions
*   **Database:** **Neo4j 5.x** + **JSON Vector Store** (7 collections).
*   **Schema:** 17 Entity Types, 13 Relationship Types.
*   **Retrieval:** **Hybrid RRF** (Vector + Graph) + **Reasoning Engine** (LLM Synthesis).
*   **LLM Stack:** Gemini 2.0 Flash (LLM) + `gemini-embedding-001`.

### Metrics (Final)
*   **Nodes:** 2,301 (Local) / 2,235+ (Neo4j)
*   **Relationships:** 4,431 (Local) / 4,066+ (Neo4j)
*   **Avg Relationships/Article:** 19.1 (Excellent density)
*   **Embedding Dimensions:** 3,072

---

## 4. Recommendations / Next Steps (Post-Completion)

Since the standalone KB is effectively complete, the focus shifts to **Integration**:

1.  **Integration with Core 3:**
    *   Map the `ComplianceQueryRequest` and `RiskClassificationRequest` models to Core 3's agent tool definitions.
    *   Deploy the `src/retrieval` module as a library for Core 3.

2.  **Maintenance:**
    *   Monitor `gemini-embedding-001` deprecation timelines.
    *   Consider migrating JSON vector store to a persistent scalable solution (e.g., Qdrant/Weaviate) if dataset grows significantly beyond current 2k docs.

3.  **Expansion:**
    *   Add more "Enforcement Actions" as they happen.
    *   Refine `ReasoningEngine` prompts based on real-world usage feedback.


---


## SOURCE: `docs/archive/compliance_case_studies.txt`

COMPLIANCE CASE STUDIES — GDPR + EU AI Act Knowledge Graph Reasoning Tests
============================================================================
Total: 88 case studies across 18 categories
Purpose: Test knowledge graph reasoning, multi-hop queries, and cross-regulation analysis

================================================================================
CATEGORY 1: PROHIBITED AI PRACTICES (Cases 1-5)
================================================================================

=== CASE STUDY 1 ===
Difficulty: Hard
Category: Prohibited AI Practices
Scenario: A municipal government in Germany develops an AI system that assigns each citizen a "civic reliability score" based on their tax compliance, parking ticket history, library book returns, and social media activity. Citizens with low scores are deprioritised for public housing applications and denied access to certain municipal sports facilities.
Question: Is this system lawful under the EU AI Act and GDPR?

Expected Answer Summary:
- AI Act Art 5(1)(c): PROHIBITED — this is social scoring by a public authority. The system evaluates/classifies natural persons over time based on social behaviour, leading to detrimental treatment in unrelated contexts (housing, sports access based on parking tickets)
- AI Act Art 5(1)(c)(i): The unfavourable treatment occurs in contexts unrelated to where data was collected (library returns affecting housing)
- AI Act Art 5(1)(c)(ii): Treatment is disproportionate to the social behaviour
- GDPR Art 22(1): Automated decisions producing legal effects (housing denial) without human intervention
- GDPR Art 9: Social media analysis likely processes special category data (political opinions, religious beliefs)
- GDPR Art 6: No valid legal basis — legitimate interest cannot override fundamental rights at this scale
- Outcome: System must be immediately discontinued. No conformity assessment possible — it is outright prohibited

Expected Citations:
- EU AI Act Article 5(1)(c), 5(1)(c)(i), 5(1)(c)(ii)
- GDPR Articles 6, 9, 22
- Enforcement precedent: Clearview AI (multiple DPA fines for prohibited biometric practices)

Reasoning Path:
civic_reliability_score → CLASSIFIED_AS → social_scoring → PROHIBITED_BY → AI_Act_Art_5(1)(c)
social_scoring → USES → social_behaviour_data → OVER_TIME → classification
classification → LEADS_TO → detrimental_treatment → IN_CONTEXT → unrelated_to_original
civic_reliability_score → PRODUCES → legal_effects → TRIGGERS → GDPR_Art_22
social_media_analysis → PROCESSES → special_category_data → TRIGGERS → GDPR_Art_9

=== CASE STUDY 2 ===
Difficulty: Medium
Category: Prohibited AI Practices
Scenario: An online gambling platform uses an AI system to detect users who are psychologically vulnerable to addiction (based on behavioural patterns, time-of-day usage, and spending patterns) and then dynamically adjusts bonus offers and game difficulty to maximise their spending.
Question: Does this violate the EU AI Act prohibition on exploiting vulnerabilities?

Expected Answer Summary:
- AI Act Art 5(1)(b): PROHIBITED — the system exploits vulnerabilities of persons due to a specific situation (addiction vulnerability) to materially distort their behaviour in a manner causing significant harm
- The AI identifies the vulnerability and then uses it to increase spending — this is the exact pattern Art 5(1)(b) targets
- The "significant harm" element is met through financial harm and reinforcement of addictive behaviour
- GDPR Art 5(1)(a): Unfair processing — using personal data to exploit identified weaknesses
- GDPR Art 22: Automated decision-making affecting the individual (adjusted game parameters)
- Even if consent was obtained for data processing, consent cannot override a prohibited practice under the AI Act
- Outcome: Prohibited outright. The detection system itself may be lawful (e.g., for protection purposes), but using detection results to exploit rather than protect is prohibited

Expected Citations:
- EU AI Act Article 5(1)(b)
- GDPR Articles 5(1)(a), 22
- EDPB Guidelines on automated decision-making and profiling

Reasoning Path:
gambling_ai → DETECTS → vulnerability_to_addiction → EXPLOITS → specific_social_situation
exploitation → DISTORTS → spending_behaviour → CAUSES → significant_financial_harm
gambling_ai → PROHIBITED_BY → AI_Act_Art_5(1)(b)
dynamic_adjustment → CONSTITUTES → automated_decision → TRIGGERS → GDPR_Art_22

=== CASE STUDY 3 ===
Difficulty: Hard
Category: Prohibited AI Practices
Scenario: A private security company scrapes publicly available images from LinkedIn, Facebook, and Instagram to build a facial recognition database for retail loss prevention. Stores subscribe to the service to identify known shoplifters. The company is based in Israel but sells to EU retailers.
Question: What EU regulations does this system violate?

Expected Answer Summary:
- AI Act Art 5(1)(e): PROHIBITED — creating or expanding facial recognition databases through untargeted scraping of facial images from the internet
- GDPR Art 9: Biometric data (facial templates) is special category data — no valid legal basis for mass scraping
- GDPR Art 6(1): No consent, no contract, no legitimate interest can justify mass scraping for facial recognition
- GDPR Art 3(2): GDPR applies extraterritorially — Israeli company monitoring behaviour of EU individuals
- AI Act Art 2(1): AI Act applies as the system is placed on the EU market (sold to EU retailers)
- Enforcement precedent: Clearview AI — fined EUR 90.5M+ by multiple EU DPAs for identical conduct
- Even the "known shoplifters" framing doesn't help — the DATABASE is built through prohibited scraping
- Outcome: Prohibited under both regulations. EU retailers using this service are also liable

Expected Citations:
- EU AI Act Article 5(1)(e)
- GDPR Articles 3(2), 6(1), 9
- Enforcement: Clearview AI — CNIL EUR 20M, Garante EUR 20M, HDPA EUR 20M, AP EUR 30.5M

Reasoning Path:
facial_recognition_db → BUILT_BY → untargeted_scraping → FROM → internet_images
untargeted_scraping → PROHIBITED_BY → AI_Act_Art_5(1)(e)
facial_templates → CLASSIFIED_AS → biometric_data → SPECIAL_CATEGORY → GDPR_Art_9
israeli_company → SELLS_TO → EU_retailers → TRIGGERS → GDPR_Art_3(2) + AI_Act_Art_2
clearview_ai_enforcement → PRECEDENT_FOR → identical_conduct

=== CASE STUDY 4 ===
Difficulty: Medium
Category: Prohibited AI Practices
Scenario: A workplace productivity tool uses webcam analysis to infer the emotional state of employees during meetings (detecting stress, disengagement, frustration) and generates weekly "engagement reports" for managers.
Question: Is workplace emotion recognition permitted under the EU AI Act?

Expected Answer Summary:
- AI Act Art 5(1)(f): PROHIBITED — emotion recognition AI in the workplace is explicitly banned
- The prohibition covers AI systems that "infer emotions of a natural person in the areas of workplace" regardless of purpose
- Exception: Only permitted for "medical or safety reasons" — engagement reporting does not qualify
- GDPR Art 9: Emotion data derived from biometric processing (facial analysis) is special category data
- GDPR Art 5(1)(c): Data minimisation violated — webcam emotion analysis is excessive for productivity monitoring
- GDPR Art 88: Member State employment data protection provisions may impose additional restrictions
- Enforcement precedent: H&M EUR 35.3M fine for systematic employee surveillance
- Outcome: Prohibited. No conformity assessment, no exemption. Must cease immediately

Expected Citations:
- EU AI Act Article 5(1)(f)
- GDPR Articles 5(1)(c), 9, 88
- Enforcement: H&M (HmbBfDI) — EUR 35.3M for employee surveillance

Reasoning Path:
emotion_recognition → IN_CONTEXT → workplace → PROHIBITED_BY → AI_Act_Art_5(1)(f)
exception_check → medical_or_safety → NOT_APPLICABLE → engagement_reporting
facial_analysis → PRODUCES → biometric_data → TRIGGERS → GDPR_Art_9
employee_monitoring → PRECEDENT → H&M_fine → EUR_35.3M

=== CASE STUDY 5 ===
Difficulty: Easy
Category: Prohibited AI Practices
Scenario: A police department in France wants to deploy real-time facial recognition cameras across the city centre to identify all individuals with outstanding arrest warrants for minor offences (e.g., unpaid fines, traffic violations).
Question: Is this use of real-time biometric identification permitted?

Expected Answer Summary:
- AI Act Art 5(1)(h): Real-time remote biometric identification in public spaces for law enforcement is PROHIBITED as a general rule
- Exceptions in Art 5(1)(h) are narrowly defined: (i) search for abduction/trafficking victims, (ii) imminent threats to life/terrorist attacks, (iii) serious criminal offences (Annex II) with custodial sentence ≥4 years
- Minor offences (unpaid fines, traffic violations) do NOT qualify for any exception
- Art 5(3): Even if an exception applied, prior judicial authorisation is required
- Art 5(2): Each use must be necessary and proportionate — blanket city-wide deployment fails proportionality
- GDPR Art 9: Biometric data processing requires explicit exemption
- Outcome: Prohibited. Minor offences cannot justify real-time biometric identification in public spaces

Expected Citations:
- EU AI Act Article 5(1)(h), 5(1)(h)(iii), 5(2), 5(3)
- EU AI Act Annex II (list of qualifying criminal offences)
- GDPR Article 9

Reasoning Path:
real_time_facial_recognition → IN → public_spaces → FOR → law_enforcement → PROHIBITED_BY → AI_Act_Art_5(1)(h)
exception_check → minor_offences → NOT_IN → Annex_II → EXCEPTION_FAILS
blanket_deployment → FAILS → proportionality_test → Art_5(2)

================================================================================
CATEGORY 2: HIGH-RISK AI (Cases 6-10)
================================================================================

=== CASE STUDY 6 ===
Difficulty: Medium
Category: High-Risk AI
Scenario: A European bank wants to use an AI system to automatically reject loan applications based on credit scoring. The system uses personal financial data and produces legally binding decisions without human review.
Question: What are the combined GDPR and EU AI Act compliance requirements?

Expected Answer Summary:
- GDPR Art 22: Automated decision-making prohibition applies — must provide human intervention
- GDPR Art 35: DPIA required (automated profiling with legal effects)
- GDPR Art 6: Need lawful basis (likely Art 6(1)(b) contract or Art 6(1)(f) legitimate interest)
- AI Act Art 6(2) + Annex III(5)(b): Credit scoring is HIGH-RISK AI — evaluating creditworthiness of natural persons
- AI Act Art 9: Risk management system required throughout entire lifecycle
- AI Act Art 14: Human oversight required for high-risk AI
- AI Act Art 13: Transparency obligations — deployer must understand system outputs
- AI Act Art 26: Deployer obligations — bank must use system in accordance with instructions
- Cumulative: Both GDPR DPIA and AI Act conformity assessment needed

Expected Citations:
- GDPR Articles 6, 22, 35
- EU AI Act Articles 6, 9, 13, 14, 26
- Annex III Category 5(b)

Reasoning Path:
credit_scoring → CLASSIFIED_AS → high_risk → VIA → Annex_III_5(b)
high_risk → REQUIRES → conformity_assessment + risk_management_system
credit_scoring → PRODUCES → legal_effects → TRIGGERS → GDPR_Art_22
GDPR_Art_22 → HAS_EXCEPTION → contract_necessity → HAS_CONDITION → human_intervention
credit_scoring → TRIGGERS → GDPR_Art_35 → REQUIRES → dpia
AI_Act_Art_14 + GDPR_Art_22 → BOTH_REQUIRE → human_oversight

=== CASE STUDY 7 ===
Difficulty: Hard
Category: High-Risk AI
Scenario: A multinational recruitment platform deploys an AI system that screens CVs, ranks candidates, and automatically schedules or rejects candidates for interviews. The system was trained on 10 years of historical hiring data from predominantly male-dominated tech companies.
Question: What compliance requirements apply and what specific risks arise from the training data?

Expected Answer Summary:
- AI Act Annex III(4)(a): HIGH-RISK — AI for recruitment and selection of natural persons, including filtering applications and evaluating candidates
- AI Act Art 10: Data governance requirements — training data must be representative; historical bias from male-dominated companies creates discriminatory outcomes
- AI Act Art 10(2)(f): Must examine data for possible biases that could lead to discrimination
- AI Act Art 10(5): Special provision — to extent necessary for bias monitoring, processing of special categories (gender) is permitted
- AI Act Art 9: Risk management must specifically address bias and discrimination risks
- AI Act Art 14: Human oversight — a human must be able to override automated rejections
- GDPR Art 22: Automated decisions with significant effects on individuals — must offer human intervention
- GDPR Art 9: If the system infers gender, ethnicity, or age from CV data, special category processing may be triggered
- GDPR Art 35: DPIA required — large-scale profiling with significant effects
- Enforcement precedent: Amazon abandoned biased AI recruiting tool (2018) that systematically discriminated against women
- Outcome: Lawful IF all requirements met, but training data bias creates high compliance risk

Expected Citations:
- EU AI Act Articles 6(2), 9, 10, 14, 26
- Annex III Category 4(a)
- GDPR Articles 9, 22, 35
- EDPB Guidelines on profiling and automated decision-making (WP251)

Reasoning Path:
cv_screening → CLASSIFIED_AS → high_risk → VIA → Annex_III_4(a)
training_data → FROM → male_dominated_companies → RISK → gender_bias
AI_Act_Art_10(2)(f) → REQUIRES → bias_examination → OF → training_data
automatic_rejection → TRIGGERS → GDPR_Art_22 → REQUIRES → human_intervention
cv_analysis → MAY_INFER → gender_ethnicity → TRIGGERS → GDPR_Art_9

=== CASE STUDY 8 ===
Difficulty: Medium
Category: High-Risk AI
Scenario: A hospital deploys an AI diagnostic system that analyses MRI scans to detect brain tumours. The system provides a confidence score and recommended diagnosis to radiologists who make the final clinical decision.
Question: What classification does this AI system receive and what requirements apply?

Expected Answer Summary:
- AI Act Art 6(1): This is a SAFETY COMPONENT of a medical device — if the AI is part of or feeds into a device under Regulation (EU) 2017/745 (MDR), it is high-risk under Art 6(1)
- AI Act Annex I(11): Medical devices regulation (EU) 2017/745 is listed as Union harmonisation legislation
- AI Act Annex III(5)(a): Also potentially high-risk as AI evaluating eligibility/access to healthcare services
- AI Act Art 9: Risk management system — must address risks of false negatives (missed tumours) and false positives
- AI Act Art 13: Must be transparent to radiologists about confidence levels and limitations
- AI Act Art 14: Human oversight — radiologist makes final decision (this is good practice, already in place)
- GDPR Art 9(2)(h): Health data processing — permitted for healthcare purposes under Art 9(2)(h) with appropriate safeguards
- GDPR Art 35: DPIA required — large-scale processing of health data
- GDPR Art 25: Data protection by design — MRI data must be pseudonymised where possible
- Outcome: Lawful but requires both medical device conformity assessment AND AI Act high-risk requirements

Expected Citations:
- EU AI Act Articles 6(1), 9, 13, 14
- EU AI Act Annex I(11), Annex III Category 5(a)
- GDPR Articles 9(2)(h), 25, 35
- Regulation (EU) 2017/745 (Medical Devices Regulation)

Reasoning Path:
mri_diagnostic_ai → COMPONENT_OF → medical_device → REGULATED_BY → MDR_2017/745
MDR_2017/745 → LISTED_IN → Annex_I(11) → TRIGGERS → AI_Act_Art_6(1) → high_risk
health_data → SPECIAL_CATEGORY → GDPR_Art_9 → EXCEPTION → Art_9(2)(h)_healthcare
radiologist_oversight → SATISFIES → AI_Act_Art_14 + GDPR_Art_22_exception

=== CASE STUDY 9 ===
Difficulty: Hard
Category: High-Risk AI
Scenario: An EU Member State's border agency deploys an AI-powered lie detector at airport immigration. Travellers from certain visa-requiring countries must answer questions while the system analyses micro-expressions and voice patterns. The system flags "deceptive" travellers for additional screening.
Question: What is the AI Act classification and what fundamental rights issues arise?

Expected Answer Summary:
- AI Act Annex III(7)(a): HIGH-RISK — AI systems used as polygraphs or similar tools in migration/border control
- AI Act Annex III(7)(b): Also high-risk as assessing risk of persons entering the territory
- AI Act Art 5(1)(f): POTENTIALLY PROHIBITED — if the system infers emotions in the area of border control, it may engage the emotion recognition prohibition (though the exception for "safety reasons" could be argued)
- AI Act Art 14: Critical human oversight required — cannot automatically deny entry based solely on AI output
- AI Act Art 5(3): Parallel to biometric identification — no decision producing adverse legal effects based solely on AI output
- AI Act Art 27: Fundamental rights impact assessment required before deployment
- GDPR Art 9: Biometric data (micro-expressions, voice patterns) is special category data
- GDPR Art 22: Flagging for additional screening has significant effects — Art 22 applies
- Discrimination risk: Targeting only visa-requiring country nationals raises Art 21 Charter discrimination concerns
- Outcome: Lawful only with extreme safeguards, fundamental rights impact assessment, and robust human oversight

Expected Citations:
- EU AI Act Articles 5(1)(f), 14, 27
- Annex III Categories 7(a), 7(b)
- GDPR Articles 9, 22
- EU Charter of Fundamental Rights Article 21 (non-discrimination)

Reasoning Path:
ai_lie_detector → AT → border_control → CLASSIFIED_AS → high_risk → VIA → Annex_III_7(a)
micro_expression_analysis → MAY_CONSTITUTE → emotion_recognition → CHECK → Art_5(1)(f)_prohibition
voice_biometrics → CLASSIFIED_AS → special_category_data → TRIGGERS → GDPR_Art_9
country_based_targeting → RAISES → discrimination_risk → UNDER → EU_Charter_Art_21
AI_Act_Art_27 → REQUIRES → fundamental_rights_impact_assessment → BEFORE → deployment

=== CASE STUDY 10 ===
Difficulty: Easy
Category: High-Risk AI
Scenario: A European university uses an AI proctoring system during online exams that monitors students through webcams, detects "suspicious behaviour" (looking away, multiple faces, background noise), and automatically flags potential cheating incidents for review.
Question: What is the AI Act classification of this system?

Expected Answer Summary:
- AI Act Annex III(3)(d): HIGH-RISK — AI systems for monitoring and detecting prohibited behaviour of students during tests in educational institutions
- AI Act Art 9: Risk management system must address false positive risks (legitimate behaviour flagged as cheating)
- AI Act Art 13: Transparency — students must be informed about how the system works and what it monitors
- AI Act Art 14: Human oversight — flagged incidents must be reviewed by humans before any consequence
- AI Act Art 10: Training data must not encode biases (e.g., certain skin tones triggering false positives)
- GDPR Art 6: Legal basis required — likely Art 6(1)(e) public interest task for public universities
- GDPR Art 35: DPIA required — systematic monitoring of individuals in educational context
- GDPR Art 5(1)(f): Webcam monitoring creates integrity/confidentiality obligations
- Outcome: Lawful as high-risk AI with full compliance requirements — NOT prohibited

Expected Citations:
- EU AI Act Articles 6(2), 9, 10, 13, 14
- Annex III Category 3(d)
- GDPR Articles 5(1)(f), 6, 35

Reasoning Path:
exam_proctoring → MONITORS → student_behaviour → DURING → tests → CLASSIFIED_AS → high_risk
high_risk_classification → VIA → Annex_III_3(d) → education_monitoring
webcam_monitoring → REQUIRES → GDPR_Art_35_DPIA + AI_Act_Art_9_risk_management
flagging_system → REQUIRES → human_review → AI_Act_Art_14

================================================================================
CATEGORY 3: AUTOMATED DECISION-MAKING (Cases 11-15)
================================================================================

=== CASE STUDY 11 ===
Difficulty: Medium
Category: Automated Decision-Making
Scenario: An insurance company uses an AI model to automatically set car insurance premiums based on driving behaviour data collected from a telematics device. Drivers with "risky" patterns (late-night driving, sudden braking) pay significantly higher premiums with no option to challenge the AI's assessment.
Question: What GDPR rights does the data subject have regarding this automated pricing?

Expected Answer Summary:
- GDPR Art 22(1): This is automated decision-making producing "significant effects" (financial — higher premiums). The individual has the right NOT to be subject to this without safeguards
- GDPR Art 22(3): Must provide meaningful information about the logic involved, and the right to obtain human intervention, express their point of view, and contest the decision
- GDPR Art 13(2)(f): Right to be informed about the existence of automated decision-making including meaningful information about the logic, significance, and envisaged consequences
- GDPR Art 15(1)(h): Right of access to information about automated decision-making
- GDPR Art 35: DPIA required — systematic profiling with significant financial effects
- AI Act Annex III(5)(c): HIGH-RISK — AI for risk assessment and pricing in relation to natural persons for insurance
- AI Act Art 14: Human oversight mechanism required
- Outcome: Insurer must provide opt-out from fully automated pricing, offer human review on request, and explain the AI logic

Expected Citations:
- GDPR Articles 13(2)(f), 15(1)(h), 22(1), 22(3), 35
- EU AI Act Article 14, Annex III Category 5(c)

Reasoning Path:
telematics_pricing → PRODUCES → significant_financial_effects → TRIGGERS → GDPR_Art_22
GDPR_Art_22(3) → GRANTS → right_to_human_intervention + right_to_contest
insurance_ai_pricing → CLASSIFIED_AS → high_risk → VIA → Annex_III_5(c)
no_challenge_option → VIOLATES → GDPR_Art_22(3)

=== CASE STUDY 12 ===
Difficulty: Hard
Category: Automated Decision-Making
Scenario: A European tax authority uses an AI system to automatically flag tax returns for audit. The system uses income data, profession, postcode, and historical compliance patterns to assign an "audit risk score." Flagged individuals receive automatic audit notification letters. The algorithm is not disclosed due to "tax enforcement confidentiality."
Question: What rights does a flagged taxpayer have to understand and challenge the AI assessment?

Expected Answer Summary:
- GDPR Art 22: Automated decision producing legal effects (audit obligation) — but Art 22(2)(b) allows exception for decisions authorised by Member State law with suitable safeguards
- GDPR Art 22(3): Even under the Art 22(2)(b) exception, data subjects retain rights to obtain human intervention and contest the decision
- GDPR Art 15(1)(h): Right to meaningful information about the logic of automated processing — "enforcement confidentiality" cannot completely override this, though Art 23(1)(e) allows restrictions for important financial interest of public authority
- GDPR Art 23(1)(e): Member State MAY restrict Art 15 rights to protect important financial interest (tax enforcement) — but restrictions must be proportionate
- AI Act Annex III(5)(a): HIGH-RISK — AI used by public authorities to evaluate eligibility for public services/benefits
- AI Act Art 13: Deployer (tax authority) must understand the system's functioning
- AI Act Art 86: Right to explanation — affected persons have right to explanation of individual decision-making by high-risk AI
- CJEU Schrems I principle: Fundamental rights cannot be entirely overridden by public authority interests
- Outcome: Taxpayer has LIMITED but not eliminated rights — must receive some explanation, can request human review

Expected Citations:
- GDPR Articles 15(1)(h), 22, 22(2)(b), 22(3), 23(1)(e)
- EU AI Act Articles 13, 86
- Annex III Category 5(a)

Reasoning Path:
tax_audit_flagging → AUTOMATED_DECISION → legal_effects → TRIGGERS → GDPR_Art_22
public_authority → MAY_RELY_ON → Art_22(2)(b)_exception → REQUIRES → suitable_safeguards
enforcement_confidentiality → RESTRICTS → Art_15 → VIA → Art_23(1)(e) → MUST_BE_PROPORTIONATE
AI_Act_Art_86 → GRANTS → right_to_explanation → FOR → high_risk_AI_decisions

=== CASE STUDY 13 ===
Difficulty: Medium
Category: Automated Decision-Making
Scenario: A social media platform uses an AI content moderation system that automatically removes posts, temporarily suspends accounts, and permanently bans users who violate community guidelines. A user's political commentary is flagged as "hate speech" and their account is suspended for 30 days without detailed explanation.
Question: Does GDPR's automated decision-making protection apply to content moderation?

Expected Answer Summary:
- GDPR Art 22: Debated — account suspension arguably produces "significant effects" on the individual (loss of platform access, speech restrictions). But the CJEU and EDPB have not definitively resolved whether platform moderation constitutes Art 22 automated decision-making
- GDPR Art 22(2)(b): Platform may argue contractual necessity (Terms of Service allow content moderation)
- GDPR Art 13(2)(f), Art 15(1)(h): Regardless of Art 22 applicability, user has right to information about automated processing logic
- AI Act Art 6(3): Content moderation AI may be exempt from high-risk classification if it does not pose "significant risk" to fundamental rights — but Art 6(3) proviso: ANY AI that performs profiling is ALWAYS high-risk
- AI Act Annex III(8)(b): Potentially high-risk if the platform's algorithms could influence democratic processes
- Digital Services Act (DSA): Additional obligations for very large platforms re: content moderation transparency
- Outcome: Grey area under GDPR Art 22, but transparency obligations clearly apply. Need to provide explanation and appeal mechanism

Expected Citations:
- GDPR Articles 13(2)(f), 15(1)(h), 22, 22(2)(b)
- EU AI Act Articles 6(3)
- Annex III Categories 8(b)
- Digital Services Act (complementary regulation)

Reasoning Path:
content_moderation_ai → REMOVES_CONTENT + SUSPENDS_ACCOUNTS → significant_effects?
account_suspension → TRIGGERS → GDPR_Art_22 (debated) → platform_argues → Art_22(2)(b)_contract
content_moderation → PERFORMS → profiling → AI_Act_Art_6(3)_proviso → ALWAYS_high_risk
user_rights → Art_13(2)(f) + Art_15(1)(h) → right_to_information_about_logic

=== CASE STUDY 14 ===
Difficulty: Easy
Category: Automated Decision-Making
Scenario: An online retailer uses an AI system to automatically adjust product prices for individual customers based on their browsing history, purchase history, device type, and location. A customer discovers they are being charged 15% more than other customers for the same product.
Question: What GDPR provisions apply to personalised pricing?

Expected Answer Summary:
- GDPR Art 22(1): Personalised pricing based on profiling that produces "significant financial effects" — Art 22 applies
- GDPR Art 13(2)(f): Must inform customers about the existence of profiling and personalised pricing BEFORE purchase
- GDPR Art 21(1): Right to object to profiling for direct marketing/personalised pricing based on legitimate interest
- GDPR Art 5(1)(a): Fairness principle — covert personalised pricing without disclosure is unfair processing
- GDPR Art 6(1)(a): If consent is relied upon, must be specific and informed (customer must know about dynamic pricing)
- AI Act: Personalised pricing AI for retail is NOT listed in Annex III — likely NOT high-risk (unless profiling proviso applies)
- Enforcement precedent: Amazon EUR 746M fine — ad targeting without valid consent; similar principles apply to price targeting
- Outcome: Not prohibited, but requires transparency, valid legal basis, and right to object

Expected Citations:
- GDPR Articles 5(1)(a), 6(1)(a), 13(2)(f), 21(1), 22(1)
- Enforcement: Amazon/CNPD — EUR 746M for behavioural targeting without consent

Reasoning Path:
personalised_pricing → BASED_ON → profiling → TRIGGERS → GDPR_Art_22
covert_pricing → VIOLATES → GDPR_Art_5(1)(a)_fairness + Art_13(2)(f)_transparency
customer → HAS_RIGHT → Art_21(1)_object_to_profiling
amazon_enforcement → PRECEDENT_FOR → behavioural_targeting_without_consent

=== CASE STUDY 15 ===
Difficulty: Hard
Category: Automated Decision-Making
Scenario: A European public employment service uses an AI system to profile unemployed individuals and automatically assign them to different service tiers: "high employability" (minimal support), "medium" (standard counselling), or "low employability" (intensive intervention). The categorisation affects benefit duration and available training programmes.
Question: What safeguards are required for automated profiling in public employment services?

Expected Answer Summary:
- GDPR Art 22(1): Automated decision with legal effects — benefit duration and service level directly affect the individual
- GDPR Art 22(2)(b): May be authorised by Member State law, but must include suitable safeguards
- GDPR Art 22(4): Must NOT be based on special category data unless Art 9(2)(g) applies (substantial public interest)
- GDPR Art 35: DPIA mandatory — systematic profiling by public authority with significant effects
- AI Act Annex III(5)(a): HIGH-RISK — AI used by public authorities to evaluate eligibility for essential public services/benefits
- AI Act Art 9: Risk management must address risks of incorrect categorisation (e.g., person wrongly assigned "low employability")
- AI Act Art 14: Human oversight — caseworker must be able to override the AI's tier assignment
- AI Act Art 86: Right to explanation of individual AI decisions
- Enforcement precedent: Austrian AMS algorithm controversy (employment profiling algorithm challenged in Austrian courts)
- Outcome: Lawful only with DPIA, conformity assessment, human oversight, explanation, and right to contest

Expected Citations:
- GDPR Articles 22(1), 22(2)(b), 22(4), 35
- EU AI Act Articles 9, 14, 86
- Annex III Category 5(a)

Reasoning Path:
employment_profiling → AUTOMATED_DECISION → affects_benefits → TRIGGERS → GDPR_Art_22
public_authority → RELIES_ON → Art_22(2)(b) → REQUIRES → suitable_safeguards
employment_ai → CLASSIFIED_AS → high_risk → VIA → Annex_III_5(a)
tier_assignment → REQUIRES → human_oversight → AI_Act_Art_14
individual_affected → HAS_RIGHT → AI_Act_Art_86_explanation

================================================================================
CATEGORY 4: DATA SUBJECT RIGHTS (Cases 16-20)
================================================================================

=== CASE STUDY 16 ===
Difficulty: Medium
Category: Data Subject Rights
Scenario: A data subject sends an access request to a social media company asking for all personal data held about them, including: (1) inferences the AI recommendation algorithm has made about their interests, (2) the profile categories the AI has assigned them to, and (3) the logic behind why certain content was shown to them.
Question: To what extent must the company comply with this access request?

Expected Answer Summary:
- GDPR Art 15(1): Right of access covers ALL personal data — including AI-generated inferences and profile categories if they relate to identified/identifiable person
- GDPR Art 15(1)(h): Must provide "meaningful information about the logic involved" in automated decision-making/profiling
- GDPR Art 4(4): Profiling definition — "any form of automated processing of personal data consisting of the use of personal data to evaluate certain personal aspects" — this covers algorithmic categorisation
- CJEU C-434/16 Nowak: Broad interpretation — even subjective assessments about a person constitute personal data
- Inferences: Yes, inferred interests and assigned profile categories ARE personal data (they relate to the individual)
- Logic explanation: Must be "meaningful" but need not disclose full algorithmic details or trade secrets
- GDPR Art 12(5): Response within one month (extendable by two months)
- Enforcement precedent: Spotify EUR 5M fine — access responses must be clear and structured, not just raw data dumps
- Outcome: Must provide (1) inferences, (2) profile categories, (3) meaningful explanation of logic — but not full source code

Expected Citations:
- GDPR Articles 4(4), 12(5), 15(1), 15(1)(h)
- CJEU C-434/16 Nowak (personal data includes subjective assessments)
- Enforcement: Spotify/IMY — EUR 5M for inadequate access responses

Reasoning Path:
access_request → COVERS → personal_data → INCLUDES → AI_inferences + profile_categories
AI_inferences → ABOUT → identified_person → ARE → personal_data → CJEU_Nowak
Art_15(1)(h) → REQUIRES → meaningful_logic_explanation → NOT → full_algorithm_disclosure
spotify_enforcement → REQUIRES → clear_structured_response → NOT → raw_data_dump

=== CASE STUDY 17 ===
Difficulty: Hard
Category: Data Subject Rights
Scenario: An individual requests that a company erase all their personal data under GDPR Article 17 (right to erasure). However, the company's AI model was trained on a dataset that included this person's data. The model has already been deployed in production.
Question: Does the right to erasure extend to retraining the AI model to remove the individual's data influence?

Expected Answer Summary:
- GDPR Art 17(1): Right to erasure applies to personal data in the TRAINING dataset — this must be deleted
- AI model parameters: Highly debated — if the trained model has memorised or can regenerate the individual's data, the model weights may constitute personal data. If the model is fully generalised and cannot reproduce individual data, model weights may not be personal data
- GDPR Art 17(1)(b): If consent was the legal basis for training and consent is withdrawn, data must be erased
- GDPR Art 17(3): Exceptions — scientific research (Art 17(3)(d)) may apply IF erasure would render research impossible, but commercial AI deployment is unlikely to qualify
- Practical implications: May require retraining (computationally expensive) or applying "machine unlearning" techniques
- Enforcement precedent: OpenAI/ChatGPT Italian ban — Garante required mechanism for data subjects to request correction/erasure of AI-generated outputs about them
- EDPB guidance emerging: Trend towards requiring meaningful erasure that affects model behaviour, not just deleting source records
- Outcome: Training data must be deleted. Model retraining may be required if model can reproduce individual data.

Expected Citations:
- GDPR Articles 17(1), 17(1)(b), 17(3)(d)
- Enforcement: OpenAI/Garante — required erasure/correction mechanisms for AI training data
- EDPB Guidelines on processing of personal data through AI systems

Reasoning Path:
erasure_request → TARGETS → training_dataset → MUST_DELETE → source_data
trained_model → CONTAINS → generalised_patterns → QUESTION → are_weights_personal_data?
model_memorisation → IF → can_reproduce_individual_data → THEN → weights_are_personal_data → MUST_RETRAIN
OpenAI_enforcement → PRECEDENT → erasure_extends_to_AI_training

=== CASE STUDY 18 ===
Difficulty: Medium
Category: Data Subject Rights
Scenario: A customer of a digital bank wants to exercise data portability (Art 20) to move to a competing bank. The data includes: (1) transaction history, (2) AI-generated spending categories, (3) AI-predicted creditworthiness score, and (4) the bank's internal fraud risk assessment.
Question: Which data elements fall within the scope of data portability?

Expected Answer Summary:
- GDPR Art 20(1): Right to portability covers data PROVIDED BY the data subject in a structured, commonly used, machine-readable format
- GDPR Art 20(1)(a): Only data processed based on consent or contractual necessity — NOT legitimate interest
- Transaction history: YES — this is "provided by" the data subject through their actions (observed data)
- AI spending categories: DEBATABLE — "inferred" data is generally NOT covered by portability (Art 29 WP guidelines distinguish "provided" from "inferred/derived")
- AI creditworthiness score: NO — this is derived/inferred data, not provided by the data subject
- Fraud risk assessment: NO — this is the controller's own assessment, not data provided by the subject
- GDPR Art 15(1): However, ALL four categories are accessible under the right of access (Art 15) even if not portable
- Outcome: Transaction history is clearly portable. Spending categories arguable. Credit score and fraud assessment are NOT portable but are accessible

Expected Citations:
- GDPR Articles 15(1), 20(1), 20(1)(a)
- Article 29 Working Party Guidelines on Data Portability (WP242)
- EDPB Guidelines on processing of personal data

Reasoning Path:
portability_request → SCOPE → data_provided_by_subject → Art_20(1)
transaction_history → PROVIDED_BY → data_subject → PORTABLE → YES
ai_spending_categories → INFERRED_BY → controller → PORTABLE → DEBATABLE
creditworthiness_score → DERIVED_BY → controller → PORTABLE → NO
fraud_assessment → CREATED_BY → controller → PORTABLE → NO
ALL_data → ACCESSIBLE_UNDER → Art_15 → regardless_of_portability

=== CASE STUDY 19 ===
Difficulty: Easy
Category: Data Subject Rights
Scenario: A person discovers that a health insurance company has used their social media posts to train an AI model that predicts health risks. The person never consented to their social media data being used for health risk prediction.
Question: What rights can the data subject exercise?

Expected Answer Summary:
- GDPR Art 21(1): Right to object to processing based on legitimate interest or public interest — insurer must stop unless compelling legitimate grounds
- GDPR Art 17(1)(c): Right to erasure — if the individual objects and no overriding legitimate grounds exist, data must be deleted
- GDPR Art 9: Health-related inferences from social media constitute special category data — explicit consent required under Art 9(2)(a)
- GDPR Art 6(1): No valid legal basis — social media scraping for insurance purposes unlikely to satisfy any Art 6 ground
- GDPR Art 77: Right to lodge complaint with supervisory authority
- GDPR Art 82: Right to compensation for material or non-material damage
- AI Act Annex III(5)(c): If the AI is used for health insurance pricing, it is HIGH-RISK
- Outcome: Individual can object, demand erasure, file complaint, and seek compensation. Processing is likely unlawful

Expected Citations:
- GDPR Articles 6, 9, 17(1)(c), 21(1), 77, 82
- EU AI Act Annex III Category 5(c)

Reasoning Path:
social_media_data → USED_FOR → health_risk_prediction → WITHOUT_CONSENT
health_inferences → SPECIAL_CATEGORY → GDPR_Art_9 → REQUIRES → explicit_consent
no_consent → UNLAWFUL_PROCESSING → TRIGGERS → Art_17_erasure + Art_21_objection + Art_77_complaint + Art_82_compensation

=== CASE STUDY 20 ===
Difficulty: Medium
Category: Data Subject Rights
Scenario: A job applicant receives an automated rejection email after applying to a company that uses AI-based CV screening. The email says "unfortunately your application was not successful" but provides no information about how the decision was made or that AI was involved.
Question: What information was the applicant entitled to receive and what rights can they now exercise?

Expected Answer Summary:
- GDPR Art 13(2)(f): BEFORE data collection, the company should have informed the applicant about the existence of automated decision-making, meaningful information about the logic, significance, and envisaged consequences
- GDPR Art 14(2)(g): If data was obtained from third parties (e.g., LinkedIn), same obligation applies
- GDPR Art 22(1): Automated decision producing legal effects (rejection from employment) — applicant has right not to be subject to purely automated decisions
- GDPR Art 22(3): Right to obtain human intervention, express their point of view, and contest the decision
- GDPR Art 15(1)(h): Right to request information about the automated decision-making after the fact
- AI Act Annex III(4)(a): CV screening is HIGH-RISK — company had obligation to implement human oversight under Art 14
- AI Act Art 26(8): Deployer must inform individuals that they are subject to high-risk AI
- Outcome: Company violated transparency obligations. Applicant can demand explanation, human review, and may challenge the decision

Expected Citations:
- GDPR Articles 13(2)(f), 14(2)(g), 15(1)(h), 22(1), 22(3)
- EU AI Act Articles 14, 26(8)
- Annex III Category 4(a)

Reasoning Path:
automated_rejection → NO_AI_DISCLOSURE → VIOLATES → Art_13(2)(f) + Art_26(8)
cv_screening → HIGH_RISK → Annex_III_4(a) → REQUIRES → AI_disclosure
applicant → EXERCISES → Art_22(3) → obtain_human_intervention + contest_decision
applicant → EXERCISES → Art_15(1)(h) → request_logic_explanation

================================================================================
CATEGORY 5: INTERNATIONAL TRANSFERS (Cases 21-24)
================================================================================

=== CASE STUDY 21 ===
Difficulty: Hard
Category: International Transfers
Scenario: A European healthcare startup trains its diagnostic AI model using a US cloud provider (AWS/Azure). Patient medical records from German hospitals are uploaded to US servers for model training. The startup relies on Standard Contractual Clauses (SCCs) as the transfer mechanism.
Question: What are the GDPR requirements for this international transfer, and are SCCs sufficient?

Expected Answer Summary:
- GDPR Art 44: Any transfer of personal data to a third country must comply with Chapter V
- GDPR Art 46(2)(c): SCCs can be used as a transfer mechanism, but since Schrems II, supplementary measures are often required
- GDPR Art 9: Health data is special category — heightened protection requirements for transfers
- Transfer Impact Assessment (TIA): Required post-Schrems II to assess whether US law (FISA 702, EO 12333) undermines SCC protections
- EU-US Data Privacy Framework: If the US cloud provider is certified under the DPF, an adequacy decision under Art 45 may apply (since July 2023)
- GDPR Art 35: DPIA required for large-scale health data processing in the cloud
- GDPR Art 28: Data processing agreement with cloud provider required (controller-processor relationship)
- Supplementary measures: Technical measures (encryption where the provider cannot access keys), pseudonymisation before transfer, or keeping data within EU data centres
- Enforcement precedent: Meta EUR 1.2B fine for relying on SCCs without adequate supplementary measures; Uber EUR 290M fine for transfers without valid mechanism
- Outcome: SCCs alone may be insufficient. Must conduct TIA, consider DPF certification, and implement supplementary technical measures

Expected Citations:
- GDPR Articles 9, 28, 35, 44, 46(2)(c)
- CJEU C-311/18 Schrems II
- Enforcement: Meta/DPC — EUR 1.2B; Uber/AP — EUR 290M for transfer violations

Reasoning Path:
health_data → TRANSFERRED_TO → US_cloud → REQUIRES → Chapter_V_compliance
SCCs → POST_SCHREMS_II → REQUIRE → supplementary_measures + TIA
US_cloud_provider → CHECK → DPF_certification → IF_YES → Art_45_adequacy
health_data → SPECIAL_CATEGORY → HEIGHTENED_PROTECTION → DPIA_required
meta_1.2B_enforcement → PRECEDENT → SCCs_alone_insufficient

=== CASE STUDY 22 ===
Difficulty: Medium
Category: International Transfers
Scenario: A French AI company trains a large language model on publicly available European web data. After training, the model is deployed globally — including to users in China, Brazil, and the US. When users interact with the model, their prompts may contain personal data.
Question: Does deploying a globally accessible AI model constitute an international transfer of personal data?

Expected Answer Summary:
- GDPR Art 4(2): "Processing" includes any operation performed on personal data — serving model responses based on user prompts is processing
- GDPR Art 44: Transfer occurs when personal data is transmitted to a third country or international organisation
- Model deployment analysis: If the model is hosted in the EU but accessed from third countries, user prompt data flowing to EU servers is NOT a transfer OUT. But if model inference runs on servers in third countries, personal data IN prompts IS being transferred
- Training data: If the model memorised EU personal data and can reproduce it in third countries, this could constitute a transfer
- GDPR Art 3(2): GDPR applies to the French company regardless of where users are located
- Adequacy decisions: Different for each country — US (DPF), Brazil (no adequacy), China (no adequacy)
- Outcome: Depends on server architecture. EU-hosted model serving global users = minimal transfer risk. Model replicated to non-EU servers = transfers requiring Chapter V compliance

Expected Citations:
- GDPR Articles 3(2), 4(2), 44, 45, 46
- CJEU Schrems II principles

Reasoning Path:
global_model_deployment → WHERE_IS → inference_infrastructure?
EU_hosted_model → users_connect_to_EU → NO_TRANSFER_OUT → minimal_risk
model_replicated_to → US_servers → TRANSFERS → Art_44 → CHECK → DPF_adequacy
model_replicated_to → China_servers → TRANSFERS → Art_44 → NO_ADEQUACY → need_SCCs + supplementary_measures

=== CASE STUDY 23 ===
Difficulty: Hard
Category: International Transfers
Scenario: A US-based AI research lab (not certified under the EU-US Data Privacy Framework) partners with a European university to train a medical AI model. The university sends pseudonymised patient MRI scans to the US lab. The pseudonymisation key is retained by the university in Germany.
Question: Does this transfer still require Chapter V compliance, or does pseudonymisation remove GDPR obligations?

Expected Answer Summary:
- GDPR Recital 26: Pseudonymised data IS still personal data — the data relates to identifiable individuals because the university holds the re-identification key
- GDPR Art 4(5): Pseudonymisation is a security measure, NOT anonymisation — GDPR still applies
- GDPR Art 44: Transfer to US lab requires Chapter V compliance even for pseudonymised data
- However: From the US lab's perspective, if they CANNOT re-identify individuals (no access to the key), the data MAY be "anonymous" to them — but GDPR still considers it personal data because re-identification is possible by the university
- GDPR Art 9: MRI scans are health data — special category even when pseudonymised
- No DPF certification: SCCs required + Transfer Impact Assessment + supplementary measures
- GDPR Art 89(1): Scientific research processing may benefit from derogations but NOT from Chapter V transfer requirements
- Best practice: Consider federated learning (model travels to data, not data to model) or synthetic data to avoid transfers entirely
- Outcome: Chapter V compliance IS required. Pseudonymisation reduces risk but does not eliminate GDPR applicability

Expected Citations:
- GDPR Articles 4(5), 9, 44, 46, 89(1)
- GDPR Recital 26 (pseudonymisation vs anonymisation)
- Enforcement: Meta/DPC EUR 1.2B (transfer mechanism inadequacy)

Reasoning Path:
pseudonymised_MRI → STILL → personal_data → PER → Recital_26 + Art_4(5)
university → HOLDS → re_identification_key → THEREFORE → identifiable
transfer_to_US → REQUIRES → Chapter_V → Art_44
no_DPF_certification → REQUIRES → SCCs + TIA + supplementary_measures
research_exception → Art_89(1) → DOES_NOT → exempt_from_Chapter_V
alternative → federated_learning → AVOIDS → transfer_entirely

=== CASE STUDY 24 ===
Difficulty: Medium
Category: International Transfers
Scenario: An EU company uses an Indian outsourcing firm for data annotation (labelling images for AI training). The images contain faces of EU citizens. The annotation is done on the Indian firm's local servers. After annotation, the labelled dataset is returned to the EU.
Question: What transfer safeguards are required for the data annotation arrangement?

Expected Answer Summary:
- GDPR Art 44: Transfer of facial images to India constitutes an international data transfer — India has no adequacy decision
- GDPR Art 46(2)(c): SCCs required between EU company (controller) and Indian firm (processor)
- GDPR Art 28: Data processing agreement required specifying subject matter, duration, nature, purpose
- GDPR Art 9: Facial images enabling identification are biometric data — special category processing
- Transfer Impact Assessment: Required to assess Indian law's compatibility with GDPR protections
- GDPR Art 32: Indian firm must implement appropriate security measures
- AI Act relevance: If the training data is for a high-risk AI system, data governance requirements under Art 10 extend to annotation quality
- Practical: Consider on-site annotation (Indian annotators work on EU-hosted platform via remote desktop) to avoid actual data transfer
- Outcome: Lawful with SCCs + DPA + TIA + security measures. Remote annotation on EU servers is a better alternative

Expected Citations:
- GDPR Articles 9, 28, 32, 44, 46(2)(c)
- EU AI Act Article 10 (data governance for high-risk AI)

Reasoning Path:
facial_images → TRANSFERRED_TO → India → NO_ADEQUACY → requires_safeguards
EU_company → CONTROLLER → Indian_firm → PROCESSOR → requires → Art_28_DPA + Art_46_SCCs
facial_images → BIOMETRIC_DATA → Art_9 → heightened_protection
alternative → remote_annotation_on_EU_servers → AVOIDS → physical_transfer

================================================================================
CATEGORY 6: SPECIAL CATEGORY DATA (Cases 25-29)
================================================================================

=== CASE STUDY 25 ===
Difficulty: Medium
Category: Special Category Data
Scenario: A pharmaceutical company wants to use an AI system to identify patients suitable for a clinical trial. The system analyses electronic health records from multiple hospitals, including diagnoses, medications, genetic markers, and treatment outcomes.
Question: What legal basis can justify processing this health and genetic data for AI-driven patient selection?

Expected Answer Summary:
- GDPR Art 9(1): Health data AND genetic data — both explicitly listed as special categories. Processing is prohibited UNLESS an exception in Art 9(2) applies
- GDPR Art 9(2)(a): Explicit consent — possible but problematic at scale (need consent before screening records)
- GDPR Art 9(2)(h): Processing necessary for healthcare purposes — may apply if done by health professionals bound by confidentiality
- GDPR Art 9(2)(i): Public health interest — clinical trial identification may qualify under Member State law
- GDPR Art 9(2)(j): Scientific research purposes — subject to Art 89(1) safeguards (pseudonymisation, data minimisation)
- GDPR Art 35: DPIA mandatory — large-scale processing of health and genetic data
- GDPR Art 36: Prior consultation with DPA may be required if DPIA indicates high residual risk
- AI Act Annex III(5)(a): If used to evaluate eligibility for healthcare, HIGH-RISK classification
- GDPR Art 5(1)(c): Data minimisation — only screen data fields relevant to trial criteria
- Outcome: Lawful under Art 9(2)(j) scientific research + Art 89(1) safeguards, OR Art 9(2)(h) with health professional involvement. DPIA mandatory.

Expected Citations:
- GDPR Articles 5(1)(c), 9(1), 9(2)(a)(h)(i)(j), 35, 36, 89(1)
- EU AI Act Annex III Category 5(a)

Reasoning Path:
health_records + genetic_data → SPECIAL_CATEGORY → Art_9(1) → PROHIBITED_UNLESS_EXCEPTION
clinical_trial_selection → POSSIBLE_BASIS → Art_9(2)(j)_research + Art_89(1)_safeguards
pharmaceutical_company → CHECK → Art_9(2)(h) → REQUIRES → health_professional_supervision
large_scale_health_processing → MANDATORY → DPIA → Art_35

=== CASE STUDY 26 ===
Difficulty: Hard
Category: Special Category Data
Scenario: A fintech startup develops an AI system that analyses users' voice patterns during phone interactions to detect stress levels and uses this as one factor in assessing creditworthiness. The system claims voice analysis reveals financial stress more accurately than traditional credit scoring.
Question: What special category data issues arise from voice-based stress detection for credit decisions?

Expected Answer Summary:
- GDPR Art 9(1): Voice patterns for stress detection may constitute biometric data if used for identification purposes, AND constitute health-related data if inferring mental/emotional state
- GDPR Art 9: Even if not "biometric identification," inferring health/emotional state from voice processing is processing data CONCERNING health — special category
- AI Act Art 5(1)(f): Emotion recognition — if this infers emotions, it may engage the workplace prohibition. For financial services, not explicitly prohibited but raises Art 9 + fairness concerns
- AI Act Annex III(5)(b): Credit scoring is HIGH-RISK — voice-based stress assessment combined with credit scoring doubles the regulatory burden
- GDPR Art 22: Automated credit decision with significant effects — Art 22 applies
- GDPR Art 22(4): Decision must NOT be based on special category data unless Art 9(2)(a) explicit consent or Art 9(2)(g) substantial public interest applies
- GDPR Art 5(1)(c): Data minimisation — voice stress analysis for creditworthiness is arguably excessive
- Outcome: Almost certainly unlawful — combining voice-based emotion/health inference with automated credit decisions violates Art 22(4) read with Art 9

Expected Citations:
- GDPR Articles 5(1)(c), 9(1), 22, 22(4)
- EU AI Act Articles 5(1)(f), 6(2)
- Annex III Categories 1(c), 5(b)

Reasoning Path:
voice_stress_detection → INFERS → emotional_state → CONSTITUTES → health_data → Art_9
voice_patterns → MAY_BE → biometric_data → Art_9
credit_scoring + voice_analysis → AUTOMATED_DECISION → Art_22 → WITH → special_category_input
Art_22(4) → PROHIBITS → automated_decisions_based_on → special_category_data
result → LIKELY_UNLAWFUL → unless_explicit_consent_Art_9(2)(a)

=== CASE STUDY 27 ===
Difficulty: Medium
Category: Special Category Data
Scenario: A political party uses an AI system to analyse voters' social media posts, "likes," and shared content to infer their political opinions. The system then creates targeted political advertisements tailored to individual voters' inferred political leanings.
Question: What GDPR and AI Act provisions does this political micro-targeting engage?

Expected Answer Summary:
- GDPR Art 9(1): Political opinions are EXPLICITLY listed as special category data. Inferring political views from social media constitutes processing special category data
- GDPR Art 9(2)(a): Explicit consent required — not obtained through social media scraping
- GDPR Art 9(2)(d): Data "manifestly made public" exception — limited: a public "like" may not constitute manifestly making one's political opinion public
- GDPR Art 9(2)(e): Does NOT apply — political parties cannot claim this exception for marketing
- GDPR Art 21(2): Absolute right to object to processing for direct marketing — political advertising qualifies
- AI Act Annex III(8)(b): HIGH-RISK — AI systems intended to influence voting behaviour in elections
- AI Act Art 5(1)(a): If the targeting uses subliminal or manipulative techniques to distort voting behaviour, it may be PROHIBITED
- Enforcement precedent: Cambridge Analytica scandal — led to ICO and FTC enforcement actions
- Outcome: Unlawful without explicit consent. High-risk AI classification applies. Potentially prohibited if manipulative.

Expected Citations:
- GDPR Articles 9(1), 9(2)(a)(d), 21(2)
- EU AI Act Articles 5(1)(a), Annex III Category 8(b)

Reasoning Path:
social_media_analysis → INFERS → political_opinions → SPECIAL_CATEGORY → Art_9
no_explicit_consent → UNLAWFUL → Art_9(2)(a)_not_met
political_ads → DIRECT_MARKETING → Art_21(2) → absolute_right_to_object
influence_voting → Annex_III_8(b) → HIGH_RISK + potentially → Art_5(1)(a) → PROHIBITED

=== CASE STUDY 28 ===
Difficulty: Easy
Category: Special Category Data
Scenario: A fitness app uses AI to track users' exercise patterns, heart rate, sleep quality, and nutrition intake to provide personalised health recommendations. The app shares aggregated (but not fully anonymised) health data with insurance partners who offer premium discounts.
Question: What GDPR requirements apply to sharing health data from a fitness app with insurance companies?

Expected Answer Summary:
- GDPR Art 9(1): Heart rate, sleep data, and health recommendations = health data (special category)
- GDPR Art 9(2)(a): Need explicit consent for health data processing — generic app terms are insufficient
- "Aggregated but not anonymised": If individuals can be re-identified, data is still personal data (Recital 26)
- GDPR Art 6(1)(a) + Art 9(2)(a): Consent must be specific, informed, and separate for the insurance sharing purpose — cannot be bundled with app functionality
- GDPR Art 7(4): Consent must be freely given — cannot condition app access on allowing insurance data sharing
- GDPR Art 5(1)(b): Purpose limitation — users consented to health recommendations, not insurance data sharing
- AI Act Annex III(5)(c): If insurance companies use this data for AI-driven pricing, it is HIGH-RISK
- Outcome: Requires separate, explicit, freely given consent specifically for insurance sharing. Aggregation without full anonymisation is insufficient protection.

Expected Citations:
- GDPR Articles 5(1)(b), 6(1)(a), 7(4), 9(1), 9(2)(a)
- GDPR Recital 26 (identifiability)
- EU AI Act Annex III Category 5(c)

Reasoning Path:
fitness_data → INCLUDES → heart_rate + sleep → HEALTH_DATA → Art_9
sharing_with_insurers → NEW_PURPOSE → REQUIRES → separate_explicit_consent
aggregated_not_anonymised → STILL → personal_data → Recital_26
consent_bundling → VIOLATES → Art_7(4) → freely_given_requirement

=== CASE STUDY 29 ===
Difficulty: Hard
Category: Special Category Data
Scenario: An AI-powered hiring platform analyses video interviews and assesses candidates' facial expressions, tone of voice, and word choice. The system claims to detect personality traits, cultural fit, and leadership potential. A candidate who wears a religious headscovering receives consistently lower "cultural fit" scores.
Question: What GDPR and AI Act issues arise from this AI video interview analysis?

Expected Answer Summary:
- GDPR Art 9(1): Religious headcovering → the system may be inferring religious beliefs (special category data)
- GDPR Art 9: Biometric data (facial analysis) is special category — and it is being used to make employment decisions
- GDPR Art 22(4): Automated hiring decision must NOT be based on special category data without explicit consent
- AI Act Annex III(4)(a): HIGH-RISK — AI for recruitment and evaluation of candidates
- AI Act Art 10(2)(f): Training data must be examined for biases — if the model was trained predominantly on candidates without religious headcoverings, it has encoded discriminatory bias
- AI Act Art 5(1)(g): If the system categorises individuals based on biometric data to infer religious beliefs, this is PROHIBITED
- AI Act Art 5(1)(f): Emotion recognition in workplace context — PROHIBITED if inferring emotions from facial expressions
- EU Employment Equality Directive: Discrimination based on religion is illegal under EU law
- Enforcement precedent: H&M EUR 35.3M for employee data profiling
- Outcome: Multiple violations — prohibited emotion recognition, prohibited biometric categorisation for religion, unlawful special category processing, discriminatory bias

Expected Citations:
- GDPR Articles 9(1), 22(4)
- EU AI Act Articles 5(1)(f), 5(1)(g), 10(2)(f)
- Annex III Category 4(a)
- Enforcement: H&M EUR 35.3M

Reasoning Path:
video_interview_ai → ANALYSES → facial_expressions → emotion_recognition → PROHIBITED → Art_5(1)(f)_workplace
headcovering_bias → INFERS → religious_beliefs → Art_5(1)(g) → PROHIBITED_biometric_categorisation
training_data_bias → VIOLATES → Art_10(2)(f) → discrimination_by_design
hiring_decision → BASED_ON → special_category → VIOLATES → Art_22(4)

================================================================================
CATEGORY 7: SCOPE QUESTIONS (Cases 30-33)
================================================================================

=== CASE STUDY 30 ===
Difficulty: Easy
Category: Scope Questions
Scenario: A hobbyist in Belgium builds a personal AI chatbot that uses a locally hosted LLM to help manage their family calendar, draft personal emails, and keep track of household expenses. The system runs entirely on their home computer and is not connected to the internet. The household data includes family members' names, schedules, and spending.
Question: Does the GDPR or EU AI Act apply to this purely personal AI system?

Expected Answer Summary:
- GDPR Art 2(2)(c): GDPR does NOT apply to processing by a natural person in the course of a "purely personal or household activity"
- GDPR Recital 18: Personal correspondence and address keeping are explicitly cited as household activities — calendar/email/expenses management qualifies
- Condition: No disclosure to an indefinite number of persons (no internet connection = no public exposure)
- AI Act Art 2(10): The AI Act does NOT apply to AI systems used exclusively for "personal non-professional activity" by natural persons
- AI Act Recital 25: Confirms exclusion of AI research and development activities and purely personal/household use
- HOWEVER: If the hobbyist processes OTHER people's data (e.g., contacts' information) and shares it externally, the household exemption narrows
- Outcome: Neither GDPR nor AI Act applies — purely personal/household use on local hardware with no external sharing

Expected Citations:
- GDPR Article 2(2)(c), Recital 18
- EU AI Act Article 2(10), Recital 25

Reasoning Path:
personal_ai_chatbot → local_only → no_internet → purely_household
household_activity → EXEMPT_FROM → GDPR → Art_2(2)(c) + Recital_18
personal_non_professional → EXEMPT_FROM → AI_Act → Art_2(10) + Recital_25
condition → no_external_disclosure → exemption_holds

=== CASE STUDY 31 ===
Difficulty: Medium
Category: Scope Questions
Scenario: A European defence ministry develops an AI system for autonomous military drone target identification. The system is designed exclusively for military operations. However, the same ministry also considers using a modified version for civilian border surveillance.
Question: Which version(s) of this AI system fall under the EU AI Act?

Expected Answer Summary:
- AI Act Art 2(3): The AI Act does NOT apply to AI systems developed or used exclusively for military purposes
- Military drone AI: EXEMPT — if developed and used exclusively for military operations, the AI Act does not apply
- Civilian border surveillance version: FULLY SUBJECT to the AI Act — once adapted for civilian use, the military exemption evaporates
- AI Act Annex III(7): Border surveillance AI is HIGH-RISK — AI for migration/border control management
- AI Act Art 2(3) is narrow: "Exclusively" for military means any dual-use triggers full AI Act compliance
- GDPR: Military processing may be exempt under Art 2(2)(a) (national security) for the military version, but civilian border use triggers GDPR fully
- Key insight: The "same technology" distinction — the underlying model may be the same, but the APPLICATION determines regulatory scope
- Outcome: Military version exempt. Civilian border version = high-risk AI under AI Act + full GDPR obligations

Expected Citations:
- EU AI Act Articles 2(3), 6(2)
- Annex III Category 7(b), 7(d)
- GDPR Article 2(2)(a)

Reasoning Path:
military_drone_ai → EXCLUSIVELY_MILITARY → EXEMPT → AI_Act_Art_2(3)
civilian_border_version → NOT_EXCLUSIVELY_MILITARY → SUBJECT_TO → AI_Act
border_surveillance → HIGH_RISK → Annex_III_7(b)(d)
dual_use_key → application_determines_scope → NOT → underlying_technology

=== CASE STUDY 32 ===
Difficulty: Hard
Category: Scope Questions
Scenario: A US-based AI company (with no EU establishment) develops a general-purpose AI model and makes it available as an open-source download. A European company downloads the model, fine-tunes it on EU personal data for a high-risk healthcare application, and deploys it in German hospitals.
Question: Who bears responsibility under the GDPR and AI Act — the US AI company, the European company, or both?

Expected Answer Summary:
- AI Act — US company: As provider of a general-purpose AI model (GPAI), obligations under Art 53 apply (transparency, documentation, copyright policy). If the model is "open source" under Art 53(2), reduced obligations may apply
- AI Act — European company: By fine-tuning the GPAI model for a HIGH-RISK use, they become the PROVIDER of the high-risk AI system under Art 25 (treating downstream deployers as providers when they substantially modify the system)
- AI Act Art 25(1)(c): An operator becomes a provider when they make a "substantial modification" to a high-risk AI system
- GDPR — US company: If the model was NOT trained on EU personal data and has no EU processing, GDPR may not apply to the US company
- GDPR — European company: Fully responsible as DATA CONTROLLER for fine-tuning on EU health data and deployment
- GDPR Art 9: Health data processing for the fine-tuned model — special category obligations
- GDPR Art 26: If US and EU companies jointly determine purposes/means, JOINT CONTROLLER arrangement may arise
- Outcome: US company has GPAI model obligations. European company bears FULL high-risk AI provider + GDPR controller obligations. Possible joint controller status.

Expected Citations:
- EU AI Act Articles 25(1)(c), 53, 53(2)
- GDPR Articles 4(7), 9, 26
- AI Act Chapter V (GPAI model obligations)

Reasoning Path:
US_company → provides → GPAI_model → obligations → AI_Act_Art_53
open_source_model → reduced_obligations → Art_53(2) → BUT → transparency_still_required
EU_company → fine_tunes → for_high_risk → BECOMES → provider → Art_25(1)(c)
EU_company → processes → EU_health_data → DATA_CONTROLLER → GDPR_Art_4(7)
GDPR_does_not_reach → US_company_IF → no_EU_data_processing

=== CASE STUDY 33 ===
Difficulty: Medium
Category: Scope Questions
Scenario: A European university's computer science department uses personal data (student records, examination results) as part of an AI research project studying algorithmic fairness. The research is purely academic with no commercial intent. Researchers claim GDPR does not apply because it is "scientific research."
Question: Does the GDPR research exemption eliminate all data protection obligations?

Expected Answer Summary:
- GDPR Art 89(1): Scientific research processing is NOT exempt from GDPR. Art 89 provides for DEROGATIONS (reduced obligations) but not a blanket exemption
- GDPR Art 89(2): Member States MAY provide derogations from Arts 15, 16, 18, 21 (access, rectification, restriction, objection) for research — but only IF safeguards in Art 89(1) are met
- GDPR Art 89(1) safeguards: Technical and organisational measures, particularly pseudonymisation, must be implemented
- GDPR Art 5(1)(b): Purpose limitation has a research exception — further processing for scientific research is "not incompatible" with original purpose
- GDPR Art 5(1)(e): Storage limitation — data can be kept longer for research IF Art 89(1) safeguards apply
- STILL REQUIRED: Legal basis (Art 6), DPIA if high-risk (Art 35), security measures (Art 32), data protection principles (Art 5)
- Student data: Processing examination data for unrelated AI research is a NEW purpose — needs its own legal basis
- Outcome: Research is NOT exempt. Reduced rights obligations possible under Art 89(2), but core GDPR principles, legal basis, and security requirements fully apply.

Expected Citations:
- GDPR Articles 5(1)(b), 5(1)(e), 6, 32, 35, 89(1), 89(2)

Reasoning Path:
scientific_research → NOT → exempt_from_GDPR
Art_89 → provides → DEROGATIONS → NOT → blanket_exemption
Art_89(1) → REQUIRES → safeguards → especially → pseudonymisation
core_obligations → Art_5 + Art_6 + Art_32 + Art_35 → STILL_APPLY
student_data_for_AI_research → NEW_PURPOSE → needs_own_legal_basis

================================================================================
CATEGORY 8: CROSS-REGULATION OVERLAP (Cases 34-38)
================================================================================

=== CASE STUDY 34 ===
Difficulty: Hard
Category: Cross-Regulation Overlap
Scenario: A European smart city project deploys an integrated AI system that: (1) monitors traffic via cameras with license plate recognition, (2) tracks pedestrian flow using anonymised Wi-Fi probe requests, (3) optimises traffic lights using real-time data, and (4) shares traffic pattern data with a US cloud analytics platform.
Question: Map the full regulatory obligations across GDPR and the EU AI Act for each component.

Expected Answer Summary:
Component 1 — License plate recognition:
- GDPR Art 6(1)(e): Public interest legal basis
- GDPR Art 35: DPIA required — systematic monitoring of public space
- AI Act: NOT explicitly in Annex III for traffic, BUT Art 6(1) — if embedded in critical infrastructure (road traffic), HIGH-RISK under Annex III(2)

Component 2 — Wi-Fi tracking:
- GDPR: IF truly anonymised (cannot re-identify), GDPR does not apply (Recital 26)
- HOWEVER: Wi-Fi MAC addresses are personal data; "anonymised" probe requests may still be identifiable through correlation
- ePrivacy Directive Art 5(3): Accessing device information (Wi-Fi probes) requires consent

Component 3 — Traffic light optimisation:
- AI Act Annex III(2): HIGH-RISK — AI as safety component in management/operation of road traffic
- AI Act Art 9: Risk management system required — malfunctioning traffic AI creates physical safety risks
- AI Act Art 14: Human oversight — operators must be able to override AI traffic decisions

Component 4 — US cloud sharing:
- GDPR Art 44: International transfer requires Chapter V compliance
- Check US provider DPF certification
- GDPR Art 28: Data processing agreement required
- DPIA must assess transfer risks

Cumulative: Multiple overlapping high-risk classifications, DPIA covering all components, transfer safeguards, and AI Act conformity assessment for components 1 and 3.

Expected Citations:
- GDPR Articles 6(1)(e), 28, 35, 44
- EU AI Act Articles 6(1), 9, 14
- Annex III Category 2 (critical infrastructure — road traffic)
- ePrivacy Directive Article 5(3)

Reasoning Path:
smart_city → FOUR_COMPONENTS → each_assessed_separately
license_plate → personal_data → DPIA → Art_35
wifi_tracking → anonymisation_CHECK → IF_identifiable → GDPR_applies
traffic_optimisation → safety_component → road_traffic → Annex_III_2 → HIGH_RISK
US_cloud → international_transfer → Art_44 → Chapter_V
cumulative → overlapping_requirements → DPIA + conformity_assessment + transfer_safeguards

=== CASE STUDY 35 ===
Difficulty: Hard
Category: Cross-Regulation Overlap
Scenario: A European e-commerce company deploys a generative AI customer service chatbot that: (1) processes customer purchase history and personal details to provide personalised responses, (2) can access and modify customer accounts (address changes, returns), (3) logs all conversations for quality training, and (4) is powered by a US-hosted large language model via API.
Question: What are the combined GDPR and AI Act obligations for this chatbot deployment?

Expected Answer Summary:
GDPR obligations:
- Art 6(1)(b): Contractual necessity for processing order/account data in customer service
- Art 13: Transparency — must inform customers they are interacting with AI, not human
- Art 22: If the chatbot makes decisions (processing returns, account changes) without human review, Art 22 applies
- Art 5(1)(b): Purpose limitation — using conversations for training is a DIFFERENT purpose requiring separate basis
- Art 5(1)(e): Conversation logs — retention must be limited and justified
- Art 44: API calls to US-hosted LLM = international data transfer. Customer personal data in prompts sent to US servers
- Art 28: Data processing agreement with LLM provider required
- Art 35: DPIA recommended — large-scale automated processing with account modification capabilities

AI Act obligations:
- AI Act Art 50(1): Transparency — users must be informed they are interacting with an AI system (deployer obligation)
- AI Act Art 53: If powered by a GPAI model, the model provider has transparency and documentation obligations
- AI Act classification: Customer service chatbot is likely NOT high-risk (not in Annex III) unless it makes autonomous decisions with significant effects

Cross-regulation:
- Both GDPR Art 13/22 and AI Act Art 50 require informing users about AI
- GDPR transfer rules AND AI Act GPAI obligations apply simultaneously to the US LLM provider
- Training on conversation data requires BOTH GDPR legal basis AND AI Act data governance compliance
- Outcome: Moderate complexity — GDPR fully applies, AI Act transparency applies, transfer safeguards essential for US API

Expected Citations:
- GDPR Articles 5(1)(b)(e), 6(1)(b), 13, 22, 28, 35, 44
- EU AI Act Articles 50(1), 53

Reasoning Path:
chatbot → PROCESSES → personal_data → GDPR_Art_6(1)(b)
chatbot → IS_AI → must_disclose → GDPR_Art_13 + AI_Act_Art_50(1)
account_modifications → autonomous? → IF_YES → GDPR_Art_22
conversation_logs → training_purpose → NEW_PURPOSE → Art_5(1)(b)
API_to_US → personal_data_in_prompts → transfer → Art_44

=== CASE STUDY 36 ===
Difficulty: Medium
Category: Cross-Regulation Overlap
Scenario: A hospital group develops an AI triage system for emergency departments that analyses patient symptoms, vital signs, and medical history to assign urgency levels (1-5). Patients with higher urgency scores are seen first. A patient assigned a low urgency score suffers a cardiac event while waiting.
Question: What are the overlapping GDPR and AI Act obligations, and what liability framework applies to the AI's incorrect triage?

Expected Answer Summary:
AI Act classification:
- Annex III(5)(d): HIGH-RISK — AI for emergency healthcare patient triage
- Art 9: Risk management must specifically address false-low-urgency risk (the exact scenario that occurred)
- Art 14: Human oversight by triage nurses — AI should SUPPORT, not replace, clinical judgment
- Art 15: Accuracy requirements — must demonstrate acceptable false negative rate for critical conditions
- Art 13: Transparency — clinicians must understand the system's limitations

GDPR obligations:
- Art 9(2)(h): Health data processing — permitted for healthcare with health professional handling
- Art 22: Triage assignment affects medical care timing — significant effect on the individual
- Art 35: DPIA required — high-risk health data processing
- Art 5(1)(d): Accuracy principle — inaccurate risk assessment has direct health consequences

Liability:
- AI Act Art 79: Post-market monitoring — system failures must be reported and addressed
- Product Liability Directive (revised 2024): AI systems included — manufacturer/provider liable for defective AI
- GDPR Art 82: Compensation for damage resulting from GDPR violation
- Medical negligence: Hospital has duty of care regardless of AI system — human override failure is separate liability ground
- Outcome: Multiple liability sources — AI Act provider obligations, GDPR controller liability, product liability, and medical negligence

Expected Citations:
- GDPR Articles 5(1)(d), 9(2)(h), 22, 35, 82
- EU AI Act Articles 9, 13, 14, 15, 79
- Annex III Category 5(d)
- Product Liability Directive

Reasoning Path:
triage_ai → Annex_III_5(d) → HIGH_RISK → full_compliance_required
incorrect_triage → Art_9_risk_management → SHOULD_HAVE_ADDRESSED → false_low_urgency
human_oversight → Art_14 → triage_nurse → should_override → but_did_they?
patient_harm → LIABILITY → AI_Act_provider + GDPR_Art_82 + Product_Liability + medical_negligence

=== CASE STUDY 37 ===
Difficulty: Medium
Category: Cross-Regulation Overlap
Scenario: A European retail bank deploys an AI system to detect potentially fraudulent transactions in real-time. The system automatically blocks suspicious transactions and sends alerts to customers. It processes transaction amounts, locations, merchant categories, device information, and behavioural patterns.
Question: How do GDPR's automated decision-making rules interact with the AI Act's requirements for this fraud detection system?

Expected Answer Summary:
GDPR analysis:
- Art 22(2)(b): Automated blocking IS automated decision-making with significant effects — but Art 22(2)(b) allows it when authorised by EU/Member State law (PSD2 / anti-fraud regulation)
- Art 22(2)(a): Also allowed when necessary for contract performance (protecting customer's account)
- Art 22(3): Even under exceptions, must provide right to obtain human intervention and contest blocked transactions
- Art 6(1)(f): Legitimate interest is valid basis for fraud detection
- Art 35: DPIA required — systematic profiling with financial effects
- Art 13(2)(f): Must inform customers about automated fraud monitoring at account opening

AI Act analysis:
- Annex III(5)(b): Credit scoring is high-risk, but fraud detection is EXCLUDED from high-risk classification ("with the exception of AI systems used for the purpose of detecting financial fraud")
- This is a critical distinction — fraud detection AI gets a carve-out from high-risk requirements
- However, AI Act general provisions on transparency (Art 50) still apply

Cross-regulation interaction:
- GDPR provides STRONGER protection than AI Act for this use case (Art 22 safeguards apply even though AI Act classifies it as non-high-risk)
- This demonstrates that GDPR and AI Act protections are CUMULATIVE — the higher standard applies
- Outcome: AI Act = lighter touch (non-high-risk). GDPR = full automated decision-making safeguards. GDPR prevails here.

Expected Citations:
- GDPR Articles 6(1)(f), 13(2)(f), 22(2)(a)(b), 22(3), 35
- EU AI Act Annex III Category 5(b) (fraud detection exception)
- AI Act Article 50

Reasoning Path:
fraud_detection_ai → CHECK → Annex_III_5(b) → EXCEPTION → "detecting financial fraud" → NOT_high_risk
BUT → GDPR_Art_22 → STILL_APPLIES → automated_blocking = significant_effect
Art_22(2)(a)(b) → exceptions_available → contract_performance + law_authorisation
GDPR_prevails → stronger_protection → cumulative_application

=== CASE STUDY 38 ===
Difficulty: Hard
Category: Cross-Regulation Overlap
Scenario: A large European company deploys a comprehensive AI-driven HR system that: (1) screens CVs and ranks candidates during recruitment, (2) monitors employee productivity through keyboard/mouse activity tracking, (3) uses sentiment analysis on internal communications to predict attrition risk, and (4) generates automated performance review summaries that influence promotion decisions.
Question: Provide a complete compliance map covering all GDPR and AI Act requirements for each component.

Expected Answer Summary:
Component 1 — CV screening:
- AI Act Annex III(4)(a): HIGH-RISK — AI for recruitment and candidate evaluation
- AI Act requirements: Art 9 (risk management), Art 10 (data governance — bias audit), Art 13 (transparency to HR), Art 14 (human oversight), Art 26 (deployer obligations)
- GDPR Art 22: Automated decision producing significant effects — need human intervention option
- GDPR Art 13(2)(f): Must inform candidates about AI involvement
- GDPR Art 35: DPIA required

Component 2 — Productivity monitoring:
- AI Act Art 5(1)(f): If emotion recognition is involved, PROHIBITED in workplace. Keyboard/mouse tracking alone is NOT emotion recognition — likely NOT prohibited
- AI Act Annex III(4)(b): HIGH-RISK — AI to monitor and evaluate performance/behaviour of employees
- GDPR Art 6: Legal basis assessment (legitimate interest requires balancing test — employee monitoring is intrusive)
- GDPR Art 88: Member State employment data provisions may restrict monitoring
- GDPR Art 5(1)(c): Data minimisation — is keystroke-level monitoring proportionate?

Component 3 — Sentiment analysis:
- AI Act Art 5(1)(f): PROHIBITED — this IS emotion recognition in the workplace
- Analysing sentiment of communications to infer employee emotions falls squarely within the prohibition
- No "medical or safety" exception applies to attrition prediction
- This component must be DISCONTINUED immediately

Component 4 — Automated performance reviews:
- AI Act Annex III(4)(b): HIGH-RISK — AI for promotion/termination decisions
- GDPR Art 22: Automated decisions influencing promotion = significant effects
- GDPR Art 22(3): Right to human intervention applied to each performance review
- AI Act Art 14: Human reviewer must be able to override automated assessment

Cross-regulation map:
- Component 1: High-risk AI + GDPR Art 22 = dual compliance
- Component 2: High-risk AI + GDPR employment data provisions = dual compliance
- Component 3: PROHIBITED under AI Act = must cease
- Component 4: High-risk AI + GDPR Art 22 = dual compliance
- Enforcement precedent: H&M EUR 35.3M for systematic employee surveillance
- Outcome: Components 1, 2, 4 lawful with extensive safeguards. Component 3 PROHIBITED.

Expected Citations:
- GDPR Articles 5(1)(c), 6, 13(2)(f), 22, 35, 88
- EU AI Act Articles 5(1)(f), 9, 10, 13, 14, 26
- Annex III Categories 4(a), 4(b)
- Enforcement: H&M/HmbBfDI — EUR 35.3M for employee surveillance

Reasoning Path:
hr_system → FOUR_COMPONENTS → assessed_individually
cv_screening → Annex_III_4(a) → high_risk + Art_22 → dual_compliance
productivity_monitoring → Annex_III_4(b) → high_risk + Art_88 → dual_compliance
sentiment_analysis → emotion_recognition → workplace → Art_5(1)(f) → PROHIBITED
performance_reviews → Annex_III_4(b) → high_risk + Art_22 → dual_compliance
h&m_enforcement → PRECEDENT → employee_surveillance_fines

================================================================================
CATEGORY 9: GPAI & FOUNDATION MODELS (Cases 39-44)
================================================================================

=== CASE STUDY 39 ===
Difficulty: Hard
Category: GPAI & Foundation Models
Scenario: A European AI startup develops a general-purpose AI model with 200 billion parameters, trained on a diverse multilingual corpus including scraped web data, books, and academic papers. The model is offered via API to downstream companies who build customer-facing products. The total compute used for training exceeds 10^25 FLOPS.
Question: What are the AI Act obligations for this GPAI model provider, and does it qualify as a systemic risk model?

Expected Answer Summary:
- AI Act Art 51(1): A GPAI model is classified as having SYSTEMIC RISK if trained with total compute > 10^25 FLOPS — this model qualifies
- AI Act Art 51(2): Commission may also designate systemic risk based on capabilities, reach, or impact — FLOPS threshold is a presumption
- AI Act Art 53: General GPAI obligations apply — technical documentation, transparency to downstream providers, copyright compliance policy, training data summary
- AI Act Art 55: ADDITIONAL obligations for systemic risk models — adversarial testing (red-teaming), model evaluation against state-of-the-art benchmarks, systemic risk assessment and mitigation, incident reporting to AI Office, adequate cybersecurity
- AI Act Art 53(1)(d): Must provide detailed summary of training data content — including copyrighted materials
- AI Act Art 53(1)(c): Must have a policy to comply with EU copyright law (Directive 2019/790), including text and data mining opt-out obligations
- GDPR: If training data includes personal data scraped from the web, GDPR applies — need Art 6 legal basis, Art 14 notification obligations (if data not obtained from data subjects directly)
- GDPR Art 17: Must have mechanism to address erasure requests related to training data
- Outcome: Full GPAI obligations + systemic risk requirements. Dual GDPR and AI Act compliance needed for training data.

Expected Citations:
- EU AI Act Articles 51(1), 51(2), 53, 55
- GDPR Articles 6, 14, 17
- Directive 2019/790 (Copyright in the Digital Single Market)

Reasoning Path:
gpai_model → 200B_params → compute > 10^25_FLOPS → Art_51(1) → SYSTEMIC_RISK
systemic_risk → REQUIRES → Art_55 → red_teaming + risk_assessment + incident_reporting
gpai_provider → Art_53 → documentation + transparency + copyright_policy
web_scraping → personal_data → GDPR_applies → Art_6 + Art_14 + Art_17

=== CASE STUDY 40 ===
Difficulty: Medium
Category: GPAI & Foundation Models
Scenario: An open-source community develops and releases a general-purpose AI model under the Apache 2.0 licence. The model has 7 billion parameters and was trained with compute well below 10^25 FLOPS. The release includes model weights, training code, and a model card. A European fintech company downloads the model and fine-tunes it for automated credit scoring.
Question: How do AI Act GPAI obligations differ between the open-source provider and the downstream fintech company?

Expected Answer Summary:
- AI Act Art 53(2): Open-source GPAI models have REDUCED obligations — only need to provide: (a) model card with technical documentation summary, and (b) copyright compliance policy. Exempted from most Art 53(1) requirements
- Art 53(2) condition: Reduced obligations ONLY if the model does not have systemic risk — 7B parameters + low compute = no systemic risk, so reduced obligations apply
- Fintech company: By fine-tuning an open-source model for credit scoring (Annex III(5)(b)), the company becomes the PROVIDER of a HIGH-RISK AI system under Art 25(1)(c) — substantial modification for a high-risk use
- Art 25(1)(c): When a downstream deployer substantially modifies a GPAI model and places it on market for a high-risk use, they assume FULL provider obligations
- Full high-risk obligations for fintech: Art 9 (risk management), Art 10 (data governance), Art 13 (transparency), Art 14 (human oversight), Art 15 (accuracy), conformity assessment
- GDPR Art 22: Credit scoring = automated decision with legal effects — GDPR Art 22 safeguards apply independently
- Outcome: Open-source developer has minimal obligations. Fintech company bears full high-risk AI provider + GDPR controller obligations.

Expected Citations:
- EU AI Act Articles 25(1)(c), 53(2)
- Annex III Category 5(b)
- GDPR Article 22

Reasoning Path:
open_source_model → below_systemic_threshold → Art_53(2) → REDUCED_obligations
fintech → fine_tunes → for_credit_scoring → Annex_III_5(b) → HIGH_RISK
fine_tuning → substantial_modification → Art_25(1)(c) → fintech_becomes_PROVIDER
fintech → FULL_obligations → Art_9 + Art_10 + Art_13 + Art_14 + conformity_assessment

=== CASE STUDY 41 ===
Difficulty: Hard
Category: GPAI & Foundation Models
Scenario: A European media company integrates a third-party GPAI model (via API) to generate news article summaries and headlines. The GPAI provider is based in the US. A generated summary contains fabricated quotes attributed to a real EU politician, which are published on the media company's website and go viral.
Question: Who is liable under the AI Act and GDPR — the GPAI provider, the media company, or both?

Expected Answer Summary:
- AI Act Art 53(1)(a): GPAI provider must provide documentation to downstream deployers about model capabilities and LIMITATIONS (including hallucination risks)
- AI Act Art 50(2): AI-generated content that could be mistaken for genuine content must be MARKED as AI-generated — the media company failed to label the output
- AI Act Art 50(4): Deepfake-like content (fabricated quotes attributed to real persons) must be disclosed as AI-generated
- AI Act — GPAI provider liability: If the provider failed to document hallucination risks or provide adequate guardrails, they bear responsibility under Art 53
- AI Act — Media company liability: As DEPLOYER, the media company must use the system "in accordance with instructions" (Art 26) and implement quality controls. Publishing AI output without review = deployer negligence
- GDPR Art 5(1)(d): Accuracy principle — publishing fabricated quotes about an identifiable person violates data accuracy obligations
- GDPR Art 82: The politician can claim compensation from the media company (controller) for non-material damage (reputational harm)
- GDPR Art 17: Right to erasure — politician can demand immediate removal of fabricated content
- Product Liability: Revised Product Liability Directive includes AI — GPAI provider may face liability for defective output
- Outcome: BOTH parties liable — GPAI provider for inadequate documentation/guardrails, media company for failure to review and label AI content

Expected Citations:
- EU AI Act Articles 26, 50(2), 50(4), 53(1)(a)
- GDPR Articles 5(1)(d), 17, 82
- Product Liability Directive (revised)

Reasoning Path:
gpai_generates → fabricated_quotes → about_real_person → published_without_review
gpai_provider → Art_53(1)(a) → must_document → hallucination_risks
media_company → deployer → Art_26 → must_verify_output → FAILED
fabricated_quotes → Art_50(4) → must_label_as_AI → NOT_DONE
politician → GDPR_Art_5(1)(d) → accuracy_violated → Art_82 → compensation

=== CASE STUDY 42 ===
Difficulty: Medium
Category: GPAI & Foundation Models
Scenario: A European cloud provider offers a "model-as-a-service" platform where customers can deploy various GPAI models (both proprietary and open-source). The platform provides the compute infrastructure but does not modify or fine-tune the models. A customer deploys a GPAI model on this platform to generate synthetic personal data for software testing.
Question: What is the cloud provider's status under the AI Act — are they a provider, deployer, or distributor?

Expected Answer Summary:
- AI Act Art 3(3): "Provider" = develops or has developed an AI system or GPAI model and places it on the market or into service under own name
- AI Act Art 3(4): "Deployer" = uses an AI system under their authority (except personal non-professional use)
- Cloud provider analysis: They provide INFRASTRUCTURE, not the AI system itself — they are neither the provider of the GPAI model nor the deployer of the application
- AI Act Art 25(3): An entity that provides tools, services, or infrastructure for high-risk AI systems is NOT considered a provider merely for that reason
- However: If the cloud platform curates, recommends, or bundles specific models, the analysis may shift toward distributor obligations
- GPAI model provider: Retains Art 53 obligations regardless of where the model is hosted
- Customer using the model: Is the DEPLOYER and potentially the PROVIDER if they create a distinct AI system
- Synthetic personal data: If synthetic data can be linked to real individuals, GDPR still applies (Recital 26 identifiability test)
- Outcome: Cloud provider = infrastructure supplier (limited obligations). GPAI model originator = provider under Art 53. Customer = deployer/provider depending on use.

Expected Citations:
- EU AI Act Articles 3(3), 3(4), 25(3), 53
- GDPR Recital 26

Reasoning Path:
cloud_provider → provides → infrastructure → NOT → AI_system_provider
Art_25(3) → infrastructure_supplier → NOT_automatically → provider
gpai_model_originator → RETAINS → Art_53_obligations
customer → DEPLOYS → model → IS → deployer → potentially → provider_if_new_system
synthetic_data → identifiability_test → Recital_26 → IF_linkable → GDPR_applies

=== CASE STUDY 43 ===
Difficulty: Easy
Category: GPAI & Foundation Models
Scenario: A European company uses a GPAI model to generate marketing images for social media campaigns. The AI creates photorealistic images of fictitious people wearing the company's products. The images are posted on Instagram and Facebook without any disclosure that they are AI-generated.
Question: What AI Act transparency obligations apply to AI-generated images?

Expected Answer Summary:
- AI Act Art 50(2): Deployers of AI systems that generate SYNTHETIC content (images, audio, video, text) that resembles authentic content must DISCLOSE that the content is AI-generated
- AI Act Art 50(2): Disclosure must be in a "machine-readable format" and clearly visible — applies to photorealistic images of fictitious persons
- AI Act Art 50(4): Content constituting a "deep fake" (AI-generated content falsely appearing to depict real persons) has additional labelling requirements — BUT here the people are fictitious, so Art 50(4) deep fake provisions are less directly applicable
- AI Act Art 50(2) exception: Does not apply if content is part of an "obviously creative, satirical, artistic or fictional" work — standard marketing images likely do NOT qualify for this exception
- GPAI provider obligation: Art 53(1)(b) — provider of the GPAI model must ensure outputs are marked in machine-readable format to enable downstream compliance
- GDPR: Fictitious persons = no identifiable data subjects = GDPR does NOT apply to the generated images themselves
- Platform terms: Instagram/Facebook may impose additional AI content labelling requirements
- Outcome: AI Act Art 50(2) labelling required. Must disclose AI-generated nature clearly and in machine-readable format.

Expected Citations:
- EU AI Act Articles 50(2), 50(4), 53(1)(b)

Reasoning Path:
ai_generated_images → photorealistic → synthetic_content → Art_50(2) → MUST_LABEL
fictitious_persons → NOT → deep_fake → Art_50(4) → less_applicable
marketing_images → NOT → artistic_or_satirical → exception_does_NOT_apply
gpai_provider → Art_53(1)(b) → must_enable → machine_readable_marking

=== CASE STUDY 44 ===
Difficulty: Hard
Category: GPAI & Foundation Models
Scenario: A consortium of European research institutions develops a large multimodal GPAI model capable of processing text, images, and video. Training data includes: (a) licensed datasets, (b) web-scraped content including EU citizens' social media posts and photos, and (c) medical imaging datasets obtained from hospital partnerships. The model is released under a research licence for non-commercial use, but several companies begin using it commercially.
Question: What are the cumulative obligations regarding training data governance, copyright, and personal data?

Expected Answer Summary:
- AI Act Art 53(1)(c): Must comply with EU copyright law — Directive 2019/790 Art 4 allows text and data mining (TDM) UNLESS rights holders opt out. Must respect TDM opt-outs for web-scraped content
- AI Act Art 53(1)(d): Must provide sufficiently detailed summary of training data — enabling copyright holders to identify their content
- GDPR — Web-scraped social media data: Personal data of EU citizens processed without consent. Art 6 legal basis needed (legitimate interest under Art 6(1)(f) — but balancing test difficult at scale). Art 14 requires notification to data subjects whose data was scraped
- GDPR — Medical imaging data: Art 9 special category (health data) — requires explicit consent Art 9(2)(a) or research exception Art 9(2)(j) with Art 89(1) safeguards. Hospital partnership must include Art 28 DPA if consortium is processor
- Licence enforcement: "Non-commercial" licence does not absolve the consortium from AI Act obligations. Companies using it commercially become providers under Art 25 — but consortium's original obligations remain
- AI Act Art 53(2): Research licence ≠ open source licence. Reduced obligations under Art 53(2) only apply to models with "open-source" parameters and weights made publicly available under qualifying licences
- Outcome: Complex multi-layered compliance — copyright TDM rules, GDPR for web-scraped data, Art 9 for medical data, and ongoing obligations regardless of downstream licence violations

Expected Citations:
- EU AI Act Articles 25, 53(1)(c)(d), 53(2)
- GDPR Articles 6, 9, 14, 28, 89(1)
- Directive 2019/790 Articles 3, 4 (Text and Data Mining)

Reasoning Path:
training_data → THREE_SOURCES → each_assessed_separately
licensed_datasets → compliant → BUT → check_TDM_opt_outs
web_scraped_data → personal_data → Art_6 + Art_14 → notification_required
medical_imaging → health_data → Art_9 → research_exception → Art_9(2)(j) + Art_89(1)
research_licence → NOT → open_source → Art_53(2)_reduced_obligations → DO_NOT_APPLY
commercial_misuse → downstream_companies → become_providers → Art_25

================================================================================
CATEGORY 10: TRANSPARENCY & EXPLAINABILITY (Cases 45-49)
================================================================================

=== CASE STUDY 45 ===
Difficulty: Medium
Category: Transparency & Explainability
Scenario: A European insurance company uses a deep neural network for underwriting decisions. When a customer asks why their premiums increased by 40%, the company responds: "Our AI model determined your risk profile warrants a higher premium." No further detail is provided. The model is a black-box system with no built-in explainability features.
Question: Does this response satisfy GDPR and AI Act transparency requirements?

Expected Answer Summary:
- GDPR Art 13(2)(f): Must provide "meaningful information about the logic involved" in automated decision-making — a generic statement about "AI model" is NOT meaningful
- GDPR Art 15(1)(h): On access request, must explain the logic, significance, and envisaged consequences of automated processing — requires describing the KEY FACTORS that influenced the decision
- GDPR Recital 71: Explanation should allow the data subject to "understand" the decision — requires indicating which data categories and features most influenced the outcome
- AI Act Annex III(5)(c): Insurance pricing AI is HIGH-RISK — subject to Art 13 transparency
- AI Act Art 13(1): High-risk AI must be designed to be sufficiently transparent for deployers to interpret outputs appropriately
- AI Act Art 13(3)(b)(ii): Instructions of use must include "the level of accuracy, robustness and cybersecurity... and any known circumstance that may impact that level"
- AI Act Art 86: Right to explanation for decisions made by high-risk AI systems affecting individuals
- Outcome: Response is INADEQUATE. Must provide: (i) key factors/features used, (ii) their relative influence, (iii) how those factors led to the increase, (iv) right to human review

Expected Citations:
- GDPR Articles 13(2)(f), 15(1)(h), Recital 71
- EU AI Act Articles 13, 86
- Annex III Category 5(c)

Reasoning Path:
generic_AI_explanation → NOT → meaningful_information → VIOLATES → Art_13(2)(f) + Art_15(1)(h)
insurance_pricing → HIGH_RISK → Art_13 → requires → interpretable_outputs
Art_86 → right_to_explanation → must_describe → key_factors + relative_influence
black_box_model → inadequate_by_design → VIOLATES → Art_13(1)_transparency

=== CASE STUDY 46 ===
Difficulty: Hard
Category: Transparency & Explainability
Scenario: A European law enforcement agency uses a predictive policing AI system to forecast crime hotspots and allocate patrol resources. The system generates heat maps of predicted criminal activity based on historical crime data, socio-economic indicators, and weather patterns. A civil liberties organisation files an access request demanding full disclosure of the algorithm.
Question: What transparency obligations exist for predictive policing AI, and can algorithmic secrecy be justified?

Expected Answer Summary:
- GDPR Art 15(1)(h): Right to meaningful information about the logic of automated processing — but Art 23(1)(d) allows restrictions when necessary for "prevention, investigation, detection or prosecution of criminal offences"
- GDPR Art 23(1): Restrictions must be necessary and proportionate, applied on a case-by-case basis — blanket refusal to disclose anything is disproportionate
- AI Act Art 6(2) + Annex III(6)(a): HIGH-RISK — AI used by law enforcement for predicting occurrence of criminal offences based on profiling or assessment of personality traits
- AI Act Art 13: Transparency to the DEPLOYER (police agency) is mandatory even if public disclosure is restricted
- AI Act Art 14: Human oversight — police officers must understand the system's limitations and not blindly follow AI predictions
- AI Act Art 27: FUNDAMENTAL RIGHTS IMPACT ASSESSMENT required before deployment by law enforcement
- Bias risk: Historical crime data encodes past enforcement bias (over-policing of certain neighbourhoods) — Art 10(2)(f) requires bias examination
- Outcome: Full public disclosure of algorithm NOT required. But: (i) deploying agency must fully understand the system, (ii) affected individuals retain limited transparency rights, (iii) fundamental rights assessment mandatory, (iv) training data bias must be addressed

Expected Citations:
- GDPR Articles 15(1)(h), 23(1)(d)
- EU AI Act Articles 10(2)(f), 13, 14, 27
- Annex III Category 6(a)
- EU Charter of Fundamental Rights Articles 7, 8, 21

Reasoning Path:
predictive_policing → Annex_III_6(a) → HIGH_RISK → full_compliance
algorithm_disclosure → RESTRICTED → Art_23(1)(d) → criminal_enforcement_exception
BUT → restriction_must_be → proportionate → NOT_blanket_refusal
deployer_transparency → Art_13 → police_MUST_understand → system_limitations
historical_crime_data → encodes → enforcement_bias → Art_10(2)(f) → must_address

=== CASE STUDY 47 ===
Difficulty: Easy
Category: Transparency & Explainability
Scenario: A European airline deploys an AI chatbot for customer support that handles booking changes, cancellations, and complaints. Some customers believe they are speaking with a human agent because the chatbot uses a human name ("Hi, I'm Sarah!") and natural conversational language.
Question: What transparency obligations apply to AI chatbots interacting with customers?

Expected Answer Summary:
- AI Act Art 50(1): Deployers of AI systems DESIGNED TO INTERACT WITH NATURAL PERSONS must inform individuals that they are interacting with an AI system — MANDATORY, no exceptions for customer service
- AI Act Art 50(1): Disclosure must be made "in a timely, clear, and intelligible manner" — using a human name and persona WITHOUT AI disclosure violates this
- GDPR Art 13: General transparency obligation — must inform data subjects about data processing purposes and automated decision-making
- GDPR Art 22: If the chatbot makes decisions (e.g., denying a refund or processing a cancellation), Art 22 automated decision-making rules apply
- Consumer protection: Directive 2005/29/EC (Unfair Commercial Practices) — presenting AI as human to influence customer decisions may constitute a misleading commercial practice
- Outcome: MUST disclose AI nature before or at start of interaction. Using a human name WITHOUT disclaiming AI status is a violation. "Hi, I'm Sarah, an AI assistant" would comply.

Expected Citations:
- EU AI Act Article 50(1)
- GDPR Articles 13, 22
- Directive 2005/29/EC (Unfair Commercial Practices)

Reasoning Path:
ai_chatbot → interacts_with → natural_persons → Art_50(1) → MUST_DISCLOSE_AI
human_name_persona → WITHOUT_disclosure → VIOLATES → Art_50(1)
booking_decisions → automated → Art_22 → may_apply
misleading_identity → Directive_2005/29/EC → unfair_commercial_practice

=== CASE STUDY 48 ===
Difficulty: Hard
Category: Transparency & Explainability
Scenario: A European government agency uses an AI system to score asylum applications based on interview transcripts, country-of-origin information, and document analysis. The system assigns a "credibility score" to each applicant. Caseworkers have access to the score but not to the reasons behind it. An asylum seeker whose application was rejected wants to understand why they received a low credibility score.
Question: What level of explanation must be provided for AI-assisted asylum decisions?

Expected Answer Summary:
- AI Act Annex III(7)(c): HIGH-RISK — AI used to assess asylum applications or examine applications for residence
- AI Act Art 14: Human oversight MUST include the ability to fully understand the system's outputs — caseworkers who cannot see reasons VIOLATE Art 14(4)(a) which requires understanding "capacities and limitations"
- AI Act Art 86: Right to clear and meaningful explanation of the role of the AI system in the decision-making procedure and the main elements of the decision taken
- AI Act Art 14(4)(b): Human overseers must be able to "correctly interpret the high-risk AI system's output" — a raw score without reasoning fails this
- GDPR Art 22: Asylum decisions are "legal effects" — full Art 22 protections apply
- GDPR Art 15(1)(h): Meaningful information about logic — particularly critical given fundamental rights at stake (right to asylum under Art 18 EU Charter)
- GDPR Art 22(3): Right to human intervention — caseworker must make a genuinely independent assessment, not rubber-stamp the AI score
- EU Charter Art 47: Right to effective judicial review — impossible without understanding the basis of the decision
- Outcome: HIGHEST level of explanation required. Credibility scoring without reasons is unlawful. Caseworkers must understand AND be able to explain the AI's reasoning.

Expected Citations:
- EU AI Act Articles 14(4)(a)(b), 86
- Annex III Category 7(c)
- GDPR Articles 15(1)(h), 22, 22(3)
- EU Charter of Fundamental Rights Articles 18, 47

Reasoning Path:
asylum_credibility_scoring → Annex_III_7(c) → HIGH_RISK → strictest_requirements
score_without_reasons → VIOLATES → Art_14(4)(a) → caseworker_cannot_understand
asylum_seeker → fundamental_rights → EU_Charter_Art_18_47 → highest_explanation_standard
Art_86 → clear_meaningful_explanation → REQUIRED → for_individual_affected
caseworker_rubber_stamping → VIOLATES → Art_14(4)(b) + Art_22(3)

=== CASE STUDY 49 ===
Difficulty: Medium
Category: Transparency & Explainability
Scenario: A European e-commerce platform uses a recommendation AI to suggest products to users. The system processes browsing history, past purchases, demographic data, and inferred preferences. A user notices they are consistently shown luxury items at inflated prices and believes they are being profiled and manipulated.
Question: What transparency rights does the user have regarding the recommendation system?

Expected Answer Summary:
- GDPR Art 13(2)(f): Must inform users about "the existence of automated decision-making, including profiling" and "meaningful information about the logic involved, as well as the significance and the envisaged consequences"
- GDPR Art 15(1)(h): On access request, must disclose the profiling categories, inferences, and how they affect what the user sees
- GDPR Art 21(1): Right to object to profiling based on legitimate interest — platform must stop profiling unless compelling legitimate grounds
- GDPR Art 4(4): Recommendation systems that "evaluate certain personal aspects" constitute PROFILING
- AI Act Art 50(1): Not directly applicable to recommendation systems unless they interact directly with users (chatbot-style)
- AI Act Art 6(3): Profiling proviso — AI that performs profiling of natural persons is ALWAYS considered high-risk — but this applies to profiling with "significant" effects; product recommendations may not reach the threshold
- DSA Art 27: Very Large Online Platforms (VLOPs) must provide transparency about recommendation algorithms and offer a non-profiling-based alternative
- Enforcement precedent: Amazon EUR 746M fine — lack of consent for behavioural advertising/targeting
- Outcome: Strong transparency rights under GDPR. User can demand explanation and object to profiling. DSA may add additional obligations for large platforms.

Expected Citations:
- GDPR Articles 4(4), 13(2)(f), 15(1)(h), 21(1)
- EU AI Act Article 6(3) (profiling proviso)
- Digital Services Act Article 27

Reasoning Path:
recommendation_ai → evaluates → personal_aspects → CONSTITUTES → profiling → Art_4(4)
user → HAS_RIGHT → Art_13(2)(f) → meaningful_logic_information
user → HAS_RIGHT → Art_21(1) → object_to_profiling
luxury_price_targeting → POTENTIAL → Art_22_significant_effects → DEBATED
DSA_Art_27 → VLOPs → must_offer → non_profiling_alternative

================================================================================
CATEGORY 11: CHILDREN'S DATA & VULNERABLE GROUPS (Cases 50-54)
================================================================================

=== CASE STUDY 50 ===
Difficulty: Medium
Category: Children's Data & Vulnerable Groups
Scenario: A popular children's educational app uses an AI system to adapt lesson difficulty based on the child's performance, attention patterns (detected via device interaction), and learning speed. The app collects children's names, ages, school grades, and behavioural interaction data. Parents consent to data processing when creating the child's account.
Question: What specific GDPR protections apply to AI processing of children's data in educational apps?

Expected Answer Summary:
- GDPR Art 8(1): For information society services offered directly to a child, consent is valid only if the child is at least 16 years old (or lower age set by Member State, minimum 13). Below that threshold, parental consent is required
- GDPR Art 8(2): Controller must make "reasonable efforts" to verify that parental consent was given — merely ticking a box is insufficient
- GDPR Recital 38: "Children merit specific protection with regard to their personal data, as they may be less aware of the risks, consequences and safeguards concerned"
- GDPR Art 5(1)(c): Data minimisation — is tracking "attention patterns" of children proportionate for educational purposes?
- GDPR Art 25: Data protection by design — must implement age-appropriate design standards
- GDPR Art 35: DPIA required — processing children's data at scale with AI profiling
- AI Act Annex III(3)(a): HIGH-RISK — AI systems used to determine access to or admission to educational institutions
- AI Act Recital 47: AI systems used in education should be designed considering the particular vulnerability of children
- AI Act Art 9: Risk management must specifically consider risks to children as vulnerable users
- Outcome: Heightened protection required. Parental consent must be verifiable. Data minimisation strictly applied. DPIA mandatory. High-risk if AI determines educational outcomes.

Expected Citations:
- GDPR Articles 5(1)(c), 8(1), 8(2), 25, 35, Recital 38
- EU AI Act Articles 9, Annex III Category 3(a), Recital 47

Reasoning Path:
children_educational_app → Art_8 → parental_consent_required → must_verify
attention_tracking → Art_5(1)(c) → data_minimisation → proportionality_check
children_data → Recital_38 → specific_protection → heightened_standards
ai_adaptive_learning → IF → determines_educational_access → Annex_III_3(a) → HIGH_RISK

=== CASE STUDY 51 ===
Difficulty: Hard
Category: Children's Data & Vulnerable Groups
Scenario: A social media platform with a minimum age requirement of 13 uses AI age estimation technology to verify user ages. The system analyses facial features from selfies to estimate whether the user is under 13. If the AI estimates the user is underage, the account is restricted or blocked. The system has a 15% false positive rate (adults incorrectly classified as children) and a 5% false negative rate (children incorrectly passing verification).
Question: What are the GDPR and AI Act implications of AI-based age verification?

Expected Answer Summary:
- AI Act Art 50(3): AI systems that use biometric categorisation (e.g., age estimation from facial features) must inform the individual about the system's operation at the time of exposure
- GDPR Art 9: Facial analysis for age estimation may constitute BIOMETRIC DATA processing — special category
- GDPR Art 9(2)(g): May be justified under "substantial public interest" (child protection), subject to Member State law providing suitable safeguards
- AI Act: Age verification AI is NOT explicitly listed in Annex III — but if it determines access to services (educational institution or information services), it may intersect with Annex III (3)(a) or (8)
- False positive issue (15%): Adults wrongly blocked from service — proportionality concern under GDPR Art 5(1)(c) and affects user rights
- False negative issue (5%): Children bypassing age gate — undermines the very purpose of the system
- AI Act Art 15: Accuracy, robustness, and cybersecurity — 15% false positive rate may fail accuracy requirements
- GDPR Art 22: Age estimation decision (block/allow) is automated decision with significant effects — Art 22 applies
- Alternative approaches: Age assurance via third-party verification may be less intrusive than biometric analysis
- Outcome: Lawful in principle for child protection, but biometric processing requires Art 9 basis. High false positive rate raises proportionality concerns. Must provide human review for blocked users.

Expected Citations:
- GDPR Articles 5(1)(c), 9, 9(2)(g), 22
- EU AI Act Articles 15, 50(3)

Reasoning Path:
age_estimation → facial_analysis → biometric_data → Art_9 → special_category
child_protection → substantial_public_interest → Art_9(2)(g) → may_justify
false_positive_15% → adults_blocked → Art_22 → right_to_contest
false_negative_5% → children_bypass → effectiveness_concern
Art_15 → accuracy_requirements → 15%_FP_rate → potential_failure

=== CASE STUDY 52 ===
Difficulty: Easy
Category: Children's Data & Vulnerable Groups
Scenario: A toy manufacturer embeds an AI voice assistant in a children's smart toy. The toy records children's voice commands, conversations, and questions, sending them to cloud servers for processing. The toy also collects the child's name, age, and location to personalise responses.
Question: What GDPR and AI Act requirements apply to AI-enabled smart toys collecting children's data?

Expected Answer Summary:
- GDPR Art 8: Children's data — parental consent required and must be verified
- GDPR Art 5(1)(c): Data minimisation — must question whether recording ALL conversations is necessary. Voice commands for toy functionality may be justified; continuous recording is excessive
- GDPR Art 5(1)(e): Storage limitation — conversations must not be retained longer than necessary for the toy to function
- GDPR Art 32: Security — cloud transmission of children's voice data requires encryption and robust security
- GDPR Art 35: DPIA required — systematic monitoring of children through smart devices
- GDPR Art 25: Data protection by design — implement on-device processing where possible to avoid cloud transmission
- AI Act Art 50(1): Must inform users (parents/children) that they are interacting with an AI system
- ePrivacy Directive Art 5(3): Accessing device microphone requires consent — applies to the smart toy
- Enforcement precedent: VTech data breach (2015) — exposed children's data; My Friend Cayla toy banned in Germany for surveillance concerns
- Outcome: Strict requirements. Parental consent, minimal data collection, robust security, DPIA, and AI disclosure all mandatory.

Expected Citations:
- GDPR Articles 5(1)(c)(e), 8, 25, 32, 35
- EU AI Act Article 50(1)
- ePrivacy Directive Article 5(3)

Reasoning Path:
smart_toy → records → children_voice → GDPR_Art_8 → parental_consent
continuous_recording → EXCESSIVE → Art_5(1)(c) → data_minimisation
cloud_transmission → Art_32 → encryption_required
children_monitoring → Art_35 → DPIA_mandatory
voice_assistant → Art_50(1) → must_disclose_AI

=== CASE STUDY 53 ===
Difficulty: Hard
Category: Children's Data & Vulnerable Groups
Scenario: A European school district deploys an AI system that analyses students' classroom behaviour through CCTV cameras to detect signs of bullying, violence, and distress. The system flags incidents to teachers and school administrators in real time. Parents were informed via a general school newsletter but individual consent was not obtained.
Question: Is AI-based behavioural surveillance of children in schools lawful under GDPR and the AI Act?

Expected Answer Summary:
- GDPR Art 6(1)(e): Schools may rely on "public interest" or "exercise of official authority" — but surveillance via AI goes beyond normal educational tasks
- GDPR Art 6(1)(a): Consent is problematic — not freely given due to power imbalance between school and parents. EDPB guidance: consent in educational context is often not freely given
- GDPR Art 35: DPIA MANDATORY — systematic monitoring of children in an educational environment on a large scale
- GDPR Art 5(1)(c): Data minimisation — continuous CCTV analysis of ALL student behaviour is disproportionate to detecting specific incidents
- GDPR Recital 38: Children merit specific protection — heightened bar for AI surveillance of minors
- AI Act Annex III(3)(d): HIGH-RISK — AI for monitoring and detecting prohibited behaviour of students during tests or in educational institutions
- AI Act Art 9: Risk management — must specifically address false positive risks (children wrongly flagged as bullies) and stigmatisation effects
- AI Act Art 14: Human oversight — flags must be reviewed by humans before any intervention
- Newsletter notification: INSUFFICIENT under Art 13 — must provide specific, detailed information about AI processing to each parent individually
- Outcome: Very high compliance burden. Likely disproportionate under GDPR. If permitted at all, requires individual parental notification, DPIA, high-risk AI compliance, and robust human oversight.

Expected Citations:
- GDPR Articles 5(1)(c), 6(1)(a)(e), 13, 35, Recital 38
- EU AI Act Articles 9, 14
- Annex III Category 3(d)

Reasoning Path:
school_cctv_ai → monitors → children_behaviour → HIGHEST_SCRUTINY
consent → power_imbalance → NOT_freely_given → Art_6(1)(a)_problematic
public_interest → Art_6(1)(e) → surveillance_exceeds → normal_educational_task
Annex_III_3(d) → monitoring_students → HIGH_RISK → full_compliance
continuous_surveillance → Art_5(1)(c) → disproportionate → data_minimisation_fails
newsletter_notification → INSUFFICIENT → Art_13 → requires_specific_individual_notice

=== CASE STUDY 54 ===
Difficulty: Medium
Category: Children's Data & Vulnerable Groups
Scenario: A European healthcare AI startup develops a mental health chatbot targeted at teenagers (ages 13-17). The chatbot uses AI to detect signs of depression, anxiety, and self-harm from conversation patterns and recommends coping strategies. It processes sensitive mental health data and can escalate to human counsellors if suicide risk is detected.
Question: What legal framework applies to an AI mental health tool for minors?

Expected Answer Summary:
- GDPR Art 8: For ages 13-17, Member State dependent — some allow consent from 13, others require parental consent until 16. Must comply with applicable Member State threshold
- GDPR Art 9: Mental health data = HEALTH DATA (special category). Requires explicit consent Art 9(2)(a), or Art 9(2)(h) healthcare processing with appropriate safeguards
- GDPR Art 9(2)(c): "Vital interests" exception may apply for suicide risk escalation when the teenager cannot give consent (e.g., imminent self-harm)
- GDPR Art 35: DPIA mandatory — large-scale processing of minors' health data through AI
- AI Act Annex III(5)(a): Potentially HIGH-RISK — AI evaluating access to or providing healthcare services
- AI Act Art 5(1)(b): Must NOT exploit vulnerability (mental health struggles of teenagers) — system must genuinely help, not retain users through dependency
- AI Act Art 9: Risk management must address: (i) incorrect detection of self-harm, (ii) failure to detect genuine suicide risk, (iii) inappropriate coping advice
- AI Act Art 50(1): Must inform teenagers they are interacting with AI, not a human counsellor
- Professional liability: If the chatbot provides medical/therapeutic advice, medical device regulations may also apply
- Outcome: Lawful but EXTREMELY high compliance burden. Requires: age-appropriate consent, special category basis, DPIA, high-risk AI compliance, suicide risk protocols, and clear AI disclosure.

Expected Citations:
- GDPR Articles 8, 9(2)(a)(c)(h), 35
- EU AI Act Articles 5(1)(b), 9, 50(1)
- Annex III Category 5(a)
- Regulation (EU) 2017/745 (MDR) if medical device

Reasoning Path:
mental_health_chatbot → for_minors → HIGHEST_PROTECTION_STANDARD
mental_health_data → Art_9 → health_data → explicit_consent_or_healthcare_exception
suicide_risk_escalation → Art_9(2)(c) → vital_interests → emergency_exception
teenager_vulnerability → Art_5(1)(b) → must_NOT_exploit → must_PROTECT
false_negatives → missed_suicide_risk → Art_9_risk_management → CRITICAL

================================================================================
CATEGORY 12: ENFORCEMENT & PENALTIES (Cases 55-59)
================================================================================

=== CASE STUDY 55 ===
Difficulty: Medium
Category: Enforcement & Penalties
Scenario: A medium-sized European adtech company (annual turnover EUR 50 million) processes personal data from 15 million EU users for behavioural advertising without valid consent. The company also deploys an AI profiling system classified as high-risk under the AI Act without completing a conformity assessment. A supervisory authority investigates.
Question: What is the maximum penalty exposure under both GDPR and the AI Act, and can penalties be cumulative?

Expected Answer Summary:
- GDPR Art 83(5)(a): Processing without valid consent = up to EUR 20 million or 4% of total worldwide annual turnover, whichever is HIGHER. For this company: max EUR 20M (4% of EUR 50M = EUR 2M, so EUR 20M ceiling applies)
- AI Act Art 99(3): Deploying a high-risk AI system without conformity assessment = up to EUR 15 million or 3% of total worldwide annual turnover. For this company: max EUR 15M
- AI Act Art 99(6): For SMEs and startups, penalties are the lower of the percentage or fixed amount — but with EUR 50M turnover, the company may not qualify as SME
- Cumulative penalties: GDPR and AI Act are separate regulations — penalties CAN be imposed cumulatively for different violations. However, the ne bis in idem principle (Art 50 EU Charter) prevents double punishment for the SAME factual conduct
- AI Act Art 99(7): When determining penalties, authorities must consider penalties already imposed under GDPR for related conduct
- GDPR Art 83(2): Aggravating factors — 15 million affected users, intentional nature (no attempt to get consent), and duration of infringement
- Outcome: Total theoretical exposure up to EUR 35M. In practice, authorities coordinate to avoid double punishment, but separate violations of distinct regulations can be penalised separately.

Expected Citations:
- GDPR Article 83(5)(a), 83(2)
- EU AI Act Article 99(3), 99(6), 99(7)
- EU Charter Article 50 (ne bis in idem)

Reasoning Path:
no_consent → GDPR_Art_83(5)(a) → up_to → EUR_20M_or_4%_turnover
no_conformity_assessment → AI_Act_Art_99(3) → up_to → EUR_15M_or_3%_turnover
cumulative? → separate_regulations → separate_violations → CAN_cumulate
BUT → Art_99(7) → must_consider → existing_GDPR_penalties
ne_bis_in_idem → Art_50_Charter → same_conduct → no_double_punishment

=== CASE STUDY 56 ===
Difficulty: Hard
Category: Enforcement & Penalties
Scenario: An EU supervisory authority discovers that a large US tech company (worldwide turnover EUR 200 billion) has been operating a prohibited AI practice under Art 5(1)(c) (social scoring) across multiple EU Member States. Simultaneously, the company has violated GDPR Art 9 (special category data processing without basis), Art 5(1)(a) (fairness), and failed to cooperate with the investigation (Art 31).
Question: What is the maximum combined penalty, and how is cross-border enforcement coordinated?

Expected Answer Summary:
- AI Act Art 99(2): Prohibited AI practices (Art 5 violations) = up to EUR 35 million or 7% of total worldwide annual turnover. For this company: 7% of EUR 200B = EUR 14 BILLION (applicable since higher than EUR 35M)
- GDPR Art 83(5): Art 9 violation = up to 4% turnover = EUR 8 BILLION
- GDPR Art 83(4)(a): Art 31 failure to cooperate = up to 2% turnover = EUR 4 BILLION (lower tier)
- GDPR Art 60: Cross-border enforcement via "one-stop-shop" mechanism — Lead Supervisory Authority coordinates with Concerned Supervisory Authorities
- AI Act Art 74: Market surveillance authorities in each Member State enforce AI Act — coordination via European AI Board
- AI Act Art 99(7): AI Act fines must account for GDPR fines already imposed for overlapping conduct
- GDPR Art 83(2)(a)-(k): Aggravating factors — multiple violations, large scale, special category data, non-cooperation
- Enforcement precedent: Meta EUR 1.2B + EUR 395M + EUR 265M = cumulative GDPR fines for related but distinct violations
- Outcome: Theoretical maximum exceeds EUR 20 billion. Real-world penalties would be lower but still unprecedented. Cross-border coordination through one-stop-shop (GDPR) and AI Board (AI Act).

Expected Citations:
- GDPR Articles 31, 60, 83(4)(a), 83(5)
- EU AI Act Articles 74, 99(2), 99(7)

Reasoning Path:
prohibited_AI_practice → Art_99(2) → 7%_turnover → EUR_14B
Art_9_violation → Art_83(5) → 4%_turnover → EUR_8B
non_cooperation → Art_83(4)(a) → 2%_turnover → EUR_4B
cross_border → GDPR_Art_60 → one_stop_shop + AI_Act_Art_74 → AI_Board
Art_99(7) → penalty_coordination → avoid_double_counting

=== CASE STUDY 57 ===
Difficulty: Easy
Category: Enforcement & Penalties
Scenario: A European startup with annual turnover of EUR 2 million and 15 employees deploys a high-risk AI system for recruitment screening without performing a conformity assessment. The startup argues it was unaware of AI Act requirements and had no compliance team.
Question: Does the AI Act provide leniency for small enterprises?

Expected Answer Summary:
- AI Act Art 99(6): For SMEs including startups, the maximum fine is the LOWER of the fixed amount or the percentage — this is a meaningful concession
- For this startup: Art 99(3) penalty = lower of EUR 15M or 3% of EUR 2M (EUR 60K). Startup pays max EUR 60K, not EUR 15M
- AI Act Art 99(7): When setting fine amount, authority must consider: size of the undertaking, nature/gravity/duration of infringement, good faith, actions taken to mitigate, degree of cooperation
- AI Act Recital 165: Emphasises that penalties for SMEs should be proportionate to their size and economic viability
- AI Act Art 62: AI regulatory sandboxes — Member States must establish sandboxes that give priority to SMEs to test AI systems under regulatory guidance before full compliance
- Ignorance of the law: NOT a defence, but may reduce penalty under Art 99(7) "degree of negligence" factor. First violation by a small entity typically attracts guidance and corrective measures before financial penalty
- GDPR parallel: Similar graduated approach — Art 83(2)(a) considers "nature, gravity and duration"
- Outcome: Yes, significant penalty reduction for SMEs. EUR 60K max vs EUR 15M. Sandboxes and guidance available. But ignorance does not exempt from compliance.

Expected Citations:
- EU AI Act Articles 62, 99(3), 99(6), 99(7), Recital 165
- GDPR Article 83(2)

Reasoning Path:
startup → EUR_2M_turnover → 15_employees → SME
Art_99(6) → lower_of → EUR_15M_or_3%_turnover → EUR_60K_max
Art_99(7) → mitigating_factors → unaware + first_violation + cooperation
Art_62 → regulatory_sandbox → priority_for_SMEs
ignorance → NOT_a_defence → BUT → reduces_penalty

=== CASE STUDY 58 ===
Difficulty: Hard
Category: Enforcement & Penalties
Scenario: A DPA conducts an audit of a European bank and finds: (1) the bank's credit scoring AI has a systematic racial bias affecting 50,000 loan applicants over 3 years, (2) no DPIA was ever conducted, (3) no human oversight mechanism exists for automated rejections, and (4) affected customers were never informed about AI involvement in their loan decisions. The bank's turnover is EUR 10 billion.
Question: Map all violations to specific articles and determine penalty tiers.

Expected Answer Summary:
Violation 1 — Racial bias in credit scoring:
- GDPR Art 5(1)(a): Fairness principle violation → Tier 2 penalty: Art 83(5)(a) = up to 4% turnover = EUR 400M
- AI Act Art 10(2)(f): Failure to examine training data for biases → corrective measures under Art 99(3) = up to 3% turnover = EUR 300M

Violation 2 — No DPIA:
- GDPR Art 35: Failure to conduct DPIA → Tier 1 penalty: Art 83(4)(a) = up to 2% turnover = EUR 200M

Violation 3 — No human oversight:
- GDPR Art 22(3): No human intervention mechanism → Tier 2 penalty: Art 83(5)(b) = up to 4% turnover = EUR 400M
- AI Act Art 14: No human oversight for high-risk AI → Art 99(3) = up to 3% turnover = EUR 300M

Violation 4 — No AI disclosure:
- GDPR Art 13(2)(f): Failure to inform about automated decision-making → Tier 2 penalty: Art 83(5)(b) = up to 4% turnover = EUR 400M
- AI Act Art 26(8): Deployer failed to inform individuals about high-risk AI → Art 99(3) = up to 3% = EUR 300M

- GDPR Art 83(3): Where violations concern SAME processing operations, total penalty shall not exceed the highest applicable amount — NOT simply additive
- 50,000 affected over 3 years: Significant aggravating factors under Art 83(2)
- Enforcement precedent: CJEU C-807/21 Deutsche Wohnen — companies CAN be fined even without identifying a specific responsible individual
- Outcome: Total exposure significant but Art 83(3) caps cumulative GDPR fines at highest single tier. Combined GDPR + AI Act penalties calculated separately.

Expected Citations:
- GDPR Articles 5(1)(a), 13(2)(f), 22(3), 35, 83(3), 83(4)(a), 83(5)(a)(b)
- EU AI Act Articles 10(2)(f), 14, 26(8), 99(3)
- CJEU C-807/21 Deutsche Wohnen

Reasoning Path:
racial_bias → Art_5(1)(a) → Tier_2 → 4%_turnover
no_DPIA → Art_35 → Tier_1 → 2%_turnover
no_human_oversight → Art_22(3) + AI_Act_Art_14 → dual_violation
no_AI_disclosure → Art_13(2)(f) + Art_26(8) → dual_violation
Art_83(3) → cumulative_cap → highest_single_tier → NOT_additive
BUT → GDPR_fines + AI_Act_fines → separate_calculations

=== CASE STUDY 59 ===
Difficulty: Medium
Category: Enforcement & Penalties
Scenario: A European company operating a prohibited AI system (real-time biometric identification in public spaces without authorisation) is ordered by the AI Office to cease operations. The company continues operating the system for 6 months while challenging the decision in court, arguing that an ongoing legal challenge suspends the enforcement action.
Question: Can the company continue operating during a legal challenge, and what are the consequences of non-compliance with an enforcement order?

Expected Answer Summary:
- AI Act Art 99(2): Operating a prohibited AI practice = up to EUR 35M or 7% of worldwide turnover — the MOST severe tier
- AI Act Art 16(j): Provider must immediately take corrective actions or withdraw/recall system when ordered by authority
- AI Act Art 79: Market surveillance authority can order withdrawal from market — non-compliance is an additional violation
- Legal challenge: An ongoing court challenge does NOT automatically suspend an enforcement order unless the court grants interim measures (suspension of enforcement)
- Administrative law principle: Administrative decisions are generally presumed valid and enforceable until annulled by a court — the company MUST comply while challenging
- AI Act Art 99(7)(h): Non-cooperation and continued infringement AFTER enforcement action = heavy aggravating factor
- GDPR Art 83(2)(j): Compliance with corrective measures previously ordered is a factor — non-compliance increases penalty
- Additional: 6 months of continued operation = separate ongoing infringement, potentially calculated per day of non-compliance
- Outcome: Challenge does NOT suspend enforcement. Continued operation = additional violations + significantly increased penalties. Company must cease and challenge simultaneously.

Expected Citations:
- EU AI Act Articles 16(j), 79, 99(2), 99(7)(h)
- GDPR Article 83(2)(j)

Reasoning Path:
prohibited_AI → enforcement_order → MUST_CEASE_IMMEDIATELY
legal_challenge → does_NOT → automatically_suspend → enforcement
continued_operation → 6_months → ADDITIONAL_violation → aggravating_factor
Art_99(7)(h) → non_cooperation → INCREASES_penalty
administrative_law → decision_valid → until_court_annuls

================================================================================
CATEGORY 13: DATA PROTECTION BY DESIGN & DEFAULT (Cases 60-64)
================================================================================

=== CASE STUDY 60 ===
Difficulty: Medium
Category: Data Protection by Design & Default
Scenario: A European smart home company develops an AI-powered home security system that uses indoor cameras, microphones, and motion sensors to detect intruders. By default, the system records 24/7 audio and video, retains footage for 90 days, and uploads all data to cloud servers. Users CAN change settings to reduce recording, but the default configuration maximizes data collection.
Question: Does the default configuration violate GDPR's data protection by default principle?

Expected Answer Summary:
- GDPR Art 25(2): Data protection by DEFAULT — by default, only personal data necessary for each specific purpose should be processed. Default settings must be the most privacy-friendly
- Art 25(2) specifics: "By default, personal data shall not be made accessible without the individual's intervention to an indefinite number of natural persons"
- 24/7 recording by DEFAULT: Violates Art 25(2) — security monitoring can be achieved with motion-triggered recording rather than continuous surveillance
- 90-day retention DEFAULT: Violates Art 5(1)(e) storage limitation — must justify why 90 days is necessary. Shorter default with user-configurable extension would comply
- Cloud upload DEFAULT: Violates Art 25(2) — local storage with optional cloud backup would be the privacy-protective default
- GDPR Art 25(1): Data protection by DESIGN — must implement technical measures like encryption, pseudonymisation, and access controls at the design stage
- AI Act Art 9: If the AI security system is safety-related, risk management must address privacy as a design requirement
- Enforcement precedent: EDPB Guidelines 4/2019 on Article 25 — "Data Protection by Design and by Default"
- Outcome: Default configuration VIOLATES Art 25(2). Must change defaults to: motion-triggered recording, shorter retention, local storage. Users may opt INTO more data collection.

Expected Citations:
- GDPR Articles 5(1)(e), 25(1), 25(2)
- EDPB Guidelines 4/2019 on Data Protection by Design and by Default

Reasoning Path:
default_24/7_recording → EXCESSIVE → Art_25(2) → privacy_friendly_default_required
default_90_day_retention → Art_5(1)(e) → must_justify → shorter_default_better
default_cloud_upload → Art_25(2) → local_storage → should_be_default
Art_25(1) → design_stage → encryption + pseudonymisation + access_controls

=== CASE STUDY 61 ===
Difficulty: Hard
Category: Data Protection by Design & Default
Scenario: A European hospital develops an AI diagnostic system in-house. During development, engineers use REAL patient data (un-anonymised MRI scans, diagnoses, and treatment records) in the development/testing environment. The production system has full encryption and access controls, but the development environment has minimal security. A developer's laptop with patient data is stolen.
Question: What GDPR obligations were breached in the development process, and how does data protection by design apply to AI development?

Expected Answer Summary:
- GDPR Art 25(1): Data protection by design applies to the ENTIRE lifecycle of processing — including development and testing, not just production deployment
- GDPR Art 32: Appropriate security measures — development environment with real patient data must have equivalent security to production
- GDPR Art 5(1)(c): Data minimisation — should use SYNTHETIC or ANONYMISED data for development/testing rather than real patient records
- GDPR Art 5(1)(f): Integrity and confidentiality — using real data on developer laptops without encryption violates this
- GDPR Art 9: Health data is special category — heightened security obligations even in dev environments
- GDPR Art 33: Data breach — stolen laptop with patient data must be reported to DPA within 72 hours
- GDPR Art 34: If breach is likely to result in high risk to patients, patients must also be notified
- AI Act Art 10: Data governance — if the AI is high-risk (medical AI), data quality and governance requirements apply to training/testing data too
- Best practice: Use federated learning or differential privacy during development; use synthetic patient data for testing
- Outcome: Multiple violations — no DPbD in development process, inadequate security, data minimisation failure. Breach notification required.

Expected Citations:
- GDPR Articles 5(1)(c)(f), 9, 25(1), 32, 33, 34
- EU AI Act Article 10

Reasoning Path:
real_patient_data → in_dev_environment → Art_25(1) → DPbD_applies_to_ALL_stages
minimal_security → Art_32 → inappropriate → same_data_needs_same_protection
real_data_for_testing → Art_5(1)(c) → should_use_synthetic_or_anonymised
laptop_stolen → Art_33 → breach_notification → 72_hours
health_data → Art_9 → heightened_protection → even_in_development

=== CASE STUDY 62 ===
Difficulty: Easy
Category: Data Protection by Design & Default
Scenario: A European SaaS company builds a project management tool with AI-powered features (task prioritisation, workload prediction, meeting summarisation). The registration form collects: name, email, job title, department, phone number, date of birth, home address, national ID number, and social media profiles. Only name, email, and job title are necessary for the tool to function.
Question: Does the registration form comply with data protection by default?

Expected Answer Summary:
- GDPR Art 25(2): Data protection by default — only personal data NECESSARY for each specific purpose should be processed. Collecting home address, national ID, DOB, and social media for a project management tool is clearly unnecessary
- GDPR Art 5(1)(c): Data minimisation — must collect only data adequate, relevant, and limited to what is necessary
- GDPR Art 5(1)(b): Purpose limitation — home address and national ID have no legitimate purpose for project management
- GDPR Art 25(2): Default must be minimum data — optional fields should not be pre-selected or required
- Solution: Mandatory fields = name, email, job title. Optional fields = phone number, department. Remove entirely = DOB, home address, national ID, social media
- Enforcement precedent: AEPD (Spain) and CNIL (France) have fined companies for collecting excessive registration data
- Outcome: VIOLATES Art 25(2) and Art 5(1)(c). Must redesign registration to collect only necessary data. Additional fields may be optional but cannot be mandatory.

Expected Citations:
- GDPR Articles 5(1)(b)(c), 25(2)

Reasoning Path:
registration_form → collects → 9_fields → only_3_necessary → EXCESSIVE
home_address + national_ID → NO_PURPOSE → project_management → Art_5(1)(b)
Art_25(2) → default = minimum → mandatory_fields → name_email_jobtitle_only
Art_5(1)(c) → data_minimisation → remove_unnecessary_fields

=== CASE STUDY 63 ===
Difficulty: Hard
Category: Data Protection by Design & Default
Scenario: A European autonomous vehicle manufacturer uses AI for navigation, object detection, and collision avoidance. The vehicle's cameras and LIDAR continuously capture images of pedestrians, cyclists, and other vehicles (including licence plates and faces). This data is transmitted to central servers for model improvement. The manufacturer has not implemented any edge-processing or on-device anonymisation.
Question: How should data protection by design be implemented in autonomous vehicle AI systems?

Expected Answer Summary:
- GDPR Art 25(1): Data protection by design — must implement appropriate technical and organisational measures at the design stage. For autonomous vehicles, this means privacy-preserving architecture from the start
- GDPR Art 5(1)(c): Data minimisation — continuous capture of pedestrian faces and licence plates for model improvement is EXCESSIVE if the AI only needs obstacle detection, not identification
- Key DPbD measures required:
  (1) Edge processing: Anonymise faces and licence plates ON DEVICE before any cloud transmission
  (2) Federated learning: Train models locally on vehicles, share only model updates (not raw data) with servers
  (3) Differential privacy: Add noise to training data to prevent individual identification
  (4) Automatic deletion: Raw sensor data deleted after real-time processing; only anonymised/aggregated data retained
- GDPR Art 6(1)(f): Legitimate interest may support SAFETY processing (collision avoidance) but NOT bulk transmission of identifiable data for model improvement
- AI Act Art 9: Risk management for autonomous vehicles as safety-critical HIGH-RISK AI
- AI Act Annex III(2): HIGH-RISK — AI as safety component in road traffic management
- EDPB Guidelines 01/2020: Connected vehicles — specific guidance on privacy in automotive AI
- Outcome: Must redesign architecture for on-device anonymisation and federated learning. Transmitting raw identifiable data to cloud servers is a DPbD failure.

Expected Citations:
- GDPR Articles 5(1)(c), 6(1)(f), 25(1)
- EU AI Act Articles 9, Annex III Category 2
- EDPB Guidelines 01/2020 on Connected Vehicles

Reasoning Path:
autonomous_vehicle → cameras → capture → pedestrians_faces_plates → personal_data
cloud_transmission → raw_data → Art_25(1) → DPbD_failure
required_measures → edge_anonymisation + federated_learning + differential_privacy
Art_5(1)(c) → face_capture → excessive → for_obstacle_detection
Annex_III_2 → safety_component → road_traffic → HIGH_RISK

=== CASE STUDY 64 ===
Difficulty: Medium
Category: Data Protection by Design & Default
Scenario: A European HR software company builds an AI-powered employee analytics dashboard. The system aggregates employee data (performance reviews, email response times, meeting attendance, project completion rates) and presents managers with "team health scores" and individual productivity rankings. Although the seller promotes it as "aggregate analytics," managers can easily drill down to see individual employee metrics.
Question: Does the "aggregate" framing satisfy data protection by design if individual-level data is accessible?

Expected Answer Summary:
- GDPR Art 25(1): DPbD requires implementing effective measures — labelling a system "aggregate" while enabling individual drill-down is NOT genuine privacy by design; it is cosmetic framing
- GDPR Art 25(2): By default, individual-level data should NOT be accessible. Aggregate view should be the default with controlled access to individual data only when justified
- GDPR Art 5(1)(a): Fairness and transparency — marketing the tool as "aggregate analytics" while providing individual surveillance is misleading to both the implementing company and employees
- GDPR Art 5(1)(c): Data minimisation — collecting email response times and meeting attendance for productivity scoring may be excessive
- GDPR Art 88: Member State employment provisions — many EU countries have strict rules on employee monitoring requiring works council consultation
- AI Act Annex III(4)(b): HIGH-RISK — AI for monitoring and evaluating performance of employees
- AI Act Art 26(8): Deployer must inform employees that high-risk AI is being used for monitoring
- Enforcement precedent: H&M EUR 35.3M — systematic employee profiling through manager notes; analogous to systematic AI profiling
- Outcome: "Aggregate" label does NOT satisfy DPbD. Must genuinely limit default access to aggregate data. Individual drill-down requires specific justification, access controls, and employee notification.

Expected Citations:
- GDPR Articles 5(1)(a)(c), 25(1), 25(2), 88
- EU AI Act Articles 26(8), Annex III Category 4(b)
- Enforcement: H&M EUR 35.3M

Reasoning Path:
aggregate_framing → BUT → individual_drill_down → NOT_genuine_DPbD
Art_25(2) → default → aggregate_only → individual_access → controlled_exception
email_response_times → Art_5(1)(c) → excessive → for_productivity
employee_monitoring → Annex_III_4(b) → HIGH_RISK → Art_26(8) → must_inform
H&M_precedent → systematic_employee_profiling → EUR_35.3M

================================================================================
CATEGORY 14: CONTROLLER-PROCESSOR RELATIONS IN AI (Cases 65-69)
================================================================================

=== CASE STUDY 65 ===
Difficulty: Medium
Category: Controller-Processor Relations in AI
Scenario: A European hospital (controller) contracts an AI company (processor) to develop a diagnostic AI model. The contract specifies the AI company must train the model exclusively on the hospital's patient data and delete all data after model delivery. Instead, the AI company retains a copy of the training data and uses it to improve a separate commercial product sold to other hospitals.
Question: What GDPR violations arise from the AI company's unauthorised use of training data?

Expected Answer Summary:
- GDPR Art 28(3)(a): Processor must process data ONLY on documented instructions of the controller — using data for a separate commercial product violates the instruction limitation
- GDPR Art 28(10): A processor that determines purposes and means of processing (deciding to use data for their own product) BECOMES A CONTROLLER for that processing — and is fully liable
- GDPR Art 29: Processor must not process except on instructions of the controller
- GDPR Art 5(1)(b): Purpose limitation — data provided for diagnostic AI development, NOT for commercial product development
- GDPR Art 9: Patient data is special category (health data) — the AI company has NO legal basis under Art 9(2) for this secondary use
- GDPR Art 83(4): Violating Art 28 processor obligations = up to EUR 10M or 2% worldwide turnover
- GDPR Art 82: Both controller and processor may be liable for damages — but the hospital may be absolved if it can prove it was not responsible for the processor's violation
- The hospital: Should have conducted due diligence, included audit rights in Art 28 DPA, and monitored compliance
- Outcome: AI company becomes controller for the unauthorised processing. Violates Art 28, 29, 5(1)(b), and 9. Liable for penalties and damages.

Expected Citations:
- GDPR Articles 5(1)(b), 9, 28(3)(a), 28(10), 29, 82, 83(4)
- EDPB Guidelines 07/2020 on Controller and Processor

Reasoning Path:
ai_company → PROCESSOR → hospital_data → INSTRUCTED → train_model_only
ai_company → RETAINS_DATA → uses_for_own_product → VIOLATES → Art_28(3)(a) + Art_29
own_purposes → Art_28(10) → BECOMES_CONTROLLER → fully_liable
patient_data → Art_9 → NO_legal_basis → for_commercial_product
hospital → should_have → audit_rights → Art_28_DPA → due_diligence

=== CASE STUDY 66 ===
Difficulty: Hard
Category: Controller-Processor Relations in AI
Scenario: Three European banks form a consortium to jointly train a fraud detection AI model using their combined transaction data. Each bank contributes its customer data. They hire a shared AI vendor to host the training infrastructure and manage the model development. No formal agreement between the banks exists regarding their data protection roles.
Question: What is the data protection role of each party, and what agreements are required?

Expected Answer Summary:
- GDPR Art 26: The three banks are JOINT CONTROLLERS — they jointly determine the purposes (fraud detection) and means (combined training) of processing. Must establish a joint controller arrangement
- GDPR Art 26(1): Joint controller arrangement must determine respective responsibilities for GDPR compliance, including: (i) who handles data subject rights, (ii) who provides transparency information, (iii) allocation of liability
- GDPR Art 26(2): The "essence" of the arrangement must be made available to data subjects — regardless of internal allocation, data subjects can exercise rights against ANY of the controllers
- AI vendor: Is a PROCESSOR under Art 28 — processes data on behalf of the joint controllers
- GDPR Art 28: Each bank (or the consortium collectively) must have a Data Processing Agreement with the AI vendor
- GDPR Art 35: Joint DPIA required — each bank contributing customer data to a shared training pool for AI development
- GDPR Art 6(1)(f): Legitimate interest may be the legal basis for fraud detection — but must conduct a balancing test considering the scale of data sharing
- No formal agreement: Significant GDPR violation — Art 26 REQUIRES a documented arrangement. Without it, all three banks are fully liable for all processing
- Outcome: Must establish Art 26 joint controller arrangement + Art 28 DPA with AI vendor. Joint DPIA required. Each bank remains accessible to data subjects.

Expected Citations:
- GDPR Articles 6(1)(f), 26(1), 26(2), 28, 35
- EDPB Guidelines 07/2020 on Controller and Processor
- CJEU C-210/16 Wirtschaftsakademie (joint controller concept)

Reasoning Path:
three_banks → jointly_determine → purposes_and_means → Art_26 → JOINT_CONTROLLERS
no_formal_agreement → VIOLATES → Art_26(1) → must_document_responsibilities
AI_vendor → processes_on_behalf → PROCESSOR → Art_28 → DPA_required
combined_customer_data → Art_35 → joint_DPIA → high_risk_at_scale
Art_26(2) → data_subjects → can_exercise_rights → against_ANY_controller

=== CASE STUDY 67 ===
Difficulty: Medium
Category: Controller-Processor Relations in AI
Scenario: A European company uses a US-based AI-as-a-service provider for document analysis. The AI provider's terms of service state: "We may use your input data to improve our models and services." The European company uploads contracts containing employee names, salaries, and client information.
Question: Does the AI provider's model improvement clause create a controller-processor compliance issue?

Expected Answer Summary:
- GDPR Art 28(3)(a): Processor must process ONLY on controller's instructions — "may use data to improve services" goes beyond the controller's instructed purpose (document analysis)
- If the AI provider processes data for ITS OWN purposes (model improvement), it becomes a CONTROLLER for that processing under Art 28(10) — triggering full controller obligations
- GDPR Art 5(1)(b): Purpose limitation — data uploaded for document analysis, NOT for model training
- GDPR Art 6: The AI provider needs its OWN legal basis for model improvement — cannot piggyback on the European company's basis
- GDPR Art 44: If data is processed in the US for model improvement, international transfer rules apply to THAT processing too
- European company responsibility: By accepting these ToS and uploading personal data, the European company FAILS its controller due diligence obligation under Art 28(1) — must only use processors providing "sufficient guarantees"
- Solution: (i) Negotiate ToS to remove model improvement clause, OR (ii) Opt out of model training (most providers now offer this), OR (iii) Use a processor that commits to instruction-only processing
- Enforcement precedent: OpenAI/Garante investigation — model training on user input data was a central concern
- Outcome: The clause is problematic. European company must ensure processor does NOT use data beyond instructed purpose. Both parties may face liability.

Expected Citations:
- GDPR Articles 5(1)(b), 6, 28(1), 28(3)(a), 28(10), 44
- Enforcement: OpenAI/Garante investigation (Italy)

Reasoning Path:
model_improvement_clause → AI_provider_uses → input_data → for_OWN_purposes
Art_28(3)(a) → beyond_instructions → VIOLATES → processor_obligations
Art_28(10) → AI_provider → BECOMES_CONTROLLER → for_model_improvement
European_company → accepted_ToS → Art_28(1) → due_diligence_failure
solution → opt_out_of_training → OR → negotiate_ToS → instruction_only

=== CASE STUDY 68 ===
Difficulty: Easy
Category: Controller-Processor Relations in AI
Scenario: An EU e-commerce company hires a cloud provider to host its recommendation AI system. The cloud provider only provides compute infrastructure (CPU/GPU) and storage — it does not access, process, or analyse any customer data. The e-commerce company fully controls the AI model, data, and application logic.
Question: Is the cloud provider a "processor" under the GDPR?

Expected Answer Summary:
- GDPR Art 4(8): Processor = entity that processes personal data ON BEHALF OF the controller
- Key question: Does the cloud provider "process" personal data? Art 4(2) defines processing very broadly — including "storage"
- If the cloud provider STORES personal data on its servers (even encrypted), it is technically processing data and IS a processor
- Even if the cloud provider has no access to decrypted data, the act of hosting/storing constitutes processing
- GDPR Art 28: Data Processing Agreement required — even for infrastructure-only providers
- DPA scope: Can be minimal — covering security measures, data location, sub-processor authorisation, breach notification
- If cloud provider provides ONLY physical infrastructure (colocation) with no logical access: The line blurs — some argue colocation is not processing. But most DPAs and EDPB guidance treat cloud hosting as processing
- AI Act Art 25(3): Providing compute infrastructure does NOT make the cloud provider a provider of the AI system — AI Act and GDPR roles can differ
- Outcome: YES, cloud provider is likely a processor for GDPR purposes. Art 28 DPA required. But under AI Act, it is NOT the AI system provider.

Expected Citations:
- GDPR Articles 4(2), 4(8), 28
- EU AI Act Article 25(3)
- EDPB Guidelines 07/2020 on Controller and Processor

Reasoning Path:
cloud_provider → stores → personal_data → Art_4(2) → "storage" = processing
processing_on_behalf → Art_4(8) → PROCESSOR → YES
Art_28 → DPA_required → even_for_infrastructure
AI_Act_Art_25(3) → infrastructure → NOT → AI_system_provider

=== CASE STUDY 69 ===
Difficulty: Hard
Category: Controller-Processor Relations in AI
Scenario: A European company deploys an AI system from Vendor A for initial data collection and preprocessing, feeds the output to Vendor B's AI model for analysis, and then uses Vendor C's platform for visualisation and reporting. Customer personal data flows through all three vendor systems. No vendor has sight of the full data pipeline, and there is no overarching data processing agreement covering the chain.
Question: How should controller-processor relationships be structured in a multi-vendor AI pipeline?

Expected Answer Summary:
- GDPR Art 28(1): Controller (European company) must use ONLY processors providing "sufficient guarantees" — applies to EACH vendor in the chain
- GDPR Art 28(2): No sub-processing without controller authorisation — if any vendor sub-contracts, controller must approve
- GDPR Art 28(3): SEPARATE DPA required with EACH vendor — covering: purpose limitation, security, deletion, audit rights, breach notification
- GDPR Art 28(4): Sub-processor chain obligations — each processor must impose the same data protection obligations on any sub-processor
- No overarching DPA: SIGNIFICANT violation — each vendor processes personal data without controller-processor agreement
- Data flow mapping: Controller must MAP the full data pipeline — which personal data goes to which vendor, for what purpose, and what each vendor can access
- GDPR Art 5(1)(f): Each handoff in the pipeline is a security risk — integrity/confidentiality obligations apply at every stage
- AI Act Art 25(2)(c): If the combined pipeline constitutes a high-risk AI system, the integrator (European company) is the provider and must ensure the entire system complies
- EDPB Guidelines 07/2020: Controller remains responsible for the ENTIRE processing chain — cannot delegate compliance through vendor contracts
- Outcome: Must establish individual DPAs with all three vendors, map data flows, conduct DPIA covering the full pipeline, and ensure security at each handoff. Controller remains fully liable for the entire chain.

Expected Citations:
- GDPR Articles 5(1)(f), 28(1), 28(2), 28(3), 28(4)
- EU AI Act Article 25(2)(c)
- EDPB Guidelines 07/2020 on Controller and Processor

Reasoning Path:
multi_vendor_pipeline → Vendor_A → Vendor_B → Vendor_C → all_process_personal_data
no_overarching_DPA → VIOLATES → Art_28(3) → DPA_required_for_each
controller → must_MAP → full_data_pipeline → Art_5(1)(f)
Art_28(4) → sub_processor_obligations → cascade_DOWN_the_chain
AI_Act_Art_25(2)(c) → integrator → may_be_provider → for_combined_system
controller_responsibility → Art_28(1) → cannot_delegate → compliance

================================================================================
CATEGORY 15: CONSENT & LEGAL BASIS (Cases 70-74)
================================================================================

=== CASE STUDY 70 ===
Difficulty: Medium
Category: Consent & Legal Basis
Scenario: A European online retailer adds a new feature: AI-powered personalised product recommendations. The retailer updates its privacy policy to include a paragraph about AI recommendations and sends an email to all 5 million customers stating: "By continuing to use our service, you consent to AI-powered personalisation." No opt-in mechanism is provided.
Question: Does "continued use" constitute valid consent for AI-based profiling under GDPR?

Expected Answer Summary:
- GDPR Art 4(11): Consent must be "freely given, specific, informed and unambiguous indication of the data subject's wishes by which he or she, by a statement or by a clear affirmative action, agrees to the processing"
- GDPR Art 7(1): Controller must be able to DEMONSTRATE that consent was given — "continued use" provides no demonstrable record
- GDPR Art 7(2): Consent request must be clearly distinguishable from other matters — buried in a privacy policy update is NOT distinguishable
- GDPR Recital 32: "Silence, pre-ticked boxes or inactivity should NOT constitute consent" — continued use IS inactivity
- CJEU C-673/17 Planet49: Confirmed that pre-ticked boxes and implicit consent are not valid — consent requires active opt-in
- GDPR Art 21(1): Even if another legal basis is used (Art 6(1)(f) legitimate interest), users have right to object to profiling
- Alternative to consent: The retailer could use Art 6(1)(f) legitimate interest for basic recommendations, but would need to conduct a balancing test and provide opt-out
- Enforcement precedent: Amazon/CNPD EUR 746M — consent for behavioural targeting must be specific and affirmative
- Outcome: "Continued use" is NOT valid consent. Must implement affirmative opt-in mechanism or rely on legitimate interest with opt-out.

Expected Citations:
- GDPR Articles 4(11), 7(1), 7(2), 21(1), Recital 32
- CJEU C-673/17 Planet49
- Enforcement: Amazon/CNPD EUR 746M

Reasoning Path:
continued_use → inactivity → Recital_32 → NOT_consent
no_affirmative_action → Art_4(11) → not_unambiguous
buried_in_privacy_policy → Art_7(2) → not_distinguishable
Planet49 → CJEU → active_opt_in_required
alternative → Art_6(1)(f) → legitimate_interest → with_opt_out

=== CASE STUDY 71 ===
Difficulty: Hard
Category: Consent & Legal Basis
Scenario: A European hospital wants to use existing patient records (collected for treatment purposes under Art 9(2)(h)) to train an AI diagnostic model. The hospital argues this is "compatible further processing" under Art 5(1)(b) since the AI will also be used for diagnostic purposes. 3 million patient records spanning 10 years would be used. Individual re-consent from all patients is impractical.
Question: Can the hospital rely on "compatible purpose" for AI training, or does it need a new legal basis?

Expected Answer Summary:
- GDPR Art 5(1)(b): Further processing for a purpose compatible with the original purpose does NOT require a new legal basis — but must pass the compatibility test
- GDPR Art 6(4): Compatibility factors: (a) link between original and new purpose, (b) context/relationship, (c) nature of data, (d) possible consequences, (e) existence of safeguards
- Compatibility analysis:
  (a) Link: Strong — both treatment and diagnostic AI serve healthcare
  (b) Context: Hospital-patient relationship maintained
  (c) Nature: Health data — special category, weighs AGAINST liberal interpretation
  (d) Consequences: Model could benefit future patients but also present risks (bias, inaccuracy)
  (e) Safeguards: Pseudonymisation, access controls, DPIA — essential
- GDPR Art 5(1)(b) proviso: Further processing for scientific research is "NOT incompatible" with original purpose IF Art 89(1) safeguards are met — this is a strong argument
- GDPR Art 9(2)(j): Alternative basis — scientific research in healthcare, with Art 89(1) safeguards
- GDPR Art 89(1): Requires technical and organisational safeguards, in particular pseudonymisation
- GDPR Art 35: DPIA MANDATORY for large-scale health data processing
- Key issue: AI model training is NOT the same as individual patient treatment — it is research/development, which has broader implications
- Outcome: Likely lawful under Art 5(1)(b) + Art 89(1) (research compatible purpose) OR Art 9(2)(j) (research basis). But DPIA mandatory, pseudonymisation required, and must provide Art 14 information to patients (since data was not collected for this purpose).

Expected Citations:
- GDPR Articles 5(1)(b), 6(4), 9(2)(h)(j), 14, 35, 89(1)

Reasoning Path:
patient_records → collected_for → treatment → Art_9(2)(h)
AI_training → new_purpose → compatible? → Art_6(4) → compatibility_test
research_proviso → Art_5(1)(b) → "not_incompatible" → IF → Art_89(1)_safeguards
pseudonymisation → Art_89(1) → REQUIRED → for_research_further_processing
3M_records → Art_35 → DPIA_MANDATORY → large_scale_health_data

=== CASE STUDY 72 ===
Difficulty: Easy
Category: Consent & Legal Basis
Scenario: A European mobile app collects location data to provide navigation services (Art 6(1)(b) contract). The app developer decides to also use the accumulated location data to train an AI model that predicts traffic patterns and sells the insights to urban planning consultancies. Users were not informed about this secondary use.
Question: Can location data collected under contractual necessity be repurposed for commercial AI training?

Expected Answer Summary:
- GDPR Art 6(1)(b): Contractual necessity covers processing necessary for the performance of the contract (navigation) — NOT for unrelated commercial purposes
- GDPR Art 5(1)(b): Purpose limitation — navigation data was collected for navigation, not for training commercial AI models. This is a DIFFERENT purpose
- GDPR Art 6(4): Compatibility test — selling traffic insights to consultancies is commercially motivated, not related to the user relationship, and was not communicated. Likely INCOMPATIBLE
- GDPR Art 13: Users were NEVER informed about the AI training purpose — transparency violation
- GDPR Art 6(1)(a): New consent needed for the new purpose — specific, informed consent for AI training and commercial data sharing
- GDPR Art 6(1)(f): Legitimate interest MIGHT apply if data is properly ANONYMISED before AI training — but location data is extremely difficult to truly anonymise
- GDPR Art 5(1)(c): Data minimisation — selling granular location insights raises concerns even if "aggregated"
- Outcome: Cannot repurpose without new legal basis. Must either obtain specific consent for AI training purpose or genuinely anonymise data (which is technically challenging for location data).

Expected Citations:
- GDPR Articles 5(1)(b)(c), 6(1)(a)(b)(f), 6(4), 13

Reasoning Path:
location_data → collected_under → Art_6(1)(b) → for_navigation
AI_training → different_purpose → Art_5(1)(b) → purpose_limitation_violation
no_user_notification → Art_13 → transparency_violation
new_purpose → requires → new_legal_basis → Art_6(1)(a)_consent
anonymisation → location_data → technically_challenging → residual_risk

=== CASE STUDY 73 ===
Difficulty: Hard
Category: Consent & Legal Basis
Scenario: A European government agency wants to deploy an AI-powered video surveillance system in public spaces to detect abandoned luggage (potential security threats). The system processes video feeds in real-time, capturing faces of thousands of people daily. The agency argues no consent is needed because it relies on Art 6(1)(e) (public interest/official authority) and that the primary purpose is public safety, not identifying individuals.
Question: What legal basis is appropriate, and can facial data processing be avoided?

Expected Answer Summary:
- GDPR Art 6(1)(e): Public interest / official authority — valid legal basis IF established in Member State law with clear legal foundation
- GDPR Art 6(3): Art 6(1)(e) must be established by EU or Member State law — cannot be self-declared by the agency without statutory authority
- GDPR Art 9: Faces captured on video = biometric data if processed for identification. BUT if the system only detects OBJECTS (luggage) without identifying people, Art 9 may not be triggered
- Key technical question: Can the system detect abandoned luggage WITHOUT processing facial/biometric data? Yes — object detection AI can analyse shapes and movement patterns WITHOUT facial recognition
- GDPR Art 25(1): Data protection by design — if abandoned luggage detection is the purpose, the system should be DESIGNED to blur or ignore faces and process only object-related features
- GDPR Art 5(1)(c): Data minimisation — processing thousands of faces daily when the purpose is detecting luggage is disproportionate
- AI Act analysis: If the system processes biometric data in public spaces, Art 5(1)(h) real-time biometric prohibition may apply. If purely object detection, the prohibition does not apply
- GDPR Art 35: DPIA mandatory — large-scale video surveillance in public spaces
- Outcome: Art 6(1)(e) is appropriate IF established by law. System MUST be designed to detect objects without facial processing (DPbD). If faces are processed, Art 9 + Art 5 AI Act implications arise.

Expected Citations:
- GDPR Articles 5(1)(c), 6(1)(e), 6(3), 9, 25(1), 35
- EU AI Act Article 5(1)(h)

Reasoning Path:
public_safety → Art_6(1)(e) → requires → Member_State_law_basis → Art_6(3)
facial_data → AVOIDABLE → object_detection_only → Art_25(1) → DPbD
IF_faces_processed → biometric → Art_9 + AI_Act_Art_5(1)(h) → potential_prohibition
data_minimisation → Art_5(1)(c) → faces_unnecessary → for_luggage_detection
large_scale_surveillance → Art_35 → DPIA_MANDATORY

=== CASE STUDY 74 ===
Difficulty: Medium
Category: Consent & Legal Basis
Scenario: A European employer deploys AI-powered scheduling software that analyses employee availability, skills, performance ratings, and personal preferences to generate optimal work schedules. The employer relies on Art 6(1)(b) (contractual necessity) as the legal basis, arguing that scheduling is part of the employment contract.
Question: Is contractual necessity the correct legal basis for AI-driven employee scheduling?

Expected Answer Summary:
- GDPR Art 6(1)(b): Contractual necessity — must be genuinely NECESSARY for contract performance, not merely useful or efficient
- EDPB Guidelines 02/2019: Art 6(1)(b) should be interpreted strictly — "necessary" means the processing must be objectively necessary, not just helpful to the controller
- Basic scheduling: Yes, organising work shifts is necessary for the employment contract
- AI-powered analysis of performance + preferences: Goes BEYOND basic scheduling. Performance rating analysis for scheduling is NOT strictly necessary for shift allocation — a simpler system would suffice
- GDPR Art 6(1)(f): Legitimate interest may be more appropriate for the AI-enhanced features — but requires a balancing test considering employee privacy
- GDPR Art 88: Member State employment law may provide specific basis — many countries have works council requirements for AI scheduling tools
- AI Act Annex III(4)(b): If the AI monitors/evaluates employee performance as part of scheduling, it is HIGH-RISK
- GDPR Art 22: If scheduling decisions significantly affect the employee (e.g., always assigned undesirable shifts due to AI scoring), Art 22 protections apply
- Outcome: Art 6(1)(b) valid for BASIC scheduling. For AI features using performance data, Art 6(1)(f) legitimate interest (with balancing test) is more appropriate. Works council consultation may be required.

Expected Citations:
- GDPR Articles 6(1)(b), 6(1)(f), 22, 88
- EDPB Guidelines 02/2019 on Article 6(1)(b)
- EU AI Act Annex III Category 4(b)

Reasoning Path:
basic_scheduling → Art_6(1)(b) → contractual_necessity → VALID
performance_analysis → goes_BEYOND → strict_necessity → Art_6(1)(b)_insufficient
Art_6(1)(f) → legitimate_interest → for_AI_features → balancing_test_required
employee_performance → Annex_III_4(b) → HIGH_RISK → if_AI_evaluates
Art_88 → Member_State_law → works_council → may_be_required

================================================================================
CATEGORY 16: SECTOR-SPECIFIC AI APPLICATIONS (Cases 75-80)
================================================================================

=== CASE STUDY 75 ===
Difficulty: Medium
Category: Sector-Specific AI Applications
Scenario: A European energy utility deploys an AI system to manage smart grid electricity distribution. The system uses household-level energy consumption data (collected via smart meters every 15 minutes) to predict demand, optimise distribution, and detect energy theft. The system also identifies patterns correlating with occupancy (when residents are home or away).
Question: What GDPR and AI Act issues arise from AI-powered smart grid management?

Expected Answer Summary:
- GDPR Art 6(1)(e): Public interest — energy distribution management may rely on this where established by energy regulation
- GDPR Art 5(1)(c): Data minimisation — 15-minute granularity reveals highly detailed lifestyle patterns (when residents wake, cook, use devices). Aggregated hourly data may suffice for grid management
- GDPR Art 5(1)(b): Purpose limitation — data collected for energy billing/distribution, NOT for occupancy detection. Inferring when people are home is a separate purpose
- GDPR Art 35: DPIA required — systematic monitoring of household behaviour at scale
- GDPR Art 25(1): Data protection by design — smart meter data should be aggregated/anonymised at the earliest possible point
- ePrivacy Directive: Smart meter data on user behaviour may fall under electronic communications privacy rules
- AI Act Annex III(2): HIGH-RISK — AI as safety component in the management of critical infrastructure (energy/electricity supply under Art 6(1))
- AI Act Art 9: Risk management must address grid failure risks from AI errors
- Energy theft detection: May be justified by legitimate interest, but proportionality assessment required
- Outcome: HIGH-RISK AI system. Data minimisation critical. Occupancy inference is a separate purpose requiring its own legal basis. DPIA mandatory.

Expected Citations:
- GDPR Articles 5(1)(b)(c), 6(1)(e), 25(1), 35
- EU AI Act Articles 6(1), 9, Annex III Category 2

Reasoning Path:
smart_meter_data → 15_min_granularity → reveals → lifestyle_patterns → Art_5(1)(c)
occupancy_inference → separate_purpose → Art_5(1)(b) → needs_own_basis
energy_grid_AI → critical_infrastructure → Annex_III_2 → HIGH_RISK
DPbD → Art_25(1) → aggregate_at_earliest_point → before_transmission

=== CASE STUDY 76 ===
Difficulty: Hard
Category: Sector-Specific AI Applications
Scenario: A European pharmaceutical company uses an AI system to analyse adverse drug reaction (ADR) reports submitted by patients and healthcare professionals. The system processes patient medical histories, medication details, and symptom descriptions to identify potential safety signals. The AI automatically generates safety reports submitted to the European Medicines Agency (EMA).
Question: What GDPR and AI Act compliance issues arise from AI-driven pharmacovigilance?

Expected Answer Summary:
- Legal obligation: EU Pharmacovigilance legislation (Regulation (EU) 1235/2010, Directive 2001/83/EC) REQUIRES companies to monitor adverse reactions — this establishes a LEGAL OBLIGATION basis
- GDPR Art 6(1)(c): Legal obligation — pharmaceutical companies are legally required to process ADR data, providing a clear legal basis
- GDPR Art 9(2)(i): Processing necessary for public health — safety of medicinal products qualifies
- GDPR Art 9(2)(h): Healthcare processing with professional secrecy obligations
- GDPR Art 14: Where ADR reports come from healthcare professionals (not directly from patients), Art 14 transparency obligations apply to patients
- AI Act Annex III(5)(a): Potentially HIGH-RISK — AI evaluating health-related information to assess safety signals
- AI Act Art 9: Risk management — incorrect AI safety signal identification could either: (i) miss a genuine safety issue (false negative — patient harm), or (ii) trigger unnecessary drug withdrawal (false positive — patient access harm)
- AI Act Art 14: Human oversight — AI-generated safety reports to EMA must be reviewed and validated by qualified pharmacovigilance officers
- GDPR Art 35: DPIA required — large-scale health data processing for a purpose beyond individual treatment
- Outcome: Lawful and often legally required. But: AI outputs must have human oversight, DPIAs required, risk management must address both false positive and false negative risks.

Expected Citations:
- GDPR Articles 6(1)(c), 9(2)(h)(i), 14, 35
- EU AI Act Articles 9, 14, Annex III Category 5(a)
- Regulation (EU) 1235/2010 (Pharmacovigilance)

Reasoning Path:
pharmacovigilance → legal_obligation → Art_6(1)(c) → clear_basis
ADR_data → health_data → Art_9 → Art_9(2)(i)_public_health
AI_safety_signals → false_negative → missed_harm → Art_9_risk_management
AI_generated_reports → Art_14 → human_review → by_qualified_pharmacovigilance_officer
patient_not_informed → Art_14 → transparency_to_data_subjects

=== CASE STUDY 77 ===
Difficulty: Medium
Category: Sector-Specific AI Applications
Scenario: A European EdTech company develops an AI tutoring system that adapts to individual student learning styles. The system tracks eye movements (via webcam), typing speed, response times, and emotional engagement to optimise lesson delivery. Universities adopt the system for 200,000 students across the EU.
Question: What specific GDPR and AI Act requirements apply to AI-powered adaptive learning at scale?

Expected Answer Summary:
- AI Act Annex III(3)(a): HIGH-RISK — AI used in educational or vocational training to determine access to education or evaluate students
- AI Act Art 9: Risk management — must address risks of: (i) AI misjudging learning styles leading to poor education, (ii) bias against certain learning patterns, (iii) eye tracking creating surveillance pressure
- AI Act Art 5(1)(f): Eye movement analysis for emotional engagement = EMOTION RECOGNITION in education — potentially PROHIBITED in education context if it infers emotions
- AI Act exception check: Art 5(1)(f) exception — "medical or safety reasons" — optimising lesson delivery does NOT qualify
- GDPR Art 9: Eye-tracking biometric data if used for identification; emotional state inference = health-related data (special category)
- GDPR Art 25(2): Data protection by default — most privacy-protective settings as default. Eye tracking should be OPT-IN, not default
- GDPR Art 35: DPIA mandatory — 200,000 students, systematic monitoring, biometric/special category data possible
- GDPR Art 5(1)(c): Data minimisation — eye tracking and emotional engagement monitoring may be excessive for adaptive learning; simpler signals (quiz performance, time-on-task) may suffice
- Outcome: Eye/emotion tracking component likely PROHIBITED under AI Act Art 5(1)(f). Adaptive learning based on academic performance is lawful but high-risk. DPIA mandatory.

Expected Citations:
- GDPR Articles 5(1)(c), 9, 25(2), 35
- EU AI Act Articles 5(1)(f), 9, Annex III Category 3(a)

Reasoning Path:
adaptive_learning → Annex_III_3(a) → HIGH_RISK → education_evaluation
eye_tracking + emotional_engagement → emotion_recognition → Art_5(1)(f) → POTENTIALLY_PROHIBITED
exception_check → medical_or_safety → NOT_applicable → lesson_optimisation
biometric_data → Art_9 → special_category → heightened_protection
200K_students → Art_35 → DPIA_mandatory → large_scale

=== CASE STUDY 78 ===
Difficulty: Easy
Category: Sector-Specific AI Applications
Scenario: A European insurance company uses an AI system to process motor vehicle accident claims. The system analyses photos of vehicle damage, repair cost databases, and policy terms to generate settlement offers within 24 hours. Claimants can accept the AI-generated offer or request human review.
Question: What are the GDPR and AI Act requirements for this AI claims processing system?

Expected Answer Summary:
- GDPR Art 22(1): AI-generated settlement offers = automated decisions with financial effects. BUT: the option for human review satisfies Art 22(2)(a) (consent) or Art 22(3) (right to human intervention)
- GDPR Art 13(2)(f): Must inform claimants that the initial offer is AI-generated and explain the logic (what factors determine the offer amount)
- GDPR Art 15(1)(h): Claimants have right to access information about the automated decision-making logic
- AI Act Annex III(5)(c): HIGH-RISK — AI for claim assessment and pricing in insurance for natural persons
- AI Act Art 14: Human oversight — option for human review satisfies this (good practice already in place)
- AI Act Art 13: Transparency to deployer — insurance adjusters reviewing AI decisions must understand the model's basis
- AI Act Art 9: Risk management — must address: under-settlement (harm to claimant), over-settlement (insurer loss), and systematic bias in damage assessment
- GDPR Art 6(1)(b): Contractual necessity — processing claims under the insurance contract
- Outcome: Well-designed system. Human review option satisfies both GDPR Art 22 and AI Act Art 14. Must ensure transparency and proper risk management. HIGH-RISK classification.

Expected Citations:
- GDPR Articles 6(1)(b), 13(2)(f), 15(1)(h), 22
- EU AI Act Articles 9, 13, 14, Annex III Category 5(c)

Reasoning Path:
ai_claims_processing → Annex_III_5(c) → HIGH_RISK → insurance_assessment
settlement_offer → automated_decision → Art_22 → BUT → human_review_available → SATISFIES
human_review_option → SATISFIES → Art_14 + Art_22(3) → good_design
Art_13(2)(f) → must_inform → AI_generated_offer → explain_logic

=== CASE STUDY 79 ===
Difficulty: Hard
Category: Sector-Specific AI Applications
Scenario: A European agricultural cooperative deploys an AI-powered precision farming system that uses satellite imagery, drone footage, soil sensors, and weather data to optimise crop management. However, the drone footage captures neighbouring farms and public roads, processing images of people and vehicles. The system also uses farmer profile data (farm size, revenue, debt levels, crop history) to recommend financial products (loans, insurance).
Question: Map the full GDPR and AI Act requirements for the precision farming AI system.

Expected Answer Summary:
Component 1 — Crop management AI:
- AI Act: Agricultural AI NOT explicitly listed in Annex III — likely NOT high-risk for crop management
- GDPR: Satellite/sensor data about soil and weather = NOT personal data. No GDPR issue for this component

Component 2 — Drone footage:
- GDPR Art 6: Capturing images of neighbouring properties and public roads — processing personal data (identifiable persons, licence plates). Need legal basis — Art 6(1)(f) legitimate interest with strong balancing test
- GDPR Art 5(1)(c): Data minimisation — must implement geofencing or automatic blurring for areas outside the cooperative's land
- GDPR Art 14: Neighbours whose data is incidentally captured must be informed
- GDPR Art 35: DPIA may be required — systematic drone surveillance of an area
- AI Act Art 50(3): If the AI uses biometric categorisation from drone footage, disclosure required

Component 3 — Financial product recommendations:
- GDPR Art 22: If AI recommendations influence loan/insurance decisions, automated decision-making rules apply
- AI Act Annex III(5)(b)(c): If the AI assesses creditworthiness or insurance risk based on farmer data, HIGH-RISK
- GDPR Art 5(1)(b): Purpose limitation — crop management data repurposed for financial recommendations is a NEW purpose

- Outcome: Multi-layered. Crop AI = low risk. Drone surveillance = GDPR compliance needed. Financial recommendations = potentially HIGH-RISK AI + GDPR Art 22.

Expected Citations:
- GDPR Articles 5(1)(b)(c), 6(1)(f), 14, 22, 35
- EU AI Act Articles 50(3), Annex III Categories 5(b), 5(c)

Reasoning Path:
crop_management → satellite + sensors → NOT_personal_data → no_GDPR
drone_footage → captures → neighbours_and_roads → personal_data → Art_6(1)(f)
geofencing + blurring → Art_5(1)(c) → DPbD_measures
financial_recommendations → farmer_profile → credit/insurance → Annex_III_5(b)(c) → HIGH_RISK
purpose_limitation → crop_data → repurposed → financial_products → Art_5(1)(b) → violation

=== CASE STUDY 80 ===
Difficulty: Medium
Category: Sector-Specific AI Applications
Scenario: A European telecom operator deploys an AI system that analyses customer call records (CDRs), browsing patterns, app usage data, and location data to predict customer churn. Customers identified as "high churn risk" receive targeted retention offers (discounts, upgrades). The system processes data of 30 million subscribers.
Question: What GDPR requirements apply to AI-driven customer churn prediction and targeted retention?

Expected Answer Summary:
- GDPR Art 6(1)(f): Legitimate interest — churn prediction and retention marketing may rely on this, but requires balancing test given the breadth of data (call records, browsing, location)
- GDPR Art 5(1)(c): Data minimisation — analysing browsing patterns AND location data AND call records is extremely invasive. Each data type must be justified as necessary for churn prediction
- GDPR Art 21(1): Right to object to profiling based on legitimate interest — must be prominently communicated to customers
- GDPR Art 21(2): If the retention offers constitute "direct marketing," the RIGHT TO OBJECT IS ABSOLUTE
- GDPR Art 13(2)(f): Must inform customers about the profiling and automated aspects of churn prediction
- GDPR Art 35: DPIA mandatory — large-scale profiling of 30 million subscribers
- ePrivacy Directive Art 5(3): Accessing device-level data (app usage, browsing patterns) requires consent — cannot rely on GDPR legitimate interest alone for ePrivacy-covered data
- ePrivacy Directive Art 6: Traffic data (CDRs) processing beyond what is necessary for billing requires consent
- GDPR Art 22: If churn score leads to automated pricing decisions (different offers for different customers), Art 22 may apply
- Outcome: GDPR legitimate interest possible for basic churn prediction but ePrivacy consent required for CDRs, browsing, and app data. Must provide opt-out. DPIA mandatory.

Expected Citations:
- GDPR Articles 5(1)(c), 6(1)(f), 13(2)(f), 21(1)(2), 22, 35
- ePrivacy Directive Articles 5(3), 6

Reasoning Path:
churn_prediction → profiling → 30M_subscribers → Art_35 → DPIA_mandatory
call_records + browsing → ePrivacy_Art_5(3) + Art_6 → CONSENT_required
legitimate_interest → Art_6(1)(f) → balancing_test → invasive_data → difficult
retention_marketing → Art_21(2) → absolute_right_to_object → direct_marketing
data_minimisation → Art_5(1)(c) → each_data_type → must_justify_separately

================================================================================
CATEGORY 17: AI GOVERNANCE & COMPLIANCE FRAMEWORKS (Cases 81-85)
================================================================================

=== CASE STUDY 81 ===
Difficulty: Hard
Category: AI Governance & Compliance Frameworks
Scenario: A large European financial group (bank, insurance arm, and wealth management division) wants to establish a unified AI governance framework covering all AI systems deployed across the group. They currently have 47 AI systems in production: 12 are high-risk under the AI Act, 30 involve GDPR-regulated personal data processing, and 5 are purely internal analytics with no personal data.
Question: What elements should a comprehensive GDPR + AI Act governance framework include, and how should responsibilities be allocated?

Expected Answer Summary:
- AI Act Art 17: Quality Management System (QMS) — required for ALL providers of high-risk AI. Must include: policies for regulatory compliance, data management, risk management, post-market monitoring, communication with authorities
- AI Act Art 9: Risk management system — continuous process throughout the lifecycle of each high-risk AI system
- GDPR Art 37-39: Data Protection Officer (DPO) — mandatory for large-scale processing. DPO role should integrate AI oversight
- GDPR Art 30: Records of processing activities — must include AI-related processing operations
- AI Act Art 26: Deployer obligations — each business division deploying high-risk AI must maintain usage logs, conduct monitoring, and report
- Framework elements:
  (1) AI inventory/registry: Catalogue all 47 systems with risk classification
  (2) Role allocation: AI Officer (Art 17 compliance), DPO (GDPR compliance), Chief Risk Officer (risk management overlap)
  (3) Conformity assessment pipeline: Standardised process for new AI systems before deployment
  (4) DPIA + AI risk management integration: Single assessment combining GDPR Art 35 DPIA and AI Act Art 9 risk management
  (5) Human oversight framework: Define who reviews AI outputs for each high-risk system (Art 14)
  (6) Incident response: Integrated procedure for data breaches (Art 33 GDPR) and AI incidents (Art 62 AI Act)
  (7) Training: Staff awareness of both GDPR and AI Act obligations
  (8) Audit trail: Logging and documentation for all high-risk AI systems (Art 12 AI Act)
- Outcome: Integrated governance framework that addresses both regulations simultaneously, avoiding siloed compliance.

Expected Citations:
- GDPR Articles 30, 33, 35, 37-39
- EU AI Act Articles 9, 12, 14, 17, 26, 62

Reasoning Path:
47_AI_systems → inventory → risk_classification → FIRST_STEP
12_high_risk → AI_Act_Art_17 → QMS_required
30_with_personal_data → GDPR_compliance → DPO + DPIA + Art_30
integrated_framework → DPIA + Art_9_risk_management → combined_assessment
role_allocation → AI_Officer + DPO + CRO → clear_responsibilities
incident_response → Art_33_GDPR + Art_62_AI_Act → unified_procedure

=== CASE STUDY 82 ===
Difficulty: Medium
Category: AI Governance & Compliance Frameworks
Scenario: A European high-risk AI system provider must conduct a conformity assessment before placing its credit scoring system on the market. The system uses personal financial data, employment information, and age to predict loan default probability.
Question: What does the AI Act conformity assessment process involve for this high-risk AI system?

Expected Answer Summary:
- AI Act Art 43(1): For credit scoring (Annex III(5)(b)), the provider conducts a SELF-ASSESSMENT (internal conformity procedure under Annex VI) — no third-party notified body required
- AI Act Annex VI: Internal conformity assessment requires:
  (1) QMS established per Art 17
  (2) Technical documentation per Annex IV — system description, design specifications, development process, risk management details, training/testing data description
  (3) Testing: System tested against accuracy, robustness, and cybersecurity benchmarks (Art 15)
  (4) Bias testing: Examination of training data for biases (Art 10) — age and employment data may encode discriminatory patterns
  (5) Human oversight measures documented (Art 14)
  (6) Logging capabilities confirmed (Art 12)
- AI Act Art 47: EU Declaration of Conformity — provider issues written declaration that the system meets all Chapter III requirements
- AI Act Art 49: CE marking — must affix CE mark before placing on market
- AI Act Art 16: Post-market monitoring system must be established
- GDPR integration: DPIA (Art 35) should be conducted IN PARALLEL with AI Act conformity assessment — many elements overlap
- Outcome: Self-assessment conformity procedure. Provider documents compliance with all Chapter III requirements, issues declaration, affixes CE mark, and establishes post-market monitoring.

Expected Citations:
- EU AI Act Articles 16, 43(1), 47, 49, Annex IV, Annex VI
- GDPR Article 35

Reasoning Path:
credit_scoring → Annex_III_5(b) → Art_43(1) → self_assessment → Annex_VI
Annex_VI → QMS + technical_docs + testing + bias_audit + human_oversight + logging
Art_47 → EU_Declaration_of_Conformity → written_declaration
Art_49 → CE_marking → before_market_placement
Art_16 → post_market_monitoring → ONGOING
DPIA → Art_35 → parallel_with → conformity_assessment

=== CASE STUDY 83 ===
Difficulty: Easy
Category: AI Governance & Compliance Frameworks
Scenario: A European company purchases a high-risk AI system from a provider for use in employee performance evaluation. The provider conducted a conformity assessment and provided instructions for use. The company (deployer) wants to understand its specific obligations.
Question: What are the deployer's obligations under the AI Act for a high-risk AI system?

Expected Answer Summary:
- AI Act Art 26(1): Use the system IN ACCORDANCE with the provider's instructions of use
- AI Act Art 26(2): Assign human oversight to competent, trained, and authorised individuals
- AI Act Art 26(3): Ensure input data is relevant and sufficiently representative for the intended purpose
- AI Act Art 26(4): Monitor operation and report to provider/authority if risks identified
- AI Act Art 26(5): Maintain logs automatically generated by the system for at least 6 months (or as specified by EU/Member State law)
- AI Act Art 26(6): Conduct a DPIA when required by GDPR Art 35 — deployer responsibility
- AI Act Art 26(7): Cooperate with competent authorities
- AI Act Art 26(8): Inform affected individuals (employees) that they are subject to a high-risk AI system — BEFORE the system is first applied
- AI Act Art 27: Fundamental rights impact assessment — required before deployment by deployers that are public bodies or private entities providing public services (may apply depending on company size/sector)
- GDPR Art 35: DPIA under GDPR — deployer (as controller) conducts this independently of the provider's conformity assessment
- Outcome: Deployer has significant independent obligations. Cannot simply rely on provider's conformity assessment. Must train oversight staff, monitor system, maintain logs, and inform employees.

Expected Citations:
- EU AI Act Articles 26(1)-(8), 27
- GDPR Article 35

Reasoning Path:
deployer → purchases → high_risk_AI → provider_completed → conformity_assessment
BUT → deployer_has → OWN_obligations → Art_26(1)-(8)
Art_26(2) → human_oversight → competent_trained_persons → deployer_responsibility
Art_26(5) → maintain_logs → minimum_6_months
Art_26(8) → inform_employees → BEFORE_first_use
GDPR_Art_35 → DPIA → deployer_responsibility → independent_of_provider

=== CASE STUDY 84 ===
Difficulty: Hard
Category: AI Governance & Compliance Frameworks
Scenario: A European AI company that developed a high-risk biometric identification system discovers a significant accuracy issue 8 months after deployment — the system's false positive rate for certain ethnic groups is 10x higher than for others. Multiple deployers across the EU are using the system. Some deployers have reported incidents to the provider.
Question: What are the post-market monitoring and incident reporting obligations?

Expected Answer Summary:
- AI Act Art 72: Post-market monitoring system MUST be established by the provider — proportionate to the nature and risks of the system. Should have detected bias earlier
- AI Act Art 72(3): Post-market monitoring plan must include analysis of interaction with other AI systems and feedback from deployers — deployer incident reports should have triggered investigation
- AI Act Art 73(1): SERIOUS INCIDENT reporting — provider must report to market surveillance authorities of Member States where the incident occurred. This bias issue constitutes a serious incident if it led to discrimination
- AI Act Art 73(4): Report within 15 DAYS of provider becoming aware of a serious incident (or 2 days if risk to health/safety/fundamental rights)
- AI Act Art 73(5): Must notify all deployers of the affected system
- AI Act Art 20: Corrective actions — provider must take immediate corrective action: (i) inform all deployers, (ii) issue system update addressing bias, (iii) if not fixable, withdraw/recall system
- AI Act Art 16(j): Provider must ensure corrective actions are taken when system does not conform to requirements
- GDPR implications: If biased decisions affected individuals (e.g., false identifications), GDPR Art 33 data breach notification may also be triggered. Art 82 — affected individuals have right to compensation
- Outcome: Immediate incident reporting to authorities. Notify all deployers. Take corrective action or withdraw. Potential liability for discriminatory outcomes.

Expected Citations:
- EU AI Act Articles 16(j), 20, 72, 73(1)(4)(5)
- GDPR Articles 33, 82

Reasoning Path:
accuracy_issue → 10x_higher_FP_for_ethnic_groups → SERIOUS_INCIDENT
Art_72 → post_market_monitoring → should_have_detected_earlier
Art_73(1) → serious_incident_report → to_MSA → within_15_days
Art_73(5) → notify_ALL_deployers → across_EU
Art_20 → corrective_actions → update_or_withdraw
GDPR_Art_82 → affected_individuals → right_to_compensation

=== CASE STUDY 85 ===
Difficulty: Medium
Category: AI Governance & Compliance Frameworks
Scenario: A European regulatory sandbox participant (an AI startup) is developing a novel AI system for predicting judicial outcomes. The system analyses past court decisions, legal arguments, and judge-specific patterns to predict case outcomes for commercial litigation clients. The startup is testing within a Member State's AI regulatory sandbox under Art 57.
Question: What benefits and limitations does the regulatory sandbox provide?

Expected Answer Summary:
- AI Act Art 57: Member States must establish at least one AI regulatory sandbox by 2 August 2026 — provides controlled environment for developing and testing innovative AI before market entry
- AI Act Art 57(1): Sandbox provides regulatory guidance from competent authorities during development
- AI Act Art 57(5): Sandbox participants are NOT exempt from GDPR, AI Act, or other EU law — sandbox provides GUIDANCE, not exemptions
- AI Act Art 57(9): Personal data may be processed in the sandbox for AI development subject to specific safeguards: (i) informed consent or other lawful basis, (ii) data anonymised/pseudonymised, (iii) appropriate access controls, (iv) data deleted after sandbox period
- AI Act Art 62: Sandboxes must prioritise access for SMEs and startups
- AI Act Art 57(13): Processing within sandbox must be proportionate and subject to supervisory authority oversight
- Judicial outcome prediction: This AI system may be HIGH-RISK under Annex III(8)(a) — AI assisting judicial authorities. But if used by lawyers (not courts), classification may differ
- GDPR: Past court decisions may contain personal data — names of parties, witnesses. Art 6(1)(f) legitimate interest or Art 9(2)(f) (data manifestly made public in court proceedings) may apply
- Outcome: Sandbox provides guidance and controlled testing, NOT compliance exemptions. GDPR and AI Act fully apply. Startup benefits from regulatory engagement and clarity before market entry.

Expected Citations:
- EU AI Act Articles 57, 62
- Annex III Category 8(a)
- GDPR Articles 6(1)(f), 9(2)(f)

Reasoning Path:
regulatory_sandbox → Art_57 → controlled_testing_environment
NOT_exempt → from_GDPR_or_AI_Act → guidance_only → Art_57(5)
judicial_prediction → Annex_III_8(a) → IF_assisting_courts → HIGH_RISK
BUT → used_by_lawyers → classification_may_differ
court_decisions → personal_data → names_of_parties → Art_9(2)(f) → manifestly_public
sandbox_benefits → regulatory_guidance + testing_environment + priority_SME_access

================================================================================
CATEGORY 18: EMERGING TECH & NOVEL SCENARIOS (Cases 86-88)
================================================================================

=== CASE STUDY 86 ===
Difficulty: Hard
Category: Emerging Tech & Novel Scenarios
Scenario: A European company develops an AI-powered digital twin of a hospital. The digital twin simulates patient flows, resource allocation, and treatment outcomes using real patient data (demographics, diagnoses, treatment histories) from the actual hospital. The digital twin is used to: (1) test new operational procedures before real-world implementation, (2) train junior doctors using simulated patient scenarios, and (3) share the simulation with a US pharmaceutical company for drug trial modelling.
Question: What GDPR and AI Act requirements apply to AI digital twins built on real patient data?

Expected Answer Summary:
- GDPR Art 9: Patient data = health data (special category) — EVERY use requires an Art 9(2) exception
- Component 1 — Operational testing:
  - GDPR Art 9(2)(h): Healthcare management may apply if done by health professionals
  - GDPR Art 5(1)(b): Compatible purpose with original treatment — but must pass Art 6(4) compatibility test
  - Should use PSEUDONYMISED data — Art 89(1) safeguards
- Component 2 — Training junior doctors:
  - GDPR Art 9(2)(h): Medical training qualifies as healthcare purpose
  - BUT: Simulated patient scenarios based on REAL patients — data minimisation requires using synthetic patients where possible
  - AI Act Annex III(3)(a): If AI evaluates/assesses trainees based on their interaction with the digital twin, HIGH-RISK
- Component 3 — US pharmaceutical sharing:
  - GDPR Art 44: International transfer to US — Chapter V compliance required
  - GDPR Art 9: No Art 9 exception for sharing health data with a pharmaceutical company for commercial purposes without explicit consent
  - Solution: Anonymise or use synthetic data before sharing. If truly anonymised, GDPR does not apply to the shared data
- Overall: DPIA mandatory (Art 35). Data protection by design requires pseudonymisation throughout (Art 25(1)). The digital twin architecture should separate identifiable data from simulation logic.
- Outcome: Lawful for components 1-2 with safeguards. Component 3 requires anonymisation or explicit consent + transfer mechanisms. DPIA mandatory.

Expected Citations:
- GDPR Articles 5(1)(b), 9(2)(h), 25(1), 35, 44, 89(1)
- EU AI Act Annex III Category 3(a)

Reasoning Path:
digital_twin → built_on → real_patient_data → Art_9 → special_category
operational_testing → Art_9(2)(h) → healthcare_management → WITH → pseudonymisation
doctor_training → Art_9(2)(h) → healthcare_training → prefer_synthetic_patients
US_pharma_sharing → Art_44 → Chapter_V + Art_9 → needs_consent_or_anonymisation
DPbD → Art_25(1) → separate → identifiable_data → from → simulation_logic

=== CASE STUDY 87 ===
Difficulty: Hard
Category: Emerging Tech & Novel Scenarios
Scenario: A European tech company develops a brain-computer interface (BCI) that uses AI to interpret neural signals for controlling assistive devices (wheelchair, prosthetic limb). The system processes raw neural data, learns individual brain patterns over time, and adapts its responses to each user. The company also wants to use aggregated neural data to improve the AI model for future users.
Question: What novel GDPR and AI Act issues arise from AI systems processing neural data?

Expected Answer Summary:
- GDPR Art 9: Neural data = HEALTH DATA (special category) as it reveals information about an individual's neurological state. Also potentially BIOMETRIC DATA if neural patterns can uniquely identify individuals
- GDPR Art 9(2)(h): For assistive device control — healthcare purpose under professional supervision may apply
- GDPR Art 9(2)(a): Explicit consent required for non-medical uses (model improvement)
- GDPR Art 5(1)(c): Data minimisation — raw neural data is extremely granular. Must process only the signal features necessary for device control, not full neural recordings
- GDPR Art 25(1): Data protection by design — on-device preprocessing to extract only relevant features before any data leaves the BCI device
- AI Act classification: BCI as assistive medical device → Regulation (EU) 2017/745 (MDR) → AI Act Art 6(1) → HIGH-RISK (safety component of medical device listed in Annex I)
- AI Act Art 9: Risk management — catastrophic if AI misinterprets neural signals (wheelchair moves unintended direction, prosthetic grip fails). HIGHEST safety standards
- AI Act Art 10: Data governance for training data — neural data is highly individual; model trained on one user may not generalise safely
- Emerging regulation: EU proposed regulation on neurorights and neural data protection — even stronger protections than GDPR may apply in future
- Model improvement: Must be fully anonymised or require explicit consent. Neural patterns may be uniquely identifying — true anonymisation extremely difficult
- Outcome: HIGHEST protection required. Special category data. High-risk medical device AI. Data protection by design critical. Aggregation for model improvement requires explicit consent due to identification risk.

Expected Citations:
- GDPR Articles 5(1)(c), 9, 9(2)(a)(h), 25(1)
- EU AI Act Articles 6(1), 9, 10, Annex I(11)
- Regulation (EU) 2017/745 (MDR)

Reasoning Path:
neural_data → health_data + potential_biometric → Art_9 → HIGHEST_protection
BCI_assistive_device → medical_device → MDR_2017/745 → Annex_I(11) → Art_6(1) → HIGH_RISK
misinterpretation_risk → Art_9 → risk_management → safety_critical
DPbD → Art_25(1) → on_device_preprocessing → extract_features_only
model_improvement → neural_patterns → uniquely_identifying → anonymisation_very_difficult → explicit_consent

=== CASE STUDY 88 ===
Difficulty: Hard
Category: Emerging Tech & Novel Scenarios
Scenario: A European consortium develops a decentralised AI system using blockchain for model governance. Multiple hospitals contribute to training a federated medical AI model — each hospital trains locally and shares only model updates (gradients) via a blockchain ledger. The blockchain immutably records all model updates, training metadata (timestamps, hospital identifiers, dataset sizes), and performance metrics. A patient at one hospital requests erasure of their data under Art 17.
Question: How do GDPR erasure rights interact with blockchain immutability and federated AI learning?

Expected Answer Summary:
- GDPR Art 17(1): Right to erasure — patient can request deletion of personal data. Hospital must delete the patient's records from its local training dataset
- Federated learning advantage: Patient data NEVER left the hospital — only model gradients were shared. This is a DPbD win
- Model gradients: Recent research shows gradients CAN leak individual data (gradient inversion attacks). If gradients contain personal data, they are subject to GDPR
- Blockchain immutability: Model updates recorded on blockchain CANNOT be deleted. This creates tension with Art 17
- GDPR Art 17(1) vs blockchain: If model gradients on the blockchain constitute personal data (because they can be used to reconstruct patient information), the immutability of blockchain CONFLICTS with erasure rights
- Solutions:
  (1) Ensure gradients DO NOT contain personal data — apply differential privacy with sufficient noise to prevent gradient inversion
  (2) Off-chain storage: Store gradients off-chain with references on-chain; delete off-chain data on erasure request
  (3) Chameleon blockchain: Use hash-based references that can be updated to point to null data
  (4) Machine unlearning: Retrain the model excluding the patient's data, and record the updated model on-chain
- GDPR Art 25(1): DPbD requires designing the blockchain/federated system architecture to ACCOMMODATE erasure from the start
- GDPR Art 5(1)(e): Storage limitation — blockchain stores data forever, which conflicts with this principle
- AI Act Art 10: Data governance requires mechanisms to address data quality issues including erasure requests in training data
- Outcome: Federated learning is privacy-positive. But blockchain immutability creates serious GDPR tension. Must use differential privacy on gradients and off-chain storage patterns. Pure on-chain gradient storage is likely GDPR non-compliant.

Expected Citations:
- GDPR Articles 5(1)(e), 17(1), 25(1)
- EU AI Act Article 10

Reasoning Path:
federated_learning → patient_data_stays_local → DPbD_advantage
BUT → gradients → may_leak → individual_data → gradient_inversion_attacks
blockchain → immutable → CANNOT_delete → Art_17_tension
solution_1 → differential_privacy → noise → prevents_gradient_inversion
solution_2 → off_chain_storage → deletable → on_chain_references_only
Art_25(1) → DPbD → design_for_erasure → from_architecture_start
Art_5(1)(e) → storage_limitation → blockchain_forever → CONFLICTS

================================================================================
END OF COMPLIANCE CASE STUDIES
================================================================================
Summary:
- Total case studies: 88
- Category 1 (Prohibited AI Practices): Cases 1-5
- Category 2 (High-Risk AI): Cases 6-10
- Category 3 (Automated Decision-Making): Cases 11-15
- Category 4 (Data Subject Rights): Cases 16-20
- Category 5 (International Transfers): Cases 21-24
- Category 6 (Special Category Data): Cases 25-29
- Category 7 (Scope Questions): Cases 30-33
- Category 8 (Cross-Regulation Overlap): Cases 34-38
- Category 9 (GPAI & Foundation Models): Cases 39-44
- Category 10 (Transparency & Explainability): Cases 45-49
- Category 11 (Children's Data & Vulnerable Groups): Cases 50-54
- Category 12 (Enforcement & Penalties): Cases 55-59
- Category 13 (Data Protection by Design & Default): Cases 60-64
- Category 14 (Controller-Processor Relations in AI): Cases 65-69
- Category 15 (Consent & Legal Basis): Cases 70-74
- Category 16 (Sector-Specific AI Applications): Cases 75-80
- Category 17 (AI Governance & Compliance Frameworks): Cases 81-85
- Category 18 (Emerging Tech & Novel Scenarios): Cases 86-88
- Difficulty distribution: Easy (16), Medium (37), Hard (35)
- Each case includes: Scenario, Question, Expected Answer Summary, Expected Citations, Reasoning Path


---


## SOURCE: `docs/archive/data_scraper_README.md`



---


## SOURCE: `docs/archive/data_scraper_annex_format.md`

DATA SET 4: EU AI Act Annexes (Full Text)
Source: Same EUR-Lex link as AI Act

What I need: Full text of Annexes I, III, IV, VI, VII, VIII.

Format:

=== ANNEX I ===
Title: List of Union harmonisation legislation
Section A:
1. Directive 2006/42/EC...
2. ...

=== ANNEX III ===
Title: High-risk AI systems referred to in Article 6(2)
1. Biometrics:
   (a) AI systems intended to be used for...
   (b) ...
2. Critical infrastructure:
   (a) ...
3. Education and vocational training:
   (a) ...
...all 8 categories with sub-items...

=== ANNEX IV ===
Title: Technical documentation referred to in Article 11
1. A general description of the AI system including:
   (a) its intended purpose...
   (b) ...
File name: ai_act_annexes.txt

---


## SOURCE: `docs/archive/data_scraper_format.md`

## DATA SET 8: Compliance Case Studies (LLM-Generated)

**What I need**: 30-40 realistic compliance scenario questions with expected answers. These will be used to test the knowledge graph reasoning.

**You can generate these with an LLM.** Use this format:

```
=== CASE STUDY 1 ===
Difficulty: Medium
Scenario: A European bank wants to use an AI system to automatically reject loan applications based on credit scoring. The system uses personal financial data and produces legally binding decisions without human review.
Question: What are the combined GDPR and EU AI Act compliance requirements?

Expected Answer Summary:
- GDPR Art 22: Automated decision-making prohibition applies — must provide human intervention
- GDPR Art 35: DPIA required (automated profiling with legal effects)
- GDPR Art 6: Need lawful basis (likely Art 6(1)(b) contract or Art 6(1)(f) legitimate interest)
- AI Act Art 6 + Annex III(5)(a): Credit scoring is HIGH-RISK AI
- AI Act Art 14: Human oversight required for high-risk AI
- AI Act Art 13: Transparency and information to deployer required
- Cumulative: Both DPIA and conformity assessment needed

Expected Citations:
- GDPR Articles 6, 22, 35
- EU AI Act Articles 6, 9, 13, 14, 26
- Annex III Category 5(a)

Reasoning Path:
credit_scoring → CLASSIFIED_AS → high_risk → REQUIRES → conformity_assessment
credit_scoring → TRIGGERS → GDPR_ART_22 → HAS_EXCEPTION → contract_necessity → HAS_CONDITION → human_intervention
credit_scoring → TRIGGERS → GDPR_ART_35 → REQUIRES → dpia
```

**Categories of scenarios to cover** (3-5 each):
1. **Prohibited AI practices** — social scoring, manipulation, biometric identification
2. **High-risk AI** — hiring, credit scoring, law enforcement, healthcare
3. **Automated decision-making** — profiling, credit, insurance, hiring
4. **Data subject rights** — access, erasure, portability with AI systems
5. **International transfers** — AI models trained on EU data, cloud processing
6. **Special category data** — health AI, biometric systems, political profiling
7. **Scope questions** — does GDPR/AI Act apply? Household, military, research
8. **Cross-regulation overlap** — where both GDPR and AI Act apply simultaneously

**File name**: `compliance_case_studies.txt`

---


## SOURCE: `docs/archive/data_scraper_recital_format.md`

DATA SET 3: Key GDPR Recitals
Source: Same EUR-Lex link as GDPR

What I need: Full text for the 50 most important recitals (not all 173).

Format:

=== RECITAL 1 ===
The protection of natural persons in relation to the processing...

=== RECITAL 4 ===
The processing of personal data should be designed to serve...

=== RECITAL 26 ===
The principles of data protection should apply to any information...
Priority recitals (these are the most cited in case law and guidance):

---


---

# Run: docs/ (absorbed at archive)

---


## SOURCE: `docs/README.md`

# AlloyCode — Project Overview & System Architecture

**Last updated:** 2026-04-13
**Status:** Phase 1 (active) — pivoting from free-text assessment to static repo compliance scanning

---

## 1. What it is

AlloyCode is a **static compliance scanner for AI codebases** that maps detected code patterns to concrete EU AI Act and GDPR obligations. Point it at a GitHub repo; it returns a report of likely regulatory violations with **file:line anchors** and article citations.

Two entrypoints:

1. **Web UI** — paste a GitHub URL, run a one-shot scan, read the findings report.
2. **VS Code extension** (Phase 3) — scans on save / commit / schedule, surfaces findings as editor diagnostics.

---

## 2. Why this exists (and why the old direction was wrong)

**The old direction (shipped, now being retired):** user types a free-text description of their AI system into a form; five agents classify it against the EU AI Act. This had three fatal portfolio problems:

- Input is vibes — the user can be vague, wrong, or dishonest. The classifier has no ground truth.
- Every demo looks the same: a textbox, a loading spinner, a markdown report.
- No differentiator vs. any LLM-wrapper project.

**The new direction:** the input is **real code from a real repo**. Findings cite **real files and real lines**. The knowledge graph (2,301 nodes of EU AI Act + GDPR structure) becomes a **rule corpus**, not a research Q&A bot. Every claim in the report is grounded in an artifact the reviewer can open.

This is the gap in the AI-governance tooling landscape: Credo AI and Holistic AI collect self-reported answers; Fairlearn / AIF360 audit models at runtime with access to training data; Guardrails AI validates LLM outputs. **Nobody statically scans AI application code against regulatory obligations.**

---

## 3. Competitive landscape — what we borrow

Modern security / compliance scanners converged on a common shape. We borrow it directly.

| Tool | Pattern we borrow |
|---|---|
| Semgrep | Rule catalog as data (YAML), not hand-coded if/else |
| SonarQube | Confidence scoring + per-rule severity + suppressions via config |
| Snyk | Dependency / SBOM scanning; findings tied to fix suggestions |
| GitGuardian | Pre-commit and on-save delta scanning for low-friction UX |
| Trivy | Deterministic scanning first; LLMs only for narrative post-hoc |
| OpenSSF Scorecard | Repo hygiene signals that compose into a score |

**Core principle** shared across all of them: **LLMs are kept out of the detection hot path.** Static analysis is fast, cheap, explainable; LLMs are slow, expensive, and hallucinate. AlloyCode follows the same rule — deterministic scanners and KG lookups find the facts; Gemini only writes the human narrative at the end.

---

## 4. System architecture

Three live modules after the pivot (monitor is decommissioned).

```
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND (Next.js 16, Port 3000)                               │
│  Pages: /scan (new), /scans/[id], /knowledge, /approvals        │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTP fetch → localhost:8004
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (FastAPI, Port 8004)                              │
│  • code_analyzer/     — clone + scan + profile (NEW)            │
│  • agents/            — Risk Classifier, Technical Assessor,    │
│                         Legal Research, Doc Generator           │
│  • LangGraph workflow · Postgres · Redis · Gemini 2.5           │
└───────────────────────┬─────────────────────────────────────────┘
                        │ POST /api/v1/hybrid/reason
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE_ENGINE (FastAPI, Port 8001)                          │
│  • Neo4j: 2,301 nodes / 4,423 rels + native vector index        │
│  • 2,198 embeddings (3072-dim) stored as :Entity.embedding      │
│  • Hybrid retrieval (RRF) + multi-hop reasoning                 │
└─────────────────────────────────────────────────────────────────┘
```

**Decommissioned:** `monitor/` (was Port 8002). Drift/bias/Prometheus machinery provided no usable signal in a portfolio demo — see [REFERENCE.md](REFERENCE.md) §6 for the honest audit.

---

## 5. End-to-end data flow (one scan)

```
 [1] User pastes GitHub URL in /scan
        │
        ▼
 [2] Orchestrator: POST /api/v1/scans
        • Create scan_id, persist initial state, return 202
        • Background task picks up from here
        │
        ▼
 [3] code_analyzer.ingest
        • git clone --depth=1 → temp workspace
        • Detect language(s), framework(s), topology
        • Build file index + dep manifest (requirements.txt, pyproject, package.json)
        │
        ▼
 [4] code_analyzer.scan  ← 10 deterministic detection rules
        • Import-based scanners (biometric libs, LLM SDKs, …)
        • AST scanners (FastAPI/Flask routes, model-inference sites)
        • File-pattern scanners (model cards, DPIA docs, data cards)
        • Content scanners (prohibited-practice keywords)
        • Output: findings[] with {rule_id, file, line, excerpt, confidence}
        │
        ▼
 [5] code_analyzer.profile
        • Aggregate findings into "AI System Profile" JSON
        • Structured replacement for the old free-text description
        │
        ▼
 [6] Orchestrator LangGraph agents consume profile
        • Risk Classifier → EU AI Act tier (grounded in profile signals)
        • Technical Assessor → GDPR gap analysis
        • Legal Research → calls knowledge_engine with profile signals
        • Doc Generator → DPIA / ROPA / conformity scaffolds
        • (Human-in-loop approval retained for Critical severity)
        │
        ▼
 [7] Knowledge_engine.hybrid/reason
        • Vector search seeded on finding signal (e.g., "face_recognition lib")
        • Multi-hop graph traversal from matched Obligations
        • RRF fusion → Articles + Obligations + Recitals
        • Gemini synth → answer + citations (used for narrative only)
        │
        ▼
 [8] Report rendered at /scans/[id]
        • Each finding: file:line excerpt + severity + mapped articles
        •                         + suggested remediation + KG citations
        • Downloadable as JSON / markdown (PDF in Phase 2)
```

---

## 6. Integration contracts

**Frontend → Orchestrator**
```
POST /api/v1/scans              { repo_url, branch?, depth? }  → 202 { scan_id }
GET  /api/v1/scans/{id}         → scan state + findings
GET  /api/v1/scans              → list
GET  /api/v1/audit-log?scan_id  → per-scan event stream
POST /api/v1/approvals/{id}/decide  (unchanged — Critical findings pause for review)
```

**Orchestrator → Knowledge_engine**
```
POST /api/v1/hybrid/reason      { question, anchors[] }
  — anchors[] = detected signals (e.g., ["face_recognition", "biometric_id"])
  — forces retrieval to be grounded in observed code patterns, not prose embeddings
```

**Knowledge_engine internals** (unchanged)
```
/api/v1/vector/search · /api/v1/graph/traverse · /api/v1/hybrid/search · /api/v1/hybrid/reason
```

---

## 7. Scope of Phase 1 (what ships first)

| In | Out (for Phase 1) |
|---|---|
| GitHub public repo scan via URL | Private repo auth |
| Python-only scanners (AST + imports) | Tree-sitter / multi-language |
| 10 MVP detection rules | Full rule catalog |
| ~30 mapped obligations from KG | All 1,325 |
| One-pass full-repo scan | Delta scan / on-save |
| Web report UI | PDF export, VS Code extension |
| Orchestrator retains LangGraph + human-in-loop | Monitor module, drift/bias, Prometheus |

See [REFERENCE.md](REFERENCE.md) for the rule catalog, KG schema, implementation status, and full roadmap.

---

*Supersedes and merges the prior `01_PROJECT_PORTFOLIO.md` (multi-project portfolio pitch) and `02_ARCHITECTURE_AND_INTEGRATION.md` (pre-pivot architecture).*


---


## SOURCE: `docs/REFERENCE.md`

# AlloyCode — Technical Reference

**Last updated:** 2026-04-13
**Covers:** Knowledge base schema · Rule catalog · Implementation status · Roadmap

---

## 1. Knowledge Base — the moat

The KG and vector store are the **rule corpus** for the scanner. Every detection rule (§3) maps to Articles / Obligations stored here. Do not throw this away — this is the single hardest thing in the repo to rebuild.

### 1.1 Current state (verified 2026-04-13)

| Store | Count | Notes |
|---|---|---|
| Neo4j nodes | **2,301** | Every node carries `Entity` super-label + one specialized label |
| Neo4j relationships | **4,423** | |
| Vector store docs | **2,198** | Custom JSON store (not ChromaDB — Python 3.14 compat; legacy folder name) |
| Vector collections | **7** | articles, obligations, recitals, definitions, concepts, rights, interpretive |
| Embedding model | `gemini-embedding-001` | 768-dim, cosine similarity |

### 1.2 Entity types (19)

| Label | Count | Label | Count |
|---|--:|---|--:|
| Obligation | 1,325 | AISystemType | 19 |
| Recital | 353 | Right | 19 |
| Article | 212 | Actor | 18 |
| Exemption | 96 | DataType | 17 |
| Definition | 90 | EnforcementAction | 15 |
| Concept | 47 | Annex | 13 |
| Chapter | 24 | Penalty | 6 |
| Guideline | 21 | RiskCategory | 4 |
| CaseLaw | 20 | Regulation | 2 |

### 1.3 Relationship types (top 13)

| Type | Count | Type | Count |
|---|--:|---|--:|
| REQUIRES | 1,008 | PART_OF | 270 |
| APPLIES_TO | 939 | PERMITS | 232 |
| CONTAINS | 602 | EXEMPTS | 96 |
| REFERENCES | 587 | DEFINES | 90 |
| INTERPRETS | 303 | CITES / PROHIBITS | 85 each |
| ENFORCES | 50 | COMPLEMENTS | 76 |

### 1.4 Raw data inventory (still on disk for rebuild)

89 files, 5.7 MB under [../legacy_prototypes/New_Data/](../legacy_prototypes/New_Data/) (already ingested into `knowledge_engine/parsed_data/`):

| Category | Files | Entities |
|---|---|---|
| GDPR chapters | 11 `.txt` | 99 articles |
| GDPR recitals | 1 `.txt` | 173 recitals |
| EU AI Act chapters | 13 `.txt` | 113 articles |
| EU AI Act recitals | 1 `.txt` | ~180 recitals |
| EU AI Act annexes | 1 `.txt` | 13 annexes |
| CJEU case law | 17 `.txt` | 20 decisions |
| EDPB guidelines | 22 `.txt` | 22 guidelines |
| Enforcement actions | 18 `.txt` | 15 DPA decisions |

### 1.5 ID naming convention (unchanged)

| Pattern | Example | Meaning |
|---|---|---|
| `GDPR_ART_{N}` | `GDPR_ART_35` | GDPR Article |
| `AIACT_ART_{N}` | `AIACT_ART_14` | AI Act Article |
| `AIACT_ANNEX_{ROMAN}` | `AIACT_ANNEX_III` | AI Act Annex |
| `GDPR_DEF_{TERM}` | `GDPR_DEF_BIOMETRIC_DATA` | Definition |
| `OBL_{REG}_{NAME}` | `OBL_GDPR_LAWFUL_BASIS` | Obligation |
| `CJEU_C_{NUM}` | `CJEU_C_311_18` | Case law |
| `ENF_{NAME}` | `ENF_CLEARVIEW_AI` | Enforcement action |

### 1.6 Rebuild pipeline

Scripts in [../knowledge_engine/scripts/](../knowledge_engine/scripts/), run in order:

```
01_parse_raw_data.py            raw_data/*.txt → parsed_data/{legal,entities,interpretive}/*.json
02_load_structural_kg.py        → Regulation / Article / Annex nodes
02a_extract_structural_rels.py  → CONTAINS / REFERENCES edges
02b_validate_graph_local.py     → integrity check
03_extract_semantic.py          → concepts, principles
03b_extract_obligations.py      → 1,325 Obligation nodes
03c_extract_cross_regulation.py → GDPR ↔ AI Act bridges
03e_extract_concepts.py         → Concept nodes
03f_extract_rights.py           → Right nodes
03d_validate_full_graph.py      → validation
04_load_full_kg.py              → final state (2,301/4,423)
05_load_vector_store.py         → embed text → write to Neo4j :Entity.embedding
07_run_golden_tests.py          → 6 golden queries
08_coverage_report.py           → coverage metrics
09_load_vectors_to_neo4j.py     → bulk-load pre-computed embeddings → Neo4j
```

---

## 2. AI System Profile (the new orchestrator input)

The scanner's job is to produce this JSON artifact from a repo. Agents consume it instead of free-text.

```jsonc
{
  "scan_id": "scn_01H...",
  "repo": { "url": "...", "ref": "main", "commit": "abc123", "languages": ["python"] },
  "ai_components": [
    { "kind": "llm_sdk",        "evidence": [{"file": "src/chat.py", "line": 12, "import": "openai"}] },
    { "kind": "biometric_lib",  "evidence": [{"file": "src/verify.py", "line": 3, "import": "face_recognition"}] }
  ],
  "decision_surfaces": [
    { "endpoint": "POST /api/approve", "file": "src/api/approve.py", "line": 42,
      "calls_model": true, "has_human_review": false }
  ],
  "data_signals": {
    "pii_fields": ["email", "national_id"],
    "has_dpia_doc": false,
    "has_model_card": false,
    "has_data_card": false,
    "audit_logging": "partial"
  },
  "findings": [ /* see §3 */ ]
}
```

This is what every agent downstream reads.

---

## 3. Rule Catalog — Phase 1 MVP (10 rules)

Rules live in [../orchestrator/src/code_analyzer/rules/](../orchestrator/src/code_analyzer/rules/) as YAML (Semgrep-style; rule-as-data). Each maps to one or more KG obligations.

### 3.1 Rule definitions

| # | ID | Detects | Technique | Severity | Maps to |
|---|---|---|---|---|---|
| 1 | `AI-001` | Biometric / face / emotion recognition libs | Import scan: `face_recognition`, `deepface`, `mediapipe.solutions.face`, `dlib.get_frontal_face_detector`, `fer` | Critical | AIACT Art 5(1)(f,h) · Annex III §1 · GDPR Art 9 |
| 2 | `AI-002` | LLM / generative AI usage | Import scan: `openai`, `anthropic`, `google.generativeai`, `transformers`, `langchain`, `llama_index` | High | AIACT Art 50 · Art 52 |
| 3 | `AI-003` | User-facing AI decision endpoint | AST: FastAPI/Flask route returning model inference, no `human_review` / `approval` keyword in handler | High | AIACT Art 14 · GDPR Art 22 |
| 4 | `AI-004` | Missing transparency disclosure | File absence: no `model_card.md`, no `/disclose` endpoint, no "AI-generated" / "this is an AI" string in user-facing templates | Medium | AIACT Art 13 + 50 |
| 5 | `AI-005` | PII handling without DPIA marker | Regex/AST on schemas: fields matching `email\|ssn\|national_id\|biometric\|health`; no `dpia.md` / `DPIA.md` in repo root | High | GDPR Art 35 · Art 9 |
| 6 | `AI-006` | Training-data source opacity | File scan: `.csv` / `.parquet` / HuggingFace dataset refs in training scripts; no `data_card.md` / `DATASHEET.md` | Medium | AIACT Art 10 |
| 7 | `AI-007` | No logging / audit trail on AI decisions | AST: inference call not wrapped in `logger.*` / audit call within same function scope | Medium | AIACT Art 12 |
| 8 | `AI-008` | Social-scoring / behavioral-prediction keywords | Content scan in docstrings, README, identifiers: `social_score`, `trustworthiness`, `creditworthiness_by_behavior`, `predictive_policing` | Critical | AIACT Art 5(1)(c) |
| 9 | `AI-009` | Real-time biometric in public-space context | Co-occurrence: `AI-001` signal + keywords `cctv`, `public`, `street`, `realtime`, `live_stream` within 20 LOC or same file | Critical | AIACT Art 5(1)(h) |
| 10 | `AI-010` | No human-override mechanism for high-risk endpoint | AST: `AI-003` endpoint + no sibling `override` / `reject` / `appeal` route in same router | High | AIACT Art 14(4) |

### 3.2 Rule schema (YAML)

```yaml
# orchestrator/src/code_analyzer/rules/AI-001_biometric_libs.yml
id: AI-001
title: Biometric recognition library usage
severity: critical
technique: import_scan
languages: [python]
patterns:
  imports:
    - face_recognition
    - deepface
    - dlib.get_frontal_face_detector
    - mediapipe.solutions.face_detection
    - fer
maps_to:
  articles: [AIACT_ART_5, AIACT_ANNEX_III, GDPR_ART_9]
  obligation_anchors: [biometric_id, face_recognition, special_category_data]
confidence:
  base: 0.9
  dampeners:
    - { when: "file_matches: tests/|spec/", factor: 0.4 }  # test file → low confidence
    - { when: "import_unused: true", factor: 0.5 }
remediation: >
  Real-time remote biometric identification in publicly accessible spaces is
  prohibited by AI Act Art 5(1)(h) except for narrow law-enforcement carve-outs.
  If used in a closed / consented context, it remains a high-risk system under
  Annex III §1 and triggers GDPR Art 9 special-category requirements. Add a
  DPIA (GDPR Art 35) and a lawful basis under Art 9(2).
```

### 3.3 Confidence & suppressions

- Each finding carries a **confidence score 0.0–1.0** (base × dampeners).
- Suppressions via `.alloycode.yml` at repo root (pattern copied from Semgrep):
  ```yaml
  suppress:
    - rule: AI-001
      path: "tests/**"
    - rule: AI-002
      reason: "Internal tool, no user-facing transparency obligation"
      expires: 2026-12-31
  ```

### 3.4 Scanner architecture

```
orchestrator/src/code_analyzer/
├── __init__.py
├── ingest.py              # shallow clone, language detect, file index
├── profile.py             # aggregate findings -> AI System Profile
├── rules/                 # rule definitions (YAML)
│   ├── AI-001_biometric_libs.yml
│   └── ... (10 total)
├── scanners/
│   ├── base.py            # Scanner ABC, loads rules, emits findings
│   ├── import_scanner.py  # ast.Import / ast.ImportFrom walks
│   ├── ast_scanner.py     # AST pattern matching (routes, inference calls)
│   ├── file_pattern.py    # presence/absence of marker files
│   └── content_scanner.py # regex on docstrings, README, identifiers
└── mapper.py              # finding -> KG obligation via knowledge_engine
```

Folded into orchestrator (not a separate service) — fewer moving parts for a portfolio project. Extract later if it grows.

---

## 4. Orchestrator — revised agent contract

Each agent now consumes the **AI System Profile** (§2) instead of free-text.

| Agent | Before | After |
|---|---|---|
| Risk Classifier | "user typed a description" → LLM guesses tier | Reads `ai_components` + `decision_surfaces` → deterministic tier bands → LLM refines |
| Technical Assessor | Free-text GDPR gap analysis | Walks `data_signals` + detected PII fields → KG lookup for each gap |
| Legal Research | Generic `question` to knowledge_engine | `anchors[]` grounded in profile signals → focused RRF retrieval |
| Doc Generator | Writes DPIA / ROPA from scratch | Fills DPIA template with actual evidence (file:line) from profile |
| Supervisor | LangGraph orchestration | **Unchanged** — same state machine, richer state |

The LangGraph state machine in [../orchestrator/src/agents/supervisor.py](../orchestrator/src/agents/supervisor.py) and the human-in-loop approval queue ([../orchestrator/src/control_plane/approval_queue.py](../orchestrator/src/control_plane/approval_queue.py)) are retained. Only the input contract changes.

---

## 5. API surface — after Phase 1

### 5.1 Orchestrator (Port 8004)

| Endpoint | Method | Purpose | Status |
|---|---|---|---|
| `/api/v1/scans` | POST | Submit repo URL for scan | **NEW** |
| `/api/v1/scans` | GET | List scans | **NEW** |
| `/api/v1/scans/{id}` | GET | Scan state + findings report | **NEW** |
| `/api/v1/scans/{id}/profile` | GET | Raw AI System Profile JSON | **NEW** |
| `/api/v1/scans/{id}/findings` | GET | Flat findings list | **NEW** |
| `/api/v1/approvals` / `/approvals/{id}/decide` | GET/POST | Human-in-loop (retained) | Kept |
| `/api/v1/audit-log` | GET | Event stream per scan | Kept |
| `/api/v1/assessments*` | — | Old free-text endpoints | **DEPRECATED — removed** |

### 5.2 Knowledge_engine (Port 8001) — unchanged

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/vector/search` | POST | Semantic top-K |
| `/api/v1/graph/traverse` | POST | Multi-hop Cypher |
| `/api/v1/hybrid/search` | POST | RRF fusion |
| `/api/v1/hybrid/reason` | POST | Fusion + LLM synth (accepts new `anchors[]` param) |
| `/health` | GET | Health + node/doc counts |

---

## 6. Honest audit — why `monitor/` was removed

The pre-pivot audit rated `monitor/` at 85% complete. On honest re-review, for a **portfolio project**, it added weight without signal:

| Claim | Reality |
|---|---|
| Drift detection | Needs continuous traffic to show anything. Run 6 golden tests once → flat lines forever. |
| Bias detection | Chi-square on protected attributes requires a dataset with protected attributes. We didn't have one. |
| Article 14 compliance check | One rule: `if risk=="HIGH_RISK" and not human_reviewed: flag`. The orchestrator already enforces this at the workflow level. |
| Prometheus metrics | Collected but nothing consumed them. No Grafana wired. |
| Monitored "all systems" | Monitored only the orchestrator's own agents — circular. |

**What was removed:**
- `monitor/` service from [../docker-compose.yml](../docker-compose.yml)
- Entries in [../pipeline.ps1](../pipeline.ps1) (start/stop actions)
- `/monitoring` page from frontend + sidebar link
- Port 8002 is no longer in use
- The one useful idea — a per-scan audit log — lives in the orchestrator (`/api/v1/audit-log`)

Freed ~1,500 LOC, 2 Docker services (monitor + monitoring-postgres), and simplified the deploy story.

---

## 7. Implementation status (post-pivot snapshot)

| Component | Status | Notes |
|---|---|---|
| knowledge_engine (2,301 nodes) | ✅ Complete | No changes needed |
| Neo4j Aura instance | ⚠️ Live | Auto-pauses after 3 days on free tier; resumes on demand |
| Orchestrator LangGraph core | ✅ Kept | Input contract being reshaped |
| Orchestrator `code_analyzer/` module | ⬜ **Phase 1 — to build** | Scanner, rules, profile |
| 10 MVP detection rules | ⬜ **Phase 1 — to build** | Python-only AST/import/file-pattern |
| Finding → KG obligation mapper | ⬜ **Phase 1 — to build** | Uses `/hybrid/reason` with anchors |
| Frontend `/scan` page | ⬜ **Phase 1 — to build** | URL input → progress → findings |
| Frontend `/scans/[id]` report | ⬜ **Phase 1 — to build** | file:line anchored findings, article citations |
| Frontend `/knowledge` page | ✅ Kept | Force-directed KG explorer — demoable as-is |
| Old `/assessments/*` pages | 🗑️ To remove | Replaced by `/scans/*` |
| `monitor/` module + `/monitoring` page | ✅ Removed | See §6 |
| Tree-sitter / multi-language scanner | ⬜ Phase 2 | Python-first keeps Phase 1 small |
| VS Code extension | ⬜ Phase 3 | Depends on stable scan API |
| PDF report export | ⬜ Phase 2 | Markdown → weasyprint |
| Delta / on-save scan API | ⬜ Phase 2 | Prereq for VS Code extension |

---

## 8. Roadmap

### Phase 1 — Prove the thesis (current)

Goal: demoable end-to-end scan of a real public Python AI repo producing file:line findings mapped to KG articles.

- [ ] Scaffold `orchestrator/src/code_analyzer/`
- [ ] Ingest: `git clone --depth=1`, language detect, file index
- [ ] Implement 10 rules as YAML + 4 scanners (import, AST, file-pattern, content)
- [ ] Profile aggregator → `AISystemProfile` schema
- [ ] Mapper: findings → obligations via knowledge_engine `/hybrid/reason`
- [ ] Reshape agents to consume profile (not free-text)
- [ ] Frontend `/scan` + `/scans/[id]` pages
- [x] Delete `monitor/` module + `/monitoring` page
- [ ] Delete old `/assessments/*` pages
- [ ] Golden test: scan a known-violating fixture repo → assert expected findings

### Phase 2 — Make it good

- Expand to ~50 rules across tree-sitter (JS/TS/Go/Java)
- Full obligation catalog mapping (~1,325 obligations)
- LLM-generated narrative in report (post-detection)
- SBOM / dependency graph scanning (catch transitive AI usage)
- Scan history + diff view (what changed since last scan)
- PDF export

### Phase 3 — VS Code extension

- Delta scans on save / commit
- Diagnostics in Problems panel with file:line + article reference
- Code lens: "Run full compliance scan"
- Authentication for private repos
- Publish to VS Code Marketplace

---

## 9. Key risks (called out honestly)

| Risk | Mitigation |
|---|---|
| **False positives** — `import face_recognition` in a test file is noise | Dampener rules; `.alloycode.yml` suppressions; confidence score |
| **Signal → obligation mapping is soft** | KG provides grounded citations; every finding links to the Article; reviewer can judge fit |
| **Python-only limits demo repos** | Phase 1 scope accepted; tree-sitter in Phase 2 |
| **Neo4j Aura free tier auto-pauses** | Not worth fixing for a portfolio; resume on demand takes 30s |
| **LLM cost if narrative is per-finding** | Narrative is per-scan, not per-finding; batched single Gemini call |

---

*Supersedes and merges the prior `03_KB_DESIGN_AND_CONSTRUCTION.md` (KG schema) and `04_IMPLEMENTATION_AUDIT.md` (pre-pivot audit).*


---


## SOURCE: `docs/MEMORY.md`

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
- 7 logical collections written as `:Entity.embedding` properties on Neo4j nodes (graph_store hosts the native HNSW vector index `entity_embedding`)
- 2,198 documents embedded with `gemini-embedding-001` (3,072 dimensions)
- Collections: articles (212), recitals (353), interpretive (56), definitions (90), obligations (1,421), concepts (47), rights (19)
- Single Neo4j vector index over `:Entity`; queries filter by `n.collection`. The earlier JSON-backed VectorStore and Weaviate sidecar were both retired
- Exit gates updated: concepts >= 40, rights >= 15
- Companion script `09_load_vectors_to_neo4j.py` bulk-loads pre-computed embeddings (skips the Gemini round-trip)

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
- Test files:
  - `test_extractors.py` (20 tests): ConceptExtractor (7), RightExtractor (7), DefinitionExtractor (2), ObligationExtractor (4)
  - `test_retrieval.py`: QueryModels + ReasoningEngine (vector retrieval is exercised end-to-end by `scripts/07_run_golden_tests.py` against live Aura, since the vector store is now Neo4j-native and not unit-mockable)
- Fixtures in `conftest.py`: sample articles, sample retrieval results

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
- **Vector store**: Neo4j native vector index (`entity_embedding`, HNSW, cosine, dim=3072) over `:Entity.embedding`
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
      graph_store.py             # Neo4j CRUD + native vector index (entity_embedding)
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
    05_load_vector_store.py      # Phase 5: Embed text + write embeddings to Neo4j
    06_demo_query.py             # Demo: Graph RAG queries (--reason for LLM mode)
    07_run_golden_tests.py       # Golden query test suite (6 cases)
    08_coverage_report.py        # Coverage report (5 checks)
    09_load_vectors_to_neo4j.py  # Bulk-load pre-computed embeddings -> Neo4j
  tests/
    conftest.py                  # Fixtures: sample articles
    test_extractors.py           # 20 tests: concept, right, definition, obligation
    test_retrieval.py            # query models + reasoning engine (vector covered by 07)
  golden_tests/
    test_queries.json            # 6 golden test cases with expected outputs
  parsed_data/
    legal/                       # Articles, recitals, chapters, annexes
    interpretive/                # Case law, guidelines, enforcement
    entities/                    # Definitions, actors, obligations, concepts, rights, etc.
    relationships/               # All relationship JSON files
  # Vectors live in Neo4j as :Entity.embedding (cosine, dim=3072) — no
  # separate vector store directory anymore.
```

## Known Issues & Gotchas
1. **Modality detection**: First-match "shall not" before "shall" gives wrong results — use frequency-based detection
2. **Paragraphs format**: `article["paragraphs"]` is `dict[str, str|dict]` keyed by para number, NOT a list
3. **Gemini SDK**: `google-generativeai` deprecated, use `google-genai` with `genai.Client()` API
4. **Embedding model**: `gemini-embedding-001` (NOT `text-embedding-004` which 404s on new SDK)
5. **Definition extraction**: 90/94 defs (24/26 GDPR, 66/68 AI Act) — 4 missing use non-standard formatting
6. **Neo4j COMPLEMENTS dedup**: 84 JSON edges -> 76 in Neo4j (bidirectional pairs with same props collapsed)
7. **Orphan node fixes**: CaseLaw (Directive 95/46/EC pattern), Guidelines (scan 20000 chars not 5000), Enforcement (raw text fallback)
8. **Vector backend history**: ChromaDB (Python 3.14 incompatible) → JSON-backed VectorStore → Weaviate sidecar → **Neo4j native vector index** (current). Each prior backend is gone from the codebase.
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


---
