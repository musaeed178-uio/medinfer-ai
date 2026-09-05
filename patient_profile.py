# SPDX-License-Identifier: AGPL-3.0-or-later
"""Patient profiles and diagnosis history stored as JSON in ./data.

The schema is append-only: new keys may be added to history entries, but
existing keys (timestamp, symptoms, results, top_disease, confidence) are
never removed, so files written by older versions keep loading.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional

from kb_catalog import age_band


class PatientProfile:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.profiles_path = os.path.join(self.data_dir, "saved_profiles.json")
        self.history_path = os.path.join(self.data_dir, "diagnosis_history.json")
        self.saved_profiles: list[dict[str, Any]] = self._load_profiles()
        self.current_profile: dict[str, Any] = (
            self.saved_profiles[0] if self.saved_profiles else self._create_default_profile()
        )
        self.history: list[dict[str, Any]] = self._load_history()

    # ------------------------------------------------------------------
    # Profile persistence
    # ------------------------------------------------------------------
    def _create_default_profile(self) -> dict[str, Any]:
        return {
            "name": "",
            "age": 0,
            "gender": "Other",
            "blood_type": "Unknown",
            "phone": "",
            "email": "",
            "created_at": datetime.now().isoformat(),
        }

    def _load_profiles(self) -> list[dict[str, Any]]:
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_profiles(self) -> None:
        with open(self.profiles_path, "w", encoding="utf-8") as f:
            json.dump(self.saved_profiles, f, ensure_ascii=False, indent=2)

    def save_current_profile(self) -> None:
        # Update or add current profile.
        name = self.current_profile.get("name", "").strip()
        if not name:
            name = f"Patient_{len(self.saved_profiles) + 1}"
            self.current_profile["name"] = name

        # Check if a profile with this name already exists.
        for i, profile in enumerate(self.saved_profiles):
            if profile.get("name") == name:
                self.saved_profiles[i] = self.current_profile
                self._save_profiles()
                return
        self.saved_profiles.append(self.current_profile)
        self._save_profiles()

    def get_current_profile(self) -> dict[str, Any]:
        return self.current_profile.copy()

    def get_saved_profiles(self) -> list[dict[str, Any]]:
        return self.saved_profiles.copy()

    def load_profile(self, index: int) -> bool:
        if 0 <= index < len(self.saved_profiles):
            self.current_profile = self.saved_profiles[index].copy()
            return True
        return False

    def delete_profile(self, index: int) -> bool:
        if 0 <= index < len(self.saved_profiles):
            self.saved_profiles.pop(index)
            self._save_profiles()
            if not self.saved_profiles:
                self.current_profile = self._create_default_profile()
            elif index >= len(self.saved_profiles):
                self.current_profile = self.saved_profiles[-1].copy()
            else:
                self.current_profile = self.saved_profiles[index].copy()
            return True
        return False

    # ------------------------------------------------------------------
    # Diagnosis history
    # ------------------------------------------------------------------
    def add_diagnosis(
        self,
        symptoms: list[str],
        results: list[dict[str, Any]],
        top_disease: str,
        confidence: int,
        extras: Optional[dict[str, Any]] = None,
    ) -> None:
        """Record a diagnosis; ``extras`` may hold severities/temperature/..."""
        entry: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": list(symptoms),
            "results": results,
            "top_disease": top_disease,
            "confidence": confidence,
        }
        if extras:
            entry.update(extras)
        self.history.insert(0, entry)
        self._save_history()

    def _save_history(self) -> None:
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def _load_history(self) -> list[dict[str, Any]]:
        if os.path.exists(self.history_path):
            with open(self.history_path, encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        return self.history[:limit]

    def clear_history(self) -> None:
        self.history = []
        self._save_history()

    # ------------------------------------------------------------------
    # Statistics and risk
    # ------------------------------------------------------------------
    def get_statistics(self) -> dict[str, Any]:
        if not self.history:
            return {
                "total_diagnoses": 0,
                "most_common_disease": "N/A",
                "average_confidence": 0,
                "recent_symptoms": [],
            }

        disease_counts: dict[str, int] = {}
        total_confidence = 0
        all_symptoms: list[str] = []
        for entry in self.history:
            disease = entry.get("top_disease", "")
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
            total_confidence += entry.get("confidence", 0)
            all_symptoms.extend(entry.get("symptoms", []))

        most_common = max(disease_counts, key=disease_counts.get) if disease_counts else "N/A"
        avg_confidence = round(total_confidence / len(self.history), 1)

        symptom_counts: dict[str, int] = {}
        for s in all_symptoms:
            symptom_counts[s] = symptom_counts.get(s, 0) + 1
        recent_symptoms = sorted(symptom_counts, key=symptom_counts.get, reverse=True)[:10]

        return {
            "total_diagnoses": len(self.history),
            "most_common_disease": most_common,
            "average_confidence": avg_confidence,
            "recent_symptoms": recent_symptoms,
            "disease_distribution": disease_counts,
        }

    def get_risk_factors(self) -> list[str]:
        """Age bands the current profile belongs to (see kb_catalog.age_band)."""
        band = age_band(self.current_profile.get("age", 0))
        return [band] if band else []
