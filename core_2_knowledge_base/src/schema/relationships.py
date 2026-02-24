"""Relationship type definitions for the EU AI Regulatory Knowledge Graph.

25 relationship types covering: structural, semantic, interpretive,
cross-regulation, and enforcement links.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    """All 25 relationship types in the knowledge graph."""
    # Structural
    CONTAINS = "CONTAINS"
    PART_OF = "PART_OF"
    REFERENCES = "REFERENCES"
    AMENDS = "AMENDS"
    REPEALS = "REPEALS"

    # Definitional
    DEFINES = "DEFINES"

    # Normative (obligations, prohibitions, permissions)
    REQUIRES = "REQUIRES"
    PROHIBITS = "PROHIBITS"
    PERMITS = "PERMITS"
    TRIGGERS = "TRIGGERS"
    EXEMPTS = "EXEMPTS"

    # Actor and scope
    APPLIES_TO = "APPLIES_TO"
    ENFORCED_BY = "ENFORCED_BY"
    RESPONSIBLE_FOR = "RESPONSIBLE_FOR"
    PROCESSES = "PROCESSES"
    PROTECTS = "PROTECTS"

    # Classification
    REGULATED_BY = "REGULATED_BY"
    CLASSIFIED_AS = "CLASSIFIED_AS"
    MITIGATED_BY = "MITIGATED_BY"

    # Interpretive
    INTERPRETS = "INTERPRETS"
    HAS_EXCEPTION = "HAS_EXCEPTION"

    # Cross-regulation
    COMPLEMENTS = "COMPLEMENTS"
    SUPERSEDES = "SUPERSEDES"

    # Enforcement / case law
    PENALISED_BY = "PENALISED_BY"
    CITES = "CITES"


class InteractionType(str, Enum):
    """Required property on COMPLEMENTS edges — distinguishes cross-regulation semantics."""
    REINFORCES = "REINFORCES"            # Both regulations require the same thing
    CREATES_EXCEPTION = "CREATES_EXCEPTION"  # One regulation creates exception to other's prohibition
    CO_TRIGGERS = "CO_TRIGGERS"          # Both assessments required simultaneously
    CUMULATIVE = "CUMULATIVE"            # Penalties or requirements stack
    DELEGATES = "DELEGATES"              # One regulation defers to the other


class Relationship(BaseModel):
    """A directed edge in the knowledge graph."""
    source_id: str
    target_id: str
    type: RelationshipType
    properties: dict[str, Any] = Field(default_factory=dict)

    # Cross-reference context
    source_paragraph: str | None = None
    target_paragraph: str | None = None
    confidence: float = 1.0
    rationale: str | None = None

    # For COMPLEMENTS edges
    interaction_type: InteractionType | None = None
