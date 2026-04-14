"""Entity type definitions for the EU AI Regulatory Knowledge Graph.

19 entity types covering: structural legal provisions, semantic extractions,
interpretive content, and enforcement/case law.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────────

class EntityType(str, Enum):
    """All 19 entity types in the knowledge graph."""
    REGULATION = "Regulation"
    CHAPTER = "Chapter"
    ARTICLE = "Article"
    RECITAL = "Recital"
    ANNEX = "Annex"
    DEFINITION = "Definition"
    CONCEPT = "Concept"
    OBLIGATION = "Obligation"
    EXEMPTION = "Exemption"
    RIGHT = "Right"
    PENALTY = "Penalty"
    AUTHORITY = "Authority"
    ACTOR = "Actor"
    DATA_TYPE = "DataType"
    AI_SYSTEM_TYPE = "AISystemType"
    RISK_CATEGORY = "RiskCategory"
    CASE_LAW = "CaseLaw"
    GUIDELINE = "Guideline"
    ENFORCEMENT_ACTION = "EnforcementAction"


class ObligationType(str, Enum):
    MUST = "MUST"
    MUST_NOT = "MUST_NOT"
    SHOULD = "SHOULD"
    MAY = "MAY"


class RiskLevel(str, Enum):
    PROHIBITED = "PROHIBITED"
    HIGH_RISK = "HIGH_RISK"
    LIMITED_RISK = "LIMITED_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"


class RegulationId(str, Enum):
    GDPR = "GDPR"
    EU_AI_ACT = "EU_AI_ACT"


# ── Provenance mixin ───────────────────────────────────────────────────────

class Provenance(BaseModel):
    """Provenance metadata for versioning and auditability."""
    source_url: str | None = None
    source_version: str | None = None
    loaded_at: datetime = Field(default_factory=datetime.utcnow)
    is_current: bool = True
    superseded_by: str | None = None


# ── Base entity ────────────────────────────────────────────────────────────

class Entity(BaseModel):
    """Base entity — all KG nodes inherit from this."""
    id: str
    type: EntityType
    name: str
    description: str | None = None
    source_text: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    provenance: Provenance = Field(default_factory=Provenance)


# ── Structural entities ────────────────────────────────────────────────────

class Regulation(Entity):
    type: EntityType = EntityType.REGULATION
    effective_date: str | None = None
    regulation_id: RegulationId | None = None


class Chapter(Entity):
    type: EntityType = EntityType.CHAPTER
    regulation_id: RegulationId | None = None
    chapter_number: int | None = None


class Article(Entity):
    type: EntityType = EntityType.ARTICLE
    regulation_id: RegulationId | None = None
    chapter: str | None = None
    article_number: str | None = None
    title: str | None = None
    full_text: str | None = None
    paragraphs: dict[str, Any] = Field(default_factory=dict)
    modality: str | None = None
    applies_to_actors: list[str] = Field(default_factory=list)
    cross_references: list[str] = Field(default_factory=list)


class Recital(Entity):
    type: EntityType = EntityType.RECITAL
    regulation_id: RegulationId | None = None
    recital_number: int | None = None
    full_text: str | None = None
    article_references: list[str] = Field(default_factory=list)


class Annex(Entity):
    type: EntityType = EntityType.ANNEX
    regulation_id: RegulationId = RegulationId.EU_AI_ACT
    annex_number: str | None = None  # Roman numeral string
    title: str | None = None
    sections: list[dict[str, Any]] = Field(default_factory=list)
    full_text: str | None = None


# ── Semantic entities (extracted from article text) ────────────────────────

class Definition(Entity):
    type: EntityType = EntityType.DEFINITION
    regulation_id: RegulationId | None = None
    term: str = ""
    definition_text: str = ""
    article_reference: str | None = None
    definition_number: int | None = None
    synonyms: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)


class Obligation(Entity):
    type: EntityType = EntityType.OBLIGATION
    obligation_type: ObligationType = ObligationType.MUST
    source_article: str | None = None
    source_paragraph: str | None = None
    source_text: str | None = None
    applies_to: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    deadline: str | None = None
    penalty_reference: str | None = None


class Exemption(Entity):
    type: EntityType = EntityType.EXEMPTION
    source_article: str | None = None
    source_paragraph: str | None = None
    exempts_from: str | None = None  # obligation ID
    condition_text: str | None = None
    conditions: list[str] = Field(default_factory=list)


class Right(Entity):
    type: EntityType = EntityType.RIGHT
    regulation_id: RegulationId | None = None
    source_article: str | None = None
    right_holder: str | None = None  # e.g., "data_subject"
    conditions: list[str] = Field(default_factory=list)


class Concept(Entity):
    type: EntityType = EntityType.CONCEPT
    regulation_id: RegulationId | None = None
    related_articles: list[str] = Field(default_factory=list)
    category: str | None = None  # e.g., "principle", "processing_operation", "compliance_concept"


class Penalty(Entity):
    type: EntityType = EntityType.PENALTY
    regulation_id: RegulationId | None = None
    source_article: str | None = None
    max_fine_eur: int | None = None
    max_fine_turnover_pct: float | None = None
    tier: str | None = None
    applies_to_articles: list[str] = Field(default_factory=list)


# ── Actor and classification entities ──────────────────────────────────────

class Actor(Entity):
    type: EntityType = EntityType.ACTOR
    regulation_id: RegulationId | None = None
    definition_article: str | None = None
    responsibilities: list[str] = Field(default_factory=list)


class Authority(Entity):
    type: EntityType = EntityType.AUTHORITY
    jurisdiction: str | None = None
    authority_type: str | None = None  # "DPA", "AI_Office", "Notified_Body"


class DataType(Entity):
    type: EntityType = EntityType.DATA_TYPE
    parent_type: str | None = None
    is_special_category: bool = False
    regulated_by: list[str] = Field(default_factory=list)


class AISystemType(Entity):
    type: EntityType = EntityType.AI_SYSTEM_TYPE
    risk_category: str | None = None
    annex_reference: str | None = None
    use_case_area: str | None = None


class RiskCategory(Entity):
    type: EntityType = EntityType.RISK_CATEGORY
    risk_level: RiskLevel | None = None
    source_article: str | None = None
    annex_reference: str | None = None


# ── Interpretive entities ──────────────────────────────────────────────────

class CaseLaw(Entity):
    type: EntityType = EntityType.CASE_LAW
    case_number: str | None = None
    case_name: str | None = None
    full_name: str | None = None
    court: str | None = None
    decision_date: str | None = None
    topic: str | None = None
    provisions_interpreted: list[str] = Field(default_factory=list)
    holding: str | None = None
    key_legal_points: list[str] = Field(default_factory=list)
    practical_impact: list[str] = Field(default_factory=list)
    ai_relevance: list[str] = Field(default_factory=list)


class Guideline(Entity):
    type: EntityType = EntityType.GUIDELINE
    reference: str | None = None
    topics: list[str] = Field(default_factory=list)
    tier: str | None = None
    full_text: str | None = None
    article_references: list[str] = Field(default_factory=list)


class EnforcementAction(Entity):
    type: EntityType = EntityType.ENFORCEMENT_ACTION
    authority: str | None = None
    target: str | None = None
    decision_date: str | None = None
    fine_amount_eur: int | None = None
    fine_category: str | None = None
    violations: list[str] = Field(default_factory=list)
    facts: str | None = None
    key_findings: list[str] = Field(default_factory=list)
    corrective_measures: list[str] = Field(default_factory=list)
    ai_relevance: list[str] = Field(default_factory=list)


# ── Entity factory ─────────────────────────────────────────────────────────

ENTITY_TYPE_MAP: dict[EntityType, type[Entity]] = {
    EntityType.REGULATION: Regulation,
    EntityType.CHAPTER: Chapter,
    EntityType.ARTICLE: Article,
    EntityType.RECITAL: Recital,
    EntityType.ANNEX: Annex,
    EntityType.DEFINITION: Definition,
    EntityType.CONCEPT: Concept,
    EntityType.OBLIGATION: Obligation,
    EntityType.EXEMPTION: Exemption,
    EntityType.RIGHT: Right,
    EntityType.PENALTY: Penalty,
    EntityType.AUTHORITY: Authority,
    EntityType.ACTOR: Actor,
    EntityType.DATA_TYPE: DataType,
    EntityType.AI_SYSTEM_TYPE: AISystemType,
    EntityType.RISK_CATEGORY: RiskCategory,
    EntityType.CASE_LAW: CaseLaw,
    EntityType.GUIDELINE: Guideline,
    EntityType.ENFORCEMENT_ACTION: EnforcementAction,
}


def entity_from_dict(data: dict[str, Any]) -> Entity:
    """Factory: create the correct Entity subclass from a dict with 'type' key.

    This fixes the core_2 bug where _record_to_entity() always returned base Entity.
    """
    entity_type = EntityType(data.get("type", "Concept"))
    cls = ENTITY_TYPE_MAP.get(entity_type, Entity)
    return cls(**data)
