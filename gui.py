import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from controller import MedicalController
from patient_profile import PatientProfile
from report_exporter import ReportExporter
import threading
import re
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ModernMedicalGUI:
    def __init__(self):
        self.controller = MedicalController()
        self.patient = PatientProfile()
        self.exporter = ReportExporter()
        self.selected_symptoms = {}
        self.current_results = []
        self.symptom_widgets = {}
        self.all_symptom_data = []

        self.root = ctk.CTk()
        self.root.title("MedInfer AI - Medical Diagnosis System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(fg_color="#0f1115")

        self._build_layout()
        self._load_symptoms()
        self._update_patient_label()

    def _build_layout(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=16, fg_color="#161922")
        self.sidebar.pack(side="left", fill="y", padx=(0, 12), pady=0)
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True)

        self.frames = {}
        self._build_dashboard()
        self._build_disease_info()
        self._build_history()
        self._build_profile()

        self.show_frame("dashboard")

    def _build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="🏥 MedInfer AI", font=("Segoe UI", 24, "bold"), text_color="#00d4ff").pack(pady=25)

        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("📖 Disease Info", "disease_info"),
            ("📜 History", "history"),
            ("👤 Patient Profile", "profile")
        ]
        self.nav_buttons = {}
        for text, key in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", hover_color="#2a2d3e",
                                font=("Segoe UI", 15), anchor="w", height=48, corner_radius=10,
                                command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[key] = btn

        ctk.CTkLabel(self.sidebar, text="v2.0 | AI Expert System", text_color="#555", font=("Segoe UI", 10)).pack(side="bottom", pady=(0, 10))

    def show_frame(self, frame_name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color="#2a2d3e" if k == frame_name else "transparent")

    def _build_dashboard(self):
        dash = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["dashboard"] = dash
        
        dash.grid_columnconfigure(0, weight=1)
        dash.grid_columnconfigure(1, weight=1)
        dash.grid_rowconfigure(0, weight=0)
        dash.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(dash, fg_color="#161922", corner_radius=12, height=65)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        top_bar.grid_columnconfigure(0, weight=1)

        self.patient_label = ctk.CTkLabel(top_bar, text="Patient: Guest", font=("Segoe UI", 16, "bold"), text_color="#e0e0e0")
        self.patient_label.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        ctk.CTkButton(top_bar, text="📤 Export Report", command=self._export_report, fg_color="#2a2d3e", width=130).grid(row=0, column=1, sticky="e", padx=15, pady=15)

        self.symptom_panel = self._create_scrollable_panel(dash, "Symptom Input & Selection", 1, 0)
        
        self.right_panel = ctk.CTkFrame(dash, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.diag_panel = self._create_scrollable_panel(self.right_panel, "Differential Diagnosis", 0, 0)
        
        self.exp_panel = ctk.CTkFrame(self.right_panel, corner_radius=12, fg_color="#161922")
        self.exp_panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        ctk.CTkLabel(self.exp_panel, text="🤖 AI Reasoning Engine", font=("Segoe UI", 14, "bold"), text_color="#00d4ff").pack(anchor="w", padx=15, pady=(12, 5))
        self.exp_text = ctk.CTkTextbox(self.exp_panel, font=("Segoe UI", 12), wrap="word", fg_color="#1e212b", text_color="#d0d0d0")
        self.exp_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self._build_symptom_controls()

    def _create_scrollable_panel(self, parent, title, row, col):
        panel = ctk.CTkScrollableFrame(parent, label_text=title, corner_radius=12, fg_color="#161922")
        panel.grid(row=row, column=col, sticky="nsew")
        return panel

    def _build_symptom_controls(self):
        self.nlp_frame = ctk.CTkFrame(self.symptom_panel, fg_color="#1e212b", corner_radius=10)
        self.nlp_frame.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(self.nlp_frame, text="💬 Natural Language Input", font=("Segoe UI", 12, "bold"), text_color="#00d4ff").pack(anchor="w", padx=12, pady=(10, 5))
        
        self.nlp_entry = ctk.CTkTextbox(self.nlp_frame, height=50, font=("Segoe UI", 11), fg_color="#0f1115")
        self.nlp_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.nlp_entry.insert("0.0", "Example: I have a high fever, cough, and severe headache for 2 days...")
        
        nlp_btn_frame = ctk.CTkFrame(self.nlp_frame, fg_color="transparent")
        nlp_btn_frame.pack(fill="x", padx=12, pady=(0, 10))
        
        ctk.CTkButton(nlp_btn_frame, text="🔍 Analyze Text", command=self._analyze_nlp, width=120, fg_color="#00d4ff", text_color="#000", font=("Segoe UI", 11, "bold")).pack(side="left")
        
        self.nlp_feedback = ctk.CTkLabel(nlp_btn_frame, text="", font=("Segoe UI", 11), text_color="#00d4ff")
        self.nlp_feedback.pack(side="right")

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self._filter_symptoms)
        ctk.CTkEntry(self.symptom_panel, placeholder_text="🔍 Search symptoms...", textvariable=self.search_var, height=35, fg_color="#1e212b").pack(fill="x", pady=(0, 10))

        self.symptom_container = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.symptom_container.pack(fill="both", expand=True)

        self.action_frame = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=15)

        self.diagnose_btn = ctk.CTkButton(self.action_frame, text="🔍 Run Diagnosis", command=self._run_diagnosis, fg_color="#00d4ff", text_color="#000", font=("Segoe UI", 14, "bold"))
        self.diagnose_btn.pack(side="left", padx=5)
        ctk.CTkButton(self.action_frame, text="Clear All", command=self._clear_symptoms, fg_color="transparent", border_width=1, width=100).pack(side="left", padx=5)

        self.loading_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", width=150)
        self.loading_bar.pack(side="right", padx=10)

    def _build_symptom_list(self, data):
        for w in self.symptom_container.winfo_children():
            w.destroy()
        self.symptom_categories = {}
        grouped = {}
        for cat, sym in data:
            grouped.setdefault(cat, []).append(sym)

        for cat, symptoms in grouped.items():
            frame = ctk.CTkFrame(self.symptom_container, fg_color="transparent")
            frame.pack(fill="x", pady=(8, 4))
            ctk.CTkLabel(frame, text=f"🔹 {cat}", font=("Segoe UI", 12, "bold"), text_color="#00d4ff").pack(anchor="w", padx=5)
            
            grid = ctk.CTkFrame(frame, fg_color="transparent")
            grid.pack(fill="x", padx=10)
            self.symptom_categories[cat] = []
            
            for i, sym in enumerate(symptoms):
                r, c = divmod(i, 2)
                row_frame = ctk.CTkFrame(grid, fg_color="#1e212b", corner_radius=8)
                row_frame.grid(row=r, column=c, padx=4, pady=3, sticky="ew")

                var = ctk.BooleanVar(value=False)
                cb = ctk.CTkCheckBox(row_frame, text=sym.replace("_", " ").title(), variable=var, 
                                     command=lambda s=sym, v=var: self._on_symptom_toggle(s, v), font=("Segoe UI", 11))
                cb.pack(side="left", padx=8, pady=6)

                sev_var = ctk.StringVar(value="Moderate")
                menu = ctk.CTkOptionMenu(row_frame, values=["Mild", "Moderate", "Severe"], variable=sev_var, 
                                         width=95, height=26, fg_color="#2a2d3e", button_color="#3a3f5c",
                                         command=lambda v, s=sym: self._update_severity(s, v))
                menu.pack(side="right", padx=6, pady=6)
                menu.pack_forget()

                self.symptom_widgets[sym] = {"var": var, "sev": sev_var, "menu": menu}
                self.symptom_categories[cat].append(sym)
            grid.grid_columnconfigure(0, weight=1)
            grid.grid_columnconfigure(1, weight=1)

    def _on_symptom_toggle(self, symptom, var):
        menu = self.symptom_widgets[symptom]["menu"]
        if var.get():
            menu.pack(side="right", padx=6, pady=6)
            self.selected_symptoms[symptom] = menu.get()
        else:
            menu.pack_forget()
            self.selected_symptoms.pop(symptom, None)

    def _update_severity(self, symptom, value):
        self.selected_symptoms[symptom] = value

    def _analyze_nlp(self):
        text = self.nlp_entry.get("1.0", "end-1c").lower()
        if not text.strip() or "example" in text:
            self.nlp_feedback.configure(text="⚠️ Please enter your symptoms first")
            return
            
        words = re.findall(r'\b\w+\b', text)
        matched = set()
        for w in words:
            if len(w) < 3: continue
            for _, sym in self.all_symptom_data:
                if w in sym.replace("_", " ") or sym.replace("_", " ") in w:
                    matched.add(sym)
        
        if not matched:
            self.nlp_feedback.configure(text="❌ No matching symptoms found")
            return
            
        count = 0
        for sym in matched:
            if not self.symptom_widgets[sym]["var"].get():
                self.symptom_widgets[sym]["var"].set(True)
                self._on_symptom_toggle(sym, self.symptom_widgets[sym]["var"])
                count += 1
                
        self.nlp_feedback.configure(text=f"✅ Detected & selected {count} symptoms")
        self.root.after(3000, lambda: self.nlp_feedback.configure(text=""))

    def _run_diagnosis(self):
        if not self.selected_symptoms:
            messagebox.showwarning("No Symptoms", "Please select at least one symptom.")
            return
        self.loading_bar.start()
        self.diagnose_btn.configure(state="disabled")
        threading.Thread(target=self._diagnose_thread, args=(list(self.selected_symptoms.keys()),), daemon=True).start()

    def _diagnose_thread(self, symptoms_list):
        self.current_results = self.controller.diagnose(symptoms_list)
        self.root.after(0, self._update_results)

    def _update_results(self):
        self.loading_bar.stop()
        self.diagnose_btn.configure(state="normal")
        for w in self.diag_panel.winfo_children():
            w.destroy()

        if not self.current_results:
            ctk.CTkLabel(self.diag_panel, text="No matching diseases found. Try adding more symptoms.", font=("Segoe UI", 13), text_color="#888").pack(pady=30)
            self.exp_text.delete("1.0", "end")
            return

        for i, res in enumerate(self.current_results[:3]):
            self._create_diag_card(res, i+1)
        self._generate_explanation()

        profile = self.patient.get_current_profile()
        top = self.current_results[0]
        self.patient.add_diagnosis(list(self.selected_symptoms.keys()), self.current_results, top["disease"], top["confidence"])

    def _create_diag_card(self, res, rank):
        conf = res["confidence"]
        risk = "Low" if conf < 40 else ("Moderate" if conf < 70 else "Critical")
        color = "#2ecc71" if risk == "Low" else ("#f1c40f" if risk == "Moderate" else "#e74c3c")
        info = self.controller.get_disease_info(res["disease"])

        card = ctk.CTkFrame(self.diag_panel, fg_color="#1e212b", corner_radius=10, border_width=1, border_color="#333")
        card.pack(fill="x", pady=8, padx=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(header, text=f"#{rank} {res['disease'].replace('_', ' ').title()}", font=("Segoe UI", 14, "bold")).pack(side="left")
        
        if info.get("is_emergency"):
            ctk.CTkLabel(header, text="🚨 EMERGENCY", text_color="#e74c3c", font=("Segoe UI", 11, "bold"), fg_color="#2a1a1a").pack(side="right", padx=5)

        prog = ctk.CTkProgressBar(card, width=350, progress_color=color, fg_color="#2a2d3e")
        prog.pack(fill="x", padx=15, pady=(0, 4))
        prog.set(conf / 100)

        ctk.CTkLabel(card, text=f"Confidence: {conf}%  |  Risk: {risk}  |  Category: {info.get('category', 'N/A').title()}", font=("Segoe UI", 11), text_color="#aaa").pack(anchor="w", padx=15, pady=(0, 8))

    def _generate_explanation(self):
        if not self.current_results: return
        top = self.current_results[0]
        info = self.controller.get_disease_info(top["disease"])
        kb_symptoms = self.controller.get_disease_symptoms(top["disease"])
        matched = [s for s in self.selected_symptoms.keys() if s in kb_symptoms]
        missing = [s for s in kb_symptoms if s not in self.selected_symptoms]

        text = f"🔍 AI Analysis: {top['disease'].replace('_', ' ').title()}\n\n"
        text += f"Based on your inputs, the system identifies a {info['category']} condition. "
        text += f"The diagnosis leans toward this conclusion because {', '.join(matched[:3])} strongly align with typical clinical patterns for this disease.\n\n"
        text += f"📊 Confidence Score: {top['confidence']}% (Weighted Severity Adjusted)\n"
        text += f"⚠️ Missing Indicators: {', '.join(missing[:3]) if missing else 'None significant'}\n"
        text += f"💡 Recommendation: {info['recommendation']}"

        self.exp_text.delete("1.0", "end")
        self.exp_text.insert("1.0", text)

    def _clear_symptoms(self):
        for sym, w in self.symptom_widgets.items():
            w["var"].set(False)
            w["menu"].pack_forget()
        self.selected_symptoms.clear()
        for w in self.diag_panel.winfo_children():
            w.destroy()
        self.exp_text.delete("1.0", "end")
        self.nlp_entry.delete("1.0", "end")
        self.nlp_entry.insert("0.0", "Example: I have a high fever, cough, and severe headache for 2 days...")
        self.nlp_feedback.configure(text="")

    def _filter_symptoms(self, *args):
        query = self.search_var.get().lower()
        filtered = [(cat, sym) for cat, sym in self.all_symptom_data if query in sym.replace("_", " ")]
        self._build_symptom_list(filtered if query else self.all_symptom_data)

    def _load_symptoms(self):
        cat_map = self.controller.get_symptom_category_map()
        self.all_symptom_data = [(cat, sym) for cat, syms in cat_map.items() for sym in syms]
        self._build_symptom_list(self.all_symptom_data)

    # ================= DISEASE INFO PAGE =================
    def _build_disease_info(self):
        info_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["disease_info"] = info_frame
        
        ctk.CTkLabel(info_frame, text="📖 Disease Encyclopedia", font=("Segoe UI", 20, "bold")).pack(pady=15)
        
        main_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=20, pady=10)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=2)
        main_grid.grid_rowconfigure(0, weight=1)

        # Left: List of diseases
        list_frame = ctk.CTkFrame(main_grid, fg_color="#161922", corner_radius=12)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(list_frame, text="All Diseases", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        self.disease_listbox = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.disease_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Right: Details panel
        self.detail_frame = ctk.CTkFrame(main_grid, fg_color="#161922", corner_radius=12)
        self.detail_frame.grid(row=0, column=1, sticky="nsew")
        
        self.detail_title = ctk.CTkLabel(self.detail_frame, text="Select a disease to view details", font=("Segoe UI", 16, "bold"), text_color="#888")
        self.detail_title.pack(pady=40)
        
        self.detail_content = ctk.CTkTextbox(self.detail_frame, font=("Segoe UI", 12), wrap="word", fg_color="#1e212b", text_color="#d0d0d0")
        self.detail_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.detail_content.pack_forget()

        self._populate_disease_list()

    def _populate_disease_list(self):
        diseases = self.controller.get_all_diseases()
        for d in diseases:
            btn = ctk.CTkButton(self.disease_listbox, text=d.replace("_", " ").title(), 
                                fg_color="transparent", hover_color="#2a2d3e", 
                                font=("Segoe UI", 13), anchor="w", height=40,
                                command=lambda dis=d: self._show_disease_detail(dis))
            btn.pack(fill="x", padx=5, pady=2)

    def _show_disease_detail(self, disease):
        info = self.controller.get_disease_info(disease)
        symptoms = self.controller.get_disease_symptoms(disease)
        
        self.detail_title.configure(text=info["name"].replace("_", " ").title())
        self.detail_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.detail_content.delete("1.0", "end")
        
        text = f"Category: {info['category'].title()}\n\n"
        text += f"Description:\n{info['description']}\n\n"
        text += f"Recommendation:\n{info['recommendation']}\n\n"
        
        if info.get("is_emergency"):
            text += "🚨 EMERGENCY: This condition requires immediate medical attention.\n\n"
            
        text += f"Associated Symptoms ({len(symptoms)}):\n"
        for s in symptoms:
            text += f"  • {s.replace('_', ' ').title()}\n"
            
        self.detail_content.insert("1.0", text)

    # ================= HISTORY PAGE =================
    def _build_history(self):
        hist = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["history"] = hist
        ctk.CTkLabel(hist, text="Diagnosis History", font=("Segoe UI", 20, "bold")).pack(pady=15)
        
        self.hist_tree = ctk.CTkFrame(hist, fg_color="#161922", corner_radius=12)
        self.hist_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.hist_list = ctk.CTkTextbox(self.hist_tree, font=("Segoe UI", 12), wrap="word", fg_color="#161922", text_color="#d0d0d0")
        self.hist_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkButton(hist, text="Refresh History", command=self._refresh_history, fg_color="#2a2d3e").pack(pady=10)
        ctk.CTkButton(hist, text="Clear History", command=self._clear_history, fg_color="transparent", border_width=1).pack(pady=5)
        self._refresh_history()

    def _refresh_history(self):
        self.hist_list.delete("1.0", "end")
        history = self.patient.get_history()
        if not history:
            self.hist_list.insert("1.0", "No diagnosis history recorded yet.")
            return
        for entry in history:
            ts = entry.get("timestamp", "N/A")[:19]
            syms = ", ".join(s.replace("_", " ").title() for s in entry.get("symptoms", [])[:4])
            dis = entry.get("top_disease", "N/A").replace("_", " ").title()
            conf = entry.get("confidence", 0)
            self.hist_list.insert("end", f"📅 {ts}\n🩺 {syms}\n✅ {dis} ({conf}%)\n{'─'*40}\n")

    def _clear_history(self):
        if messagebox.askyesno("Clear", "Delete all history?"):
            self.patient.clear_history()
            self._refresh_history()

    # ================= PROFILE PAGE =================
    def _build_profile(self):
        prof = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["profile"] = prof
        ctk.CTkLabel(prof, text="Patient Profile", font=("Segoe UI", 20, "bold")).pack(pady=15)
        
        form = ctk.CTkFrame(prof, fg_color="#161922", corner_radius=12)
        form.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.profile_vars = {}
        fields = [("Name", "name"), ("Age", "age"), ("Gender", "gender"), ("Blood Type", "blood_type")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form, text=label, font=("Segoe UI", 13)).grid(row=i, column=0, padx=20, pady=10, sticky="w")
            if key in ["gender", "blood_type"]:
                vals = ["Male", "Female", "Other"] if key == "gender" else ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                var = ctk.StringVar()
                menu = ctk.CTkOptionMenu(form, variable=var, values=vals, width=200, fg_color="#1e212b")
                menu.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            else:
                var = ctk.StringVar()
                entry = ctk.CTkEntry(form, textvariable=var, width=200, fg_color="#1e212b")
                entry.grid(row=i, column=1, padx=20, pady=10, sticky="w")
            self.profile_vars[key] = var

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(btn_frame, text="Save Profile", command=self._save_profile, fg_color="#00d4ff", text_color="#000").pack(side="left", padx=10)
        
        self.saved_patients_btn = ctk.CTkButton(btn_frame, text="👥 Saved Patients", command=self._show_saved_patients, fg_color="#2a2d3e")
        self.saved_patients_btn.pack(side="left", padx=10)
        self.saved_patients_btn.pack_forget()
        
        self._load_profile_data()
        self._update_saved_patients_button()

    def _save_profile(self):
        data = {k: v.get() for k, v in self.profile_vars.items()}
        if data["age"]:
            try: data["age"] = int(data["age"])
            except: data["age"] = 0
        self.patient.current_profile.update(data)
        self.patient.save_current_profile()
        self._update_patient_label()
        self._update_saved_patients_button()
        messagebox.showinfo("Saved", "Profile saved successfully.")

    def _load_profile_data(self):
        data = self.patient.get_current_profile()
        for k, v in self.profile_vars.items():
            v.set(str(data.get(k, "")))

    def _update_patient_label(self):
        name = self.patient.get_current_profile().get("name", "Guest")
        self.patient_label.configure(text=f"👤 Patient: {name if name else 'Guest'}")

    def _update_saved_patients_button(self):
        if len(self.patient.saved_profiles) > 0:
            self.saved_patients_btn.pack(side="left", padx=10)
        else:
            self.saved_patients_btn.pack_forget()

    def _show_saved_patients(self):
        if hasattr(self, 'saved_patients_win') and self.saved_patients_win.winfo_exists():
            self.saved_patients_win.lift()
            return
            
        self.saved_patients_win = ctk.CTkToplevel(self.root)
        self.saved_patients_win.title("Saved Patients")
        self.saved_patients_win.geometry("400x500")
        self.saved_patients_win.configure(fg_color="#161922")
        self.saved_patients_win.transient(self.root)
        self.saved_patients_win.grab_set()
        
        ctk.CTkLabel(self.saved_patients_win, text="Saved Patients", font=("Segoe UI", 18, "bold")).pack(pady=15)
        
        list_frame = ctk.CTkScrollableFrame(self.saved_patients_win, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        profiles = self.patient.saved_profiles
        if not profiles:
            ctk.CTkLabel(list_frame, text="No saved patients yet.", text_color="#888").pack(pady=20)
            return
            
        for i, p in enumerate(profiles):
            name = p.get("name", "Unknown")
            age = p.get("age", "N/A")
            gender = p.get("gender", "N/A")
            
            frame = ctk.CTkFrame(list_frame, fg_color="#1e212b", corner_radius=8)
            frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(frame, text=f"👤 {name} (Age: {age}, {gender})", font=("Segoe UI", 12)).pack(side="left", padx=10, pady=8)
            
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=5)
            
            ctk.CTkButton(btn_frame, text="Load", width=60, height=28, 
                          command=lambda idx=i: self._load_patient(idx)).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="Delete", width=60, height=28, fg_color="#e74c3c",
                          command=lambda idx=i: self._delete_patient(idx)).pack(side="left", padx=2)

    def _load_patient(self, index):
        if self.patient.load_profile(index):
            self._load_profile_data()
            self._update_patient_label()
            if hasattr(self, 'saved_patients_win') and self.saved_patients_win.winfo_exists():
                self.saved_patients_win.destroy()
            messagebox.showinfo("Loaded", f"Loaded profile for {self.patient.current_profile.get('name')}")

    def _delete_patient(self, index):
        if messagebox.askyesno("Delete", "Delete this patient profile?"):
            self.patient.delete_profile(index)
            self._load_profile_data()
            self._update_patient_label()
            self._update_saved_patients_button()
            if hasattr(self, 'saved_patients_win') and self.saved_patients_win.winfo_exists():
                self.saved_patients_win.destroy()
            self._show_saved_patients()

    # ================= EXPORT & THEME =================
    def _export_report(self):
        if not self.current_results:
            messagebox.showwarning("Export", "Run a diagnosis first.")
            return
        profile = self.patient.get_current_profile()
        info = self.controller.get_disease_info(self.current_results[0]["disease"])
        exp = self.controller.get_explanation(self.current_results[0]["disease"], list(self.selected_symptoms.keys()))
        path = self.exporter.export_txt(profile, list(self.selected_symptoms.keys()), self.current_results, exp, info)
        if path: messagebox.showinfo("Success", f"Report saved:\n{path}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernMedicalGUI()
    app.run()
