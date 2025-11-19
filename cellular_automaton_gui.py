#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from scipy import signal
from abc import ABC, abstractmethod
import json
import os

try:
    from PIL import Image

    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

# Load all automaton classes from the broken file
#!/usr/bin/env python3
"""
Cellular Automaton GUI
Supports multiple modes:
- Conway's Game of Life
- High Life (B36/S23)
- Immigration Game (multi-color)
- Rainbow Game (6 colors)
- Langton's Ant
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import numpy as np
from scipy import signal
from abc import ABC, abstractmethod
import json
import os
import time
from collections import deque

# Optional Pillow for export features
try:
    from PIL import Image, ImageDraw

    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False


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


class ConwayGameOfLife(CellularAutomaton):
    """Conway's Game of Life implementation"""

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name):
        """Load a predefined pattern onto the grid"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x = self.width // 2
        center_y = self.height // 2

        if pattern_name == "Classic Mix":
            self._add_classic_mix(center_x, center_y)
        elif pattern_name == "Glider Gun":
            self._add_glider_gun(center_x, center_y)
        elif pattern_name == "Puffers":
            self._add_puffers(center_x, center_y)
        elif pattern_name == "Oscillators":
            self._add_oscillators(center_x, center_y)
        elif pattern_name == "Spaceships":
            self._add_spaceships(center_x, center_y)
        elif pattern_name == "Random Soup":
            self._add_random_soup()
        elif pattern_name == "R-Pentomino":
            self._add_r_pentomino(center_x, center_y)
        elif pattern_name == "Acorn":
            self._add_acorn(center_x, center_y)

    def _add_classic_mix(self, center_x, center_y):
        """Add interesting default patterns to the grid"""
        # Glider (top-left area)
        glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in glider:
            x, y = center_x - 30 + dx, center_y - 25 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Blinker (top area)
        blinker = [(0, 0), (1, 0), (2, 0)]
        for dx, dy in blinker:
            x, y = center_x + dx - 1, center_y - 30 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Toad (center-left)
        toad = [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)]
        for dx, dy in toad:
            x, y = center_x - 25 + dx, center_y + dy - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Lightweight spaceship (LWSS)
        lwss = [
            (1, 0),
            (4, 0),
            (0, 1),
            (0, 2),
            (4, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ]
        for dx, dy in lwss:
            x, y = center_x + 15 + dx, center_y - 15 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Block (stable pattern)
        block = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in block:
            x, y = center_x - 30 + dx, center_y + 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Beehive (stable pattern)
        beehive = [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)]
        for dx, dy in beehive:
            x, y = center_x + 20 + dx, center_y + 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_glider_gun(self, center_x, center_y):
        """Gosper's Glider Gun - produces gliders indefinitely"""
        gun = [
            (0, 4),
            (0, 5),
            (1, 4),
            (1, 5),
            (10, 4),
            (10, 5),
            (10, 6),
            (11, 3),
            (11, 7),
            (12, 2),
            (12, 8),
            (13, 2),
            (13, 8),
            (14, 5),
            (15, 3),
            (15, 7),
            (16, 4),
            (16, 5),
            (16, 6),
            (17, 5),
            (20, 2),
            (20, 3),
            (20, 4),
            (21, 2),
            (21, 3),
            (21, 4),
            (22, 1),
            (22, 5),
            (24, 0),
            (24, 1),
            (24, 5),
            (24, 6),
            (34, 2),
            (34, 3),
            (35, 2),
            (35, 3),
        ]
        for dx, dy in gun:
            x, y = center_x - 18 + dx, center_y - 5 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_puffers(self, center_x, center_y):
        """Add puffer trains that leave debris"""
        # Puffer train
        puffer = [
            (0, 0),
            (2, 0),
            (3, 1),
            (3, 2),
            (0, 3),
            (3, 3),
            (1, 4),
            (2, 4),
            (3, 4),
            (6, 1),
            (6, 2),
            (6, 3),
            (7, 0),
            (7, 2),
            (8, 1),
            (8, 2),
            (11, 0),
            (13, 0),
            (14, 1),
            (14, 2),
            (11, 3),
            (14, 3),
            (12, 4),
            (13, 4),
            (14, 4),
        ]
        for dx, dy in puffer:
            x, y = center_x - 7 + dx, center_y - 2 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_oscillators(self, center_x, center_y):
        """Collection of various oscillators"""
        # Blinker (period 2)
        blinker = [(0, 0), (1, 0), (2, 0)]
        for dx, dy in blinker:
            x, y = center_x - 30 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Toad (period 2)
        toad = [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)]
        for dx, dy in toad:
            x, y = center_x - 20 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Beacon (period 2)
        beacon = [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)]
        for dx, dy in beacon:
            x, y = center_x - 5 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # Pulsar (period 3)
        pulsar_pattern = [
            (2, 0),
            (3, 0),
            (4, 0),
            (8, 0),
            (9, 0),
            (10, 0),
            (0, 2),
            (5, 2),
            (7, 2),
            (12, 2),
            (0, 3),
            (5, 3),
            (7, 3),
            (12, 3),
            (0, 4),
            (5, 4),
            (7, 4),
            (12, 4),
            (2, 5),
            (3, 5),
            (4, 5),
            (8, 5),
            (9, 5),
            (10, 5),
            (2, 7),
            (3, 7),
            (4, 7),
            (8, 7),
            (9, 7),
            (10, 7),
            (0, 8),
            (5, 8),
            (7, 8),
            (12, 8),
            (0, 9),
            (5, 9),
            (7, 9),
            (12, 9),
            (0, 10),
            (5, 10),
            (7, 10),
            (12, 10),
            (2, 12),
            (3, 12),
            (4, 12),
            (8, 12),
            (9, 12),
            (10, 12),
        ]
        for dx, dy in pulsar_pattern:
            x, y = center_x - 6 + dx, center_y + dy - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_spaceships(self, center_x, center_y):
        """Collection of various spaceships"""
        # Glider
        glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in glider:
            x, y = center_x - 30 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # LWSS
        lwss = [
            (1, 0),
            (4, 0),
            (0, 1),
            (0, 2),
            (4, 2),
            (0, 3),
            (1, 3),
            (2, 3),
            (3, 3),
        ]
        for dx, dy in lwss:
            x, y = center_x - 15 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # MWSS (Middleweight Spaceship)
        mwss = [
            (2, 0),
            (0, 1),
            (4, 1),
            (0, 2),
            (0, 3),
            (4, 3),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 4),
        ]
        for dx, dy in mwss:
            x, y = center_x + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # HWSS (Heavyweight Spaceship)
        hwss = [
            (2, 0),
            (3, 0),
            (0, 1),
            (5, 1),
            (0, 2),
            (0, 3),
            (5, 3),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 4),
            (5, 4),
        ]
        for dx, dy in hwss:
            x, y = center_x + 15 + dx, center_y - 20 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_random_soup(self):
        """Add random cells for interesting evolution"""
        for i in range(self.height):
            for j in range(self.width):
                if np.random.random() < 0.15:  # 15% chance
                    self.grid[i, j] = 1

    def _add_r_pentomino(self, center_x, center_y):
        """R-pentomino - evolves for 1103 generations"""
        r_pentomino = [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
        for dx, dy in r_pentomino:
            x, y = center_x + dx - 1, center_y + dy - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_acorn(self, center_x, center_y):
        """Acorn pattern - takes 5206 generations to stabilize"""
        acorn = [(1, 0), (3, 1), (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)]
        for dx, dy in acorn:
            x, y = center_x + dx - 3, center_y + dy - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def step(self):
        """Optimized step using convolution for neighbor counting"""
        # Convolution kernel for counting neighbors
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        # Count neighbors using convolution with wrap-around boundaries
        neighbors = signal.convolve2d(
            self.grid,
            kernel,
            mode="same",
            boundary="wrap",
        )

        # Apply Conway's rules vectorized
        # Birth: dead cell with 3 neighbors becomes alive
        # Survival: live cell with 2 or 3 neighbors stays alive
        self.grid = ((self.grid == 1) & ((neighbors == 2) | (neighbors == 3))) | (
            (self.grid == 0) & (neighbors == 3)
        )
        self.grid = self.grid.astype(int)

    def get_grid(self):
        return self.grid

    def handle_click(self, x, y):
        """Toggle cell state"""
        self.grid[y, x] = 1 - self.grid[y, x]


class LangtonsAnt(CellularAutomaton):
    """Langton's Ant implementation"""

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        # Start ant in the middle, facing up
        self.ant_x = self.width // 2
        self.ant_y = self.height // 2
        self.ant_dir = 0  # 0=North, 1=East, 2=South, 3=West

    def step(self):
        # Current cell color
        current_color = self.grid[self.ant_y, self.ant_x]

        # Flip the color of the current square
        self.grid[self.ant_y, self.ant_x] = 1 - current_color

        # Turn: if white (0), turn right; if black (1), turn left
        if current_color == 0:
            self.ant_dir = (self.ant_dir + 1) % 4  # Turn right
        else:
            self.ant_dir = (self.ant_dir - 1) % 4  # Turn left

        # Move forward
        if self.ant_dir == 0:  # North
            self.ant_y = (self.ant_y - 1) % self.height
        elif self.ant_dir == 1:  # East
            self.ant_x = (self.ant_x + 1) % self.width
        elif self.ant_dir == 2:  # South
            self.ant_y = (self.ant_y + 1) % self.height
        else:  # West
            self.ant_x = (self.ant_x - 1) % self.width

    def get_grid(self):
        # Create a copy with the ant position highlighted
        display_grid = self.grid.copy()
        display_grid[self.ant_y, self.ant_x] = 2  # Special value for ant
        return display_grid

    def handle_click(self, x, y):
        """Move ant to clicked position"""
        self.ant_x = x
        self.ant_y = y


class HighLife(CellularAutomaton):
    """High Life - B36/S23 (replicators possible)"""

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name):
        """Load a predefined pattern onto the grid"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x = self.width // 2
        center_y = self.height // 2

        if pattern_name == "Replicator":
            self._add_replicator(center_x, center_y)
        elif pattern_name == "Random Soup":
            self._add_random_soup()

    def _add_replicator(self, center_x, center_y):
        """Add a replicator pattern unique to HighLife"""
        replicator = [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (2, 2), (1, 3)]
        for dx, dy in replicator:
            x, y = center_x + dx - 1, center_y + dy - 1
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

    def _add_random_soup(self):
        """Add random cells for interesting evolution"""
        for i in range(self.height):
            for j in range(self.width):
                if np.random.random() < 0.15:
                    self.grid[i, j] = 1

    def step(self):
        """Optimized step using convolution for neighbor counting"""
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        neighbors = signal.convolve2d(
            self.grid,
            kernel,
            mode="same",
            boundary="wrap",
        )

        # HighLife rules: B36/S23
        # Birth on 3 or 6 neighbors, Survival on 2 or 3
        birth = (self.grid == 0) & ((neighbors == 3) | (neighbors == 6))
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        self.grid = (birth | survival).astype(int)

    def get_grid(self):
        return self.grid

    def handle_click(self, x, y):
        """Toggle cell state"""
        self.grid[y, x] = 1 - self.grid[y, x]


def parse_bs(rule_str):
    """Parse B/S rule notation like 'B3/S23' -> (birth_set, survival_set).

    Returns two Python sets of neighbor counts.
    """
    rule = rule_str.upper().replace(" ", "")
    b_part, s_part = set(), set()
    if "B" in rule:
        try:
            b_idx = rule.index("B")
            # Find end of B section
            s_idx = rule.index("S") if "S" in rule else len(rule)
            b_digits = "".join(ch for ch in rule[b_idx + 1 : s_idx] if ch.isdigit())
            b_part = {int(ch) for ch in b_digits}
        except Exception:
            b_part = set()
    if "S" in rule:
        try:
            s_idx = rule.index("S")
            # Find end of S section
            end = len(rule)
            s_digits = "".join(ch for ch in rule[s_idx + 1 : end] if ch.isdigit())
            s_part = {int(ch) for ch in s_digits}
        except Exception:
            s_part = set()
    return b_part, s_part


class LifeLikeAutomaton(CellularAutomaton):
    """Generic life-like CA with B/S rules."""

    def __init__(self, width, height, birth=None, survival=None):
        self.birth = set(birth or {3})
        self.survival = set(survival or {2, 3})
        super().__init__(width, height)

    def set_rules(self, birth, survival):
        self.birth = set(birth)
        self.survival = set(survival)

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        if pattern_name == "Random Soup":
            for i in range(self.height):
                for j in range(self.width):
                    if np.random.random() < 0.15:
                        self.grid[i, j] = 1

    def step(self):
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        neighbors = signal.convolve2d(
            self.grid,
            kernel,
            mode="same",
            boundary="wrap",
        )
        # Compute birth/survival with any-of logic
        birth_any = (
            np.logical_or.reduce([(neighbors == n) for n in self.birth])
            if self.birth
            else False
        )
        surv_any = (
            np.logical_or.reduce([(neighbors == n) for n in self.survival])
            if self.survival
            else False
        )
        birth = (self.grid == 0) & birth_any
        survival = (self.grid == 1) & surv_any
        self.grid = (birth | survival).astype(int)

    def get_grid(self):
        return self.grid

    def handle_click(self, x, y):
        self.grid[y, x] = 1 - self.grid[y, x]


class ImmigrationGame(CellularAutomaton):
    """Immigration Game - Multi-state automaton with 4 colors"""

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name):
        """Load a predefined pattern onto the grid"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x = self.width // 2
        center_y = self.height // 2

        if pattern_name == "Color Mix":
            self._add_color_mix(center_x, center_y)
        elif pattern_name == "Random Soup":
            self._add_random_soup()

    def _add_color_mix(self, center_x, center_y):
        """Add patterns with different colors"""
        # State 1 glider
        glider1 = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in glider1:
            x, y = center_x - 20 + dx, center_y - 15 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1

        # State 2 blinker
        blinker2 = [(0, 0), (1, 0), (2, 0)]
        for dx, dy in blinker2:
            x, y = center_x + dx - 1, center_y - 15 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 2

        # State 3 block
        block3 = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for dx, dy in block3:
            x, y = center_x + 10 + dx, center_y - 15 + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 3

    def _add_random_soup(self):
        """Add random colored cells"""
        for i in range(self.height):
            for j in range(self.width):
                if np.random.random() < 0.15:
                    self.grid[i, j] = np.random.randint(1, 4)

    def step(self):
        new_grid = np.zeros_like(self.grid)

        for i in range(self.height):
            for j in range(self.width):
                # Count neighbors by state
                neighbor_count = 0
                neighbor_states = []

                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % self.height, (j + dj) % self.width
                        if self.grid[ni, nj] > 0:
                            neighbor_count += 1
                            neighbor_states.append(self.grid[ni, nj])

                # Immigration rules: same as Conway's but color is successor
                current_state = self.grid[i, j]

                if current_state > 0:  # Cell is alive
                    if neighbor_count in [2, 3]:
                        new_grid[i, j] = current_state
                else:  # Cell is dead
                    if neighbor_count == 3:
                        # New cell takes the "next" state of its parents
                        if neighbor_states:
                            avg_state = int(np.mean(neighbor_states))
                            new_grid[i, j] = (avg_state % 3) + 1

        self.grid = new_grid

    def get_grid(self):
        return self.grid

    def handle_click(self, x, y):
        """Cycle through cell states"""
        self.grid[y, x] = (self.grid[y, x] + 1) % 4


