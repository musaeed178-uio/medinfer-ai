# SPDX-License-Identifier: AGPL-3.0-or-later
"""Shared pytest fixtures.

Tests import the project's top-level modules, so the project root is put on
``sys.path`` here (tests/ has no __init__.py).
"""

import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kb_catalog import KBCatalog  # noqa: E402


@pytest.fixture(scope="session")
def catalog() -> KBCatalog:
    return KBCatalog.load()


@pytest.fixture(scope="session")
def controller():
    """A live engine (SWI-Prolog). Tests using it skip when unavailable."""
    pytest.importorskip("pyswip")
    if shutil.which("swipl") is None:
        pytest.skip("SWI-Prolog (swipl) is not on PATH")
    from controller import MedicalController
    return MedicalController()
