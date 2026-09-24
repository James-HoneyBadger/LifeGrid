# Contributing to LifeGrid

Thanks for your interest in contributing! This guide covers setup, workflow, and standards for the Rust/egui rewrite of LifeGrid.

---

## Development Setup

### Prerequisites

- [Rust](https://rustup.rs/) 1.75 or later
- A C linker (`gcc` or `clang`)
  - Debian/Ubuntu: `sudo apt-get install build-essential`
  - macOS: Xcode Command Line Tools
- A display server (X11 or Wayland on Linux) to run the GUI

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

1. **Fork** the repository and clone your fork.
2. **Create a branch** from `master`:

   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make your changes** – keep commits focused and well-described.
4. **Run checks** before submitting:

   ```bash
   cargo test          # unit tests
   cargo clippy        # lints
   cargo fmt --check   # formatting
   ```

5. **Open a pull request** against `master`.

---

## Code Standards

### Formatting

- Run `cargo fmt` before committing.
- Use the default rustfmt style. No unformatted code is accepted.

### Linting

- Aim for zero warnings from `cargo clippy`.
- Use `#[allow(...)]` only with a comment explaining why the lint is suppressed.

### Tests

- New automaton logic should include unit tests in the same file or a `tests/` submodule.
- Run the full suite with `cargo test`.

### Safety

- Avoid `unsafe` blocks. The codebase does not use any.

### Documentation

- Add doc comments (`///`) for public items.
- Update `README.md`, `CHANGELOG.md`, and this file when behaviour changes.

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
       fn name(&self) -> &'static str { "My Automaton" }
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
       fn available_patterns(&self) -> &'static [&'static str] { &["Random Soup"] }
       fn load_pattern(&mut self, _pattern: &str) {
           // load or randomise
       }
   }
   ```

2. Add `pub mod <name>;` and `pub use <name>::MyAutomaton;` in `automata/mod.rs`.
3. Add `"My Automaton"` to the `ALL_MODES` constant in `automata/mod.rs`.
4. Add a match arm for it in the `make_automaton` factory in `automata/mod.rs`.
5. Update `README.md` and `CHANGELOG.md`.

---

## Project Layout

| Path | Purpose |
|------|---------|
| `lifegrid-rs/src/app.rs` | egui application, UI panels, event loop |
| `lifegrid-rs/src/automata/` | All automaton implementations + trait |
| `lifegrid-rs/src/core/` | Grid, boundary, undo manager, app config |
| `lifegrid-rs/src/patterns.rs` | Hardcoded Conway pattern point data |
| `lifegrid-rs/src/export.rs` | PNG and GIF export |

---

## Reporting Issues

Open a GitHub issue with:

- A clear title and description
- Steps to reproduce (for bugs)
- Expected vs. actual behaviour
- Rust version (`rustc --version`) and OS
- Screenshots or GIFs if they help illustrate the problem

---

## Pull Request Checklist

- [ ] Branch is up to date with `master`
- [ ] `cargo test` passes
- [ ] `cargo clippy` produces no new warnings
- [ ] `cargo fmt --check` passes
- [ ] Documentation is updated where necessary
- [ ] CHANGELOG.md is updated for user-facing changes

---

## License

By contributing you agree that your contributions will be licensed under the [MIT License](LICENSE).
