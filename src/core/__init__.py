"""Core automation logic separated from GUI.

This package provides a clean, testable API for cellular automaton simulation
without any GUI dependencies. It enables CLI usage and easier integration with
other tools.
"""

from .config import SimulatorConfig
from .undo_manager import UndoManager

# NOTE: Simulator is intentionally NOT imported here to avoid a circular
# dependency: core.simulator → automata → core.boundary → core.__init__
# Import Simulator directly:  from core.simulator import Simulator

__all__ = [
    "SimulatorConfig",
    "UndoManager",
]
