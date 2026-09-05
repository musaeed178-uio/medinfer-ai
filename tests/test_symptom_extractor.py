# SPDX-License-Identifier: AGPL-3.0-or-later
"""Tests for free-text symptom extraction (pure Python, no Prolog needed)."""

import pytest

from symptom_extractor import SymptomExtractor


@pytest.fixture(scope="module")
def extractor(catalog):
    return SymptomExtractor(catalog)


def test_multiword_phrases(extractor):
    result = extractor.extract("I have loss of appetite and shortness of breath")
    assert set(result.symptom_ids) == {"loss_of_appetite", "shortness_of_breath"}


def test_single_symptom_phrase_self_match(extractor):
    """Every symptom can be matched by typing its own display name."""
    names = [s.replace("_", " ") for s in extractor.catalog.symptoms]
    for name in names:
        result = extractor.extract(f"I have {name}")
        assert result.symptom_ids, f"no match for {name!r}"


def test_aliases(extractor):
    assert "nasal_congestion" in extractor.extract("I have a stuffy nose").symptom_ids
    assert "fever" in extractor.extract("feeling feverish since last night").symptom_ids
    assert "fatigue" in extractor.extract("I feel exhausted all the time").symptom_ids


def test_negation(extractor):
    result = extractor.extract("I have no fever but my cough is bad")
    assert "fever" not in result.symptom_ids
    assert "cough" in result.symptom_ids


def test_negation_clause_boundary(extractor):
    # 'no' must not leak across 'but' into a later symptom
    result = extractor.extract("no fever, but I have a runny nose and sneezing")
    assert "fever" not in result.symptom_ids
    assert {"runny_nose", "sneezing"} <= set(result.symptom_ids)


def test_severity_attribution(extractor):
    result = extractor.extract("a high fever, a dry cough and a severe headache")
    assert result.severities.get("fever") == "severe"
    assert result.severities.get("cough") == "moderate"   # not polluted by 'high'
    assert result.severities.get("headache") == "severe"


def test_severity_mild(extractor):
    result = extractor.extract("just a mild headache")
    assert result.severities.get("headache") == "mild"


def test_durations_numeric_and_words(extractor):
    result = extractor.extract("fever for 2 days and a cough for one week")
    assert result.durations.get("fever") == "2 day"
    assert result.durations.get("cough") == "1 week"


def test_temperature_fahrenheit_and_celsius(extractor):
    assert extractor.extract("my temperature is 102 f").temperature_c == pytest.approx(38.9, abs=0.1)
    assert extractor.extract("a fever of 39.5 degrees celsius").temperature_c == 39.5


def test_temperature_without_units(extractor):
    assert extractor.extract("temperature of 101").temperature_c == pytest.approx(38.3, abs=0.1)


def test_temperature_only_text_still_captured(extractor):
    result = extractor.extract("only my temperature: 38.9")
    assert result.temperature_c == pytest.approx(38.9, abs=0.1)
    assert not result.has_any()


def test_no_match_returns_empty(extractor):
    result = extractor.extract("I feel totally fine today")
    assert not result.has_any()
    assert result.temperature_c is None
