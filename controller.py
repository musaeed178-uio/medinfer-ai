import os
from pyswip import Prolog


class MedicalController:
    def __init__(self):
        self.prolog = Prolog()
        kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medical_kb.pl")
        self.prolog.consult(kb_path)

    def get_all_symptoms(self):
        results = list(self.prolog.query("get_all_symptoms(S)"))
        if results:
            return results[0]["S"]
        return []

    def get_all_diseases(self):
        results = list(self.prolog.query("get_all_diseases(D)"))
        if results:
            return results[0]["D"]
        return []

    def get_disease_symptoms(self, disease):
        results = list(self.prolog.query(f"get_disease_symptoms('{disease}', S)"))
        if results:
            return results[0]["S"]
        return []

    def get_disease_info(self, disease):
        desc_results = list(self.prolog.query(f"description({disease}, D)"))
        cat_results = list(self.prolog.query(f"category({disease}, C)"))
        rec_results = list(self.prolog.query(f"recommendation({disease}, R)"))
        emerg_results = list(self.prolog.query(f"is_emergency({disease})"))

        desc = str(desc_results[0]["D"]) if desc_results else "No description available."
        cat = str(cat_results[0]["C"]) if cat_results else "unknown"
        rec = str(rec_results[0]["R"]) if rec_results else "Consult a healthcare professional."
        is_emerg = len(emerg_results) > 0

        return {
            "name": disease,
            "description": desc,
            "category": cat,
            "recommendation": rec,
            "is_emergency": is_emerg,
        }

    def get_all_categories(self):
        results = list(self.prolog.query("all_categories(C)"))
        if results:
            return results[0]["C"]
        return []

    def get_diseases_by_category(self, category):
        results = list(self.prolog.query(f"diseases_by_category('{category}', D)"))
        if results:
            return results[0]["D"]
        return []

    def diagnose(self, selected_symptoms):
        if not selected_symptoms:
            return []

        self.prolog.retractall("patient_has(_)")

        symptoms_str = ",".join(selected_symptoms)
        for s in selected_symptoms:
            self.prolog.assertz(f"patient_has({s})")

        diseases = list(self.prolog.query(f"possible_disease(D, [{symptoms_str}])"))
        disease_names = [str(sol["D"]) for sol in diseases]

        results = []
        for disease in disease_names:
            conf_sol = list(self.prolog.query(f"confidence({disease}, [{symptoms_str}], C)"))
            match_sol = list(self.prolog.query(f"matched_symptoms({disease}, [{symptoms_str}], M)"))
            total_sol = list(self.prolog.query(f"total_symptoms({disease}, T)"))

            conf = int(conf_sol[0]["C"]) if conf_sol else 0
            matched = int(match_sol[0]["M"]) if match_sol else 0
            total = int(total_sol[0]["T"]) if total_sol else 0

            results.append({
                "disease": disease,
                "confidence": conf,
                "matched": matched,
                "total": total,
            })

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results

    def get_explanation(self, disease, selected_symptoms):
        matched = []
        missing = []
        kb_symptoms = self.get_disease_symptoms(disease)

        for s in kb_symptoms:
            s_str = str(s)
            if s_str in selected_symptoms:
                matched.append(s_str)
            else:
                missing.append(s_str)

        symptoms_str = ",".join(selected_symptoms)
        conf_result = list(self.prolog.query(f"confidence({disease}, [{symptoms_str}], C)"))
        conf = conf_result[0]["C"] if conf_result else 0

        explanation = (
            f"Possible Diagnosis: {disease.replace('_', ' ').title()}\n"
            f"Confidence: {conf}%\n"
            f"Matched Symptoms: {', '.join(matched)}\n"
            f"Missing Symptoms: {', '.join(missing)}"
        )
        return explanation

    def forward_chain(self, selected_symptoms):
        if not selected_symptoms:
            return []

        symptoms_str = ",".join(selected_symptoms)
        results = []
        for sol in self.prolog.query(f"forward_chain([{symptoms_str}], Conclusions)"):
            raw = sol["Conclusions"]
            for item in raw:
                item_str = str(item)
                parts = item_str.strip("()").split(",")
                disease = parts[0].strip()
                conf = int(parts[1].strip())
                results.append({"disease": disease, "confidence": conf})

        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results

    def verify_disease(self, disease, selected_symptoms):
        symptoms_str = ",".join(selected_symptoms)
        result = list(self.prolog.query(f"verify_disease({disease}, [{symptoms_str}])"))
        return len(result) > 0

    def search_symptoms(self, query):
        all_symptoms = self.get_all_symptoms()
        query_lower = query.lower()
        return [s for s in all_symptoms if query_lower in s.replace("_", " ").lower()]

    def search_diseases(self, query):
        all_diseases = self.get_all_diseases()
        query_lower = query.lower()
        return [d for d in all_diseases if query_lower in d.replace("_", " ").lower()]

    def get_symptom_category_map(self):
        body_systems = {
            "General": ["fever", "fatigue", "chills", "sweating", "weight_loss", "loss_of_appetite"],
            "Respiratory": ["cough", "shortness_of_breath", "sore_throat", "wheezing", "runny_nose", "nasal_congestion", "sneezing", "coughing_blood"],
            "Neurological": ["headache", "dizziness", "blurred_vision", "sensitivity_to_light", "confusion", "insomnia", "difficulty_concentrating"],
            "Gastrointestinal": ["nausea", "vomiting", "diarrhea", "abdominal_pain", "bloating"],
            "Musculoskeletal": ["body_ache", "joint_pain", "muscle_pain", "back_pain", "stiff_joints", "stiff_neck"],
            "Skin": ["rash", "pale_skin", "yellowing_of_skin", "skin_rash"],
            "Cardiovascular": ["chest_pain", "rapid_heartbeat", "cold_hands_and_feet"],
            "Urinary": ["frequent_urination", "burning_urination", "blood_in_urine"],
            "Psychological": ["sadness", "loss_of_interest"],
            "ENT": ["itchy_eyes", "red_eyes", "swollen_glands", "facial_pain"],
            "Other": ["increased_thirst"],
        }
        return body_systems

    def cleanup(self):
        self.prolog.retractall("patient_has(_)")
