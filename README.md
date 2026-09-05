# MedInfer AI - Medical Diagnosis Expert System

An AI-powered expert system that helps users identify possible diseases from
their symptoms. Reasoning runs in **SWI-Prolog** over a rule-based knowledge
base; the **Python/CustomTkinter** GUI collects symptoms from checkboxes or
free text and explains the ranked candidates.

> **Disclaimer:** this system is for **educational and demonstration purposes
> only**. It is NOT a substitute for professional medical diagnosis. Always
> consult a qualified healthcare provider.

## Features

### Core
- Disease prediction across **25+ diseases** from **48 selectable symptoms**
  organized into 11 body systems
- Rule-based candidate selection and severity-weighted confidence in Prolog
- Per-symptom **Mild / Moderate / Severe** rating that genuinely affects the
  confidence score (scores are normalized and capped at 100%)
- **Age-aware scoring**: conditions with age-band risk factors (e.g. flu,
  pneumonia, COVID-19 in the elderly) are transparently adjusted and labeled
- **Natural-language input**: describe symptoms in a sentence - the parser
  understands multi-word symptoms and synonyms ("stuffy nose", "high
  temperature"), skips negated ones ("no fever"), rates severity from nearby
  adjectives, and captures **duration** ("for 2 days") and **temperature**
  ("102 F")
- **Differential diagnosis panel** with per-disease likelihood, matched/total
  indicators and emergency badges
- **Triage "next step" guidance**: EMERGENCY (go now) / URGENT (see a
  clinician today) / SELF-CARE, driven by emergency conditions, red-flag
  symptoms, high temperature and prolonged fever

### Data & reporting
- **Patient profile management** (name, age, gender, blood type) with saved
  patients
- **Diagnosis history** storing symptoms, severities, temperature, durations
  and full result lists
- **Report export** to **TXT or PDF** with patient info, severity breakdown,
  results table, explanation and disclaimer
- **Disease encyclopedia** with descriptions, categories, recommendations,
  emergency flags, age-risk groups and symptom lists
- **Symptom search that never loses your selection**, disease categories and
  dark UI

## Architecture

```
┌──────────────────────────  gui.py  ─────────────────────────┐
│  checkbox symptoms + severities    free text (NLP)          │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               │                    symptom_extractor.py
               │                    (pure Python, no engine)
               ▼                              ▼
        controller.py  ───────────────────►  kb_catalog.py (KBCatalog)
               │  assert patient facts            ▲
               ▼                                  │
        medical_kb.pl (SWI-Prolog engine)   kb_catalog.json
        facts + inference rules            (single source of truth)
                                                │
                                   generate_kb.py (regenerates facts)
```

- **`kb_catalog.json`** is the *single source of truth* for all knowledge
  content (diseases, symptoms, aliases, weights, risk factors). The GUI, the
  NLP parser and the age-risk logic read it directly.
- **`medical_kb.pl`** holds the same facts (generated) plus the hand-written
  inference rules. `controller.py` asserts the patient's symptoms and asks the
  Prolog engine which diseases are possible and how confident each match is.
- A pytest guarantees the committed `medical_kb.pl` is never out of sync with
  the catalog (`tests/test_generate_kb.py`).

## Project structure

```
├── gui.py               # CustomTkinter GUI
├── controller.py        # Python <-> Prolog bridge + triage/explanation
├── kb_catalog.py        # typed loader/models for the knowledge catalog
├── kb_catalog.json      # ⭐ single source of truth for knowledge content
├── generate_kb.py       # regenerates medical_kb.pl facts from the catalog
├── medical_kb.pl        # Prolog knowledge base (facts generated + rules)
├── symptom_extractor.py # free-text -> symptoms/severity/duration/temperature
├── patient_profile.py   # patient profiles + diagnosis history (JSON)
├── report_exporter.py   # TXT/PDF report export
├── tests/               # pytest suite (engine tests skip without SWI-Prolog)
├── data/                # auto-created; patient data (gitignored)
├── gui.spec             # PyInstaller spec (bundles the KB data files)
├── LICENSE              # GNU AGPL-3.0
└── requirements*.txt
```

## Prerequisites

- Python 3.8+
- [SWI-Prolog](https://www.swi-prolog.org/) (must be installed and on PATH;
  the app shows a friendly message when it is missing)

## Installation

```bash
pip install -r requirements.txt        # runtime
pip install -r requirements-dev.txt    # + pytest for development
```

## Usage

```bash
python gui.py
```

1. Set up your patient profile (optional; age enables age-risk adjustment)
2. Select symptoms (rate them Mild/Moderate/Severe) **or** describe them in
   one sentence and press *Analyze Text*
3. Click **Run Diagnosis** to see the ranked differential with confidence,
   matched indicators, emergency flags and **next-step guidance**
4. View the explanation, then export a TXT/PDF report

## Extending the knowledge base

Add or edit diseases/symptoms in **`kb_catalog.json`**, then regenerate the
Prolog facts:

```bash
python generate_kb.py          # rewrite medical_kb.pl from the catalog
python generate_kb.py --check  # verify it is up to date (exit 1 if stale)
```

Prefer editing the catalog over hand-editing `medical_kb.pl`: any manual
change inside the generated block is overwritten on the next run, and tests
fail if the committed file drifts from the catalog. The inference rules at
the bottom of `medical_kb.pl` remain hand-written.

## Tests

```bash
python -m pytest -q
```

Engine integration tests (tests/test_controller.py) run automatically when
SWI-Prolog is on PATH and are skipped otherwise.

## Reasoning notes

- Candidate diseases must match at least two symptoms
  (`possible_disease/1` in the KB).
- Confidence = (sum of matched symptoms' weights × user severity factor) ÷
  (sum of the disease's total weights), rounded and capped at 100%.
- The severity factors are mild 0.8 / moderate 1.0 / severe 1.25; disease
  symptoms can carry additional per-symptom weights (e.g. `coughing_blood`
  for tuberculosis).
- Age-risk bands (child / adolescent / adult / middle_aged / elderly) add a
  transparent +5-point adjustment when the patient's age band matches a
  disease risk factor.

## License

Copyright (C) 2026 MedInfer AI contributors.
Licensed under the **GNU Affero General Public License v3.0 or later**
(SPDX: `AGPL-3.0-or-later`); see [LICENSE](LICENSE).

AGPL note: if you deploy a modified version of this software as a network
service (for example a web symptom checker), you must make your modified
source code available to that service's users (AGPL section 13). This project
is for education and demonstration only and is **not** a regulated medical
device.
