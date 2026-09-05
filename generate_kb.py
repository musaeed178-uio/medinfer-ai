# SPDX-License-Identifier: AGPL-3.0-or-later
"""Regenerate the facts block of medical_kb.pl from kb_catalog.json.

kb_catalog.json is the single source of truth for the expert system's
knowledge content. The facts between the BEGIN/END markers in
medical_kb.pl are produced by this script; the header and the inference
rules at the bottom of that file are maintained by hand.

Usage:
    python generate_kb.py            # rewrite medical_kb.pl from the catalog
    python generate_kb.py --check    # exit non-zero if medical_kb.pl is stale
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(HERE, "kb_catalog.json")
KB_PATH = os.path.join(HERE, "medical_kb.pl")

BEGIN_MARKER = "% ------------------- GENERATED FACTS (BEGIN) -------------------"
END_MARKER = "% ------------------- GENERATED FACTS (END) -------------------"


def _num(value):
    """Format a numeric weight losslessly (1.0, 1.2, 1.5, ...)."""
    return repr(float(value))


def build_facts(catalog):
    """Return the generated facts block (without the marker lines)."""
    meta = catalog.get("_meta", {})
    body_systems = catalog["body_systems"]
    diseases = catalog["diseases"]

    # Symptoms in body-system order.
    symptom_order = []
    for system in body_systems.values():
        symptom_order.extend(system["symptoms"].keys())

    lines = []
    lines.append("%% Knowledge facts generated from kb_catalog.json (version %s)." % meta.get("version", "?"))
    lines.append("%% Do not edit by hand - regenerate with: python generate_kb.py")
    lines.append("")

    lines.append("% Diseases")
    for d in diseases:
        lines.append("disease(%s)." % d)
    lines.append("")

    lines.append("% Disease categories")
    for d, info in diseases.items():
        lines.append("category(%s, %s)." % (d, info["category"]))
    lines.append("")

    lines.append("% Disease descriptions")
    for d, info in diseases.items():
        lines.append("description(%s, '%s')." % (d, info["description"]))
    lines.append("")

    lines.append("% Recommendations")
    for d, info in diseases.items():
        lines.append("recommendation(%s, '%s')." % (d, info["recommendation"]))
    lines.append("")

    lines.append("% Emergency flags")
    for d, info in diseases.items():
        if info["emergency"]:
            lines.append("is_emergency(%s)." % d)
    lines.append("")

    lines.append("% Symptoms")
    for s in symptom_order:
        lines.append("symptom(%s)." % s)
    lines.append("")

    lines.append("% Disease-symptom links")
    for d, info in diseases.items():
        for s in info["symptoms"]:
            lines.append("has_symptom(%s, %s)." % (d, s))
    lines.append("")

    lines.append("% Severity weights (one per disease-symptom pair; symptoms without an")
    lines.append("% explicit weight in the catalog default to 1.0)")
    for d, info in diseases.items():
        weights = info.get("weights", {})
        for s in info["symptoms"]:
            lines.append("severity_weight(%s, %s, %s)." % (d, s, _num(weights.get(s, 1.0))))
    lines.append("")

    lines.append("% Age-based risk factors")
    for d, info in diseases.items():
        for band in info.get("risk_factors", {}).get("age", []):
            lines.append("risk_factor(%s, age, %s)." % (d, band))
    lines.append("")

    return "\n".join(lines)


def build_kb(catalog):
    """Return the full medical_kb.pl content (header + facts + rules)."""
    text = open(KB_PATH, encoding="utf-8").read()
    return splice_facts(text, build_facts(catalog))


def splice_facts(text, facts_block):
    """Replace everything between BEGIN_MARKER and END_MARKER in ``text``."""
    start = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < 0:
        raise RuntimeError(
            "medical_kb.pl is missing the generated-facts markers (%r / %r); "
            "cannot regenerate." % (BEGIN_MARKER, END_MARKER))
    start = text.find("\n", start) + 1       # keep BEGIN marker line
    end = text.rfind("\n", 0, end)           # keep END marker line
    return text[:start] + facts_block + text[end:] + ("\n" if not text[end:].endswith("\n") else "")


def load_catalog(path=CATALOG_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if medical_kb.pl is not up to date")
    args = parser.parse_args(argv)

    catalog = load_catalog()
    generated = build_kb(catalog)
    current = open(KB_PATH, encoding="utf-8").read()

    if args.check:
        if generated != current:
            print("medical_kb.pl is out of date; run: python generate_kb.py", file=sys.stderr)
            return 1
        print("medical_kb.pl is up to date.")
        return 0

    with open(KB_PATH, "w", encoding="utf-8") as f:
        f.write(generated)
    print("Regenerated %s from kb_catalog.json." % KB_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
