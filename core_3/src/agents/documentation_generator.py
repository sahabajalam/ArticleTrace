"""Documentation Generator Agent for compliance documents."""

import json
from datetime import datetime
from typing import Any

from src.agents.base import BaseAgent
from src.config import settings
from src.state.compliance_state import ComplianceState, ComplianceDocument


class DocumentationGeneratorAgent(BaseAgent):
    """
    Generates compliance documentation based on assessment results.

    Documents generated:
    - DPIA (Data Protection Impact Assessment) - GDPR Article 35
    - ROPA (Record of Processing Activities) - GDPR Article 30
    - Conformity Assessment - EU AI Act (High-Risk systems)
    - Transparency Notice - EU AI Act Article 52
    """

    DOCUMENT_TYPES = {
        "DPIA": {
            "full_name": "Data Protection Impact Assessment",
            "source": "GDPR Article 35",
            "required_when": ["special_category_data", "automated_decision_making", "high_risk"],
        },
        "ROPA": {
            "full_name": "Record of Processing Activities",
            "source": "GDPR Article 30",
            "required_when": ["always"],  # Required for most organizations
        },
        "CONFORMITY_ASSESSMENT": {
            "full_name": "EU AI Act Conformity Assessment",
            "source": "EU AI Act Article 43",
            "required_when": ["high_risk"],
        },
        "TRANSPARENCY_NOTICE": {
            "full_name": "AI System Transparency Notice",
            "source": "EU AI Act Article 52",
            "required_when": ["limited_risk", "user_facing"],
        },
    }

    def __init__(self):
        super().__init__(
            name="documentation_generator",
            model=settings.primary_model,  # Use best model for document generation
        )

    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Generate required compliance documents.

        Returns state update with compliance_docs.
        """
        start_time = datetime.utcnow()
        total_cost = 0.0

        risk_classification = state.get("risk_classification", {})
        gdpr_audit = state.get("gdpr_audit", {})
        legal_citations = state.get("legal_citations", {})

        # Determine which documents are required
        required_docs = self._determine_requirements(risk_classification, gdpr_audit)

        documents: list[ComplianceDocument] = []

        for doc_type in required_docs:
            doc_content, cost = await self._generate_document(
                doc_type=doc_type,
                state=state,
            )
            total_cost += cost

            if doc_content:
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                documents.append(
                    ComplianceDocument(
                        doc_type=doc_type,
                        content=doc_content,
                        filename=f"{doc_type.lower()}_{timestamp}.md",
                        format="markdown",
                    )
                )

        compliance_docs = {
            "documents": [d.model_dump() for d in documents],
            "required_docs": required_docs,
            "generated_count": len(documents),
        }

        duration = (datetime.utcnow() - start_time).total_seconds()

        self.logger.info(
            "Documentation generation complete",
            documents_generated=len(documents),
            required_docs=required_docs,
        )

        audit_update = self.build_audit_update(
            state,
            action="documentation_generation",
            output=compliance_docs,
            cost_usd=total_cost,
            duration_seconds=duration,
        )

        return {
            "compliance_docs": compliance_docs,
            "confidence_scores": {
                "documentation_generator": 0.90,
            },
            "current_step": "documentation_generated",
            **audit_update,
        }

    def _determine_requirements(
        self,
        risk_classification: dict[str, Any],
        gdpr_audit: dict[str, Any],
    ) -> list[str]:
        """Determine which documents are legally required."""
        required = []

        risk_category = risk_classification.get("category", "")

        # DPIA required conditions
        if gdpr_audit.get("dpia_required", False):
            required.append("DPIA")
        elif gdpr_audit.get("special_category_data", False):
            required.append("DPIA")
        elif risk_category in ["HIGH_RISK", "PROHIBITED"]:
            required.append("DPIA")

        # ROPA is almost always required
        required.append("ROPA")

        # Conformity Assessment for high-risk systems
        if risk_category == "HIGH_RISK":
            required.append("CONFORMITY_ASSESSMENT")

        # Transparency Notice for limited risk or user-facing
        if risk_category == "LIMITED_RISK":
            required.append("TRANSPARENCY_NOTICE")

        return list(set(required))  # Remove duplicates

    async def _generate_document(
        self,
        doc_type: str,
        state: ComplianceState,
    ) -> tuple[str, float]:
        """Generate a specific compliance document."""
        doc_info = self.DOCUMENT_TYPES.get(doc_type, {})

        if doc_type == "DPIA":
            return await self._generate_dpia(state, doc_info)
        elif doc_type == "ROPA":
            return await self._generate_ropa(state, doc_info)
        elif doc_type == "CONFORMITY_ASSESSMENT":
            return await self._generate_conformity_assessment(state, doc_info)
        elif doc_type == "TRANSPARENCY_NOTICE":
            return await self._generate_transparency_notice(state, doc_info)
        else:
            return "", 0.0

    async def _generate_dpia(
        self,
        state: ComplianceState,
        doc_info: dict[str, Any],
    ) -> tuple[str, float]:
        """Generate DPIA document."""
        system_description = state["system_description"]
        risk_classification = state.get("risk_classification", {})
        gdpr_audit = state.get("gdpr_audit", {})
        legal_citations = state.get("legal_citations", {})

        prompt = f"""Generate a complete Data Protection Impact Assessment (DPIA) pursuant to GDPR Article 35.

