"""Parser for EU AI Act annexes.

Handles:
- 1 file → 13 annexes (I–XIII)
- Irregular structure per annex (lists, sections, document templates)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


# Roman numeral mapping
ROMAN_TO_INT = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
    "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
}

INT_TO_ROMAN = {v: k for k, v in ROMAN_TO_INT.items()}


class AnnexParser(BaseParser):
    """Parse EU AI Act annexes."""

    DELIMITER = r"=== ANNEX ([IVX]+) ==="

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Parse all annexes from the single annexes file."""
        blocks = self.split_file(file_path)
        annexes = []

        for block in blocks:
            roman = block["delimiter_match"][0]
            annex_num = ROMAN_TO_INT.get(roman, 0)
            raw = block["raw_text"]

            annex = self._parse_annex_block(roman, annex_num, raw)
            annex["source_file"] = block["source_file"]
            annexes.append(annex)

        return annexes

    def _parse_annex_block(
        self, roman: str, annex_num: int, raw_text: str
    ) -> dict[str, Any]:
        """Parse a single annex block."""
        lines = raw_text.split("\n")

        # Extract title
        title = ""
        content_start = 0
        if lines:
            title_match = re.match(r"^Title:\s*(.+)", lines[0])
            if title_match:
                title = title_match.group(1).strip()
                content_start = 1

        content = "\n".join(lines[content_start:]).strip()

        # Parse sections (numbered items, lettered items, section headings)
        sections = self._parse_sections(content)

        # Extract article references
        article_refs = []
        for ref_num in self.extract_article_references(content):
            article_refs.append(f"AIACT_ART_{ref_num}")

        return {
            "id": f"AIACT_ANNEX_{roman}",
            "type": "Annex",
            "name": f"Annex {roman}",
            "title": title,
            "regulation_id": "EU_AI_ACT",
            "annex_number": roman,
            "full_text": content,
            "sections": sections,
            "article_references": article_refs,
            "description": title,
        }

    @staticmethod
    def _parse_sections(text: str) -> list[dict[str, Any]]:
        """Parse annex content into sections.

        Handles:
            Section A. Title
            1. Item text
            2. Item text
              (a) sub-item
        """
        sections: list[dict[str, Any]] = []
        current_section: dict[str, Any] | None = None
        current_items: list[str] = []

        for line in text.split("\n"):
            # Section heading: "Section A.", "SECTION 1.", "Area N:", numbered heading
            section_match = re.match(
                r"^(?:Section\s+[A-Z]\.|SECTION\s+\d+\.|Area\s+\d+[.:])(.*)$",
                line, re.IGNORECASE,
            )
            if section_match:
                if current_section is not None:
                    current_section["items"] = current_items
                    sections.append(current_section)
                current_section = {
                    "heading": line.strip(),
                    "title": section_match.group(1).strip(),
                    "items": [],
                }
                current_items = []
                continue

            # Numbered items: "1.", "2.", etc.
            item_match = re.match(r"^(\d+)\.\s+(.+)", line)
            if item_match:
                current_items.append(line.strip())
                continue

            # Lettered sub-items
            sub_match = re.match(r"^\s*\([a-z]\)\s+(.+)", line)
            if sub_match:
                current_items.append(line.strip())
                continue

            # Dash items
            dash_match = re.match(r"^\s*[—–-]\s+(.+)", line)
            if dash_match:
                current_items.append(line.strip())
                continue

            # Continuation
            if line.strip() and current_items:
                current_items[-1] += " " + line.strip()

        # Flush last section
        if current_section is not None:
            current_section["items"] = current_items
            sections.append(current_section)
        elif current_items:
            sections.append({"heading": "", "title": "", "items": current_items})

        return sections
