"""Rule-based extraction for actors, data types, risk categories, penalties, AI system types.

These entities are fully deterministic — defined in specific articles with known structures.
No LLM needed.
"""

from __future__ import annotations

from typing import Any


class RuleBasedExtractor:
    """Extract structured entities from known article locations."""

    def extract_actors(self) -> list[dict[str, Any]]:
        """Extract actor entities from GDPR and AI Act definitions."""
        actors = [
            # GDPR actors (from Art 4)
            {"id": "ACTOR_CONTROLLER", "name": "Controller", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Natural or legal person which determines the purposes and means of processing"},
            {"id": "ACTOR_PROCESSOR", "name": "Processor", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Natural or legal person which processes personal data on behalf of the controller"},
            {"id": "ACTOR_DATA_SUBJECT", "name": "Data Subject", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Identified or identifiable natural person"},
            {"id": "ACTOR_DPO", "name": "Data Protection Officer", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_37", "description": "Designated officer overseeing data protection compliance"},
            {"id": "ACTOR_SUPERVISORY_AUTHORITY", "name": "Supervisory Authority", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Independent public authority established by a Member State"},
            {"id": "ACTOR_RECIPIENT", "name": "Recipient", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Natural or legal person to which personal data are disclosed"},
            {"id": "ACTOR_THIRD_PARTY", "name": "Third Party", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Person other than data subject, controller, processor, or authorized persons"},
            {"id": "ACTOR_REPRESENTATIVE", "name": "Representative", "regulation_id": "GDPR",
             "definition_article": "GDPR_ART_4", "description": "Person designated to represent controller/processor in EU"},
            # AI Act actors (from Art 3)
            {"id": "ACTOR_PROVIDER", "name": "Provider", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person that develops an AI system or has one developed and places it on the market"},
            {"id": "ACTOR_DEPLOYER", "name": "Deployer", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person using an AI system under its authority"},
            {"id": "ACTOR_IMPORTER", "name": "Importer", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person located in EU placing AI system from third country on market"},
            {"id": "ACTOR_DISTRIBUTOR", "name": "Distributor", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person in supply chain making AI system available, other than provider/importer"},
            {"id": "ACTOR_PRODUCT_MANUFACTURER", "name": "Product Manufacturer", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Manufacturer placing AI system with their product under their name"},
            {"id": "ACTOR_AUTHORISED_REP", "name": "Authorised Representative", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person in EU with written mandate from provider"},
            {"id": "ACTOR_NOTIFIED_BODY", "name": "Notified Body", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Conformity assessment body designated under AI Act"},
            {"id": "ACTOR_MARKET_SURVEILLANCE", "name": "Market Surveillance Authority", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "National authority carrying out market surveillance"},
            {"id": "ACTOR_AI_OFFICE", "name": "AI Office", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_64", "description": "Commission body supporting AI Act implementation"},
            {"id": "ACTOR_AFFECTED_PERSON", "name": "Affected Person", "regulation_id": "EU_AI_ACT",
             "definition_article": "AIACT_ART_3", "description": "Person subject to or affected by an AI system"},
        ]
        for a in actors:
            a["type"] = "Actor"
            a.setdefault("responsibilities", [])
        return actors

    def extract_data_types(self) -> list[dict[str, Any]]:
        """Extract data type hierarchy from GDPR Art 4 + Art 9."""
        data_types = [
            # Root
            {"id": "DT_PERSONAL_DATA", "name": "Personal Data", "parent_type": None,
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "Any information relating to an identified or identifiable natural person"},
            # Special categories (Art 9)
            {"id": "DT_BIOMETRIC", "name": "Biometric Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_4", "GDPR_ART_9"], "description": "Data from specific technical processing of physical/physiological/behavioural characteristics"},
            {"id": "DT_HEALTH", "name": "Health Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_4", "GDPR_ART_9"], "description": "Data related to physical or mental health"},
            {"id": "DT_GENETIC", "name": "Genetic Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_4", "GDPR_ART_9"], "description": "Data relating to inherited or acquired genetic characteristics"},
            {"id": "DT_RACIAL_ETHNIC", "name": "Racial/Ethnic Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_9"], "description": "Data revealing racial or ethnic origin"},
            {"id": "DT_POLITICAL", "name": "Political Opinions", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_9"], "description": "Data revealing political opinions"},
            {"id": "DT_RELIGIOUS", "name": "Religious/Philosophical Beliefs", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_9"], "description": "Data revealing religious or philosophical beliefs"},
            {"id": "DT_TRADE_UNION", "name": "Trade Union Membership", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_9"], "description": "Data revealing trade union membership"},
            {"id": "DT_SEXUAL_ORIENTATION", "name": "Sexual Orientation", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": True, "regulated_by": ["GDPR_ART_9"], "description": "Data concerning sex life or sexual orientation"},
            {"id": "DT_CRIMINAL", "name": "Criminal Conviction Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_10"], "description": "Data relating to criminal convictions and offences (Art 10 separate regime)"},
            # Pseudonymised — still personal data per Recital 26 + Art 4(5)
            {"id": "DT_PSEUDONYMISED", "name": "Pseudonymised Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "Personal data processed so it cannot be attributed without additional information. STILL personal data under GDPR."},
            # Regular personal data subtypes
            {"id": "DT_LOCATION", "name": "Location Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "Data about physical location of a person"},
            {"id": "DT_ONLINE_IDENTIFIER", "name": "Online Identifiers", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "IP addresses, cookie identifiers, device fingerprints"},
            {"id": "DT_FINANCIAL", "name": "Financial Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "Bank account, transaction, credit data"},
            {"id": "DT_BEHAVIOURAL", "name": "Behavioural Data", "parent_type": "DT_PERSONAL_DATA",
             "is_special_category": False, "regulated_by": ["GDPR_ART_4"], "description": "Data used for profiling: browsing, purchase patterns"},
            # Non-personal
            {"id": "DT_ANONYMISED", "name": "Anonymised Data", "parent_type": None,
             "is_special_category": False, "regulated_by": [], "description": "Truly anonymous data — GDPR does not apply (Recital 26)"},
            {"id": "DT_AGGREGATED", "name": "Aggregated Data", "parent_type": None,
             "is_special_category": False, "regulated_by": [], "description": "Irreversibly aggregated data — non-personal only if re-identification impossible"},
        ]
        for dt in data_types:
            dt["type"] = "DataType"
        return data_types

    def extract_risk_categories(self) -> list[dict[str, Any]]:
        """Extract AI Act risk classification from Art 5, Art 6, Annex III, Art 50."""
        categories = [
            {"id": "RISK_PROHIBITED", "name": "Prohibited AI Practices", "risk_level": "PROHIBITED",
             "source_article": "AIACT_ART_5", "description": "AI practices banned outright under Art 5"},
            {"id": "RISK_HIGH", "name": "High-Risk AI Systems", "risk_level": "HIGH_RISK",
             "source_article": "AIACT_ART_6", "annex_reference": "AIACT_ANNEX_III",
             "description": "AI systems classified as high-risk under Art 6 + Annex III"},
            {"id": "RISK_LIMITED", "name": "Limited Risk AI Systems", "risk_level": "LIMITED_RISK",
             "source_article": "AIACT_ART_50", "description": "AI systems with transparency obligations under Art 50"},
            {"id": "RISK_MINIMAL", "name": "Minimal Risk AI Systems", "risk_level": "MINIMAL_RISK",
             "source_article": None, "description": "All other AI systems — no specific obligations"},
        ]
        for rc in categories:
            rc["type"] = "RiskCategory"
        return categories

    def extract_ai_system_types(self) -> list[dict[str, Any]]:
        """Extract AI system types from Art 5 (prohibited) + Annex III (high-risk) + Art 50 (limited)."""
        system_types = [
            # Prohibited (Art 5)
            {"id": "AIST_SUBLIMINAL_MANIPULATION", "name": "Subliminal Manipulation", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "AI deploying subliminal techniques to distort behaviour"},
            {"id": "AIST_VULNERABILITY_EXPLOITATION", "name": "Vulnerability Exploitation", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "AI exploiting vulnerabilities of age, disability, social/economic situation"},
            {"id": "AIST_SOCIAL_SCORING_PUBLIC", "name": "Social Scoring (Public Authority)", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Social scoring by public authorities leading to detrimental treatment"},
            {"id": "AIST_REALTIME_BIOMETRIC_PUBLIC", "name": "Real-time Biometric in Public Spaces", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Real-time remote biometric identification in publicly accessible spaces for law enforcement"},
            {"id": "AIST_EMOTION_RECOGNITION_WORK", "name": "Emotion Recognition (Workplace)", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Emotion recognition in workplace except for medical/safety reasons"},
            {"id": "AIST_EMOTION_RECOGNITION_EDU", "name": "Emotion Recognition (Education)", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Emotion recognition in educational institutions except for medical/safety reasons"},
            {"id": "AIST_UNTARGETED_FACIAL_SCRAPING", "name": "Untargeted Facial Image Scraping", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Untargeted scraping of facial images from internet/CCTV for facial recognition databases"},
            {"id": "AIST_BIOMETRIC_CATEGORISATION", "name": "Biometric Categorisation (Sensitive)", "risk_category": "RISK_PROHIBITED",
             "source_article": "AIACT_ART_5", "use_case_area": "Prohibited", "description": "Biometric categorisation inferring race, political opinions, religious beliefs, sexual orientation"},
            # High-Risk Annex III areas
            {"id": "AIST_BIOMETRIC_ID", "name": "Biometric Identification", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 1", "description": "Remote biometric identification systems"},
            {"id": "AIST_CRITICAL_INFRASTRUCTURE", "name": "Critical Infrastructure Management", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 2", "description": "AI as safety component of critical infrastructure"},
            {"id": "AIST_EDUCATION_ASSESSMENT", "name": "Education/Vocational Assessment", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 3", "description": "AI determining access to education or evaluating students"},
            {"id": "AIST_EMPLOYMENT", "name": "Employment/Workers Management", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 4", "description": "AI for recruitment, promotion, termination, task allocation, performance monitoring"},
            {"id": "AIST_ESSENTIAL_SERVICES", "name": "Essential Services Access", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 5", "description": "AI for credit scoring, insurance, emergency services, benefits eligibility"},
            {"id": "AIST_LAW_ENFORCEMENT", "name": "Law Enforcement", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 6", "description": "AI for risk assessment, polygraphs, evidence evaluation, crime prediction, profiling"},
            {"id": "AIST_MIGRATION_BORDER", "name": "Migration/Border Control", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 7", "description": "AI for risk assessment in migration, visa, asylum, border control"},
            {"id": "AIST_JUSTICE_DEMOCRACY", "name": "Justice/Democratic Processes", "risk_category": "RISK_HIGH",
             "annex_reference": "AIACT_ANNEX_III", "use_case_area": "Annex III Area 8", "description": "AI assisting judicial authorities in fact-finding, law application, dispute resolution"},
            # Limited Risk (Art 50)
            {"id": "AIST_CHATBOT", "name": "Chatbot/Conversational AI", "risk_category": "RISK_LIMITED",
             "source_article": "AIACT_ART_50", "use_case_area": "Transparency", "description": "AI system interacting with natural persons (must disclose AI nature)"},
            {"id": "AIST_DEEPFAKE", "name": "Deepfake Generation", "risk_category": "RISK_LIMITED",
             "source_article": "AIACT_ART_50", "use_case_area": "Transparency", "description": "AI generating synthetic audio, image, video content"},
            {"id": "AIST_AI_GENERATED_CONTENT", "name": "AI-Generated Content", "risk_category": "RISK_LIMITED",
             "source_article": "AIACT_ART_50", "use_case_area": "Transparency", "description": "AI-generated text on matters of public interest"},
        ]
        for ast in system_types:
            ast["type"] = "AISystemType"
        return system_types

    def extract_penalties(self) -> list[dict[str, Any]]:
        """Extract penalty tiers from GDPR Art 83 and AI Act Art 99."""
        penalties = [
            {"id": "PEN_GDPR_TIER1", "name": "GDPR Tier 1 Fine", "regulation_id": "GDPR",
             "source_article": "GDPR_ART_83", "max_fine_eur": 10000000, "max_fine_turnover_pct": 2.0,
             "tier": "Tier 1", "applies_to_articles": ["GDPR_ART_8", "GDPR_ART_11", "GDPR_ART_25", "GDPR_ART_26", "GDPR_ART_27", "GDPR_ART_28", "GDPR_ART_29", "GDPR_ART_30", "GDPR_ART_31", "GDPR_ART_32", "GDPR_ART_33", "GDPR_ART_34", "GDPR_ART_35", "GDPR_ART_36", "GDPR_ART_37", "GDPR_ART_38", "GDPR_ART_39", "GDPR_ART_42", "GDPR_ART_43"],
             "description": "Up to EUR 10M or 2% global turnover for Art 83(4) violations"},
            {"id": "PEN_GDPR_TIER2", "name": "GDPR Tier 2 Fine", "regulation_id": "GDPR",
             "source_article": "GDPR_ART_83", "max_fine_eur": 20000000, "max_fine_turnover_pct": 4.0,
             "tier": "Tier 2", "applies_to_articles": ["GDPR_ART_5", "GDPR_ART_6", "GDPR_ART_7", "GDPR_ART_9", "GDPR_ART_12", "GDPR_ART_13", "GDPR_ART_14", "GDPR_ART_15", "GDPR_ART_16", "GDPR_ART_17", "GDPR_ART_18", "GDPR_ART_19", "GDPR_ART_20", "GDPR_ART_21", "GDPR_ART_22", "GDPR_ART_44", "GDPR_ART_45", "GDPR_ART_46", "GDPR_ART_47", "GDPR_ART_48", "GDPR_ART_49"],
             "description": "Up to EUR 20M or 4% global turnover for Art 83(5) violations"},
            {"id": "PEN_GDPR_TIER3", "name": "GDPR Tier 3 Fine", "regulation_id": "GDPR",
             "source_article": "GDPR_ART_83", "max_fine_eur": 20000000, "max_fine_turnover_pct": 4.0,
             "tier": "Tier 3", "applies_to_articles": [],
             "description": "Up to EUR 20M or 4% global turnover for non-compliance with DPA order"},
            {"id": "PEN_AIACT_PROHIBITED", "name": "AI Act Prohibited AI Fine", "regulation_id": "EU_AI_ACT",
             "source_article": "AIACT_ART_99", "max_fine_eur": 35000000, "max_fine_turnover_pct": 7.0,
             "tier": "Prohibited", "applies_to_articles": ["AIACT_ART_5"],
             "description": "Up to EUR 35M or 7% global turnover for prohibited AI practices"},
            {"id": "PEN_AIACT_HIGH_RISK", "name": "AI Act High-Risk Non-Compliance Fine", "regulation_id": "EU_AI_ACT",
             "source_article": "AIACT_ART_99", "max_fine_eur": 15000000, "max_fine_turnover_pct": 3.0,
             "tier": "High-Risk", "applies_to_articles": ["AIACT_ART_6", "AIACT_ART_9", "AIACT_ART_10", "AIACT_ART_11", "AIACT_ART_12", "AIACT_ART_13", "AIACT_ART_14", "AIACT_ART_15", "AIACT_ART_43"],
             "description": "Up to EUR 15M or 3% global turnover for high-risk AI non-compliance"},
            {"id": "PEN_AIACT_INFO", "name": "AI Act Information Provision Fine", "regulation_id": "EU_AI_ACT",
             "source_article": "AIACT_ART_99", "max_fine_eur": 7500000, "max_fine_turnover_pct": 1.0,
             "tier": "Information", "applies_to_articles": [],
             "description": "Up to EUR 7.5M or 1% global turnover for incorrect information to authorities"},
        ]
        for p in penalties:
            p["type"] = "Penalty"
        return penalties
