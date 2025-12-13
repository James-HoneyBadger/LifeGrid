# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes, too-many-public-methods
# pylint: disable=too-many-locals, too-many-statements

"""Refactored GUI application composed of focused helper modules."""

from __future__ import annotations

import csv
import json

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np

from automata import LifeLikeAutomaton
from version import __version__ as LIFEGRID_VERSION
from patterns import get_pattern_description

from .config import (
    DEFAULT_CUSTOM_BIRTH,
    DEFAULT_CUSTOM_SURVIVAL,
    DEFAULT_SPEED,
    DEFAULT_CELL_SIZE,
    MIN_CELL_SIZE,
    MAX_CELL_SIZE,
    EXPORT_COLOR_MAP,
    MAX_GRID_SIZE,
    MIN_GRID_SIZE,
    MODE_FACTORIES,
    MODE_PATTERNS,
)
from .rendering import draw_grid, symmetry_positions
from .state import SimulationState
from .ui import Callbacks, TkVars, Widgets, build_ui

try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except ImportError:
    PILImage = None  # type: ignore[assignment]
    PIL_AVAILABLE = False


def _nearest_resample_filter() -> object | None:
    """Return the Pillow nearest-neighbour filter if available."""

    if not (PIL_AVAILABLE and PILImage):
        return None
    resampling = getattr(PILImage, "Resampling", PILImage)
    return getattr(resampling, "NEAREST", None)


