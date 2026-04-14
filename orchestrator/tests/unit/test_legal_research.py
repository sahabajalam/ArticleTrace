"""Unit tests for Legal Research Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json

from src.state.compliance_state import create_initial_state, LegalCitation


class TestLegalResearchAgent:
    """Tests for Legal Research Agent."""

    @pytest.fixture
    def mock_state(self):
        """Create state for testing."""
        state = create_initial_state(
            system_description="Facial recognition system for employee attendance tracking in corporate offices.",
            system_type="facial_recognition",
            deployment_context="employee_monitoring",
            company_name="TechCorp",
        )
        state["risk_classification"] = {
            "category": "HIGH_RISK",
            "article": "Article 6",
            "annex": "Annex III",
            "subcategory": "biometric_identification",
            "confidence": 0.92,
        }
        state["gdpr_audit"] = {
            "gdpr_compliant": False,
            "violations": [
                {"article": "Article 9", "issue": "Biometric data processing"},
                {"article": "Article 35", "issue": "DPIA required"},
            ],
        }
        return state

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        assert agent.name == "legal_research"
        assert agent.graphrag_url is not None

    @pytest.mark.asyncio
    async def test_extract_legal_entities(self, mock_state):
        """Test entity extraction from context."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                json.dumps({
                    "system_types": ["facial_recognition", "biometric"],
                    "data_types": ["biometric_data"],
                    "concepts": ["automated_decision", "employee_monitoring"],
                    "gdpr_articles": ["Article 9", "Article 35"],
                    "eu_ai_act_articles": ["Article 6", "Annex III"],
                    "requirements": ["DPIA", "consent"],
                    "search_queries": ["facial recognition GDPR requirements"],
                }),
                0.01,
            )

            entities, cost = await agent._extract_legal_entities(
                mock_state["system_description"],
                mock_state["risk_classification"],
                mock_state["gdpr_audit"],
            )

            assert "system_types" in entities
            assert "data_types" in entities
            assert "gdpr_articles" in entities
            assert cost > 0

    @pytest.mark.asyncio
    async def test_extract_legal_entities_handles_invalid_json(self, mock_state):
        """Test entity extraction handles invalid JSON gracefully."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ("This is not valid JSON", 0.01)

            entities, cost = await agent._extract_legal_entities(
                mock_state["system_description"],
                mock_state["risk_classification"],
                mock_state["gdpr_audit"],
            )

            # Should return default structure
            assert "system_types" in entities
            assert "search_queries" in entities
            assert len(entities["search_queries"]) > 0

    @pytest.mark.asyncio
    async def test_query_graphrag_success(self, mock_state):
        """Test successful GraphRAG query."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "paths": [
                {
                    "nodes": [
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9", "title": "Special categories"},
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 35", "title": "DPIA"},
                    ],
                    "relationship": "REQUIRES",
                    "weight": 0.9,
                }
            ]
        }

        with patch.object(agent.http_client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            entities = {"system_types": ["facial_recognition"], "data_types": ["biometric"]}
            result = await agent._query_graphrag(entities)

            assert "paths" in result
            assert len(result["paths"]) > 0

    @pytest.mark.asyncio
    async def test_query_graphrag_failure(self, mock_state):
        """Test GraphRAG query failure handling."""
        from src.agents.legal_research import LegalResearchAgent
        from src.utils.error_handling import GraphRAGError
        import httpx

        agent = LegalResearchAgent()

        with patch.object(agent.http_client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")

            entities = {"system_types": ["facial_recognition"]}

            with pytest.raises(GraphRAGError):
                await agent._query_graphrag(entities)

    @pytest.mark.asyncio
    async def test_vector_search(self, mock_state):
        """Test vector search functionality."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "text": "Article 9 prohibits processing of biometric data...",
                    "score": 0.85,
                    "metadata": {"regulation": "GDPR", "article": "Article 9"},
                }
            ]
        }

        with patch.object(agent.http_client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            entities = {"search_queries": ["biometric data GDPR"]}
            result = await agent._vector_search("biometric data", entities)

            assert "results" in result
            assert len(result["results"]) > 0

    @pytest.mark.asyncio
    async def test_vector_search_failure_returns_empty(self, mock_state):
        """Test vector search returns empty on failure."""
        from src.agents.legal_research import LegalResearchAgent
        import httpx

        agent = LegalResearchAgent()

        with patch.object(agent.http_client, "post", new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = httpx.RequestError("Connection failed")

            result = await agent._vector_search("test query", {})

            assert result == {"results": []}

    def test_rank_and_merge_articles(self):
        """Test article ranking and merging."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        graph_results = {
            "paths": [
                {
                    "nodes": [
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9", "title": "Special categories"},
                    ],
                    "relationship": "REQUIRES",
                    "weight": 0.9,
                }
            ]
        }

        vector_results = {
            "results": [
                {
                    "text": "Article 35 requires DPIA...",
                    "score": 0.8,
                    "metadata": {"regulation": "GDPR", "article": "Article 35", "title": "DPIA"},
                }
            ]
        }

        articles = agent._rank_and_merge_articles(graph_results, vector_results)

        assert len(articles) == 2
        # Check that articles are sorted by relevance
        assert articles[0].relevance_score >= articles[1].relevance_score

    def test_rank_and_merge_handles_duplicates(self):
        """Test that duplicate articles are merged correctly."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        # Same article from both sources
        graph_results = {
            "paths": [
                {
                    "nodes": [
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9"},
                    ],
                    "weight": 0.7,
                    "relationship": "REQUIRES",
                }
            ]
        }

        vector_results = {
            "results": [
                {
                    "text": "Biometric data...",
                    "score": 0.8,
                    "metadata": {"regulation": "GDPR", "article": "Article 9"},
                }
            ]
        }

        articles = agent._rank_and_merge_articles(graph_results, vector_results)

        # Should only have one article with increased score
        assert len(articles) == 1
        assert articles[0].relevance_score > 0.7  # Score should be boosted

    def test_extract_relationship_chains(self):
        """Test relationship chain extraction."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        graph_results = {
            "paths": [
                {
                    "nodes": [
                        {"name": "Article 9"},
                        {"name": "Article 35"},
                    ],
                    "relationship": "TRIGGERS",
                }
            ]
        }

        chains = agent._extract_relationship_chains(graph_results)

        assert len(chains) == 1
        assert "Article 9" in chains[0]
        assert "TRIGGERS" in " ".join(chains[0])

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        # High confidence case
        articles = [
            LegalCitation(
                regulation="GDPR",
                article_number="Article 9",
                relevance_score=0.9,
            ),
            LegalCitation(
                regulation="GDPR",
                article_number="Article 35",
                relevance_score=0.85,
            ),
        ]
        chains = [["A", "->", "B"], ["C", "->", "D"]]

        confidence = agent._calculate_confidence(articles, chains)

        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be reasonably high

    def test_calculate_confidence_no_articles(self):
        """Test confidence calculation with no articles."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        confidence = agent._calculate_confidence([], [])

        assert confidence == 0.3  # Default low confidence

    @pytest.mark.asyncio
    async def test_fallback_research(self, mock_state):
        """Test fallback research when GraphRAG unavailable."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                json.dumps({
                    "paths": [
                        {
                            "nodes": [
                                {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9", "title": "Special categories"}
                            ],
                            "relationship": "REQUIRES",
                            "weight": 0.8,
                        }
                    ]
                }),
                0.01,
            )

            entities = {"system_types": ["facial_recognition"]}
            result = await agent._fallback_research(entities)

            assert "paths" in result

    @pytest.mark.asyncio
    async def test_execute_full_workflow(self, mock_state):
        """Test full execute workflow."""
        from src.agents.legal_research import LegalResearchAgent

        agent = LegalResearchAgent()

        # Mock entity extraction
        with patch.object(agent, "_extract_legal_entities", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = (
                {
                    "system_types": ["facial_recognition"],
                    "data_types": ["biometric"],
                    "concepts": [],
                    "gdpr_articles": ["Article 9"],
                    "eu_ai_act_articles": [],
                    "requirements": [],
                    "search_queries": ["facial recognition GDPR"],
                },
                0.01,
            )

            # Mock GraphRAG query
            with patch.object(agent, "_query_graphrag", new_callable=AsyncMock) as mock_graph:
                mock_graph.return_value = {
                    "paths": [
                        {
                            "nodes": [
                                {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9"}
                            ],
                            "weight": 0.9,
                            "relationship": "APPLIES_TO",
                        }
                    ]
                }

                # Mock vector search
                with patch.object(agent, "_vector_search", new_callable=AsyncMock) as mock_vector:
                    mock_vector.return_value = {"results": []}

                    result = await agent.execute(mock_state)

                    assert "legal_citations" in result
                    assert "confidence_scores" in result
                    assert result["current_step"] == "legal_researched"

    @pytest.mark.asyncio
    async def test_execute_handles_graphrag_failure(self, mock_state):
        """Test execute handles GraphRAG failure gracefully."""
        from src.agents.legal_research import LegalResearchAgent
        from src.utils.error_handling import GraphRAGError

        agent = LegalResearchAgent()

        with patch.object(agent, "_extract_legal_entities", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = (
                {"system_types": [], "data_types": [], "concepts": [], "gdpr_articles": [], "eu_ai_act_articles": [], "requirements": [], "search_queries": ["test"]},
                0.01,
            )

            with patch.object(agent, "_query_graphrag", new_callable=AsyncMock) as mock_graph:
                mock_graph.side_effect = GraphRAGError("legal_research", "API unavailable")

                with patch.object(agent, "_fallback_research", new_callable=AsyncMock) as mock_fallback:
                    mock_fallback.return_value = {"paths": []}

                    with patch.object(agent, "_vector_search", new_callable=AsyncMock) as mock_vector:
                        mock_vector.return_value = {"results": []}

                        result = await agent.execute(mock_state)

                        # Should still complete with fallback
                        assert "legal_citations" in result
                        mock_fallback.assert_called_once()


class TestLegalCitationModel:
    """Tests for LegalCitation model."""

    def test_legal_citation_creation(self):
        """Test LegalCitation model creation."""
        citation = LegalCitation(
            regulation="GDPR",
            article_number="Article 9",
            title="Special categories of personal data",
            text_snippet="Processing of biometric data...",
            relevance_score=0.85,
            relationship="APPLIES_TO",
        )

        assert citation.regulation == "GDPR"
        assert citation.article_number == "Article 9"
        assert citation.relevance_score == 0.85

    def test_legal_citation_defaults(self):
        """Test LegalCitation default values."""
        citation = LegalCitation(
            regulation="EU_AI_ACT",
            article_number="Article 6",
        )

        assert citation.title is None
        assert citation.text_snippet is None
        assert citation.relevance_score == 0.0
        assert citation.relationship is None

    def test_legal_citation_serialization(self):
        """Test LegalCitation serialization."""
        citation = LegalCitation(
            regulation="GDPR",
            article_number="Article 35",
            relevance_score=0.9,
        )

        data = citation.model_dump()

        assert data["regulation"] == "GDPR"
        assert data["article_number"] == "Article 35"
        assert data["relevance_score"] == 0.9
