# Developer Manual — MedInfer AI

> **TL;DR for the impatient:** the knowledge content lives in `kb_catalog.json` (single source of truth). The GUI talks to `core.manager.DiagnosisManager`, which is wired in `bootstrap.py`. Inference runs in SWI-Prolog inside `medical_kb.pl`, whose facts are *generated* from the catalog by `generate_kb.py`. To add/remove/edit a disease or symptom: edit `kb_catalog.json`, then run `python generate_kb.py`. Never hand-edit the generated facts block in `medical_kb.pl`.

MedInfer AI is an AI-powered medical diagnosis expert system. Reasoning runs in **SWI-Prolog** over a rule-based knowledge base; the **Python / CustomTkinter** GUI collects symptoms via checkboxes or free text and explains the ranked candidates.

This manual explains how each piece of code works and where to look when you want to add, remove, or edit an existing feature — or rewrite the whole codebase.

---

## Table of Contents

1. [Project overview](#1-project-overview)
2. [Architecture at a glance](#2-architecture-at-a-glance)
3. [File-by-file reference](#3-file-by-file-reference)
4. [Where to look when changing things](#4-where-to-look-when-changing-things)
5. [How the Prolog engine works](#5-how-the-prolog-engine-works)
6. [Dependency wiring (composition root)](#6-dependency-wiring-composition-root)
7. [Tests](#7-tests)
8. [Rebuilding / redistributing](#8-rebuilding-redistributing)
9. [Rewriting the codebase from scratch](#9-rewriting-the-codebase-from-scratch)
10. [AGENTS.md — notes for future AI sessions](#10-agentsmd--notes-for-future-ai-sessions)

---

## 1. Project overview

| Concern | Where it lives |
|---|---|
| Knowledge content (diseases, symptoms, aliases, weights, risk factors) | `kb_catalog.json` — **single source of truth** |
| Prolog facts (generated from the catalog) + hand-written inference rules | `medical_kb.pl` |
| KB generation / sync-checking script | `generate_kb.py` |
| Typed Python loader for the catalog | `kb_catalog.py` |
| Prolog engine bridge + triage + explanation text | `controller.py` |
| Domain service that orchestrates a diagnosis run | `core/manager.py` (`DiagnosisManager`) |
| Domain models (pure data, no framework imports) | `core/models.py` |
| Free-text → symptoms / severity / duration / temperature | `symptom_extractor.py` |
| Patient profiles + diagnosis history (JSON files in `./data`) | `patient_profile.py` |
| TXT / PDF report export | `report_exporter.py` |
| CustomTkinter desktop GUI | `gui.py` |
| Composition root — the only place that wires the object graph | `bootstrap.py` |
| Entry point (`python -m medinfer` or `python __main__.py`) | `__main__.py` |
| Tests | `tests/` |

---

## 2. Architecture at a glance

```
gui.py  ──thin adapter──▶  core/manager.py (DiagnosisManager)
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
             controller.py   patient_profile.py   report_exporter.py
                    │
             kb_catalog.py ◀── kb_catalog.json   (single source of truth)
                    │
             medical_kb.pl ◀── generate_kb.py   (facts are generated)
                    │
             SWI-Prolog engine  (installed separately, must be on PATH)
```

**Key rules**:

- The GUI is a *thin adapter*. It receives a `DiagnosisManager` via constructor injection and never imports from `controller` directly (except for a couple of internal-typing conveniences).
- `core/manager.py` is the **domain service**. It owns the workflow: text analysis → symptom extraction → engine diagnosis → triage → explanation → history persistence → export.
- `controller.py` bridges Python to the Prolog engine and also owns triage logic and explanation text. It reads `kb_catalog.json` through `kb_catalog.py` for all content; it only talks to Prolog for candidate selection.
- `kb_catalog.json` is the **single source of truth** for all knowledge content. The GUI, the NLP parser, and the age-risk logic all read it directly.
- `medical_kb.pl` holds the same facts (generated) plus hand-written inference rules. `controller.py` asserts the patient's symptoms and asks Prolog which diseases are possible.
- `generate_kb.py` regenerates the facts block of `medical_kb.pl` from the catalog. A pytest (`tests/test_generate_kb.py`) guarantees the committed `.pl` file is never out of sync.

---

## 3. File-by-file reference

### `kb_catalog.json` — knowledge content

This is the file you edit to add, remove, or change diseases and symptoms.

Structure:

- `_meta` — name, version, license, note.
- `body_systems` — map of system name → `{ symptoms: { symptom_id: { aliases: [...], red_flag: bool } } }`.
- `diseases` — map of disease_id → `{ category, description, recommendation, emergency, symptoms: [...], weights: {...}, risk_factors: { age: [...] } }`.

**Adding a new symptom:**

1. Add it under the appropriate `body_systems` entry in `kb_catalog.json`.
2. Give it an `aliases` list (plain-language phrases the NLP parser and symptom search understand).
3. Mark `red_flag: true` if it is a serious-warning symptom (drives the triage "see a clinician within 24 hours" path).
4. Reference it from at least one disease's `symptoms` list, or the catalog validator will complain (see `tests/test_kb_catalog.py`).

**Adding a new disease:**

1. Add an entry under `diseases` in `kb_catalog.json`.
2. Fill in `category`, `description`, `recommendation`, `emergency`, and `symptoms`.
3. Optionally add per-symptom `weights` (defaults to `1.0` if omitted) and `risk_factors.age` bands.
4. Run `python generate_kb.py` to regenerate `medical_kb.pl`.
5. Run the tests to confirm nothing is stale or invalid.

**Removing a disease or symptom:**

1. Remove it from `kb_catalog.json`.
2. Run `python generate_kb.py`.
3. If you removed a symptom, make sure no disease still references it (the validator will catch dangling references).

### `generate_kb.py` — facts generator

Reads `kb_catalog.json` and rewrites the facts block of `medical_kb.pl` between the `BEGIN`/`END` markers.

Usage:

```bash
python generate_kb.py          # rewrite medical_kb.pl from the catalog
python generate_kb.py --check  # exit 1 if medical_kb.pl is stale
```

The script uses `_prolog_str()` to escape single quotes in descriptions/recommendations. Apostrophes in disease descriptions (e.g. "Parkinson's disease") will cause Prolog syntax errors if not escaped. The errors manifest as `Syntax error: Operator expected` at seemingly random line numbers.

### `medical_kb.pl` — Prolog knowledge base

Two parts:

1. **Generated facts block** (between the `BEGIN`/`END` markers): disease/1, category/2, description/2, recommendation/2, is_emergency/1, symptom/1, has_symptom/2, severity_weight/3, risk_factor/3. Do not hand-edit this block — it is overwritten on every `generate_kb.py` run.
2. **Hand-written inference rules** (below the markers): `possible_disease/1`, `severity_factor/2`, and any other rules you add. These stay hand-written.

Candidate diseases must match at least two symptoms (`possible_disease/1` in the KB).

### `kb_catalog.py` — typed catalog loader

Loads and validates `kb_catalog.json`, exposes it as Python dataclasses:

- `SymptomDef` — symptom_id, body_system, aliases, red_flag.
- `DiseaseDef` — disease_id, category, description, recommendation, emergency, symptoms, weights, risk_factors; plus `weight(symptom)` and `age_risk_bands()`.
- `DiagnosisResult` — disease, confidence, base_confidence, matched, total, category, emergency, risk_note; plus `as_dict()` and `name`.
- `KBCatalog` — the loaded, validated catalog; methods: `load()`, `symptoms_by_system()`, `red_flag_symptoms()`, `symptom_phrases()`, `validate()`.

Also provides `humanize()` (snake_case → Title Case), `age_band()` (age → band string), `resource_path()` (handles both normal and PyInstaller paths).

### `controller.py` — Prolog bridge + triage + explanation

`MedicalController`:

- `__init__` — loads the catalog (or accepts one), starts `Prolog()`, consults `medical_kb.pl`, and precomputes a disease→symptom graph in Python (`_precompute_disease_graph`) to avoid repeated Prolog round-trips.
- `symptoms_by_system()`, `all_symptoms()`, `all_diseases()`, `disease_info()`, `search_symptoms()`, `search_diseases()` — catalog access for the GUI, no Prolog round-trips.
- `diagnose(selected, age)` — the main engine call. Asserts `patient_has/1` and `patient_sev/2` facts, queries `possible_disease(D)`, then computes confidence in Python using the precomputed graph. Age-risk bonus (+5 points) is applied when the patient's age band matches a disease risk factor.
- `triage(results, selected, temperature_c, durations)` — returns `(level, title, guidance)` with level in `{"EMERGENCY", "URGENT", "SELF_CARE"}`. Drives on emergency conditions, red-flag symptoms, high temperature, and prolonged fever.
- `build_explanation(disease_id, selected, extraction)` — builds the natural-language explanation shown in the GUI and exports.
- `_SEV_FACTOR = {"mild": 0.8, "moderate": 1.0, "severe": 1.25}` — must match Prolog's `severity_factor` rules. If you change one, change the other.

Confidence formula:

```
confidence = (sum of matched symptoms' weights × user severity factor) ÷ (sum of the disease's total weights)
```

Rounded, capped at 100%.

Severity factors: mild 0.8 / moderate 1.0 / severe 1.25. Disease symptoms can carry additional per-symptom weights (e.g. `coughing_blood` for tuberculosis).

Age-risk bands (child / adolescent / adult / middle_aged / elderly) add a transparent +5-point adjustment when the patient's age band matches a disease risk factor.

### `symptom_extractor.py` — free-text symptom extraction

Pure Python on top of `KBCatalog`. No Prolog. Extracts:

- which symptoms the text mentions (multi-word phrases and aliases, with basic negation handling — "no fever" is skipped),
- a Mild/Moderate/Severe rating per symptom from nearby adjectives,
- durations ("for 2 days") attributed to the nearest symptom,
- a body temperature ("102 F", "a fever of 39").

`ExtractionResult` carries `symptom_ids`, `severities`, `durations`, `duration_notes`, `temperature_c`, `temperature_raw`, and `has_any()`.

Nothing here makes a diagnosis — it only turns prose into the same structured symptom/severity input the checkbox GUI produces.

### `core/models.py` — domain models

Pure data, no framework imports. These sit at the boundary between the core and presentation layers.

- `SymptomSelection` — symptom_id + severity.
- `DiagnosisSession` — the full context of one diagnosis run (symptoms, patient_age, temperature_c, durations, extraction_text).
- `DiagnosisOutcome` — everything a presentation layer needs after a diagnosis run (results, top_disease, top_confidence, explanation, triage_level, triage_title, triage_guidance).

### `core/manager.py` — DiagnosisManager (domain service)

Orchestrates the diagnosis workflow. Presentation layers call its methods and receive plain data; they never touch the Prolog engine or the knowledge catalog directly.

- `__init__(controller, patient, exporter)` — all dependencies injected.
- `catalog`, `patient`, `exporter` — read-only accessors.
- `symptoms_by_system()`, `all_diseases()`, `disease_info()` — delegated to the controller.
- `analyze_text(text)` — parses free text into structured symptom data.
- `diagnose(session)` — the main entry point the GUI calls after "Run Diagnosis". Blocks (runs the Prolog engine synchronously); the GUI adapter should call it from a background thread.
- `export_report(fmt, session, outcome)` — exports a diagnosis report.

### `patient_profile.py` — patient profiles + diagnosis history

JSON files in `./data`:

- `saved_profiles.json` — saved patient profiles.
- `diagnosis_history.json` — diagnosis history (append-only schema).
- `session.json` — remembers the last active profile across restarts.

`PatientProfile`:

- Profile persistence: `_load_profiles`, `_save_profiles`, `save_current_profile`, `load_profile`, `delete_profile`, `switch_profile`, `set_guest`.
- Session management: `_load_session` restores the last-active profile on startup, falling back to guest mode. If the session file is corrupt or missing, it falls back to guest mode.
- Diagnosis history: `add_diagnosis`, `get_history`, `clear_history`.
- Statistics: `get_statistics`, `get_risk_factors`.

### `report_exporter.py` — TXT / PDF report export

Both formats share one content builder (`_build_lines`) so the wording never drifts between output types. `reportlab` is imported lazily — if it is missing, PDF export raises a helpful error instead of breaking the rest of the application.

### `gui.py` — CustomTkinter desktop GUI

`ModernMedicalGUI`:

- Receives a `DiagnosisManager` via constructor injection.
- `_build_layout` — creates the main container, sidebar, content area, and all frames.
- `_build_sidebar` — brand mark, navigation buttons, version footer.
- `_build_dashboard` — top bar (patient info, export format, export button), symptom panel, differential diagnosis panel, explanation panel.
- `_build_symptom_browser` — creates the full grouped symptom list once; filtering only toggles visibility.
- `_on_symptom_toggle`, `_update_severity` — symptom selection state.
- `_filter_symptoms` — live search that never loses your selection.
- `_analyze_nlp` — natural-language input; clears previous symptom selections before analyzing new text (NLP clearing bug was fixed).
- `_run_diagnosis`, `_diagnose_thread` — diagnosis flow in a background thread.
- `_render_outcome` — renders a `DiagnosisOutcome` from the manager.
- `_create_diag_card` — renders a single diagnosis card with progress bar.
- `_build_disease_info` — disease encyclopedia page.
- `_build_history` — diagnosis history page.
- `_build_profile` — patient profile page.
- `_export_report` — exports a report.

Color constants are centralized at the top of `gui.py` (`BG_BASE`, `ACCENT_BLUE`, etc.). Use these, not hardcoded hex values.

### `bootstrap.py` — composition root

The ONLY place where the object graph is wired. Every entry point (GUI, CLI, tests) calls `create_manager()` to get a fully-initialized `DiagnosisManager`. Presentation layers never instantiate controllers, extractors, or patient profiles directly.

### `__main__.py` — entry point

Calls `bootstrap.create_manager()` then passes it to `ModernMedicalGUI(manager=manager)`. The GUI no longer creates its own dependencies.

---

## 4. Where to look when changing things

### Add a new disease

1. `kb_catalog.json` → `diseases` — add the entry.
2. `python generate_kb.py` — regenerate `medical_kb.pl`.
3. `python -m pytest -q` — confirm tests pass.

### Add a new symptom

1. `kb_catalog.json` → `body_systems` — add the symptom under the appropriate system.
2. Reference it from at least one disease's `symptoms` list.
3. `python generate_kb.py`.
4. `python -m pytest -q`.

### Remove a disease or symptom

1. `kb_catalog.json` — remove it.
2. `python generate_kb.py`.
3. `python -m pytest -q`.

### Edit a disease or symptom description / recommendation / weight / risk factor

1. `kb_catalog.json` — edit the entry.
2. `python generate_kb.py`.
3. `python -m pytest -q`.

### Change the inference rules

1. `medical_kb.pl` — edit the hand-written rules below the `END` marker.
2. Do **not** touch the generated facts block.
3. `python -m pytest -q`.

### Change the triage logic

1. `controller.py` → `triage()`.
2. Update tests in `tests/test_controller.py` if needed.

### Change the explanation text

1. `controller.py` → `build_explanation()`.

### Change the GUI layout / styling

1. `gui.py` — color constants at the top, layout methods, widget builders.
2. Use the centralized color constants, not hardcoded hex values.

### Change the NLP parser

1. `symptom_extractor.py` — `SymptomExtractor.extract()`, severity classification, duration parsing, temperature parsing.
2. Add/modify tests in `tests/test_symptom_extractor.py`.

### Change the patient profile / history storage

1. `patient_profile.py` — schema is append-only; new keys may be added to history entries, but existing keys are never removed.
2. Add/modify tests in `tests/test_patient_profile.py`.

### Change report export

1. `report_exporter.py` — `_build_lines()` for shared content, `_write_pdf()` for PDF rendering.
2. Add/modify tests in `tests/test_report_exporter.py`.

### Rewrite the entire codebase

See [Section 9](#9-rewriting-the-codebase-from-scratch).

---

## 5. How the Prolog engine works

`controller.py` starts a `Prolog()` instance and consults `medical_kb.pl`. For each diagnosis run:

1. It retracts any previous `patient_has/1` and `patient_sev/2` facts.
2. It asserts the patient's symptoms and severities.
3. It queries `possible_disease(D)` to get candidate diseases.
4. It computes confidence in Python using the precomputed disease→symptom graph (this avoids ~165 Prolog round-trips per diagnosis).

Performance note: pyswip's `query()` has ~50μs overhead per call from ctypes FFI + term parsing. Precompute static data in Python to avoid repeated round-trips. The disease-symptom graph is precomputed at `MedicalController.__init__()` time; confidence is calculated in Python during `diagnose()`.

`_SEV_FACTOR` in `controller.py` must match Prolog's `severity_factor` rules. If you change one, change the other.

---

## 6. Dependency wiring (composition root)

`bootstrap.py:create_manager()` is the composition root. It builds:

- `MedicalController()` — loads the catalog and starts the Prolog engine.
- `PatientProfile()` — loads/saves patient data in `./data`.
- `ReportExporter()` — report export.
- `DiagnosisManager(controller, patient, exporter)` — the domain service.

All entry points call `create_manager()`. The GUI receives the manager via constructor injection. Tests can pass a custom `PatientProfile` to `create_manager(patient=...)`.

---

## 7. Tests

```bash
python -m pytest -q
```

- `tests/conftest.py` uses `pytest.importorskip("pyswip")` and `shutil.which("swipl")` — if either is missing, controller tests are skipped automatically.
- `tests/test_kb_catalog.py` — validates the catalog (every symptom must be used by at least one disease; weights must be positive; age bands must be known).
- `tests/test_generate_kb.py` — checks that `medical_kb.pl` matches what `generate_kb.py` would produce. Run `python generate_kb.py` after editing `kb_catalog.json` or this test fails.
- `tests/test_controller.py` — engine integration tests; require SWI-Prolog on PATH.
- `tests/test_symptom_extractor.py` — NLP parser tests; pure Python, no engine needed.
- `tests/test_patient_profile.py` — profile/history tests.
- `tests/test_report_exporter.py` — export tests.

---

## 8. Rebuilding / redistributing

- `requirements.txt` — runtime dependencies.
- `requirements-dev.txt` — + pytest for development.
- `gui.spec` — PyInstaller spec (bundles the KB data files).
- `resource_path()` in `kb_catalog.py` handles both normal and PyInstaller paths.

---

## 9. Rewriting the codebase from scratch

If you want to rewrite the entire codebase, here's the minimal skeleton you need to preserve the architecture:

1. **Knowledge catalog** — a single JSON file as the source of truth for diseases, symptoms, aliases, weights, risk factors. Load it with a typed Python loader.
2. **Prolog knowledge base** — generate facts from the catalog; keep inference rules hand-written. Use a `generate_kb.py` script with BEGIN/END markers and a test that guards against drift.
3. **Engine bridge** — a controller that asserts patient facts, queries candidates, and computes confidence in Python using a precomputed graph.
4. **Domain service** — a manager that owns the workflow: text analysis → symptom extraction → engine diagnosis → triage → explanation → history persistence → export. Inject dependencies via constructor.
5. **Domain models** — pure data classes at the boundary between core and presentation.
6. **NLP extractor** — pure Python on top of the catalog; no engine.
7. **Patient profile** — JSON files in `./data`; append-only schema.
8. **Report exporter** — shared content builder for TXT and PDF.
9. **GUI** — thin adapter that receives the manager via constructor injection.
10. **Composition root** — the only place that wires the object graph.

The tests live in `tests/` and use `pytest`. Controller tests require SWI-Prolog on PATH and are skipped otherwise.

---

## 10. AGENTS.md — notes for future AI sessions

See `AGENTS.md` for non-obvious learnings:

- Layered architecture: `core/manager.py` is the domain service. `gui.py` is a thin adapter. `bootstrap.py` is the composition root.
- KB pipeline is `kb_catalog.json` → `generate_kb.py` → `medical_kb.pl`. Edit the JSON, run the generator, never hand-edit the generated facts block.
- Prolog string escaping: `generate_kb.py` uses `_prolog_str()` to escape single quotes.
- Prolog FFI is the bottleneck, not Prolog itself: precompute static data in Python.
- `_SEV_FACTOR` in `controller.py` must match Prolog's `severity_factor` rules.
- Controller tests require SWI-Prolog on PATH.
- KB validation rule: every symptom must be used by at least one disease.
- `test_committed_kb_is_up_to_date` checks that `medical_kb.pl` matches what `generate_kb.py` would produce.
- Color constants are centralized at the top of `gui.py`.
- Session persistence: `patient_profile.py` writes `data/session.json`.
- NLP clearing bug was fixed: `_analyze_nlp()` now clears all previous symptom selections before analyzing new text.
- Windows paths: `resource_path()` in `kb_catalog.py` handles both normal and PyInstaller paths.

---

## Future projects: a note on creating this manual automatically

**From now on, for every new project, create a `DEVELOPER_MANUAL.md` that documents the same things this one does:**

1. What the project is and what it does.
2. A one-diagram architecture overview.
3. A file-by-file reference explaining what each file does and how it fits in.
4. A "where to look when changing things" section — add/remove/edit feature, change inference, change GUI, change NLP, change storage, change export.
5. How the core engine works (if there is one — Prolog, LLM, rules, DB, etc.).
6. How dependencies are wired (composition root, injection).
7. How to run tests and what each test file covers.
8. How to build / redistribute / bundle.
9. A "rewriting from scratch" section that lists the minimal architectural pieces to preserve.
10. Any AI-session notes (like this project's `AGENTS.md`).

Keep it concise but complete. If the project has a single source of truth (a JSON catalog, a DB schema, a config file), call it out explicitly and say what happens when you change it. If there's a generated artifact that must stay in sync (like `medical_kb.pl`), explain the generation command and the test that guards it. If there are tricky gotchas (Prolog escaping, FFI overhead, cross-platform paths), document them prominently.

Put the manual at the repository root next to `README.md`. Update it when you change architecture, not when you change every line.