class AutomatonApp:
    """High-level GUI orchestrator for the cellular automaton simulator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LifeGrid")

        self.settings_file = "settings.json"
        self.settings = self._load_settings()

        self.state = SimulationState()
        self.custom_birth = set(DEFAULT_CUSTOM_BIRTH)
        self.custom_survival = set(DEFAULT_CUSTOM_SURVIVAL)
        self.custom_birth_text = "".join(
            str(n) for n in sorted(self.custom_birth)
        )
        self.custom_survival_text = "".join(
            str(n) for n in sorted(self.custom_survival)
        )
        self._load_custom_rules_from_settings()

        self.tk_vars: TkVars = self._create_variables()
        self.state.cell_size = self.tk_vars.cell_size.get()
        callbacks = Callbacks(
            switch_mode=self.switch_mode,
            step_once=self.step_once,
            step_back=self.step_back,
            load_pattern=self.load_pattern_handler,
            toggle_grid=self.toggle_grid,
            on_canvas_click=self.on_canvas_click,
            on_canvas_drag=self.on_canvas_drag,
        )
        self.widgets: Widgets = build_ui(
            root=self.root,
            variables=self.tk_vars,
            callbacks=callbacks,
        )
        self.widgets.start_button.configure(  # type: ignore[call-arg]
            command=self.toggle_simulation
        )

        self.state.show_grid = self.settings.get("show_grid", True)

        self._configure_bindings()
        self.switch_mode(self.tk_vars.mode.get())
        self._update_widgets_enabled_state()
        self._update_display()

        # Save settings on exit
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Menubar
        self._install_menubar()

    def _on_close(self) -> None:
        """Save settings and close the application."""
        self._save_settings()
        self.root.destroy()

    def _install_menubar(self) -> None:
        """Install the main application menubar."""

        def show_about() -> None:
            message = (
                f"LifeGrid v{LIFEGRID_VERSION}\n\n"
                "Interactive cellular automata workbench.\n"
                "Repo: https://github.com/James-HoneyBadger/LifeGrid\n"
            )
            messagebox.showinfo("About LifeGrid", message)

        def show_shortcuts() -> None:
            message = (
                "Keyboard shortcuts:\n\n"
                "Space  — Start/Stop\n"
                "S      — Step\n"
                "Left   — Step Back\n"
                "C      — Clear\n"
                "G      — Toggle grid\n"
            )
            messagebox.showinfo("Shortcuts", message)

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Pattern…", command=self.save_pattern)
        file_menu.add_command(
            label="Load Pattern…",
            command=self.load_saved_pattern,
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Export Metrics (CSV)…",
            command=self.export_metrics,
        )
        if PIL_AVAILABLE:
            file_menu.add_command(label="Export PNG…", command=self.export_png)
        else:
            file_menu.add_command(label="Export PNG…", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        menubar.add_cascade(label="File", menu=file_menu)

        sim_menu = tk.Menu(menubar, tearoff=0)
        # Keep vital play/step controls in the sidebar to avoid redundancy.
        sim_menu.add_command(label="Reset", command=self.reset_simulation)
        sim_menu.add_command(label="Clear", command=self.clear_grid)
        menubar.add_cascade(label="Simulation", menu=sim_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(
            label="Grid & View Settings…",
            command=self.open_simulation_settings,
        )
        settings_menu.add_separator()
        settings_menu.add_command(
            label="Custom Rules…",
            command=self.open_custom_rules_dialog,
        )
        presets_menu = tk.Menu(settings_menu, tearoff=0)
        presets_menu.add_command(
            label="Conway (B3/S23)",
            command=lambda: self.apply_rule_preset("3", "23"),
        )
        presets_menu.add_command(
            label="HighLife (B36/S23)",
            command=lambda: self.apply_rule_preset("36", "23"),
        )
        presets_menu.add_command(
            label="Seeds (B2/S∅)",
            command=lambda: self.apply_rule_preset("2", ""),
        )
        presets_menu.add_command(
            label="Life (B3/S0123456789)",
            command=lambda: self.apply_rule_preset("3", "0123456789"),
        )
        settings_menu.add_cascade(label="Rule Presets", menu=presets_menu)
        settings_menu.add_separator()
        settings_menu.add_command(
            label="Toggle Grid",
            command=self.toggle_grid,
        )
        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Shortcuts", command=show_shortcuts)
        help_menu.add_command(label="About LifeGrid", command=show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def apply_rule_preset(self, birth: str, survival: str) -> None:
        """Apply a preset by switching to Custom Rules and applying B/S."""

        if self.tk_vars.mode.get() != "Custom Rules":
            self.tk_vars.mode.set("Custom Rules")
            self.switch_mode("Custom Rules")

        self.custom_birth_text = birth.strip()
        self.custom_survival_text = survival.strip()
        self.apply_custom_rules(
            birth_text=self.custom_birth_text,
            survival_text=self.custom_survival_text,
        )

    def open_custom_rules_dialog(self) -> None:
        """Open a dialog to edit and apply custom life-like B/S rules."""

        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Rules")
        dialog.transient(self.root)
        dialog.grab_set()

        container = ttk.Frame(dialog, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        dialog.rowconfigure(0, weight=1)
        dialog.columnconfigure(0, weight=1)

        ttk.Label(container, text="Birth (B)").grid(
            row=0,
            column=0,
            sticky="w",
        )
        birth_var = tk.StringVar(value=self.custom_birth_text)
        birth_entry = ttk.Entry(container, textvariable=birth_var, width=20)
        birth_entry.grid(row=1, column=0, sticky="ew", pady=(2, 10))

        ttk.Label(container, text="Survival (S)").grid(
            row=2,
            column=0,
            sticky="w",
        )
        survival_var = tk.StringVar(value=self.custom_survival_text)
        survival_entry = ttk.Entry(
            container,
            textvariable=survival_var,
            width=20,
        )
        survival_entry.grid(row=3, column=0, sticky="ew", pady=(2, 10))

        hint = (
            "Use digits 0-8. Examples:\n"
            "Conway: B3 / S23\n"
            "HighLife: B36 / S23\n"
            "Seeds: B2 / S∅"
        )
        ttk.Label(container, text=hint, justify=tk.LEFT).grid(
            row=4,
            column=0,
            sticky="w",
            pady=(0, 12),
        )

        buttons = ttk.Frame(container)
        buttons.grid(row=5, column=0, sticky="e")

        def apply_from_dialog() -> None:
            if self.tk_vars.mode.get() != "Custom Rules":
                self.tk_vars.mode.set("Custom Rules")
                self.switch_mode("Custom Rules")
            self.custom_birth_text = birth_var.get().strip()
            self.custom_survival_text = survival_var.get().strip()
            self.apply_custom_rules(
                birth_text=self.custom_birth_text,
                survival_text=self.custom_survival_text,
            )

        apply_btn = ttk.Button(
            buttons,
            text="Apply",
            command=apply_from_dialog,
        )
        apply_btn.grid(row=0, column=0, padx=(0, 8))
        close_btn = ttk.Button(buttons, text="Close", command=dialog.destroy)
        close_btn.grid(row=0, column=1)

        container.columnconfigure(0, weight=1)
        dialog.bind("<Escape>", lambda _e: dialog.destroy())
        birth_entry.focus_set()

    def open_simulation_settings(self) -> None:
        """Open a small dialog to adjust simulation parameters."""

        dialog = tk.Toplevel(self.root)
        dialog.title("Grid & View Settings")
        dialog.transient(self.root)
        dialog.grab_set()

        container = ttk.Frame(dialog, padding=12)
        container.grid(row=0, column=0, sticky="nsew")
        dialog.rowconfigure(0, weight=1)
        dialog.columnconfigure(0, weight=1)

        # Mode/pattern, speed, and drawing controls live in the sidebar.
        grid_size_var = tk.StringVar(value=self.tk_vars.grid_size.get())
        custom_w_var = tk.IntVar(value=self.tk_vars.custom_width.get())
        custom_h_var = tk.IntVar(value=self.tk_vars.custom_height.get())
        cell_size_var = tk.IntVar(value=self.tk_vars.cell_size.get())
        show_grid_var = tk.BooleanVar(value=bool(self.state.show_grid))

        # Grid
        ttk.Label(container, text="Grid Preset").grid(
            row=0,
            column=0,
            sticky="w",
        )
        grid_combo = ttk.Combobox(
            container,
            textvariable=grid_size_var,
            state="readonly",
            values=["50x50", "100x100", "150x150", "200x200", "Custom"],
            width=16,
        )
        grid_combo.grid(row=1, column=0, sticky="w", pady=(2, 6))

        grid_dims = ttk.Frame(container)
        grid_dims.grid(row=2, column=0, sticky="w", pady=(0, 10))
        ttk.Label(grid_dims, text="W").grid(row=0, column=0, sticky="w")
        w_spin = tk.Spinbox(
            grid_dims,
            from_=MIN_GRID_SIZE,
            to=MAX_GRID_SIZE,
            textvariable=custom_w_var,
            width=6,
        )
        w_spin.grid(row=0, column=1, sticky="w", padx=(4, 10))
        ttk.Label(grid_dims, text="H").grid(row=0, column=2, sticky="w")
        h_spin = tk.Spinbox(
            grid_dims,
            from_=MIN_GRID_SIZE,
            to=MAX_GRID_SIZE,
            textvariable=custom_h_var,
            width=6,
        )
        h_spin.grid(row=0, column=3, sticky="w", padx=(4, 0))

        # Cell size
        ttk.Label(container, text="Cell Size").grid(
            row=3,
            column=0,
            sticky="w",
        )
        cell_spin = tk.Spinbox(
            container,
            from_=MIN_CELL_SIZE,
            to=MAX_CELL_SIZE,
            textvariable=cell_size_var,
            width=6,
        )
        cell_spin.grid(row=4, column=0, sticky="w", pady=(2, 10))

        show_grid_check = ttk.Checkbutton(
            container,
            text="Show Grid Lines",
            variable=show_grid_var,
        )
        show_grid_check.grid(row=5, column=0, sticky="w", pady=(0, 12))

        buttons = ttk.Frame(container)
        buttons.grid(row=6, column=0, sticky="e")

        def apply_settings() -> None:
            # Grid preset/custom size
            self.tk_vars.grid_size.set(grid_size_var.get())
            self.tk_vars.custom_width.set(int(custom_w_var.get()))
            self.tk_vars.custom_height.set(int(custom_h_var.get()))
            if grid_size_var.get() == "Custom":
                self.apply_custom_grid_size()
            else:
                self.on_size_preset_change(
                    tk.Event()  # type: ignore[call-arg]
                )

            # Cell size
            self.tk_vars.cell_size.set(int(cell_size_var.get()))
            self.apply_cell_size()

            # View
            self.state.show_grid = bool(show_grid_var.get())
            self._update_display()

        apply_btn = ttk.Button(buttons, text="Apply", command=apply_settings)
        apply_btn.grid(row=0, column=0, padx=(0, 8))
        close_btn = ttk.Button(buttons, text="Close", command=dialog.destroy)
        close_btn.grid(row=0, column=1)

        container.columnconfigure(0, weight=1)
        dialog.bind("<Escape>", lambda _e: dialog.destroy())

    # ------------------------------------------------------------------
    # Variable and widget helpers
    # ------------------------------------------------------------------
    def _load_settings(self) -> dict:
        """Load user settings from file."""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)  # type: ignore[no-any-return]
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_settings(self) -> None:
        """Save current settings to file."""
        settings = {
            "mode": self.tk_vars.mode.get(),
            "pattern": self.tk_vars.pattern.get(),
            "speed": self.tk_vars.speed.get(),
            "grid_size": self.tk_vars.grid_size.get(),
            "custom_width": self.tk_vars.custom_width.get(),
            "custom_height": self.tk_vars.custom_height.get(),
            "cell_size": self.tk_vars.cell_size.get(),
            "draw_mode": self.tk_vars.draw_mode.get(),
            "symmetry": self.tk_vars.symmetry.get(),
            "show_grid": self.state.show_grid,
            "custom_birth": self.custom_birth_text,
            "custom_survival": self.custom_survival_text,
        }
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
        except OSError:
            pass  # Silently fail if can't save

    def _create_variables(self) -> TkVars:
        settings = self.settings

        # Ensure we always start from a valid default on cold start.
        default_mode = "Conway's Game of Life"
        default_pattern = "Classic Mix"

        requested_mode = settings.get("mode", default_mode)
        valid_modes = set(MODE_FACTORIES.keys()) | {"Custom Rules"}
        mode = (
            requested_mode
            if requested_mode in valid_modes
            else default_mode
        )

        available_patterns = MODE_PATTERNS.get(mode, ["Empty"])
        requested_pattern = settings.get("pattern", default_pattern)
        pattern = (
            requested_pattern
            if requested_pattern in available_patterns
            else available_patterns[0]
        )

        return TkVars(
            mode=tk.StringVar(value=mode),
            pattern=tk.StringVar(value=pattern),
            speed=tk.IntVar(value=settings.get("speed", DEFAULT_SPEED)),
            grid_size=tk.StringVar(value=settings.get("grid_size", "100x100")),
            custom_width=tk.IntVar(value=settings.get("custom_width", 100)),
            custom_height=tk.IntVar(value=settings.get("custom_height", 100)),
            cell_size=tk.IntVar(
                value=settings.get("cell_size", DEFAULT_CELL_SIZE)
            ),
            draw_mode=tk.StringVar(value=settings.get("draw_mode", "toggle")),
            symmetry=tk.StringVar(value=settings.get("symmetry", "None")),
        )

    def _load_custom_rules_from_settings(self) -> None:
        """Load custom B/S rule strings from settings if present."""

        birth = self.settings.get("custom_birth")
        survival = self.settings.get("custom_survival")
        if isinstance(birth, str):
            self.custom_birth_text = birth.strip()
        if isinstance(survival, str):
            self.custom_survival_text = survival.strip()

        # Try to prime the rule sets as well.
        try:
            self.custom_birth = {
                int(ch) for ch in self.custom_birth_text if ch.isdigit()
            }
            self.custom_survival = {
                int(ch) for ch in self.custom_survival_text if ch.isdigit()
            }
        except ValueError:
            self.custom_birth = set(DEFAULT_CUSTOM_BIRTH)
            self.custom_survival = set(DEFAULT_CUSTOM_SURVIVAL)
            self.custom_birth_text = "".join(
                str(n) for n in sorted(self.custom_birth)
            )
            self.custom_survival_text = "".join(
                str(n) for n in sorted(self.custom_survival)
            )

    def _snapshot_grid(self) -> None:
        """Store a copy of the current grid for backward stepping."""

        automaton = self.state.current_automaton
        if automaton and hasattr(automaton, "grid"):
            self.state.grid_history.append(
                np.copy(automaton.grid)  # type: ignore[attr-defined]
            )

    def _reset_history_with_current_grid(self) -> None:
        """Clear history and seed it with the current grid."""

        self.state.grid_history.clear()
        self._snapshot_grid()

    def _update_pattern_description(self) -> None:
        """Show a short description for the selected pattern if available."""

        mode = self.tk_vars.mode.get()
        pattern = self.tk_vars.pattern.get()
        description = get_pattern_description(mode, pattern)
        if not description:
            description = f"{pattern} pattern preset"
        self.widgets.pattern_help.config(text=description)

    def _configure_bindings(self) -> None:
        self.root.bind("<space>", lambda _event: self.toggle_simulation())
        self.root.bind("<Key-s>", lambda _event: self.step_once())
        self.root.bind("<Key-S>", lambda _event: self.step_once())
        self.root.bind("<Key-Left>", lambda _event: self.step_back())
        self.root.bind("<Key-c>", lambda _event: self.clear_grid())
        self.root.bind("<Key-C>", lambda _event: self.clear_grid())
        self.root.bind("<Key-g>", lambda _event: self.toggle_grid())
        self.root.bind("<Key-G>", lambda _event: self.toggle_grid())

    def _update_widgets_enabled_state(self) -> None:
        # Custom-rules controls are now in the Settings menu.
        return

    # ------------------------------------------------------------------
    # Automaton control
    # ------------------------------------------------------------------
    def switch_mode(self, mode_name: str) -> None:
        """Switch to the requested automaton mode and refresh the grid."""

        self.stop_simulation()
        if mode_name == "Custom Rules":
            automaton = LifeLikeAutomaton(
                self.state.grid_width,
                self.state.grid_height,
                self.custom_birth,
                self.custom_survival,
            )
            self.state.current_automaton = automaton
        else:
            factory = MODE_FACTORIES.get(mode_name)
            if factory is None:
                raise ValueError(f"Unsupported mode: {mode_name}")
            self.state.current_automaton = factory(
                self.state.grid_width,
                self.state.grid_height,
            )

        patterns = MODE_PATTERNS.get(mode_name, ["Empty"])
        self.widgets.pattern_combo["values"] = patterns
        self.tk_vars.pattern.set(patterns[0])

        automaton = self.state.current_automaton  # type: ignore[assignment]
        if patterns:
            first_pattern = patterns[0]
        else:
            first_pattern = "Empty"
        if first_pattern != "Empty" and hasattr(automaton, "load_pattern"):
            automaton.load_pattern(first_pattern)  # type: ignore[attr-defined]

        self.state.reset_generation()
        self._reset_history_with_current_grid()
        self._update_generation_label()
        self._update_widgets_enabled_state()
        self._update_display()
        self._update_pattern_description()

    def load_pattern_handler(self) -> None:
        """Load the currently selected pattern into the simulation grid."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        pattern_name = self.tk_vars.pattern.get()
        if pattern_name == "Empty":
            automaton.reset()
        elif hasattr(automaton, "load_pattern"):
            automaton.load_pattern(pattern_name)  # type: ignore[attr-defined]
        self.state.reset_generation()
        self._reset_history_with_current_grid()
        self._update_generation_label()
        self._update_display()
        self._update_pattern_description()

    def toggle_simulation(self) -> None:
        """Start or pause the simulation loop."""

        self.state.running = not self.state.running
        if self.state.running:
            self.widgets.start_button.config(  # type: ignore[attr-defined]
                text="Stop"
            )
            self.root.after(0, self._run_simulation_loop)
        else:
            self.widgets.start_button.config(  # type: ignore[attr-defined]
                text="Start"
            )

    def stop_simulation(self) -> None:
        """Force the simulation into a stopped state."""

        self.state.running = False
        self.widgets.start_button.config(  # type: ignore[attr-defined]
            text="Start"
        )

    def _run_simulation_loop(self) -> None:
        """Advance the automaton while the simulation is marked running."""

        if not self.state.running:
            return
        self.step_once()
        delay = max(10, 1010 - self.tk_vars.speed.get() * 10)
        self.root.after(delay, self._run_simulation_loop)

    def step_once(self) -> None:
        """Advance the automaton by a single generation."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        if not self.state.grid_history:
            self._snapshot_grid()
        automaton.step()
        self.state.generation += 1
        self._snapshot_grid()
        self._update_generation_label()
        self._update_display()

    def step_back(self) -> None:
        """Revert to the previous generation if history exists."""

        automaton = self.state.current_automaton
        history = self.state.grid_history
        if not (automaton and len(history) > 1 and hasattr(automaton, "grid")):
            return
        # Discard current snapshot and restore the previous one
        history.pop()
        previous_grid = history[-1]
        automaton.grid = np.copy(previous_grid)  # type: ignore[attr-defined]
        self.state.rebuild_stats_from_history()
        self._update_generation_label()
        self._update_display()

    def _update_generation_label(self) -> None:
        generation_text = f"Generation: {self.state.generation}"
        self.widgets.gen_label.config(  # type: ignore[attr-defined]
            text=generation_text
        )

    def reset_simulation(self) -> None:
        """Reset the automaton grid to its starting state."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        self.stop_simulation()
        automaton.reset()
        self.state.reset_generation()
        self._reset_history_with_current_grid()
        self._update_generation_label()
        self._update_display()

    def clear_grid(self) -> None:
        """Clear the grid and pause the simulation."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        self.stop_simulation()
        automaton.reset()
        self.state.reset_generation()
        self._reset_history_with_current_grid()
        self._update_generation_label()
        self._update_display()

    def apply_custom_rules(
        self,
        *,
        birth_text: str | None = None,
        survival_text: str | None = None,
    ) -> None:
        """Apply custom birth/survival rule strings to the automaton."""

        automaton = self.state.current_automaton
        if not isinstance(automaton, LifeLikeAutomaton):
            messagebox.showinfo(
                "Not Custom Mode",
                "Switch to Custom Rules to apply B/S settings.",
            )
            return

        birth_text = (
            birth_text
            if birth_text is not None
            else self.custom_birth_text
        ).strip()
        survival_text = (
            survival_text
            if survival_text is not None
            else self.custom_survival_text
        ).strip()

        # Validate input
        if not birth_text and not survival_text:
            messagebox.showerror(
                "Invalid Input",
                "At least one of birth or survival rules must be specified.",
            )
            return

        try:
            birth_set = {int(ch) for ch in birth_text if ch.isdigit()}
            survival_set = {int(ch) for ch in survival_text if ch.isdigit()}

            # Check for valid neighbor counts (0-8)
            invalid_birth = birth_set - set(range(9))
            invalid_survival = survival_set - set(range(9))
            if invalid_birth or invalid_survival:
                invalid = sorted(invalid_birth | invalid_survival)
                messagebox.showerror(
                    "Invalid Input",
                    f"Neighbor counts must be between 0-8. Invalid: {invalid}",
                )
                return

        except ValueError as exc:
            messagebox.showerror(
                "Invalid Input",
                f"Failed to parse rules: {exc}",
            )
            return

        self.custom_birth = birth_set
        self.custom_survival = survival_set
        self.custom_birth_text = birth_text
        self.custom_survival_text = survival_text
        automaton.set_rules(self.custom_birth, self.custom_survival)
        automaton.reset()
        self.state.reset_generation()
        self._reset_history_with_current_grid()
        self._update_generation_label()
        self._update_display()

        # Create user-friendly rule description
        birth_str = (
            "".join(str(n) for n in sorted(birth_set))
            if birth_set
            else "∅"
        )
        survival_str = (
            "".join(str(n) for n in sorted(survival_set))
            if survival_set
            else "∅"
        )
        rule_notation = f"B{birth_str}/S{survival_str}"

        messagebox.showinfo(
            "Rules Applied",
            f"Custom rule: {rule_notation}\n\n"
            f"Birth: {sorted(birth_set) if birth_set else 'Never'}\n"
            f"Survival: {sorted(survival_set) if survival_set else 'Never'}",
        )

    # ------------------------------------------------------------------
    # Grid size helpers
    # ------------------------------------------------------------------
    def on_size_preset_change(self, _event: tk.Event[tk.Misc]) -> None:
        """Resize the grid when a preset dimension is selected."""

        preset = self.tk_vars.grid_size.get()
        if preset == "Custom":
            return
        try:
            width_str, height_str = preset.split("x", 1)
            width = int(width_str)
            height = int(height_str)
        except ValueError:
            messagebox.showerror(
                "Invalid size",
                f"Could not parse preset '{preset}'.",
            )
            return
        self.resize_grid(width, height)

    def apply_custom_grid_size(self) -> None:
        """Resize the grid based on custom width and height spinboxes."""

        self.resize_grid(
            self.tk_vars.custom_width.get(),
            self.tk_vars.custom_height.get(),
        )

    def resize_grid(self, width: int, height: int) -> None:
        """Clamp and apply a new grid size, rebuilding the automaton."""

        width = max(MIN_GRID_SIZE, min(width, MAX_GRID_SIZE))
        height = max(MIN_GRID_SIZE, min(height, MAX_GRID_SIZE))
        self.state.grid_width = width
        self.state.grid_height = height
        self.state.current_automaton = None
        self.switch_mode(self.tk_vars.mode.get())

    def apply_cell_size(self) -> None:
        """Update the rendered cell size and redraw."""

        size = self.tk_vars.cell_size.get()
        size = max(MIN_CELL_SIZE, min(size, MAX_CELL_SIZE))
        self.tk_vars.cell_size.set(size)
        self.state.cell_size = size
        self._update_display()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def save_pattern(self) -> None:
        """Persist the current grid and rules to a JSON file."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not filename:
            return
        grid = automaton.get_grid()
        payload = {
            "mode": self.tk_vars.mode.get(),
            "width": self.state.grid_width,
            "height": self.state.grid_height,
            "grid": grid.tolist(),
        }
        if isinstance(automaton, LifeLikeAutomaton):
            payload["birth"] = sorted(automaton.birth)
            payload["survival"] = sorted(automaton.survival)
        try:
            with open(filename, "w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            messagebox.showinfo("Saved", "Pattern saved successfully.")
        except OSError as exc:
            messagebox.showerror(
                "Save Failed",
                f"Could not save pattern: {exc}",
            )

    def load_saved_pattern(self) -> None:
        """Load a pattern JSON file into the active automaton."""

        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror(
                "Load Failed",
                f"Could not read file '{filename}': {exc}",
            )
            return

        # Validate required fields
        required_fields = ["mode", "width", "height", "grid"]
        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]
        if missing_fields:
            messagebox.showerror(
                "Invalid File",
                f"Missing required fields: {missing_fields}",
            )
            return

        try:
            mode = data["mode"]
            width = int(data["width"])
            height = int(data["height"])
            grid_data = np.array(data["grid"], dtype=int)
        except (ValueError, KeyError) as exc:
            messagebox.showerror(
                "Invalid Data",
                f"Invalid data format: {exc}",
            )
            return

        # Validate dimensions
        if (
            width < 10
            or width > MAX_GRID_SIZE
            or height < 10
            or height > MAX_GRID_SIZE
        ):
            messagebox.showerror(
                "Invalid Size",
                (
                    "Grid size must be between 10x10 and "
                    f"{MAX_GRID_SIZE}x{MAX_GRID_SIZE}"
                ),
            )
            return

        # Validate grid data
        expected_size = width * height
        if grid_data.size != expected_size:
            messagebox.showerror(
                "Invalid Grid",
                (
                    f"Grid data size ({grid_data.size}) doesn't match "
                    f"dimensions ({width}x{height} = {expected_size})"
                ),
            )
            return

        self.state.grid_width = width
        self.state.grid_height = height
        self.tk_vars.mode.set(mode)
        self.switch_mode(mode)

        automaton = self.state.current_automaton
        if isinstance(automaton, LifeLikeAutomaton):
            birth = data.get("birth", [])
            survival = data.get("survival", [])
            try:
                birth_set = {int(value) for value in birth}
                survival_set = {int(value) for value in survival}
                self.custom_birth = birth_set
                self.custom_survival = survival_set
                self.custom_birth_text = "".join(
                    str(n) for n in sorted(self.custom_birth)
                )
                self.custom_survival_text = "".join(
                    str(n) for n in sorted(self.custom_survival)
                )
                automaton.set_rules(birth_set, survival_set)
            except (ValueError, TypeError):
                messagebox.showwarning(
                    "Invalid Rules",
                    "Could not load custom rules, using defaults.",
                )

        try:
            expected_shape = (
                self.state.grid_height, self.state.grid_width
            )
            if automaton is not None and hasattr(automaton, "grid"):
                setattr(
                    automaton,
                    "grid",
                    grid_data.reshape(expected_shape),
                )
        except ValueError:
            messagebox.showwarning(
                "Shape Mismatch",
                (
                    "Saved grid size did not match current settings. "
                    "Resetting grid."
                ),
            )
            if automaton is not None:
                automaton.reset()

        self.state.reset_generation()
        self._update_generation_label()
        self._update_display()
        messagebox.showinfo("Loaded", f"Pattern loaded from {filename}")

    def export_png(self) -> None:
        """Export the current grid as a Pillow PNG image."""

        if not (PIL_AVAILABLE and self.state.current_automaton and PILImage):
            messagebox.showerror(
                "Unavailable",
                "Pillow is required for PNG export.",
            )
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )
        if not filename:
            return
        grid = self.state.current_automaton.get_grid()
        image = PILImage.new(
            "RGB",
            (self.state.grid_width, self.state.grid_height),
            "white",
        )
        pixels = image.load()
        if pixels is None:
            messagebox.showerror(
                "Export Failed",
                "Could not access PNG pixel buffer.",
            )
            return
        for y in range(self.state.grid_height):
            for x in range(self.state.grid_width):
                value = int(grid[y, x])
                pixels[x, y] = EXPORT_COLOR_MAP.get(
                    value,
                    (0, 0, 0),
                )
        max_dimension = max(
            self.state.grid_width,
            self.state.grid_height,
        )
        scale = max(1, 800 // max_dimension)
        image = image.resize(
            (self.state.grid_width * scale, self.state.grid_height * scale),
            _nearest_resample_filter(),  # type: ignore[arg-type]
        )
        try:
            image.save(filename)
            messagebox.showinfo("Exported", f"PNG saved to {filename}")
        except OSError as exc:
            messagebox.showerror("Export Failed", f"Could not save PNG: {exc}")

    # ------------------------------------------------------------------
    # Rendering and interactions
    # ------------------------------------------------------------------
    def _update_display(self) -> None:
        """Redraw the canvas and population statistics."""

        automaton = self.state.current_automaton
        if not (automaton and self.widgets.canvas):
            return
        grid = automaton.get_grid()
        draw_grid(
            self.widgets.canvas,
            grid,
            self.state.cell_size,
            self.state.show_grid,
        )
        stats = self.state.update_population_stats(grid)
        self.widgets.population_label.config(  # type: ignore[attr-defined]
            text=stats
        )

    def toggle_grid(self) -> None:
        """Toggle grid line visibility and refresh the canvas."""

        self.state.show_grid = not self.state.show_grid
        self._update_display()

    def on_canvas_click(self, event: tk.Event[tk.Misc]) -> None:
        """Handle a canvas click based on the active draw mode."""

        self._handle_canvas_interaction(event)

    def on_canvas_drag(self, event: tk.Event[tk.Misc]) -> None:
        """Handle a canvas drag while the pointer button is held."""

        self._handle_canvas_interaction(event)

    def _handle_canvas_interaction(self, event: tk.Event[tk.Misc]) -> None:
        """Translate canvas coordinates into grid mutations."""

        automaton = self.state.current_automaton
        if not (automaton and self.widgets.canvas):
            return
        canvas_x = self.widgets.canvas.canvasx(event.x)
        canvas_y = self.widgets.canvas.canvasy(event.y)
        x = int(canvas_x // self.state.cell_size)
        y = int(canvas_y // self.state.cell_size)
        if 0 <= x < self.state.grid_width and 0 <= y < self.state.grid_height:
            self._apply_draw_action(x, y)
            self._update_display()

    def _apply_draw_action(self, x: int, y: int) -> None:
        """Apply the selected drawing action at the given grid coordinate."""

        automaton = self.state.current_automaton
        if not automaton:
            return
        positions = symmetry_positions(
            x,
            y,
            self.state.grid_width,
            self.state.grid_height,
            self.tk_vars.symmetry.get(),
        )
        for px, py in positions:
            within_width = 0 <= px < self.state.grid_width
            within_height = 0 <= py < self.state.grid_height
            if not (within_width and within_height):
                continue
            if self.tk_vars.draw_mode.get() == "toggle":
                automaton.handle_click(px, py)
            elif self.tk_vars.draw_mode.get() == "pen" and hasattr(
                automaton, 'grid'
            ):
                automaton.grid[py, px] = 1  # type: ignore[attr-defined]
            elif self.tk_vars.draw_mode.get() == "eraser" and hasattr(
                automaton, 'grid'
            ):
                automaton.grid[py, px] = 0  # type: ignore[attr-defined]

    def export_metrics(self) -> None:
        """Export per-generation metrics to CSV."""

        if not self.state.metrics_log:
            messagebox.showinfo(
                "No Data",
                "Run the simulation to collect metrics before exporting.",
            )
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not filename:
            return

        fieldnames = [
            "generation",
            "live",
            "delta",
            "density",
            "entropy",
            "complexity",
            "cycle_period",
        ]
        try:
            with open(filename, "w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames)
                writer.writeheader()
                for row in self.state.metrics_log:
                    writer.writerow(row)
            messagebox.showinfo("Exported", f"Metrics saved to {filename}")
        except OSError as exc:
            messagebox.showerror("Export Failed", f"Could not save CSV: {exc}")


def launch() -> None:
    """Create the Tk root window and start the simulator event loop."""

    root = tk.Tk()
    AutomatonApp(root)
    root.mainloop()
