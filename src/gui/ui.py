"""Widget construction and Tk variable helpers for the GUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import tkinter as tk
from tkinter import ttk

from .config import DEFAULT_CANVAS_HEIGHT, DEFAULT_CANVAS_WIDTH, MODE_PATTERNS


# pylint: disable=too-many-instance-attributes
@dataclass
class TkVars:
    """Container for the Tkinter variables shared across widgets."""

    mode: tk.StringVar
    pattern: tk.StringVar
    speed: tk.IntVar
    grid_size: tk.StringVar
    custom_width: tk.IntVar
    custom_height: tk.IntVar
    draw_mode: tk.StringVar
    symmetry: tk.StringVar


# pylint: disable=too-many-instance-attributes
@dataclass
class Widgets:
    """References to widgets that the application interacts with later."""

    start_button: tk.Button
    pattern_combo: ttk.Combobox
    birth_entry: tk.Entry
    survival_entry: tk.Entry
    apply_rules_button: tk.Button
    gen_label: tk.Label
    population_label: tk.Label
    canvas: tk.Canvas


# pylint: disable=too-many-instance-attributes
@dataclass
class Callbacks:
    """Callback definitions for UI events."""

    switch_mode: Callable[[str], None]
    step_once: Callable[[], None]
    clear_grid: Callable[[], None]
    reset_simulation: Callable[[], None]
    load_pattern: Callable[[], None]
    save_pattern: Callable[[], None]
    load_saved_pattern: Callable[[], None]
    export_png: Callable[[], None]
    apply_custom_rules: Callable[[], None]
    size_preset_changed: Callable[[tk.Event[tk.Misc]], None]
    apply_custom_size: Callable[[], None]
    toggle_grid: Callable[[], None]
    on_canvas_click: Callable[[tk.Event[tk.Misc]], None]
    on_canvas_drag: Callable[[tk.Event[tk.Misc]], None]


def build_ui(
    root: tk.Tk,
    variables: TkVars,
    callbacks: Callbacks,
    show_export: bool,
) -> Widgets:
    """Create the Tkinter widget layout and wire up callbacks."""

    _configure_style(root)
    sidebar, content = _create_layout(root)

    pattern_combo = _add_automaton_section(
        sidebar,
        variables,
        callbacks,
        show_export,
    )
    start_button, gen_label = _add_simulation_section(
        sidebar,
        variables,
        callbacks,
    )
    population_label = _add_population_section(sidebar)
    (
        birth_entry,
        survival_entry,
        apply_rules_button,
    ) = _add_custom_rules_section(sidebar, callbacks)
    _add_grid_section(sidebar, variables, callbacks)
    _add_drawing_section(sidebar, variables)
    canvas = _add_canvas_area(content, callbacks)

    return Widgets(
        start_button=start_button,
        pattern_combo=pattern_combo,
        birth_entry=birth_entry,
        survival_entry=survival_entry,
        apply_rules_button=apply_rules_button,
        gen_label=gen_label,
        population_label=population_label,
        canvas=canvas,
    )


def _configure_style(root: tk.Tk) -> None:
    """Apply a neutral ttk theme with subtle card styling."""

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    style.configure("Card.TLabelframe", padding=8)
    style.configure("Card.TFrame", padding=8)


def _create_layout(root: tk.Tk) -> tuple[ttk.Frame, ttk.Frame]:
    """Create the shell layout and return the sidebar and content frames."""

    shell = ttk.Frame(root, padding=10)
    shell.pack(fill=tk.BOTH, expand=True)
    shell.columnconfigure(1, weight=1)
    shell.rowconfigure(0, weight=1)

    sidebar = ttk.Frame(shell, style="Card.TFrame")
    sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 10))

    content = ttk.Frame(shell)
    content.grid(row=0, column=1, sticky="nsew")
    content.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=1)

    return sidebar, content


def _add_automaton_section(
    parent: ttk.Frame,
    variables: TkVars,
    callbacks: Callbacks,
    show_export: bool,
) -> ttk.Combobox:
    """Build the automaton selection area and return the pattern combobox."""

    mode_frame = ttk.Labelframe(
        parent,
        text="Automaton",
        style="Card.TLabelframe",
    )
    mode_frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(mode_frame, text="Mode").pack(anchor=tk.W)
    mode_combo = ttk.Combobox(
        mode_frame,
        textvariable=variables.mode,
        state="readonly",
        values=list(MODE_PATTERNS.keys()),
    )
    mode_combo.pack(fill=tk.X, pady=(2, 6))
    mode_combo.bind(
        "<<ComboboxSelected>>",
        lambda _event: callbacks.switch_mode(variables.mode.get()),
    )

    ttk.Label(mode_frame, text="Pattern").pack(anchor=tk.W)
    pattern_combo = ttk.Combobox(
        mode_frame,
        textvariable=variables.pattern,
        state="readonly",
    )
    pattern_combo.pack(fill=tk.X, pady=(2, 6))
    pattern_combo.bind(
        "<<ComboboxSelected>>",
        lambda _event: callbacks.load_pattern(),
    )

    row = ttk.Frame(mode_frame)
    row.pack(fill=tk.X, pady=(4, 0))
    ttk.Button(row, text="Save", command=callbacks.save_pattern).pack(
        side=tk.LEFT,
        expand=True,
        fill=tk.X,
        padx=(0, 4),
    )
    ttk.Button(row, text="Load", command=callbacks.load_saved_pattern).pack(
        side=tk.LEFT,
        expand=True,
        fill=tk.X,
    )
    if show_export:
        ttk.Button(
            mode_frame,
            text="Export PNG",
            command=callbacks.export_png,
        ).pack(fill=tk.X, pady=(6, 0))

    return pattern_combo


def _add_simulation_section(
    parent: ttk.Frame,
    variables: TkVars,
    callbacks: Callbacks,
) -> tuple[tk.Button, ttk.Label]:
    """Add simulation controls and return start button and generation label."""

    frame = ttk.Labelframe(
        parent,
        text="Simulation",
        style="Card.TLabelframe",
    )
    frame.pack(fill=tk.X, pady=(0, 10))

    toolbar = ttk.Frame(frame)
    toolbar.pack(fill=tk.X)

    start_button = tk.Button(
        toolbar,
        text="Start",
        command=lambda: None,
        width=9,
        bg="#4caf50",
        fg="white",
        relief=tk.FLAT,
    )
    start_button.pack(side=tk.LEFT, padx=(0, 6))

    ttk.Button(
        toolbar,
        text="Step",
        command=callbacks.step_once,
        width=7,
    ).pack(
        side=tk.LEFT,
    )
    ttk.Button(
        toolbar,
        text="Clear",
        command=callbacks.clear_grid,
        width=7,
    ).pack(
        side=tk.LEFT,
        padx=(6, 0),
    )
    ttk.Button(
        toolbar,
        text="Reset",
        command=callbacks.reset_simulation,
        width=7,
    ).pack(
        side=tk.LEFT,
        padx=(6, 0),
    )

    ttk.Label(frame, text="Speed").pack(anchor=tk.W, pady=(8, 2))
    tk.Scale(
        frame,
        from_=1,
        to=100,
        orient=tk.HORIZONTAL,
        variable=variables.speed,
        length=200,
        showvalue=False,
    ).pack(fill=tk.X)

    ttk.Button(frame, text="Toggle Grid", command=callbacks.toggle_grid).pack(
        fill=tk.X,
        pady=(8, 0),
    )

    gen_label = ttk.Label(
        frame,
        text="Generation: 0",
        font=("Arial", 10, "bold"),
    )
    gen_label.pack(anchor=tk.W, pady=(8, 0))

    return start_button, gen_label


def _add_population_section(parent: ttk.Frame) -> ttk.Label:
    """Add the population stats card and return the label widget."""

    frame = ttk.Labelframe(
        parent,
        text="Population",
        style="Card.TLabelframe",
    )
    frame.pack(fill=tk.X, pady=(0, 10))
    label = ttk.Label(
        frame,
        text="Live: 0 | Δ: +0 | Peak: 0 | Density: 0.0%",
        wraplength=220,
        justify=tk.LEFT,
    )
    label.pack(anchor=tk.W)
    return label


def _add_custom_rules_section(
    parent: ttk.Frame,
    callbacks: Callbacks,
) -> tuple[ttk.Entry, ttk.Entry, ttk.Button]:
    """Add the custom rule inputs and return the relevant widgets."""

    frame = ttk.Labelframe(
        parent,
        text="Custom Rules",
        style="Card.TLabelframe",
    )
    frame.pack(fill=tk.X, pady=(0, 10))

    row = ttk.Frame(frame)
    row.pack(fill=tk.X)
    ttk.Label(row, text="B").pack(side=tk.LEFT)
    birth_entry = ttk.Entry(row, width=8)
    birth_entry.pack(side=tk.LEFT, padx=(4, 12))
    ttk.Label(row, text="S").pack(side=tk.LEFT)
    survival_entry = ttk.Entry(row, width=8)
    survival_entry.pack(side=tk.LEFT, padx=(4, 0))

    apply_button = ttk.Button(
        frame,
        text="Apply",
        command=callbacks.apply_custom_rules,
    )
    apply_button.pack(fill=tk.X, pady=(6, 0))

    return birth_entry, survival_entry, apply_button


def _add_grid_section(
    parent: ttk.Frame,
    variables: TkVars,
    callbacks: Callbacks,
) -> None:
    """Add grid configuration controls."""

    frame = ttk.Labelframe(
        parent,
        text="Grid",
        style="Card.TLabelframe",
    )
    frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(frame, text="Preset").pack(anchor=tk.W)
    size_combo = ttk.Combobox(
        frame,
        textvariable=variables.grid_size,
        state="readonly",
        values=["50x50", "100x100", "150x150", "200x200", "Custom"],
    )
    size_combo.pack(fill=tk.X, pady=(2, 6))
    size_combo.bind("<<ComboboxSelected>>", callbacks.size_preset_changed)

    row = ttk.Frame(frame)
    row.pack(fill=tk.X)
    ttk.Label(row, text="W").pack(side=tk.LEFT)
    tk.Spinbox(
        row,
        from_=10,
        to=500,
        textvariable=variables.custom_width,
        width=5,
    ).pack(side=tk.LEFT, padx=(4, 12))
    ttk.Label(row, text="H").pack(side=tk.LEFT)
    tk.Spinbox(
        row,
        from_=10,
        to=500,
        textvariable=variables.custom_height,
        width=5,
    ).pack(side=tk.LEFT, padx=(4, 0))

    ttk.Button(frame, text="Apply", command=callbacks.apply_custom_size).pack(
        fill=tk.X,
        pady=(6, 0),
    )


def _add_drawing_section(parent: ttk.Frame, variables: TkVars) -> None:
    """Add drawing tool radio buttons and symmetry selector."""

    frame = ttk.Labelframe(
        parent,
        text="Drawing",
        style="Card.TLabelframe",
    )
    frame.pack(fill=tk.X)

    ttk.Label(frame, text="Tool").pack(anchor=tk.W)
    row = ttk.Frame(frame)
    row.pack(anchor=tk.W, pady=(2, 6))
    ttk.Radiobutton(
        row,
        text="Toggle",
        variable=variables.draw_mode,
        value="toggle",
    ).pack(side=tk.LEFT)
    ttk.Radiobutton(
        row,
        text="Pen",
        variable=variables.draw_mode,
        value="pen",
    ).pack(side=tk.LEFT, padx=(8, 0))
    ttk.Radiobutton(
        row,
        text="Eraser",
        variable=variables.draw_mode,
        value="eraser",
    ).pack(side=tk.LEFT, padx=(8, 0))

    ttk.Label(frame, text="Symmetry").pack(anchor=tk.W)
    ttk.Combobox(
        frame,
        textvariable=variables.symmetry,
        state="readonly",
        values=["None", "Horizontal", "Vertical", "Both", "Radial"],
    ).pack(fill=tk.X, pady=(2, 0))


def _add_canvas_area(parent: ttk.Frame, callbacks: Callbacks) -> tk.Canvas:
    """Create the scrollable canvas area and return the canvas widget."""

    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")

    canvas = tk.Canvas(
        frame,
        bg="white",
        width=DEFAULT_CANVAS_WIDTH,
        height=DEFAULT_CANVAS_HEIGHT,
        highlightthickness=1,
        highlightbackground="#cccccc",
    )
    h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    canvas.grid(row=0, column=0, sticky=tk.NSEW)
    h_scroll.grid(row=1, column=0, sticky=tk.EW, pady=(4, 0))
    v_scroll.grid(row=0, column=1, sticky=tk.NS, padx=(4, 0))

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    canvas.bind("<Button-1>", callbacks.on_canvas_click)
    canvas.bind("<B1-Motion>", callbacks.on_canvas_drag)

    return canvas
