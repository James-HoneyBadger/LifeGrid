"""Base class for cellular automata"""

from abc import ABC, abstractmethod


class CellularAutomaton(ABC):
    """Base class for cellular automaton implementations"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    @abstractmethod
    def reset(self):
        """Reset the automaton to initial state"""
        pass

    @abstractmethod
    def step(self):
        """Perform one step of the simulation"""
        pass

    @abstractmethod
    def get_grid(self):
        """Return the current grid state for rendering"""
        pass

    @abstractmethod
    def handle_click(self, x, y):
        """Handle mouse click at grid position (x, y)"""
        pass
