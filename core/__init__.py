# SPDX-License-Identifier: AGPL-3.0-or-later
"""Domain layer: reusable core that presentation layers consume.

The core exposes :class:`DiagnosisManager` as the main orchestration service.
Presentation adapters (GUI, CLI) instantiate it via the composition root
(:func:`bootstrap.create_manager`) and call its methods — they never import
from ``gui`` or ``controller`` directly.
"""

from core.manager import DiagnosisManager
from core.models import DiagnosisSession, SymptomSelection

__all__ = ["DiagnosisManager", "DiagnosisSession", "SymptomSelection"]
