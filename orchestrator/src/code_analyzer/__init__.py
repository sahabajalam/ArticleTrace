"""Static compliance scanner for AI codebases.

Phase 1: scans a cloned repo for patterns that trigger EU AI Act / GDPR
obligations, emits findings with file:line anchors, aggregates into an
AISystemProfile that downstream agents consume.
"""

from src.code_analyzer.models import (
    Severity,
    Finding,
    Evidence,
    AIComponent,
    DecisionSurface,
    DataSignals,
    RepoInfo,
    AISystemProfile,
)
from src.code_analyzer.scan import run_scan

__all__ = [
    "Severity",
    "Finding",
    "Evidence",
    "AIComponent",
    "DecisionSurface",
    "DataSignals",
    "RepoInfo",
    "AISystemProfile",
    "run_scan",
]
