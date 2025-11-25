"""Tests for HighLife automaton."""

# pylint: disable=import-error

import numpy as np

from automata.highlife import HighLife


def test_highlife_initialization():
    """Test that HighLife initializes with empty grid"""
    highlife = HighLife(10, 10)
    assert highlife.width == 10
    assert highlife.height == 10
    assert highlife.grid.shape == (10, 10)
    assert np.all(highlife.grid == 0)


def test_replicator_pattern():
    """Test that the replicator pattern grows as expected"""
    highlife = HighLife(20, 20)
    highlife.load_pattern("Replicator")
    
    # Count initial live cells
    initial_count = np.sum(highlife.grid)
    assert initial_count == 7  # Replicator has 7 cells
    
    # After steps, it should replicate
    highlife.step()
    after_step1 = np.sum(highlife.grid)
    assert after_step1 > initial_count  # Should have grown


def test_random_soup():
    """Test that random soup creates some live cells"""
    highlife = HighLife(10, 10)
    highlife.load_pattern("Random Soup")
    
    live_cells = np.sum(highlife.grid)
    assert live_cells > 0  # Should have some live cells
    assert live_cells < 100  # But not all cells


def test_highlife_rules():
    """Test HighLife B36/S23 rules"""
    highlife = HighLife(5, 5)
    
    # Set up a cell with 6 neighbors (should birth)
    highlife.grid[1, 1] = 0  # Center cell dead
    highlife.grid[0, 0] = 1
    highlife.grid[0, 1] = 1
    highlife.grid[0, 2] = 1
    highlife.grid[1, 0] = 1
    highlife.grid[1, 2] = 1
    highlife.grid[2, 1] = 1
    # Leave grid[2,0] and grid[2,2] as 0, so 6 neighbors
    
    highlife.step()
    assert highlife.grid[1, 1] == 1  # Should be born with 6 neighbors


def test_handle_click_toggles():
    """Test that clicking toggles cell state"""
    highlife = HighLife(5, 5)

    # Initially empty
    assert highlife.grid[2, 2] == 0

    # Click to activate
    highlife.handle_click(2, 2)
    assert highlife.grid[2, 2] == 1

    # Click again to deactivate
    highlife.handle_click(2, 2)
    assert highlife.grid[2, 2] == 0


def test_reset_clears_grid():
    """Test that reset clears the grid"""
    highlife = HighLife(5, 5)

    # Add some live cells
    highlife.grid[1, 1] = 1
    highlife.grid[2, 2] = 1
    highlife.grid[3, 3] = 1

    # Reset should clear everything
    highlife.reset()
    assert np.all(highlife.grid == 0)