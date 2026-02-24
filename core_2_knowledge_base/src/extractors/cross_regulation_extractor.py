"""Cross-regulation COMPLEMENTS edge extraction.

Maps known interactions between GDPR and EU AI Act articles.
Each edge has an interaction_type property:
  REINFORCES, CREATES_EXCEPTION, CO_TRIGGERS, CUMULATIVE, DELEGATES

Sources:
- Explicit cross-references found during Phase 1 parsing
- Known mappings from legal analysis (hand-curated for accuracy)
"""

from __future__ import annotations

from typing import Any


# Hand-curated cross-regulation mappings with interaction types
# Format: (gdpr_art, ai_act_art, interaction_type, description)
CROSS_MAPPINGS: list[tuple[str, str, str, str]] = [
    # --- REINFORCES: AI Act strengthens/extends GDPR requirement ---
    ("GDPR_ART_22", "AIACT_ART_14", "REINFORCES",
     "Automated decision-making (GDPR) reinforced by human oversight requirements (AI Act)"),
    ("GDPR_ART_13", "AIACT_ART_13", "REINFORCES",
     "Information provision to data subjects (GDPR) reinforced by transparency requirements (AI Act)"),
    ("GDPR_ART_14", "AIACT_ART_13", "REINFORCES",
     "Information for indirect collection (GDPR) reinforced by AI Act transparency"),
    ("GDPR_ART_5", "AIACT_ART_10", "REINFORCES",
     "Data quality principles (GDPR) reinforced by training data governance (AI Act)"),
    ("GDPR_ART_25", "AIACT_ART_9", "REINFORCES",
     "Data protection by design (GDPR) reinforced by risk management system (AI Act)"),
    ("GDPR_ART_32", "AIACT_ART_15", "REINFORCES",
     "Security of processing (GDPR) reinforced by accuracy/robustness/cybersecurity (AI Act)"),
    ("GDPR_ART_30", "AIACT_ART_12", "REINFORCES",
     "Records of processing (GDPR) reinforced by record-keeping/logging (AI Act)"),
    ("GDPR_ART_12", "AIACT_ART_50", "REINFORCES",
     "Transparent communication (GDPR) reinforced by AI transparency obligations"),
    ("GDPR_ART_15", "AIACT_ART_86", "REINFORCES",
     "Right of access (GDPR) reinforced by right to explanation for AI decisions (AI Act)"),
    ("GDPR_ART_22", "AIACT_ART_86", "REINFORCES",
     "Automated decision rights (GDPR) reinforced by AI Act explanation rights"),
    ("GDPR_ART_37", "AIACT_ART_26", "REINFORCES",
     "DPO designation (GDPR) reinforced by deployer human oversight obligation (AI Act)"),
    ("GDPR_ART_24", "AIACT_ART_26", "REINFORCES",
     "Controller responsibility (GDPR) reinforced by deployer obligations (AI Act)"),

    # --- CO_TRIGGERS: Both regulations apply simultaneously ---
    ("GDPR_ART_35", "AIACT_ART_27", "CO_TRIGGERS",
     "DPIA (GDPR) and FRIA (AI Act) both required for high-risk AI processing personal data"),
    ("GDPR_ART_36", "AIACT_ART_27", "CO_TRIGGERS",
     "Prior consultation with DPA (GDPR) co-triggered with fundamental rights impact assessment (AI Act)"),
    ("GDPR_ART_6", "AIACT_ART_10", "CO_TRIGGERS",
     "Legal basis for processing (GDPR) + training data requirements (AI Act) both apply to AI training"),
    ("GDPR_ART_9", "AIACT_ART_10", "CO_TRIGGERS",
     "Special category data (GDPR) + bias detection data (AI Act) create dual compliance requirement"),
    ("GDPR_ART_28", "AIACT_ART_25", "CO_TRIGGERS",
     "Processor obligations (GDPR) + provider obligations (AI Act) when processor deploys high-risk AI"),
    ("GDPR_ART_44", "AIACT_ART_5", "CO_TRIGGERS",
     "International transfer rules (GDPR) + prohibited practices (AI Act) both restrict cross-border AI"),
    ("GDPR_ART_7", "AIACT_ART_50", "CO_TRIGGERS",
     "Consent conditions (GDPR) + transparency (AI Act) both apply to AI chatbots processing personal data"),

    # --- CUMULATIVE: Penalties/requirements stack ---
    ("GDPR_ART_83", "AIACT_ART_99", "CUMULATIVE",
     "GDPR fines (up to 4% turnover) + AI Act fines (up to 7%) = cumulative up to 11% turnover"),
    ("GDPR_ART_58", "AIACT_ART_64", "CUMULATIVE",
     "DPA investigative powers (GDPR) + market surveillance powers (AI Act) create dual oversight"),
    ("GDPR_ART_77", "AIACT_ART_85", "CUMULATIVE",
     "Right to lodge complaint with DPA (GDPR) + right to complaint under AI Act = dual remedy"),

    # --- CREATES_EXCEPTION: One regulation creates exception to the other ---
    ("GDPR_ART_9", "AIACT_ART_10", "CREATES_EXCEPTION",
     "AI Act Art 10(5) creates exception to GDPR Art 9 ban: allows special category processing for bias detection"),
    ("GDPR_ART_6", "AIACT_ART_10", "CREATES_EXCEPTION",
     "AI Act Art 10 creates specific legal basis for training data processing beyond GDPR Art 6 grounds"),
    ("GDPR_ART_22", "AIACT_ART_14", "CREATES_EXCEPTION",
     "AI Act human oversight may satisfy GDPR Art 22(3) 'suitable measures' requirement"),
    ("GDPR_ART_17", "AIACT_ART_12", "CREATES_EXCEPTION",
     "AI Act logging requirements may limit right to erasure when logs needed for compliance"),
    ("GDPR_ART_5", "AIACT_ART_10", "CREATES_EXCEPTION",
     "AI Act training data retention may create exception to GDPR storage limitation principle"),

    # --- DELEGATES: One regulation defers to the other ---
    ("GDPR_ART_2", "AIACT_ART_2", "DELEGATES",
     "AI Act Art 2(7) defers to GDPR for personal data processing: 'This Regulation is without prejudice to' GDPR"),
    ("GDPR_ART_51", "AIACT_ART_70", "DELEGATES",
     "GDPR DPAs have jurisdiction for AI systems processing personal data; AI Act national authorities for other AI matters"),
    ("GDPR_ART_40", "AIACT_ART_69", "DELEGATES",
     "GDPR codes of conduct + AI Act codes of practice: each regulation owns its domain"),
    ("GDPR_ART_42", "AIACT_ART_43", "DELEGATES",
     "GDPR certification + AI Act conformity assessment: separate but complementary schemes"),
    ("GDPR_ART_45", "AIACT_ART_5", "DELEGATES",
     "Adequacy decisions (GDPR) remain with Commission; AI Act prohibited practices independently assessed"),

    # --- Additional mappings for completeness ---
    ("GDPR_ART_33", "AIACT_ART_62", "CO_TRIGGERS",
     "Data breach notification (GDPR) + serious incident reporting (AI Act) both triggered by AI system failures"),
    ("GDPR_ART_34", "AIACT_ART_62", "CO_TRIGGERS",
     "Communication to data subjects (GDPR) + incident reporting (AI Act) create dual notification duty"),
    ("GDPR_ART_16", "AIACT_ART_15", "REINFORCES",
     "Right to rectification (GDPR) reinforced by AI Act accuracy requirements"),
    ("GDPR_ART_21", "AIACT_ART_14", "REINFORCES",
     "Right to object (GDPR) reinforced by human oversight right to override AI (AI Act)"),
    ("GDPR_ART_20", "AIACT_ART_11", "REINFORCES",
     "Data portability (GDPR) related to AI Act technical documentation requirements"),
    ("GDPR_ART_39", "AIACT_ART_26", "REINFORCES",
     "DPO tasks (GDPR) complemented by deployer monitoring obligations (AI Act)"),
    ("GDPR_ART_47", "AIACT_ART_5", "CO_TRIGGERS",
     "Binding corporate rules (GDPR) + prohibited practices (AI Act) for multinational AI deployments"),
    ("GDPR_ART_49", "AIACT_ART_5", "CO_TRIGGERS",
     "Transfer derogations (GDPR) + prohibited practices (AI Act) for international AI systems"),

    # Annex-level links
    ("GDPR_ART_35", "AIACT_ART_6", "CO_TRIGGERS",
     "DPIA (GDPR) co-triggered when AI system classified as high-risk under Art 6/Annex III"),
    ("GDPR_ART_9", "AIACT_ART_6", "CO_TRIGGERS",
     "Special category processing (GDPR) intersects with high-risk AI classification (AI Act)"),
]


