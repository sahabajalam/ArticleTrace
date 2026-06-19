"""Hybrid obligation and exemption extraction.

Strategy:
1. Rule-based: Scan all articles for obligation signals (shall, must, required)
   and exemption signals (shall not apply, derogation, exempted, without prejudice).
2. For each candidate paragraph, use Gemini to structure:
   - obligation_type: MUST / MUST_NOT / MAY / SHALL
   - duty_bearer: who must comply (actor ID if possible)
   - right_holder: who benefits (actor ID if possible)
   - condition: under what conditions
   - trigger: what event triggers the obligation
   - description: plain-language summary

Rate limiting: Gemini free tier = 15 RPM. We batch paragraphs per article
and send 1 request per article to stay well under limits.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any


# Obligation signal patterns
OBLIGATION_PATTERNS = [
    (r"\bshall\b(?!\s+not\s+apply)", "SHALL"),
    (r"\bmust\b", "MUST"),
    (r"\bis required to\b", "MUST"),
    (r"\bshall ensure\b", "SHALL"),
    (r"\bshall be\s+(?:obliged|required)\b", "MUST"),
]

PROHIBITION_PATTERNS = [
    (r"\bshall not\b", "MUST_NOT"),
    (r"\bshall be prohibited\b", "MUST_NOT"),
    (r"\bmust not\b", "MUST_NOT"),
    (r"\bis prohibited\b", "MUST_NOT"),
]

EXEMPTION_PATTERNS = [
    (r"\bshall not apply\b", "EXEMPTION"),
    (r"\bwithout prejudice\b", "EXEMPTION"),
    (r"\bby way of derogation\b", "EXEMPTION"),
    (r"\bdoes not apply\b", "EXEMPTION"),
    (r"\bexempted?\b", "EXEMPTION"),
    (r"\bnotwithstanding\b", "EXEMPTION"),
    (r"\bprovided that\b", "CONDITION"),
    (r"\bsubject to\b", "CONDITION"),
    (r"\bwhere\b.*\bthe\b", "CONDITION"),
]

PERMISSION_PATTERNS = [
    (r"\bmay\b", "MAY"),
    (r"\bis entitled to\b", "MAY"),
    (r"\bhas the right to\b", "RIGHT"),
]

# Known actor patterns to auto-detect duty_bearer / right_holder
ACTOR_MAP = {
    r"\bcontroller\b": "ACTOR_CONTROLLER",
    r"\bprocessor\b": "ACTOR_PROCESSOR",
    r"\bdata subject\b": "ACTOR_DATA_SUBJECT",
    r"\bsupervisory authorit": "ACTOR_SUPERVISORY_AUTHORITY",
    r"\bdata protection officer\b": "ACTOR_DPO",
    r"\bprovider\b": "ACTOR_PROVIDER",
    r"\bdeployer\b": "ACTOR_DEPLOYER",
    r"\bimporter\b": "ACTOR_IMPORTER",
    r"\bdistributor\b": "ACTOR_DISTRIBUTOR",
    r"\bnotified bod": "ACTOR_NOTIFIED_BODY",
    r"\bmarket surveillance\b": "ACTOR_MARKET_SURVEILLANCE",
    r"\bauthorised representative\b": "ACTOR_AUTHORISED_REP",
    r"\baffected person\b": "ACTOR_AFFECTED_PERSON",
    r"\bmember state\b": "MEMBER_STATE",
    r"\bcommission\b": "EU_COMMISSION",
}


class ObligationExtractor:
    """Extract obligations, prohibitions, exemptions, and permissions from articles."""

    def __init__(self, use_llm: bool = False, genai_client: Any = None, model: str = "gemini-2.5-flash"):
        self.use_llm = use_llm
        self.client = genai_client
        self.model = model
        self._request_count = 0
        self._last_request_time = 0.0

    def extract_from_articles(
        self, articles: list[dict[str, Any]], regulation_id: str
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Extract obligations and exemptions from all articles.

        Returns:
            (obligations, exemptions) - lists of entity dicts
        """
        prefix = "GDPR" if regulation_id == "GDPR" else "AIACT"
        obligations: list[dict[str, Any]] = []
        exemptions: list[dict[str, Any]] = []

        for article in articles:
            art_id = article["id"]
            full_text = article.get("full_text", "")
            paragraphs = article.get("paragraphs", {})

            # paragraphs is dict: {"1": "text" or {"intro": ..., "a": ...}, "2": ...}
            flat_paras: list[tuple[str, str]] = []  # (para_num, text)

            if isinstance(paragraphs, dict) and paragraphs:
                for para_key, para_val in paragraphs.items():
                    if isinstance(para_val, dict):
                        # Has sub-items: join intro + sub-items
                        parts = []
                        if para_val.get("intro"):
                            parts.append(para_val["intro"])
                        for sub_key in sorted(para_val.keys()):
                            if sub_key != "intro" and isinstance(para_val[sub_key], str):
                                parts.append(para_val[sub_key])
                        para_text = " ".join(parts)
                    elif isinstance(para_val, str):
                        para_text = para_val
                    else:
                        continue
                    flat_paras.append((para_key, para_text))
            elif full_text:
                # Fallback: split full_text on paragraph numbers
                para_splits = re.split(r"(?:^|\n)(\d+)\.\s+", full_text)
                for i in range(1, len(para_splits) - 1, 2):
                    flat_paras.append((para_splits[i], para_splits[i + 1].strip()))
                if not flat_paras:
                    flat_paras.append(("0", full_text))

            # Process each paragraph
            for para_num, para_text in flat_paras:
                if not para_text:
                    continue

                detected = self._classify_paragraph(para_text)
                if not detected:
                    continue

                for det_type, signal_text in detected:
                    entity_id = f"{prefix}_OBL_{art_id.split('_')[-1]}_P{para_num}_{det_type}"

                    duty_bearer = self._detect_actor(para_text, is_bearer=True)
                    right_holder = self._detect_actor(para_text, is_bearer=False)
                    condition = self._detect_condition(para_text)

                    entity = {
                        "id": entity_id,
                        "name": f"Art {art_id.split('_')[-1]} Para {para_num} - {det_type}",
                        "regulation_id": regulation_id,
                        "article_reference": art_id,
                        "paragraph_number": para_num,
                        "obligation_type": det_type,
                        "duty_bearer": duty_bearer,
                        "right_holder": right_holder,
                        "condition": condition,
                        "description": para_text[:200],
                        "source_text": para_text,
                    }

                    if det_type == "EXEMPTION":
                        entity["type"] = "Exemption"
                        exemptions.append(entity)
                    else:
                        entity["type"] = "Obligation"
                        obligations.append(entity)

        # If LLM is enabled, refine a calibration set
        if self.use_llm and self.client:
            obligations = self._llm_refine(obligations[:10]) + obligations[10:]

        return obligations, exemptions

    def _classify_paragraph(self, text: str) -> list[tuple[str, str]]:
        """Classify a paragraph into obligation types.

        Returns list of (type, matched_signal) tuples.
        We return at most one per category to avoid duplicates.
        """
        found: dict[str, str] = {}

        # Check exemptions first (they override obligations)
        for pattern, det_type in EXEMPTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) and det_type not in found:
                found[det_type] = pattern
                break  # One exemption signal is enough

        # Check prohibitions
        for pattern, det_type in PROHIBITION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) and det_type not in found:
                found[det_type] = pattern
                break

        # Check obligations (only if no prohibition found)
        if "MUST_NOT" not in found:
            for pattern, det_type in OBLIGATION_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE) and det_type not in found:
                    found[det_type] = pattern
                    break

        # Check permissions
        for pattern, det_type in PERMISSION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE) and det_type not in found:
                found[det_type] = pattern
                break

        return [(t, s) for t, s in found.items()]

    def _detect_actor(self, text: str, is_bearer: bool = True) -> str | None:
        """Detect duty_bearer (subject before 'shall') or right_holder (object/beneficiary)."""
        # Simple heuristic: first actor mention before "shall" = bearer
        # Actor mentions after "shall" = right holder
        text_lower = text.lower()

        if is_bearer:
            # Look for actor before first obligation keyword
            shall_pos = len(text_lower)
            for kw in ["shall", "must", "is required"]:
                pos = text_lower.find(kw)
                if pos != -1 and pos < shall_pos:
                    shall_pos = pos

            search_text = text_lower[:shall_pos]
        else:
            # Look for actor after first obligation keyword
            shall_pos = 0
            for kw in ["shall", "must", "is required"]:
                pos = text_lower.find(kw)
                if pos != -1:
                    shall_pos = pos
                    break
            search_text = text_lower[shall_pos:]

        for pattern, actor_id in ACTOR_MAP.items():
            if re.search(pattern, search_text):
                return actor_id

        return None

    def _detect_condition(self, text: str) -> str | None:
        """Extract condition clause if present."""
        # Common condition patterns
        patterns = [
            r"(?:where|if|provided that|subject to|unless)\s+(.{10,100}?)(?:\.|,\s*the\s+)",
            r"(?:in the case of|in cases where)\s+(.{10,100}?)(?:\.|,)",
        ]
        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return None

    def _llm_refine(self, obligations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Use Gemini to refine/validate a batch of obligations.

        This is the calibration step: run on 10 gold-standard articles,
        compare rule-based vs LLM output, then decide if full LLM pass is needed.
        """
        if not obligations:
            return obligations

        # Rate limit: 15 RPM on free tier
        self._rate_limit()

        prompt = self._build_refinement_prompt(obligations)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            refined = self._parse_llm_response(response.text, obligations)
            return refined
        except Exception as e:
            print(f"  LLM refinement failed: {e}")
            return obligations

    def _rate_limit(self) -> None:
        """Enforce rate limit of 15 RPM."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < 4.0:  # 60s / 15 = 4s between requests
            time.sleep(4.0 - elapsed)
        self._last_request_time = time.time()
        self._request_count += 1

    def _build_refinement_prompt(self, obligations: list[dict[str, Any]]) -> str:
        """Build prompt for LLM refinement."""
        items = []
        for o in obligations:
            items.append(
                f"ID: {o['id']}\n"
                f"Type: {o['obligation_type']}\n"
                f"Bearer: {o.get('duty_bearer', 'unknown')}\n"
                f"Text: {o['source_text'][:300]}\n"
            )

        return (
            "You are a legal analysis assistant. For each obligation below, validate and improve:\n"
            "1. Is the obligation_type correct? (SHALL, MUST, MUST_NOT, MAY, EXEMPTION)\n"
            "2. Who is the duty_bearer? (controller, processor, provider, deployer, etc.)\n"
            "3. Who is the right_holder? (data_subject, affected_person, etc.)\n"
            "4. What is the condition/trigger?\n"
            "5. Write a 1-sentence plain-language description.\n\n"
            "Return JSON array with fields: id, obligation_type, duty_bearer, right_holder, condition, description\n\n"
            + "\n---\n".join(items)
        )

    def _parse_llm_response(
        self, response_text: str, originals: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Parse LLM response and merge with originals."""
        # Try to extract JSON from response
        json_match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if not json_match:
            return originals

        try:
            refined = json.loads(json_match.group())
        except json.JSONDecodeError:
            return originals

        # Merge refinements into originals by ID
        refined_map = {r["id"]: r for r in refined if "id" in r}
        for orig in originals:
            if orig["id"] in refined_map:
                ref = refined_map[orig["id"]]
                if ref.get("obligation_type"):
                    orig["obligation_type"] = ref["obligation_type"]
                if ref.get("duty_bearer"):
                    orig["duty_bearer"] = ref["duty_bearer"]
                if ref.get("right_holder"):
                    orig["right_holder"] = ref["right_holder"]
                if ref.get("condition"):
                    orig["condition"] = ref["condition"]
                if ref.get("description"):
                    orig["description"] = ref["description"]

        return originals
