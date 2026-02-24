"""Legal Research Agent for GraphRAG integration with Project 3."""

import json
from datetime import datetime
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.agents.base import BaseAgent
from src.config import settings
from src.state.compliance_state import ComplianceState, LegalCitation
from src.utils.error_handling import GraphRAGError


class LegalResearchAgent(BaseAgent):
    """
    Legal Research Agent that queries Project 3 GraphRAG.

    Performs multi-hop reasoning across GDPR and EU AI Act
    to find relevant legal citations and relationship chains.
    """

    def __init__(self):
        super().__init__(
            name="legal_research",
            model=settings.secondary_model,
        )
        self.graphrag_url = settings.graphrag_api_url
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Execute legal research using GraphRAG.

        Returns state update with legal_citations.
        """
        start_time = datetime.utcnow()
        total_cost = 0.0

        system_description = state["system_description"]
        risk_classification = state.get("risk_classification", {})
        gdpr_audit = state.get("gdpr_audit", {})

        # Step 1: Extract legal entities from the context
        entities, cost = await self._extract_legal_entities(
            system_description,
            risk_classification,
            gdpr_audit,
        )
        total_cost += cost

        # Step 2: Query GraphRAG for relevant articles
        try:
            graph_results = await self._query_graphrag(entities)
        except GraphRAGError as e:
            self.logger.warning(
                "GraphRAG query failed, falling back to LLM-based research",
                error=str(e),
            )
            graph_results = await self._fallback_research(entities)

        # Step 3: Perform vector search for supporting context
        try:
            vector_results = await self._vector_search(
                query=system_description,
                entities=entities,
            )
        except Exception as e:
            self.logger.warning("Vector search failed", error=str(e))
            vector_results = {"results": []}

        # Step 4: Synthesize findings
        relevant_articles = self._rank_and_merge_articles(graph_results, vector_results)
        relationship_chains = self._extract_relationship_chains(graph_results)

        # Calculate confidence based on results
        confidence = self._calculate_confidence(relevant_articles, relationship_chains)

        legal_research = {
            "relevant_articles": [a.model_dump() for a in relevant_articles],
            "relationship_chains": relationship_chains,
            "confidence": confidence,
            "query_used": json.dumps(entities),
            "entities_extracted": entities,
        }

        duration = (datetime.utcnow() - start_time).total_seconds()

        self.logger.info(
            "Legal research complete",
            articles_found=len(relevant_articles),
            chains_found=len(relationship_chains),
            confidence=confidence,
        )

        audit_update = self.build_audit_update(
            state,
            action="legal_research",
            output=legal_research,
            cost_usd=total_cost,
            duration_seconds=duration,
        )

        return {
            "legal_citations": legal_research,
            "confidence_scores": {
                "legal_research": confidence,
            },
            "current_step": "legal_researched",
            **audit_update,
        }

    async def _extract_legal_entities(
        self,
        system_description: str,
        risk_classification: dict[str, Any],
        gdpr_audit: dict[str, Any],
    ) -> tuple[dict[str, Any], float]:
        """Extract legal entities for graph traversal."""
        # Build context from previous agents
        context_parts = [f"System: {system_description}"]

        if risk_classification:
            context_parts.append(f"Risk Category: {risk_classification.get('category', 'unknown')}")
            if risk_classification.get("annex"):
                context_parts.append(f"Relevant Annex: {risk_classification.get('annex')}")

        if gdpr_audit:
            violations = gdpr_audit.get("violations", [])
            if violations:
                articles = [v.get("article", "") for v in violations]
                context_parts.append(f"GDPR Violations: {', '.join(articles)}")

        context = "\n".join(context_parts)

        prompt = f"""Extract legal entities from this AI compliance context for graph-based legal research.

CONTEXT:
{context}

Extract entities relevant to EU AI Act and GDPR compliance.

Return a JSON object:
{{
    "system_types": ["list of AI system types, e.g., facial_recognition, credit_scoring"],
    "data_types": ["list of data types, e.g., biometric_data, personal_data"],
    "concepts": ["list of legal concepts, e.g., automated_decision, special_category_data"],
    "gdpr_articles": ["list of relevant GDPR articles, e.g., Article 9, Article 22"],
    "eu_ai_act_articles": ["list of relevant EU AI Act articles/annexes"],
    "requirements": ["list of requirements, e.g., DPIA, conformity_assessment"],
    "search_queries": ["list of natural language queries for vector search"]
}}

