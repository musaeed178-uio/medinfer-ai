# SPDX-License-Identifier: AGPL-3.0-or-later
"""Controller bridging the GUI to the Prolog engine and the knowledge catalog.

* Knowledge content (diseases, symptoms, metadata) lives in kb_catalog.json
  and is exposed here through :class:`kb_catalog.KBCatalog`.
* Inference (candidate selection + severity-weighted confidence) runs in the
  SWI-Prolog engine over medical_kb.pl, whose facts are generated from the
  same catalog.
"""

from __future__ import annotations

from typing import Any, Optional

from pyswip import Prolog

from kb_catalog import (
    KBCatalog,
    DiagnosisResult,
    DiseaseDef,
    age_band,
    humanize,
    resource_path,
)

VALID_SEVERITIES = ("mild", "moderate", "severe")
AGE_RISK_BONUS = 5          # percentage points added when an age-band risk matches
EMERGENCY_CONFIDENCE = 50   # minimum confidence before an emergency disease is a "go now"
URGENT_TEMPERATURE_C = 39.5
URGENT_FEVER_DAYS = 3


class MedicalEngineError(RuntimeError):
    """Raised when the Prolog engine cannot be started or consulted."""


class MedicalController:
    def __init__(self, catalog: Optional[KBCatalog] = None):
        self.catalog = catalog or KBCatalog.load()
        self.prolog = Prolog()
        try:
            kb_path = resource_path("medical_kb.pl")
            self.prolog.consult(kb_path)
        except Exception as exc:  # noqa: BLE001 - surface a friendly message
            raise MedicalEngineError(
                "The AI engine (SWI-Prolog) could not start. Install SWI-Prolog "
                "from https://www.swi-prolog.org/ and make sure 'swipl' is on your PATH."
            ) from exc

    # ------------------------------------------------------------------
    # Catalog access for the GUI (no Prolog round-trips needed)
    # ------------------------------------------------------------------
    def symptoms_by_system(self) -> list[tuple[str, list[str]]]:
        """[(body system, [symptom ids])] as shown in the symptom browser."""
        return self.catalog.symptoms_by_system()

    def all_symptoms(self) -> list[str]:
        return list(self.catalog.symptoms)

    def all_diseases(self) -> list[str]:
        return list(self.catalog.diseases)

    def disease_info(self, disease_id: str) -> DiseaseDef:
        return self.catalog.diseases[disease_id]

    def search_symptoms(self, query: str) -> list[str]:
        q = query.lower().replace("_", " ")
        return [s for s in self.all_symptoms() if q in s.replace("_", " ")]

    def search_diseases(self, query: str) -> list[str]:
        q = query.lower().replace("_", " ")
        return [d for d in self.all_diseases() if q in d.replace("_", " ")]

    # ------------------------------------------------------------------
    # Diagnosis
    # ------------------------------------------------------------------
    def diagnose(
        self,
        selected: dict[str, str],
        age: Optional[int] = None,
    ) -> list[DiagnosisResult]:
        """Run the Prolog engine over the selected symptom->severity map.

        ``selected`` maps a symptom id to "mild" | "moderate" | "severe".
        Returns candidates ranked by confidence (age-risk adjusted, capped
        at 100).
        """
        if not selected:
            return []

        self.prolog.retractall("patient_has(_)")
        self.prolog.retractall("patient_sev(_, _)")
        for symptom, severity in selected.items():
            sev = severity.lower() if severity.lower() in VALID_SEVERITIES else "moderate"
            self.prolog.assertz(f"patient_has({symptom})")
            self.prolog.assertz(f"patient_sev({symptom}, {sev})")

        candidates = [str(r["D"]) for r in self.prolog.query("possible_disease(D)")]
        band = age_band(age)

        results: list[DiagnosisResult] = []
        for disease_id in candidates:
            defn = self.catalog.diseases.get(disease_id)
            if defn is None:
                continue  # catalog is authoritative; never query content prolog lacks
            confidence = self._query_int(f"confidence({disease_id}, C)")
            matched = self._query_int(f"matched_symptoms({disease_id}, M)")
            total = self._query_int(f"total_symptoms({disease_id}, T)")

            risk_note: Optional[str] = None
            base_confidence = confidence
            if band and band in defn.age_risk_bands():
                risk_note = (
                    f"Age {age} ({band}): elevated risk for {defn.name}; "
                    f"confidence adjusted +{AGE_RISK_BONUS}%"
                )
                confidence = min(100, base_confidence + AGE_RISK_BONUS)

            results.append(DiagnosisResult(
                disease=disease_id,
                confidence=confidence,
                base_confidence=base_confidence,
                matched=matched,
                total=total,
                category=defn.category,
                emergency=defn.emergency,
                risk_note=risk_note,
            ))

        results.sort(key=lambda r: (-r.confidence, -r.matched))
        return results

    # ------------------------------------------------------------------
    # Triage guidance ("what to do next")
    # ------------------------------------------------------------------
    def triage(
        self,
        results: list[DiagnosisResult],
        selected: dict[str, str],
        temperature_c: Optional[float] = None,
        durations: Optional[dict[str, str]] = None,
    ) -> tuple[str, str, str]:
        """Return (level, title, guidance) with level in {"EMERGENCY", "URGENT", "SELF_CARE"}."""
        durations = durations or {}
        selected_red_flags = self.catalog.red_flag_symptoms() & set(selected)

        if not results:
            return "SELF_CARE", "Self-care", (
                "No likely condition matched your symptoms. Rest, monitor how you feel, "
                "and re-run the diagnosis if new symptoms appear or symptoms worsen."
            )

        top = results[0]

        # Fever thresholds worth surfacing regardless of the top diagnosis.
        fever_days = self._duration_days(durations.get("fever"))
        high_temperature = temperature_c is not None and temperature_c >= URGENT_TEMPERATURE_C

        if top.emergency and top.confidence >= EMERGENCY_CONFIDENCE:
            return "EMERGENCY", "Seek emergency care now", (
                f"{top.name} is a potentially serious condition and your symptom "
                f"pattern fits it strongly ({top.confidence}%). If breathing is "
                "difficult, symptoms are worsening, or you feel confused, go to the "
                "nearest emergency department or call your local emergency number."
            )

        if selected_red_flags:
            names = ", ".join(humanize(s) for s in sorted(selected_red_flags))
            return "URGENT", "See a clinician within 24 hours", (
                f"You reported a red-flag symptom ({names}). These can indicate a "
                "serious condition even when the top match looks mild. Please contact "
                "a doctor or urgent-care clinic today."
            )

        if top.emergency:
            return "URGENT", "See a clinician today", (
                f"{top.name} can be serious ({top.confidence}% match). Even if you "
                "feel okay right now, arrange to see a clinician promptly."
            )

        if high_temperature or (fever_days is not None and fever_days >= URGENT_FEVER_DAYS):
            detail = (
                f"Your temperature is {temperature_c:.1f} °C." if high_temperature
                else f"Your fever has lasted {fever_days:.0f} day(s)."
            )
            return "URGENT", "Check in with a clinician", (
                f"{detail} A prolonged or very high fever deserves medical review. "
                "Please contact a doctor if it does not improve with rest and fluids."
            )

        return "SELF_CARE", "Self-care and monitoring", (
            "Your symptoms most closely match a mild, self-limiting condition. Rest, "
            "stay hydrated, and monitor yourself. If symptoms persist beyond a few "
            "days, worsen, or new red-flag symptoms appear, see a clinician."
        )

    # ------------------------------------------------------------------
    # Explanation text (single implementation shared by GUI + exports)
    # ------------------------------------------------------------------
    def build_explanation(
        self,
        disease_id: str,
        selected: dict[str, str],
        extraction: Optional[Any] = None,
    ) -> str:
        defn = self.catalog.diseases[disease_id]
        selected_ids = set(selected)
        matched = [s for s in defn.symptoms if s in selected_ids]
        missing = [s for s in defn.symptoms if s not in selected_ids]

        lines: list[str] = []
        lines.append(f"AI Analysis: {defn.name}")
        lines.append("")
        lines.append(
            f"This is a {defn.category} condition. The engine matched {len(matched)} of "
            f"{len(defn.symptoms)} typical indicators for {defn.name}, so it ranks as "
            "the most probable candidate given what you reported."
        )
        if matched:
            sev = ", ".join(f"{humanize(s)} ({selected[s].title()})" for s in matched)
            lines.append("")
            lines.append(f"Matched symptoms: {sev}")
        if missing:
            lines.append("")
            lines.append(f"Missing indicators: {', '.join(humanize(s) for s in missing[:4])}")
        if extraction is not None:
            notes = self._context_notes(extraction)
            if notes:
                lines.append("")
                lines.extend(notes)
        lines.append("")
        lines.append(f"Recommendation: {defn.recommendation}")
        lines.append("")
        lines.append(
            "Disclaimer: this analysis is for educational purposes only and is not a "
            "medical diagnosis. Always consult a qualified healthcare provider."
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Small helpers
    # ------------------------------------------------------------------
    def _context_notes(self, extraction: Any) -> list[str]:
        notes: list[str] = []
        sev = getattr(extraction, "severities", {})
        high_sev = [humanize(s) for s, level in sev.items() if level == "severe"]
        if high_sev:
            notes.append(f"Severe symptoms noted: {', '.join(high_sev)}.")
        if getattr(extraction, "durations", None):
            dur = ", ".join(
                f"{humanize(s)} for {d}" for s, d in extraction.durations.items()
            )
            notes.append(f"Duration: {dur}.")
        temp = getattr(extraction, "temperature_c", None)
        if temp is not None:
            notes.append(f"Reported temperature: {temp:.1f} °C.")
        return notes

    @staticmethod
    def _duration_days(label: Optional[str]) -> Optional[float]:
        """Best-effort '3 day' -> 3.0 from a duration label."""
        if not label:
            return None
        import re
        m = re.search(r"(\d+(?:\.\d+)?)\s*(\w+)", label)
        if not m:
            return None
        value, unit = float(m.group(1)), m.group(2).rstrip("s")
        if unit == "day":
            return value
        if unit == "week":
            return value * 7
        if unit == "hour":
            return value / 24.0
        if unit == "month":
            return value * 30.0
        return None

    def _query_int(self, goal: str) -> int:
        for row in self.prolog.query(goal):
            for value in row.values():
                try:
                    return int(value)
                except (TypeError, ValueError):
                    continue
        return 0

    def cleanup(self) -> None:
        self.prolog.retractall("patient_has(_)")
        self.prolog.retractall("patient_sev(_, _)")
