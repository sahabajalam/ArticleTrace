"""Parser for GDPR and EU AI Act recitals.

Handles:
- GDPR: 1 file → 173 recitals
- AI Act: 1 file → 180 recitals
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


class RecitalParser(BaseParser):
    """Parse recitals from single-file compilations."""

    DELIMITER = r"=== RECITAL (\d+) ==="

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_file(self, file_path: Path, regulation_id: str) -> list[dict[str, Any]]:
        """Parse all recitals from a single file.

        Returns:
            List of recital dicts.
        """
        blocks = self.split_file(file_path)
        prefix = "GDPR" if regulation_id == "GDPR" else "AIACT"
        recitals = []

        for block in blocks:
            recital_num = int(block["delimiter_match"][0])
            text = block["raw_text"].strip()

            # Extract article references from recital text
            article_refs = []
            for ref_num in self.extract_article_references(text):
                article_refs.append(f"{prefix}_ART_{ref_num}")

            recitals.append({
                "id": f"{prefix}_REC_{recital_num}",
                "type": "Recital",
                "name": f"Recital {recital_num}",
                "regulation_id": regulation_id,
                "recital_number": recital_num,
                "full_text": text,
                "article_references": article_refs,
                "description": text[:200] + "..." if len(text) > 200 else text,
                "source_text": text,
            })

        return recitals
