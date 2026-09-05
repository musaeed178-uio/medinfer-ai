# SPDX-License-Identifier: AGPL-3.0-or-later
"""Composition root — the ONLY place where the object graph is wired.

Every entry point (GUI, CLI, tests) calls :func:`create_manager` to get
a fully-initialised :class:`core.DiagnosisManager`.  Presentation layers
never instantiate controllers, extractors, or patient profiles directly.

See the ``building-multi-ui-apps`` skill for the architectural rationale:
dependencies flow downward, the core never imports from presentation, and
the composition root is the single place to understand the object graph.
"""

from __future__ import annotations

from typing import Optional

from controller import MedicalController, MedicalEngineError
from patient_profile import PatientProfile
from report_exporter import ReportExporter

from core.manager import DiagnosisManager


def create_manager(
    patient: Optional[PatientProfile] = None,
) -> DiagnosisManager:
    """Build and return a fully-wired DiagnosisManager.

    Parameters
    ----------
    patient :
        An existing PatientProfile to use (e.g. from tests).
        If ``None``, a fresh one is created with default data directory.

    Raises
    ------
    MedicalEngineError
        If the SWI-Prolog engine cannot be started.
    """
    controller = MedicalController()
    profile = patient or PatientProfile()
    exporter = ReportExporter()
    return DiagnosisManager(
        controller=controller,
        patient=profile,
        exporter=exporter,
    )
