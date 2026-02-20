# pylint: disable=duplicate-code

"""Conway's Game of Life implementation."""

from __future__ import annotations

import warnings
import numpy as np

from core.boundary import BoundaryMode, convolve_with_boundary
from patterns import PATTERN_DATA

from .base import CellularAutomaton


class ConwayGameOfLife(CellularAutomaton):
    """Conway's Game of Life implementation."""

    def __init__(self, width: int, height: int) -> None:
        self.grid = np.zeros((height, width), dtype=int)
        self._kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)
        super().__init__(width, height)

    def reset(self) -> None:
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name: str) -> None:
        """Load a predefined pattern onto the grid."""
        # Handle procedural patterns first (before clearing)
        if pattern_name == "Random Soup":
            self.grid = np.zeros((self.height, self.width), dtype=int)
            self._add_random_soup()
            return

        # Load from JSON-backed pattern data
        pattern_data_dict = PATTERN_DATA.get("Conway's Game of Life", {})
        if pattern_name in pattern_data_dict:
            points, _ = pattern_data_dict[pattern_name]
            self.grid = np.zeros((self.height, self.width), dtype=int)
            if points:
                center_x = self.width // 2
                center_y = self.height // 2
                for dx, dy in points:
                    x, y = center_x + dx, center_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.grid[y, x] = 1
            return
        # Unknown pattern name: leave grid unchanged and warn
        warnings.warn(
            f"Unknown pattern '{pattern_name}' for Conway's Game of Life."
            " Grid unchanged."
        )

    def _add_random_soup(self) -> None:
        random_mask = np.random.random(self.grid.shape) < 0.15
        self.grid[random_mask] = 1

    def step(self) -> None:
        """Advance the automaton by one generation."""
        bnd = BoundaryMode.from_string(self.boundary)
        neighbors = convolve_with_boundary(self.grid, self._kernel, bnd)
        self.grid = (
            ((self.grid == 1) & ((neighbors == 2) | (neighbors == 3)))
            | ((self.grid == 0) & (neighbors == 3))
        ).astype(int)

    def get_grid(self) -> np.ndarray:
        return self.grid

    def handle_click(self, x: int, y: int) -> None:
        self.grid[y, x] = 1 - self.grid[y, x]

    def get_available_patterns(self) -> list[str]:
        """Get list of available patterns for Conway's Game of Life."""
        try:
            pattern_data_dict = PATTERN_DATA.get("Conway's Game of Life", {})
            patterns = list(pattern_data_dict.keys())
            patterns.append("Random Soup")
            return sorted(patterns)
        except (AttributeError, TypeError):
            return ["Random Soup"]
