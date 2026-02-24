"""Technical Assessor Agent for GDPR compliance audit."""

import json
from datetime import datetime
from typing import Any

from src.agents.base import BaseAgent
from src.config import settings
from src.state.compliance_state import (
    ComplianceState,
    GDPRViolation,
    GDPRWarning,
    ViolationSeverity,
)


class TechnicalAssessorAgent(BaseAgent):
    """
    GDPR Compliance Auditor Agent.

    Audits AI systems for GDPR compliance across key articles:
    - Article 5(1)(c): Data Minimization
    - Article 6: Lawful Basis
    - Article 9: Special Category Data
    - Article 22: Automated Decision-Making
    - Article 32: Data Security
    - Article 35: DPIA Requirements
    """

    GDPR_CHECKLIST = {
        "data_minimization": {
            "article": "Article 5(1)(c)",
            "title": "Data Minimization",
            "questions": [
                "Does the system collect only data necessary for its purpose?",
                "Is there a defined data retention period?",
                "Are unused data fields deleted?",
            ],
            "severity_if_violated": ViolationSeverity.MEDIUM,
        },
        "lawful_basis": {
            "article": "Article 6",
            "title": "Lawful Basis for Processing",
            "questions": [
                "What is the lawful basis for processing?",
                "If consent: Is it freely given, specific, informed, and unambiguous?",
                "If legitimate interests: Has a balancing test been performed?",
            ],
            "severity_if_violated": ViolationSeverity.HIGH,
        },
        "special_category_data": {
            "article": "Article 9",
            "title": "Special Categories of Personal Data",
            "questions": [
                "Does the system process biometric data for identification?",
                "Does the system process health data?",
                "Does the system process data revealing racial/ethnic origin?",
                "Is there an Article 9(2) exception (explicit consent, vital interests)?",
            ],
            "severity_if_violated": ViolationSeverity.CRITICAL,
        },
        "automated_decisions": {
            "article": "Article 22",
            "title": "Automated Decision-Making",
            "questions": [
                "Are decisions made solely by automated means?",
                "Do decisions produce legal or similarly significant effects?",
                "Is there meaningful human involvement in the decision process?",
                "Can individuals request human review of automated decisions?",
            ],
            "severity_if_violated": ViolationSeverity.HIGH,
        },
        "data_security": {
            "article": "Article 32",
            "title": "Security of Processing",
            "questions": [
                "Are appropriate technical measures in place?",
                "Is data encrypted at rest and in transit?",
                "Are access controls implemented?",
            ],
            "severity_if_violated": ViolationSeverity.HIGH,
        },
    }

    def __init__(self):
        super().__init__(
            name="technical_assessor",
            model=settings.primary_model,  # Use better model for complex analysis
        )

    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Execute GDPR compliance audit.

        Returns state update with gdpr_audit results.
        """
        start_time = datetime.utcnow()
        total_cost = 0.0

        system_description = state["system_description"]
        risk_classification = state.get("risk_classification", {})

        violations: list[GDPRViolation] = []
        warnings: list[GDPRWarning] = []
        recommendations: list[str] = []

        # First, analyze the data flows
        data_flows, cost = await self._analyze_data_flows(system_description)
        total_cost += cost

        # Check each GDPR requirement
        for requirement_id, requirement_info in self.GDPR_CHECKLIST.items():
            result, cost = await self._check_requirement(
                system_description=system_description,
                data_flows=data_flows,
                requirement=requirement_info,
            )
            total_cost += cost

            if result["status"] == "VIOLATION":
                violations.append(
                    GDPRViolation(
                        article=requirement_info["article"],
                        issue=result["issue"],
                        severity=requirement_info["severity_if_violated"],
                        evidence=result.get("evidence"),
                    )
                )
            elif result["status"] == "WARNING":
                warnings.append(
                    GDPRWarning(
                        article=requirement_info["article"],
                        issue=result["issue"],
                        severity=ViolationSeverity.MEDIUM,
                    )
                )

            if result.get("recommendation"):
                recommendations.append(result["recommendation"])

        # Determine special category data processing
        processes_special_category = any(
            v.article == "Article 9" for v in violations
        ) or data_flows.get("has_special_category_data", False)

        # Check if Article 22 applies
        automated_decision_making = data_flows.get("has_automated_decisions", False)

        # Identify lawful basis
        lawful_basis = await self._identify_lawful_basis(system_description, data_flows)

        # Generate recommendations based on findings
        recommendations.extend(
            self._generate_recommendations(violations, warnings, risk_classification)
        )

        # Check if DPIA is required
        dpia_required = self._is_dpia_required(
            violations=violations,
            processes_special_category=processes_special_category,
            automated_decision_making=automated_decision_making,
            risk_classification=risk_classification,
        )

        if dpia_required:
            recommendations.insert(0, "DPIA (Data Protection Impact Assessment) is REQUIRED under GDPR Article 35")

        gdpr_audit = {
            "gdpr_compliant": len(violations) == 0,
            "violations": [v.model_dump() for v in violations],
            "warnings": [w.model_dump() for w in warnings],
            "recommendations": recommendations,
            "lawful_basis": lawful_basis,
            "special_category_data": processes_special_category,
            "automated_decision_making": automated_decision_making,
            "dpia_required": dpia_required,
            "data_flows": data_flows,
        }

        duration = (datetime.utcnow() - start_time).total_seconds()

        self.logger.info(
            "GDPR audit complete",
            gdpr_compliant=gdpr_audit["gdpr_compliant"],
            violation_count=len(violations),
            warning_count=len(warnings),
            dpia_required=dpia_required,
        )

        # Build partial state update (reducers handle merge/append)
        audit_update = self.build_audit_update(
            state,
            action="gdpr_audit",
            output=gdpr_audit,
            cost_usd=total_cost,
            duration_seconds=duration,
        )

        return {
            "gdpr_audit": gdpr_audit,
            "confidence_scores": {
                "technical_assessor": 0.85 if len(violations) == 0 else 0.90,
            },
            "current_step": "gdpr_audited",
            **audit_update,
        }

    async def _analyze_data_flows(self, system_description: str) -> tuple[dict[str, Any], float]:
        """Analyze data flows in the system."""
        prompt = f"""Analyze the data flows in this AI system.

