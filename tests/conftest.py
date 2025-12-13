"""Pytest configuration.

Ensures the `src/` directory is on `sys.path` early enough that test modules
can import from `src` at collection time (e.g. `from gui.app import
AutomatonApp`).
"""

from __future__ import annotations

import os
import sys

# Insert at import time (pytest imports conftest before collecting tests).
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SRC_PATH = os.path.join(_REPO_ROOT, "src")
if _SRC_PATH not in sys.path:
    sys.path.insert(0, _SRC_PATH)
