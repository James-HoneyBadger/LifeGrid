# Changelog

All notable changes to LifeGrid are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [4.1.1] — 2026-06-08

### Added

- TypeScript web app: Run N controls in the side panel for fixed-step bursts.
- TypeScript web app: `N` keyboard shortcut to trigger Run N using the configured step count.
- TypeScript web app: session persistence in `localStorage` (model, pattern, grid state, speed, zoom, viewport, generation).
- TypeScript web app: explicit Save/Load buttons for session state restore.
- TypeScript web app: boundary mode control (`Wrap`/`Fixed`/`Reflect`) with persisted selection and boundary-aware stepping.
- TypeScript web app: Vitest boundary regression tests for wrap/fixed/reflect behavior and Langton's Ant edge handling.

### Changed

- Rust native app: Langton's Ant now honors selected boundary mode (`Wrap`/`Fixed`/`Reflect`) instead of always wrapping.

---

## [4.1.0] — 2026-06-06

### Added

- New TypeScript web application in `lifegrid-ts` (Vite + strict TypeScript + Canvas renderer).
- Expanded TypeScript model support: Conway, High Life, Seeds, Day & Night, Maze,
  Wireworld, Brian's Brain, Immigration, Rainbow, Hexagonal, Generations,
  and Langton's Ant.
- TypeScript interaction system with model-aware click behavior and multi-state coloring.
- TypeScript undo/redo history (`Ctrl+Z`, `Ctrl+Y`, `Ctrl+Shift+Z`).
- TypeScript PNG export from canvas (`E` shortcut).
- TypeScript viewport controls:
  - Middle-mouse pan
  - Wheel/keyboard zoom (`+` / `-`)
  - Center view (`C`)
  - Fit to viewport (`F`)
- TypeScript minimap overlay with click-to-jump navigation.

### Changed

- Native Rust UI simplification pass:
  - text-first toolbar controls
  - reduced visual noise in side panel
  - beginner/advanced mode toggle
  - quick-action row and onboarding helper text.
- Added new Rust native models: Seeds, Day & Night, Maze.
- Added starter patterns for new Rust models to improve first-run behavior.
- Added inline mode descriptions in the native mode selector.

### Documentation

- README restructured for dual-platform architecture and current feature set.
- CONTRIBUTING updated with Rust + TypeScript workflows, checks, and model parity guidance.

## [4.0.0] — 2026-05-15

### Changed

- **Full rewrite in Rust.** The entire codebase has been ported from Python/Tkinter to
  Rust using [eframe](https://github.com/emilk/egui/tree/master/crates/eframe) and
  [egui](https://github.com/emilk/egui) for the native GUI.
- All 10 automaton modes re-implemented as Rust structs behind a `Box<dyn Automaton>`
  trait object interface.
- Neighbour counting ported to pure Rust nested loops (no NumPy/SciPy dependency).
- Persistent config now stored as JSON at `~/.config/lifegrid/lifegrid_config.json`.
- Conway patterns hardcoded in `src/patterns.rs` (replaces the missing `patterns.json`).
- PNG export implemented with the `image` crate.
- Undo/redo retained (100-state `VecDeque` in `core/undo.rs`).
- Three boundary modes (Wrap, Fixed, Reflect) retained.

### Removed

- Python source, CLI, REST/WebSocket API, plugin system, GPU acceleration, autosave,
  Sphinx docs, Makefile, Dockerfile, and all Python packaging files.

---

## [3.2.0] — 2026-02-19 *(Python, archived)*

### Added

- Run N Steps dialog (`Simulation → Run N Steps…`, shortcut `N`).
- F5 Randomize command fills the grid with a random soup.
- Scroll-wheel zoom adjusts cell size between 2 and 64 px.
- GIF and RLE export menu items wired to `ExportManager` and `RLEEncoder`.
- Boundary mode indicator in the window title bar.
- AutoSave manager started on app init, stopped on close.
- Command palette entries for all new actions.

### Fixed

- Boundary mode propagation across all 10 automata.
- `CellularAutomaton` double `reset()` call in `__init__`.
- `LifeLikeAutomaton` Moore-neighbourhood kernel moved to a class-level constant.
- `LangtonsAnt.get_population_grid()` no longer includes the ant-position marker.
- `copy_selection()` now captures all non-zero states, fixing multi-state copy/paste.
- `step_back()` timeline and population graph now synchronise correctly.
- Drag undo checkpoint creates one entry per drag gesture, not one per cell.
- `SimulationState.export_metrics_csv()` dynamically discovers all metric keys.
- `seen_hashes` memory capped at 2 000 entries with oldest-first eviction.

---

## [3.1.0] — 2025-06-17 *(Python, archived)*

### Added

- Headless CLI (`src/cli.py`).
- Boundary modes: wrap, fixed, reflect.
- Optional GPU acceleration via CuPy (`src/performance/gpu.py`).
- Generation timeline scrubber and population graph.
- Breakpoint system (pause on population/generation/density conditions).
- Rule explorer with 10 named rulesets.
- Command palette (`Ctrl+Shift+P`).
- Theme editor with 3 built-in presets.
- Pattern shape search.
- Collaborative WebSocket sessions.
- Hexagonal Life mode.
- 71-test suite in `tests/test_thorough.py`.

---

## [3.0.0] — 2025-06-01 *(Python, archived)*

### Added

- Modern Tkinter GUI with toolbar, status bar, and tabbed settings panel.
- 9 built-in automata modes.
- Drawing tools, pattern browser, light/dark themes, undo/redo.
- Statistics, heatmaps, symmetry detection, rule discovery.
- Export to PNG, GIF, MP4, WebM, JSON, CSV.
- Plugin system (Day & Night included).
- FastAPI REST + WebSocket API.

---

## [2.0.0] — 2025-04-15 *(Python, archived)*

### Added

- Multi-mode automata engine with shared `CellularAutomaton` base class.
- Grid rendering with zoom and pan.
- Pattern loading from JSON.

---

## [1.0.0] — 2025-02-01 *(Python, archived)*

### Added

- Initial release with Conway's Game of Life.
- Simple Tkinter canvas renderer.
- Start, stop, step, and reset controls.
