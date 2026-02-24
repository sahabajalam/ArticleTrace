"""Tests for entity extractors."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.extractors.concept_extractor import ConceptExtractor, ALL_CONCEPTS
from src.extractors.right_extractor import RightExtractor, ALL_RIGHTS
from src.extractors.definition_extractor import DefinitionExtractor
from src.extractors.obligation_extractor import ObligationExtractor


# ── Concept Extractor ─────────────────────────────────────────────────────────

class TestConceptExtractor:
    def test_all_concepts_have_required_fields(self):
        """Every concept definition must have id, name, category, keywords."""
        for c in ALL_CONCEPTS:
            assert "id" in c, f"Missing id: {c}"
            assert "name" in c, f"Missing name: {c}"
            assert "category" in c, f"Missing category: {c}"
            assert "keywords" in c and len(c["keywords"]) > 0, f"Missing keywords: {c['id']}"
            assert "article_patterns" in c, f"Missing article_patterns: {c['id']}"

    def test_concept_ids_unique(self):
        """All concept IDs must be unique."""
        ids = [c["id"] for c in ALL_CONCEPTS]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_concept_count_at_least_40(self):
        """We should have at least 40 curated concepts."""
        assert len(ALL_CONCEPTS) >= 40

    def test_extract_all_returns_concepts_and_rels(self, sample_articles):
        extractor = ConceptExtractor()
        concepts, rels = extractor.extract_all(sample_articles)
        assert len(concepts) >= 40
        assert len(rels) > 0
        # All concepts should have type field
        for c in concepts:
            assert c["type"] == "Concept"

    def test_gdpr_principles_present(self):
        """All 9 GDPR principles from Art 5 should be in concepts."""
        principle_ids = [c["id"] for c in ALL_CONCEPTS if c["category"] == "gdpr_principle"]
        assert len(principle_ids) == 9
        assert "CONCEPT_LAWFULNESS" in principle_ids
        assert "CONCEPT_ACCOUNTABILITY" in principle_ids

    def test_keyword_matching_finds_articles(self, sample_articles):
        """Keyword matching should find articles with relevant text."""
        extractor = ConceptExtractor()
        concepts, rels = extractor.extract_all(sample_articles)

        # CONCEPT_ACCOUNTABILITY should link to GDPR_ART_5 (contains "accountability")
        accountability = next(c for c in concepts if c["id"] == "CONCEPT_ACCOUNTABILITY")
        assert "GDPR_ART_5" in accountability["related_articles"]

    def test_concept_categories(self):
        """Should have 4 concept categories."""
        categories = set(c["category"] for c in ALL_CONCEPTS)
        assert "gdpr_principle" in categories
        assert "processing_operation" in categories
        assert "compliance_concept" in categories
        assert "ai_concept" in categories


# ── Right Extractor ───────────────────────────────────────────────────────────

class TestRightExtractor:
    def test_all_rights_have_required_fields(self):
        for r in ALL_RIGHTS:
            assert "id" in r
            assert "name" in r
            assert "regulation_id" in r
            assert "source_articles" in r and len(r["source_articles"]) > 0
            assert "right_holder" in r

    def test_right_ids_unique(self):
        ids = [r["id"] for r in ALL_RIGHTS]
        assert len(ids) == len(set(ids))

    def test_right_count(self):
        assert len(ALL_RIGHTS) >= 15

    def test_extract_all_returns_rights_and_rels(self):
        extractor = RightExtractor()
        rights, rels = extractor.extract_all()
        assert len(rights) >= 15
        assert len(rels) > 0
        for r in rights:
            assert r["type"] == "Right"

    def test_gdpr_rights_present(self):
        gdpr_rights = [r for r in ALL_RIGHTS if r["regulation_id"] == "GDPR"]
        assert len(gdpr_rights) >= 12
        ids = [r["id"] for r in gdpr_rights]
        assert "RIGHT_ACCESS" in ids
        assert "RIGHT_ERASURE" in ids
        assert "RIGHT_PORTABILITY" in ids

    def test_ai_act_rights_present(self):
        ai_rights = [r for r in ALL_RIGHTS if r["regulation_id"] == "EU_AI_ACT"]
        assert len(ai_rights) >= 3
        ids = [r["id"] for r in ai_rights]
        assert "RIGHT_AI_EXPLANATION" in ids

    def test_cross_regulation_links(self):
        extractor = RightExtractor()
        _, rels = extractor.extract_all()
        cross_refs = [r for r in rels if r.get("properties", {}).get("link_type") == "cross_regulation_right"]
        assert len(cross_refs) >= 3


# ── Definition Extractor ──────────────────────────────────────────────────────

class TestDefinitionExtractor:
    def test_extract_from_article(self, sample_definition_article):
        extractor = DefinitionExtractor()
        defs = extractor.extract_from_article(sample_definition_article, "GDPR")
        assert len(defs) == 2
        terms = [d["term"] for d in defs]
        assert "personal data" in terms
        assert "processing" in terms

    def test_definition_has_required_fields(self, sample_definition_article):
        extractor = DefinitionExtractor()
        defs = extractor.extract_from_article(sample_definition_article, "GDPR")
        for d in defs:
            assert d["type"] == "Definition"
            assert d["regulation_id"] == "GDPR"
            assert d["article_reference"] == "GDPR_ART_4"
            assert d["definition_text"]


# ── Obligation Extractor ──────────────────────────────────────────────────────

class TestObligationExtractor:
    def test_extract_from_articles(self, sample_articles):
        extractor = ObligationExtractor(use_llm=False)
        obls, exs = extractor.extract_from_articles(
            [a for a in sample_articles if a["regulation_id"] == "GDPR"], "GDPR"
        )
        assert len(obls) > 0

    def test_obligation_type_detection(self):
        extractor = ObligationExtractor(use_llm=False)
        results = extractor._classify_paragraph(
            "The controller shall ensure that personal data are processed lawfully."
        )
        types = [t for t, _ in results]
        assert "SHALL" in types or "MUST" in types

    def test_prohibition_detection(self):
        extractor = ObligationExtractor(use_llm=False)
        results = extractor._classify_paragraph(
            "Processing of special categories shall be prohibited."
        )
        types = [t for t, _ in results]
        assert "MUST_NOT" in types

    def test_actor_detection(self):
        extractor = ObligationExtractor(use_llm=False)
        bearer = extractor._detect_actor(
            "The controller shall implement appropriate measures.", is_bearer=True
        )
        assert bearer == "ACTOR_CONTROLLER"
