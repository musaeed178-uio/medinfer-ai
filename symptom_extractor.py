# SPDX-License-Identifier: AGPL-3.0-or-later
"""Free-text symptom extraction used by the GUI's natural-language input.

Pure Python on top of :class:`kb_catalog.KBCatalog`, so it can be unit-tested
without SWI-Prolog. It extracts:

* which symptoms the text mentions (multi-word phrases and aliases, with
  basic negation handling),
* a Mild/Moderate/Severe rating per symptom from nearby adjectives,
* durations ("for 2 days") attributed to the nearest symptom,
* a body temperature ("102 F", "a fever of 39").

Nothing here makes a diagnosis - it only turns prose into the same structured
symptom/severity input the checkbox GUI produces.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from kb_catalog import KBCatalog

SEVERE_WORDS = frozenset({
    "very", "severe", "extremely", "extreme", "intense", "terrible",
    "agonizing", "unbearable", "excruciating", "worst", "constant",
    "persistent", "high", "really", "badly",
})
MILD_WORDS = frozenset({
    "mild", "slight", "slightly", "minor", "low", "low-grade", "bit", "little",
})
NEGATION_WORDS = frozenset({
    "no", "not", "never", "without", "none", "longer",
    "don't", "dont", "doesn't", "doesnt", "didn't", "didnt", "won't", "wont",
})
# Words that end a negated clause ("no cough but fever" must keep fever).
# Punctuation is kept in the normalized text as its own token so it acts as
# a hard boundary for both negation and severity attribution.
CLAUSE_BOUNDS = frozenset({
    ",", ".", ";", "but", "and", "yet", "however", "while",
    "although", "though", "whereas", "then", "so", "also",
})

_WORD_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "couple": 2, "few": 3,
}
_DURATION_UNITS = {
    "day": "day", "days": "day", "week": "week", "weeks": "week",
    "month": "month", "months": "month", "hour": "hour", "hours": "hour",
    "hr": "hour", "hrs": "hour", "year": "year", "years": "year",
}

_NUM_RE = r"(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a couple of|a few|several)"


@dataclass
class ExtractionResult:
    """Structured output of :meth:`SymptomExtractor.extract`."""

    symptom_ids: list[str] = field(default_factory=list)
    severities: dict[str, str] = field(default_factory=dict)
    durations: dict[str, str] = field(default_factory=dict)
    duration_notes: list[str] = field(default_factory=list)
    temperature_c: Optional[float] = None
    temperature_raw: Optional[str] = None

    def has_any(self) -> bool:
        return bool(self.symptom_ids)


def _normalize(text: str) -> str:
    """Lowercase; keep letters/digits/apostrophes and . , ; as word boundaries."""
    text = text.lower().replace("°", " degrees ")
    text = re.sub(r"[^a-z0-9'.,;]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _token_pattern(token: str) -> str:
    return re.escape(token) + r"(?:s|es|ed|ing)?"


def _phrase_regex(phrase: str) -> re.Pattern:
    body = r"\s+".join(_token_pattern(t) for t in phrase.split())
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")


def _classify_severity(context_words: list[str]) -> str:
    words = set(w.strip("'") for w in context_words)
    if words & SEVERE_WORDS:
        return "severe"
    if words & MILD_WORDS:
        return "mild"
    return "moderate"


def _token_index(norm: str, char_pos: int) -> int:
    return len(norm[:char_pos].split())


class SymptomExtractor:
    """Match symptoms (with aliases), severities, durations and temperature."""

    def __init__(self, catalog: KBCatalog):
        self.catalog = catalog
        # symptom_id -> list of (regex, display phrase), primary first.
        self._matchers: dict[str, list[tuple[re.Pattern, str]]] = {}
        for symptom_id, phrases in catalog.symptom_phrases().items():
            self._matchers[symptom_id] = [
                (_phrase_regex(p), p) for p in phrases if p.strip()
            ]

    # ------------------------------------------------------------------
    def extract(self, text: str) -> ExtractionResult:
        norm = _normalize(text)
        result = ExtractionResult()
        if not norm:
            return result

        tokens = norm.split()

        # Temperature is parsed even when no symptom phrase matched
        # (e.g. "my temperature is 102" should still be captured).
        result.temperature_c, result.temperature_raw = self._find_temperature(norm)

        # 1) which symptoms are mentioned (aliases + negation aware)
        matched: list[tuple[str, int, int]] = []
        for symptom_id, matchers in self._matchers.items():
            for regex, _phrase in matchers:
                hit = None
                for m in regex.finditer(norm):
                    if not self._is_negated(tokens, norm, m.start()):
                        hit = m
                        break
                if hit is not None:
                    matched.append((symptom_id, hit.start(), hit.end()))
                    break

        if not matched:
            return result

        matched.sort(key=lambda t: t[1])

        # 2) severity per matched symptom (unique ids in text order).
        # Adjectives only count when they sit in the same clause as the
        # symptom and do not describe an earlier symptom.
        matched_token_starts = {_token_index(norm, s) for _sid, s, _e in matched}
        seen: set[str] = set()
        ordered: list[str] = []
        for symptom_id, start, _end in matched:
            if symptom_id in seen:
                continue
            seen.add(symptom_id)
            ordered.append(symptom_id)
            k = _token_index(norm, start)
            context: list[str] = []
            j = k - 1
            while j >= 0 and len(context) < 4:
                token = tokens[j]
                if token in CLAUSE_BOUNDS or j in matched_token_starts:
                    break
                context.append(token)
                j -= 1
            if k < len(tokens):
                context.append(tokens[k])
            result.severities[symptom_id] = _classify_severity(context)
        result.symptom_ids = ordered

        # 3) durations -> nearest preceding symptom
        idx = 0
        for pos, label in self._find_durations(norm):
            while idx < len(matched) - 1 and matched[idx + 1][1] <= pos:
                idx += 1
            owner, start, _end = matched[idx]
            if start <= pos:
                result.durations.setdefault(owner, label)
            elif label not in result.duration_notes:
                result.duration_notes.append(label)

        return result

    @staticmethod
    def _is_negated(tokens: list[str], norm: str, start: int) -> bool:
        """True when the phrase at ``start`` sits inside a negated clause."""
        k = _token_index(norm, start)
        for j in range(k - 1, max(-1, k - 5), -1):
            token = tokens[j].strip("'")
            if token in NEGATION_WORDS:
                return True
            if token in CLAUSE_BOUNDS:
                break
        return False

    @staticmethod
    def _find_durations(norm: str) -> list[tuple[int, str]]:
        pattern = re.compile(
            r"\b" + _NUM_RE + r"\s*(?:-|–|to)?\s*"
            r"(days?|weeks?|months?|hours?|hrs?|years?)\b")
        out: list[tuple[int, str]] = []
        for m in pattern.finditer(norm):
            amount_tok = m.group(1)
            unit_raw = m.group(2).lower()
            if amount_tok.isdigit():
                amount = amount_tok
            elif amount_tok in _WORD_NUM:
                amount = str(_WORD_NUM[amount_tok])
            else:  # "a couple of", "a few", "several"
                amount = amount_tok
            unit = _DURATION_UNITS.get(unit_raw, unit_raw.rstrip("s"))
            out.append((m.start(), f"{amount} {unit}"))
        out.sort(key=lambda t: t[0])
        return out

    @staticmethod
    def _find_temperature(norm: str) -> tuple[Optional[float], Optional[str]]:
        number = r"\d{2,3}(?:\.\d+)?"
        explicit = re.compile(
            r"\b(" + number + r")\s*(?:degrees?|deg)?\s*([fc]|fahrenheit|celsius)\b")
        keyed = re.compile(
            r"\b(?:temperature|temp|fever)(?:s|ed|ing)?\s+"
            r"(?:of|is|at|reading|around|about|was|:)?\s*"
            r"(" + number + r")\s*(?:degrees?|deg)?\s*([fc]|fahrenheit|celsius)?\b")

        def to_celsius(value: float, unit: Optional[str]) -> Optional[float]:
            if unit and unit.startswith("f"):
                return round((value - 32) * 5 / 9, 1)
            if unit and unit.startswith("c"):
                return round(value, 1)
            if 95.0 <= value <= 112.0:    # no unit: typical Fahrenheit fever range
                return round((value - 32) * 5 / 9, 1)
            if 33.0 <= value <= 45.0:     # or Celsius
                return round(value, 1)
            return None

        for m in explicit.finditer(norm):
            value, unit = float(m.group(1)), m.group(2).lower()
            c = to_celsius(value, unit)
            if c is not None:
                return c, norm[m.start():m.end()]
        for m in keyed.finditer(norm):
            value, unit = float(m.group(1)), (m.group(2) or "").lower() or None
            c = to_celsius(value, unit)
            if c is not None:
                return c, norm[m.start():m.end()]
        return None, None
