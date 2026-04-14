"""Hand-curated concept extraction for GDPR and EU AI Act.

Concepts are abstract legal/compliance notions that appear across multiple articles.
Unlike definitions (which have formal "X means Y" text), concepts are identified by
their recurrence and legal significance.

Categories:
  - GDPR principles (Art 5)
  - Processing operations
  - Compliance concepts
  - AI Act concepts
"""

from __future__ import annotations

import re
from typing import Any


# ── Concept definitions ──────────────────────────────────────────────────────

GDPR_PRINCIPLES = [
    {"id": "CONCEPT_LAWFULNESS", "name": "Lawfulness", "category": "gdpr_principle",
     "description": "Personal data must be processed lawfully, with a valid legal basis (Art 6)",
     "article_patterns": [r"GDPR_ART_5", r"GDPR_ART_6"],
     "keywords": ["lawful", "lawfulness", "legal basis", "legitimacy"]},
    {"id": "CONCEPT_FAIRNESS", "name": "Fairness", "category": "gdpr_principle",
     "description": "Personal data must be processed fairly, without adverse effects on data subjects",
     "article_patterns": [r"GDPR_ART_5"],
     "keywords": ["fair", "fairness", "fairly"]},
    {"id": "CONCEPT_TRANSPARENCY", "name": "Transparency", "category": "gdpr_principle",
     "description": "Data processing must be transparent to data subjects (Art 12-14)",
     "article_patterns": [r"GDPR_ART_5", r"GDPR_ART_12", r"GDPR_ART_13", r"GDPR_ART_14"],
     "keywords": ["transparent", "transparency", "inform", "information"]},
    {"id": "CONCEPT_PURPOSE_LIMITATION", "name": "Purpose Limitation", "category": "gdpr_principle",
     "description": "Data collected for specified, explicit, legitimate purposes only",
     "article_patterns": [r"GDPR_ART_5"],
     "keywords": ["purpose limitation", "specified purpose", "legitimate purpose"]},
    {"id": "CONCEPT_DATA_MINIMISATION", "name": "Data Minimisation", "category": "gdpr_principle",
     "description": "Data must be adequate, relevant, and limited to what is necessary",
     "article_patterns": [r"GDPR_ART_5"],
     "keywords": ["data minimisation", "minimisation", "adequate", "relevant and limited"]},
    {"id": "CONCEPT_ACCURACY", "name": "Accuracy", "category": "gdpr_principle",
     "description": "Personal data must be accurate and kept up to date",
     "article_patterns": [r"GDPR_ART_5", r"GDPR_ART_16"],
     "keywords": ["accuracy", "accurate", "inaccurate", "rectif"]},
    {"id": "CONCEPT_STORAGE_LIMITATION", "name": "Storage Limitation", "category": "gdpr_principle",
     "description": "Data kept in identifiable form no longer than necessary",
     "article_patterns": [r"GDPR_ART_5"],
     "keywords": ["storage limitation", "retention", "no longer than necessary"]},
    {"id": "CONCEPT_INTEGRITY_CONFIDENTIALITY", "name": "Integrity and Confidentiality", "category": "gdpr_principle",
     "description": "Appropriate security measures to protect personal data",
     "article_patterns": [r"GDPR_ART_5", r"GDPR_ART_32"],
     "keywords": ["integrity", "confidentiality", "security of processing", "appropriate security"]},
    {"id": "CONCEPT_ACCOUNTABILITY", "name": "Accountability", "category": "gdpr_principle",
     "description": "Controller must demonstrate compliance with data protection principles",
     "article_patterns": [r"GDPR_ART_5", r"GDPR_ART_24"],
     "keywords": ["accountability", "demonstrate compliance", "responsible for"]},
]

