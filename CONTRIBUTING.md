# Contributing to LifeGrid

Thanks for contributing. LifeGrid is now a dual-platform project with:

- `lifegrid-rs` (Rust native desktop)
- `lifegrid-ts` (TypeScript web)

Please keep changes scoped, tested, and documented.

---

## Prerequisites

### Rust stack (`lifegrid-rs`)

- Rust 1.75+ via [rustup](https://rustup.rs)
- A C toolchain/linker (`clang` or `gcc`)
- Desktop display server (macOS, X11, Wayland)

### TypeScript stack (`lifegrid-ts`)

- Node.js 18+
- npm 9+

---

## Local Setup

Clone and prepare both apps:

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid

# Rust app
cd lifegrid-rs
cargo build

# TypeScript app
cd ../lifegrid-ts
npm install
npm run build
```

Run apps:

```bash
# Rust desktop
cd lifegrid-rs
cargo run

# TypeScript web
cd ../lifegrid-ts
npm run dev
```

---

## Pull Request Workflow

1. Fork and clone.
2. Create a feature branch from `master`.
3. Make focused commits.
4. Run relevant checks (see below).
5. Update docs when behavior changes.
6. Open PR against `master`.

---

## Required Checks

### Rust changes

```bash
cd lifegrid-rs
cargo build
cargo test
cargo clippy
cargo fmt --check
```

### TypeScript changes

```bash
cd lifegrid-ts
npm run test
npm run build
```

---

## Coding Standards

### General

- Keep APIs and UX consistent across Rust and TS where practical.
- Prefer small, reviewable PRs.
- Avoid unrelated refactors in feature PRs.

### Rust

- Format with `cargo fmt`.
- Keep `cargo clippy` clean.
- Avoid `unsafe` unless absolutely required and justified.

### TypeScript

- Keep strict type safety (`tsconfig` strict mode).
- Avoid `any`; prefer explicit interfaces and narrow unions.
- Keep model behavior isolated in `src/automata/models.ts` unless a new file split is justified.

---

## Adding a New Automaton Model

For feature parity, update both stacks when possible.

### Rust path

1. Add `lifegrid-rs/src/automata/<name>.rs` implementing `Automaton`.
2. Register module and export in `lifegrid-rs/src/automata/mod.rs`.
3. Add mode label to `ALL_MODES`.
4. Add factory match arm in `make_automaton`.
5. Ensure pattern list and click behavior are defined.

### TypeScript path

1. Add model class to `lifegrid-ts/src/automata/models.ts` implementing `Automaton`.
2. Register it in `createModel` and `ALL_MODELS`.
3. Add `colorForState` and `handleClick` behavior for multi-state models.
4. Verify rendering and interactions in `lifegrid-ts/src/main.ts`.

### Documentation

Update all of:

- `README.md` model lists and controls (if changed)
- `CHANGELOG.md` (under `Unreleased`)

---

## Project Layout

| Path | Purpose |
|---|---|
| `lifegrid-rs/src/app.rs` | Native UI panels and simulation loop |
| `lifegrid-rs/src/automata/` | Rust automata implementations |
| `lifegrid-rs/src/core/` | Grid, boundary, undo, config |
| `lifegrid-ts/src/main.ts` | Web UI, interactions, rendering |
| `lifegrid-ts/src/automata/models.ts` | TS model registry and logic |
| `lifegrid-ts/src/core/` | Shared TS interfaces and grid |

---

## Reporting Issues

Include:

- Clear description and reproduction steps
- Expected and actual behavior
- Platform impacted (`lifegrid-rs`, `lifegrid-ts`, or both)
- Environment details (`rustc --version` and/or `node -v`, OS, browser)

---

## License

By contributing, you agree your contributions are licensed under the MIT License.
