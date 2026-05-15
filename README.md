# LifeGrid

A cellular automaton simulator written in Rust with a native egui GUI.

![Rust](https://img.shields.io/badge/rust-2021-orange)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Version 4.0.0](https://img.shields.io/badge/version-4.0.0-blue)

---

## Features

### Automata Modes

| Mode | Description |
|------|-------------|
| Conway's Game of Life | B3/S23 — the classic |
| HighLife | B36/S23 — supports replicators |
| Immigration | Two-color Conway variant |
| Rainbow | Six-color Conway variant |
| Langton's Ant | Turing-complete ant on a grid |
| Wireworld | 4-state electronic circuit simulation |
| Brian's Brain | 3-state firing/refractory model |
| Generations | Multi-state fading automaton |
| Hexagonal Life | Hexagonal grid with offset-row neighbours |
| Custom Rules | Arbitrary B/S rule string (e.g. `B36/S23`) |

### GUI

- **Simulation controls** — Play/Pause, single Step, Reset, configurable speed (1–200 steps/s)
- **Undo / Redo** — up to 100 states with ↩/↪ buttons
- **Pattern library** — built-in patterns per mode selected from a dropdown
- **Boundary modes** — Wrap (toroidal), Fixed (dead border), Reflect
- **Cell size** — 2–32 px per cell with a slider
- **Grid lines** — toggle on/off
- **Population graph** — real-time sparkline in the sidebar
- **Click / drag** to toggle cells on the canvas
- **PNG export** — save the current grid as a PNG snapshot
- **Persistent config** — window settings saved to `~/.config/lifegrid/lifegrid_config.json`

### Built-in Patterns (Conway modes)

Glider, Blinker, Toad, Beacon, Block, Beehive, Loaf, Boat, LWSS, MWSS,
R-Pentomino, Acorn, Pulsar, Glider Gun, Random Soup

---

## Installation

### Requirements

- Rust 1.75 or later (`rustup` recommended)
- A display server (X11 or Wayland) for the GUI window

### Quick Start

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid/lifegrid-rs
cargo run --release
```

### Build Only

```bash
cd lifegrid-rs
cargo build --release
./target/release/lifegrid
```

---

## Usage

### Keyboard / Mouse

| Action | Input |
|--------|-------|
| Toggle cell | Left-click on canvas |
| Draw cells | Click and drag |
| Play / Pause | ▶ Pause button in sidebar |
| Single step | ⏭ Step button |
| Reset | ⏹ Reset button |
| Undo | ↩ Undo button |
| Redo | ↪ Redo button |

### Custom Rules

Select **Custom Rules** from the Mode dropdown and type a rule string in
B/S notation into the text field, e.g. `B36/S23` (HighLife) or `B2/S` (Seeds).
The automaton rebuilds immediately on each keystroke.

### Exporting

Click **Export PNG** in the controls panel and choose a save location.
The PNG is written at the current cell size, so zoom in for a larger image.

---

## Project Structure

```
LifeGrid/
├── lifegrid-rs/          # Rust application
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs       # Entry point
│       ├── app.rs        # egui application, UI, event loop
│       ├── patterns.rs   # Hardcoded Conway pattern data
│       ├── export.rs     # PNG export
│       ├── automata/     # All 10 automaton implementations
│       │   ├── mod.rs    # Automaton trait + factory
│       │   ├── conway.rs
│       │   ├── highlife.rs
│       │   ├── lifelike.rs
│       │   ├── ant.rs
│       │   ├── briansbrain.rs
│       │   ├── wireworld.rs
│       │   ├── generations.rs
│       │   ├── immigration.rs
│       │   ├── rainbow.rs
│       │   └── hexagonal.rs
│       └── core/         # Grid, boundary, undo, config
│           ├── mod.rs
│           ├── grid.rs
│           ├── boundary.rs
│           ├── undo.rs
│           └── config.rs
├── LICENSE
├── README.md
├── CHANGELOG.md
└── CONTRIBUTING.md
```

---

## License

MIT — see [LICENSE](LICENSE).


![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)
![Version 3.2.0](https://img.shields.io/badge/version-3.2.0-orange)

---

## Features

### Automata Modes

| Mode | Rule / Description |
|------|--------------------|
| Conway's Game of Life | B3/S23 — the classic |
| HighLife | B36/S23 — supports replicators |
| Immigration | Two-color Conway variant |
| Rainbow | Multi-color Conway variant |
| Langton's Ant | Turing-complete ant on a grid |
| Wireworld | 4-state electronic circuit simulation |
| Brian's Brain | 3-state firing/refractory model |
| Generations | Multi-state fading automaton |
| Hexagonal Life | Hexagonal grid variant |
| Custom Rules | Arbitrary B/S rule strings |

### GUI

- **Drawing tools** — pencil, eraser, stamp, and selection with configurable brush size and shape (square / circle / diamond)
- **Simulation controls** — start, stop, step, reset, speed slider, undo/redo (up to 100 states)
- **Pattern library** — built-in patterns per mode with a pattern browser and RLE import/export
- **Themes** — light and dark themes plus a visual theme editor with custom presets
- **Generation timeline** — scrub backward and forward through simulation history
- **Population graph** — real-time population-over-time chart in the sidebar
- **Breakpoint system** — pause the simulation when population, generation, or density conditions are met
- **Rule explorer** — browse 10 named rulesets (Seeds, Day & Night, Diamoeba, etc.) and apply them instantly
- **Command palette** — `Ctrl+Shift+P` quick-access to every action
- **Pattern shape search** — draw a shape and find matching patterns by similarity
- **Grid overlays** — symmetry guides, cell age heatmaps, activity heatmaps
- **Export** — PNG snapshots, animated GIF, MP4/WebM video, JSON state, CSV statistics

### CLI

Run simulations headlessly for scripting and batch processing:

```bash
python src/cli.py --mode conway --steps 500 --export output/result.gif --fps 15
```

Supports `--mode`, `--rule` (custom B/S), `--width`, `--height`, `--cell-size`, `--export` (png/gif/mp4/webm/csv/json), `--fps`, `--snapshot-every`, and `--quiet`.

### REST & WebSocket API

Start the API server:

```bash
uvicorn src.api.app:app --reload
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/session` | Create a simulation session |
| `POST` | `/session/{id}/step` | Advance one or more generations |
| `GET` | `/session/{id}/state` | Get grid state as JSON |
| `POST` | `/session/{id}/pattern` | Load a pattern by name or RLE |
| `WS` | `/session/{id}/stream` | Stream simulation frames at ~20 Hz |
| `WS` | `/collab/{id}` | Multi-user collaborative editing |

### GPU Acceleration

Optional CUDA-based acceleration via CuPy. Falls back to NumPy automatically when no GPU is available.

```bash
pip install cupy-cuda12x   # match your CUDA version
```

### Plugin System

Drop a `.py` file into the `plugins/` directory to add a new automaton mode. See [docs/plugin_development.md](docs/plugin_development.md) for details.

Included plugin: **Day & Night** (B3678/S34678).

---

## Installation

### Requirements

- Python 3.11 or later
- Tcl/Tk (included with most Python distributions)

### Quick Start

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid
pip install -r requirements.txt
python src/main.py
```

### Development Install

```bash
make install-dev
```

This installs LifeGrid in editable mode with all optional dependencies (docs, export, dev tools).

### Build a Standalone Executable

```bash
make executable
```

Uses PyInstaller with the included `lifegrid.spec`.

---

## Usage

### GUI

```bash
python src/main.py
# or
make run
```

#### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start / Stop |
| `S` | Single step |
| `R` | Reset grid |
| `G` | Toggle grid lines |
| `C` | Clear grid |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+S` | Export PNG |
| `Ctrl+Shift+P` | Command palette |
| `D` | Toggle drawing mode |
| `B` | Open breakpoint manager |
| `+` / `-` | Zoom in / out |
| `Ctrl+Shift+R` | Open rule explorer |

### CLI

```bash
# Run Conway for 1000 steps, export animated GIF
python src/cli.py --mode conway --steps 1000 --export sim.gif

# Run HighLife with a 200x200 grid, export MP4 at 30 fps
python src/cli.py --mode highlife -W 200 -H 200 --steps 500 --export video.mp4 --fps 30

# Custom B/S rule, export CSV statistics
python src/cli.py --rule B36/S23 --steps 2000 --export stats.csv

# Run WireWorld for 1000 steps, capturing every 100th frame as an animated GIF
python src/cli.py --mode wireworld --steps 1000 --snapshot-every 100 --export sim.gif
```

### API

```bash
# Start the server
uvicorn src.api.app:app --host 0.0.0.0 --port 8000

# Create a session
curl -X POST http://localhost:8000/session \
  -H "Content-Type: application/json" \
  -d '{"width": 64, "height": 64, "mode": "conway"}'

# Step the simulation
curl -X POST http://localhost:8000/session/<id>/step \
  -H "Content-Type: application/json" \
  -d '{"steps": 10}'
```

---

## Project Structure

```
LifeGrid/
├── src/
│   ├── main.py              # GUI entry point
│   ├── cli.py               # Headless CLI
│   ├── patterns.py           # Pattern definitions
│   ├── plugin_system.py      # Plugin loader
│   ├── export_manager.py     # PNG/GIF/MP4/WebM/JSON export
│   ├── config_manager.py     # Persistent app settings
│   ├── ui_enhancements.py    # Theme manager
│   ├── automata/             # All automaton implementations
│   ├── core/                 # Simulator, config, undo, boundary modes
│   ├── gui/                  # GUI app, rendering, tools, new features
│   ├── api/                  # FastAPI REST + WebSocket + collaboration
│   ├── advanced/             # Statistics, pattern analysis, RLE, heatmaps
│   └── performance/          # GPU acceleration, benchmarking
├── plugins/                  # User-installable automaton plugins
├── tests/                    # Test suite (71 tests)
├── examples/                 # Example scripts
├── output/                   # Default export directory
└── docs/                     # Documentation
```

---

## Testing

```bash
# Run the full test suite
make test

# Run with coverage report
make coverage
```

71 tests covering the simulator, all automata modes, boundary conditions, GPU module, CLI, REST API, collaborative sessions, breakpoints, pattern system, statistics, and more.

---

## Documentation

Full documentation is in the [`docs/`](docs/) directory:

- [Installation](docs/installation.md)
- [User Guide](docs/user_guide.md)
- [CLI Reference](docs/cli_reference.md)
- [API Reference](docs/api_reference.md)
- [Architecture](docs/architecture.md)
- [Plugin Development](docs/plugin_development.md)

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Author

**Honey Badger Universe**