PROCESSING_OPERATIONS = [
    {"id": "CONCEPT_PROFILING", "name": "Profiling", "category": "processing_operation",
     "description": "Automated processing to evaluate personal aspects of a natural person",
     "article_patterns": [r"GDPR_ART_4", r"GDPR_ART_22", r"AIACT_ART_6"],
     "keywords": ["profiling", "evaluating personal aspects", "automated processing"]},
    {"id": "CONCEPT_AUTOMATED_DECISION", "name": "Automated Decision-Making", "category": "processing_operation",
     "description": "Decisions based solely on automated processing with legal or similar effects",
     "article_patterns": [r"GDPR_ART_22", r"AIACT_ART_14", r"AIACT_ART_86"],
     "keywords": ["automated decision", "solely automated", "without human intervention"]},
    {"id": "CONCEPT_PSEUDONYMISATION", "name": "Pseudonymisation", "category": "processing_operation",
     "description": "Processing so data cannot be attributed without additional information",
     "article_patterns": [r"GDPR_ART_4", r"GDPR_ART_25", r"GDPR_ART_32"],
     "keywords": ["pseudonymisation", "pseudonymised", "pseudonymization"]},
    {"id": "CONCEPT_CONSENT", "name": "Consent", "category": "processing_operation",
     "description": "Freely given, specific, informed, unambiguous indication of agreement",
     "article_patterns": [r"GDPR_ART_4", r"GDPR_ART_6", r"GDPR_ART_7", r"GDPR_ART_8", r"GDPR_ART_9"],
     "keywords": ["consent", "freely given", "unambiguous"]},
    {"id": "CONCEPT_LEGITIMATE_INTEREST", "name": "Legitimate Interest", "category": "processing_operation",
     "description": "Legal basis for processing where controller's interest is not overridden by data subject rights",
     "article_patterns": [r"GDPR_ART_6"],
     "keywords": ["legitimate interest", "balancing test", "overridden by"]},
    {"id": "CONCEPT_INTERNATIONAL_TRANSFER", "name": "International Data Transfer", "category": "processing_operation",
     "description": "Transfer of personal data to third countries or international organisations",
     "article_patterns": [r"GDPR_ART_44", r"GDPR_ART_45", r"GDPR_ART_46", r"GDPR_ART_47", r"GDPR_ART_48", r"GDPR_ART_49"],
     "keywords": ["transfer", "third country", "adequacy", "appropriate safeguards"]},
    {"id": "CONCEPT_DATA_BREACH", "name": "Data Breach", "category": "processing_operation",
     "description": "Breach of security leading to accidental or unlawful destruction, loss, alteration, or disclosure",
     "article_patterns": [r"GDPR_ART_4", r"GDPR_ART_33", r"GDPR_ART_34"],
     "keywords": ["data breach", "personal data breach", "security incident"]},
    {"id": "CONCEPT_JOINT_CONTROLLERSHIP", "name": "Joint Controllership", "category": "processing_operation",
     "description": "Two or more controllers jointly determine purposes and means of processing",
     "article_patterns": [r"GDPR_ART_26"],
     "keywords": ["joint controller", "jointly determine"]},
    {"id": "CONCEPT_DATA_PROTECTION_BY_DESIGN", "name": "Data Protection by Design and Default", "category": "processing_operation",
     "description": "Implementing data protection principles through technical and organisational measures from the design stage",
     "article_patterns": [r"GDPR_ART_25"],
     "keywords": ["by design", "by default", "data protection by design"]},
    {"id": "CONCEPT_SPECIAL_CATEGORY_PROCESSING", "name": "Special Category Processing", "category": "processing_operation",
     "description": "Processing of sensitive personal data under Art 9 with specific safeguards",
     "article_patterns": [r"GDPR_ART_9"],
     "keywords": ["special categor", "sensitive data", "article 9"]},
]

