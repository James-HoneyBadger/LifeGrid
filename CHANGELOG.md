# Changelog

All notable changes to LifeGrid are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.2.0] — 2026-02-19

### Added

- **Run N Steps** — new `Simulation → Run N Steps…` menu item and `N` keyboard shortcut; shows a dialog to enter a step count and runs the simulation forward in a single call.
- **F5 Randomize** — `F5` key and `Simulation → Randomize` command fill the grid with a random soup (`load_pattern("Random Soup")`).
- **Scroll-wheel zoom** — mouse scroll on the canvas adjusts cell size between 2 and 64 px without requiring the keyboard.
- **GIF export menu item** — `File → Export GIF…` invokes `ExportManager.export_gif` on the current frame buffer.
- **RLE export menu item** — `File → Export RLE…` invokes `RLEEncoder.encode_to_file` on the current grid.
- **Boundary indicator in title bar** — the window title now includes the active boundary mode, e.g. `LifeGrid — Conway's Game of Life [reflect]`.
- **AutoSave wired into GUI** — `AutoSaveManager` is started on app init and stopped cleanly on window close; autosave JSON files include generation, mode, and grid state.
- **Command palette entries** — Run N Steps, Randomize, Export GIF, and Export RLE are all searchable via `Ctrl+Shift+P`.

### Fixed

- **Boundary mode propagation** — all 10 automata (`ConwayGameOfLife`, `HighLife`, `LifeLikeAutomaton`, `Wireworld`, `BriansBrain`, `GenerationsAutomaton`, `ImmigrationGame`, `RainbowGame`, `LangtonsAnt`, `HexagonalGameOfLife`) now route neighbour convolutions through `convolve_with_boundary()`, honouring the active `wrap` / `fixed` / `reflect` setting.
- **`CellularAutomaton` base** — removed a double `reset()` call from `__init__`; added `self.boundary = "wrap"` as a guaranteed instance attribute.
- **`LifeLikeAutomaton` kernel** — moved the Moore-neighbourhood kernel to a class-level constant (`_KERNEL`) to avoid re-allocation on every step.
- **`LangtonsAnt.get_population_grid()`** — new method returns the raw cell grid without the ant-position marker, fixing over-counted population statistics.
- **`copy_selection()`** — now captures all `!= 0` states instead of only `== 1`, fixing multi-state automata copy/paste.
- **`apply_custom_rules()` silent mode** — added `silent: bool = False` parameter; preset application passes `silent=True` so switching presets no longer shows error dialogs on valid rules.
- **`step_back()` timeline sync** — after stepping back, the generation timeline slider and population graph are now updated in sync.
- **`_set_boundary()`** — propagates the selected mode to `automaton.boundary` and reflects the change in the window title.
- **Drag undo checkpoint** — `on_canvas_drag()` uses a `_drag_undo_pushed` sentinel so only one undo entry is created per drag gesture, not one per cell.
- **`SimulationState.export_metrics_csv()`** — now dynamically discovers all keys from log entries (`live`, `delta`, `density`, `entropy`, `complexity`, `cycle_period`) instead of a hard-coded set that was missing several columns.
- **`_calculate_complexity()` performance** — vectorised using `numpy.lib.stride_tricks.sliding_window_view`; eliminates the O(H×W) Python nested loop.
- **`seen_hashes` memory cap** — `SimulationState.seen_hashes` evicts the oldest 1 000 entries when the dict reaches 2 000 entries, preventing unbounded memory growth in long simulations.
- **`SimulationState` duplicate field** — removed the duplicated `is_running` dataclass field.
- **`SimulatorConfig.to_dict()`** — converts `birth_rule` and `survival_rule` sets to sorted lists so the result is JSON-serialisable.
- **Circular import** — removed `Simulator` from `core/__init__.py` to break the `core → automata → core` import cycle; callers use `from core.simulator import Simulator` directly.

### Performance

- **PIL fast-path renderer** — `rendering.py` now uses a Pillow-backed `_draw_pil_fast()` that constructs a numpy RGB pixel array and issues a single `canvas.create_image()` call when Pillow is installed and grid lines are hidden, replacing thousands of per-cell `create_rectangle()` calls.
- **`RuleDiscovery.observe_transition()`** — vectorised using `np.roll` stacking to build an `(8, H, W)` neighbourhood tensor and flatten to `(H*W, 8)` — eliminates the O(H×W) Python nested loop.

