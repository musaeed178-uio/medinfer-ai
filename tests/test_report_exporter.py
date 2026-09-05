# SPDX-License-Identifier: AGPL-3.0-or-later
"""Report exporter tests (TXT always; PDF when reportlab is installed)."""

import pytest

from report_exporter import ReportExporter

PATIENT = {"name": "Ada Lovelace", "age": 36, "gender": "Female", "blood_type": "O+"}
RESULTS = [{
    "disease": "covid19", "confidence": 62, "base_confidence": 57,
    "matched": 4, "total": 8, "category": "viral", "emergency": True,
    "risk_note": "Age 70 (elderly): elevated risk for Covid19",
}]
INFO = {
    "name": "Covid19", "category": "viral",
    "description": "A respiratory illness caused by SARS-CoV-2.",
    "recommendation": "Isolate and monitor oxygen.",
    "is_emergency": True,
}
EXPLANATION = "AI Analysis: Covid19\n\nMatched symptoms: Fever (Severe), Cough (Moderate)."


@pytest.fixture(scope="module")
def exporter():
    return ReportExporter()


def test_export_txt(exporter, tmp_path):
    path = exporter.export(
        "txt", PATIENT, {"fever": "severe", "cough": "moderate"}, RESULTS,
        EXPLANATION, INFO, {"temperature_c": 38.9, "durations": {"fever": "2 day"}},
        save_path=str(tmp_path / "report.txt"))
    assert path is not None
    body = open(path, encoding="utf-8").read()
    assert "Ada Lovelace" in body
    assert "Fever (Severe)" in body and "Cough (Moderate)" in body
    assert "38.9" in body
    assert "EMERGENCY" in body
    assert "DISCLAIMER" in body


def test_export_unknown_kind(exporter, tmp_path):
    with pytest.raises(ValueError):
        exporter.export("docx", PATIENT, {}, RESULTS, EXPLANATION, INFO,
                        save_path=str(tmp_path / "x.docx"))


def test_export_history_txt(exporter, tmp_path):
    history = [{
        "timestamp": "2024-01-01T10:00:00",
        "symptoms": ["fever", "cough"],
        "top_disease": "flu", "confidence": 60,
        "temperature_c": 38.3,
    }]
    path = exporter.export_history_txt(history, PATIENT, save_path=str(tmp_path / "h.txt"))
    body = open(path, encoding="utf-8").read()
    assert "Flu" in body and "38.3" in body


def test_export_pdf(exporter, tmp_path):
    reportlab = pytest.importorskip("reportlab")
    path = exporter.export(
        "pdf", PATIENT, {"fever": "severe"}, RESULTS, EXPLANATION, INFO,
        save_path=str(tmp_path / "report.pdf"))
    assert path is not None
    with open(path, "rb") as f:
        assert f.read(5) == b"%PDF-"
