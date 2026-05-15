# Contributing to LifeGrid

Thanks for your interest in contributing! This guide covers setup, workflow, and standards.

---

## Development Setup

### Prerequisites

- Rust 1.75 or later — install via [rustup](https://rustup.rs)
- A C linker (`gcc` or `clang`) — on Debian/Ubuntu: `sudo apt-get install build-essential`
- A display server (X11 or Wayland) to run the GUI

### Clone and Build

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid/lifegrid-rs
cargo build
```

Run in development mode:

```bash
cargo run
```

Build an optimised release binary:

```bash
cargo build --release
./target/release/lifegrid
```

---

## Workflow

1. **Fork and clone** the repository.
2. **Create a branch** from `master`:
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make your changes** — keep commits focused and well-described.
4. **Run checks** before submitting:
   ```bash
   cargo test          # unit tests
   cargo clippy        # lints
   cargo fmt --check   # formatting
   ```
5. **Open a pull request** against `master`.

---

## Code Standards

- **Formatting**: `cargo fmt` (rustfmt defaults). No unformatted code is accepted.
- **Linting**: zero warnings from `cargo clippy`. Use `#[allow(...)]` only with a comment explaining why.
- **Tests**: new automaton logic should include unit tests in the same file or a `tests/` submodule.
- **No `unsafe`**: avoid `unsafe` blocks. The codebase does not use any.

---

## Adding an Automaton Mode

1. Create `lifegrid-rs/src/automata/<name>.rs` implementing the `Automaton` trait:

   ```rust
   use crate::core::{BoundaryMode, Grid};
   use super::Automaton;

   pub struct MyAutomaton {
       grid: Grid,
       boundary: BoundaryMode,
   }

   impl MyAutomaton {
       pub fn new(width: usize, height: usize) -> Self {
           Self {
               grid: Grid::new(width, height),
               boundary: BoundaryMode::default(),
           }
       }
   }

   impl Automaton for MyAutomaton {
       fn name(&self) -> &str { "My Automaton" }
       fn step(&mut self) { /* implement rules */ }
       fn reset(&mut self) { self.grid.clear(); }
       fn get_grid(&self) -> &Grid { &self.grid }
       fn get_grid_mut(&mut self) -> &mut Grid { &mut self.grid }
       fn set_boundary(&mut self, b: BoundaryMode) { self.boundary = b; }
       fn boundary(&self) -> BoundaryMode { self.boundary }
       fn handle_click(&mut self, x: usize, y: usize) {
           let v = self.grid.get(y, x);
           self.grid.set(y, x, if v == 0 { 1 } else { 0 });
       }
       fn available_patterns(&self) -> &[&str] { &["Random Soup"] }
       fn load_pattern(&mut self, _pattern: &str) {
           // load or randomise
       }
   }
   ```

2. `pub mod <name>;` and `pub use <name>::MyAutomaton;` in `automata/mod.rs`.
3. Add `"My Automaton"` to the `ALL_MODES` constant in `automata/mod.rs`.
4. Add a match arm for it in the `make_automaton` factory in `automata/mod.rs`.

---

## Project Layout

| Path | Purpose |
|------|---------|
| `lifegrid-rs/src/app.rs` | egui application, UI panels, event loop |
| `lifegrid-rs/src/automata/` | All automaton implementations + trait |
| `lifegrid-rs/src/core/` | Grid, boundary, undo manager, app config |
| `lifegrid-rs/src/patterns.rs` | Hardcoded Conway pattern point data |
| `lifegrid-rs/src/export.rs` | PNG export |

---

## Reporting Issues

Open a GitHub issue with:

- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs. actual behaviour
- Rust version (`rustc --version`) and OS

---

## License

By contributing you agree that your contributions will be licensed under the MIT License.


---

## Development Setup

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid
make install-dev
```

This installs all dependencies (runtime, dev, docs, export) in editable mode.

### Prerequisites

- Python 3.11+
- Tcl/Tk
- Git

---

## Workflow

1. **Fork and clone** the repository.
2. **Create a branch** from `master`:
   ```bash
   git checkout -b feature/my-feature
   ```
3. **Make your changes** — keep commits focused and well-described.
4. **Run the checks** before submitting:
   ```bash
   make lint       # flake8 + pylint
   make typecheck  # mypy
   make test       # pytest (71 tests)
   ```
5. **Open a pull request** against `master`.

---

## Code Standards

- **Style**: PEP 8. Use `make format` (black + isort) to auto-format.
- **Type hints**: All public functions and methods should have type annotations. Run `make typecheck` to verify.
- **Linting**: Zero warnings from `flake8` and zero errors from `pylint --errors-only`.
- **Tests**: New features should include tests in `tests/`. Run `make test`.
- **Docstrings**: Use Google-style docstrings for public APIs.

---

## Adding An Automaton Mode

### As a plugin (recommended)

Create a `.py` file in `plugins/` that subclasses `AutomatonPlugin`:

```python
from src.plugin_system import AutomatonPlugin
from src.automata.base import CellularAutomaton

class MyPlugin(AutomatonPlugin):
    @property
    def name(self) -> str:
        return "My Automaton"

    @property
    def description(self) -> str:
        return "Description of the rules"

    @property
    def version(self) -> str:
        return "1.0"

    def create_automaton(self, width: int, height: int) -> CellularAutomaton:
        # Return your automaton instance
        ...
```

Plugins are auto-discovered at startup — no code changes to the core required.

### As a built-in mode

1. Create a new file in `src/automata/` subclassing `CellularAutomaton`.
2. Export it from `src/automata/__init__.py`.
3. Register it in `src/gui/config.py` (`MODE_FACTORIES` and `MODE_PATTERNS`).
4. Add patterns to `src/patterns.py`.
5. Add a CLI alias in `src/cli.py`.
6. Write tests.

---

## Project Layout

| Directory | Purpose |
|-----------|---------|
| `src/automata/` | Automaton implementations |
| `src/core/` | Simulator engine, config, undo, boundary |
| `src/gui/` | GUI application and widgets |
| `src/api/` | FastAPI REST + WebSocket server |
| `src/advanced/` | Statistics, analysis, RLE, heatmaps |
| `src/performance/` | GPU acceleration, benchmarking |
| `plugins/` | User-installable plugins |
| `tests/` | Test suite |
| `docs/` | Documentation |
| `examples/` | Example scripts |

---

## Reporting Issues

Open a GitHub issue with:

- A clear title and description
- Steps to reproduce (if it's a bug)
- Expected vs. actual behavior
- Python version and OS

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
