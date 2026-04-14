"""Parser for EDPB guidelines.

Handles:
- 19 GL_* files + 2 WP* files = 21 individual guidelines
- Structured header fields: Reference, Topics, Tier
- Full text with section headings (preserved for vector store chunking)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


class GuidelineParser(BaseParser):
    """Parse EDPB guidelines from individual files."""

    DELIMITER = r"=== GUIDELINE:\s*(.+?)\s*==="

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_directory(self, guidelines_dir: Path) -> list[dict[str, Any]]:
        """Parse all individual guideline files (skip compilation and index)."""
        guidelines: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        for file_path in sorted(guidelines_dir.glob("*.txt")):
            # Skip compilation and index files
            if file_path.stem in ("edpb_guidelines_detailed", "edpb_index"):
                continue

            file_guidelines = self._parse_guideline_file(file_path)
            for gl in file_guidelines:
                if gl["id"] not in seen_ids:
                    seen_ids.add(gl["id"])
                    guidelines.append(gl)

        return guidelines

    def _parse_guideline_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Parse a single guideline file."""
        blocks = self.split_file(file_path)
        guidelines = []

        for block in blocks:
            header = block["delimiter_match"][0].strip()
            raw = block["raw_text"]
            gl = self._parse_guideline_block(header, raw, str(file_path))
            guidelines.append(gl)

        return guidelines

    def _parse_guideline_block(
        self, header: str, raw_text: str, source_file: str
    ) -> dict[str, Any]:
        """Parse a single guideline block."""
        # Split on --- PREAMBLE --- marker
        preamble_split = re.split(r"---\s*PREAMBLE\s*---", raw_text, maxsplit=1)
        header_section = preamble_split[0]
        full_text = preamble_split[1].strip() if len(preamble_split) > 1 else ""

        # Parse header fields
        fields = self.parse_key_value_fields(header_section)

        reference = fields.get("Reference", "").strip()
        topics_raw = fields.get("Topics", "")
        tier = fields.get("Tier", "").strip()

        # Parse topics
        topics = [t.strip() for t in topics_raw.split(",") if t.strip()]

        # Build ID from reference: "Guidelines 05/2022" → "EDPB_GL_05_2022"
        gl_id = self._build_id(reference)

        # Extract article references from header + first portion of full text
        # Guidelines are large (up to 220KB), scan first 20K chars for references
        scan_text = header_section + " " + full_text[:20000]
        article_refs = []
        for ref_num in self.extract_article_references(scan_text):
            article_refs.append(f"GDPR_ART_{ref_num}")

        return {
            "id": gl_id,
            "type": "Guideline",
            "name": header,
            "reference": reference,
            "topics": topics,
            "tier": tier,
            "full_text": full_text,
            "article_references": article_refs,
            "description": header,
            "source_file": source_file,
        }

    @staticmethod
    def _build_id(reference: str) -> str:
        """Build a normalized ID from a guideline reference.

        Examples:
            "Guidelines 05/2022" → "EDPB_GL_05_2022"
            "WP251rev.01 (endorsed by EDPB)" → "EDPB_WP251"
        """
        # WP-style references
        wp_match = re.match(r"(WP\d+)", reference)
        if wp_match:
            return f"EDPB_{wp_match.group(1)}"

        # GL-style: "Guidelines NN/YYYY" or "Guidelines N/YYYY"
        gl_match = re.search(r"(\d+)/(\d{4})", reference)
        if gl_match:
            return f"EDPB_GL_{gl_match.group(1).zfill(2)}_{gl_match.group(2)}"

        # Fallback: sanitize
        sanitized = re.sub(r"[^A-Za-z0-9]", "_", reference)
        return f"EDPB_{sanitized}"