SYSTEM INFORMATION:
- Description: {system_description}
- System Type: {state.get('system_type', 'AI System')}
- Deployment Context: {state.get('deployment_context', 'Not specified')}
- Company: {state.get('company_name', 'Organization')}

RISK CLASSIFICATION:
{json.dumps(risk_classification, indent=2)}

GDPR AUDIT RESULTS:
{json.dumps(gdpr_audit, indent=2)}

LEGAL CITATIONS:
{json.dumps(legal_citations.get('relevant_articles', [])[:5], indent=2) if legal_citations else 'None available'}

Generate a professional DPIA document in Markdown format with the following sections:

# Data Protection Impact Assessment (DPIA)
**Pursuant to GDPR Article 35**

## 1. Description of Processing Operation
- System name and purpose
- Nature of processing
- Scope of processing
- Context of processing

## 2. Assessment of Necessity and Proportionality
- Is the processing necessary for the stated purpose?
- Is it proportionate to the aim?
- Could less intrusive alternatives achieve the same goal?

## 3. Assessment of Risks to Data Subjects
- Identified risks (from GDPR audit)
- Likelihood assessment (High/Medium/Low)
- Severity assessment (High/Medium/Low)
- Risk matrix

## 4. Measures to Address Risks
- Technical measures
- Organizational measures
- Safeguards

## 5. Consultation Requirements
- DPO consultation recommendation
- Supervisory authority consultation (if required)

## 6. Conclusion
- Overall risk assessment
- Recommendation (proceed/proceed with measures/do not proceed)

## 7. Document Metadata
- Date generated
- Assessment version
- Review schedule

Use formal legal language. Cite specific GDPR articles. Do not leave any placeholders.
Return the complete document in Markdown format."""

        response, cost = await self.invoke_llm(prompt)
        return response, cost

    async def _generate_ropa(
        self,
        state: ComplianceState,
        doc_info: dict[str, Any],
    ) -> tuple[str, float]:
        """Generate ROPA document."""
        system_description = state["system_description"]
        gdpr_audit = state.get("gdpr_audit", {})

        prompt = f"""Generate a Record of Processing Activities (ROPA) pursuant to GDPR Article 30.

SYSTEM INFORMATION:
- Description: {system_description}
- System Type: {state.get('system_type', 'AI System')}
- Company: {state.get('company_name', 'Organization')}

DATA FLOWS:
{json.dumps(gdpr_audit.get('data_flows', {}), indent=2)}

Generate a professional ROPA document in Markdown format:

# Record of Processing Activities (ROPA)
**Pursuant to GDPR Article 30**

## Processing Activity Details

| Field | Information |
|-------|-------------|
| Processing Activity Name | [Name] |
| Controller Name | [Organization] |
| Controller Contact | [Contact details] |
| DPO Contact | [If applicable] |

## Categories of Data Subjects
[List who is affected]

## Categories of Personal Data
[List data types processed]

## Purpose of Processing
[Describe purposes]

## Lawful Basis
[State lawful basis under Article 6]

## Categories of Recipients
[List who receives data]

## International Transfers
[Describe any transfers outside EEA]

