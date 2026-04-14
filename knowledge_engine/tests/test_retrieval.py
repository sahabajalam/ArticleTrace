"""Tests for retrieval engine and reasoning engine."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.stores.vector_store import VectorStore
from src.retrieval.query_models import (
    ComplianceQueryRequest,
    ComplianceQueryResponse,
    Citation,
    ConfidenceLevel,
    ReasoningStep,
    ANSWER_TEMPLATES,
)


# ── Vector Store ──────────────────────────────────────────────────────────────

class TestVectorStore:
    def test_add_and_count(self, mock_vector_store):
        vs = mock_vector_store
        ids = ["doc1", "doc2"]
        texts = ["Hello world", "Goodbye world"]
        embeddings = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        metas = [{"type": "test"}, {"type": "test"}]

        added = vs.add_documents("articles", ids, texts, embeddings, metas)
        assert added == 2
        assert vs.count("articles") == 2

    def test_deduplication(self, mock_vector_store):
        vs = mock_vector_store
        ids = ["doc1", "doc1"]
        texts = ["Hello", "Hello"]
        embeddings = [[1.0, 0.0], [1.0, 0.0]]
        metas = [{"type": "t"}, {"type": "t"}]

        added = vs.add_documents("articles", ids, texts, embeddings, metas)
        assert added == 1

    def test_query_returns_nearest(self, mock_vector_store):
        vs = mock_vector_store
        ids = ["a", "b", "c"]
        texts = ["Alpha", "Beta", "Charlie"]
        embeddings = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        metas = [{"type": "x"}, {"type": "x"}, {"type": "x"}]

        vs.add_documents("articles", ids, texts, embeddings, metas)
        result = vs.query("articles", [1.0, 0.0, 0.0], n_results=2)

        assert result["ids"][0][0] == "a"  # Most similar to [1,0,0]
        assert len(result["ids"][0]) == 2

    def test_metadata_filter(self, mock_vector_store):
        vs = mock_vector_store
        ids = ["gdpr1", "ai1"]
        texts = ["GDPR article", "AI Act article"]
        embeddings = [[1.0, 0.0], [0.9, 0.1]]
        metas = [{"regulation_id": "GDPR"}, {"regulation_id": "EU_AI_ACT"}]

        vs.add_documents("articles", ids, texts, embeddings, metas)
        result = vs.query("articles", [1.0, 0.0], n_results=2, where={"regulation_id": "GDPR"})

        assert len(result["ids"][0]) == 1
        assert result["ids"][0][0] == "gdpr1"

    def test_cosine_similarity(self):
        sim = VectorStore._cosine_similarity([1.0, 0.0], [1.0, 0.0])
        assert abs(sim - 1.0) < 0.001

        sim = VectorStore._cosine_similarity([1.0, 0.0], [0.0, 1.0])
        assert abs(sim) < 0.001

    def test_clear_all(self, mock_vector_store):
        vs = mock_vector_store
        vs.add_documents("articles", ["a"], ["text"], [[1.0]], [{"t": "t"}])
        assert vs.count("articles") == 1
        vs.clear_all()
        assert vs.count("articles") == 0

    def test_collections_include_concepts_and_rights(self):
        assert "concepts" in VectorStore.COLLECTIONS
        assert "rights" in VectorStore.COLLECTIONS


# ── Query Models ──────────────────────────────────────────────────────────────

class TestQueryModels:
    def test_compliance_query_request(self):
        req = ComplianceQueryRequest(question="test question")
        assert req.question == "test question"
        assert req.max_results == 10
        assert req.include_reasoning is True

    def test_compliance_query_response(self):
        resp = ComplianceQueryResponse(
            question="test",
            answer="test answer",
            answer_type="prohibition",
            confidence=ConfidenceLevel.HIGH,
        )
        assert resp.answer_type == "prohibition"
        assert resp.confidence == ConfidenceLevel.HIGH

    def test_citation_model(self):
        c = Citation(
            entity_id="GDPR_ART_5",
            entity_type="Article",
            regulation_id="GDPR",
            article_number="5",
        )
        assert c.entity_id == "GDPR_ART_5"

    def test_answer_templates_all_present(self):
        expected = ["prohibition", "obligation", "conditional_permission",
                    "non_applicable", "legal_uncertainty", "general"]
        for t in expected:
            assert t in ANSWER_TEMPLATES


# ── Reasoning Engine (unit tests without LLM) ────────────────────────────────

class TestReasoningEngine:
    def test_classify_intent_prohibition(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        # Create a minimal instance just for intent classification
        engine = ReasoningEngine.__new__(ReasoningEngine)
        assert engine._classify_intent("Is social scoring prohibited?") == "prohibition"

    def test_classify_intent_obligation(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)
        assert engine._classify_intent("What obligations does a controller have?") == "obligation"

    def test_classify_intent_right(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)
        assert engine._classify_intent("What is the right to access personal data?") == "right"

    def test_classify_intent_cross_regulation(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)
        assert engine._classify_intent("How do GDPR and AI Act interact on transparency?") == "cross_regulation"

    def test_classify_intent_general(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)
        assert engine._classify_intent("What is data protection?") == "general"

    def test_extract_citations(self, sample_retrieval_results):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        answer = "Under Article 22 GDPR, data subjects have rights. Article 14 AI Act requires human oversight."
        citations = engine._extract_citations(answer, sample_retrieval_results)

        ids = [c.entity_id for c in citations]
        assert "GDPR_ART_22" in ids
        assert "AIACT_ART_14" in ids

    def test_validate_citations(self, sample_retrieval_results):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        citations = [
            Citation(entity_id="GDPR_ART_22", entity_type="Article"),
            Citation(entity_id="GDPR_ART_99", entity_type="Article"),  # Not in results
        ]
        validated = engine._validate_citations(citations, sample_retrieval_results)

        # First should be verified, second unverified
        assert validated[0].relevance_score >= 0.8
        assert validated[1].relevance_score < 0.8

    def test_score_confidence_high(self, sample_retrieval_results):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        citations = [Citation(entity_id="GDPR_ART_22", relevance_score=1.0)]
        confidence = engine._score_confidence(sample_retrieval_results, citations)
        assert confidence in (ConfidenceLevel.HIGH, ConfidenceLevel.MEDIUM)

    def test_score_confidence_low_empty(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        confidence = engine._score_confidence([], [])
        assert confidence == ConfidenceLevel.LOW

    def test_determine_answer_type(self):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        assert engine._determine_answer_type("prohibition", "This is prohibited.") == "prohibition"
        assert engine._determine_answer_type("exemption", "GDPR does not apply.") == "non_applicable"
        assert engine._determine_answer_type("general", "Here is some info.") == "general"

    def test_build_context(self, sample_retrieval_results):
        from src.retrieval.reasoning_engine import ReasoningEngine
        engine = ReasoningEngine.__new__(ReasoningEngine)

        context = engine._build_context(sample_retrieval_results)
        assert "GDPR_ART_22" in context
        assert "AIACT_ART_14" in context
