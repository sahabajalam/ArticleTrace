"""Shared test fixtures for EU AI Knowledge Base tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_gdpr_article() -> dict:
    """A sample GDPR article dict (Art 5 - Principles)."""
    return {
        "id": "GDPR_ART_5",
        "type": "Article",
        "name": "Article 5 - Principles relating to processing of personal data",
        "regulation_id": "GDPR",
        "article_number": "5",
        "full_text": (
            "1. Personal data shall be: (a) processed lawfully, fairly and in a "
            "transparent manner in relation to the data subject; (b) collected for "
            "specified, explicit and legitimate purposes and not further processed in "
            "a manner that is incompatible with those purposes; (c) adequate, relevant "
            "and limited to what is necessary in relation to the purposes for which "
            "they are processed (data minimisation); (d) accurate and, where necessary, "
            "kept up to date; (e) kept in a form which permits identification of data "
            "subjects for no longer than is necessary; (f) processed in a manner that "
            "ensures appropriate security of the personal data. "
            "2. The controller shall be responsible for, and be able to demonstrate "
            "compliance with, paragraph 1 (accountability)."
        ),
        "paragraphs": {
            "1": {
                "intro": "Personal data shall be:",
                "a": "processed lawfully, fairly and in a transparent manner",
                "b": "collected for specified, explicit and legitimate purposes",
                "c": "adequate, relevant and limited to what is necessary",
                "d": "accurate and, where necessary, kept up to date",
                "e": "kept in a form which permits identification for no longer than necessary",
                "f": "processed in a manner that ensures appropriate security",
            },
            "2": "The controller shall be responsible for, and be able to demonstrate compliance with, paragraph 1 (accountability).",
        },
    }


@pytest.fixture
def sample_ai_act_article() -> dict:
    """A sample AI Act article dict (Art 14 - Human Oversight)."""
    return {
        "id": "AIACT_ART_14",
        "type": "Article",
        "name": "Article 14 - Human oversight",
        "regulation_id": "EU_AI_ACT",
        "article_number": "14",
        "full_text": (
            "1. High-risk AI systems shall be designed and developed in such a way "
            "that they can be effectively overseen by natural persons during the "
            "period in which they are in use. 2. Human oversight shall aim to prevent "
            "or minimise risks to health, safety or fundamental rights."
        ),
        "paragraphs": {
            "1": "High-risk AI systems shall be designed and developed in such a way that they can be effectively overseen by natural persons.",
            "2": "Human oversight shall aim to prevent or minimise risks to health, safety or fundamental rights.",
        },
    }


@pytest.fixture
def sample_articles(sample_gdpr_article, sample_ai_act_article) -> list[dict]:
    """List of sample articles for extraction tests."""
    return [sample_gdpr_article, sample_ai_act_article]


@pytest.fixture
def sample_definition_article() -> dict:
    """A sample GDPR Art 4 (definitions) article."""
    return {
        "id": "GDPR_ART_4",
        "type": "Article",
        "name": "Article 4 - Definitions",
        "regulation_id": "GDPR",
        "article_number": "4",
        "full_text": (
            "(1) 'personal data' means any information relating to an identified "
            "or identifiable natural person; "
            "(2) 'processing' means any operation or set of operations which is "
            "performed on personal data;"
        ),
        "paragraphs": {},
    }


@pytest.fixture
def mock_vector_store(tmp_path):
    """Create a temporary VectorStore for testing."""
    from src.stores.vector_store import VectorStore
    return VectorStore(persist_dir=str(tmp_path / "test_vectors"))


@pytest.fixture
def sample_retrieval_results() -> list[dict]:
    """Sample retrieval results for reasoning engine tests."""
    return [
        {
            "entity_id": "GDPR_ART_22",
            "rrf_score": 0.032,
            "sources": ["vector", "graph"],
            "in_both": True,
            "metadata": {"type": "Article", "regulation_id": "GDPR"},
            "document": "Article 22 - Automated individual decision-making, including profiling. The data subject shall have the right not to be subject to a decision based solely on automated processing.",
            "vector_similarity": 0.85,
            "graph_score": 0.5,
            "vector_rank": 1,
            "graph_rank": 2,
        },
        {
            "entity_id": "AIACT_ART_14",
            "rrf_score": 0.028,
            "sources": ["vector"],
            "in_both": False,
            "metadata": {"type": "Article", "regulation_id": "EU_AI_ACT"},
            "document": "Article 14 - Human oversight. High-risk AI systems shall be designed for effective human oversight.",
            "vector_similarity": 0.78,
            "graph_score": 0,
            "vector_rank": 2,
            "graph_rank": "-",
        },
    ]
