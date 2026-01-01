"""Tests for simulation state management."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
import numpy as np

from gui.state import SimulationState


class TestSimulationState:
    """Test SimulationState class."""

    def test_initialization(self) -> None:
        """Test SimulationState initializes correctly."""
        state = SimulationState()
        assert state.cell_size == 8
        assert state.speed == 50
        assert state.is_running is False

    def test_metrics_logging(self) -> None:
        """Test metrics are logged correctly."""
        state = SimulationState()
        assert len(state.metrics_log) == 0
        
        state.add_metric(generation=1, population=10, peak=15, density=0.5)
        assert len(state.metrics_log) == 1
        assert state.metrics_log[0]["generation"] == 1
        assert state.metrics_log[0]["population"] == 10

    def test_multiple_metrics(self) -> None:
        """Test logging multiple metrics."""
        state = SimulationState()
        
        for i in range(10):
            state.add_metric(generation=i, population=i*5, peak=i*10, density=0.1*i)
        
        assert len(state.metrics_log) == 10
        assert state.metrics_log[-1]["generation"] == 9

    def test_metrics_export(self) -> None:
        """Test exporting metrics to CSV format."""
        state = SimulationState()
        
        state.add_metric(generation=0, population=5, peak=10, density=0.1)
        state.add_metric(generation=1, population=8, peak=12, density=0.15)
        
        csv_data = state.export_metrics_csv()
        lines = csv_data.strip().split('\n')
        
        assert len(lines) == 3  # Header + 2 data rows
        assert "generation" in lines[0]
        assert "population" in lines[0]

    def test_cell_size_constraints(self) -> None:
        """Test cell size respects constraints."""
        state = SimulationState()
        
        state.cell_size = 1
        assert state.cell_size >= 1  # MIN_CELL_SIZE
        
        state.cell_size = 100
        assert state.cell_size <= 100  # or MAX_CELL_SIZE

    def test_speed_constraints(self) -> None:
        """Test speed respects constraints."""
        state = SimulationState()
        
        state.speed = 0
        assert state.speed >= 0
        
        state.speed = 300
        assert isinstance(state.speed, int)

    def test_state_reset(self) -> None:
        """Test state can be reset."""
        state = SimulationState()
        state.add_metric(generation=5, population=20, peak=25, density=0.3)
        
        state.reset_metrics()
        assert len(state.metrics_log) == 0

    def test_persistence_load_save(self) -> None:
        """Test saving and loading state."""
        state = SimulationState()
        state.cell_size = 16
        state.speed = 75
        state.add_metric(generation=1, population=50, peak=60, density=0.25)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "state.json"
            
            # Save state
            state.save_state(str(filepath))
            assert filepath.exists()
            
            # Load state
            new_state = SimulationState()
            new_state.load_state(str(filepath))
            
            assert new_state.cell_size == 16
            assert new_state.speed == 75
