# SPDX-License-Identifier: AGPL-3.0-or-later
"""MedInfer AI - Medical Diagnosis System (desktop GUI).

Symptom input happens either by clicking checkboxes (optionally rating each
symptom Mild/Moderate/Severe) or by typing free text that is parsed by
:mod:`symptom_extractor`. The diagnosis itself runs in the SWI-Prolog engine
through :class:`controller.MedicalController`.
"""

import threading
import tkinter as tk
from tkinter import messagebox
from typing import Any, Optional

import customtkinter as ctk

from controller import MedicalController, MedicalEngineError
from kb_catalog import DiagnosisResult, humanize
from patient_profile import PatientProfile
from report_exporter import ReportExporter
from symptom_extractor import ExtractionResult, SymptomExtractor

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

SEVERITY_LABELS = ("Mild", "Moderate", "Severe")
_SEVERITY_VALUE = {label: label.lower() for label in SEVERITY_LABELS}
_SEVERITY_TITLE = {value: label for label, value in _SEVERITY_VALUE.items()}

TRIAGE_COLORS = {
    "EMERGENCY": "#e74c3c",
    "URGENT": "#f1c40f",
    "SELF_CARE": "#2ecc71",
}
LIKELIHOOD = (
    (40, "Low", "#2ecc71"),
    (70, "Moderate", "#f1c40f"),
    (101, "High", "#e74c3c"),
)


