#!/bin/bash
# Bootstrap environment and launch the cellular automaton simulator.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
REQUIREMENTS_FILE="$ROOT_DIR/requirements.txt"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Error: Python 3 is not installed." >&2
    exit 1
fi

"$PYTHON_BIN" - <<'PY'
import sys

required = (3, 13)
current = sys.version_info[:2]
if current < required:
    sys.stderr.write(
        f"Error: Python {required[0]}.{required[1]}+ is required; found {current[0]}.{current[1]}.\n"
    )
    raise SystemExit(1)
PY

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null
"$VENV_DIR/bin/python" -m pip install -r "$REQUIREMENTS_FILE"

exec "$VENV_DIR/bin/python" "$ROOT_DIR/src/main.py"
