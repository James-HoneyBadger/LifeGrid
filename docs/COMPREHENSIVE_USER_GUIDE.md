# LifeGrid — Comprehensive User Guide

**Version:** 2.0.0  
**Last Updated:** December 2025

A complete guide to installing, running, and mastering the LifeGrid cellular automaton simulator.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Interface Guide](#interface-guide)
5. [Modes & Patterns](#modes--patterns)
6. [Drawing Tools](#drawing-tools)
7. [Custom Rules](#custom-rules)
8. [Advanced Features](#advanced-features)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Workflow Examples](#workflow-examples)
11. [Troubleshooting](#troubleshooting)
12. [Tips & Tricks](#tips--tricks)

---

## Overview

**LifeGrid** is an interactive workbench for experimenting with cellular automata—mathematical models where cells evolve according to simple rules based on their neighbors. The simulator provides:

- **9 built-in automata modes** (Conway's Game of Life, HighLife, Immigration, Rainbow, Langton's Ant, Wireworld, Brian's Brain, Generations, and Custom Rules)
- **Pattern presets** for quick exploration
- **Real-time statistics** tracking population, entropy, and complexity
- **Drawing tools** with multiple modes and symmetry options
- **Save/Load functionality** for patterns as JSON
- **PNG export** for snapshots (when Pillow is installed)
- **Backward stepping** to rewind simulation history
- **Fast convolution-based rendering** via SciPy

---

## Installation

### System Requirements

- **Python:** 3.8 or higher
- **Tkinter:** Usually bundled with Python (for the GUI)
- **NumPy 1.24+:** For grid calculations
- **SciPy 1.11+:** For fast neighbor-counting convolutions
- **Pillow 10+** (optional): For PNG export functionality

### Installation Steps

#### 1. Clone or Download the Repository

```bash
# LifeGrid Comprehensive Guide

This document combines an end-user guide and a technical reference for the LifeGrid cellular automaton workbench.

---
## Part 1 — User Guide

### 1. What is LifeGrid?
LifeGrid is a Tkinter-based desktop simulator for exploring cellular automata. It includes classic rules (Conway, HighLife, Langton's Ant), colorful multi-state variants, and a custom B/S rule editor. Features include drawing tools with symmetry, pattern presets, backward stepping, live metrics, and optional PNG export.

### 2. Installation
Requirements: Python 3.13+, Tkinter, NumPy, SciPy, Pillow (optional for PNG export).

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Running
From the repo root:
```bash
python src/main.py
```
Or:
```bash
./run.sh
```

### 4. UI Overview (sidebar → top to bottom)
- **Automaton**: Select Mode, then Pattern. Helper text shows a short description.
- **Simulation**: Start/Stop, Step, Step Back (undo one generation), Clear, Reset, Speed slider, Generation counter, Grid toggle.
- **Patterns**: Save current grid, Load JSON pattern, Export PNG (if Pillow installed).
- **Custom Rules**: Birth (B) digits, Survival (S) digits, preset buttons (Conway, HighLife, Seeds, Life), Apply Rules.
- **Grid**: Preset sizes (50–200) or custom width/height (10–500) with Apply.
- **Drawing**: Draw mode (Toggle/Pen/Eraser) and Symmetry (None, Horizontal, Vertical, Both, Radial).
- **Canvas**: Main grid area with optional grid lines.

### 5. Keyboard Shortcuts
- Space: Start/Stop
- S: Step once
- Left Arrow: Step Back
- C: Clear grid
- G: Toggle grid lines

### 6. Modes and Built-in Patterns
- Conway (B3/S23): Classic Mix, Glider Gun, Spaceships, Oscillators, Puffers, R-Pentomino, Acorn, Random Soup
- HighLife (B36/S23): Replicator, Random Soup
- Immigration: Color Mix, Random Soup
- Rainbow: Rainbow Mix, Random Soup
- Langton's Ant: Empty starter
- Custom Rules: Random Soup starter, user-defined B/S

### 7. Drawing and Symmetry
- **Toggle**: Click flips a cell.
- **Pen**: Click/drag paints live cells.
- **Eraser**: Click/drag clears cells.
- Symmetry mirrors strokes across chosen axes for fast pattern creation.

### 8. Custom Rules (B/S)
- Enter digits 0–8 for Birth (B) and Survival (S); leave blank to disable that set.
- Use preset buttons for common rules (Conway B3/S23, HighLife B36/S23, Seeds B2/S, Life B3/S0123456789).
- Click **Apply Rules** to reset and run with the new rule; history is cleared and reseeded.
- Confirmation dialog shows B#/S# notation and the parsed sets.

### 9. Patterns: Save, Load, Export
- **Save**: Writes JSON with mode, size, grid state, and metadata.
- **Load File**: Restores a saved pattern (mode, size, and grid).
- **Export PNG**: Saves a snapshot of the canvas (visible when Pillow installed).

### 10. Resizing the Grid
- Choose a preset or enter custom width/height (10–500) and click Apply. Resizing recreates the automaton and clears history.

### 11. Backward Stepping
- **Step Back** reverses one generation using stored grid snapshots (deque with max length for memory safety). Metrics are recomputed from history.

### 12. Performance Tips
- Smaller grids draw faster; hide grid lines for slight gains.
- SciPy accelerates neighbor counting for Life-like rules.
- PNG export is optional; omit Pillow if not needed.

### 13. Troubleshooting
- Missing Tkinter: install a Python build with Tk support.
- Missing numpy/scipy: `pip install -r requirements.txt`.
- PNG export button missing: install Pillow.
- Slow on large grids: reduce size or cell size, ensure SciPy is present.

---
## Part 2 — Technical Reference

### 1. Architecture Overview
- **Entry Point**: `src/main.py` creates `AutomatonApp`.
- **State**: `gui/state.py` stores generation counters, histories, and grid history (deque) for step-back.
- **GUI**: `gui/ui.py` builds widgets/styles; `gui/app.py` wires callbacks and simulation logic.
- **Rendering**: `gui/rendering.py` draws grids and symmetry helper coordinates.
- **Automata**: Implementations under `automata/` with a shared base.
- **Patterns**: `patterns.py` maps mode/pattern to coordinates plus description text.
- **Config/Registry**: `gui/config.py` registers automaton factories, defaults, and pattern lists.

### 2. Key Modules and Responsibilities
- **gui/app.py**
  - Event wiring: start/stop, step, step back, clear, reset, pattern load/save/export.
  - History: `_snapshot_grid`, `_reset_history_with_current_grid`, `step_back` (restores grid and rebuilds metrics).
  - Custom rules: `apply_custom_rules` parses B/S digits, validates 0–8, sets rules on `LifeLikeAutomaton`, resets state, and confirms notation.
  - Mode switching: `switch_mode` constructs automata via registry and seeds patterns.
  - Pattern handling: `load_pattern_handler`, `save_pattern`, `load_saved_pattern`.
  - Export: CSV metrics export (always), PNG export when Pillow is available.

- **gui/ui.py**
  - Layout: sidebar cards for automaton, simulation, population, custom rules, grid, drawing, and canvas.
  - Styling: modern light theme, accent buttons, muted helper text.
  - Widgets returned via `Widgets` dataclass for app callbacks.

- **gui/state.py**
  - Tracks generation, population/entropy/complexity histories, cycle detection, and `grid_history` (deque of numpy arrays) used by step-back.
  - `rebuild_stats_from_history` recomputes metrics after rewinding.

- **gui/rendering.py**
  - Canvas drawing for grids and optional grid lines.
  - Symmetry helpers: `symmetry_positions` returns mirrored coordinates for drawing tools.

- **automata/**
  - `base.py`: Shared interface (`step`, `handle_click`, `grid` storage where applicable).
  - `conway.py`, `highlife.py`, `immigration.py`, `rainbow.py`, `ant.py`, `lifelike.py`: Rule-specific logic; Life-like rules use NumPy (and SciPy when present) for neighbor counting.

- **patterns.py**
  - `PATTERN_DATA` holds coordinates and human-readable descriptions per mode/pattern.
  - `get_pattern_description` exposes descriptions for the UI helper label.

### 3. Design Rationale
- **Modularity**: GUI wiring (`app.py`) separated from widget creation (`ui.py`) and rendering (`rendering.py`) to keep concerns isolated.
- **Registries**: `MODE_FACTORIES` and `MODE_PATTERNS` in `config.py` centralize automaton and pattern registration for easy extension.
- **Performance**: NumPy arrays for grids; SciPy `convolve2d` used when available for fast neighbor counts; history deque size capped for memory safety.
- **Usability**: Preset patterns, rule helper text, symmetry tools, step-back, and keyboard shortcuts lower friction for experimentation.
- **Safety**: Input validation for custom rules (digits 0–8), grid size bounds (10–500), and file operations with error handling.

### 4. Control Flow (high level)
1. `main.py` -> `AutomatonApp` -> `build_ui` returns widgets.
2. Mode selection builds an automaton instance via `MODE_FACTORIES` and seeds pattern.
3. Simulation loop (start): schedules repeated `step_once` via Tk `after` using the speed variable.
4. `step_once` updates grid, metrics, display; `step_back` pops history, restores grid, rebuilds stats.
5. Drawing events route through `_apply_draw_action` with symmetry-expanded coordinates.

### 5. Data and Persistence
- **Patterns**: JSON files include mode, size, grid matrix.
- **Metrics Export**: CSV with per-generation stats (generation, live cells, deltas, peaks, density, entropy, complexity).
- **PNG Export**: Rendered canvas saved when Pillow installed (optional path).
- **Settings**: Basic window/grid toggles persisted to `settings.json` (if implemented).

### 6. Extending LifeGrid
- Add a new automaton: implement under `automata/`, expose in `__init__.py`, register in `gui/config.py` with a factory and default patterns.
- Add patterns: update `PATTERN_DATA` and `MODE_PATTERNS`; supply descriptions for UI helper text.
- Add UI controls: extend `gui/ui.py` card sections; wire callbacks in `gui/app.py`.
- Improve performance: batch draw diff-only cells; consider offscreen buffers; tune history max length.
- Testing: add pytest cases under `tests/` for new automata, rule parsing, and pattern placement.

### 7. Error Handling and Validation
- Custom rules: reject non-digit or out-of-range counts; require at least one of B or S.
- Grid sizing: enforce bounds (min 10, max 500) and reinstantiate automata safely.
- File IO: user-facing message boxes on failures for save/load/export operations.

### 8. Known Limitations / Future Ideas
- Animation/GIF export not yet available.
- Rendering draws full grid each frame (diff rendering could improve large grids).
- GUI tests are minimal; logic tests cover Conway primarily.

---
## Part 3 — Quick Reference
- Run: `python src/main.py`
- Shortcuts: Space (start/stop), S (step), Left Arrow (step back), C (clear), G (grid)
- Custom Rules: enter digits for B/S or use presets; click Apply Rules
- Save/Load: JSON patterns; Export PNG when Pillow installed
- Step Back: available when history has snapshots; rebuilds metrics after rewind

Enjoy exploring and extending LifeGrid!
- **Conway:** B3/S23 (classic Game of Life)
- **HighLife:** B36/S23 (self-replicating patterns)
- **Seeds:** B2/S (produces fractals)
- **Life:** B3/S0123456789 (rare variant)

**Apply Rules:**
- Validates and applies your custom birth/survival rules
- Resets the grid and generation counter
- Shows confirmation with B/S notation

#### 5. Grid Configuration

**Preset Sizes:**
- 50×50, 100×100, 150×150, 200×200

**Custom Size:**
- Width spinner: 10–500 cells
- Height spinner: 10–500 cells
- Apply button to set custom dimensions

**Grid Display Toggle:**
- Show/hide gridlines for cleaner visualization
- Keyboard shortcut: **G**

#### 6. Speed Control

**Speed Slider:**
- Range: 1 (slowest) to 100 (fastest)
- Controls the delay between generations in milliseconds
- Useful for complex patterns that generate slowly

#### 7. Drawing Tools

**Tool Mode:**
- **Toggle:** Click individual cells to flip their state (alive ↔ dead)
- **Pen:** Drag to activate cells (draw live cells)
- **Eraser:** Drag to deactivate cells (draw dead cells)

**Symmetry Options:**
- **None:** Draw freely without mirroring
- **Horizontal:** Mirror across the vertical axis
- **Vertical:** Mirror across the horizontal axis
- **Both:** Mirror both horizontally and vertically (4-way symmetry)
- **Radial:** Rotate and mirror in 8 directions (8-fold symmetry)

**Example Workflow:**
1. Select Pen mode and Horizontal symmetry
2. Draw on the left side of the grid
3. Changes are automatically mirrored to the right side

### Canvas Area

The large white area displays the cellular automaton:
- **Left-click** or drag to apply the current drawing tool
- **Scroll bars** (if grid exceeds visible area) to navigate
- **Gridlines** (optional) show cell boundaries
- **Cell colors** depend on the mode:
  - **Black:** Dead cell
  - **White or bright colors:** Live/active cells
  - **Modes like Immigration use multiple colors** for different cell states

---

## Modes & Patterns

### Conway's Game of Life

**Rules:** B3/S23
- A cell is born if it has exactly 3 neighbors
- A cell survives if it has 2 or 3 neighbors
- All other cells die

**Famous Patterns:**
- **Glider:** A pattern that moves diagonally (period-4)
- **Blinker:** A period-2 oscillator (3 cells in a row)
- **Block:** A stable 2×2 square (period-1, never changes)
- **Gosper Glider Gun:** A "gun" that continuously fires gliders

**Preset Patterns in LifeGrid:**
- Classic Mix
- Glider Gun
- Spaceships
- Oscillators
- Puffers
- R-Pentomino
- Acorn
- Random Soup

### High Life (B36/S23)

**Rules:** B3 or B6 / S2 or S3
- Similar to Conway but cells are also born with 6 neighbors
- Produces self-replicating patterns called "replicators"

**Preset Patterns:**
- Replicator
- Random Soup

**Interesting Behavior:**
- More chaotic than Conway; patterns grow quickly
- Self-replicating structures are rare but stunning

### Immigration Game

**Rules:** Three-state life-like with color
- Cells exist in three states: empty, color A, color B
- When a cell is born, it takes the color of the majority of its neighbors

**Preset Patterns:**
- Color Mix
- Random Soup

**Visual Effect:**
- Creates beautiful fractals with colored regions
- Great for aesthetic exploration

### Rainbow Game

**Rules:** Six-state color variant
- Cells cycle through 6 colors
- Combines elements of life-like rules with rainbow coloration

**Preset Patterns:**
- Color Mix
- Random Soup

**Use Case:**
- Demonstrates chaotic behavior with vibrant visuals

### Langton's Ant

**Rules:** Single turmite on a 2D grid
- An "ant" moves and rotates based on cell colors
- Cells flip color when the ant passes over them

**Behavior:**
- Creates intricate patterns before entering a repetitive phase
- Famous for its "highway" (emergent repeating structure)

**Pattern:** Only one preset (Langton's initial configuration)

### Wireworld

**Rules:** Four-state "electronic circuit" simulator
- **Empty:** Dead state
- **Conductor:** Neutral state
- **Electron Head:** Active moving signal
- **Electron Tail:** Following the head

**Use Case:**
- Simulate digital logic gates and circuits
- Educational tool for understanding computation

### Brian's Brain

**Rules:** Three-state (B2/S/C1)
- **Resting (dead):** Can become firing (birth)
- **Firing (alive):** Always transitions to refractory next generation
- **Refractory:** Returns to resting

**Visual Style:**
- Very organized, geometric patterns
- Great for exploring structured complexity

### Generations

**Rules:** Cells progress through aging states
- Each generation, live cells age and eventually die
- Configurable number of age states
- Creates "memory" effects in patterns

### Custom Rules

**Define Your Own Rules:**
- Enter any B/S combination (B0-8 / S0-8)
- Preset buttons for quick access to famous rules
- Real-time feedback on rule validity

**Examples:**
- B3/S23 — Conway's Game of Life
- B36/S23 — HighLife
- B2/S — Seeds
- B45/S34 — Majority rule

---

## Drawing Tools

### Basic Usage

1. **Select a Drawing Mode:**
   - Toggle, Pen, or Eraser
   
2. **Optionally Select Symmetry:**
   - None, Horizontal, Vertical, Both, or Radial
   
3. **Click or Drag on the Canvas:**
   - Single click applies the tool to one cell
   - Click-and-drag applies the tool along a line

### Drawing Modes Explained

#### Toggle Mode
- **Action:** Click flips a cell's state (alive ↔ dead)
- **Use:** Manual pattern creation, precise edits
- **Example:** Click to place a single glider

#### Pen Mode
- **Action:** Drag to activate (set alive) cells
- **Use:** Drawing continuous shapes, creating live regions
- **Example:** Draw a line of cells

#### Eraser Mode
- **Action:** Drag to deactivate (set dead) cells
- **Use:** Cleaning up patterns, removing unwanted cells
- **Example:** Clear a corridor through a dense population

### Symmetry Options Explained

#### None
- Standard drawing behavior
- Changes apply exactly where clicked
- **Use Case:** Fine-grained control

#### Horizontal
- Mirrors across the vertical center axis
- Changes on the left side are mirrored to the right
- **Use Case:** Creating symmetric patterns quickly

#### Vertical
- Mirrors across the horizontal center axis
- Changes above the center are mirrored below
- **Use Case:** Top-to-bottom symmetry

#### Both (4-Way)
- Combines horizontal and vertical mirroring
- One change affects 4 locations (quadrants)
- **Use Case:** Creating perfectly balanced patterns

#### Radial (8-Way)
- Rotational mirroring in 8 directions (45° increments)
- One change affects 8 locations around the center
- **Use Case:** Creating intricate radially-symmetric designs

### Workflow: Creating a Custom Pattern

1. Start with a clear grid (click Clear)
2. Select Pen mode and Both symmetry
3. Draw a small shape in one quadrant
4. Your shape automatically mirrors to fill the grid symmetrically
5. Click Start to run the simulation
6. Observe how your symmetric pattern evolves

---

## Custom Rules

### Understanding B/S Notation

**B** = Birth rules (dead cell becomes alive)  
**S** = Survival rules (live cell stays alive)

Each followed by digits 0–8 (neighbor counts).

### Examples

| Rule | Name | Behavior |
|------|------|----------|
| B3/S23 | Conway | Complex, long-lived patterns |
| B36/S23 | HighLife | Self-replicating structures |
| B2/S | Seeds | Explosive growth, fractals |
| B45/S34 | Majority | Spreads and fills regions |
| B/S012345678 | All Survive | Cells never die (stable blob) |

### Creating Custom Rules

1. **Switch to "Custom Rules" mode** from the Mode dropdown
2. **Enter birth digits** in the Birth field (e.g., "3" or "36")
3. **Enter survival digits** in the Survival field (e.g., "23")
4. **(Optional) Use a preset button** to quickly load a famous rule:
   - Conway
   - HighLife
   - Seeds
   - Life
5. **Click "Apply Rules"** to activate

### Validation Feedback

- **Error:** "At least one of birth or survival rules must be specified"
  - Solution: Enter at least one digit in Birth or Survival
  
- **Error:** "Neighbor counts must be between 0-8"
  - Solution: Only use digits 0–8; no other characters
  
- **Success:** Confirmation dialog shows the rule in B/S notation

### Experimentation Tips

- Start with one birth rule, e.g., B3
- Gradually add or remove survival rules
- Run a few generations to observe behavior
- Test with random soup patterns to see overall dynamics

---

## Advanced Features

### Backward Stepping

**Rewind the simulation:**
- Click the "Step Back" button, or
- Press **Left Arrow** key

**How It Works:**
- Each generation's grid is automatically saved (up to 500 generations)
- Backward stepping pops from the history and restores the previous grid
- Population metrics are recalculated to match the rewound state

**Limitations:**
- History is cleared when you modify the grid via drawing
- Limited to 500 most recent generations (memory efficiency)
- Cannot step back beyond the initial pattern

### Population Statistics & Cycle Detection

**Tracked Metrics:**
- **Population:** Live cell count per generation
- **Peak:** Maximum population in current session
- **Entropy:** Measure of cell randomness
- **Complexity:** Pattern diversity score
- **Cycle Period:** If a repeating cycle is detected

**Cycle Detection:**
- Automatically identifies periodic patterns
- Displays cycle length when found
- Useful for analyzing pattern stability

### CSV Export

**Export Metrics:**
1. Click **Export CSV** (appears when Pillow is installed)
2. Choose a save location
3. CSV file contains per-generation data:
   - Generation number
   - Population count
   - Population delta
   - Entropy
   - Complexity

**Use Case:**
- Analyze population dynamics in spreadsheets
- Create charts of behavior over time
- Compare different rules quantitatively

### PNG Export

**Save Snapshots:**
1. Pause the simulation (or step to a desired generation)
2. Click **Export PNG** (requires Pillow)
3. Choose a save location and filename
4. PNG is saved with current grid visualization

**Features:**
- Saves exact current grid state
- Gridlines optional
- Uses nearest-neighbor resampling for sharp pixels

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Toggle Start/Stop (play/pause) |
| **S** | Step once (advance one generation) |
| **Left Arrow** | Step back (rewind one generation) |
| **C** | Clear the grid |
| **G** | Toggle gridlines on/off |
| **Mouse drag** | Apply current drawing tool |

---

## Workflow Examples

### Example 1: Exploring Conway's Game of Life

1. Mode: Conway's Game of Life
2. Pattern: Classic Mix
3. Click Start to observe patterns
4. Watch for gliders, blinkers, and still lifes
5. Use Step Back to rewind interesting moments
6. Adjust speed slider if simulation runs too fast

### Example 2: Creating a Symmetric Pattern

1. Mode: Any mode
2. Grid: 100×100 (default)
3. Select Pen tool, Both (4-way) symmetry
4. Draw a small shape in the top-left quadrant
5. Observe symmetric mirroring in real-time
6. Click Start to see the symmetric pattern evolve

### Example 3: Experimenting with Custom Rules

1. Mode: Custom Rules
2. Click the "Seeds" preset (B2/S)
3. Pattern: Random Soup
4. Click Start to observe fractal-like growth
5. Click Stop and try the "HighLife" preset (B36/S23)
6. Compare how different rules affect the same initial pattern

### Example 4: Analyzing Population Dynamics

1. Mode: Conway's Game of Life
2. Pattern: R-Pentomino (a long-lived pattern)
3. Click Start and let it run for 100+ generations
4. Observe Population, Peak, and Cycle metrics
5. Use Step Back to navigate to interesting moments
6. Export CSV to analyze population trends

### Example 5: Designing a Circuit with Wireworld

1. Mode: Wireworld
2. Grid: Custom 50×50 (smaller for detailed design)
3. Draw conductors with Pen tool in straight lines
4. Place electron heads (different color) at strategic points
5. Click Start to simulate signal propagation
6. Observe how signals flow through your "circuit"

---

## Troubleshooting

### Application Won't Start

**Error:** "No module named 'tkinter'"
- **Cause:** Tkinter not bundled with your Python installation
- **Solution:** Install a Python distribution that includes Tkinter, or install separately:
  - Linux (Ubuntu/Debian): `sudo apt-get install python3-tk`
  - macOS: install a Python build that includes Tk support (or a matching `python-tk` package)

**Error:** "No module named 'numpy'" or "scipy"
- **Cause:** Dependencies not installed
- **Solution:** Run `pip install -r requirements.txt` in the project directory

### Simulation Runs Very Slowly

**Cause:** Grid size too large or speed slider set too low
- **Solution:**
  1. Reduce grid size (100×100 instead of 200×200)
  2. Increase speed slider value
  3. Disable gridlines (press G)

**Cause:** Complex pattern generating many updates
- **Solution:**
  - Let it stabilize (cycles tend to become simple)
  - Use Step Back to rewind to an earlier, simpler state

### Drawing Tool Doesn't Work

**Issue:** Changes not appearing when clicking the canvas
- **Solution:**
  1. Ensure you're not in Start mode (paused state required for drawing)
  2. Check that grid dimensions are set (apply if custom size changed)
  3. Try clicking the canvas directly, not near edges

### PNG Export Fails

**Error:** "No module named 'PIL'"
- **Cause:** Pillow not installed
- **Solution:** `pip install Pillow`

### Pattern Doesn't Load

**Error:** Pattern dropdown shows "no selection"
- **Solution:**
  1. Select a mode first (dropdown should populate)
  2. Click on a pattern name from the dropdown
  3. Pattern loads automatically

### Unsupported Rule Shows Error

**Error:** "Birth/Survival rule invalid"
- **Solution:** Ensure:
  1. Only digits 0-8 are entered
  2. At least one digit is present in Birth or Survival
  3. No spaces or special characters (except hyphens for ranges, if supported)

---

## Tips & Tricks

### 1. Speed Up Exploration

- Use preset patterns to quickly load interesting configurations
- Click Step repeatedly to advance slowly and observe details
- Use Backward Stepping to revisit interesting moments

### 2. Create Stable Patterns

- Conway's Game of Life still lifes: Block, Beehive, Loaf, Tub
- Search for oscillators with period 2, 3, or 4
- Use seeds mode to generate fractals

### 3. Maximize Learning

- Read pattern names and descriptions
- Experiment with each mode systematically
- Compare how the same initial pattern evolves under different rules
- Use cycle detection to identify long-term behavior

### 4. Optimize Performance

- Start with 100×100 grid for responsive interaction
- Disable gridlines for smooth animation
- Increase speed slider for fast-running patterns
- Use smaller grid if running on low-powered hardware

### 5. Artistic Exploration

- Symmetry tools help create aesthetically pleasing patterns
- Rainbow and Immigration modes produce colorful visuals
- Langton's Ant creates intricate "highways"
- Export PNG snapshots of interesting generations

### 6. Workflow Efficiency

- Save frequently-used patterns as JSON files
- Use keyboard shortcuts (Space, S, Left Arrow, C, G)
- Preset rules buttons in Custom mode speed up rule selection
- Keep multiple grid size presets configured

### 7. Experimental Rules

- Start with Conway (B3/S23) as a baseline
- Try B2/S (Seeds) for fractal growth
- Try B36/S23 (HighLife) for replicators
- Try B45/S34 (Majority) for spreading behavior

---

## Additional Resources

### External Links

- **Conway's Game of Life:** https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
- **Cellular Automata:** https://en.wikipedia.org/wiki/Cellular_automaton
- **Online Patterns Database:** https://www.conwaylife.com/ (LifeWiki)
- **Turmites & Ants:** https://en.wikipedia.org/wiki/Turmite

### Project Resources

- **GitHub Repository:** https://github.com/James-HoneyBadger/LifeGrid
- **Technical Reference:** See `TECHNICAL_REFERENCE.md` for architecture details
- **Development Guide:** See `DEVELOPMENT.md` for contributing changes

---

## Conclusion

LifeGrid is a powerful tool for exploring the fascinating world of cellular automata. Whether you're a student learning about complex systems, a researcher analyzing rule behavior, or an artist creating beautiful patterns, LifeGrid provides an intuitive, responsive platform for experimentation.

Start with the built-in patterns, explore the various modes, and gradually venture into custom rule creation. The possibilities are endless!

**Happy simulating!**
