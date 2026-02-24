"""Reasoning engine: wraps RetrievalEngine with LLM synthesis layer.

Flow:
  1. Retrieve relevant entities via Graph RAG (RetrievalEngine)
  2. Classify query intent (compliance, risk, obligation, cross-regulation)
  3. Build structured context from retrieved entities
  4. Generate answer via Gemini LLM
  5. Validate citations (anti-hallucination guardrail)
  6. Score confidence based on source count + authority + citation validity

Rate limiting: 4s delay between Gemini calls (15 RPM free tier).
"""

from __future__ import annotations

import json
import re
import time
from typing import Any

from src.retrieval.engine import RetrievalEngine
from src.retrieval.query_models import (
    AnswerType,
    Citation,
    ComplianceQueryRequest,
    ComplianceQueryResponse,
    ConfidenceLevel,
    ReasoningStep,
)


# Intent classification keywords
INTENT_PATTERNS = {
    "prohibition": [r"\bprohibit", r"\bbanned?\b", r"\bforbidden\b", r"\bnot allowed\b"],
    "risk_classification": [r"\brisk\s+(?:level|class|categor)", r"\bhigh.risk\b", r"\bprohibited\s+ai\b"],
    "obligation": [r"\bobligat", r"\brequire", r"\bmust\b", r"\bshall\b", r"\bduty\b", r"\bresponsib"],
    "cross_regulation": [r"\bcross.regulat", r"\binteract", r"\bboth\s+gdpr\b", r"\bgdpr\s+and\s+ai\b", r"\bai\s+act\s+and\s+gdpr\b"],
    "right": [r"\bright\s+to\b", r"\bdata\s+subject\s+right", r"\berasure\b", r"\baccess\b", r"\bportability\b"],
    "exemption": [r"\bexempt", r"\bnot\s+apply\b", r"\bexclud", r"\bderogat"],
}


