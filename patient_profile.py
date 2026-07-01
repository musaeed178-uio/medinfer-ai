import json
import os
from datetime import datetime


class PatientProfile:
    def __init__(self, data_dir=None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.profiles_path = os.path.join(self.data_dir, "saved_profiles.json")
        self.history_path = os.path.join(self.data_dir, "diagnosis_history.json")
        self.saved_profiles = self._load_profiles()
        self.current_profile = self.saved_profiles[0] if self.saved_profiles else self._create_default_profile()
        self.history = self._load_history()

    def _create_default_profile(self):
        return {
            "name": "",
            "age": 0,
            "gender": "Other",
            "blood_type": "Unknown",
            "phone": "",
            "email": "",
            "created_at": datetime.now().isoformat(),
        }

    def _load_profiles(self):
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, "r") as f:
                return json.load(f)
        return []

    def _save_profiles(self):
        with open(self.profiles_path, "w") as f:
            json.dump(self.saved_profiles, f, indent=2)

    def _load_history(self):
        if os.path.exists(self.history_path):
            with open(self.history_path, "r") as f:
                return json.load(f)
        return []

    def save_current_profile(self):
        # Update or add current profile
        name = self.current_profile.get("name", "").strip()
        if not name:
            name = f"Patient_{len(self.saved_profiles) + 1}"
            self.current_profile["name"] = name

        # Check if profile already exists by name
        for i, p in enumerate(self.saved_profiles):
            if p.get("name") == name:
                self.saved_profiles[i] = self.current_profile
                self._save_profiles()
                return
        self.saved_profiles.append(self.current_profile)
        self._save_profiles()

    def get_current_profile(self):
        return self.current_profile.copy()

    def get_saved_profiles(self):
        return self.saved_profiles.copy()

    def load_profile(self, index):
        if 0 <= index < len(self.saved_profiles):
            self.current_profile = self.saved_profiles[index].copy()
            return True
        return False

    def delete_profile(self, index):
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

    def add_diagnosis(self, symptoms, results, top_disease, confidence):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms,
            "results": results,
            "top_disease": top_disease,
            "confidence": confidence,
        }
        self.history.insert(0, entry)
        self._save_history()

    def _save_history(self):
        with open(self.history_path, "w") as f:
            json.dump(self.history, f, indent=2)

    def get_history(self, limit=50):
        return self.history[:limit]

    def clear_history(self):
        self.history = []
        self._save_history()

    def get_statistics(self):
        if not self.history:
            return {
                "total_diagnoses": 0,
                "most_common_disease": "N/A",
                "average_confidence": 0,
                "recent_symptoms": [],
            }

        disease_counts = {}
        total_confidence = 0
        all_symptoms = []

        for entry in self.history:
            disease = entry.get("top_disease", "")
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
            total_confidence += entry.get("confidence", 0)
            all_symptoms.extend(entry.get("symptoms", []))

        most_common = max(disease_counts, key=disease_counts.get) if disease_counts else "N/A"
        avg_confidence = round(total_confidence / len(self.history), 1) if self.history else 0

        symptom_counts = {}
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

    def get_risk_factors(self):
        age = self.current_profile.get("age", 0)
        gender = self.current_profile.get("gender", "")
        risks = []

        if age < 5:
            risks.append("child")
        elif 5 <= age < 18:
            risks.append("adolescent")
        elif 18 <= age < 40:
            risks.append("adult")
        elif 40 <= age < 65:
            risks.append("middle_aged")
        else:
            risks.append("elderly")

        return risks
