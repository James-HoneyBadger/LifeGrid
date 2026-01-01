#!/usr/bin/env python3
"""
Custom Plugin Example
======================

This example demonstrates how to create a custom cellular automaton
using the plugin system.

Usage:
    python custom_plugin.py
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.plugin_system import AutomatonPlugin, PluginManager


class InvertAutomaton(AutomatonPlugin):
    """A simple automaton that inverts all cells each generation."""
    
    def __init__(self):
        super().__init__(
            name="Invert Automaton",
            description="Inverts all cells each generation"
        )
    
    def step(self, grid: np.ndarray) -> np.ndarray:
        """Invert all cells."""
        return 1 - grid
    
    def get_color(self, state: int) -> tuple:
        """Return color for cell state."""
        return (255, 255, 255) if state == 1 else (0, 0, 0)


class MajorityRuleAutomaton(AutomatonPlugin):
    """Each cell becomes the most common state in its neighborhood."""
    
    def __init__(self):
        super().__init__(
            name="Majority Rule",
            description="Cells adopt the majority state in their neighborhood"
        )
    
    def step(self, grid: np.ndarray) -> np.ndarray:
        """Apply majority rule."""
        from scipy.signal import convolve2d
        
        # Count neighbors (including self)
        kernel = np.ones((3, 3))
        neighbor_sum = convolve2d(grid, kernel, mode='same', boundary='wrap')
        
        # Majority rule: >4.5 means majority are alive
        return (neighbor_sum > 4.5).astype(int)
    
    def get_color(self, state: int) -> tuple:
        """Return color for cell state."""
        return (100, 200, 255) if state == 1 else (20, 20, 40)


class RandomWalkAutomaton(AutomatonPlugin):
    """Each alive cell randomly moves to a neighbor."""
    
    def __init__(self):
        super().__init__(
            name="Random Walk",
            description="Living cells randomly walk around"
        )
    
    def step(self, grid: np.ndarray) -> np.ndarray:
        """Move cells randomly."""
        new_grid = np.zeros_like(grid)
        height, width = grid.shape
        
        # For each alive cell
        alive_cells = np.argwhere(grid == 1)
        for y, x in alive_cells:
            # Random direction
            dy = np.random.randint(-1, 2)
            dx = np.random.randint(-1, 2)
            
            # Move cell (with wrapping)
            new_y = (y + dy) % height
            new_x = (x + dx) % width
            new_grid[new_y, new_x] = 1
        
        return new_grid
    
    def get_color(self, state: int) -> tuple:
        """Return color for cell state."""
        return (255, 100, 100) if state == 1 else (0, 0, 0)


def main():
    """Demonstrate custom plugins."""
    print("=" * 60)
    print("LifeGrid - Custom Plugin Example")
    print("=" * 60)
    print()
    
    # Create plugin manager
    manager = PluginManager()
    
    # Register custom plugins
    print("Registering custom plugins...")
    manager.register_plugin(InvertAutomaton())
    manager.register_plugin(MajorityRuleAutomaton())
    manager.register_plugin(RandomWalkAutomaton())
    
    # List all plugins
    print("\nRegistered plugins:")
    print("-" * 60)
    for i, (name, desc) in enumerate(manager.list_plugins().items(), 1):
        print(f"{i}. {name}")
        print(f"   {desc}")
        print()
    
    # Test Invert Automaton
    print("Testing Invert Automaton:")
    print("-" * 60)
    invert = manager.create_automaton("Invert Automaton")
    grid = np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]])
    print("Initial grid:")
    print(grid)
    print("\nAfter 1 step (inverted):")
    grid = invert.step(grid)
    print(grid)
    print("\nAfter 2 steps (inverted again, back to original):")
    grid = invert.step(grid)
    print(grid)
    print()
    
    # Test Majority Rule
    print("Testing Majority Rule Automaton:")
    print("-" * 60)
    majority = manager.create_automaton("Majority Rule")
    grid = np.array([[1, 1, 0, 0, 0],
                     [1, 1, 0, 0, 0],
                     [0, 0, 1, 1, 1],
                     [0, 0, 1, 1, 1],
                     [0, 0, 1, 1, 1]])
    print("Initial grid:")
    print(grid)
    print("\nAfter 1 step:")
    grid = majority.step(grid)
    print(grid)
    print("\nAfter 2 steps:")
    grid = majority.step(grid)
    print(grid)
    print()
    
    # Test Random Walk
    print("Testing Random Walk Automaton:")
    print("-" * 60)
    walk = manager.create_automaton("Random Walk")
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 5] = 1  # Single cell in center
    print(f"Initial: 1 cell at position (5, 5)")
    print(f"Population: {np.sum(grid)}")
    
    for i in range(5):
        grid = walk.step(grid)
        positions = np.argwhere(grid == 1)
        print(f"Step {i+1}: cell at position {tuple(positions[0])}")
    
    print("\nPlugin examples complete!")


if __name__ == "__main__":
    main()
