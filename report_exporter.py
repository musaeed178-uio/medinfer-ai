# SPDX-License-Identifier: AGPL-3.0-or-later
"""Export diagnosis reports to plain text or PDF.

Both formats share one content builder (``_build_lines``) so the wording
never drifts between output types. ``reportlab`` is imported lazily - if it
is missing, PDF export raises a helpful error instead of breaking the rest
of the application.
"""

from __future__ import annotations

import os
from datetime import datetime
from tkinter import filedialog
from typing import Any, Optional

from kb_catalog import humanize


class ReportExporter:
    """Create printable diagnosis / history reports."""

    def __init__(self) -> None:
        pass

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------
    def export(
        self,
        kind: str,
        patient_info: dict[str, Any],
        selected: dict[str, str],
        results: list[dict[str, Any]],
        explanation: str,
        disease_info: dict[str, Any],
        extras: Optional[dict[str, Any]] = None,
        save_path: Optional[str] = None,
    ) -> Optional[str]:
        """Export a report; returns the path written or None when cancelled.

        ``kind`` is "txt" or "pdf". ``selected`` maps symptom id -> severity,
        ``results`` are DiagnosisResult.as_dict() dicts, ``disease_info`` the
        details of the top result, and ``extras`` may carry temperature and
        duration context captured from free text.
        """
        if kind not in ("txt", "pdf"):
            raise ValueError(f"Unsupported report kind: {kind!r}")

        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        extension = ".pdf" if kind == "pdf" else ".txt"
        if save_path is None:
            save_path = filedialog.asksaveasfilename(
                defaultextension=extension,
                filetypes=[(f"{kind.upper()} files", f"*{extension}"), ("All files", "*.*")],
                initialfile=f"diagnosis_report_{stamp}{extension}",
            )
        if not save_path:
            return None

        lines = self._build_lines(patient_info, selected, results, explanation,
                                  disease_info, extras or {})
        if kind == "txt":
            with open(save_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        else:
            self._write_pdf(save_path, lines)
        return save_path

    def export_history_txt(
        self,
        history: list[dict[str, Any]],
        patient_info: dict[str, Any],
        save_path: Optional[str] = None,
    ) -> Optional[str]:
        if save_path is None:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"diagnosis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            )
        if not save_path:
            return None

        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("       DIAGNOSIS HISTORY REPORT")
        lines.append("=" * 60)
        lines.append(f"Patient: {patient_info.get('name', 'N/A')}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Records: {len(history)}")
        lines.append("")
        for i, entry in enumerate(history, 1):
            ts = entry.get("timestamp", "N/A")
            try:
                ts = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError):
                pass
            lines.append(f"--- Record #{i} ---")
            lines.append(f"Date: {ts}")
            lines.append(f"Symptoms: {', '.join(humanize(s) for s in entry.get('symptoms', []))}")
            lines.append(f"Top Diagnosis: {humanize(entry.get('top_disease', 'N/A'))}")
            lines.append(f"Confidence: {entry.get('confidence', 0)}%")
            temp = entry.get("temperature_c")
            if temp is not None:
                lines.append(f"Temperature: {float(temp):.1f} C")
            lines.append("")

        with open(save_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return save_path

    # ------------------------------------------------------------------
    # Shared content builder
    # ------------------------------------------------------------------
    def _build_lines(
        self,
        patient_info: dict[str, Any],
        selected: dict[str, str],
        results: list[dict[str, Any]],
        explanation: str,
        disease_info: dict[str, Any],
        extras: dict[str, Any],
    ) -> list[str]:
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("       MEDICAL DIAGNOSIS REPORT")
        lines.append("       AI-Based Medical Diagnosis Expert System")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        lines.append("-" * 60)
        lines.append("PATIENT INFORMATION")
        lines.append("-" * 60)
        lines.append(f"Name: {patient_info.get('name', 'N/A')}")
        lines.append(f"Age: {patient_info.get('age', 'N/A')}")
        lines.append(f"Gender: {patient_info.get('gender', 'N/A')}")
        lines.append(f"Blood Type: {patient_info.get('blood_type', 'N/A')}")
        temp = extras.get("temperature_c")
        if temp is not None:
            lines.append(f"Reported Temperature: {float(temp):.1f} C")
        lines.append("")

        lines.append("-" * 60)
        lines.append("SELECTED SYMPTOMS")
        lines.append("-" * 60)
        for i, (symptom, severity) in enumerate(selected.items(), 1):
            suffix = f" ({severity.title()})" if severity else ""
            lines.append(f"  {i}. {humanize(symptom)}{suffix}")
        durations = extras.get("durations") or {}
        if durations:
            lines.append(
                "  Duration: " + ", ".join(
                    f"{humanize(s)}: {d}" for s, d in durations.items()))
        lines.append("")

        lines.append("-" * 60)
        lines.append("DIAGNOSIS RESULTS")
        lines.append("-" * 60)
        lines.append(f"{'Rank':<6}{'Disease':<30}{'Confidence':<15}{'Matched/Total'}")
        lines.append("-" * 60)
        for i, result in enumerate(results[:10], 1):
            lines.append(
                f"{i:<6}{humanize(result['disease']):<30}{result['confidence']}%"
                f"{'':<12}{result['matched']}/{result['total']}")
        lines.append("")

        if results:
            top = results[0]
            lines.append("-" * 60)
            lines.append("TOP DIAGNOSIS DETAILS")
            lines.append("-" * 60)
            lines.append(f"Disease: {humanize(top['disease'])}")
            lines.append(f"Category: {disease_info.get('category', 'N/A').title()}")
            lines.append(f"Confidence: {top['confidence']}%")
            if top.get("risk_note"):
                lines.append(f"Risk: {top['risk_note']}")
            lines.append("")
            lines.append("Description:")
            lines.append(f"  {disease_info.get('description', 'N/A')}")
            lines.append("")
            lines.append("Recommendation:")
            lines.append(f"  {disease_info.get('recommendation', 'N/A')}")
            lines.append("")
            if disease_info.get("is_emergency"):
                lines.append("*** EMERGENCY: This condition requires immediate medical attention ***")
                lines.append("")

        lines.append("-" * 60)
        lines.append("EXPLANATION")
        lines.append("-" * 60)
        lines.append(explanation)
        lines.append("")

        lines.append("=" * 60)
        lines.append("DISCLAIMER: This report is generated by an AI expert system for")
        lines.append("educational purposes only. It is NOT a substitute for professional")
        lines.append("medical diagnosis. Always consult a qualified healthcare provider.")
        lines.append("=" * 60)
        return lines

    # ------------------------------------------------------------------
    # PDF rendering
    # ------------------------------------------------------------------
    def _write_pdf(self, path: str, lines: list[str]) -> None:
        try:
            from reportlab.lib.enums import TA_CENTER
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.units import mm
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "PDF export needs the 'reportlab' package. Install it with:\n"
                "    pip install reportlab"
            ) from exc
        from xml.sax.saxutils import escape

        base = getSampleStyleSheet()
        title = ParagraphStyle(
            "ReportTitle", parent=base["Title"], fontSize=16, alignment=TA_CENTER)
        subtitle = ParagraphStyle(
            "ReportSubtitle", parent=base["BodyText"], fontSize=9,
            alignment=TA_CENTER, textColor="#666666")
        heading = ParagraphStyle(
            "ReportHeading", parent=base["Heading2"], fontSize=12,
            spaceBefore=10, spaceAfter=4, textColor="#0b3d66")
        body = ParagraphStyle(
            "ReportBody", parent=base["BodyText"], fontSize=10, leading=14)

        dirname = os.path.dirname(os.path.abspath(path))
        os.makedirs(dirname, exist_ok=True)
        doc = SimpleDocTemplate(
            path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
            topMargin=16 * mm, bottomMargin=16 * mm,
            title="MedInfer AI Diagnosis Report",
            author="MedInfer AI - Medical Diagnosis Expert System",
        )
        story: list[Any] = []
        for line in lines:
            stripped = line.strip()
            if not stripped or set(stripped) <= set("=-"):
                story.append(Spacer(1, 5))
                continue
            text = escape(stripped)
            if stripped == "MEDICAL DIAGNOSIS REPORT":
                story.append(Paragraph(text, title))
            elif stripped.startswith("AI-Based Medical"):
                story.append(Paragraph(text, subtitle))
            elif self._is_heading(stripped):
                story.append(Paragraph(text, heading))
            else:
                story.append(Paragraph(text, body))
        doc.build(story)

    @staticmethod
    def _is_heading(text: str) -> bool:
        """True for all-caps section headings such as 'PATIENT INFORMATION'."""
        return len(text) > 3 and all(
            ch.isupper() or ch in " &/()-" for ch in text)
