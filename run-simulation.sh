#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/lifegrid-rs"

if [[ ! -f "$APP_DIR/Cargo.toml" ]]; then
  echo "Error: Could not find Cargo.toml in $APP_DIR" >&2
  exit 1
fi

cd "$APP_DIR"
cargo run --release
