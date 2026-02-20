"""Base class for cellular automata"""

from abc import ABC, abstractmethod

import numpy as np


class CellularAutomaton(ABC):
    """Base class for cellular automaton implementations."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # Derived classes should initialize this before calling
        # super().__init__().  We intentionally do NOT call self.reset() here
        # because subclasses already initialise self.grid in their own
        # __init__ before delegating here.
        if not hasattr(self, "grid"):
            self.grid: np.ndarray = np.zeros((height, width), dtype=int)
        # Boundary mode: 'wrap' | 'fixed' | 'reflect'
        self.boundary: str = "wrap"

    @abstractmethod
    def reset(self) -> None:
        """Reset the automaton to its initial state."""

    @abstractmethod
    def step(self) -> None:
        """Advance the simulation by one generation."""

    @abstractmethod
    def get_grid(self) -> np.ndarray:
        """Return the current grid state for rendering."""

    @abstractmethod
    def handle_click(self, x: int, y: int) -> None:
        """Handle mouse click at grid position ``(x, y)``."""
