# SPDX-License-Identifier: AGPL-3.0-or-later
"""Live-engine tests (require SWI-Prolog; skipped automatically otherwise)."""

import pytest


def test_empty_and_single_symptom_yield_no_diagnosis(controller):
    assert controller.diagnose({}) == []
    # the engine requires at least two matched indicators
    assert controller.diagnose({"fever": "moderate"}) == []


def test_results_ranked_with_bounded_confidence(controller):
    selected = {"fever": "moderate", "cough": "moderate",
                "fatigue": "moderate", "body_ache": "mild"}
    results = controller.diagnose(selected)
    assert results
    confidences = [r.confidence for r in results]
    assert confidences == sorted(confidences, reverse=True)
    for r in results:
        assert 0 <= r.confidence <= 100
        assert 0 < r.matched <= r.total
        assert r.category


def test_severity_scales_confidence(controller):
    mild = controller.diagnose({"fever": "mild", "cough": "mild", "fatigue": "mild"})
    severe = controller.diagnose({"fever": "severe", "cough": "severe", "fatigue": "severe"})
    mild_map = {r.disease: r for r in mild}
    for r in severe:
        if r.disease in mild_map:
            assert r.confidence >= mild_map[r.disease].confidence, r.disease
            assert r.matched == mild_map[r.disease].matched


def test_severity_severe_increases_top_score(controller):
    base = controller.diagnose({"fever": "mild", "cough": "mild", "fatigue": "mild"})
    boost = controller.diagnose({"fever": "severe", "cough": "mild", "fatigue": "mild"})
    base_top = {r.disease: r.confidence for r in base}
    # the disease with a severity_weight on fever must improve
    flu_base = base_top.get("flu")
    for r in boost:
        if r.disease == "flu" and flu_base is not None:
            assert r.confidence > flu_base  # flu carries a fever severity weight


def test_age_risk_adjustment_pneumonia(controller):
    selected = {"cough": "moderate", "shortness_of_breath": "moderate",
                "fever": "moderate", "fatigue": "moderate"}
    adult = controller.diagnose(selected, age=40)
    elderly = controller.diagnose(selected, age=72)
    by_name = {r.disease: r for r in elderly}
    assert "pneumonia" in by_name
    elderly_p = by_name["pneumonia"]
    assert elderly_p.risk_note and "elderly" in elderly_p.risk_note
    assert elderly_p.confidence == elderly_p.base_confidence + 5
    adult_by_name = {r.disease: r for r in adult}
    if "pneumonia" in adult_by_name:
        assert adult_by_name["pneumonia"].risk_note is None
        assert adult_by_name["pneumonia"].base_confidence == elderly_p.base_confidence


def test_emergency_flag_and_triage(controller):
    selected = {s: "severe" for s in
                ("fever", "headache", "joint_pain", "muscle_pain",
                 "rash", "nausea", "vomiting", "swollen_glands")}
    results = controller.diagnose(selected)
    assert results and results[0].disease == "dengue"
    assert results[0].emergency and results[0].confidence == 100
    level, title, _guidance = controller.triage(results, selected)
    assert level == "EMERGENCY"


def test_red_flag_triggers_urgent(controller):
    # flu-like symptoms are not urgent on their own...
    benign = {"fever": "moderate", "cough": "moderate", "fatigue": "moderate"}
    results = controller.diagnose(benign)
    level, _title, _guidance = controller.triage(results, benign)
    assert level == "SELF_CARE"
    # ...but reporting a red-flag symptom must escalate to at least URGENT
    # (it can become EMERGENCY when the top match is itself an emergency
    # disease above the confidence threshold, which outranks URGENT).
    red = dict(benign)
    red["coughing_blood"] = "moderate"
    results_red = controller.diagnose(red)
    level_red, _t, _g = controller.triage(results_red, red)
    assert level_red in ("URGENT", "EMERGENCY")


def test_high_temperature_or_long_fever_is_urgent(controller):
    benign = {"fever": "moderate", "cough": "moderate"}
    results = controller.diagnose(benign)
    level, _title, _guidance = controller.triage(results, benign)
    assert level == "SELF_CARE"
    level2, _t, _g = controller.triage(results, benign, temperature_c=40.0)
    assert level2 == "URGENT"
    level3, _t, _g = controller.triage(results, benign,
                                        durations={"fever": "5 day"})
    assert level3 == "URGENT"


def test_explanation_includes_matched_and_missing(controller):
    selected = {"fever": "severe", "cough": "moderate", "headache": "mild"}
    results = controller.diagnose(selected)
    top = results[0]
    text = controller.build_explanation(top.disease, selected)
    assert top.name in text
    assert "Matched symptoms" in text and "Fever (Severe)" in text
    assert "Recommendation" in text
