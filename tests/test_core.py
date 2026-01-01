"""Tests for the core simulator module."""

from __future__ import annotations

import numpy as np
import pytest

from core.simulator import Simulator
from core.config import SimulatorConfig
from core.undo_manager import UndoManager


class TestSimulatorConfig:
    """Test SimulatorConfig."""

    def test_default_config(self) -> None:
        """Test default configuration."""
        config = SimulatorConfig()
        assert config.width == 100
        assert config.height == 100
        assert config.speed == 50

    def test_config_from_dict(self) -> None:
        """Test creating config from dictionary."""
        data = {
            "width": 200,
            "height": 150,
            "speed": 100,
        }
        config = SimulatorConfig.from_dict(data)
        assert config.width == 200
        assert config.height == 150
        assert config.speed == 100

    def test_config_to_dict(self) -> None:
        """Test converting config to dictionary."""
        config = SimulatorConfig(width=75, height=75, speed=25)
        data = config.to_dict()
        
        assert data["width"] == 75
        assert data["height"] == 75
        assert data["speed"] == 25


class TestUndoManager:
    """Test undo/redo functionality."""

    def test_undo_manager_initialization(self) -> None:
        """Test undo manager initializes correctly."""
        manager = UndoManager(max_history=50)
        assert not manager.can_undo()
        assert not manager.can_redo()

    def test_push_and_undo(self) -> None:
        """Test pushing state and undoing."""
        manager = UndoManager()
        grid = np.ones((10, 10))
        
        manager.push_state("Create grid", grid)
        assert manager.can_undo()
        assert not manager.can_redo()
        
        result = manager.undo()
        assert result is not None
        name, state = result
        assert name == "Create grid"
        assert np.array_equal(state, grid)

    def test_undo_and_redo(self) -> None:
        """Test undo followed by redo."""
        manager = UndoManager()
        grid1 = np.zeros((10, 10))
        grid2 = np.ones((10, 10))
        
        manager.push_state("Step 1", grid1)
        manager.push_state("Step 2", grid2)
        
        manager.undo()
        assert manager.can_redo()
        
        result = manager.redo()
        assert result is not None

    def test_undo_clears_redo(self) -> None:
        """Test that pushing new state clears redo."""
        manager = UndoManager()
        grid1 = np.zeros((10, 10))
        grid2 = np.ones((10, 10))
        
        manager.push_state("Step 1", grid1)
        manager.undo()
        assert manager.can_redo()
        
        manager.push_state("Step 2", grid2)
        assert not manager.can_redo()

    def test_history_summary(self) -> None:
        """Test getting history summary."""
        manager = UndoManager()
        grid = np.zeros((10, 10))
        
        manager.push_state("Action 1", grid)
        manager.push_state("Action 2", grid)
        
        summary = manager.get_history_summary()
        assert summary["undo_count"] == 2
        assert summary["redo_count"] == 0


class TestSimulator:
    """Test the core Simulator class."""

    def test_simulator_initialization(self) -> None:
        """Test simulator initializes correctly."""
        sim = Simulator()
        assert sim.generation == 0
        assert len(sim.metrics_log) == 0

    def test_simulator_with_custom_config(self) -> None:
        """Test simulator with custom config."""
        config = SimulatorConfig(width=50, height=50, speed=100)
        sim = Simulator(config)
        assert sim.config.width == 50
        assert sim.config.height == 50

    def test_initialize_conway(self) -> None:
        """Test initializing Conway's Life."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life")
        
        assert sim.automaton is not None
        grid = sim.get_grid()
        assert grid.shape == (100, 100)

    def test_initialize_with_pattern(self) -> None:
        """Test initializing with pattern."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Glider Gun")
        
        grid = sim.get_grid()
        # Glider gun should have some live cells
        assert np.count_nonzero(grid) > 0

    def test_step_simulation(self) -> None:
        """Test stepping through simulation."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        
        initial_pop = np.count_nonzero(sim.get_grid())
        metrics = sim.step(1)
        
        assert len(metrics) == 1
        assert sim.generation == 1
        assert len(sim.metrics_log) == 1

    def test_multiple_steps(self) -> None:
        """Test multiple steps."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        
        sim.step(5)
        assert sim.generation == 5
        assert len(sim.metrics_log) == 5

    def test_set_cell(self) -> None:
        """Test setting individual cells."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life")
        
        sim.set_cell(50, 50, 1)
        grid = sim.get_grid()
        assert grid[50, 50] == 1

    def test_reset(self) -> None:
        """Test resetting simulation."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        
        initial_pop = np.count_nonzero(sim.get_grid())
        assert initial_pop > 0
        
        sim.reset()
        assert sim.generation == 0
        assert len(sim.metrics_log) == 0

    def test_undo_functionality(self) -> None:
        """Test undo within simulator."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        
        initial_grid = np.copy(sim.get_grid())
        sim.step(1)
        stepped_grid = np.copy(sim.get_grid())
        
        assert not np.array_equal(initial_grid, stepped_grid)
        
        sim.undo()
        assert np.array_equal(sim.get_grid(), initial_grid)

    def test_metrics_summary(self) -> None:
        """Test getting metrics summary."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        sim.step(3)
        
        summary = sim.get_metrics_summary()
        assert summary["generations"] == 3
        assert summary["current_population"] >= 0

    def test_callback_on_step(self) -> None:
        """Test callback is called on step."""
        sim = Simulator()
        sim.initialize("Conway's Game of Life", "Random Soup")
        
        called_with = []
        
        def callback(metrics: dict) -> None:
            called_with.append(metrics)
        
        sim.set_on_step_callback(callback)
        sim.step(2)
        
        assert len(called_with) == 2

    def test_invalid_automaton_mode(self) -> None:
        """Test error on invalid automaton mode."""
        sim = Simulator()
        with pytest.raises(ValueError):
            sim.initialize("NonexistentMode")

    def test_high_life_mode(self) -> None:
        """Test HighLife automaton."""
        sim = Simulator()
        sim.initialize("HighLife", "Random Soup")
        
        grid = sim.get_grid()
        assert grid.shape == (100, 100)

    def test_different_modes(self) -> None:
        """Test initializing different automaton modes."""
        modes = [
            "Conway's Game of Life",
            "HighLife",
            "Langton's Ant",
            "Wireworld",
            "Brian's Brain",
            "Generations",
            "Immigration",
            "Rainbow",
        ]
        
        for mode in modes:
            sim = Simulator()
            sim.initialize(mode)
            assert sim.automaton is not None
            assert sim.get_grid().shape == (100, 100)