COMPLIANCE_CONCEPTS = [
    {"id": "CONCEPT_DPIA", "name": "Data Protection Impact Assessment", "category": "compliance_concept",
     "description": "Assessment of impact of processing operations on data subject rights (Art 35)",
     "article_patterns": [r"GDPR_ART_35", r"GDPR_ART_36"],
     "keywords": ["impact assessment", "DPIA", "data protection impact"]},
    {"id": "CONCEPT_PRIOR_CONSULTATION", "name": "Prior Consultation", "category": "compliance_concept",
     "description": "Consulting supervisory authority before high-risk processing (Art 36)",
     "article_patterns": [r"GDPR_ART_36"],
     "keywords": ["prior consultation", "consult the supervisory"]},
    {"id": "CONCEPT_RECORDS_OF_PROCESSING", "name": "Records of Processing Activities", "category": "compliance_concept",
     "description": "Maintaining records of all processing activities under controller/processor responsibility",
     "article_patterns": [r"GDPR_ART_30"],
     "keywords": ["records of processing", "record of processing", "maintain a record"]},
    {"id": "CONCEPT_DATA_BREACH_NOTIFICATION", "name": "Data Breach Notification", "category": "compliance_concept",
     "description": "Notifying supervisory authority and data subjects of personal data breaches",
     "article_patterns": [r"GDPR_ART_33", r"GDPR_ART_34"],
     "keywords": ["breach notification", "notify the supervisory", "notify the data subject", "without undue delay"]},
    {"id": "CONCEPT_DPO_DESIGNATION", "name": "DPO Designation", "category": "compliance_concept",
     "description": "Designating a Data Protection Officer when required",
     "article_patterns": [r"GDPR_ART_37", r"GDPR_ART_38", r"GDPR_ART_39"],
     "keywords": ["data protection officer", "designate a DPO", "DPO"]},
    {"id": "CONCEPT_CERTIFICATION", "name": "Certification", "category": "compliance_concept",
     "description": "Voluntary certification mechanisms to demonstrate GDPR compliance",
     "article_patterns": [r"GDPR_ART_42", r"GDPR_ART_43"],
     "keywords": ["certification", "seal", "mark", "accreditation"]},
    {"id": "CONCEPT_CODES_OF_CONDUCT", "name": "Codes of Conduct", "category": "compliance_concept",
     "description": "Approved codes of conduct as compliance tool",
     "article_patterns": [r"GDPR_ART_40", r"GDPR_ART_41"],
     "keywords": ["code of conduct", "codes of conduct"]},
    {"id": "CONCEPT_ONE_STOP_SHOP", "name": "One-Stop-Shop Mechanism", "category": "compliance_concept",
     "description": "Lead supervisory authority mechanism for cross-border processing",
     "article_patterns": [r"GDPR_ART_56", r"GDPR_ART_60"],
     "keywords": ["one-stop-shop", "lead supervisory", "cross-border"]},
    {"id": "CONCEPT_BINDING_CORPORATE_RULES", "name": "Binding Corporate Rules", "category": "compliance_concept",
     "description": "Internal rules for international data transfers within a group of enterprises",
     "article_patterns": [r"GDPR_ART_47"],
     "keywords": ["binding corporate rules", "BCR"]},
    {"id": "CONCEPT_STANDARD_CONTRACTUAL_CLAUSES", "name": "Standard Contractual Clauses", "category": "compliance_concept",
     "description": "Commission-approved clauses for international data transfers",
     "article_patterns": [r"GDPR_ART_46"],
     "keywords": ["standard contractual clauses", "SCC", "model clauses"]},
    {"id": "CONCEPT_ADEQUACY_DECISION", "name": "Adequacy Decision", "category": "compliance_concept",
     "description": "Commission decision that a third country provides adequate data protection",
     "article_patterns": [r"GDPR_ART_45"],
     "keywords": ["adequacy decision", "adequate level of protection"]},
    {"id": "CONCEPT_SUPERVISORY_COOPERATION", "name": "Supervisory Authority Cooperation", "category": "compliance_concept",
     "description": "Cooperation and consistency mechanisms between supervisory authorities",
     "article_patterns": [r"GDPR_ART_60", r"GDPR_ART_61", r"GDPR_ART_63"],
     "keywords": ["mutual assistance", "consistency mechanism", "cooperation"]},
    {"id": "CONCEPT_PROCESSOR_AGREEMENT", "name": "Processor Agreement", "category": "compliance_concept",
     "description": "Binding contract or legal act governing processing by a processor",
     "article_patterns": [r"GDPR_ART_28"],
     "keywords": ["processor agreement", "binding contract", "on behalf of"]},
]