class CrossRegulationExtractor:
    """Extract COMPLEMENTS edges between GDPR and AI Act articles."""

    def extract_cross_regulation_edges(self) -> list[dict[str, Any]]:
        """Generate all cross-regulation COMPLEMENTS relationships.

        Each relationship has:
        - source_id: GDPR article
        - target_id: AI Act article
        - type: COMPLEMENTS
        - properties: {interaction_type, description}
        """
        edges: list[dict[str, Any]] = []
        seen: set[str] = set()

        for gdpr_art, ai_art, interaction, desc in CROSS_MAPPINGS:
            # Create bidirectional key to avoid exact duplicates
            key = f"{gdpr_art}|{ai_art}|{interaction}"
            if key in seen:
                continue
            seen.add(key)

            edges.append({
                "source_id": gdpr_art,
                "target_id": ai_art,
                "type": "COMPLEMENTS",
                "properties": {
                    "interaction_type": interaction,
                    "description": desc,
                },
            })

            # Also add reverse direction
            edges.append({
                "source_id": ai_art,
                "target_id": gdpr_art,
                "type": "COMPLEMENTS",
                "properties": {
                    "interaction_type": interaction,
                    "description": desc,
                },
            })

        return edges

    def extract_auto_cross_references(
        self, gdpr_articles: list[dict], ai_articles: list[dict]
    ) -> list[dict[str, Any]]:
        """Auto-detect additional cross-references from parsed article text.

        Looks for GDPR articles referencing AI Act and vice versa.
        These supplement the hand-curated mappings.
        """
        edges: list[dict[str, Any]] = []

        # Build valid ID sets
        gdpr_ids = {a["id"] for a in gdpr_articles}
        ai_ids = {a["id"] for a in ai_articles}

        # Check if GDPR articles reference AI Act articles
        for art in gdpr_articles:
            for ref in art.get("cross_references", []):
                if ref in ai_ids:
                    edges.append({
                        "source_id": art["id"],
                        "target_id": ref,
                        "type": "COMPLEMENTS",
                        "properties": {
                            "interaction_type": "REFERENCES",
                            "description": f"Auto-detected: {art['id']} references {ref}",
                            "auto_detected": True,
                        },
                    })

        # Check if AI Act articles reference GDPR articles
        for art in ai_articles:
            for ref in art.get("cross_references", []):
                if ref in gdpr_ids:
                    edges.append({
                        "source_id": art["id"],
                        "target_id": ref,
                        "type": "COMPLEMENTS",
                        "properties": {
                            "interaction_type": "REFERENCES",
                            "description": f"Auto-detected: {art['id']} references {ref}",
                            "auto_detected": True,
                        },
                    })

        return edges