## Retention Period
[State retention period or criteria]

## Technical and Organizational Measures
[Describe security measures per Article 32]

## Document Metadata
- Date Created: {datetime.utcnow().strftime('%Y-%m-%d')}
- Last Updated: {datetime.utcnow().strftime('%Y-%m-%d')}
- Version: 1.0

Return the complete document in Markdown format."""

        response, cost = await self.invoke_llm(prompt)
        return response, cost

    async def _generate_conformity_assessment(
        self,
        state: ComplianceState,
        doc_info: dict[str, Any],
    ) -> tuple[str, float]:
        """Generate EU AI Act Conformity Assessment."""
        system_description = state["system_description"]
        risk_classification = state.get("risk_classification", {})
        gdpr_audit = state.get("gdpr_audit", {})

        prompt = f"""Generate an EU AI Act Conformity Assessment document for a high-risk AI system.

SYSTEM INFORMATION:
- Description: {system_description}
- System Type: {state.get('system_type', 'AI System')}
- Risk Category: {risk_classification.get('category', 'HIGH_RISK')}
- Annex Classification: {risk_classification.get('annex', 'Annex III')}
- Subcategory: {risk_classification.get('subcategory', 'Not specified')}

REQUIREMENTS:
{json.dumps(risk_classification.get('requirements', []), indent=2)}

Generate a professional Conformity Assessment document in Markdown format:

# EU AI Act Conformity Assessment
**High-Risk AI System Assessment pursuant to EU AI Act Article 43**

## 1. System Identification
- System name and version
- Provider information
- Intended purpose
- High-risk classification justification

## 2. Requirements Assessment

### 2.1 Risk Management System (Article 9)
- Risk identification measures
- Risk mitigation measures
- Residual risk assessment

### 2.2 Data and Data Governance (Article 10)
- Training data requirements
- Data quality measures
- Bias detection and mitigation

### 2.3 Technical Documentation (Article 11)
- Documentation completeness
- Update procedures

### 2.4 Record-Keeping (Article 12)
- Logging capabilities
- Traceability measures

### 2.5 Transparency (Article 13)
- User information provisions
- Instructions for use

### 2.6 Human Oversight (Article 14)
- Human oversight measures
- Override capabilities
- Decision explanation features

### 2.7 Accuracy, Robustness, Cybersecurity (Article 15)
- Accuracy metrics
- Robustness testing
- Security measures

## 3. Conformity Declaration
- Assessment outcome
- CE marking eligibility
- Registration requirements

## 4. Document Metadata
- Assessment Date: {datetime.utcnow().strftime('%Y-%m-%d')}
- Assessor: EU AI Act Compliance Agent
- Version: 1.0
- Next Review: [12 months from assessment]

Return the complete document in Markdown format."""

        response, cost = await self.invoke_llm(prompt)
        return response, cost

    async def _generate_transparency_notice(
        self,
        state: ComplianceState,
        doc_info: dict[str, Any],
    ) -> tuple[str, float]:
        """Generate Transparency Notice for user-facing AI."""
        system_description = state["system_description"]

        prompt = f"""Generate an AI System Transparency Notice pursuant to EU AI Act Article 52.

SYSTEM INFORMATION:
- Description: {system_description}
- System Type: {state.get('system_type', 'AI System')}
- Deployment Context: {state.get('deployment_context', 'Not specified')}

Generate a clear, user-friendly transparency notice in Markdown format:

# AI System Transparency Notice
**Pursuant to EU AI Act Article 52**

## Notice to Users

This notice informs you about the use of artificial intelligence in this system.

### What This System Does
[Clear description of the AI system's function]

### How AI is Used
[Explanation of how AI assists or makes decisions]

### Your Rights
- Right to know you are interacting with AI
- Right to human review of significant decisions
- Right to explanation of AI-assisted decisions

### Contact Information
For questions about this AI system, contact:
[Organization contact details]

### Data Processing
For information about how your data is processed, please refer to our Privacy Notice.

---
*This notice is provided in compliance with EU AI Act Article 52 transparency requirements.*
*Last Updated: {datetime.utcnow().strftime('%Y-%m-%d')}*

Return the complete notice in Markdown format. Keep language simple and accessible."""

        response, cost = await self.invoke_llm(prompt)
        return response, cost
