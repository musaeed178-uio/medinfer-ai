# SPDX-License-Identifier: AGPL-3.0-or-later
"""Domain models — pure data, no framework imports.

These sit at the boundary between the core and presentation layers.
Both the GUI and any future CLI/API consume the same structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from kb_catalog import DiagnosisResult, humanize


@dataclass
class SymptomSelection:
    """A symptom with its severity, as the user expressed it."""

    symptom_id: str
    severity: str = "moderate"  # "mild" | "moderate" | "severe"

    @property
    def name(self) -> str:
        return humanize(self.symptom_id)


@dataclass
class DiagnosisSession:
    """The full context of one diagnosis run.

    Built by the GUI adapter from user interactions, passed into
    :meth:`DiagnosisManager.diagnose`, and returned as part of the result.
    It carries everything the core needs without referencing widgets.
    """

    symptoms: dict[str, str] = field(default_factory=dict)  # symptom_id -> severity
    patient_age: Optional[int] = None
    temperature_c: Optional[float] = None
    durations: dict[str, str] = field(default_factory=dict)
    extraction_text: Optional[str] = None  # raw NLP input, for context notes

    @property
    def symptom_ids(self) -> list[str]:
        return list(self.symptoms.keys())

    def to_selected(self) -> dict[str, str]:
        """Return the symptom→severity map expected by the controller."""
        return dict(self.symptoms)


@dataclass
class DiagnosisOutcome:
    """Everything a presentation layer needs after a diagnosis run."""

    results: list[DiagnosisResult]
    top_disease: Optional[str] = None
    top_confidence: int = 0
    explanation: str = ""
    triage_level: str = ""     # "EMERGENCY" | "URGENT" | "SELF_CARE"
    triage_title: str = ""
    triage_guidance: str = ""

    @property
    def has_results(self) -> bool:
        return bool(self.results)

    @property
    def top_result(self) -> Optional[DiagnosisResult]:
        return self.results[0] if self.results else None