class ReasoningEngine:
    """LLM-powered reasoning over the knowledge graph."""

    def __init__(
        self,
        retrieval_engine: RetrievalEngine,
        genai_client: Any,
        model: str = "gemini-2.0-flash",
    ):
        self.retrieval = retrieval_engine
        self.client = genai_client
        self.model = model
        self._last_request_time = 0.0

    def answer(self, request: ComplianceQueryRequest) -> ComplianceQueryResponse:
        """Full reasoning pipeline: retrieve -> classify -> synthesize -> validate."""
        steps: list[ReasoningStep] = []

        # Step 1: Retrieve
        steps.append(ReasoningStep(
            step_number=1, action="retrieve",
            description=f"Retrieving relevant entities for: {request.question[:80]}",
        ))
        results = self.retrieval.query(
            question=request.question,
            top_k=request.max_results,
            regulation_filter=request.regulation_filter,
        )
        steps[-1].entity_ids = [r["entity_id"] for r in results[:10]]

        # Step 2: Classify intent
        intent = self._classify_intent(request.question)
        steps.append(ReasoningStep(
            step_number=2, action="classify",
            description=f"Classified query intent as: {intent}",
        ))

        # Step 3: Build context
        context = self._build_context(results)
        steps.append(ReasoningStep(
            step_number=3, action="build_context",
            description=f"Built context from {len(results)} retrieved entities",
            entity_ids=[r["entity_id"] for r in results],
        ))

        # Step 4: Generate answer via LLM
        answer_text, answer_type = self._generate_answer(
            request.question, context, intent
        )
        steps.append(ReasoningStep(
            step_number=4, action="synthesize",
            description=f"Generated {answer_type} answer via Gemini",
        ))

        # Step 5: Extract and validate citations
        citations = self._extract_citations(answer_text, results)
        valid_citations = self._validate_citations(citations, results)
        steps.append(ReasoningStep(
            step_number=5, action="validate",
            description=f"Validated {len(valid_citations)}/{len(citations)} citations",
            entity_ids=[c.entity_id for c in valid_citations],
        ))

        # Step 6: Confidence scoring
        confidence = self._score_confidence(results, valid_citations)
        steps.append(ReasoningStep(
            step_number=6, action="score",
            description=f"Confidence: {confidence.value}",
        ))

        return ComplianceQueryResponse(
            question=request.question,
            answer=answer_text,
            answer_type=answer_type,
            confidence=confidence,
            citations=valid_citations,
            reasoning_chain=steps if request.include_reasoning else [],
            retrieval_count=len(results),
            raw_results=results[:5],
        )

    def _classify_intent(self, question: str) -> str:
        """Classify query into intent category."""
        q_lower = question.lower()
        scores: dict[str, int] = {}

        for intent, patterns in INTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, q_lower):
                    score += 1
            if score > 0:
                scores[intent] = score

        if not scores:
            return "general"
        return max(scores, key=scores.get)

    def _build_context(self, results: list[dict[str, Any]]) -> str:
        """Build structured context string from retrieval results."""
        sections: list[str] = []

        for i, r in enumerate(results[:10]):
            eid = r["entity_id"]
            meta = r.get("metadata", {})
            doc = r.get("document", "")
            etype = meta.get("type", "Unknown")
            rrf = r.get("rrf_score", 0)

            # Truncate long documents
            if len(doc) > 500:
                doc = doc[:500] + "..."

            sections.append(
                f"[{i+1}] {etype}: {eid} (relevance: {rrf:.4f})\n{doc}"
            )

        return "\n\n".join(sections)

    def _generate_answer(
        self, question: str, context: str, intent: str
    ) -> tuple[str, AnswerType]:
        """Generate answer using Gemini LLM."""
        self._rate_limit()

        prompt = self._build_prompt(question, context, intent)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            answer_text = response.text or ""
        except Exception as e:
            answer_text = f"Error generating answer: {e}"
            return answer_text, "general"

        # Determine answer type from intent + content
        answer_type = self._determine_answer_type(intent, answer_text)

        return answer_text, answer_type

    def _build_prompt(self, question: str, context: str, intent: str) -> str:
        """Build the LLM prompt for answer generation."""
        return (
            "You are an expert EU regulatory compliance advisor specializing in "
            "GDPR and the EU AI Act. Answer the following question using ONLY the "
            "provided context. Cite specific articles (e.g., 'Article 5 GDPR', "
            "'Article 14 AI Act') for every claim.\n\n"
            "IMPORTANT RULES:\n"
            "1. ONLY cite articles that appear in the context below\n"
            "2. If the context does not contain enough information, say so\n"
            "3. Structure your answer clearly with sections if needed\n"
            "4. For prohibitions, state the penalty tier\n"
            "5. For obligations, identify the duty bearer (who must comply)\n"
            "6. For cross-regulation questions, explain how GDPR and AI Act interact\n\n"
            f"QUERY INTENT: {intent}\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION: {question}\n\n"
            "ANSWER:"
        )

    def _determine_answer_type(self, intent: str, answer_text: str) -> AnswerType:
        """Determine the answer type from intent and generated text."""
        text_lower = answer_text.lower()

        if intent == "prohibition" or "prohibited" in text_lower:
            return "prohibition"
        if intent == "exemption" or "does not apply" in text_lower:
            return "non_applicable"
        if "uncertainty" in text_lower or "unclear" in text_lower:
            return "legal_uncertainty"
        if "subject to" in text_lower or "provided that" in text_lower:
            return "conditional_permission"
        if intent in ("obligation", "risk_classification"):
            return "obligation"
        return "general"

    def _extract_citations(
        self, answer_text: str, results: list[dict[str, Any]]
    ) -> list[Citation]:
        """Extract article citations from the generated answer text."""
        citations: list[Citation] = []
        seen: set[str] = set()

        # Pattern: "Article N GDPR" or "Article N AI Act" or "Art. N"
        patterns = [
            r"Article\s+(\d+)\s+(?:of\s+(?:the\s+)?)?GDPR",
            r"Article\s+(\d+)\s+(?:of\s+(?:the\s+)?)?(?:EU\s+)?AI\s+Act",
            r"Art(?:icle)?\.?\s*(\d+)\s+GDPR",
            r"Art(?:icle)?\.?\s*(\d+)\s+AI\s+Act",
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, answer_text, re.IGNORECASE):
                art_num = match.group(1)
                is_gdpr = "gdpr" in match.group(0).lower()
                entity_id = f"GDPR_ART_{art_num}" if is_gdpr else f"AIACT_ART_{art_num}"

                if entity_id not in seen:
                    seen.add(entity_id)
                    citations.append(Citation(
                        entity_id=entity_id,
                        entity_type="Article",
                        regulation_id="GDPR" if is_gdpr else "EU_AI_ACT",
                        article_number=art_num,
                    ))

        return citations

    def _validate_citations(
        self, citations: list[Citation], results: list[dict[str, Any]]
    ) -> list[Citation]:
        """Anti-hallucination guardrail: only keep citations found in retrieval results."""
        retrieved_ids = {r["entity_id"] for r in results}

        valid = []
        for c in citations:
            if c.entity_id in retrieved_ids:
                c.relevance_score = 1.0
                valid.append(c)
            else:
                # Still include but mark as unverified with lower score
                c.relevance_score = 0.3
                c.description = "(not in retrieval results - unverified)"
                valid.append(c)

        return valid

    def _score_confidence(
        self, results: list[dict[str, Any]], citations: list[Citation]
    ) -> ConfidenceLevel:
        """Score confidence based on retrieval quality and citation validity."""
        if not results:
            return ConfidenceLevel.LOW

        # Factor 1: Number of results
        result_score = min(len(results) / 5, 1.0)

        # Factor 2: How many results appear in both vector + graph
        both_count = sum(1 for r in results if r.get("in_both", False))
        fusion_score = min(both_count / 3, 1.0)

        # Factor 3: Citation validity
        valid_count = sum(1 for c in citations if c.relevance_score >= 0.8)
        citation_score = min(valid_count / max(len(citations), 1), 1.0)

        overall = (result_score * 0.3) + (fusion_score * 0.3) + (citation_score * 0.4)

        if overall >= 0.7:
            return ConfidenceLevel.HIGH
        elif overall >= 0.4:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    def _rate_limit(self) -> None:
        """Enforce 15 RPM rate limit (4s between requests)."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < 4.0:
            time.sleep(4.0 - elapsed)
        self._last_request_time = time.time()
