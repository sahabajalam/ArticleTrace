"""Compliance agents for EU AI Act assessment."""

from src.agents.base import BaseAgent
from src.agents.risk_classifier import RiskClassifierAgent
from src.agents.technical_assessor import TechnicalAssessorAgent
from src.agents.legal_research import LegalResearchAgent
from src.agents.documentation_generator import DocumentationGeneratorAgent
from src.agents.supervisor import SupervisorAgent

__all__ = [
    "BaseAgent",
    "RiskClassifierAgent",
    "TechnicalAssessorAgent",
    "LegalResearchAgent",
    "DocumentationGeneratorAgent",
    "SupervisorAgent",
]
