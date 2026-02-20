"""pytest configuration and shared fixtures for the LifeGrid test suite."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the src/ directory is on sys.path so that all tests can import
# from the package modules without installing the project first.
_src = str(Path(__file__).resolve().parent.parent / "src")
if _src not in sys.path:
    sys.path.insert(0, _src)
