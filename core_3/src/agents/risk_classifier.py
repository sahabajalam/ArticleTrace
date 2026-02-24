"""Risk Classifier Agent for EU AI Act classification."""

import json
from datetime import datetime
from typing import Any

from src.agents.base import BaseAgent
from src.config import settings
from src.state.compliance_state import ComplianceState, RiskCategory


class RiskClassifierAgent(BaseAgent):
    """
    Classifies AI systems according to EU AI Act risk categories.

    Categories:
    - PROHIBITED (Article 5): Systems that cannot be deployed
    - HIGH_RISK (Annex III): Systems requiring conformity assessment
    - LIMITED_RISK (Article 52): Systems with transparency requirements
    - MINIMAL_RISK: Systems with no specific obligations
    """

    # EU AI Act Article 5: Prohibited AI Practices
    PROHIBITED_PATTERNS = [
        "subliminal manipulation",
        "exploit vulnerabilities based on age",
        "exploit vulnerabilities based on disability",
        "social scoring by public authorities",
        "real-time remote biometric identification in public spaces",
        "predictive policing based on individual assessment",
        "emotion recognition in workplace",
        "emotion recognition in education",
        "untargeted scraping of facial images",
        "inferring emotions of natural persons in law enforcement",
    ]

    # Annex III: High-Risk AI Systems
    HIGH_RISK_CATEGORIES = {
        "biometric_identification": {
            "description": "Biometric identification and categorisation",
            "examples": ["facial_recognition", "gait_analysis", "voice_recognition", "fingerprint_identification"],
            "annex_section": "Annex III (1)",
        },
        "critical_infrastructure": {
            "description": "Management and operation of critical infrastructure",
            "examples": ["traffic_management", "water_supply", "gas_supply", "electricity_grid"],
            "annex_section": "Annex III (2)",
        },
        "education": {
            "description": "Education and vocational training",
            "examples": ["exam_scoring", "admission_decisions", "learning_assessment", "proctoring"],
            "annex_section": "Annex III (3)",
        },
        "employment": {
            "description": "Employment, workers management and access to self-employment",
            "examples": ["cv_screening", "recruitment", "performance_evaluation", "promotion_decisions", "task_allocation", "attendance_tracking"],
            "annex_section": "Annex III (4)",
        },
        "essential_services": {
            "description": "Access to essential private and public services",
            "examples": ["credit_scoring", "insurance_pricing", "social_benefits", "emergency_services_dispatch"],
            "annex_section": "Annex III (5)",
        },
        "law_enforcement": {
            "description": "Law enforcement",
            "examples": ["crime_prediction", "evidence_evaluation", "risk_assessment", "polygraph"],
            "annex_section": "Annex III (6)",
        },
        "migration": {
            "description": "Migration, asylum and border control",
            "examples": ["visa_decision", "asylum_assessment", "border_control", "document_verification"],
            "annex_section": "Annex III (7)",
        },
        "justice": {
            "description": "Administration of justice and democratic processes",
            "examples": ["case_prioritization", "sentence_recommendation", "legal_research_for_judgments"],
            "annex_section": "Annex III (8)",
        },
    }

    def __init__(self):
        super().__init__(
            name="risk_classifier",
            model=settings.secondary_model,  # Use cheaper model for classification
        )

    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Execute risk classification.

        Returns state update with risk_classification and confidence_scores.
        """
        start_time = datetime.utcnow()

        system_description = state["system_description"]
        system_type = state["system_type"]
        deployment_context = state["deployment_context"]

        session_id = state.get("session_id")

        # Step 1: Extract capabilities using LLM
        capabilities = await self._extract_capabilities(
            system_description, system_type, deployment_context, session_id
        )

        # Step 2: Check for prohibited patterns
        prohibited_check = self._check_prohibited(capabilities)
        if prohibited_check["is_prohibited"]:
            classification = {
                "category": RiskCategory.PROHIBITED.value,
                "article": "Article 5",
                "annex": None,
                "subcategory": None,
                "reason": prohibited_check["reason"],
                "confidence": prohibited_check["confidence"],
                "requirements": [],
                "action": "DEPLOYMENT_FORBIDDEN",
            }
            return self._create_response(state, classification, start_time)

        # Step 3: Check for high-risk categories
        high_risk_check = self._check_high_risk(capabilities)
        if high_risk_check["is_high_risk"]:
            classification = {
                "category": RiskCategory.HIGH_RISK.value,
                "article": None,
                "annex": high_risk_check["annex"],
                "subcategory": high_risk_check["subcategory"],
                "reason": high_risk_check["reason"],
                "confidence": high_risk_check["confidence"],
                "requirements": [
                    "Conformity assessment required",
                    "CE marking mandatory",
                    "Registration in EU database",
                    "Human oversight required",
                    "Technical documentation required",
                    "Quality management system required",
                ],
                "action": "REQUIRES_CONFORMITY_ASSESSMENT",
            }
            return self._create_response(state, classification, start_time)

        # Step 4: Check for limited risk (transparency requirements)
        if self._is_user_facing(capabilities, deployment_context):
            classification = {
                "category": RiskCategory.LIMITED_RISK.value,
                "article": "Article 52",
                "annex": None,
                "subcategory": None,
                "reason": "System interacts directly with users and must disclose AI nature",
                "confidence": 0.85,
                "requirements": [
                    "Users must be informed they are interacting with AI",
                    "AI-generated content must be marked",
                ],
                "action": "REQUIRES_TRANSPARENCY_NOTICE",
            }
            return self._create_response(state, classification, start_time)

        # Step 5: Default to minimal risk
        classification = {
            "category": RiskCategory.MINIMAL_RISK.value,
            "article": None,
            "annex": None,
            "subcategory": None,
            "reason": "System does not fall into prohibited, high-risk, or limited-risk categories",
            "confidence": 0.80,
            "requirements": ["No specific legal obligations under EU AI Act"],
            "action": "NO_SPECIFIC_REQUIREMENTS",
        }
        return self._create_response(state, classification, start_time)

    async def _extract_capabilities(
        self,
        system_description: str,
        system_type: str,
        deployment_context: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """Extract system capabilities using LLM."""
        prompt = f"""Analyze this AI system and extract its key characteristics.

