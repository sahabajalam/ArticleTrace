"""Hand-curated right extraction from GDPR Art 12-22 and AI Act Art 85-86.

Rights are specific entitlements granted to data subjects (GDPR) or affected persons (AI Act).
Each right maps to its source article(s) and the right holder.
"""

from __future__ import annotations

from typing import Any


# ── Right definitions ────────────────────────────────────────────────────────

GDPR_RIGHTS = [
    {"id": "RIGHT_TRANSPARENT_INFO", "name": "Right to Transparent Information",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_12"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to receive information in a concise, transparent, intelligible and easily accessible form"},
    {"id": "RIGHT_INFORMATION_COLLECTED", "name": "Right to Information (Direct Collection)",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_13"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to be informed when personal data is collected directly from the data subject"},
    {"id": "RIGHT_INFORMATION_INDIRECT", "name": "Right to Information (Indirect Collection)",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_14"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to be informed when personal data is obtained from sources other than the data subject"},
    {"id": "RIGHT_ACCESS", "name": "Right of Access",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_15"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to obtain confirmation of processing and access to personal data and supplementary information"},
    {"id": "RIGHT_RECTIFICATION", "name": "Right to Rectification",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_16"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to have inaccurate personal data rectified without undue delay"},
    {"id": "RIGHT_ERASURE", "name": "Right to Erasure (Right to be Forgotten)",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_17"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to have personal data erased when no longer necessary, consent withdrawn, or unlawfully processed"},
    {"id": "RIGHT_RESTRICTION", "name": "Right to Restriction of Processing",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_18"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to restrict processing in certain circumstances (accuracy contested, unlawful, no longer needed)"},
    {"id": "RIGHT_NOTIFICATION", "name": "Right to Notification of Rectification/Erasure/Restriction",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_19"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to be informed about recipients notified of rectification, erasure, or restriction"},
    {"id": "RIGHT_PORTABILITY", "name": "Right to Data Portability",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_20"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to receive personal data in structured, commonly used, machine-readable format and transmit to another controller"},
    {"id": "RIGHT_OBJECT", "name": "Right to Object",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_21"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to object to processing based on legitimate interest or public interest, including profiling"},
    {"id": "RIGHT_AUTOMATED_DECISIONS", "name": "Right Not to be Subject to Automated Decisions",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_22"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right not to be subject to decisions based solely on automated processing which produce legal or significant effects"},
    {"id": "RIGHT_LODGE_COMPLAINT", "name": "Right to Lodge a Complaint",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_77"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to lodge a complaint with a supervisory authority"},
    {"id": "RIGHT_EFFECTIVE_REMEDY_SA", "name": "Right to Effective Judicial Remedy (Against SA)",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_78"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to effective judicial remedy against a supervisory authority decision"},
    {"id": "RIGHT_EFFECTIVE_REMEDY_CTRL", "name": "Right to Effective Judicial Remedy (Against Controller/Processor)",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_79"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to effective judicial remedy against a controller or processor"},
    {"id": "RIGHT_COMPENSATION", "name": "Right to Compensation",
     "regulation_id": "GDPR", "source_articles": ["GDPR_ART_82"],
     "right_holder": "ACTOR_DATA_SUBJECT",
     "description": "Right to receive compensation for material or non-material damage from GDPR infringement"},
]

AI_ACT_RIGHTS = [
    {"id": "RIGHT_AI_EXPLANATION", "name": "Right to Explanation of AI Decision",
     "regulation_id": "EU_AI_ACT", "source_articles": ["AIACT_ART_86"],
     "right_holder": "ACTOR_AFFECTED_PERSON",
     "description": "Right of affected persons to obtain clear and meaningful explanations of AI system decisions affecting their rights"},
    {"id": "RIGHT_AI_COMPLAINT", "name": "Right to Complain About AI System",
     "regulation_id": "EU_AI_ACT", "source_articles": ["AIACT_ART_85"],
     "right_holder": "ACTOR_AFFECTED_PERSON",
     "description": "Right to lodge a complaint with market surveillance authority about AI system non-compliance"},
    {"id": "RIGHT_AI_EFFECTIVE_REMEDY", "name": "Right to Effective Remedy (AI Act)",
     "regulation_id": "EU_AI_ACT", "source_articles": ["AIACT_ART_85"],
     "right_holder": "ACTOR_AFFECTED_PERSON",
     "description": "Right to effective judicial remedy in relation to AI system decisions"},
    {"id": "RIGHT_AI_NOTIFICATION", "name": "Right to AI System Disclosure",
     "regulation_id": "EU_AI_ACT", "source_articles": ["AIACT_ART_50"],
     "right_holder": "ACTOR_AFFECTED_PERSON",
     "description": "Right to be informed when interacting with an AI system or when subject to emotion recognition/biometric categorisation"},
]

ALL_RIGHTS = GDPR_RIGHTS + AI_ACT_RIGHTS


class RightExtractor:
    """Extract right entities and their relationships from curated definitions."""

    def extract_all(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Extract all rights and build relationships.

        Returns:
            (rights, relationships) - rights entities and their links to articles/actors.
        """
        rights: list[dict[str, Any]] = []
        relationships: list[dict[str, Any]] = []

        for right_def in ALL_RIGHTS:
            right = {
                "id": right_def["id"],
                "type": "Right",
                "name": right_def["name"],
                "regulation_id": right_def["regulation_id"],
                "source_article": right_def["source_articles"][0],
                "right_holder": right_def["right_holder"],
                "description": right_def["description"],
                "conditions": [],
            }
            rights.append(right)

            # APPLIES_TO: right -> source article(s)
            for art_id in right_def["source_articles"]:
                relationships.append({
                    "source_id": right_def["id"],
                    "target_id": art_id,
                    "type": "APPLIES_TO",
                    "properties": {"role": "source_article"},
                })

            # APPLIES_TO: right -> right holder actor
            if right_def["right_holder"]:
                relationships.append({
                    "source_id": right_def["id"],
                    "target_id": right_def["right_holder"],
                    "type": "APPLIES_TO",
                    "properties": {"role": "right_holder"},
                })

        # Cross-regulation links between overlapping rights
        cross_links = self._build_cross_links()
        relationships.extend(cross_links)

        return rights, relationships

    def _build_cross_links(self) -> list[dict[str, Any]]:
        """Build REFERENCES edges between related rights across regulations."""
        links = [
            # GDPR automated decisions <-> AI Act explanation
            ("RIGHT_AUTOMATED_DECISIONS", "RIGHT_AI_EXPLANATION"),
            # GDPR complaint <-> AI Act complaint
            ("RIGHT_LODGE_COMPLAINT", "RIGHT_AI_COMPLAINT"),
            # GDPR judicial remedy <-> AI Act remedy
            ("RIGHT_EFFECTIVE_REMEDY_CTRL", "RIGHT_AI_EFFECTIVE_REMEDY"),
        ]

        rels = []
        for src, tgt in links:
            rels.append({
                "source_id": src,
                "target_id": tgt,
                "type": "REFERENCES",
                "properties": {"link_type": "cross_regulation_right"},
            })
        return rels
