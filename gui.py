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

from core.manager import DiagnosisManager
from core.models import DiagnosisOutcome, DiagnosisSession
from kb_catalog import DiagnosisResult, humanize
from symptom_extractor import ExtractionResult

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Clinical Precision palette ──────────────────────────────────────
# Deep blue-charcoal surfaces with trust-blue accents.
# Avoids the generic cyan-on-black AI-generated default.
BG_BASE = "#0D1117"
BG_SURFACE = "#151B23"
BG_CARD = "#1C2333"
BG_CARD_INNER = "#0D1117"
BORDER_COLOR = "#21262D"
BORDER_LIGHT = "#30363D"

ACCENT_BLUE = "#3B82F6"       # primary actions, headings
ACCENT_GREEN = "#10B981"      # health, success, self-care
ACCENT_AMBER = "#F59E0B"      # warnings, guest badge
ACCENT_RED = "#EF4444"        # emergency, danger

TEXT_PRIMARY = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
TEXT_MUTED = "#484F58"

SEVERITY_LABELS = ("Mild", "Moderate", "Severe")
_SEVERITY_VALUE = {label: label.lower() for label in SEVERITY_LABELS}
_SEVERITY_TITLE = {value: label for label, value in _SEVERITY_VALUE.items()}

TRIAGE_COLORS = {
    "EMERGENCY": ACCENT_RED,
    "URGENT": ACCENT_AMBER,
    "SELF_CARE": ACCENT_GREEN,
}
LIKELIHOOD = (
    (40, "Low", ACCENT_GREEN),
    (70, "Moderate", ACCENT_AMBER),
    (101, "High", ACCENT_RED),
)


