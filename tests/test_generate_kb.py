# SPDX-License-Identifier: AGPL-3.0-or-later
"""The generated Prolog facts must always match kb_catalog.json.

Editing one source without regenerating the other is caught here, because
regenerating in memory must reproduce the committed medical_kb.pl byte for
byte (the hand-written header and rules stay untouched).
"""

import os

import generate_kb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_committed_kb_is_up_to_date():
    catalog = generate_kb.load_catalog()
    generated = generate_kb.build_kb(catalog)
    current = open(generate_kb.KB_PATH, encoding="utf-8").read()
    assert generated == current, (
        "medical_kb.pl is out of date. Run: python generate_kb.py")


def test_markers_present_and_facts_generated():
    text = open(generate_kb.KB_PATH, encoding="utf-8").read()
    assert generate_kb.BEGIN_MARKER in text
    assert generate_kb.END_MARKER in text
    # no severity wildcard should exist; every pair is explicit
    assert "severity_weight(_, _, 1.0)." not in text


def test_generated_facts_cover_catalog():
    catalog = generate_kb.load_catalog()
    facts = generate_kb.build_facts(catalog)
    for disease_id in catalog["diseases"]:
        assert f"disease({disease_id})." in facts
        assert f"description({disease_id}, '" in facts
        assert f"recommendation({disease_id}, '" in facts
        assert f"category({disease_id}, " in facts
    symptom_ids = [s for block in catalog["body_systems"].values()
                   for s in block["symptoms"]]
    for symptom in symptom_ids:
        assert f"symptom({symptom})." in facts


def test_splice_preserves_rules_and_markers():
    sample = ("HEADER\n" + generate_kb.BEGIN_MARKER + "\nOLD FACTS\n"
              + generate_kb.END_MARKER + "\nRULES\n")
    out = generate_kb.splice_facts(sample, "NEW FACTS")
    assert out == ("HEADER\n" + generate_kb.BEGIN_MARKER + "\nNEW FACTS\n"
                   + generate_kb.END_MARKER + "\nRULES\n")