class RainbowGame(CellularAutomaton):
    """Rainbow Game - Multi-color variant with 6 colors"""

    def reset(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)

    def load_pattern(self, pattern_name):
        """Load a predefined pattern onto the grid"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        center_x = self.width // 2
        center_y = self.height // 2

        if pattern_name == "Rainbow Mix":
            self._add_rainbow_mix(center_x, center_y)
        elif pattern_name == "Random Soup":
            self._add_random_soup()

    def _add_rainbow_mix(self, center_x, center_y):
        """Add patterns with different rainbow colors"""
        patterns = [
            # Red glider (state 1)
            ([(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)], -30, -20, 1),
            # Orange blinker (state 2)
            ([(0, 0), (1, 0), (2, 0)], -15, -20, 2),
            # Yellow toad (state 3)
            ([(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)], 0, -20, 3),
            # Green block (state 4)
            ([(0, 0), (1, 0), (0, 1), (1, 1)], 15, -20, 4),
            # Blue beehive (state 5)
            ([(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)], 25, -20, 5),
            # Purple beacon (state 6)
            ([(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)], -20, 0, 6),
        ]

        for pattern, offset_x, offset_y, state in patterns:
            for dx, dy in pattern:
                x, y = center_x + offset_x + dx, center_y + offset_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[y, x] = state

    def _add_random_soup(self):
        """Add random colored cells"""
        for i in range(self.height):
            for j in range(self.width):
                if np.random.random() < 0.15:
                    self.grid[i, j] = np.random.randint(1, 7)

    def step(self):
        new_grid = np.zeros_like(self.grid)

        for i in range(self.height):
            for j in range(self.width):
                # Count neighbors and track their colors
                neighbor_count = 0
                neighbor_colors = []

                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = (i + di) % self.height, (j + dj) % self.width
                        if self.grid[ni, nj] > 0:
                            neighbor_count += 1
                            neighbor_colors.append(self.grid[ni, nj])

                current_state = self.grid[i, j]

                if current_state > 0:  # Cell is alive
                    if neighbor_count in [2, 3]:
                        new_grid[i, j] = current_state
                else:  # Cell is dead
                    if neighbor_count == 3:
                        # New cell is average of neighbor colors
                        if neighbor_colors:
                            new_grid[i, j] = int(np.mean(neighbor_colors))

        self.grid = new_grid

    def get_grid(self):
        return self.grid

    def handle_click(self, x, y):
        """Cycle through rainbow colors"""
        self.grid[y, x] = (self.grid[y, x] + 1) % 7


class CellularAutomatonGUI:
    """Main GUI for Cellular Automaton"""

    def __init__(self, root):
        self.root = root
        self.root.title("Cellular Automaton Simulator")

        # Configuration
        self.grid_width = 100
        self.grid_height = 100
        self.cell_size = 8

        # State
        self.running = False
        self.current_automaton = None
        self.generation = 0

        # Variables
        self.mode_var = tk.StringVar(value="Conway's Game of Life")
        self.pattern_var = tk.StringVar(value="Classic Mix")
        self.speed_var = tk.IntVar(value=50)
        self.grid_size_var = tk.StringVar(value="100x100")
        self.custom_width = tk.IntVar(value=100)
        self.custom_height = tk.IntVar(value=100)
        self.draw_mode_var = tk.StringVar(value="toggle")
        self.symmetry_var = tk.StringVar(value="None")
        self.show_grid = True  # Grid lines on by default

        # Modes
        self.modes = {
            "Conway's Game of Life": (
                "conway",
                [
                    "Classic Mix",
                    "Glider Gun",
                    "Spaceships",
                    "Oscillators",
                    "Puffers",
                    "R-Pentomino",
                    "Acorn",
                    "Random Soup",
                ],
            ),
            "High Life": ("highlife", ["Replicator", "Random Soup"]),
            "Immigration Game": ("immigration", ["Color Mix", "Random Soup"]),
            "Rainbow Game": ("rainbow", ["Rainbow Mix", "Random Soup"]),
            "Langton's Ant": ("ant", ["Empty"]),
            "Custom Rules": ("custom", ["Random Soup"]),
        }

        # Create widgets first
        self.create_widgets()

        # Initialize automaton after widgets exist
        self.switch_mode("Conway's Game of Life")
        self.draw_grid()

    def create_widgets(self):
        # Control panel at top
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10)

        # Row 0: Mode and basic controls
        tk.Label(control_frame, text="Mode:").grid(row=0, column=0, padx=5, sticky=tk.E)
        mode_combo = ttk.Combobox(
            control_frame, textvariable=self.mode_var, state="readonly", width=20
        )
        mode_combo["values"] = list(self.modes.keys())
        mode_combo.grid(row=0, column=1, padx=5)
        mode_combo.bind(
            "<<ComboboxSelected>>", lambda e: self.switch_mode(self.mode_var.get())
        )

        self.start_button = tk.Button(
            control_frame,
            text="Start",
            command=self.toggle_simulation,
            width=10,
            bg="#4caf50",
            fg="white",
        )
        self.start_button.grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Step", command=self.step_once, width=8).grid(
            row=0, column=3, padx=5
        )
        tk.Button(
            control_frame,
            text="Clear",
            command=self.clear_grid,
            width=8,
            bg="#f44336",
            fg="white",
        ).grid(row=0, column=4, padx=5)
        tk.Button(
            control_frame, text="Reset", command=self.reset_simulation, width=8
        ).grid(row=0, column=5, padx=5)

        # Row 1: Pattern controls
        tk.Label(control_frame, text="Pattern:").grid(
            row=1, column=0, padx=5, sticky=tk.E
        )
        self.pattern_combo = ttk.Combobox(
            control_frame, textvariable=self.pattern_var, state="readonly", width=20
        )
        self.pattern_combo.grid(row=1, column=1, padx=5)
        self.pattern_combo.bind(
            "<<ComboboxSelected>>", lambda e: self.load_pattern_handler()
        )

        tk.Button(control_frame, text="Save", command=self.save_pattern, width=8).grid(
            row=1, column=2, padx=5
        )
        tk.Button(
            control_frame, text="Load File", command=self.load_saved_pattern, width=8
        ).grid(row=1, column=3, padx=5)
        if PIL_AVAILABLE:
            tk.Button(
                control_frame, text="Export PNG", command=self.export_png, width=10
            ).grid(row=1, column=4, padx=5)

        # Row 2: Custom rules (for Custom Rules mode)
        tk.Label(control_frame, text="Custom B/S:").grid(
            row=2, column=0, padx=5, sticky=tk.E
        )
        tk.Label(control_frame, text="B:").grid(row=2, column=1, sticky=tk.W)
        self.birth_entry = tk.Entry(control_frame, width=8)
        self.birth_entry.grid(row=2, column=1, padx=(20, 5), sticky=tk.W)
        self.birth_entry.insert(0, "3")
        tk.Label(control_frame, text="S:").grid(row=2, column=2, sticky=tk.W)
        self.survival_entry = tk.Entry(control_frame, width=8)
        self.survival_entry.grid(row=2, column=2, padx=(20, 5), sticky=tk.W)
        self.survival_entry.insert(0, "23")
        tk.Button(
            control_frame, text="Apply Rules", command=self.apply_custom_rules, width=10
        ).grid(row=2, column=3, padx=5)

        # Row 3: Grid size
        tk.Label(control_frame, text="Grid Size:").grid(
            row=3, column=0, padx=5, sticky=tk.E
        )
        size_combo = ttk.Combobox(
            control_frame, textvariable=self.grid_size_var, state="readonly", width=12
        )
        size_combo["values"] = ["50x50", "100x100", "150x150", "200x200", "Custom"]
        size_combo.grid(row=3, column=1, padx=5, sticky=tk.W)
        size_combo.bind("<<ComboboxSelected>>", self.on_size_preset_change)

        tk.Label(control_frame, text="W:").grid(row=3, column=2, sticky=tk.W)
        self.width_spinbox = tk.Spinbox(
            control_frame, from_=10, to=500, textvariable=self.custom_width, width=6
        )
        self.width_spinbox.grid(row=3, column=2, padx=(20, 2), sticky=tk.W)
        tk.Label(control_frame, text="H:").grid(row=3, column=3, sticky=tk.W)
        self.height_spinbox = tk.Spinbox(
            control_frame, from_=10, to=500, textvariable=self.custom_height, width=6
        )
        self.height_spinbox.grid(row=3, column=3, padx=(20, 2), sticky=tk.W)
        tk.Button(
            control_frame, text="Apply", command=self.apply_custom_grid_size, width=8
        ).grid(row=3, column=4, padx=5)

        # Row 4: Draw mode and symmetry
        tk.Label(control_frame, text="Draw:").grid(row=4, column=0, padx=5, sticky=tk.E)
        tk.Radiobutton(
            control_frame, text="Toggle", variable=self.draw_mode_var, value="toggle"
        ).grid(row=4, column=1, sticky=tk.W)
        tk.Radiobutton(
            control_frame, text="Pen", variable=self.draw_mode_var, value="pen"
        ).grid(row=4, column=2, sticky=tk.W)
        tk.Radiobutton(
            control_frame, text="Eraser", variable=self.draw_mode_var, value="eraser"
        ).grid(row=4, column=3, sticky=tk.W)

        tk.Label(control_frame, text="Symmetry:").grid(row=4, column=4, sticky=tk.E)
        symmetry_combo = ttk.Combobox(
            control_frame, textvariable=self.symmetry_var, state="readonly", width=12
        )
        symmetry_combo["values"] = ["None", "Horizontal", "Vertical", "Both", "Radial"]
        symmetry_combo.grid(row=4, column=5, padx=5)

        # Row 5: Speed and generation
        tk.Label(control_frame, text="Speed:").grid(
            row=5, column=0, padx=5, sticky=tk.E
        )
        speed_slider = tk.Scale(
            control_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=150,
        )
        speed_slider.grid(row=5, column=1, columnspan=2, sticky=tk.W, padx=5)

        tk.Button(
            control_frame, text="Toggle Grid", command=self.toggle_grid, width=10
        ).grid(row=5, column=3, padx=5)

        self.gen_label = tk.Label(
            control_frame, text="Generation: 0", font=("Arial", 10, "bold")
        )
        self.gen_label.grid(row=5, column=4, columnspan=2, padx=5)

        # Canvas frame
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame, bg="white", width=800, height=600)
        h_scroll = tk.Scrollbar(
            canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview
        )
        v_scroll = tk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        h_scroll.grid(row=1, column=0, sticky=tk.EW)
        v_scroll.grid(row=0, column=1, sticky=tk.NS)

        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        # Bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

    def switch_mode(self, mode_name):
        """Switch to a different automaton mode"""
        self.stop_simulation()
        mode_key, patterns = self.modes[mode_name]

        if mode_key == "conway":
            self.current_automaton = ConwayGameOfLife(self.grid_width, self.grid_height)
        elif mode_key == "highlife":
            self.current_automaton = HighLife(self.grid_width, self.grid_height)
        elif mode_key == "immigration":
            self.current_automaton = ImmigrationGame(self.grid_width, self.grid_height)
        elif mode_key == "rainbow":
            self.current_automaton = RainbowGame(self.grid_width, self.grid_height)
        elif mode_key == "ant":
            self.current_automaton = LangtonsAnt(self.grid_width, self.grid_height)
        elif mode_key == "custom":
            self.current_automaton = LifeLikeAutomaton(
                self.grid_width, self.grid_height, {3}, {2, 3}
            )

        # Update pattern list
        self.pattern_combo["values"] = patterns
        if patterns:
            self.pattern_var.set(patterns[0])
            # Load the default pattern for this mode
            if patterns[0] != "Empty" and hasattr(
                self.current_automaton, "load_pattern"
            ):
                self.current_automaton.load_pattern(patterns[0])

        self.generation = 0
        self.update_display()

    def load_pattern_handler(self):
        """Load selected pattern"""
        pattern_name = self.pattern_var.get()
        if hasattr(self.current_automaton, "load_pattern"):
            self.current_automaton.load_pattern(pattern_name)
            self.generation = 0
            self.update_display()

    def toggle_simulation(self):
        """Start/stop the simulation"""
        self.running = not self.running
        if self.running:
            self.start_button.config(text="Stop", bg="#ff9800")
            self.run_simulation()
        else:
            self.start_button.config(text="Start", bg="#4caf50")

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False
        self.start_button.config(text="Start", bg="#4caf50")

    def run_simulation(self):
        """Run simulation loop"""
        if self.running:
            self.step_once()
            delay = max(10, 1010 - self.speed_var.get() * 10)
            self.root.after(delay, self.run_simulation)

    def step_once(self):
        """Perform one simulation step"""
        if self.current_automaton:
            self.current_automaton.step()
            self.generation += 1
            self.gen_label.config(text=f"Generation: {self.generation}")
            self.update_display()

    def reset_simulation(self):
        """Reset to initial state"""
        self.stop_simulation()
        if self.current_automaton:
            self.current_automaton.reset()
            self.generation = 0
            self.gen_label.config(text="Generation: 0")
            self.update_display()

    def clear_grid(self):
        """Clear the grid"""
        self.stop_simulation()
        if self.current_automaton:
            self.current_automaton.reset()
            self.generation = 0
            self.gen_label.config(text="Generation: 0")
            self.update_display()

    def apply_custom_rules(self):
        """Apply custom B/S rules"""
        if isinstance(self.current_automaton, LifeLikeAutomaton):
            try:
                birth_str = self.birth_entry.get().strip()
                survival_str = self.survival_entry.get().strip()
                birth = {int(ch) for ch in birth_str if ch.isdigit()}
                survival = {int(ch) for ch in survival_str if ch.isdigit()}
                self.current_automaton.set_rules(birth, survival)
                self.reset_simulation()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid rules: {e}")

    def on_size_preset_change(self, event=None):
        """Handle grid size preset selection"""
        size = self.grid_size_var.get()
        if size == "Custom":
            return

        parts = size.split("x")
        if len(parts) == 2:
            width = int(parts[0])
            height = int(parts[1])
            self.resize_grid(width, height)

    def apply_custom_grid_size(self):
        """Apply custom grid size"""
        width = self.custom_width.get()
        height = self.custom_height.get()
        self.resize_grid(width, height)

    def resize_grid(self, width, height):
        """Resize the grid"""
        self.stop_simulation()
        self.grid_width = width
        self.grid_height = height

        # Recreate automaton with new size
        mode_name = self.mode_var.get()
        self.switch_mode(mode_name)

    def save_pattern(self):
        """Save current pattern to file"""
        if not self.current_automaton:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if filename:
            try:
                data = {
                    "mode": self.mode_var.get(),
                    "width": self.grid_width,
                    "height": self.grid_height,
                    "grid": self.current_automaton.get_grid().tolist(),
                }
                with open(filename, "w") as f:
                    json.dump(data, f)
                messagebox.showinfo("Success", "Pattern saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

    def load_saved_pattern(self):
        """Load pattern from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    data = json.load(f)

                # Set mode and resize if needed
                mode = data.get("mode", "Conway's Game of Life")
                width = data.get("width", 100)
                height = data.get("height", 100)

                if width != self.grid_width or height != self.grid_height:
                    self.resize_grid(width, height)

                self.mode_var.set(mode)
                self.switch_mode(mode)

                # Load grid data
                grid_data = np.array(data["grid"])
                self.current_automaton.grid = grid_data
                self.generation = 0
                self.update_display()

                messagebox.showinfo("Success", "Pattern loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")

    def export_png(self):
        """Export current state as PNG"""
        if not PIL_AVAILABLE:
            messagebox.showerror("Error", "PIL/Pillow not installed")
            return

        if not self.current_automaton:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )
        if filename:
            try:
                grid = self.current_automaton.get_grid()

                # Create image
                img = Image.new("RGB", (self.grid_width, self.grid_height), "white")
                pixels = img.load()

                # Color mapping
                colors = {
                    0: (255, 255, 255),  # white
                    1: (0, 0, 0),  # black
                    2: (255, 0, 0),  # red
                    3: (0, 255, 0),  # green
                    4: (0, 0, 255),  # blue
                    5: (255, 255, 0),  # yellow
                    6: (255, 0, 255),  # magenta
                }

                for y in range(self.grid_height):
                    for x in range(self.grid_width):
                        val = int(grid[y, x])
                        pixels[x, y] = colors.get(val, (0, 0, 0))

                # Scale up
                scale = max(1, 800 // max(self.grid_width, self.grid_height))
                img = img.resize(
                    (self.grid_width * scale, self.grid_height * scale), Image.NEAREST
                )
                img.save(filename)

                messagebox.showinfo("Success", f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def draw_grid(self):
        """Initial grid drawing"""
        self.update_display()

    def update_display(self):
        """Update canvas display"""
        if not self.current_automaton:
            return

        self.canvas.delete("all")
        grid = self.current_automaton.get_grid()

        # Set scroll region
        width = self.grid_width * self.cell_size
        height = self.grid_height * self.cell_size
        self.canvas.configure(scrollregion=(0, 0, width, height))

        # Color mappings for different states
        color_map = {
            0: "white",
            1: "black",
            2: "red",
            3: "orange",
            4: "yellow",
            5: "green",
            6: "blue",
            7: "purple",
        }

        # Draw cells
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                val = int(grid[y, x])
                color = color_map.get(val, "white")

                outline = "gray" if self.show_grid else ""
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=outline, width=1
                )

    def toggle_grid(self):
        """Toggle grid line display"""
        self.show_grid = not self.show_grid
        self.update_display()

    def on_canvas_click(self, event):
        """Handle canvas click"""
        x = int(self.canvas.canvasx(event.x) // self.cell_size)
        y = int(self.canvas.canvasy(event.y) // self.cell_size)

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.apply_draw_action(x, y)
            self.update_display()

    def on_canvas_drag(self, event):
        """Handle canvas drag"""
        x = int(self.canvas.canvasx(event.x) // self.cell_size)
        y = int(self.canvas.canvasy(event.y) // self.cell_size)

        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.apply_draw_action(x, y)
            self.update_display()

    def apply_draw_action(self, x, y):
        """Apply drawing action at position"""
        if not self.current_automaton:
            return

        mode = self.draw_mode_var.get()
        symmetry = self.symmetry_var.get()

        # Get positions to modify based on symmetry
        positions = [(x, y)]

        if symmetry == "Horizontal":
            positions.append((self.grid_width - 1 - x, y))
        elif symmetry == "Vertical":
            positions.append((x, self.grid_height - 1 - y))
        elif symmetry == "Both":
            positions.append((self.grid_width - 1 - x, y))
            positions.append((x, self.grid_height - 1 - y))
            positions.append((self.grid_width - 1 - x, self.grid_height - 1 - y))
        elif symmetry == "Radial":
            cx, cy = self.grid_width // 2, self.grid_height // 2
            dx, dy = x - cx, y - cy
            for angle in [0, 90, 180, 270]:
                if angle == 0:
                    positions.append((cx + dx, cy + dy))
                elif angle == 90:
                    positions.append((cx - dy, cy + dx))
                elif angle == 180:
                    positions.append((cx - dx, cy - dy))
                elif angle == 270:
                    positions.append((cx + dy, cy - dx))

        # Apply action to all positions
        for px, py in positions:
            if 0 <= px < self.grid_width and 0 <= py < self.grid_height:
                if mode == "toggle":
                    self.current_automaton.handle_click(px, py)
                elif mode == "pen":
                    self.current_automaton.grid[py, px] = 1
                elif mode == "eraser":
                    self.current_automaton.grid[py, px] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = CellularAutomatonGUI(root)
    root.mainloop()
