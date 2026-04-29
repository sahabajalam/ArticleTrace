"""Legal Research Agent — retrieves article citations per unique rule.

Design:
  The previous implementation called `/api/v1/hybrid/reason`, which runs
  Gemini synthesis + regex citation extraction. That path has two problems
  for agent-to-agent use:
    1. 4s-per-call Gemini rate limit (15 RPM free tier) multiplied by
       every unique rule in a scan — scans with 5+ rules stall for 20s+.
    2. Citation extraction relies on regex over LLM free-text, which is
       brittle; when Gemini worded things differently the citation list
       came back empty even though retrieval found relevant articles.

  This agent talks to `/api/v1/hybrid/search` instead. That endpoint is
  pure retrieval (vector + graph RRF fusion), returns Article entities
  with full metadata already attached (`type`, `regulation_id`,
  `article_number`), and has no LLM in the hot path. Deterministic and
  fast.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import httpx

from src.agents.base import BaseAgent
from src.config import settings
from src.state.scan_state import FindingCitations, LegalCitation, ScanState


_TOP_K = 5
_HTTP_TIMEOUT = 60.0
_MAX_CONCURRENCY = 2


class LegalResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="legal_research")
        self.kb_url = (
            getattr(settings, "graphrag_api_url", None)
            or getattr(settings, "knowledge_engine_url", None)
            or "http://localhost:8001"
        )

    async def execute(self, state: ScanState) -> dict[str, Any]:
        start = datetime.utcnow()
        profile = state["profile"] or {}
        findings: list[dict[str, Any]] = [
            f for f in profile.get("findings", []) if not f.get("suppressed", False)
        ]

        unique_rules: dict[str, dict[str, Any]] = {}
        for f in findings:
            unique_rules.setdefault(f["rule_id"], f)

        if not unique_rules:
            return {
                "finding_citations": [],
                "current_step": "legal_researched",
                **self.audit_update(
                    "research_legal",
                    "no findings to research",
                    duration_seconds=0.0,
                ),
            }

        sem = asyncio.Semaphore(_MAX_CONCURRENCY)

        async def _bounded(client, rid, f):
            async with sem:
                return await self._query(client, rid, f)

        try:
            async with httpx.AsyncClient(timeout=_HTTP_TIMEOUT) as client:
                results = await asyncio.gather(
                    *[
                        _bounded(client, rule_id, f)
                        for rule_id, f in unique_rules.items()
                    ],
                    return_exceptions=True,
                )
        except Exception as e:
            self.logger.warning("Legal research failed: %s", e)
            results = []

        finding_citations: list[dict[str, Any]] = []
        cited = 0
        for (rule_id, f), res in zip(unique_rules.items(), results):
            if isinstance(res, Exception):
                self.logger.warning("rule %s lookup failed: %s", rule_id, res)
                citations, chain = [], [
                    f"1. retrieve: FAILED — {type(res).__name__}: {res}"
                ]
            else:
                citations, chain = res
                if citations:
                    cited += 1
            record = FindingCitations(
                rule_id=rule_id,
                citations=citations,
                reasoning_chain=chain,
            )
            finding_citations.append(record.model_dump(mode="json"))

        duration = (datetime.utcnow() - start).total_seconds()
        return {
            "finding_citations": finding_citations,
            "current_step": "legal_researched",
            **self.audit_update(
                "research_legal",
                f"{cited}/{len(unique_rules)} rules got citations",
                duration_seconds=duration,
            ),
        }

    async def _query(
        self,
        client: httpx.AsyncClient,
        rule_id: str,
        finding: dict[str, Any],
    ) -> tuple[list[LegalCitation], list[str]]:
        anchors: list[str] = finding.get("obligation_anchors") or []
        mapped_articles: list[str] = finding.get("mapped_articles") or []
        title = finding.get("title", rule_id)

        query = _build_query(title, anchors, mapped_articles)
        payload = {"query": query, "top_k": _TOP_K}
        try:
            r = await client.post(
                f"{self.kb_url}/api/v1/hybrid/search", json=payload
            )
            r.raise_for_status()
            data = r.json()
        except httpx.HTTPError as e:
            self.logger.warning("hybrid/search failed for %s: %s", rule_id, e)
            return [], [f"1. retrieve: FAILED — {type(e).__name__}: {e}"]
        except Exception as e:
            self.logger.exception("hybrid/search unexpected error for %s", rule_id)
            return [], [f"1. retrieve: FAILED — {type(e).__name__}: {e}"]

        try:
            raw = data.get("results") or []
            # Retrieval returns a mix of Article and Obligation entities.
            # An Obligation (e.g. AIACT_OBL_14_P1_SHALL) carries its parent
            # article in `metadata.article_reference` — pivot it up and
            # deduplicate on (regulation, article_number) so the UI never
            # shows two rows for the same article.
            citations: list[LegalCitation] = []
            seen: set[tuple[str, str]] = set()
            for r_ in raw:
                if not isinstance(r_, dict):
                    continue
                meta = r_.get("metadata") or {}
                etype = (meta.get("type") or "").lower()
                if etype not in {"article", "obligation"}:
                    continue
                citation = _to_citation(r_, anchors)
                key = (citation.regulation, citation.article_number)
                if key in seen or citation.article_number in ("", "?"):
                    continue
                seen.add(key)
                citations.append(citation)
                if len(citations) >= _TOP_K:
                    break

            chain = _build_chain(query, len(raw), citations, mapped_articles)
            return citations, chain
        except Exception as e:
            self.logger.exception("parse error for %s", rule_id)
            return [], [
                f"1. retrieve: ok — {len(data.get('results') or [])} raw hits",
                f"2. parse: FAILED — {type(e).__name__}: {e}",
            ]


def _build_query(title: str, anchors: list[str], mapped: list[str]) -> str:
    """Shape a retrieval query that blends the finding title, its
    obligation anchors, and any rule-mapped article IDs.

    The article IDs give the graph-traversal side of RRF a direct seed,
    which is why scans now surface the intended articles even when the
    semantic match is weak.
    """
    parts = [title]
    if anchors:
        parts.append("Obligations: " + ", ".join(anchors))
    if mapped:
        parts.append("Articles: " + ", ".join(mapped))
    return ". ".join(parts)


def _to_citation(result: dict[str, Any], anchors: list[str]) -> LegalCitation:
    meta = result.get("metadata") or {}
    entity_id = result.get("entity_id") or ""
    regulation = meta.get("regulation_id") or _regulation_from_id(entity_id)
    # Articles carry `article_number` directly; Obligations carry a
    # pointer like `article_reference: "AIACT_ART_26"` instead.
    article_number = (
        meta.get("article_number")
        or _article_from_id(meta.get("article_reference", ""))
        or _article_from_id(entity_id)
        or "?"
    )
    doc_text = result.get("document") or ""
    snippet = doc_text[:400] if doc_text else None
    derived_title = _first_sentence(doc_text) if doc_text else None
    score = float(result.get("rrf_score") or result.get("similarity") or 0.0)
    return LegalCitation(
        regulation=regulation or "UNKNOWN",
        article_number=article_number,
        title=derived_title,
        text_snippet=snippet,
        relevance_score=score,
        obligation_anchor=_matching_anchor(anchors, doc_text),
    )


def _build_chain(
    query: str,
    hits: int,
    citations: list[LegalCitation],
    mapped_articles: list[str],
) -> list[str]:
    chain = [f"1. retrieve: hybrid RRF search — {hits} raw hits for \"{query[:80]}\""]
    if mapped_articles:
        chain.append(
            f"2. seed: rule pre-mapped articles {', '.join(mapped_articles)}"
        )
    if citations:
        labels = [f"{c.regulation} Art. {c.article_number}" for c in citations]
        chain.append(f"{len(chain)+1}. filter: kept {len(citations)} Article entities — {', '.join(labels)}")
    else:
        chain.append(f"{len(chain)+1}. filter: no Article-type results after filtering")
    return chain


def _regulation_from_id(node_id: str) -> str:
    u = (node_id or "").upper()
    if "AIACT" in u:
        return "EU_AI_ACT"
    if "GDPR" in u:
        return "GDPR"
    return "UNKNOWN"


def _article_from_id(entity_id: str) -> str:
    if not entity_id:
        return ""
    tail = entity_id.rsplit("_", 1)[-1]
    return tail if any(ch.isdigit() for ch in tail) else ""


def _first_sentence(text: str) -> str | None:
    if not text:
        return None
    for sep in (". ", ".\n", "\n"):
        idx = text.find(sep)
        if 10 < idx < 160:
            return text[:idx].strip()
    return text[:120].strip() or None


def _matching_anchor(anchors: list[str], text: str) -> str | None:
    low = (text or "").lower()
    for a in anchors:
        if a and a.lower() in low:
            return a
    return None