SYSTEM DESCRIPTION:
{system_description}

DECLARED SYSTEM TYPE: {system_type}
DEPLOYMENT CONTEXT: {deployment_context}

Extract and return a JSON object with:
{{
    "primary_function": "string - main purpose of the system",
    "data_types": ["list of data types processed, e.g., biometric, behavioral, personal"],
    "decision_impact": "string - what decisions does this affect (e.g., hiring, credit)",
    "deployment_context": "string - where/how is it deployed",
    "affected_persons": ["list of who is affected, e.g., employees, customers, public"],
    "is_real_time": boolean,
    "involves_biometrics": boolean,
    "involves_emotions": boolean,
    "involves_profiling": boolean,
    "involves_automated_decisions": boolean,
    "is_public_space": boolean,
    "keywords": ["list of relevant keywords for classification"]
}}

Return ONLY valid JSON, no other text."""

        response, cost = await self.invoke_llm(prompt, session_id)

        try:
            # Clean response and parse JSON
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            capabilities = json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse capabilities JSON, using defaults")
            capabilities = {
                "primary_function": system_type,
                "data_types": [],
                "decision_impact": deployment_context,
                "deployment_context": deployment_context,
                "affected_persons": [],
                "is_real_time": False,
                "involves_biometrics": "biometric" in system_description.lower() or "facial" in system_description.lower(),
                "involves_emotions": "emotion" in system_description.lower(),
                "involves_profiling": False,
                "involves_automated_decisions": True,
                "is_public_space": "public" in deployment_context.lower(),
                "keywords": [system_type],
            }

        return capabilities

    def _check_prohibited(self, capabilities: dict[str, Any]) -> dict[str, Any]:
        """Check if system falls under Article 5 prohibited practices."""
        description_lower = capabilities.get("primary_function", "").lower()
        keywords = [k.lower() for k in capabilities.get("keywords", [])]

        # Check emotion recognition in workplace/education
        if capabilities.get("involves_emotions"):
            context = capabilities.get("deployment_context", "").lower()
            if "workplace" in context or "employment" in context or "work" in context:
                return {
                    "is_prohibited": True,
                    "reason": "Emotion recognition in workplace is prohibited under Article 5(1)(f)",
                    "confidence": 0.95,
                    "pattern": "emotion recognition in workplace",
                }
            if "education" in context or "school" in context or "classroom" in context:
                return {
                    "is_prohibited": True,
                    "reason": "Emotion recognition in educational institutions is prohibited under Article 5(1)(f)",
                    "confidence": 0.95,
                    "pattern": "emotion recognition in education",
                }

        # Check real-time biometrics in public spaces
        if (
            capabilities.get("involves_biometrics")
            and capabilities.get("is_real_time")
            and capabilities.get("is_public_space")
        ):
            return {
                "is_prohibited": True,
                "reason": "Real-time remote biometric identification in publicly accessible spaces is prohibited under Article 5(1)(h)",
                "confidence": 0.92,
                "pattern": "real-time remote biometric identification in public spaces",
            }

        # Check for social scoring
        if "social scoring" in description_lower or "social credit" in description_lower:
            return {
                "is_prohibited": True,
                "reason": "Social scoring by public authorities is prohibited under Article 5(1)(c)",
                "confidence": 0.95,
                "pattern": "social scoring by public authorities",
            }

        # Check for subliminal manipulation
        if "subliminal" in description_lower or "manipulation" in description_lower:
            if "unconscious" in description_lower or "unaware" in description_lower:
                return {
                    "is_prohibited": True,
                    "reason": "Subliminal manipulation techniques are prohibited under Article 5(1)(a)",
                    "confidence": 0.88,
                    "pattern": "subliminal manipulation",
                }

        return {"is_prohibited": False, "reason": None, "confidence": 0.0, "pattern": None}

    def _check_high_risk(self, capabilities: dict[str, Any]) -> dict[str, Any]:
        """Check if system falls under Annex III high-risk categories."""
        keywords = [k.lower() for k in capabilities.get("keywords", [])]
        primary_function = capabilities.get("primary_function", "").lower()
        decision_impact = capabilities.get("decision_impact", "").lower()
        data_types = [d.lower() for d in capabilities.get("data_types", [])]

        # Check each high-risk category
        for category_id, category_info in self.HIGH_RISK_CATEGORIES.items():
            examples = [e.lower() for e in category_info["examples"]]

            # Check if any example matches
            for example in examples:
                example_words = example.replace("_", " ").split()
                if any(word in primary_function for word in example_words):
                    return {
                        "is_high_risk": True,
                        "annex": category_info["annex_section"],
                        "subcategory": category_id,
                        "reason": f"System involves {example.replace('_', ' ')}, which falls under {category_info['description']}",
                        "confidence": 0.88,
                    }

                if any(word in decision_impact for word in example_words):
                    return {
                        "is_high_risk": True,
                        "annex": category_info["annex_section"],
                        "subcategory": category_id,
                        "reason": f"System impacts {example.replace('_', ' ')} decisions, which falls under {category_info['description']}",
                        "confidence": 0.85,
                    }

            # Check keywords
            for keyword in keywords:
                if keyword in examples or any(e in keyword for e in examples):
                    return {
                        "is_high_risk": True,
                        "annex": category_info["annex_section"],
                        "subcategory": category_id,
                        "reason": f"System relates to {keyword}, categorized under {category_info['description']}",
                        "confidence": 0.82,
                    }

        # Special check for biometric data in employment
        if capabilities.get("involves_biometrics"):
            if any(ctx in capabilities.get("deployment_context", "").lower()
                   for ctx in ["employment", "hiring", "work", "employee", "attendance"]):
                return {
                    "is_high_risk": True,
                    "annex": "Annex III (4)",
                    "subcategory": "employment",
                    "reason": "Biometric identification used in employment context",
                    "confidence": 0.90,
                }

        return {
            "is_high_risk": False,
            "annex": None,
            "subcategory": None,
            "reason": None,
            "confidence": 0.0,
        }

    def _is_user_facing(self, capabilities: dict[str, Any], deployment_context: str) -> bool:
        """Check if system is user-facing (requires transparency notice)."""
        user_facing_keywords = [
            "chatbot", "assistant", "customer service", "user interaction",
            "conversational", "dialogue", "chat", "support", "help desk",
        ]

        primary_function = capabilities.get("primary_function", "").lower()
        context_lower = deployment_context.lower()

        return any(kw in primary_function or kw in context_lower for kw in user_facing_keywords)

    def _create_response(
        self,
        state: ComplianceState,
        classification: dict[str, Any],
        start_time: datetime,
    ) -> dict[str, Any]:
        """Create the response dictionary for state update."""
        duration = (datetime.utcnow() - start_time).total_seconds()

        # Determine if human review is needed
        requires_human_review = (
            classification["category"] == RiskCategory.PROHIBITED.value
            or (
                classification["category"] == RiskCategory.HIGH_RISK.value
                and classification["confidence"] < 0.80
            )
        )

        self.logger.info(
            "Risk classification complete",
            category=classification["category"],
            confidence=classification["confidence"],
            requires_human_review=requires_human_review,
        )

        return {
            "risk_classification": classification,
            "confidence_scores": {
                "risk_classifier": classification["confidence"],
            },
            "requires_human_review": requires_human_review,
            "current_step": "risk_classified",
        }
