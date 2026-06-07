#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUST_DIR="$ROOT_DIR/lifegrid-rs"
TS_DIR="$ROOT_DIR/lifegrid-ts"

mode="native"
if [[ $# -gt 0 ]]; then
  mode="$1"
fi

case "$mode" in
  native|rust|rs)
    cd "$RUST_DIR"
    cargo run
    ;;
  web|ts)
    cd "$TS_DIR"
    if [[ ! -d node_modules ]]; then
      npm install
    fi
    npm run dev
    ;;
  *)
    echo "Usage: ./run.sh [native|web]"
    exit 1
    ;;
esac
