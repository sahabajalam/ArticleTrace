"""Parser for CJEU case law files.

Handles:
- 20 individual case files
- Structured fields: Full Name, Court, Decision Date, Topic, etc.
- Deduplication against compilation file
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


class CaseLawParser(BaseParser):
    """Parse CJEU case law from individual files."""

    DELIMITER = r"=== CASE:\s*(.+?)\s*==="

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_directory(self, case_law_dir: Path) -> list[dict[str, Any]]:
        """Parse all individual case law files (skip compilation and index)."""
        cases: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        for file_path in sorted(case_law_dir.glob("C*.txt")):
            file_cases = self._parse_case_file(file_path)
            for case in file_cases:
                if case["id"] not in seen_ids:
                    seen_ids.add(case["id"])
                    cases.append(case)

        return cases

    def _parse_case_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Parse a single case file (may contain 1 case)."""
        blocks = self.split_file(file_path)
        cases = []

        for block in blocks:
            case_header = block["delimiter_match"][0].strip()
            raw = block["raw_text"]
            case = self._parse_case_block(case_header, raw, str(file_path))
            cases.append(case)

        return cases

    def _parse_case_block(
        self, header: str, raw_text: str, source_file: str
    ) -> dict[str, Any]:
        """Parse a single case block into structured data."""
        fields = self.parse_key_value_fields(raw_text)

        # Extract case number from header: "C-311/18 Schrems II"
        case_num_match = re.match(r"(C-\d+/\d+)\s*(.*)", header)
        case_number = case_num_match.group(1) if case_num_match else header
        case_name = case_num_match.group(2).strip() if case_num_match else ""

        # Build ID from case number: C-311/18 → CJEU_C_311_18
        case_id = "CJEU_" + case_number.replace("-", "_").replace("/", "_")

        # Parse provisions interpreted into article refs
        provisions_raw = fields.get("Provisions Interpreted", "")
        provisions = self._parse_provisions(provisions_raw)

        # Parse list fields
        key_legal_points = self._parse_bullet_list(fields.get("Key Legal Points", ""))
        practical_impact = self._parse_bullet_list(fields.get("Practical Impact", ""))
        ai_relevance = self._parse_bullet_list(fields.get("AI Relevance", ""))

        return {
            "id": case_id,
            "type": "CaseLaw",
            "name": case_name or case_number,
            "case_number": case_number,
            "case_name": case_name,
            "full_name": fields.get("Full Name", ""),
            "court": fields.get("Court", ""),
            "decision_date": fields.get("Decision Date", ""),
            "topic": fields.get("Topic", ""),
            "provisions_interpreted": provisions,
            "holding": fields.get("Holding", ""),
            "facts": fields.get("Facts", ""),
            "key_legal_points": key_legal_points,
            "practical_impact": practical_impact,
            "ai_relevance": ai_relevance,
            "description": fields.get("Topic", ""),
            "source_text": raw_text,
            "source_file": source_file,
        }

    @staticmethod
    def _parse_provisions(text: str) -> list[str]:
        """Parse provisions into article IDs.

        Handles:
            GDPR Articles 44, 45, 46
            Directive 95/46/EC Articles 2, 4, 12, 14  (maps to GDPR equivalent)
            AI Act Articles 6, 9
            Charter Articles 7, 8  (noted but not linked)
        """
        provisions: list[str] = []

        # GDPR Articles
        gdpr_match = re.search(r"GDPR\s+Articles?\s+([\d,\s]+)", text, re.IGNORECASE)
        if gdpr_match:
            for num in re.findall(r"\d+", gdpr_match.group(1)):
                provisions.append(f"GDPR_ART_{num}")

        # Directive 95/46/EC Articles → map to GDPR equivalents
        # These pre-GDPR cases still have relevance as GDPR interprets the same concepts
        directive_match = re.search(
            r"Directive\s+95/46/?EC\s+Articles?\s+([\d,\s()a-z]+)",
            text, re.IGNORECASE,
        )
        if directive_match:
            for num in re.findall(r"\d+", directive_match.group(1)):
                # Directive 95/46/EC article numbering differs from GDPR.
                # We link to GDPR articles by number where a reasonable mapping exists.
                # Not all map 1:1, but the provisions_interpreted gives the closest match.
                art_id = f"GDPR_ART_{num}"
                if art_id not in provisions:
                    provisions.append(art_id)

        # AI Act Articles
        ai_match = re.search(r"AI\s+Act\s+Articles?\s+([\d,\s]+)", text, re.IGNORECASE)
        if ai_match:
            for num in re.findall(r"\d+", ai_match.group(1)):
                provisions.append(f"AIACT_ART_{num}")

        # Charter Articles — not in our KG scope, skip
        return provisions

    @staticmethod
    def _parse_bullet_list(text: str) -> list[str]:
        """Parse dash/bullet-separated items."""
        items = []
        for line in text.split("\n"):
            line = line.strip()
            # Remove leading bullet markers
            cleaned = re.sub(r"^[-–—•]\s*", "", line)
            if cleaned:
                items.append(cleaned)
        return items if items else [text.strip()] if text.strip() else []