SYSTEM DESCRIPTION:
{system_description}

Extract information about:
1. What personal data is collected
2. How data flows through the system
3. Who has access to the data
4. How long data is retained
5. Whether special category data (biometric, health, etc.) is processed
6. Whether automated decisions are made

Return a JSON object:
{{
    "data_collected": ["list of data types"],
    "data_sources": ["where data comes from"],
    "data_recipients": ["who receives/accesses data"],
    "retention_period": "stated retention period or 'not specified'",
    "has_special_category_data": boolean,
    "special_category_types": ["list if applicable"],
    "has_automated_decisions": boolean,
    "automated_decision_types": ["list of decision types"],
    "data_transfers": ["any cross-border transfers"],
    "security_measures_mentioned": ["any security measures mentioned"]
}}

Return ONLY valid JSON."""

        response, cost = await self.invoke_llm(prompt)

        try:
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            data_flows = json.loads(response)
        except json.JSONDecodeError:
            data_flows = {
                "data_collected": [],
                "data_sources": [],
                "data_recipients": [],
                "retention_period": "not specified",
                "has_special_category_data": False,
                "special_category_types": [],
                "has_automated_decisions": True,
                "automated_decision_types": [],
                "data_transfers": [],
                "security_measures_mentioned": [],
            }

        return data_flows, cost

    async def _check_requirement(
        self,
        system_description: str,
        data_flows: dict[str, Any],
        requirement: dict[str, Any],
    ) -> tuple[dict[str, Any], float]:
        """Check compliance with a specific GDPR requirement."""
        questions_text = "\n".join(f"- {q}" for q in requirement["questions"])

        prompt = f"""You are a GDPR compliance auditor.

SYSTEM DESCRIPTION:
{system_description}

DATA FLOWS IDENTIFIED:
{json.dumps(data_flows, indent=2)}