Return ONLY valid JSON."""

        response, cost = await self.invoke_llm(prompt)

        try:
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            entities = json.loads(response)
        except json.JSONDecodeError:
            entities = {
                "system_types": [],
                "data_types": [],
                "concepts": [],
                "gdpr_articles": [],
                "eu_ai_act_articles": [],
                "requirements": [],
                "search_queries": [system_description[:200]],
            }

        return entities, cost

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def _query_graphrag(self, entities: dict[str, Any]) -> dict[str, Any]:
        """
        Query Project 3 GraphRAG API.

        Performs graph traversal to find connected legal articles.
        """
        # Build start entities for graph traversal
        start_entities = []
        start_entities.extend(entities.get("system_types", []))
        start_entities.extend(entities.get("data_types", []))
        start_entities.extend(entities.get("concepts", []))

        if not start_entities:
            # Fallback to article-based search
            start_entities.extend(entities.get("gdpr_articles", []))
            start_entities.extend(entities.get("eu_ai_act_articles", []))

        try:
            response = await self.http_client.post(
                f"{self.graphrag_url}/api/v1/graph/traverse",
                json={
                    "start_entities": start_entities,
                    "relationship_types": ["REGULATES", "REQUIRES", "PROHIBITS", "APPLIES_TO", "DEFINES"],
                    "max_hops": 2,
                    "limit": 20,
                },
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise GraphRAGError(
                    "legal_research",
                    f"GraphRAG API returned {response.status_code}",
                    {"status_code": response.status_code},
                )
        except httpx.RequestError as e:
            raise GraphRAGError(
                "legal_research",
                f"GraphRAG API request failed: {str(e)}",
            )

    async def _vector_search(
        self,
        query: str,
        entities: dict[str, Any],
    ) -> dict[str, Any]:
        """Perform vector search for supporting text."""
        search_queries = entities.get("search_queries", [query[:200]])

        try:
            response = await self.http_client.post(
                f"{self.graphrag_url}/api/v1/vector/search",
                json={
                    "query": search_queries[0] if search_queries else query[:200],
                    "top_k": 10,
                    "filter_regulations": ["GDPR", "EU_AI_ACT"],
                },
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"results": []}
        except httpx.RequestError:
            return {"results": []}

    async def _fallback_research(self, entities: dict[str, Any]) -> dict[str, Any]:
        """
        Fallback when GraphRAG is unavailable.

        Uses LLM to generate relevant citations.
        """
        prompt = f"""Based on these legal entities, identify the most relevant GDPR and EU AI Act articles.

ENTITIES:
{json.dumps(entities, indent=2)}

For each relevant article, provide:
1. The regulation (GDPR or EU_AI_ACT)
2. The article/annex number
3. Why it's relevant
4. How it connects to other articles (relationship chains)

Return a JSON object:
{{
    "paths": [
        {{
            "nodes": [
                {{"type": "ARTICLE", "regulation": "GDPR", "number": "Article X", "title": "Title"}}
            ],
            "relationship": "REQUIRES",
            "weight": 0.9
        }}
    ]
}}

Return ONLY valid JSON."""

        response, cost = await self.invoke_llm(prompt)

        try:
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            return json.loads(response)
        except json.JSONDecodeError:
            return {"paths": []}

    def _rank_and_merge_articles(
        self,
        graph_results: dict[str, Any],
        vector_results: dict[str, Any],
    ) -> list[LegalCitation]:
        """Rank and merge articles from graph and vector search."""
        articles_map: dict[str, LegalCitation] = {}

        # Process graph results
        for path in graph_results.get("paths", []):
            for node in path.get("nodes", []):
                if node.get("type") == "ARTICLE" or node.get("type") == "Annex":
                    key = f"{node.get('regulation', 'unknown')}_{node.get('number', 'unknown')}"
                    if key not in articles_map:
                        articles_map[key] = LegalCitation(
                            regulation=node.get("regulation", "unknown"),
                            article_number=node.get("number", "unknown"),
                            title=node.get("title"),
                            relevance_score=path.get("weight", 0.5),
                            relationship=path.get("relationship"),
                        )
                    else:
                        # Increase score if found multiple times
                        articles_map[key].relevance_score = min(
                            1.0,
                            articles_map[key].relevance_score + 0.1,
                        )

        # Process vector results
        for result in vector_results.get("results", []):
            metadata = result.get("metadata", {})
            key = f"{metadata.get('regulation', 'unknown')}_{metadata.get('article', 'unknown')}"
            if key not in articles_map:
                articles_map[key] = LegalCitation(
                    regulation=metadata.get("regulation", "unknown"),
                    article_number=metadata.get("article", "unknown"),
                    title=metadata.get("title"),
                    text_snippet=result.get("text", "")[:300],
                    relevance_score=result.get("score", 0.5),
                )
            else:
                # Add text snippet if not present
                if not articles_map[key].text_snippet:
                    articles_map[key].text_snippet = result.get("text", "")[:300]

        # Sort by relevance score
        sorted_articles = sorted(
            articles_map.values(),
            key=lambda x: x.relevance_score,
            reverse=True,
        )

        return sorted_articles[:15]  # Return top 15 most relevant

    def _extract_relationship_chains(self, graph_results: dict[str, Any]) -> list[list[str]]:
        """Extract multi-hop reasoning chains from graph results."""
        chains = []

        for path in graph_results.get("paths", []):
            nodes = path.get("nodes", [])
            relationship = path.get("relationship", "RELATED_TO")

            if len(nodes) >= 2:
                chain = []
                for i, node in enumerate(nodes):
                    node_str = f"{node.get('name', node.get('number', 'unknown'))}"
                    chain.append(node_str)
                    if i < len(nodes) - 1:
                        chain.append(f"→ {relationship} →")

                chains.append(chain)

        return chains[:10]  # Return top 10 chains

    def _calculate_confidence(
        self,
        articles: list[LegalCitation],
        chains: list[list[str]],
    ) -> float:
        """Calculate overall confidence score."""
        if not articles:
            return 0.3

        # Base confidence on number and quality of results
        article_score = min(1.0, len(articles) / 10)  # More articles = higher confidence
        chain_score = min(1.0, len(chains) / 5)  # More chains = higher confidence

        avg_relevance = sum(a.relevance_score for a in articles) / len(articles)

        confidence = (article_score * 0.3) + (chain_score * 0.3) + (avg_relevance * 0.4)
        return round(min(0.95, confidence), 2)

    async def close(self):
        """Close HTTP client."""
        await self.http_client.aclose()
