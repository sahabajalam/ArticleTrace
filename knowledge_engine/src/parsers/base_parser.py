"""Base parser with shared delimiter parsing logic.

All raw data files use the pattern: === TYPE: ID ===
This base class handles splitting files on those delimiters.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


class BaseParser:
    """Splits raw text files on `=== ... ===` delimiters."""

    def __init__(self, delimiter_pattern: str):
        """
        Args:
            delimiter_pattern: Regex pattern matching the delimiter line.
                Must contain at least one capture group for the entity identifier.
                Example: r"=== ARTICLE (\d+) ==="
        """
        self._pattern = re.compile(delimiter_pattern, re.IGNORECASE)

    def split_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Split a single file into raw blocks by delimiter.

        Returns:
            List of dicts with keys:
                - 'delimiter_match': the regex match groups
                - 'raw_text': everything between this delimiter and the next
                - 'source_file': original file path
        """
        text = file_path.read_text(encoding="utf-8")
        return self.split_text(text, source_file=str(file_path))

    def split_text(self, text: str, source_file: str = "") -> list[dict[str, Any]]:
        """Split text content into raw blocks by delimiter."""
        blocks: list[dict[str, Any]] = []
        matches = list(self._pattern.finditer(text))

        for i, match in enumerate(matches):
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            raw_text = text[start:end].strip()

            blocks.append({
                "delimiter_match": match.groups(),
                "delimiter_full": match.group(0),
                "raw_text": raw_text,
                "source_file": source_file,
            })

        return blocks

    @staticmethod
    def parse_key_value_fields(text: str) -> dict[str, str]:
        """Parse structured key: value fields from a text block.

        Handles multi-line values (lines not starting with a known key
        are appended to the previous key's value).
        """
        fields: dict[str, str] = {}
        current_key: str | None = None

        for line in text.split("\n"):
            # Match "Key: value" or "Key Name: value"
            kv_match = re.match(r"^([A-Z][A-Za-z\s]+?):\s*(.*)$", line)
            if kv_match:
                current_key = kv_match.group(1).strip()
                fields[current_key] = kv_match.group(2).strip()
            elif current_key and line.strip():
                fields[current_key] += "\n" + line.strip()

        return fields

    @staticmethod
    def extract_article_references(text: str) -> list[str]:
        """Extract cross-references like 'Article 35', 'Articles 12 to 22' from text."""
        refs: set[str] = set()

        # Single article: "Article 35", "Article 6(1)(f)"
        for m in re.finditer(r"Article\s+(\d+)(?:\([\d\w]+\))*", text, re.IGNORECASE):
            refs.add(m.group(1))

        # Article range: "Articles 12 to 22"
        for m in re.finditer(r"Articles?\s+(\d+)\s+to\s+(\d+)", text, re.IGNORECASE):
            start, end = int(m.group(1)), int(m.group(2))
            for n in range(start, end + 1):
                refs.add(str(n))

        return sorted(refs, key=lambda x: int(x))
