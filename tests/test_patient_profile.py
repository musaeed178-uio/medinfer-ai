# SPDX-License-Identifier: AGPL-3.0-or-later
"""Patient profile and history persistence tests."""

import json

from patient_profile import PatientProfile


def _profile(tmp_path):
    return PatientProfile(data_dir=str(tmp_path))


def test_empty_profile_defaults(tmp_path):
    profile = _profile(tmp_path)
    assert profile.get_current_profile()["name"] == ""
    assert profile.get_history() == []
    assert profile.get_statistics()["total_diagnoses"] == 0


def test_save_load_delete_profile(tmp_path):
    profile = _profile(tmp_path)
    profile.current_profile.update({"name": "Jane", "age": 34, "gender": "Female"})
    profile.save_current_profile()
    assert len(profile.get_saved_profiles()) == 1

    other = PatientProfile(data_dir=str(tmp_path))  # fresh instance reads the file
    assert other.get_saved_profiles()[0]["name"] == "Jane"
    assert other.get_current_profile()["age"] == 34

    assert other.delete_profile(0)
    assert other.get_saved_profiles() == []


def test_duplicate_name_updates_in_place(tmp_path):
    profile = _profile(tmp_path)
    profile.current_profile.update({"name": "Jane", "age": 30})
    profile.save_current_profile()
    profile.current_profile = {"name": "Jane", "age": 31,
                               "gender": "Other", "blood_type": "Unknown"}
    profile.save_current_profile()
    profiles = profile.get_saved_profiles()
    assert len(profiles) == 1
    assert profiles[0]["age"] == 31


def test_add_diagnosis_with_extras(tmp_path):
    profile = _profile(tmp_path)
    results = [{"disease": "covid19", "confidence": 80, "matched": 5, "total": 8}]
    profile.add_diagnosis(
        ["fever", "cough"], results, "covid19", 80,
        extras={"severities": {"fever": "severe", "cough": "moderate"},
                "temperature_c": 38.9, "durations": {"fever": "2 day"}})
    history = profile.get_history()
    assert len(history) == 1
    entry = history[0]
    assert entry["top_disease"] == "covid19"
    assert entry["temperature_c"] == 38.9
    assert entry["durations"] == {"fever": "2 day"}
    assert entry["severities"]["fever"] == "severe"

    stats = profile.get_statistics()
    assert stats["total_diagnoses"] == 1
    assert stats["most_common_disease"] == "covid19"


def test_legacy_history_without_extras_still_loads(tmp_path):
    # entries written by older versions have no severities/temperature
    legacy = [{
        "timestamp": "2024-01-01T10:00:00",
        "symptoms": ["fever"],
        "results": [{"disease": "flu", "confidence": 60, "matched": 2, "total": 7}],
        "top_disease": "flu",
        "confidence": 60,
    }]
    history_path = tmp_path / "diagnosis_history.json"
    history_path.write_text(json.dumps(legacy), encoding="utf-8")
    profile = PatientProfile(data_dir=str(tmp_path))
    entry = profile.get_history()[0]
    assert entry["top_disease"] == "flu"
    assert entry.get("temperature_c") is None
    assert profile.get_statistics()["total_diagnoses"] == 1


def test_clear_history(tmp_path):
    profile = _profile(tmp_path)
    profile.add_diagnosis(["fever"], [], "flu", 60)
    profile.clear_history()
    assert profile.get_history() == []
