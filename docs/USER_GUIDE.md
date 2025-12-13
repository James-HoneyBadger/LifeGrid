# LifeGrid — User Guide

This guide explains how to install, run, and use LifeGrid. It summarizes controls, available modes, drawing tools, and
workflow tips for saving and exporting.

## What it is
A fast, interactive simulator for cellular automata with multiple modes:
- Conway's Game of Life
- High Life (B36/S23)
- Immigration Game (multi-state colors)
- Rainbow Game (6 colors)
- Langton's Ant
- Custom Rules (life-like B/S rules)

LifeGrid is written in Python with Tkinter and NumPy (SciPy optional for
speed) and exports PNG snapshots when Pillow is installed.

---

## Installation

Requirements:
- Python 3.13+
- NumPy
- SciPy (for fast convolution-based neighbor counting)
- Pillow (optional, for PNG export)

Install from the repo root:
```bash
pip install -r requirements.txt
```

If you use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows (PowerShell)
pip install -r requirements.txt
```

---

## Running the app
From the repo root:
```bash
python src/main.py
```

Or use the helper script:
```bash
./run.sh
```

---

## UI overview
LifeGrid is organized around a **minimal left sidebar** for vital controls
and a **menu bar** for everything else.

### Left sidebar (vital controls)
- **Automaton**
  - Mode: choose an automaton.
  - Pattern: choose a preset (loads immediately).
  - Pattern description: a short explanation of the selected preset.
- **Simulation**
  - Start/Stop (`Space`)
  - Step (`S`)
  - Back (Step Back, `Left Arrow`) — rewinds using a short snapshot history.
  - Speed slider (1–100)
  - Generation label
- **Population**
  - A compact summary label (live cells, delta, peak, density)
- **Drawing**
  - Tool: Toggle / Pen / Eraser
  - Symmetry: None / Horizontal / Vertical / Both / Radial

### Menu bar (everything else)
- **File**: Save/Load pattern JSON, export CSV metrics, export PNG.
- **Simulation**: Reset and Clear.
- **Settings**: Grid & View Settings, Custom Rules editor + presets, Toggle Grid.
- **Help**: shortcuts + About.

Canvas: The large area on the right renders the automaton.

---

## Modes and patterns
- Conway's Game of Life
  - Patterns: Classic Mix, Glider Gun, Spaceships, Oscillators, Puffers, R-Pentomino, Acorn, Random Soup
- High Life (B36/S23)
  - Patterns: Replicator, Random Soup
- Immigration Game
  - Patterns: Color Mix, Random Soup
- Rainbow Game
  - Patterns: Rainbow Mix, Random Soup
- Langton's Ant
  - Patterns: Empty
- Custom Rules
  - Patterns: Random Soup (start and then set rules)

Note: When switching modes, the first pattern in the list is selected by default and may automatically initialize the grid for you.

---

## Drawing on the grid
- Toggle mode: Clicking a cell flips it between active/inactive.
- Pen mode: Clicking/dragging paints active cells.
- Eraser mode: Clicking/dragging clears cells.

Symmetry options mirror each action:
- Horizontal: Mirror across the vertical axis.
- Vertical: Mirror across the horizontal axis.
- Both: Four-way mirroring.
- Radial: Four-way rotation around the center.

Tip: For precise editing, pause the simulation and enable grid lines.

---

## Resizing the grid
Open **Settings → Grid & View Settings…**.

- Choose a preset (50x50, 100x100, 150x150, 200x200) or choose Custom and
  set W/H.
- Adjust **Cell Size** to change how large each cell is drawn.

Applying grid changes recreates the automaton for the new size.

---

## Saving, loading, and exporting
- Save Pattern… (File menu): Writes a JSON file with mode, width, height, and the grid state.
- Load Pattern… (File menu): Reads a JSON file created by the app and restores the state.
- Export Metrics (CSV)… (File menu): Saves per-generation metrics to CSV.
- Export PNG… (File menu): Saves a PNG image of the current grid (requires Pillow).

Tip: Keep your pattern files in the `examples/` folder for easy sharing.

---

## Performance tips
- Lower grid dimensions or increase cell size to improve rendering speed
- Use SciPy (installed via requirements.txt) for fast neighbor counting
- Hide grid lines if you want a cleaner look and slightly less draw overhead

---

## Troubleshooting
- Tkinter not found
  - Ensure you have Python with Tk support installed
- ImportError: No module named 'scipy' or 'numpy'
  - Install dependencies: `pip install -r requirements.txt`
- Export PNG button missing
  - Pillow is optional; install it with `pip install Pillow`
- Slow performance on very large grids
  - Reduce grid size or increase cell size; ensure SciPy is installed

---

## FAQ
- Can I add my own rules?
  - Yes. Use Settings → Custom Rules… (or Settings → Rule Presets). The app will
    switch to Custom Rules mode and apply the B/S values.
- Are there keyboard shortcuts?
  - Yes:
    - `Space` Start/Stop
    - `S` Step
    - `Left Arrow` Step Back
    - `C` Clear
    - `G` Toggle grid
- Can I export animations/GIFs?
  - Not yet. PNG snapshots are supported; animations can be added in the future.

Enjoy exploring patterns! If you discover interesting ones, save them and share via JSON.