class ModernMedicalGUI:
    def __init__(self):
        try:
            self.controller = MedicalController()
        except MedicalEngineError as exc:
            messagebox.showerror("MedInfer AI could not start", str(exc))
            raise SystemExit(1) from exc

        self.patient = PatientProfile()
        self.exporter = ReportExporter()
        self.extractor = SymptomExtractor(self.controller.catalog)

        self.selected_symptoms: dict[str, str] = {}   # symptom id -> severity value
        self.symptom_widgets: dict[str, dict[str, Any]] = {}
        self.current_results: list[DiagnosisResult] = []
        self.last_extraction: Optional[ExtractionResult] = None

        self.root = ctk.CTk()
        self.root.title("MedInfer AI - Medical Diagnosis System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(fg_color="#0f1115")

        self._build_layout()
        self._build_symptom_browser()
        self._update_patient_label()

    # ==================================================================
    # Layout
    # ==================================================================
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
        ctk.CTkLabel(self.sidebar, text="🏥 MedInfer AI", font=("Segoe UI", 24, "bold"),
                     text_color="#00d4ff").pack(pady=25)
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("📖 Disease Info", "disease_info"),
            ("📜 History", "history"),
            ("👤 Patient Profile", "profile"),
        ]
        self.nav_buttons = {}
        for text, key in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent",
                                hover_color="#2a2d3e", font=("Segoe UI", 15), anchor="w",
                                height=48, corner_radius=10,
                                command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[key] = btn
        ctk.CTkLabel(self.sidebar, text="v2.0 | AI Expert System", text_color="#555",
                     font=("Segoe UI", 10)).pack(side="bottom", pady=(0, 10))

    def show_frame(self, frame_name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="#2a2d3e" if key == frame_name else "transparent")

    def _build_dashboard(self):
        dash = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["dashboard"] = dash
        dash.grid_columnconfigure(0, weight=1)
        dash.grid_columnconfigure(1, weight=1)
        dash.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(dash, fg_color="#161922", corner_radius=12, height=65)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        top_bar.grid_columnconfigure(0, weight=1)

        self.patient_label = ctk.CTkLabel(top_bar, text="Patient: Guest",
                                          font=("Segoe UI", 16, "bold"), text_color="#e0e0e0")
        self.patient_label.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        self.export_format = ctk.StringVar(value="PDF")
        format_menu = ctk.CTkOptionMenu(top_bar, values=["PDF", "TXT"], variable=self.export_format,
                                        width=90, fg_color="#2a2d3e", button_color="#3a3f5c")
        format_menu.grid(row=0, column=1, sticky="e", padx=(0, 6), pady=15)
        ctk.CTkButton(top_bar, text="📤 Export Report", command=self._export_report,
                      fg_color="#2a2d3e", width=130).grid(row=0, column=2, sticky="e",
                                                          padx=(0, 15), pady=15)

        self.symptom_panel = self._create_scrollable_panel(dash, "Symptom Input & Selection", 1, 0)

        self.right_panel = ctk.CTkFrame(dash, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.diag_panel = self._create_scrollable_panel(self.right_panel, "Differential Diagnosis", 0, 0)

        self.exp_panel = ctk.CTkFrame(self.right_panel, corner_radius=12, fg_color="#161922")
        self.exp_panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        header = ctk.CTkFrame(self.exp_panel, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12, 0))
        ctk.CTkLabel(header, text="🤖 AI Reasoning Engine", font=("Segoe UI", 14, "bold"),
                     text_color="#00d4ff").pack(side="left")
        self.triage_label = ctk.CTkLabel(self.exp_panel, text="", font=("Segoe UI", 12, "bold"),
                                         corner_radius=8, fg_color="transparent",
                                         wraplength=600, justify="left")
        self.exp_text = ctk.CTkTextbox(self.exp_panel, font=("Segoe UI", 12), wrap="word",
                                       fg_color="#1e212b", text_color="#d0d0d0")
        self.exp_text.pack(fill="both", expand=True, padx=15, pady=(8, 15))

        self._build_symptom_controls()

    def _create_scrollable_panel(self, parent, title, row, col):
        panel = ctk.CTkScrollableFrame(parent, label_text=title, corner_radius=12, fg_color="#161922")
        panel.grid(row=row, column=col, sticky="nsew")
        return panel

    # ==================================================================
    # Symptom input
    # ==================================================================
    def _build_symptom_controls(self):
        self.nlp_frame = ctk.CTkFrame(self.symptom_panel, fg_color="#1e212b", corner_radius=10)
        self.nlp_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(self.nlp_frame, text="💬 Natural Language Input",
                     font=("Segoe UI", 12, "bold"), text_color="#00d4ff").pack(anchor="w",
                                                                               padx=12, pady=(10, 5))
        self.nlp_entry = ctk.CTkTextbox(self.nlp_frame, height=50, font=("Segoe UI", 11),
                                        fg_color="#0f1115")
        self.nlp_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.nlp_entry.insert("0.0", "Example: I have a high fever, cough, and severe headache for 2 days...")

        nlp_btn_frame = ctk.CTkFrame(self.nlp_frame, fg_color="transparent")
        nlp_btn_frame.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkButton(nlp_btn_frame, text="🔍 Analyze Text", command=self._analyze_nlp,
                      width=120, fg_color="#00d4ff", text_color="#000",
                      font=("Segoe UI", 11, "bold")).pack(side="left")
        self.nlp_feedback = ctk.CTkLabel(nlp_btn_frame, text="", font=("Segoe UI", 11),
                                         text_color="#00d4ff")
        self.nlp_feedback.pack(side="right")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_symptoms)
        ctk.CTkEntry(self.symptom_panel, placeholder_text="🔍 Search symptoms...",
                     textvariable=self.search_var, height=35,
                     fg_color="#1e212b").pack(fill="x", pady=(0, 10))

        self.symptom_container = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.symptom_container.pack(fill="both", expand=True)

        self.action_frame = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=15)

        self.diagnose_btn = ctk.CTkButton(self.action_frame, text="🔍 Run Diagnosis",
                                          command=self._run_diagnosis, fg_color="#00d4ff",
                                          text_color="#000", font=("Segoe UI", 14, "bold"))
        self.diagnose_btn.pack(side="left", padx=5)
        ctk.CTkButton(self.action_frame, text="Clear All", command=self._clear_symptoms,
                      fg_color="transparent", border_width=1, width=100).pack(side="left", padx=5)
        self.loading_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", width=150)
        self.loading_bar.pack(side="right", padx=10)

    def _build_symptom_browser(self):
        """Create the full grouped symptom list once; filtering only toggles visibility."""
        for w in self.symptom_container.winfo_children():
            w.destroy()
        self.symptom_widgets = {}
        self._system_blocks: list[tuple[str, ctk.CTkFrame, list]] = []

        for system, symptom_ids in self.controller.symptoms_by_system():
            block = ctk.CTkFrame(self.symptom_container, fg_color="transparent")
            block.pack(fill="x", pady=(8, 4))
            ctk.CTkLabel(block, text=f"🔹 {system}", font=("Segoe UI", 12, "bold"),
                         text_color="#00d4ff").pack(anchor="w", padx=5)

            grid = ctk.CTkFrame(block, fg_color="transparent")
            grid.pack(fill="x", padx=10)
            grid.grid_columnconfigure(0, weight=1)
            grid.grid_columnconfigure(1, weight=1)

            rows: list[tuple[str, ctk.CTkFrame]] = []
            for i, symptom in enumerate(symptom_ids):
                row_frame = ctk.CTkFrame(grid, fg_color="#1e212b", corner_radius=8)
                row, col = divmod(i, 2)
                row_frame.grid(row=row, column=col, padx=4, pady=3, sticky="ew")

                variable = ctk.BooleanVar(value=symptom in self.selected_symptoms)
                checkbox = ctk.CTkCheckBox(
                    row_frame, text=humanize(symptom), variable=variable,
                    command=lambda s=symptom, v=variable: self._on_symptom_toggle(s, v),
                    font=("Segoe UI", 11))
                checkbox.pack(side="left", padx=8, pady=6)

                severity_var = ctk.StringVar(
                    value=_SEVERITY_TITLE.get(self.selected_symptoms.get(symptom, "moderate"),
                                              "Moderate"))
                menu = ctk.CTkOptionMenu(
                    row_frame, values=SEVERITY_LABELS, variable=severity_var,
                    width=95, height=26, fg_color="#2a2d3e", button_color="#3a3f5c",
                    command=lambda value, s=symptom: self._update_severity(s, value))
                if symptom in self.selected_symptoms:
                    menu.pack(side="right", padx=6, pady=6)

                self.symptom_widgets[symptom] = {
                    "var": variable, "sev": severity_var, "menu": menu, "row": row_frame,
                }
                rows.append((symptom, row_frame))
            self._system_blocks.append((system, block, rows))

    def _on_symptom_toggle(self, symptom, var):
        widget = self.symptom_widgets[symptom]
        if var.get():
            widget["menu"].pack(side="right", padx=6, pady=6)
            self.selected_symptoms[symptom] = _SEVERITY_VALUE[widget["sev"].get()]
        else:
            widget["menu"].pack_forget()
            self.selected_symptoms.pop(symptom, None)

    def _update_severity(self, symptom, label):
        if symptom in self.selected_symptoms:
            self.selected_symptoms[symptom] = _SEVERITY_VALUE[label]
        else:
            self.symptom_widgets[symptom]["sev"].set(label)

    def _filter_symptoms(self, *_args):
        query = self.search_var.get().strip().lower()
        visible_blocks: list[tuple[ctk.CTkFrame, bool]] = []
        for _system, block, rows in self._system_blocks:
            any_visible = False
            for symptom, row_frame in rows:
                matches = (not query) or query in humanize(symptom).lower()
                if matches:
                    row_frame.grid()
                    any_visible = True
                else:
                    row_frame.grid_remove()
            visible_blocks.append((block, any_visible))
        # Re-pack in original order so the layout never reorders.
        for block, _visible in visible_blocks:
            block.pack_forget()
        for block, visible in visible_blocks:
            if visible:
                block.pack(fill="x", pady=(8, 4))

    def _clear_symptoms(self):
        for widget in self.symptom_widgets.values():
            widget["var"].set(False)
            widget["menu"].pack_forget()
        self.selected_symptoms.clear()
        self.current_results = []
        self.last_extraction = None
        for w in self.diag_panel.winfo_children():
            w.destroy()
        self.exp_text.delete("1.0", "end")
        self.triage_label.pack_forget()
        self.nlp_entry.delete("1.0", "end")
        self.nlp_entry.insert("0.0", "Example: I have a high fever, cough, and severe headache for 2 days...")
        self.nlp_feedback.configure(text="")
        self.search_var.set("")

    # ------------------------------------------------------------------
    # Natural language input
    # ------------------------------------------------------------------
    def _analyze_nlp(self):
        text = self.nlp_entry.get("1.0", "end-1c")
        if not text.strip() or "example:" in text.lower():
            self.nlp_feedback.configure(text="⚠️ Please enter your symptoms first")
            return

        extraction = self.extractor.extract(text)
        self.last_extraction = extraction if extraction.has_any() else None

        if not extraction.has_any():
            if extraction.temperature_c is not None:
                self.nlp_feedback.configure(
                    text=f"🌡️ Captured temperature only ({extraction.temperature_c:.1f} C). "
                         "Please also select symptoms.")
            else:
                self.nlp_feedback.configure(text="❌ No matching symptoms found")
            return

        count = 0
        for symptom in extraction.symptom_ids:
            level = extraction.severities.get(symptom, "moderate")
            widget = self.symptom_widgets[symptom]
            label = _SEVERITY_TITLE[level]
            if not widget["var"].get():
                widget["var"].set(True)
                self._on_symptom_toggle(symptom, widget["var"])
                count += 1
            if widget["sev"].get() != label:
                widget["sev"].set(label)
            if symptom in self.selected_symptoms:
                self.selected_symptoms[symptom] = level

        feedback = f"✅ Detected {len(extraction.symptom_ids)} symptom(s)"
        if count:
            feedback += f" ({count} newly selected)"
        if extraction.temperature_c is not None:
            feedback += f" • 🌡️ {extraction.temperature_c:.1f} C"
        for symptom, duration in list(extraction.durations.items())[:1]:
            feedback += f" • ⏱ {humanize(symptom)} {duration}"
        self.nlp_feedback.configure(text=feedback)
        self.root.after(6000, lambda: self.nlp_feedback.configure(text=""))

    # ------------------------------------------------------------------
    # Diagnosis flow
    # ------------------------------------------------------------------
    def _run_diagnosis(self):
        if not self.selected_symptoms:
            messagebox.showwarning("No Symptoms", "Please select at least one symptom.")
            return
        self.loading_bar.start()
        self.diagnose_btn.configure(state="disabled")
        selected = dict(self.selected_symptoms)
        age = self.patient.get_current_profile().get("age") or None
        try:
            age = int(age) if age else None
        except (TypeError, ValueError):
            age = None
        threading.Thread(target=self._diagnose_thread,
                         args=(selected, age), daemon=True).start()

    def _diagnose_thread(self, selected, age):
        try:
            results = self.controller.diagnose(selected, age=age)
        except Exception as exc:  # noqa: BLE001 - report engine failures in the UI
            self.root.after(0, lambda: self._show_engine_error(exc))
            return
        self.root.after(0, lambda: self._render_results(results, selected, age))

    def _show_engine_error(self, exc):
        self.loading_bar.stop()
        self.diagnose_btn.configure(state="normal")
        messagebox.showerror("Diagnosis failed", str(exc))

    def _render_results(self, results, selected, age):
        self.loading_bar.stop()
        self.diagnose_btn.configure(state="normal")
        self.current_results = results
        for w in self.diag_panel.winfo_children():
            w.destroy()

        if not results:
            ctk.CTkLabel(self.diag_panel,
                         text="No matching diseases found. Try adding more symptoms.",
                         font=("Segoe UI", 13), text_color="#888").pack(pady=30)
            self.exp_text.delete("1.0", "end")
            self.triage_label.pack_forget()
            return

        for i, result in enumerate(results[:3], 1):
            self._create_diag_card(result, i)
        self._generate_explanation(results, selected, age)

        # Persist to history with severity / temperature context.
        top = results[0]
        extraction = self.last_extraction
        extras: dict[str, Any] = {}
        if selected:
            extras["severities"] = {s: level for s, level in selected.items()}
        if extraction is not None:
            if extraction.temperature_c is not None:
                extras["temperature_c"] = extraction.temperature_c
            if extraction.durations:
                extras["durations"] = extraction.durations
        self.patient.add_diagnosis(
            list(selected.keys()),
            [r.as_dict() for r in results],
            top.disease,
            top.confidence,
            extras or None,
        )

    def _create_diag_card(self, result: DiagnosisResult, rank: int):
        level, color = self._likelihood(result.confidence)
        card = ctk.CTkFrame(self.diag_panel, fg_color="#1e212b", corner_radius=10,
                            border_width=1, border_color="#333")
        card.pack(fill="x", pady=8, padx=8)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(header, text=f"#{rank} {result.name}",
                     font=("Segoe UI", 14, "bold")).pack(side="left")
        if result.emergency:
            ctk.CTkLabel(header, text="🚨 EMERGENCY", text_color="#e74c3c",
                         font=("Segoe UI", 11, "bold"),
                         fg_color="#2a1a1a").pack(side="right", padx=5)

        progress = ctk.CTkProgressBar(card, width=350, progress_color=color, fg_color="#2a2d3e")
        progress.pack(fill="x", padx=15, pady=(0, 4))
        progress.set(min(result.confidence / 100.0, 1.0))

        risk = "elevated" if result.risk_note else ""
        meta = (f"Likelihood: {level} | {result.confidence}% | "
                f"Category: {result.category.title()} | Matched {result.matched}/{result.total}")
        if risk:
            meta += f" | Age-risk: {risk}"
        ctk.CTkLabel(card, text=meta, font=("Segoe UI", 11),
                     text_color="#aaa").pack(anchor="w", padx=15, pady=(0, 8))

    @staticmethod
    def _likelihood(confidence: int) -> tuple[str, str]:
        for threshold, level, color in LIKELIHOOD:
            if confidence < threshold:
                return level, color
        return "High", "#e74c3c"

    def _generate_explanation(self, results, selected, age):
        top = results[0]
        level, title, guidance = self.controller.triage(
            results, selected,
            temperature_c=getattr(self.last_extraction, "temperature_c", None),
            durations=getattr(self.last_extraction, "durations", None),
        )
        color = TRIAGE_COLORS[level]
        self.triage_label.configure(text=f"🩺 Next step: {title}", text_color="#000",
                                    fg_color=color)
        self.triage_label.pack(fill="x", padx=15, pady=(10, 0))

        explanation = self.controller.build_explanation(top.disease, selected,
                                                        self.last_extraction)
        text = f"{explanation}\n\nNEXT STEPS ({title.upper()}):\n{guidance}"
        if top.risk_note:
            text = f"Risk note: {top.risk_note}\n\n{text}"
        self.exp_text.delete("1.0", "end")
        self.exp_text.insert("1.0", text)

    # ==================================================================
    # Disease info page
    # ==================================================================
    def _build_disease_info(self):
        info_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["disease_info"] = info_frame
        ctk.CTkLabel(info_frame, text="📖 Disease Encyclopedia",
                     font=("Segoe UI", 20, "bold")).pack(pady=15)

        main_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=20, pady=10)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=2)
        main_grid.grid_rowconfigure(0, weight=1)

        list_frame = ctk.CTkFrame(main_grid, fg_color="#161922", corner_radius=12)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(list_frame, text="All Diseases", font=("Segoe UI", 14, "bold")).pack(pady=10)
        self.disease_listbox = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.disease_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        self.detail_frame = ctk.CTkFrame(main_grid, fg_color="#161922", corner_radius=12)
        self.detail_frame.grid(row=0, column=1, sticky="nsew")
        self.detail_title = ctk.CTkLabel(self.detail_frame,
                                         text="Select a disease to view details",
                                         font=("Segoe UI", 16, "bold"), text_color="#888")
        self.detail_title.pack(pady=40)
        self.detail_content = ctk.CTkTextbox(self.detail_frame, font=("Segoe UI", 12),
                                             wrap="word", fg_color="#1e212b",
                                             text_color="#d0d0d0")
        self.detail_content.pack_forget()

        for disease_id in self.controller.all_diseases():
            btn = ctk.CTkButton(self.disease_listbox, text=humanize(disease_id),
                                fg_color="transparent", hover_color="#2a2d3e",
                                font=("Segoe UI", 13), anchor="w", height=40,
                                command=lambda d=disease_id: self._show_disease_detail(d))
            btn.pack(fill="x", padx=5, pady=2)

    def _show_disease_detail(self, disease_id):
        defn = self.controller.disease_info(disease_id)
        self.detail_title.configure(text=defn.name)
        self.detail_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.detail_content.delete("1.0", "end")

        text = f"Category: {defn.category.title()}\n\n"
        text += f"Description:\n{defn.description}\n\n"
        text += f"Recommendation:\n{defn.recommendation}\n\n"
        if defn.emergency:
            text += "🚨 EMERGENCY: This condition requires immediate medical attention.\n\n"
        if defn.age_risk_bands():
            bands = ", ".join(b.replace("_", " ").title() for b in defn.age_risk_bands())
            text += f"Age risk groups: {bands}\n\n"
        text += f"Associated Symptoms ({len(defn.symptoms)}):\n"
        for symptom in defn.symptoms:
            text += f"  • {humanize(symptom)}\n"
        self.detail_content.insert("1.0", text)

    # ==================================================================
    # History page
    # ==================================================================
    def _build_history(self):
        hist = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["history"] = hist
        ctk.CTkLabel(hist, text="Diagnosis History", font=("Segoe UI", 20, "bold")).pack(pady=15)

        self.hist_tree = ctk.CTkFrame(hist, fg_color="#161922", corner_radius=12)
        self.hist_tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.hist_list = ctk.CTkTextbox(self.hist_tree, font=("Segoe UI", 12), wrap="word",
                                        fg_color="#161922", text_color="#d0d0d0")
        self.hist_list.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(hist, text="Refresh History", command=self._refresh_history,
                      fg_color="#2a2d3e").pack(pady=10)
        ctk.CTkButton(hist, text="Clear History", command=self._clear_history,
                      fg_color="transparent", border_width=1).pack(pady=5)
        self._refresh_history()

    def _refresh_history(self):
        self.hist_list.delete("1.0", "end")
        history = self.patient.get_history()
        if not history:
            self.hist_list.insert("1.0", "No diagnosis history recorded yet.")
            return
        for entry in history:
            ts = entry.get("timestamp", "N/A")[:19]
            syms = ", ".join(humanize(s) for s in entry.get("symptoms", [])[:4])
            disease = humanize(entry.get("top_disease", "N/A"))
            conf = entry.get("confidence", 0)
            lines = f"📅 {ts}\n🩺 {syms}\n✅ {disease} ({conf}%)"
            temp = entry.get("temperature_c")
            if temp is not None:
                lines += f"\n🌡️ Temperature: {float(temp):.1f} C"
            durations = entry.get("durations")
            if durations:
                lines += "\n⏱ " + ", ".join(f"{humanize(s)}: {d}" for s, d in durations.items())
            self.hist_list.insert("end", lines + f"\n{'─'*40}\n")

    def _clear_history(self):
        if messagebox.askyesno("Clear", "Delete all history?"):
            self.patient.clear_history()
            self._refresh_history()

    # ==================================================================
    # Patient profile page
    # ==================================================================
    def _build_profile(self):
        prof = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["profile"] = prof
        ctk.CTkLabel(prof, text="Patient Profile", font=("Segoe UI", 20, "bold")).pack(pady=15)

        form = ctk.CTkFrame(prof, fg_color="#161922", corner_radius=12)
        form.pack(fill="both", expand=True, padx=40, pady=10)

        self.profile_vars = {}
        fields = [("Name", "name"), ("Age", "age"), ("Gender", "gender"), ("Blood Type", "blood_type")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form, text=label, font=("Segoe UI", 13)).grid(
                row=i, column=0, padx=20, pady=10, sticky="w")
            if key in ("gender", "blood_type"):
                values = (["Male", "Female", "Other"] if key == "gender"
                          else ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                var = ctk.StringVar()
                ctk.CTkOptionMenu(form, variable=var, values=values, width=200,
                                  fg_color="#1e212b").grid(row=i, column=1, padx=20, pady=10, sticky="w")
            else:
                var = ctk.StringVar()
                ctk.CTkEntry(form, textvariable=var, width=200,
                             fg_color="#1e212b").grid(row=i, column=1, padx=20, pady=10, sticky="w")
            self.profile_vars[key] = var

        ctk.CTkLabel(form, text="💡 Age is used to flag conditions with higher "
                                "risk in your age group (e.g. flu, pneumonia in the elderly).",
                     font=("Segoe UI", 11), text_color="#aaa").grid(
            row=len(fields), column=0, columnspan=2, padx=20, pady=(0, 6), sticky="w")

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)
        ctk.CTkButton(btn_frame, text="Save Profile", command=self._save_profile,
                      fg_color="#00d4ff", text_color="#000").pack(side="left", padx=10)

        self.saved_patients_btn = ctk.CTkButton(btn_frame, text="👥 Saved Patients",
                                                command=self._show_saved_patients,
                                                fg_color="#2a2d3e")
        self._load_profile_data()
        self._update_saved_patients_button()

    def _save_profile(self):
        data = {k: v.get() for k, v in self.profile_vars.items()}
        if data["age"]:
            try:
                data["age"] = int(data["age"])
            except ValueError:
                data["age"] = 0
        self.patient.current_profile.update(data)
        self.patient.save_current_profile()
        self._update_patient_label()
        self._update_saved_patients_button()
        messagebox.showinfo("Saved", "Profile saved successfully.")

    def _load_profile_data(self):
        data = self.patient.get_current_profile()
        for key, var in self.profile_vars.items():
            var.set(str(data.get(key, "")))

    def _update_patient_label(self):
        name = self.patient.get_current_profile().get("name", "Guest")
        self.patient_label.configure(text=f"👤 Patient: {name if name else 'Guest'}")

    def _update_saved_patients_button(self):
        if len(self.patient.saved_profiles) > 0:
            self.saved_patients_btn.pack(side="left", padx=10)
        else:
            self.saved_patients_btn.pack_forget()

    def _show_saved_patients(self):
        if hasattr(self, "saved_patients_win") and self.saved_patients_win.winfo_exists():
            self.saved_patients_win.lift()
            return
        self.saved_patients_win = ctk.CTkToplevel(self.root)
        self.saved_patients_win.title("Saved Patients")
        self.saved_patients_win.geometry("400x500")
        self.saved_patients_win.configure(fg_color="#161922")
        self.saved_patients_win.transient(self.root)
        self.saved_patients_win.grab_set()
        ctk.CTkLabel(self.saved_patients_win, text="Saved Patients",
                     font=("Segoe UI", 18, "bold")).pack(pady=15)

        list_frame = ctk.CTkScrollableFrame(self.saved_patients_win, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        profiles = self.patient.saved_profiles
        if not profiles:
            ctk.CTkLabel(list_frame, text="No saved patients yet.", text_color="#888").pack(pady=20)
            return
        for i, profile in enumerate(profiles):
            name = profile.get("name", "Unknown")
            age = profile.get("age", "N/A")
            gender = profile.get("gender", "N/A")
            frame = ctk.CTkFrame(list_frame, fg_color="#1e212b", corner_radius=8)
            frame.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(frame, text=f"👤 {name} (Age: {age}, {gender})",
                         font=("Segoe UI", 12)).pack(side="left", padx=10, pady=8)
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
            self._close_saved_patients()
            messagebox.showinfo("Loaded",
                                f"Loaded profile for {self.patient.current_profile.get('name')}")

    def _delete_patient(self, index):
        if messagebox.askyesno("Delete", "Delete this patient profile?"):
            self.patient.delete_profile(index)
            self._load_profile_data()
            self._update_patient_label()
            self._update_saved_patients_button()
            self._close_saved_patients()
            self._show_saved_patients()

    def _close_saved_patients(self):
        if hasattr(self, "saved_patients_win") and self.saved_patients_win.winfo_exists():
            self.saved_patients_win.destroy()

    # ==================================================================
    # Export
    # ==================================================================
    def _export_report(self):
        if not self.current_results:
            messagebox.showwarning("Export", "Run a diagnosis first.")
            return
        top = self.current_results[0]
        defn = self.controller.disease_info(top.disease)
        info = {
            "name": defn.name,
            "category": defn.category,
            "description": defn.description,
            "recommendation": defn.recommendation,
            "is_emergency": defn.emergency,
        }
        explanation = self.controller.build_explanation(
            top.disease, dict(self.selected_symptoms), self.last_extraction)
        extras: dict[str, Any] = {}
        if self.last_extraction is not None:
            if self.last_extraction.temperature_c is not None:
                extras["temperature_c"] = self.last_extraction.temperature_c
            if self.last_extraction.durations:
                extras["durations"] = self.last_extraction.durations
        try:
            path = self.exporter.export(
                self.export_format.get().lower(),
                self.patient.get_current_profile(),
                dict(self.selected_symptoms),
                [r.as_dict() for r in self.current_results],
                explanation,
                info,
                extras or None,
            )
        except RuntimeError as exc:  # e.g. reportlab missing
            messagebox.showerror("Export failed", str(exc))
            return
        if path:
            messagebox.showinfo("Success", f"Report saved:\n{path}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ModernMedicalGUI()
    app.run()
