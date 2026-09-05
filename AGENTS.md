# AGENTS.md — Non-obvious learnings for future sessions

## Architecture

- **Layered architecture**: `core/manager.py` (DiagnosisManager) is the domain service. `gui.py` is a thin adapter that receives it via constructor injection. `bootstrap.py` is the composition root — the only place that wires `MedicalController`, `PatientProfile`, `ReportExporter`. Never instantiate these directly in GUI or tests.
- **Entry point**: `__main__.py` calls `bootstrap.create_manager()` then passes it to `ModernMedicalGUI(manager=manager)`. The GUI no longer creates its own dependencies.

## Build & generation

- **KB pipeline is `kb_catalog.json` → `generate_kb.py` → `medical_kb.pl`**. Edit the JSON, run `python generate_kb.py`, then the Prolog file is regenerated. Never hand-edit the generated facts block in `medical_kb.pl`.
- **Prolog string escaping**: `generate_kb.py` uses `_prolog_str()` to escape single quotes in descriptions/recommendations. Apostrophes in disease descriptions (e.g. "Parkinson's disease") will cause Prolog syntax errors if not escaped. The errors manifest as `Syntax error: Operator expected` at seemingly random line numbers.

## Performance

- **Prolog FFI is the bottleneck, not Prolog itself**: pyswip's `query()` has ~50μs overhead per call from ctypes FFI + term parsing. Precompute static data in Python to avoid repeated round-trips. The disease-symptom graph is precomputed at `MedicalController.__init__()` time; confidence is calculated in Python during `diagnose()`.
- **`_SEV_FACTOR` in `controller.py` must match Prolog's `severity_factor` rules**. If you change one, change the other.

## Testing

- **Controller tests require SWI-Prolog on PATH**. `tests/conftest.py` uses `pytest.importorskip("pyswip")` and `shutil.which("swipl")` — if either is missing, controller tests are skipped automatically.
- **KB validation rule**: `kb_catalog.py`'s `validate()` requires every symptom to be used by at least one disease. Adding a new symptom without assigning it to a disease will fail `test_every_symptom_used_by_a_disease`.
- **`test_committed_kb_is_up_to_date`** checks that `medical_kb.pl` matches what `generate_kb.py` would produce. Run `python generate_kb.py` after editing `kb_catalog.json` or this test fails.

## GUI specifics

- **Color constants are centralized** at the top of `gui.py` (`BG_BASE`, `ACCENT_BLUE`, etc.). Use these, not hardcoded hex values.
- **Session persistence**: `patient_profile.py` writes `data/session.json` to remember the last active profile across restarts. On startup, `_load_session()` restores it. If the session file is corrupt or missing, it falls back to guest mode.
- **NLP clearing bug was fixed**: `_analyze_nlp()` now clears all previous symptom selections before analyzing new text. Without this, stale symptoms from a prior statement persist.

## Platform

- **Windows paths**: The project runs on Windows. `resource_path()` in `kb_catalog.py` handles both normal and PyInstaller paths. Tests use `tmp_path` fixture for isolation.
