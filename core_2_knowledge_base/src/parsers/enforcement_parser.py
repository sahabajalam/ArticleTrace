"""Parser for DPA enforcement actions.

Handles:
- 15 individual enforcement action files
- Structured fields: Authority, Target, Fine Amount, Violations, etc.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .base_parser import BaseParser


class EnforcementParser(BaseParser):
    """Parse enforcement actions from individual files."""

    DELIMITER = r"=== ENFORCEMENT:\s*(.+?)\s*==="

    def __init__(self):
        super().__init__(self.DELIMITER)

    def parse_directory(self, enforcement_dir: Path) -> list[dict[str, Any]]:
        """Parse all individual enforcement files (skip compilation and index)."""
        actions: list[dict[str, Any]] = []
        seen_ids: set[str] = set()

        for file_path in sorted(enforcement_dir.glob("*.txt")):
            # Skip compilation and index files
            if file_path.stem in ("enforcement_actions_detailed", "enforcement_index"):
                continue

            file_actions = self._parse_enforcement_file(file_path)
            for action in file_actions:
                if action["id"] not in seen_ids:
                    seen_ids.add(action["id"])
                    actions.append(action)

        return actions

    def _parse_enforcement_file(self, file_path: Path) -> list[dict[str, Any]]:
        """Parse a single enforcement file."""
        blocks = self.split_file(file_path)
        actions = []

        for block in blocks:
            header = block["delimiter_match"][0].strip()
            raw = block["raw_text"]
            action = self._parse_action_block(header, raw, str(file_path))
            actions.append(action)

        return actions

    def _parse_action_block(
        self, header: str, raw_text: str, source_file: str
    ) -> dict[str, Any]:
        """Parse a single enforcement action block."""
        fields = self.parse_key_value_fields(raw_text)

        # Build ID from header name
        action_id = "ENF_" + re.sub(r"[^A-Za-z0-9]", "_", header).upper()
        # Clean up multiple underscores
        action_id = re.sub(r"_+", "_", action_id).strip("_")

        # Parse fine amount
        fine_raw = fields.get("Fine Amount", "")
        fine_amount = self._parse_fine_amount(fine_raw)

        # Parse violations into article references
        # Use both the parsed field AND the full raw text (catches multi-line violations)
        violations_raw = fields.get("Violations", "")
        violations = self._parse_violations(violations_raw)
        if not violations:
            # Fallback: scan entire raw text for violation references
            violations = self._parse_violations(raw_text)

        # Parse list fields
        key_findings = self._parse_numbered_list(fields.get("Key Findings", ""))
        corrective_measures = self._parse_bullet_list(fields.get("Corrective Measures", ""))
        ai_relevance = self._parse_bullet_list(fields.get("AI Relevance", ""))

        return {
            "id": action_id,
            "type": "EnforcementAction",
            "name": header,
            "authority": fields.get("Authority", ""),
            "target": fields.get("Target", ""),
            "decision_date": fields.get("Decision Date", ""),
            "fine_amount_eur": fine_amount,
            "fine_category": fields.get("Fine Category", ""),
            "violations": violations,
            "facts": fields.get("Facts", ""),
            "key_findings": key_findings,
            "corrective_measures": corrective_measures,
            "ai_relevance": ai_relevance,
            "description": f"Enforcement against {fields.get('Target', header)}",
            "source_text": raw_text,
            "source_file": source_file,
        }

    @staticmethod
    def _parse_fine_amount(text: str) -> int | None:
        """Extract numeric fine amount from text like 'EUR 90,500,000+'."""
        # Remove currency symbols and text
        cleaned = re.sub(r"[^\d,.]", "", text.split("(")[0])  # Take first amount
        cleaned = cleaned.replace(",", "")
        if cleaned:
            try:
                return int(float(cleaned))
            except ValueError:
                return None
        return None

    @staticmethod
    def _parse_violations(text: str) -> list[str]:
        """Parse violation references into article IDs.

        Handles formats like:
            - GDPR Article 6(1), Article 9
            - GDPR Articles 12, 13, 14
            - Article 31
        """
        violations: list[str] = []

        # Match "GDPR Articles 12, 13, 14" (comma-separated)
        for m in re.finditer(r"(?:GDPR\s+)?Articles?\s+([\d,\s]+)", text, re.IGNORECASE):
            for num in re.findall(r"\d+", m.group(1)):
                art_id = f"GDPR_ART_{num}"
                if art_id not in violations:
                    violations.append(art_id)

        # Match "Article N(M)" standalone
        for m in re.finditer(r"Article\s+(\d+)(?:\([\d\w]+\))*", text, re.IGNORECASE):
            art_id = f"GDPR_ART_{m.group(1)}"
            if art_id not in violations:
                violations.append(art_id)

        # Match "AI Act Article N"
        for m in re.finditer(r"AI\s+Act\s+Article\s+(\d+)", text, re.IGNORECASE):
            art_id = f"AIACT_ART_{m.group(1)}"
            if art_id not in violations:
                violations.append(art_id)

        return violations

    @staticmethod
    def _parse_numbered_list(text: str) -> list[str]:
        """Parse numbered items like '1. Finding text'."""
        items: list[str] = []
        for line in text.split("\n"):
            cleaned = re.sub(r"^\d+\.\s*", "", line.strip())
            if cleaned:
                items.append(cleaned)
        return items

    @staticmethod
    def _parse_bullet_list(text: str) -> list[str]:
        """Parse dash/bullet-separated items."""
        items: list[str] = []
        for line in text.split("\n"):
            cleaned = re.sub(r"^[-–—•]\s*", "", line.strip())
            if cleaned:
                items.append(cleaned)
        return items if items else [text.strip()] if text.strip() else []
