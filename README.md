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
| High Life | B36/S23 — supports replicators |
| Immigration Game | Two-color Conway variant |
| Rainbow Game | Multi-color Conway variant |
| Langton's Ant | Turing-complete ant on a grid |
| Wireworld | 4-state electronic circuit simulation |
| Brian's Brain | 3-state firing/refractory model |
| Generations | Multi-state fading automaton |
| Hexagonal Life | Hexagonal grid with offset-row neighbours |
| Custom Rules | Arbitrary B/S rule string (e.g. `B36/S23`) |

### GUI

- **Simulation controls** — Play/Pause, single Step, Reset, configurable speed (1–200 steps/s)
- **Run N steps** — run a fixed number of steps in one shot via the "Run N…" dialog
- **Undo / Redo** — up to 100 states (Ctrl+Z / Ctrl+Y)
- **Pattern library** — built-in patterns per mode selected from a dropdown
- **RLE import** — paste an RLE pattern from the clipboard directly onto the grid
- **Boundary modes** — Wrap (toroidal), Fixed (dead border), Reflect
- **Cell size** — 1–64 px per cell with a slider
- **Grid lines** — toggle on/off
- **Rounded cells** — optional rounded-corner cell rendering
- **Cell aging overlay** — cells shade warmer as they stay alive longer
- **Paint state** — choose which cell state the brush paints (for multi-state automata)
- **Population graph** — real-time sparkline in the collapsing Statistics panel
- **Status bar** — live Gen / Pop / Density% / FPS readout
- **Click / drag** to paint or erase cells on the canvas
- **Zoom** — `+` / `-` keys or the cell-size slider
- **PNG export** — save the current grid as a PNG snapshot
- **GIF export** — record simulation frames and export as an animated GIF
- **Resize Grid** — change grid dimensions at any time via the "⤢ Resize Grid…" button
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
| Toggle / paint cell | Left-click on canvas |
| Erase cell | Right-click on canvas |
| Draw cells | Click and drag |
| Play / Pause | `Space` or ▶/⏸ toolbar button |
| Single step | `S` or ⏭ toolbar button |
| Reset | `R` or ⏹ toolbar button |
| Toggle grid lines | `G` |
| Undo | `Ctrl+Z` or ↩ toolbar button |
| Redo | `Ctrl+Y` or ↪ toolbar button |
| Zoom in / out | `+` / `-` |

### Custom Rules

Select **Custom Rules** from the Mode dropdown and type a rule string in
B/S notation into the text field, e.g. `B36/S23` (HighLife) or `B2/S` (Seeds).
The automaton rebuilds immediately on each keystroke.

### Exporting

Open the **💾 Export** panel in the sidebar.

- **Export PNG…** — saves the current grid at the current cell size.
- **Record frames** — tick the checkbox before running to buffer up to 500 frames, then click **Export GIF…** to save an animated GIF.

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
