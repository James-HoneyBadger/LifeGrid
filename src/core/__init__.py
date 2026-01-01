"""Core automation logic separated from GUI.

This package provides a clean, testable API for cellular automaton simulation
without any GUI dependencies. It enables CLI usage and easier integration with
other tools.
"""

from .simulator import Simulator
from .config import SimulatorConfig
from .undo_manager import UndoManager

__all__ = [
    "Simulator",
    "SimulatorConfig",
    "UndoManager",
]
