## DATA SET 8: Compliance Case Studies (LLM-Generated)

**What I need**: 30-40 realistic compliance scenario questions with expected answers. These will be used to test the knowledge graph reasoning.

**You can generate these with an LLM.** Use this format:

```
=== CASE STUDY 1 ===
Difficulty: Medium
Scenario: A European bank wants to use an AI system to automatically reject loan applications based on credit scoring. The system uses personal financial data and produces legally binding decisions without human review.
Question: What are the combined GDPR and EU AI Act compliance requirements?

Expected Answer Summary:
- GDPR Art 22: Automated decision-making prohibition applies — must provide human intervention
- GDPR Art 35: DPIA required (automated profiling with legal effects)
- GDPR Art 6: Need lawful basis (likely Art 6(1)(b) contract or Art 6(1)(f) legitimate interest)
- AI Act Art 6 + Annex III(5)(a): Credit scoring is HIGH-RISK AI
- AI Act Art 14: Human oversight required for high-risk AI
- AI Act Art 13: Transparency and information to deployer required
- Cumulative: Both DPIA and conformity assessment needed

Expected Citations:
- GDPR Articles 6, 22, 35
- EU AI Act Articles 6, 9, 13, 14, 26
- Annex III Category 5(a)

Reasoning Path:
credit_scoring → CLASSIFIED_AS → high_risk → REQUIRES → conformity_assessment
credit_scoring → TRIGGERS → GDPR_ART_22 → HAS_EXCEPTION → contract_necessity → HAS_CONDITION → human_intervention
credit_scoring → TRIGGERS → GDPR_ART_35 → REQUIRES → dpia
```

**Categories of scenarios to cover** (3-5 each):
1. **Prohibited AI practices** — social scoring, manipulation, biometric identification
2. **High-risk AI** — hiring, credit scoring, law enforcement, healthcare
3. **Automated decision-making** — profiling, credit, insurance, hiring
4. **Data subject rights** — access, erasure, portability with AI systems
5. **International transfers** — AI models trained on EU data, cloud processing
6. **Special category data** — health AI, biometric systems, political profiling
7. **Scope questions** — does GDPR/AI Act apply? Household, military, research
8. **Cross-regulation overlap** — where both GDPR and AI Act apply simultaneously

**File name**: `compliance_case_studies.txt`