# Changelog

All notable changes to LifeGrid are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [5.0.0] — 2026-09-24

### Added
- Native Rust/egui release build (`cargo build --release`).
- `run-simulation.sh` helper script at the repository root.

### Changed
- Documentation restored and enhanced as Markdown files.
- Version bumped to 5.0.0.

## [4.0.0] — 2026-05-15

### Changed
- Full rewrite in Rust. The entire codebase has been ported from Python/Tkinter to Rust using `eframe` and `egui` for the native GUI.
- All 10 automaton modes re-implemented as Rust structs behind a `Box<dyn Automaton>` trait object interface.
- Neighbour counting ported to pure Rust nested loops (no NumPy/SciPy dependency).
- Persistent config now stored as JSON at `~/.config/lifegrid/lifegrid_config.json`.
- Conway patterns hardcoded in `src/patterns.rs` (replaces the previous `patterns.json`).
- PNG export implemented with the `image` crate; GIF export records up to 500 frames.
- Undo/redo retained (100-state `VecDeque` in `core/undo.rs`).
- Three boundary modes retained: Wrap, Fixed, and Reflect.

### Removed
- Python source, CLI, REST/WebSocket API, plugin system, GPU acceleration, autosave, Sphinx docs, Makefile, Dockerfile, and all Python packaging files.

## [3.2.0] — 2026-02-19 (Python, archived)

### Added
- **Run N Steps** dialog (`Simulation → Run N Steps…`, shortcut `N`).
- **F5 Randomize** command fills the grid with a random soup.
- Scroll-wheel zoom adjusts cell size between 2 and 64 px.
- GIF and RLE export menu items wired to `ExportManager` and `RLEEncoder`.
- Boundary mode indicator in the window title bar.
- AutoSave manager started on app init and stopped on close.
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

### Performance
- PIL fast-path renderer constructs a numpy RGB pixel array and issues a single canvas image call.
- `RuleDiscovery.observe_transition()` vectorised using `np.roll` stacking.

## [3.1.0] — 2025-06-17 (Python, archived)

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

### Fixed
- `Simulator.undo()` and `Simulator.redo()` correctly pass `current_state` to `UndoManager`.
- GUI crash caused by mixing `pack` and `grid` geometry managers.
- `PopulationGraph._w` no longer shadows the internal `tk.Canvas._w` attribute.
- All flake8, mypy, and pylint issues resolved.

## [3.0.0] — 2025-06-01 (Python, archived)

### Added
- Modern Tkinter GUI with toolbar, status bar, and tabbed settings panel.
- 9 built-in automata modes.
- Drawing tools, pattern browser, light/dark themes, undo/redo.
- Statistics, heatmaps, symmetry detection, rule discovery.
- Export to PNG, GIF, MP4, WebM, JSON, CSV.
- Plugin system (`Day & Night` included).
- FastAPI REST + WebSocket API.

## [2.0.0] — 2025-04-15 (Python, archived)

### Added
- Multi-mode automata engine with shared `CellularAutomaton` base class.
- Grid rendering with zoom and pan.
- Pattern loading from JSON.
- Configuration via `SimulatorConfig` dataclass.
- Initial project scaffolding with `pyproject.toml`, `setup.py`, `Makefile`.

## [1.0.0] — 2025-02-01 (Python, archived)

### Added
- Initial release with Conway's Game of Life.
- Simple Tkinter canvas renderer.
- Start, stop, step, and reset controls.
