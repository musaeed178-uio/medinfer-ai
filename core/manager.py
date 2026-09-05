# SPDX-License-Identifier: AGPL-3.0-or-later
"""DiagnosisManager — the primary domain service.

Orchestrates the diagnosis workflow: text analysis → symptom extraction →
engine diagnosis → triage → explanation.  Presentation layers call its
methods and receive plain data; they never touch the Prolog engine or
the knowledge catalog directly.

All dependencies are injected via the constructor — the composition root
(:func:`bootstrap.create_manager`) is the only place that builds one.
"""

from __future__ import annotations

from typing import Any, Optional

from controller import MedicalController
from kb_catalog import DiagnosisResult, KBCatalog, humanize
from patient_profile import PatientProfile
from report_exporter import ReportExporter
from symptom_extractor import ExtractionResult, SymptomExtractor

from core.models import DiagnosisOutcome, DiagnosisSession


class DiagnosisManager:
    """Domain service: the single entry point for all diagnosis operations.

    Presentation layers never instantiate :class:`MedicalController`,
    :class:`SymptomExtractor`, etc. directly — they receive a fully-wired
    ``DiagnosisManager`` from the composition root.
    """

    def __init__(
        self,
        controller: MedicalController,
        patient: PatientProfile,
        exporter: ReportExporter,
    ) -> None:
        self._controller = controller
        self._patient = patient
        self._exporter = exporter
        self._extractor = SymptomExtractor(controller.catalog)

    # ── Read-only accessors (presentation layers need these) ──────────

    @property
    def catalog(self) -> KBCatalog:
        return self._controller.catalog

    @property
    def patient(self) -> PatientProfile:
        return self._patient

    @property
    def exporter(self) -> ReportExporter:
        return self._exporter

    def symptoms_by_system(self) -> list[tuple[str, list[str]]]:
        """[(body_system, [symptom_id, ...]), ...] for the symptom browser."""
        return self._controller.symptoms_by_system()

    def all_diseases(self) -> list[str]:
        return self._controller.all_diseases()

    def disease_info(self, disease_id: str):
        return self._controller.disease_info(disease_id)

    # ── Text analysis ─────────────────────────────────────────────────

    def analyze_text(self, text: str) -> ExtractionResult:
        """Parse free text into structured symptom data."""
        return self._extractor.extract(text)

    # ── Diagnosis ─────────────────────────────────────────────────────

    def diagnose(self, session: DiagnosisSession) -> DiagnosisOutcome:
        """Run the full diagnosis pipeline and return a structured outcome.

        This is the main entry point the GUI calls after the user clicks
        "Run Diagnosis".  It blocks (runs the Prolog engine synchronously);
        the GUI adapter should call it from a background thread.
        """
        if not session.symptoms:
            return DiagnosisOutcome(results=[])

        # 1) Run the Prolog engine
        results = self._controller.diagnose(
            session.to_selected(),
            age=session.patient_age,
        )

        if not results:
            return DiagnosisOutcome(results=[])

        top = results[0]

        # 2) Build explanation text
        extraction = self._build_extraction_proxy(session)
        explanation = self._controller.build_explanation(
            top.disease, session.to_selected(), extraction,
        )

        # 3) Triage
        level, title, guidance = self._controller.triage(
            results,
            session.to_selected(),
            temperature_c=session.temperature_c,
            durations=session.durations or None,
        )

        # 4) Persist to history
        extras: dict[str, Any] = {}
        if session.symptoms:
            extras["severities"] = dict(session.symptoms)
        if session.temperature_c is not None:
            extras["temperature_c"] = session.temperature_c
        if session.durations:
            extras["durations"] = dict(session.durations)
        self._patient.add_diagnosis(
            session.symptom_ids,
            [r.as_dict() for r in results],
            top.disease,
            top.confidence,
            extras or None,
        )

        return DiagnosisOutcome(
            results=results,
            top_disease=top.disease,
            top_confidence=top.confidence,
            explanation=explanation,
            triage_level=level,
            triage_title=title,
            triage_guidance=guidance,
        )

    # ── Export ────────────────────────────────────────────────────────

    def export_report(
        self,
        fmt: str,
        session: DiagnosisSession,
        outcome: DiagnosisOutcome,
    ) -> Optional[str]:
        """Export a diagnosis report. Returns the file path or None."""
        if not outcome.has_results:
            return None
        top = outcome.top_result
        defn = self._controller.disease_info(top.disease)
        info = {
            "name": defn.name,
            "category": defn.category,
            "description": defn.description,
            "recommendation": defn.recommendation,
            "is_emergency": defn.emergency,
        }
        return self._exporter.export(
            fmt,
            self._patient.get_current_profile(),
            session.to_selected(),
            [r.as_dict() for r in outcome.results],
            outcome.explanation,
            info,
            self._extras_from_session(session) or None,
        )

    # ── Private helpers ───────────────────────────────────────────────

    @staticmethod
    def _build_extraction_proxy(session: DiagnosisSession):
        """Build a minimal ExtractionResult from session data for context notes.

        The controller's ``build_explanation`` reads ``temperature_c`` and
        ``durations`` from the extraction object; we synthesize one from the
        session so the core never needs to re-parse.
        """
        ext = ExtractionResult(
            symptom_ids=session.symptom_ids,
            severities=dict(session.symptoms),
            durations=dict(session.durations),
            temperature_c=session.temperature_c,
        )
        return ext

    @staticmethod
    def _extras_from_session(session: DiagnosisSession) -> dict[str, Any]:
        extras: dict[str, Any] = {}
        if session.symptoms:
            extras["severities"] = dict(session.symptoms)
        if session.temperature_c is not None:
            extras["temperature_c"] = session.temperature_c
        if session.durations:
            extras["durations"] = dict(session.durations)
        return extras
