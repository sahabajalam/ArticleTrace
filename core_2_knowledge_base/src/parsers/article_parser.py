"""Parser for GDPR and EU AI Act articles.

Handles:
- 11 GDPR chapter files → 99 articles
- 13 AI Act chapter files → 113 articles
- Both "Name:" (GDPR) and "Title:" (AI Act) field conventions
- Paragraph-level extraction with sub-item parsing
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


class ArticleParser(BaseParser):
    """Parse articles from chapter files."""

    # Delimiter: === ARTICLE N ===
    DELIMITER = r"=== ARTICLE (\d+) ==="

    # Chapter header at top of each file
    CHAPTER_PATTERN = re.compile(r"^Chapter\s+(\d+):\s*\n\s*Name:\s*(.+)", re.MULTILINE)

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_chapter_file(
        self, file_path: Path, regulation_id: str
    ) -> dict[str, Any]:
        """Parse a single chapter file.

        Returns:
            Dict with 'chapter' metadata and 'articles' list.
        """
        text = file_path.read_text(encoding="utf-8")

        # Extract chapter metadata from file header
        chapter_match = self.CHAPTER_PATTERN.search(text)
        chapter_number = None
        chapter_name = None
        if chapter_match:
            chapter_number = int(chapter_match.group(1))
            chapter_name = chapter_match.group(2).strip()

        # Split into article blocks
        blocks = self.split_text(text, source_file=str(file_path))

        articles = []
        for block in blocks:
            article_num = block["delimiter_match"][0]
            raw = block["raw_text"]
            article = self._parse_article_block(
                article_num, raw, regulation_id, chapter_number, chapter_name
            )
            article["source_file"] = block["source_file"]
            articles.append(article)

        return {
            "chapter": {
                "number": chapter_number,
                "name": chapter_name,
                "regulation_id": regulation_id,
            },
            "articles": articles,
        }

    def parse_all(
        self, chapter_dir: Path, regulation_id: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Parse all chapter files in a directory.

        Returns:
            (chapters, articles) — both as lists of dicts.
        """
        chapters: list[dict[str, Any]] = []
        articles: list[dict[str, Any]] = []

        # Sort chapter files numerically
        files = sorted(
            chapter_dir.glob("*.txt"),
            key=lambda f: int(re.search(r"(\d+)", f.stem).group(1))
            if re.search(r"(\d+)", f.stem)
            else 0,
        )

        for file_path in files:
            result = self.parse_chapter_file(file_path, regulation_id)
            chapters.append(result["chapter"])
            articles.extend(result["articles"])

        return chapters, articles

    def _parse_article_block(
        self,
        article_num: str,
        raw_text: str,
        regulation_id: str,
        chapter_number: int | None,
        chapter_name: str | None,
    ) -> dict[str, Any]:
        """Parse a single article block into structured data."""
        lines = raw_text.split("\n")

        # Extract title/name (first line, handles both GDPR "Name:" and AI Act "Title:")
        title = ""
        content_start = 0
        if lines:
            title_match = re.match(r"^(?:Name|Title):\s*(.+)", lines[0])
            if title_match:
                title = title_match.group(1).strip()
                content_start = 1

        # Extract paragraphs and sub-items
        remaining = "\n".join(lines[content_start:]).strip()
        paragraphs = self._parse_paragraphs(remaining)

        # Build full_text from all paragraphs
        full_text = remaining

        # Extract cross-references from full text
        prefix = "GDPR" if regulation_id == "GDPR" else "AIACT"
        cross_refs = []
        for ref_num in self.extract_article_references(full_text):
            cross_refs.append(f"{prefix}_ART_{ref_num}")

        # Determine modality from text
        modality = self._detect_modality(full_text)

        # Detect actors
        actors = self._detect_actors(full_text)

        article_id = f"{prefix}_ART_{article_num}"

        return {
            "id": article_id,
            "type": "Article",
            "name": f"Article {article_num}",
            "title": title,
            "regulation_id": regulation_id,
            "chapter": f"Chapter {chapter_number}" if chapter_number else None,
            "chapter_name": chapter_name,
            "article_number": article_num,
            "full_text": full_text,
            "paragraphs": paragraphs,
            "modality": modality,
            "applies_to_actors": actors,
            "cross_references": cross_refs,
            "description": title,
        }

    @staticmethod
    def _parse_paragraphs(text: str) -> dict[str, Any]:
        """Parse paragraph-level structure.

        Handles:
            Paragraph 1: text
            Paragraph 2: text
            (a) sub-item
            (b) sub-item
        """
        paragraphs: dict[str, Any] = {}
        current_para: str | None = None
        current_text_lines: list[str] = []
        sub_items: dict[str, str] = {}

        def _flush():
            if current_para is not None:
                if sub_items:
                    paragraphs[current_para] = {
                        "intro": "\n".join(current_text_lines).strip(),
                        **sub_items,
                    }
                else:
                    paragraphs[current_para] = "\n".join(current_text_lines).strip()

        for line in text.split("\n"):
            # Paragraph N: text
            para_match = re.match(r"^Paragraph\s+(\d+):\s*(.*)", line)
            if para_match:
                _flush()
                current_para = para_match.group(1)
                current_text_lines = [para_match.group(2)] if para_match.group(2) else []
                sub_items = {}
                continue

            # Sub-items: (a), (b), (i), (ii), etc.
            sub_match = re.match(r"^\(([a-z]+|[ivx]+)\)\s*(.*)", line)
            if sub_match and current_para is not None:
                sub_items[sub_match.group(1)] = sub_match.group(2).strip()
                continue

            # Continuation line
            if current_para is not None and line.strip():
                current_text_lines.append(line.strip())

        _flush()

        # Handle articles without explicit paragraph markers (e.g., definition articles)
        if not paragraphs and text.strip():
            paragraphs["full"] = text.strip()

        return paragraphs

    @staticmethod
    def _detect_modality(text: str) -> str | None:
        """Detect the primary modality of the article by frequency."""
        text_lower = text.lower()
        # Count occurrences (positive "shall" minus "shall not")
        shall_not_count = text_lower.count("shall not") + text_lower.count("must not")
        shall_count = text_lower.count("shall") - text_lower.count("shall not")
        should_count = text_lower.count("should")
        may_count = text_lower.count("may")

        counts = {
            "MUST": shall_count,
            "MUST_NOT": shall_not_count,
            "SHOULD": should_count,
            "MAY": may_count,
        }
        # Return the dominant modality
        best = max(counts, key=counts.get)
        return best if counts[best] > 0 else None

    @staticmethod
    def _detect_actors(text: str) -> list[str]:
        """Detect which actors are referenced in the article."""
        actors = []
        actor_patterns = {
            "controller": r"\bcontroller\b",
            "processor": r"\bprocessor\b",
            "provider": r"\bprovider\b",
            "deployer": r"\bdeployer\b",
            "data_subject": r"\bdata\s+subject\b",
            "supervisory_authority": r"\bsupervisory\s+authorit",
            "importer": r"\bimporter\b",
            "distributor": r"\bdistributor\b",
            "notified_body": r"\bnotified\s+bod",
            "dpo": r"\bdata\s+protection\s+officer\b",
        }
        for actor, pattern in actor_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                actors.append(actor)
        return actors
