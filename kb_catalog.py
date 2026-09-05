# SPDX-License-Identifier: AGPL-3.0-or-later
"""Typed access to kb_catalog.json - the single source of truth.

The GUI layout, the natural-language extractor and the age-risk adjustment
all read from :class:`KBCatalog`. The Prolog facts in medical_kb.pl are
generated from the same file by generate_kb.py, so catalog and engine can
never silently drift apart (a pytest guards this).
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))


def resource_path(name: str) -> str:
    """Locate a bundled data file, also when running from a PyInstaller build."""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, name)
    return os.path.join(HERE, name)


DEFAULT_CATALOG_PATH = resource_path("kb_catalog.json")

AGE_BANDS = ("child", "adolescent", "adult", "middle_aged", "elderly")


def humanize(token: str) -> str:
    """Convert a snake_case token to a human title ('chest_pain' -> 'Chest Pain')."""
    return token.replace("_", " ").title()


def age_band(age: int | None) -> str | None:
    """Map an age (years) to one of the KB age bands, or None if unknown."""
    if not age or age < 0:
        return None
    if age < 5:
        return "child"
    if age < 18:
        return "adolescent"
    if age < 40:
        return "adult"
    if age < 65:
        return "middle_aged"
    return "elderly"


@dataclass(frozen=True)
class SymptomDef:
    """One selectable symptom."""

    symptom_id: str
    body_system: str
    aliases: tuple[str, ...] = ()
    red_flag: bool = False

    @property
    def name(self) -> str:
        return humanize(self.symptom_id)


@dataclass(frozen=True)
class DiseaseDef:
    """One disease with the metadata the GUI and reasoning need."""

    disease_id: str
    category: str
    description: str
    recommendation: str
    emergency: bool
    symptoms: tuple[str, ...]
    weights: dict[str, float] = field(default_factory=dict)
    risk_factors: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return humanize(self.disease_id)

    def weight(self, symptom: str) -> float:
        return self.weights.get(symptom, 1.0)

    def age_risk_bands(self) -> tuple[str, ...]:
        return self.risk_factors.get("age", ())


@dataclass(frozen=True)
class DiagnosisResult:
    """One candidate diagnosis returned by the reasoning engine."""

    disease: str
    confidence: int          # final score, including the age-risk adjustment
    base_confidence: int     # engine score before the age-risk adjustment
    matched: int
    total: int
    category: str
    emergency: bool
    risk_note: str | None = None

    @property
    def name(self) -> str:
        return humanize(self.disease)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class KBCatalog:
    """Loaded, validated access to the knowledge catalog."""

    def __init__(self, data: dict[str, Any]):
        meta = data.get("_meta", {})
        self.version: str = str(meta.get("version", "?"))
        self.name: str = str(meta.get("name", "Knowledge base"))

        self._body_order: list[str] = []
        self.symptoms: dict[str, SymptomDef] = {}
        for system, block in data.get("body_systems", {}).items():
            self._body_order.append(system)
            for symptom_id, entry in block.get("symptoms", {}).items():
                self.symptoms[symptom_id] = SymptomDef(
                    symptom_id=symptom_id,
                    body_system=system,
                    aliases=tuple(entry.get("aliases", [])),
                    red_flag=bool(entry.get("red_flag", False)),
                )

        self.diseases: dict[str, DiseaseDef] = {}
        for disease_id, entry in data.get("diseases", {}).items():
            self.diseases[disease_id] = DiseaseDef(
                disease_id=disease_id,
                category=entry["category"],
                description=entry["description"],
                recommendation=entry["recommendation"],
                emergency=bool(entry["emergency"]),
                symptoms=tuple(entry["symptoms"]),
                weights=dict(entry.get("weights", {})),
                risk_factors={
                    kind: tuple(bands)
                    for kind, bands in entry.get("risk_factors", {}).items()
                },
            )

    @classmethod
    def load(cls, path: str = DEFAULT_CATALOG_PATH) -> "KBCatalog":
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    # ---- ordering helpers ------------------------------------------------
    @property
    def body_systems(self) -> list[str]:
        return list(self._body_order)

    def symptoms_by_system(self) -> list[tuple[str, list[str]]]:
        """[(body_system, [symptom_id, ...]), ...] in catalog order."""
        out: list[tuple[str, list[str]]] = []
        for system in self._body_order:
            out.append((system, [s for s, d in self.symptoms.items() if d.body_system == system]))
        return out

    def red_flag_symptoms(self) -> set[str]:
        return {s for s, d in self.symptoms.items() if d.red_flag}

    def symptom_phrases(self) -> dict[str, tuple[str, ...]]:
        """symptom_id -> (primary phrase, *alias phrases) using plain words."""
        phrases: dict[str, tuple[str, ...]] = {}
        for symptom_id, sym in self.symptoms.items():
            phrases[symptom_id] = (sym.symptom_id.replace("_", " "),) + tuple(sym.aliases)
        return phrases

    # ---- validation --------------------------------------------------------
    def validate(self) -> list[str]:
        """Return a list of consistency problems (empty when the catalog is sound)."""
        problems: list[str] = []
        symptom_ids = set(self.symptoms)
        disease_ids = set(self.diseases)
        used: set[str] = set()
        for disease_id, disease in self.diseases.items():
            for symptom in disease.symptoms:
                used.add(symptom)
                if symptom not in symptom_ids:
                    problems.append(f"{disease_id}: unknown symptom '{symptom}'")
            for symptom, weight in disease.weights.items():
                if symptom not in disease.symptoms:
                    problems.append(f"{disease_id}: weight for non-symptom '{symptom}'")
                if not isinstance(weight, (int, float)) or weight <= 0:
                    problems.append(f"{disease_id}: bad weight for '{symptom}': {weight!r}")
            for band in disease.age_risk_bands():
                if band not in AGE_BANDS:
                    problems.append(f"{disease_id}: unknown age band '{band}'")
        unused = [s for s in symptom_ids if s not in used]
        if unused:
            problems.append("symptoms not used by any disease: " + ", ".join(sorted(unused)))
        return problems
