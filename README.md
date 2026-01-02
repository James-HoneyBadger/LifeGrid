Repository: https://github.com/James-HoneyBadger/LifeGrid

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/build-passing-brightgreen)
![Version](https://img.shields.io/badge/version-2.1.0-purple)
git clone https://github.com/James-HoneyBadger/LifeGrid.git
## LifeGrid

An interactive Tkinter-based workbench for experimenting with cellular
automata. The simulator ships with several classic rules, a custom B/S rule
editor, drawing tools, and quick exporting to PNG.

---

## Highlights

- **Multiple automata**: Conway's Life, HighLife, Immigration, Rainbow,
  Langton's Ant, and fully custom life-like rules.
- **Pattern presets** per mode for quick experimentation.
- **Drawing tools** with toggle/pen/eraser modes plus symmetry helpers.
- **Live statistics** for population deltas, peaks, and density.
- **Save/Load** patterns as JSON and **export PNG** snapshots (when Pillow is
  installed).
- **Keyboard shortcuts**: `Space` (start/stop), `S` (step), `Left` (step back),
  `C` (clear), `G` (toggle grid).

---

## Requirements

- Python 3.13+
- Tkinter (bundled with most Python installations)
- NumPy 1.24+
- SciPy 1.11+ (used for fast convolutions)
- Pillow 10+ (optional, enables PNG export)

Install dependencies from the repository root:

```bash
pip install -r requirements.txt
```

---

## Getting Started

Run LifeGrid from the project root:

```bash
python src/main.py
```

Or use the helper script on Unix-like systems:

```bash
./run.sh
```

**Quick workflow**
1. Pick a mode from the **Mode** dropdown.
2. Choose a **Pattern** or draw on the canvas.
3. Press **Start** (or hit `Space`) to run the simulation.
4. Adjust **Speed**, drawing tools, and symmetry as needed.
5. Use **Settings → Grid & View Settings…** for grid size, cell size, and grid
  lines.
6. Save/load/export from the **File** menu.

---

## Controls at a Glance

| Action | UI Control | Shortcut |
| --- | --- | --- |
| Start/Stop simulation | Start button | `Space` |
| Step one generation | Step button | `S` |
| Step back one generation | Back button | `Left` |
| Clear grid | Simulation → Clear | `C` |
| Toggle grid lines | Settings → Toggle Grid | `G` |
| Resize grid | Settings → Grid & View Settings… | – |
| Apply custom B/S rule | Settings → Custom Rules… | – |

Mouse interactions:

- Click to toggle/draw/erase (depends on draw mode).
- Drag while in Pen or Eraser to paint continuously.
- Symmetry options mirror strokes across selected axes.

---

## Available Modes & Patterns

- **Conway's Game of Life**: Classic Mix, Glider Gun, Spaceships, Oscillators,
  Puffers, R-Pentomino, Acorn, Random Soup.
- **HighLife (B36/S23)**: Replicator, Random Soup.
- **Immigration Game**: Color Mix, Random Soup.
- **Rainbow Game**: Rainbow Mix, Random Soup.
- **Langton's Ant**: Empty.
- **Custom Rules**: Random Soup starter pattern plus editable life-like B/S
  rules via Settings.

---

## Project Structure

```
LifeGrid/
├── src/
│   ├── automata/        # Automaton implementations
│   ├── gui/             # GUI modules (app, config, state, ui, rendering)
│   └── main.py          # Thin entry point (delegates to gui.app)
├── docs/                # README-style documentation
├── examples/            # Sample patterns
├── tests/               # Unit tests
├── requirements.txt
├── run.sh
├── LICENSE
└── README.md
```

Key GUI modules:

- `gui/app.py`: High-level application orchestration.
- `gui/ui.py`: Widget construction and event wiring.
- `gui/state.py`: Mutable simulation state container.
- `gui/config.py`: Shared constants and mode registries.
- `gui/rendering.py`: Canvas drawing helpers.

---

## Development Notes

- Launch tests with `pytest`. Current coverage targets the Conway automaton;
  extending coverage for other modes is encouraged.
- `flake8` enforces an 80-character line limit; run `flake8 src tests` before
  committing.
- To add a new automaton, implement it under `src/automata/`, expose it from
  `automata/__init__.py`, and register it in `gui/config.py`.
- The GUI is intentionally modular: prefer adding features in dedicated helper
  modules rather than growing `gui/app.py`.

Further details can be found in:

- `docs/USER_GUIDE.md` – end-user walkthrough.
- `docs/DEVELOPMENT.md` – contributor guidelines and code map.

---

## License

This project is distributed under the MIT License. See the `LICENSE` file for
full terms.
