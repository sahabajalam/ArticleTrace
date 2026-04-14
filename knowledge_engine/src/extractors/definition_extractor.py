"""Rule-based definition extraction from GDPR Art 4 and AI Act Art 3.

These articles contain numbered definition lists in the format:
    (1) 'personal data' means <definition text>;
    (2) 'processing' means <definition text>;
"""

from __future__ import annotations

import re
from typing import Any


class DefinitionExtractor:
    """Extract definitions from definition articles."""

    # Pattern: (N) 'term' means <text>
    DEF_PATTERN = re.compile(
        r"\((\d+)\)\s*['\u2018\u2019]([^'\u2018\u2019]+)['\u2018\u2019]\s*means\s+(.*?)(?=\(\d+\)\s*['\u2018\u2019]|\Z)",
        re.DOTALL,
    )

    def extract_from_article(
        self, article: dict[str, Any], regulation_id: str
    ) -> list[dict[str, Any]]:
        """Extract all definitions from a definition article (Art 3 or Art 4)."""
        prefix = "GDPR" if regulation_id == "GDPR" else "AIACT"
        article_id = article["id"]
        full_text = article.get("full_text", "")

        definitions = []

        for match in self.DEF_PATTERN.finditer(full_text):
            def_num = int(match.group(1))
            term = match.group(2).strip()
            def_text = match.group(3).strip().rstrip(";")

            def_id = self._build_id(prefix, term, def_num)

            definitions.append({
                "id": def_id,
                "type": "Definition",
                "name": term,
                "term": term,
                "definition_text": def_text,
                "regulation_id": regulation_id,
                "article_reference": article_id,
                "definition_number": def_num,
                "description": f"Definition of '{term}'",
                "source_text": match.group(0).strip(),
                "synonyms": [],
                "examples": [],
            })

        return definitions

    @staticmethod
    def _build_id(prefix: str, term: str, def_num: int) -> str:
        """Build definition ID: GDPR_DEF_PERSONAL_DATA."""
        sanitized = re.sub(r"[^a-zA-Z0-9]", "_", term.upper())
        sanitized = re.sub(r"_+", "_", sanitized).strip("_")
        return f"{prefix}_DEF_{sanitized}"