AI_CONCEPTS = [
    {"id": "CONCEPT_CONFORMITY_ASSESSMENT", "name": "Conformity Assessment", "category": "ai_concept",
     "description": "Process demonstrating that high-risk AI system meets requirements",
     "article_patterns": [r"AIACT_ART_43", r"AIACT_ART_40", r"AIACT_ART_41", r"AIACT_ART_42"],
     "keywords": ["conformity assessment", "harmonised standards"]},
    {"id": "CONCEPT_RISK_MANAGEMENT", "name": "AI Risk Management System", "category": "ai_concept",
     "description": "Continuous iterative process for managing risks of high-risk AI systems",
     "article_patterns": [r"AIACT_ART_9"],
     "keywords": ["risk management system", "risk management", "identify and analys"]},
    {"id": "CONCEPT_HUMAN_OVERSIGHT", "name": "Human Oversight", "category": "ai_concept",
     "description": "Measures enabling human oversight of high-risk AI systems during use",
     "article_patterns": [r"AIACT_ART_14", r"GDPR_ART_22"],
     "keywords": ["human oversight", "human intervention", "human-in-the-loop", "human-on-the-loop"]},
    {"id": "CONCEPT_TECHNICAL_DOCUMENTATION", "name": "Technical Documentation", "category": "ai_concept",
     "description": "Documentation demonstrating compliance with AI Act requirements",
     "article_patterns": [r"AIACT_ART_11", r"AIACT_ART_53", r"AIACT_ANNEX_IV"],
     "keywords": ["technical documentation", "documentation requirements"]},
    {"id": "CONCEPT_CE_MARKING", "name": "CE Marking", "category": "ai_concept",
     "description": "Marking indicating AI system conformity with EU legislation",
     "article_patterns": [r"AIACT_ART_48", r"AIACT_ART_49"],
     "keywords": ["CE marking", "CE mark", "declaration of conformity"]},
    {"id": "CONCEPT_REGULATORY_SANDBOX", "name": "AI Regulatory Sandbox", "category": "ai_concept",
     "description": "Controlled environment for testing innovative AI systems under regulatory supervision",
     "article_patterns": [r"AIACT_ART_57", r"AIACT_ART_58", r"AIACT_ART_59", r"AIACT_ART_60"],
     "keywords": ["regulatory sandbox", "sandbox", "controlled environment"]},
    {"id": "CONCEPT_FRIA", "name": "Fundamental Rights Impact Assessment", "category": "ai_concept",
     "description": "Assessment of AI system impact on fundamental rights before deployment",
     "article_patterns": [r"AIACT_ART_27"],
     "keywords": ["fundamental rights impact", "FRIA", "impact assessment"]},
    {"id": "CONCEPT_DATA_GOVERNANCE", "name": "AI Data Governance", "category": "ai_concept",
     "description": "Governance and management practices for training, validation, and testing data",
     "article_patterns": [r"AIACT_ART_10"],
     "keywords": ["data governance", "training data", "validation data", "testing data"]},
    {"id": "CONCEPT_TRANSPARENCY_OBLIGATION", "name": "AI Transparency Obligation", "category": "ai_concept",
     "description": "Obligation to ensure AI systems are transparent to users and affected persons",
     "article_patterns": [r"AIACT_ART_13", r"AIACT_ART_50", r"AIACT_ART_52"],
     "keywords": ["transparency obligation", "inform natural person", "disclose"]},
    {"id": "CONCEPT_POST_MARKET_MONITORING", "name": "Post-Market Monitoring", "category": "ai_concept",
     "description": "System for actively collecting and reviewing data on AI system performance after deployment",
     "article_patterns": [r"AIACT_ART_72"],
     "keywords": ["post-market monitoring", "post-market", "market surveillance"]},
    {"id": "CONCEPT_SERIOUS_INCIDENT", "name": "Serious Incident Reporting", "category": "ai_concept",
     "description": "Reporting obligations for incidents involving AI systems causing serious harm",
     "article_patterns": [r"AIACT_ART_73"],
     "keywords": ["serious incident", "incident reporting", "malfunction"]},
    {"id": "CONCEPT_RECORD_KEEPING", "name": "AI Record Keeping", "category": "ai_concept",
     "description": "Automatic logging and record-keeping for high-risk AI systems",
     "article_patterns": [r"AIACT_ART_12", r"AIACT_ART_19"],
     "keywords": ["record keeping", "automatic logging", "logs", "traceability"]},
    {"id": "CONCEPT_ROBUSTNESS", "name": "Robustness and Cybersecurity", "category": "ai_concept",
     "description": "Technical robustness and resilience of AI systems against errors and attacks",
     "article_patterns": [r"AIACT_ART_15"],
     "keywords": ["robustness", "resilience", "cybersecurity", "accuracy"]},
    {"id": "CONCEPT_GPAI", "name": "General-Purpose AI Models", "category": "ai_concept",
     "description": "AI models trained on broad data for general tasks, with specific obligations",
     "article_patterns": [r"AIACT_ART_51", r"AIACT_ART_52", r"AIACT_ART_53", r"AIACT_ART_54", r"AIACT_ART_55", r"AIACT_ART_56"],
     "keywords": ["general-purpose AI", "GPAI", "foundation model"]},
    {"id": "CONCEPT_SYSTEMIC_RISK", "name": "Systemic Risk", "category": "ai_concept",
     "description": "Risk specific to high-impact capabilities of general-purpose AI models",
     "article_patterns": [r"AIACT_ART_51", r"AIACT_ART_55"],
     "keywords": ["systemic risk", "high-impact capabilities"]},
]