---

## [3.1.0] — 2025-06-17

### Added

- **Headless CLI** (`src/cli.py`) — run simulations from the command line with `--mode`, `--rule`, `--steps`, `--export`, `--fps`, `--snapshot-every`, and `--quiet` flags.
- **Boundary modes** — wrap (toroidal), fixed (dead edges), and reflect (mirror edges) via `BoundaryMode` enum and utility functions in `src/core/boundary.py`.
- **GPU acceleration** — optional CuPy-based CUDA acceleration with automatic NumPy fallback (`src/performance/gpu.py`).
- **Generation timeline** — scrub backward and forward through past simulation states in the GUI sidebar.
- **Population graph** — real-time population-over-time chart displayed below the canvas.
- **Breakpoint system** — pause the simulation when configurable conditions on population, generation, or density are met.
- **Rule explorer** — browse and apply 10 named Life-like rulesets (Seeds, Day & Night, Diamoeba, Morley, Anneal, 2x2, HighLife, Maze, Move, Replicator).
- **Command palette** — `Ctrl+Shift+P` quick-access overlay listing all available actions.
- **Theme editor** — visual in-app editor for creating and applying custom color themes with 3 built-in presets.
- **Pattern shape search** — draw a pattern on a mini-canvas and search the library by shape similarity.
- **Collaborative sessions** — WebSocket-based multi-user grid editing via `/collab/{id}` endpoint in the API.
- **Hexagonal Life** mode — hexagonal grid variant (`src/automata/hexagonal.py`).
- **Comprehensive test suite** — 71 tests in `tests/test_thorough.py` covering all major components.

### Fixed

- `Simulator.undo()` and `Simulator.redo()` now correctly pass `current_state` to `UndoManager`.
- GUI crash caused by mixing `pack` and `grid` geometry managers on the root window.
- `PopulationGraph._w` no longer shadows the internal `tk.Canvas._w` attribute.
- All flake8, mypy, and pylint issues resolved (0 warnings, 0 errors).

---

## [3.0.0] — 2025-06-01

### Added

- Modern Tkinter GUI with toolbar, status bar, and tabbed settings panel.
- 9 built-in automata modes (Conway, HighLife, Immigration, Rainbow, Langton's Ant, Wireworld, Brian's Brain, Generations, Custom Rules).
- Drawing tools: pencil, eraser, stamp, and selection with configurable brush size and shape.
- Pattern browser with built-in pattern library and RLE import/export.
- Light and dark themes via `ThemeManager`.
- Undo/redo system (up to 100 states) via `UndoManager`.
- Statistics collection: population, density, entropy, complexity scoring.
- Enhanced statistics: box-counting fractal dimension, connected components, cluster analysis, pattern symmetry detection, radial distribution.
- Pattern analysis: bounding box extraction, period detection, displacement detection.
- Cell age tracking with blue-to-red gradient heatmaps.
- Activity and age heatmaps via `HeatmapGenerator`.
- Symmetry detection and visualization (horizontal, vertical, rotational, diagonal, point).
- Rule discovery: observe transitions, infer B/S notation, export discovered rules.
- Export to PNG, GIF, MP4, WebM, JSON, and CSV.
- Plugin system for user-installable automaton modes.
- Day & Night plugin (B3678/S34678).
- REST API via FastAPI with session management and pattern loading.
- WebSocket streaming of simulation frames at ~20 Hz.
- Persistent settings via `AppConfig` and `settings.json`.
- Autosave manager for recovery.
- Makefile with targets for install, test, lint, format, build, docs, and more.

---

## [2.0.0] — 2025-04-15

### Added

- Multi-mode automata engine with a shared `CellularAutomaton` base class.
- Grid rendering with zoom, pan, and cell-size controls.
- Basic pattern loading from JSON.
- Configuration via `SimulatorConfig` dataclass.
- Initial project scaffolding with `pyproject.toml`, `setup.py`, `Makefile`.

---

## [1.0.0] — 2025-02-01

### Added

- Initial release with Conway's Game of Life simulation.
- Simple Tkinter canvas renderer.
- Start, stop, step, and reset controls.
