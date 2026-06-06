# LifeGrid

LifeGrid is a cellular automaton sandbox with two actively maintained frontends:

- `lifegrid-rs`: native desktop app in Rust + egui
- `lifegrid-ts`: web app in TypeScript + Vite + Canvas

![Rust](https://img.shields.io/badge/rust-2021-orange)
![TypeScript](https://img.shields.io/badge/typescript-5.x-3178c6)
![LifeGrid 4.1.0](https://img.shields.io/badge/lifegrid-4.1.0-2b6cb0)
![LifeGrid TS 0.2.0](https://img.shields.io/badge/lifegrid_ts-0.2.0-0f766e)
![License MIT](https://img.shields.io/badge/license-MIT-green)

---

## Platform Overview

| Platform | Stack | Target | Entry |
|---|---|---|---|
| Native | Rust + eframe/egui | Desktop | `lifegrid-rs/src/main.rs` |
| Web | TypeScript + Vite + Canvas | Browser | `lifegrid-ts/src/main.ts` |

---

## Automata Models

### Native (`lifegrid-rs`)

- Conway's Game of Life
- High Life
- Seeds
- Day & Night
- Maze
- Hexagonal Life
- Immigration Game
- Rainbow Game
- Langton's Ant
- Wireworld
- Brian's Brain
- Generations
- Custom Rules (B/S parser)

### Web (`lifegrid-ts`)

- Conway
- High Life
- Seeds
- Day & Night
- Maze
- Wireworld
- Brian's Brain
- Immigration
- Rainbow
- Hexagonal
- Generations
- Langton's Ant

---

## Quick Start

### Native Rust App

Requirements:

- Rust 1.75+
- Desktop display server (macOS, X11, or Wayland)

Run:

```bash
cd lifegrid-rs
cargo run
```

Release build:

```bash
cd lifegrid-rs
cargo build --release
./target/release/lifegrid
```

### TypeScript Web App

Requirements:

- Node.js 18+
- npm 9+

Run dev server:

```bash
cd lifegrid-ts
npm install
npm run dev
```

Build production bundle:

```bash
cd lifegrid-ts
npm run test
npm run build
```

---

## Feature Highlights

### Native (`lifegrid-rs`)

- Play/Pause/Step/Reset controls + Run N dialog
- Undo/Redo stack
- Beginner/Advanced UI mode toggle
- Quick actions: Randomize, Center View, Fit Grid, Clear, Snapshot
- RLE import from clipboard
- PNG and GIF export
- Boundary mode selection (Wrap/Fixed/Reflect)
- Population statistics sparkline
- Cell aging and multi-state painting

### Web (`lifegrid-ts`)

- Full model picker with per-model patterns
- Play/Pause/Step/Reset + Randomize/Clear
- Undo/Redo (`Ctrl+Z`, `Ctrl+Y`, `Ctrl+Shift+Z`)
- PNG export (`E`)
- Drag draw (left) and drag erase (right)
- Pan (middle-drag), zoom (wheel / `+` / `-`)
- Center viewport (`C`) and Fit viewport (`F`)
- Minimap with click-to-jump navigation
- Generation and population counters

---

## Controls Reference

### Native (`lifegrid-rs`)

| Action | Input |
|---|---|
| Play/Pause | `Space` |
| Step | `S` |
| Reset | `R` |
| Toggle grid | `G` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` or `Ctrl+Shift+Z` |
| Zoom | `+` / `-` or mouse wheel |

### Web (`lifegrid-ts`)

| Action | Input |
|---|---|
| Play/Pause | `Space` |
| Step | `S` |
| Reset | `R` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` / `Ctrl+Shift+Z` |
| Export PNG | `E` |
| Center view | `C` |
| Fit view | `F` |
| Zoom | Mouse wheel or `+` / `-` |

---

## Repository Layout

```
LifeGrid/
├── lifegrid-rs/
│   ├── Cargo.toml
│   └── src/
│       ├── main.rs
│       ├── app.rs
│       ├── export.rs
│       ├── patterns.rs
│       ├── automata/
│       │   ├── mod.rs
│       │   ├── conway.rs
│       │   ├── highlife.rs
│       │   ├── seeds.rs
│       │   ├── daynight.rs
│       │   ├── maze.rs
│       │   ├── hexagonal.rs
│       │   ├── immigration.rs
│       │   ├── rainbow.rs
│       │   ├── ant.rs
│       │   ├── wireworld.rs
│       │   ├── briansbrain.rs
│       │   ├── generations.rs
│       │   └── lifelike.rs
│       └── core/
│           ├── mod.rs
│           ├── grid.rs
│           ├── boundary.rs
│           ├── undo.rs
│           └── config.rs
├── lifegrid-ts/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── main.ts
│       ├── style.css
│       ├── core/
│       │   ├── grid.ts
│       │   └── types.ts
│       └── automata/
│           ├── baseLifeLike.ts
│           └── models.ts
├── README.md
├── CHANGELOG.md
└── CONTRIBUTING.md
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow, checks, and coding standards.

---

## License

MIT. See [LICENSE](LICENSE).