ALL_CONCEPTS = GDPR_PRINCIPLES + PROCESSING_OPERATIONS + COMPLIANCE_CONCEPTS + AI_CONCEPTS


class ConceptExtractor:
    """Extract concept entities and their article links from curated lists."""

    def extract_all(
        self, articles: list[dict[str, Any]]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Extract concepts and link them to articles.

        Returns:
            (concepts, relationships) where relationships link concepts to articles.
        """
        # Build article lookup: id -> article dict
        article_map: dict[str, dict] = {}
        for art in articles:
            article_map[art["id"]] = art

        concepts: list[dict[str, Any]] = []
        relationships: list[dict[str, Any]] = []

        for concept_def in ALL_CONCEPTS:
            concept = {
                "id": concept_def["id"],
                "type": "Concept",
                "name": concept_def["name"],
                "category": concept_def["category"],
                "description": concept_def["description"],
                "keywords": concept_def["keywords"],
                "regulation_id": self._infer_regulation(concept_def),
            }

            # Find articles matching the explicit patterns
            matched_articles: list[str] = []
            for pattern in concept_def["article_patterns"]:
                for art_id in article_map:
                    if re.match(pattern + r"$", art_id):
                        matched_articles.append(art_id)

            # Also scan article text for keyword matches
            keyword_matches = self._find_keyword_matches(
                concept_def["keywords"], article_map, exclude=set(matched_articles)
            )
            matched_articles.extend(keyword_matches[:5])  # Cap at 5 keyword-based

            concept["related_articles"] = matched_articles
            concepts.append(concept)

            # Create APPLIES_TO relationships (concept -> article)
            for art_id in matched_articles:
                relationships.append({
                    "source_id": concept_def["id"],
                    "target_id": art_id,
                    "type": "APPLIES_TO",
                    "properties": {"link_method": "curated" if art_id in [
                        a for p in concept_def["article_patterns"]
                        for a in article_map if re.match(p + r"$", a)
                    ] else "keyword"},
                })

        # Create REFERENCES relationships between related concepts
        concept_cross_refs = self._build_concept_cross_refs()
        relationships.extend(concept_cross_refs)

        return concepts, relationships

    def _infer_regulation(self, concept_def: dict) -> str:
        """Infer regulation from article patterns."""
        has_gdpr = any("GDPR" in p for p in concept_def["article_patterns"])
        has_ai = any("AIACT" in p for p in concept_def["article_patterns"])
        if has_gdpr and has_ai:
            return "BOTH"
        elif has_ai:
            return "EU_AI_ACT"
        return "GDPR"

    def _find_keyword_matches(
        self, keywords: list[str], article_map: dict[str, dict],
        exclude: set[str], max_results: int = 5,
    ) -> list[str]:
        """Find articles containing concept keywords in their text."""
        matches: list[tuple[str, int]] = []

        for art_id, art in article_map.items():
            if art_id in exclude:
                continue
            text = (art.get("full_text", "") or "").lower()
            if not text:
                continue

            hit_count = 0
            for kw in keywords:
                if kw.lower() in text:
                    hit_count += 1

            if hit_count >= 1:
                matches.append((art_id, hit_count))

        matches.sort(key=lambda x: x[1], reverse=True)
        return [m[0] for m in matches[:max_results]]

    def _build_concept_cross_refs(self) -> list[dict[str, Any]]:
        """Build REFERENCES edges between related concepts."""
        cross_refs = [
            ("CONCEPT_LAWFULNESS", "CONCEPT_CONSENT"),
            ("CONCEPT_LAWFULNESS", "CONCEPT_LEGITIMATE_INTEREST"),
            ("CONCEPT_TRANSPARENCY", "CONCEPT_TRANSPARENCY_OBLIGATION"),
            ("CONCEPT_DPIA", "CONCEPT_FRIA"),
            ("CONCEPT_AUTOMATED_DECISION", "CONCEPT_HUMAN_OVERSIGHT"),
            ("CONCEPT_AUTOMATED_DECISION", "CONCEPT_PROFILING"),
            ("CONCEPT_DATA_PROTECTION_BY_DESIGN", "CONCEPT_DATA_MINIMISATION"),
            ("CONCEPT_DATA_BREACH", "CONCEPT_DATA_BREACH_NOTIFICATION"),
            ("CONCEPT_CERTIFICATION", "CONCEPT_CONFORMITY_ASSESSMENT"),
            ("CONCEPT_INTEGRITY_CONFIDENTIALITY", "CONCEPT_ROBUSTNESS"),
            ("CONCEPT_ACCURACY", "CONCEPT_DATA_GOVERNANCE"),
            ("CONCEPT_ACCOUNTABILITY", "CONCEPT_RECORDS_OF_PROCESSING"),
            ("CONCEPT_RISK_MANAGEMENT", "CONCEPT_DPIA"),
            ("CONCEPT_POST_MARKET_MONITORING", "CONCEPT_SERIOUS_INCIDENT"),
            ("CONCEPT_GPAI", "CONCEPT_SYSTEMIC_RISK"),
            ("CONCEPT_CE_MARKING", "CONCEPT_CONFORMITY_ASSESSMENT"),
        ]

        rels = []
        for src, tgt in cross_refs:
            rels.append({
                "source_id": src,
                "target_id": tgt,
                "type": "REFERENCES",
                "properties": {"link_type": "concept_cross_ref"},
            })
        return rels
