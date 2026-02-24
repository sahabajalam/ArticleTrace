"""Structural relationship extraction from parsed data.

Extracts all edges that can be derived from the parsed JSON without LLM:
- CONTAINS / PART_OF: Regulation -> Chapter -> Article, Regulation -> Recital/Annex
- REFERENCES: Article -> Article (cross-references parsed from article text)
- INTERPRETS: Recital -> Article, Guideline -> Article, CaseLaw -> Article
- CITES: EnforcementAction -> Article, CaseLaw -> Article
- DEFINES: Definition article -> Definition (for Art 3 / Art 4)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StructuralExtractor:
    """Extract structural relationships from parsed data files."""

    def __init__(self, parsed_data_dir: Path):
        self.parsed_dir = parsed_data_dir
        self._article_ids: set[str] = set()
        self._load_article_ids()

    def _load_article_ids(self) -> None:
        """Load all valid article IDs for reference validation."""
        for fname in ("gdpr_articles.json", "eu_ai_act_articles.json"):
            path = self.parsed_dir / "legal" / fname
            if path.exists():
                articles = json.loads(path.read_text(encoding="utf-8"))
                for a in articles:
                    self._article_ids.add(a["id"])

    def extract_all(self) -> dict[str, list[dict[str, Any]]]:
        """Extract all structural relationships.

        Returns:
            Dict with keys: containment, references, interprets, cites
            Each value is a list of relationship dicts.
        """
        containment = self._extract_containment()
        references = self._extract_cross_references()
        interprets = self._extract_interpretive_links()
        cites = self._extract_citation_links()

        return {
            "containment": containment,
            "references": references,
            "interprets": interprets,
            "cites": cites,
        }

    def _extract_containment(self) -> list[dict[str, Any]]:
        """Extract CONTAINS and PART_OF relationships.

        Regulation -> Chapter -> Article
        Regulation -> Recital
        Regulation -> Annex
        """
        rels: list[dict[str, Any]] = []

        # GDPR chapters and articles
        gdpr_chapters = self._load_json("legal/gdpr_chapters.json")
        gdpr_articles = self._load_json("legal/gdpr_articles.json")

        for ch in gdpr_chapters:
            ch_id = f"GDPR_CH_{ch['number']}"
            # Regulation -> Chapter
            rels.append(self._rel("GDPR", ch_id, "CONTAINS"))
            rels.append(self._rel(ch_id, "GDPR", "PART_OF"))

        for art in gdpr_articles:
            ch_num = art.get("chapter", "").replace("Chapter ", "")
            if ch_num:
                ch_id = f"GDPR_CH_{ch_num}"
                # Chapter -> Article
                rels.append(self._rel(ch_id, art["id"], "CONTAINS"))
                rels.append(self._rel(art["id"], ch_id, "PART_OF"))

        # AI Act chapters and articles
        ai_chapters = self._load_json("legal/ai_act_chapters.json")
        ai_articles = self._load_json("legal/eu_ai_act_articles.json")

        for ch in ai_chapters:
            ch_id = f"AIACT_CH_{ch['number']}"
            rels.append(self._rel("EU_AI_ACT", ch_id, "CONTAINS"))
            rels.append(self._rel(ch_id, "EU_AI_ACT", "PART_OF"))

        for art in ai_articles:
            ch_num = art.get("chapter", "").replace("Chapter ", "")
            if ch_num:
                ch_id = f"AIACT_CH_{ch_num}"
                rels.append(self._rel(ch_id, art["id"], "CONTAINS"))
                rels.append(self._rel(art["id"], ch_id, "PART_OF"))

        # Recitals -> Regulation
        for fname, reg_id in [
            ("legal/gdpr_recitals.json", "GDPR"),
            ("legal/ai_act_recitals.json", "EU_AI_ACT"),
        ]:
            recitals = self._load_json(fname)
            for rec in recitals:
                rels.append(self._rel(reg_id, rec["id"], "CONTAINS"))

        # Annexes -> Regulation
        annexes = self._load_json("legal/ai_act_annexes.json")
        for annex in annexes:
            rels.append(self._rel("EU_AI_ACT", annex["id"], "CONTAINS"))

        return rels

    def _extract_cross_references(self) -> list[dict[str, Any]]:
        """Extract REFERENCES relationships from article cross_references field.

        These were parsed during Phase 1 from text like 'Article 35'.
        Only include refs where both source and target exist.
        """
        rels: list[dict[str, Any]] = []

        for fname in ("legal/gdpr_articles.json", "legal/eu_ai_act_articles.json"):
            articles = self._load_json(fname)
            for art in articles:
                source_id = art["id"]
                for target_id in art.get("cross_references", []):
                    # Skip self-references
                    if target_id == source_id:
                        continue
                    # Only include if target exists in our parsed data
                    if target_id in self._article_ids:
                        rels.append(self._rel(source_id, target_id, "REFERENCES"))

        return rels

    def _extract_interpretive_links(self) -> list[dict[str, Any]]:
        """Extract INTERPRETS relationships.

        Recital -> Article (from article_references field parsed in Phase 1)
        Guideline -> Article (from article_references field)
        CaseLaw -> Article (from provisions_interpreted field)
        """
        rels: list[dict[str, Any]] = []

        # Recitals -> Articles
        for fname, prefix in [
            ("legal/gdpr_recitals.json", "GDPR"),
            ("legal/ai_act_recitals.json", "AIACT"),
        ]:
            recitals = self._load_json(fname)
            for rec in recitals:
                for ref_id in rec.get("article_references", []):
                    if ref_id in self._article_ids:
                        rels.append(self._rel(rec["id"], ref_id, "INTERPRETS"))

        # Guidelines -> Articles
        guidelines = self._load_json("interpretive/edpb_guidelines.json")
        for gl in guidelines:
            for ref_id in gl.get("article_references", []):
                if ref_id in self._article_ids:
                    rels.append(self._rel(gl["id"], ref_id, "INTERPRETS"))

        # CaseLaw -> Articles (INTERPRETS from provisions_interpreted)
        cases = self._load_json("interpretive/case_law.json")
        for case in cases:
            for ref_id in case.get("provisions_interpreted", []):
                if ref_id in self._article_ids:
                    rels.append(self._rel(case["id"], ref_id, "INTERPRETS"))

        return rels

    def _extract_citation_links(self) -> list[dict[str, Any]]:
        """Extract CITES relationships.

        EnforcementAction -> Article (from violations field)
        CaseLaw -> Article (from provisions_interpreted - also CITES since courts cite articles)
        """
        rels: list[dict[str, Any]] = []

        # Enforcement -> Articles
        actions = self._load_json("interpretive/enforcement_actions.json")
        for action in actions:
            for ref_id in action.get("violations", []):
                if ref_id in self._article_ids:
                    rels.append(self._rel(action["id"], ref_id, "CITES"))

        # CaseLaw -> Articles (CITES)
        cases = self._load_json("interpretive/case_law.json")
        for case in cases:
            for ref_id in case.get("provisions_interpreted", []):
                if ref_id in self._article_ids:
                    rels.append(self._rel(case["id"], ref_id, "CITES"))

        return rels

    def _load_json(self, relative_path: str) -> list[dict[str, Any]]:
        """Load a JSON file from parsed_data directory."""
        path = self.parsed_dir / relative_path
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _rel(source_id: str, target_id: str, rel_type: str, **props) -> dict[str, Any]:
        """Create a relationship dict."""
        return {
            "source_id": source_id,
            "target_id": target_id,
            "type": rel_type,
            "properties": props,
        }