Evaluate compliance with {requirement['article']} ({requirement['title']}).

Questions to consider:
{questions_text}

Based on the information provided, determine:
1. Is there a VIOLATION (clear non-compliance)?
2. Is there a WARNING (potential issue, needs attention)?
3. Is the system COMPLIANT with this requirement?

Return a JSON object:
{{
    "status": "COMPLIANT" | "WARNING" | "VIOLATION",
    "issue": "Description of the problem if any (empty string if compliant)",
    "evidence": "Quote or reference from system description supporting your finding",
    "recommendation": "What should be done to address the issue (empty if compliant)",
    "confidence": 0.0-1.0
}}

Return ONLY valid JSON."""

        response, cost = await self.invoke_llm(prompt)

        try:
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "status": "WARNING",
                "issue": "Unable to determine compliance status - manual review recommended",
                "evidence": "",
                "recommendation": "Manual review of this requirement is recommended",
                "confidence": 0.5,
            }

        return result, cost

    async def _identify_lawful_basis(
        self,
        system_description: str,
        data_flows: dict[str, Any],
    ) -> str | None:
        """Identify the lawful basis for data processing."""
        prompt = f"""Based on this AI system, identify the most likely lawful basis for processing personal data under GDPR Article 6.

SYSTEM DESCRIPTION:
{system_description}

DATA FLOWS:
{json.dumps(data_flows, indent=2)}

Lawful bases under Article 6(1):
(a) Consent
(b) Contract performance
(c) Legal obligation
(d) Vital interests
(e) Public task
(f) Legitimate interests

Return ONLY one of: "consent", "contract", "legal_obligation", "vital_interests", "public_task", "legitimate_interests", or "unclear"

Return just the single word, no other text."""

        response, cost = await self.invoke_llm(prompt)
        lawful_basis = response.strip().lower().replace('"', '').replace("'", "")

        valid_bases = ["consent", "contract", "legal_obligation", "vital_interests", "public_task", "legitimate_interests"]
        if lawful_basis in valid_bases:
            return lawful_basis
        return "unclear"

    def _is_dpia_required(
        self,
        violations: list[GDPRViolation],
        processes_special_category: bool,
        automated_decision_making: bool,
        risk_classification: dict[str, Any],
    ) -> bool:
        """Determine if DPIA is required under Article 35."""
        # DPIA required if processing special category data at scale
        if processes_special_category:
            return True

        # DPIA required if systematic automated decision-making with legal effects
        if automated_decision_making:
            return True

        # DPIA required for high-risk AI systems
        if risk_classification.get("category") in ["HIGH_RISK", "PROHIBITED"]:
            return True

        # DPIA required if critical violations found
        critical_violations = [v for v in violations if v.severity == ViolationSeverity.CRITICAL]
        if critical_violations:
            return True

        return False

    def _generate_recommendations(
        self,
        violations: list[GDPRViolation],
        warnings: list[GDPRWarning],
        risk_classification: dict[str, Any],
    ) -> list[str]:
        """Generate recommendations based on findings."""
        recommendations = []

        # Add recommendations based on violations
        for violation in violations:
            if violation.article == "Article 9":
                recommendations.append(
                    "Obtain explicit consent for processing special category data, "
                    "or document another Article 9(2) exception"
                )
            elif violation.article == "Article 22":
                recommendations.append(
                    "Implement meaningful human oversight for automated decisions "
                    "with legal or significant effects"
                )
            elif violation.article == "Article 6":
                recommendations.append(
                    "Document and validate the lawful basis for data processing"
                )

        # Add recommendations based on warnings
        if warnings:
            recommendations.append(
                "Review and address all warning items before deployment"
            )

        # Add recommendations based on risk level
        if risk_classification.get("category") == "HIGH_RISK":
            recommendations.extend([
                "Implement human oversight mechanisms as required by EU AI Act Article 14",
                "Establish technical documentation as required by EU AI Act Article 11",
                "Implement quality management system as required by EU AI Act Article 17",
            ])

        return recommendations