class ModernMedicalGUI:
    def __init__(self, manager: DiagnosisManager):
        self.manager = manager

        self.selected_symptoms: dict[str, str] = {}   # symptom id -> severity value
        self.symptom_widgets: dict[str, dict[str, Any]] = {}
        self.current_results: list[DiagnosisResult] = []
        self.last_extraction: Optional[ExtractionResult] = None

        self.root = ctk.CTk()
        self.root.title("MedInfer AI — Medical Diagnosis System")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        self.root.configure(fg_color=BG_BASE)

        self._build_layout()
        self._build_symptom_browser()
        self._update_patient_label()

    # ── Convenience accessors (thin adapter layer) ──────────────────
    @property
    def patient(self):
        return self.manager.patient

    @property
    def controller(self):
        return self.manager._controller

    # ==================================================================
    # Layout
    # ==================================================================
    def _build_layout(self):
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=0, fg_color=BG_SURFACE)
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
        # ── Brand mark ──
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=20, pady=(28, 6))
        ctk.CTkLabel(brand_frame, text="MedInfer", font=("Segoe UI", 22, "bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(brand_frame, text="AI Clinical Assistant", font=("Segoe UI", 10),
                     text_color=TEXT_MUTED).pack(anchor="w")

        # ── Thin divider ──
        divider = ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER_COLOR)
        divider.pack(fill="x", padx=20, pady=(12, 16))

        # ── Navigation ──
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Disease Info", "disease_info"),
            ("History", "history"),
            ("Patient Profile", "profile"),
        ]
        self.nav_buttons = {}
        for text, key in nav_items:
            btn = ctk.CTkButton(self.sidebar, text=f"  {text}", fg_color="transparent",
                                hover_color=BG_CARD, font=("Segoe UI", 13), anchor="w",
                                height=42, corner_radius=8,
                                command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

        # ── Version footer ──
        ctk.CTkLabel(self.sidebar, text="v3.0  ·  AI Expert System",
                     text_color=TEXT_MUTED, font=("Segoe UI", 9)).pack(
            side="bottom", pady=(0, 14))

    def show_frame(self, frame_name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)
        for key, btn in self.nav_buttons.items():
            if key == frame_name:
                btn.configure(fg_color=BG_CARD, text_color=ACCENT_BLUE,
                              font=("Segoe UI", 13, "bold"))
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SECONDARY,
                              font=("Segoe UI", 13))

    def _build_dashboard(self):
        dash = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["dashboard"] = dash
        dash.grid_columnconfigure(0, weight=1)
        dash.grid_columnconfigure(1, weight=1)
        dash.grid_rowconfigure(1, weight=1)

        top_bar = ctk.CTkFrame(dash, fg_color=BG_SURFACE, corner_radius=10, height=65)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        top_bar.grid_columnconfigure(0, weight=1)

        patient_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        patient_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.patient_label = ctk.CTkLabel(patient_frame, text="Patient: Guest",
                                          font=("Segoe UI", 16, "bold"), text_color=TEXT_PRIMARY)
        self.patient_label.pack(side="left")

        self.profile_badge = ctk.CTkLabel(patient_frame, text="  GUEST",
                                          font=("Segoe UI", 10, "bold"),
                                          text_color="#000",
                                          fg_color=ACCENT_AMBER,
                                          corner_radius=4,
                                          padx=8, pady=2)
        self.profile_badge.pack(side="left", padx=(10, 0))

        self.choose_profile_btn = ctk.CTkButton(
            patient_frame, text="Sign In",
            command=self._show_profile_chooser,
            fg_color=BORDER_LIGHT, hover_color=BG_CARD,
            font=("Segoe UI", 11), width=100, height=30)
        self.choose_profile_btn.pack(side="left", padx=(12, 0))

        self.guest_note = ctk.CTkLabel(
            patient_frame,
            text="Records won't be saved with guest profile",
            font=("Segoe UI", 10), text_color=ACCENT_AMBER)

        self.export_format = ctk.StringVar(value="PDF")
        format_menu = ctk.CTkOptionMenu(top_bar, values=["PDF", "TXT"], variable=self.export_format,
                                        width=90, fg_color=BORDER_LIGHT, button_color=BG_CARD)
        format_menu.grid(row=0, column=2, sticky="e", padx=(0, 6), pady=15)
        ctk.CTkButton(top_bar, text="Export Report", command=self._export_report,
                      fg_color=BORDER_LIGHT, text_color=TEXT_SECONDARY, width=130).grid(
        row=0, column=3, sticky="e", padx=(0, 15), pady=15)

        self.symptom_panel = self._create_scrollable_panel(dash, "Symptom Input & Selection", 1, 0)

        self.right_panel = ctk.CTkFrame(dash, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.diag_panel = self._create_scrollable_panel(self.right_panel, "Differential Diagnosis", 0, 0)

        self.exp_panel = ctk.CTkFrame(self.right_panel, corner_radius=10, fg_color=BG_SURFACE)
        self.exp_panel.grid(row=1, column=0, sticky="nsew", pady=(12, 0))

        header = ctk.CTkFrame(self.exp_panel, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12, 0))
        ctk.CTkLabel(header, text="AI Reasoning Engine", font=("Segoe UI", 14, "bold"),
                     text_color=ACCENT_BLUE).pack(side="left")
        self.triage_label = ctk.CTkLabel(self.exp_panel, text="", font=("Segoe UI", 12, "bold"),
                                         corner_radius=6, fg_color="transparent",
                                         wraplength=600, justify="left")
        self.exp_text = ctk.CTkTextbox(self.exp_panel, font=("Segoe UI", 12), wrap="word",
                                       fg_color=BG_CARD, text_color=TEXT_PRIMARY)
        self.exp_text.pack(fill="both", expand=True, padx=15, pady=(8, 15))

        self._build_symptom_controls()

    def _create_scrollable_panel(self, parent, title, row, col):
        panel = ctk.CTkScrollableFrame(parent, label_text=title, corner_radius=10,
                                       fg_color=BG_SURFACE,
                                       label_font=("Segoe UI", 12, "bold"),
                                       label_text_color=TEXT_SECONDARY)
        panel.grid(row=row, column=col, sticky="nsew")
        return panel

    # ==================================================================
    # Symptom input
    # ==================================================================
    def _build_symptom_controls(self):
        self.nlp_frame = ctk.CTkFrame(self.symptom_panel, fg_color=BG_CARD, corner_radius=10)
        self.nlp_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(self.nlp_frame, text="Natural Language Input",
                     font=("Segoe UI", 12, "bold"), text_color=ACCENT_BLUE).pack(anchor="w",
                                                                               padx=12, pady=(10, 5))
        self.nlp_entry = ctk.CTkTextbox(self.nlp_frame, height=50, font=("Segoe UI", 11),
                                        fg_color=BG_BASE, text_color=TEXT_SECONDARY)
        self.nlp_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.nlp_entry.insert("0.0", "Example: I have a high fever, cough, and severe headache for 2 days...")

        nlp_btn_frame = ctk.CTkFrame(self.nlp_frame, fg_color="transparent")
        nlp_btn_frame.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkButton(nlp_btn_frame, text="Analyze", command=self._analyze_nlp,
                      width=100, fg_color=ACCENT_BLUE, text_color="#fff",
                      font=("Segoe UI", 11, "bold")).pack(side="left")
        ctk.CTkButton(nlp_btn_frame, text="Run Diagnosis", command=self._run_diagnosis,
                      width=130, fg_color=ACCENT_GREEN, text_color="#fff",
                      font=("Segoe UI", 11, "bold")).pack(side="left", padx=(8, 0))
        ctk.CTkButton(nlp_btn_frame, text="Clear All", command=self._clear_symptoms,
                      width=90, fg_color="transparent", border_width=1,
                      border_color=BORDER_LIGHT, text_color=TEXT_SECONDARY,
                      font=("Segoe UI", 11)).pack(side="left", padx=(6, 0))
        self.nlp_feedback = ctk.CTkLabel(nlp_btn_frame, text="", font=("Segoe UI", 11),
                                         text_color=ACCENT_GREEN)
        self.nlp_feedback.pack(side="right")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_symptoms)
        ctk.CTkEntry(self.symptom_panel, placeholder_text="Search symptoms...",
                     textvariable=self.search_var, height=35,
                     fg_color=BG_CARD, text_color=TEXT_PRIMARY,
                     border_color=BORDER_COLOR).pack(fill="x", pady=(0, 10))

        self.symptom_container = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.symptom_container.pack(fill="both", expand=True)

        self.action_frame = ctk.CTkFrame(self.symptom_panel, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=(5, 15))

        self.diagnose_btn = ctk.CTkButton(self.action_frame, text="Run Diagnosis",
                                          command=self._run_diagnosis, fg_color=ACCENT_GREEN,
                                          text_color="#fff", font=("Segoe UI", 13, "bold"),
                                          height=38)
        self.diagnose_btn.pack(side="left", padx=5)
        ctk.CTkButton(self.action_frame, text="Clear All", command=self._clear_symptoms,
                      fg_color="transparent", border_width=1, border_color=BORDER_LIGHT,
                      text_color=TEXT_SECONDARY, width=90).pack(side="left", padx=5)
        self.loading_bar = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", width=150)
        self.loading_bar.pack(side="right", padx=10)

    def _build_symptom_browser(self):
        """Create the full grouped symptom list once; filtering only toggles visibility."""
        for w in self.symptom_container.winfo_children():
            w.destroy()
        self.symptom_widgets = {}
        self._system_blocks: list[tuple[str, ctk.CTkFrame, list]] = []

        for system, symptom_ids in self.manager.symptoms_by_system():
            block = ctk.CTkFrame(self.symptom_container, fg_color="transparent")
            block.pack(fill="x", pady=(8, 4))
            ctk.CTkLabel(block, text=system.upper(), font=("Segoe UI", 10, "bold"),
                         text_color=TEXT_MUTED).pack(anchor="w", padx=5, pady=(8, 2))

            grid = ctk.CTkFrame(block, fg_color="transparent")
            grid.pack(fill="x", padx=10)
            grid.grid_columnconfigure(0, weight=1)
            grid.grid_columnconfigure(1, weight=1)

            rows: list[tuple[str, ctk.CTkFrame]] = []
            for i, symptom in enumerate(symptom_ids):
                row_frame = ctk.CTkFrame(grid, fg_color=BG_CARD, corner_radius=6,
                                         border_width=1, border_color=BORDER_COLOR)
                row, col = divmod(i, 2)
                row_frame.grid(row=row, column=col, padx=4, pady=3, sticky="ew")

                variable = ctk.BooleanVar(value=symptom in self.selected_symptoms)
                checkbox = ctk.CTkCheckBox(
                    row_frame, text=humanize(symptom), variable=variable,
                    command=lambda s=symptom, v=variable: self._on_symptom_toggle(s, v),
                    font=("Segoe UI", 11), text_color=TEXT_PRIMARY,
                    fg_color=ACCENT_BLUE, hover_color=ACCENT_BLUE)
                checkbox.pack(side="left", padx=8, pady=6)

                severity_var = ctk.StringVar(
                    value=_SEVERITY_TITLE.get(self.selected_symptoms.get(symptom, "moderate"),
                                              "Moderate"))
                menu = ctk.CTkOptionMenu(
                    row_frame, values=SEVERITY_LABELS, variable=severity_var,
                    width=95, height=26, fg_color=BORDER_LIGHT, button_color=BG_CARD,
                    text_color=TEXT_PRIMARY,
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

        # Clear previous symptom selections so new text starts fresh.
        for widget in self.symptom_widgets.values():
            widget["var"].set(False)
            widget["menu"].pack_forget()
        self.selected_symptoms.clear()

        extraction = self.manager.analyze_text(text)
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
            session = DiagnosisSession(
                symptoms=selected,
                patient_age=age,
                temperature_c=getattr(self.last_extraction, "temperature_c", None),
                durations=getattr(self.last_extraction, "durations", {}) or {},
            )
            outcome = self.manager.diagnose(session)
        except Exception as exc:  # noqa: BLE001 - report engine failures in the UI
            self.root.after(0, lambda: self._show_engine_error(exc))
            return
        self.root.after(0, lambda: self._render_outcome(outcome))

    def _show_engine_error(self, exc):
        self.loading_bar.stop()
        self.diagnose_btn.configure(state="normal")
        messagebox.showerror("Diagnosis failed", str(exc))

    def _render_outcome(self, outcome):
        """Render a DiagnosisOutcome from the manager."""
        self.loading_bar.stop()
        self.diagnose_btn.configure(state="normal")
        self.current_results = outcome.results
        for w in self.diag_panel.winfo_children():
            w.destroy()

        if not outcome.has_results:
            ctk.CTkLabel(self.diag_panel,
                         text="No matching diseases found. Try adding more symptoms.",
                         font=("Segoe UI", 13), text_color=TEXT_MUTED).pack(pady=30)
            self.exp_text.delete("1.0", "end")
            self.triage_label.pack_forget()
            return

        for i, result in enumerate(outcome.results[:3], 1):
            self._create_diag_card(result, i)

        # Triage indicator
        color = TRIAGE_COLORS.get(outcome.triage_level, ACCENT_GREEN)
        self.triage_label.configure(text=f"  Next step: {outcome.triage_title}  ",
                                    text_color="#fff", fg_color=color)
        self.triage_label.pack(fill="x", padx=15, pady=(10, 0))

        # Explanation text
        text = outcome.explanation
        if outcome.triage_title:
            text += f"\n\nNEXT STEPS ({outcome.triage_title.upper()}):\n{outcome.triage_guidance}"
        top = outcome.top_result
        if top and top.risk_note:
            text = f"Risk note: {top.risk_note}\n\n{text}"
        self.exp_text.delete("1.0", "end")
        self.exp_text.insert("1.0", text)

    def _create_diag_card(self, result: DiagnosisResult, rank: int):
        level, color = self._likelihood(result.confidence)
        card = ctk.CTkFrame(self.diag_panel, fg_color=BG_CARD, corner_radius=8,
                            border_width=1, border_color=BORDER_COLOR)
        card.pack(fill="x", pady=6, padx=6)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(10, 4))
        ctk.CTkLabel(header, text=f"#{rank}  {result.name}",
                     font=("Segoe UI", 14, "bold"),
                     text_color=TEXT_PRIMARY).pack(side="left")
        if result.emergency:
            ctk.CTkLabel(header, text=" EMERGENCY ", text_color="#fff",
                         font=("Segoe UI", 10, "bold"),
                         fg_color=ACCENT_RED, corner_radius=4).pack(side="right", padx=5)

        progress = ctk.CTkProgressBar(card, width=350, progress_color=color,
                                      fg_color=BORDER_COLOR, height=8,
                                      corner_radius=4)
        progress.pack(fill="x", padx=14, pady=(2, 6))
        progress.set(min(result.confidence / 100.0, 1.0))

        risk = "elevated" if result.risk_note else ""
        meta = (f"Likelihood: {level}  ·  {result.confidence}%  ·  "
                f"{result.category.title()}  ·  Matched {result.matched}/{result.total}")
        if risk:
            meta += f"  ·  Age-risk: {risk}"
        ctk.CTkLabel(card, text=meta, font=("Segoe UI", 11),
                     text_color=TEXT_SECONDARY).pack(anchor="w", padx=14, pady=(0, 10))

    @staticmethod
    def _likelihood(confidence: int) -> tuple[str, str]:
        for threshold, level, color in LIKELIHOOD:
            if confidence < threshold:
                return level, color
        return "High", "#e74c3c"

    # (triage + explanation now handled by manager.diagnose() → _render_outcome)

    # ==================================================================
    # Disease info page
    # ==================================================================
    def _build_disease_info(self):
        info_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        self.frames["disease_info"] = info_frame
        ctk.CTkLabel(info_frame, text="Disease Encyclopedia",
                     font=("Segoe UI", 20, "bold"), text_color=TEXT_PRIMARY).pack(pady=15)

        main_grid = ctk.CTkFrame(info_frame, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=20, pady=10)
        main_grid.grid_columnconfigure(0, weight=1)
        main_grid.grid_columnconfigure(1, weight=2)
        main_grid.grid_rowconfigure(0, weight=1)

        list_frame = ctk.CTkFrame(main_grid, fg_color=BG_SURFACE, corner_radius=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(list_frame, text="All Diseases", font=("Segoe UI", 14, "bold"),
                     text_color=TEXT_PRIMARY).pack(pady=10)
        self.disease_listbox = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.disease_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        self.detail_frame = ctk.CTkFrame(main_grid, fg_color=BG_SURFACE, corner_radius=10)
        self.detail_frame.grid(row=0, column=1, sticky="nsew")
        self.detail_title = ctk.CTkLabel(self.detail_frame,
                                         text="Select a disease to view details",
                                         font=("Segoe UI", 16, "bold"), text_color=TEXT_MUTED)
        self.detail_title.pack(pady=40)
        self.detail_content = ctk.CTkTextbox(self.detail_frame, font=("Segoe UI", 12),
                                             wrap="word", fg_color=BG_CARD,
                                             text_color=TEXT_PRIMARY)
        self.detail_content.pack_forget()

        for disease_id in self.manager.all_diseases():
            btn = ctk.CTkButton(self.disease_listbox, text=humanize(disease_id),
                                fg_color="transparent", hover_color=BG_CARD,
                                font=("Segoe UI", 13), anchor="w", height=40,
                                command=lambda d=disease_id: self._show_disease_detail(d))
            btn.pack(fill="x", padx=5, pady=2)

    def _show_disease_detail(self, disease_id):
        defn = self.manager.disease_info(disease_id)
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
        ctk.CTkLabel(hist, text="Diagnosis History", font=("Segoe UI", 20, "bold"),
                     text_color=TEXT_PRIMARY).pack(pady=15)

        self.hist_tree = ctk.CTkFrame(hist, fg_color=BG_SURFACE, corner_radius=10)
        self.hist_tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.hist_list = ctk.CTkTextbox(self.hist_tree, font=("Segoe UI", 12), wrap="word",
                                        fg_color=BG_SURFACE, text_color=TEXT_PRIMARY)
        self.hist_list.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(hist, text="Refresh History", command=self._refresh_history,
                      fg_color=BORDER_LIGHT, text_color=TEXT_PRIMARY).pack(pady=10)
        ctk.CTkButton(hist, text="Clear History", command=self._clear_history,
                      fg_color="transparent", border_width=1, border_color=BORDER_LIGHT,
                      text_color=TEXT_SECONDARY).pack(pady=5)
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
        ctk.CTkLabel(prof, text="Patient Profile", font=("Segoe UI", 20, "bold"),
                     text_color=TEXT_PRIMARY).pack(pady=15)

        form = ctk.CTkFrame(prof, fg_color=BG_SURFACE, corner_radius=10)
        form.pack(fill="both", expand=True, padx=40, pady=10)

        self.profile_vars = {}
        fields = [("Name", "name"), ("Age", "age"), ("Gender", "gender"), ("Blood Type", "blood_type")]
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(form, text=label, font=("Segoe UI", 13),
                         text_color=TEXT_PRIMARY).grid(
                row=i, column=0, padx=20, pady=10, sticky="w")
            if key in ("gender", "blood_type"):
                values = (["Male", "Female", "Other"] if key == "gender"
                          else ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                var = ctk.StringVar()
                ctk.CTkOptionMenu(form, variable=var, values=values, width=200,
                                  fg_color=BG_CARD, text_color=TEXT_PRIMARY).grid(
                row=i, column=1, padx=20, pady=10, sticky="w")
            else:
                var = ctk.StringVar()
                ctk.CTkEntry(form, textvariable=var, width=200,
                             fg_color=BG_CARD, text_color=TEXT_PRIMARY,
                             border_color=BORDER_COLOR).grid(
                row=i, column=1, padx=20, pady=10, sticky="w")
            self.profile_vars[key] = var

        ctk.CTkLabel(form, text="Age is used to flag conditions with higher risk in your age group "
                                "(e.g. flu, pneumonia in the elderly).",
                     font=("Segoe UI", 11), text_color=TEXT_SECONDARY).grid(
            row=len(fields), column=0, columnspan=2, padx=20, pady=(0, 6), sticky="w")

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)
        ctk.CTkButton(btn_frame, text="Save Profile", command=self._save_profile,
                      fg_color=ACCENT_BLUE, text_color="#fff").pack(side="left", padx=10)

        self.saved_patients_btn = ctk.CTkButton(btn_frame, text="Saved Patients",
                                                command=self._show_saved_patients,
                                                fg_color=BORDER_LIGHT, text_color=TEXT_PRIMARY)
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
        if not name:
            name = "Guest"
        self.patient_label.configure(text=f"👤 Patient: {name}")
        if self.patient.is_guest:
            self.profile_badge.configure(text="  GUEST", fg_color=ACCENT_AMBER)
            self.guest_note.pack(side="left", padx=(8, 0))
        else:
            self.profile_badge.configure(text="  SIGNED IN", fg_color=ACCENT_GREEN)
            self.guest_note.pack_forget()

    def _update_saved_patients_button(self):
        if len(self.patient.saved_profiles) > 0:
            self.saved_patients_btn.pack(side="left", padx=10)
        else:
            self.saved_patients_btn.pack_forget()

    def _show_profile_chooser(self):
        """Open a profile chooser dialog for sign-in or switching profiles."""
        if hasattr(self, "profile_chooser_win") and self.profile_chooser_win.winfo_exists():
            self.profile_chooser_win.lift()
            return
        self.profile_chooser_win = ctk.CTkToplevel(self.root)
        self.profile_chooser_win.title("Sign In / Choose Profile")
        self.profile_chooser_win.geometry("420x520")
        self.profile_chooser_win.configure(fg_color=BG_SURFACE)
        self.profile_chooser_win.transient(self.root)
        self.profile_chooser_win.grab_set()

        ctk.CTkLabel(self.profile_chooser_win, text="Sign In / Choose Profile",
                     font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY).pack(pady=15)

        # Guest option
        guest_frame = ctk.CTkFrame(self.profile_chooser_win, fg_color=BG_CARD, corner_radius=8)
        guest_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(guest_frame, text="Continue as Guest",
                     font=("Segoe UI", 13, "bold"), text_color=TEXT_PRIMARY).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(guest_frame, text="Records won't be saved",
                     font=("Segoe UI", 10), text_color=TEXT_MUTED).pack(side="left", padx=5)
        ctk.CTkButton(guest_frame, text="Use", width=60, height=28,
                      fg_color=ACCENT_AMBER, text_color="#000",
                      command=self._choose_guest).pack(side="right", padx=10, pady=10)

        # Saved profiles
        list_frame = ctk.CTkScrollableFrame(self.profile_chooser_win, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        profiles = self.patient.saved_profiles
        if profiles:
            ctk.CTkLabel(list_frame, text="Saved Profiles:",
                         font=("Segoe UI", 13, "bold"), text_color=TEXT_SECONDARY).pack(anchor="w", pady=(5, 5))
            for i, profile in enumerate(profiles):
                name = profile.get("name", "Unknown")
                age = profile.get("age", "N/A")
                gender = profile.get("gender", "N/A")
                frame = ctk.CTkFrame(list_frame, fg_color=BG_CARD, corner_radius=8)
                frame.pack(fill="x", pady=3, padx=3)
                ctk.CTkLabel(frame, text=f"{name}  ·  Age: {age}  ·  {gender}",
                             font=("Segoe UI", 12), text_color=TEXT_PRIMARY).pack(side="left", padx=10, pady=8)
                ctk.CTkButton(frame, text="Load", width=60, height=28,
                              command=lambda idx=i: self._choose_profile(idx)).pack(side="right", padx=10, pady=8)
        else:
            ctk.CTkLabel(list_frame, text="No saved profiles yet.\nSave a profile from the Patient Profile page first.",
                         font=("Segoe UI", 12), text_color=TEXT_MUTED).pack(pady=20)

        # Create new profile shortcut
        ctk.CTkButton(self.profile_chooser_win, text="Create New Profile",
                      command=self._create_profile_from_chooser,
                      fg_color=BORDER_LIGHT, text_color=TEXT_PRIMARY, height=36).pack(pady=(5, 15), padx=15, fill="x")

    def _choose_guest(self):
        self.patient.set_guest()
        self._load_profile_data()
        self._update_patient_label()
        self._close_profile_chooser()

    def _choose_profile(self, index):
        if self.patient.switch_profile(index):
            self._load_profile_data()
            self._update_patient_label()
            self._close_profile_chooser()

    def _create_profile_from_chooser(self):
        self._close_profile_chooser()
        self.show_frame("profile")

    def _close_profile_chooser(self):
        if hasattr(self, "profile_chooser_win") and self.profile_chooser_win.winfo_exists():
            self.profile_chooser_win.destroy()

    def _show_saved_patients(self):
        if hasattr(self, "saved_patients_win") and self.saved_patients_win.winfo_exists():
            self.saved_patients_win.lift()
            return
        self.saved_patients_win = ctk.CTkToplevel(self.root)
        self.saved_patients_win.title("Saved Patients")
        self.saved_patients_win.geometry("400x500")
        self.saved_patients_win.configure(fg_color=BG_SURFACE)
        self.saved_patients_win.transient(self.root)
        self.saved_patients_win.grab_set()
        ctk.CTkLabel(self.saved_patients_win, text="Saved Patients",
                     font=("Segoe UI", 18, "bold"), text_color=TEXT_PRIMARY).pack(pady=15)

        list_frame = ctk.CTkScrollableFrame(self.saved_patients_win, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        profiles = self.patient.saved_profiles
        if not profiles:
            ctk.CTkLabel(list_frame, text="No saved patients yet.", text_color=TEXT_MUTED).pack(pady=20)
            return
        for i, profile in enumerate(profiles):
            name = profile.get("name", "Unknown")
            age = profile.get("age", "N/A")
            gender = profile.get("gender", "N/A")
            frame = ctk.CTkFrame(list_frame, fg_color=BG_CARD, corner_radius=8)
            frame.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(frame, text=f"{name}  ·  Age: {age}  ·  {gender}",
                         font=("Segoe UI", 12), text_color=TEXT_PRIMARY).pack(side="left", padx=10, pady=8)
            btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=5)
            ctk.CTkButton(btn_frame, text="Load", width=60, height=28,
                          command=lambda idx=i: self._load_patient(idx)).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="Delete", width=60, height=28, fg_color=ACCENT_RED, text_color="#fff",
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
        session = DiagnosisSession(
            symptoms=dict(self.selected_symptoms),
            temperature_c=getattr(self.last_extraction, "temperature_c", None),
            durations=getattr(self.last_extraction, "durations", {}) or {},
        )
        outcome = DiagnosisOutcome(
            results=self.current_results,
            top_disease=self.current_results[0].disease if self.current_results else None,
            explanation=self.exp_text.get("1.0", "end-1c"),
        )
        try:
            path = self.manager.export_report(
                self.export_format.get().lower(), session, outcome,
            )
        except RuntimeError as exc:  # e.g. reportlab missing
            messagebox.showerror("Export failed", str(exc))
            return
        if path:
            messagebox.showinfo("Success", f"Report saved:\n{path}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    from bootstrap import create_manager
    app = ModernMedicalGUI(manager=create_manager())
    app.run()
