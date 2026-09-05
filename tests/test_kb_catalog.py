# SPDX-License-Identifier: AGPL-3.0-or-later
"""Consistency tests for kb_catalog.json (the single source of truth)."""

import json
import os

from kb_catalog import KBCatalog, age_band, humanize


def test_catalog_is_valid(catalog):
    assert catalog.validate() == []


def test_catalog_metadata(catalog):
    assert catalog.version  # non-empty
    raw = json.load(open(os.path.join(os.path.dirname(__file__), "..", "kb_catalog.json"),
                         encoding="utf-8"))
    assert raw["_meta"]["license"] == "AGPL-3.0-or-later"


def test_minimum_scale(catalog):
    assert len(catalog.diseases) >= 25
    assert len(catalog.symptoms) >= 45
    # every body system groups at least one selectable symptom
    assert len(catalog.body_systems) >= 10


def test_every_symptom_used_by_a_disease(catalog):
    used = {s for d in catalog.diseases.values() for s in d.symptoms}
    assert set(catalog.symptoms) == used


def test_weights_reference_real_disease_symptoms(catalog):
    for disease_id, disease in catalog.diseases.items():
        for symptom, weight in disease.weights.items():
            assert symptom in disease.symptoms, (disease_id, symptom)
            assert weight > 0
        for symptom in disease.symptoms:
            assert disease.weight(symptom) > 0  # missing weights default to 1.0


def test_risk_factors_use_known_bands(catalog):
    from kb_catalog import AGE_BANDS
    for disease_id, disease in catalog.diseases.items():
        for band in disease.age_risk_bands():
            assert band in AGE_BANDS, (disease_id, band)


def test_red_flags_are_real_symptoms(catalog):
    assert catalog.red_flag_symptoms() <= set(catalog.symptoms)
    # the clinically chosen red-flag symptoms are present
    assert {"chest_pain", "coughing_blood", "confusion", "shortness_of_breath"} \
        <= catalog.red_flag_symptoms()


def test_night_sweats_is_selectable_and_used(catalog):
    # regression: night_sweats existed in Prolog but was missing from the GUI
    assert "night_sweats" in catalog.symptoms
    assert any("night_sweats" in d.symptoms for d in catalog.diseases.values())


def test_no_unused_gui_symptoms(catalog):
    # regression: skin_rash / stiff_neck were selectable but useless
    assert "skin_rash" not in catalog.symptoms
    assert "stiff_neck" not in catalog.symptoms


def test_humanize():
    assert humanize("chest_pain") == "Chest Pain"
    assert humanize("covid19") == "Covid19"


def test_age_band():
    assert age_band(None) is None
    assert age_band(0) is None
    assert age_band(4) == "child"
    assert age_band(17) == "adolescent"
    assert age_band(39) == "adult"
    assert age_band(64) == "middle_aged"
    assert age_band(65) == "elderly"
