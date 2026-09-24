# LifeGrid

A fast, native cellular-automaton simulator built with **Rust** and **egui**.

LifeGrid runs ten classic and custom automata in a single interactive window, with pattern loading, custom B/S rules, PNG/GIF export, undo/redo, and three boundary modes.

---

## Features

- **10 built-in automata modes**
  - Conway's Game of Life
  - High Life
  - Hexagonal Life
  - Immigration Game
  - Rainbow Game
  - Langton's Ant
  - Wireworld
  - Brian's Brain
  - Generations
  - Custom Rules (any Life-like B/S notation)
- **Interactive canvas** – paint, erase, drag, zoom, and pan.
- **Built-in pattern library** – classic Conway patterns (glider, blinker, glider gun, etc.) plus random soup.
- **Custom rules** – type B/S strings such as `B36/S23` or `B2/S` and see the result immediately.
- **Boundary modes** – wrap (toroidal), fixed (dead edges), and reflect (mirror edges).
- **Export** – save a PNG snapshot or record up to 500 frames and export an animated GIF.
- **Undo / redo** – 100-state history with `Ctrl+Z` / `Ctrl+Y`.
- **Persistent config** – settings are saved to `~/.config/lifegrid/lifegrid_config.json`.
- **Cross-platform** – runs on Linux, macOS, and Windows.

---

## Screenshots

<!-- TODO: add screenshots under `docs/screenshots/` -->

---

## Prerequisites

- [Rust](https://rustup.rs/) 1.75 or later
- A C linker (`gcc` or `clang`)
  - Debian/Ubuntu: `sudo apt-get install build-essential`
  - macOS: Xcode Command Line Tools
  - Windows: `rustup` usually installs the required MSVC or MinGW toolchain
- A display server (X11 or Wayland on Linux) to show the GUI window

---

## Quick Start

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid
./run-simulation.sh
```

Or, manually:

```bash
cd LifeGrid/lifegrid-rs
cargo run --release
```

---

## Build Only

```bash
cd LifeGrid/lifegrid-rs
cargo build --release
./target/release/lifegrid
```

---

## Usage

### Keyboard & Mouse

| Action | Input |
|--------|-------|
| Toggle / paint cell | Left-click on canvas |
| Erase cell | Right-click on canvas |
| Draw multiple cells | Click and drag |
| Play / Pause | `Space` or ▶/⏸ toolbar button |
| Single step | `S` or ⏭ toolbar button |
| Reset | `R` or ⏹ toolbar button |
| Toggle grid lines | `G` |
| Undo | `Ctrl+Z` or ↩ toolbar button |
| Redo | `Ctrl+Y` or ↪ toolbar button |
| Zoom in / out | `+` / `-` |

### Custom Rules

Select **Custom Rules** from the mode dropdown and type a rule string in B/S notation into the text field, for example:

- `B36/S23` – HighLife
- `B2/S` – Seeds
- `B3/S23` – Conway's Game of Life

The automaton rebuilds immediately on each keystroke.

### Exporting

Open the 💾 **Export** panel in the sidebar:

- **Export PNG…** – saves the current grid at the current cell size.
- **Record frames** – tick the checkbox before running to buffer up to 500 frames, then click **Export GIF…** to save an animated GIF.

---

## Supported Automata

| Mode | Description |
|------|-------------|
| **Conway's Game of Life** | Classic B3/S23 Life on a square grid. |
| **High Life** | B36/S23 variant with the replicator. |
| **Hexagonal Life** | B2/S34 on an offset-coordinate hexagonal grid. |
| **Immigration Game** | Two-colour Conway variant; new cells inherit the majority colour. |
| **Rainbow Game** | Six-colour cyclic cellular automaton. |
| **Langton's Ant** | Single ant on a binary grid that turns, flips cells, and moves. |
| **Wireworld** | Four-state cellular automaton for electronic logic circuits. |
| **Brian's Brain** | Three states: off, firing, refractory. |
| **Generations** | Life-like birth/survival with N fading states. |
| **Custom Rules** | Any Life-like rule via B/S notation. |

---

## Project Structure

```text
LifeGrid/
├── lifegrid-rs/              # Rust application
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs           # Entry point
│       ├── app.rs            # egui application, UI, and event loop
│       ├── patterns.rs       # Hard-coded Conway pattern data
│       ├── export.rs         # PNG and GIF export
│       ├── automata/         # All 10 automaton implementations
│       │   ├── mod.rs        # Automaton trait + factory
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
│       └── core/             # Grid, boundary, undo, and config
│           ├── mod.rs
│           ├── grid.rs
│           ├── boundary.rs
│           ├── undo.rs
│           └── config.rs
├── run-simulation.sh         # One-command build & run script
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

---

## Roadmap

- [ ] RLE pattern import / export
- [ ] Headless CLI mode
- [ ] Plugin / custom automaton loading at runtime
- [ ] GPU-accelerated grid stepping
- [ ] Activity heatmaps and statistics panels

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, workflow, and code standards.

---

## License

MIT — see [LICENSE](LICENSE).
