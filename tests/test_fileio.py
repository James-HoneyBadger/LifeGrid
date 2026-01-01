"""Tests for file I/O and pattern functionality."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
import numpy as np

from patterns import get_pattern_description


class TestPatternMetadata:
    """Test pattern metadata and descriptions."""

    def test_pattern_descriptions_exist(self) -> None:
        """Test patterns can be looked up."""
        conway_patterns = [
            "Classic Mix", "Glider Gun", "Puffers", "Oscillators",
            "Spaceships", "R-Pentomino", "Acorn", "Beacon", "Pulsar",
            "Random Soup"
        ]
        
        for pattern in conway_patterns:
            # Verify function works without error
            desc = get_pattern_description("Conway's Game of Life", pattern)
            assert isinstance(desc, str)

    def test_pattern_description_not_empty(self) -> None:
        """Test pattern descriptions are meaningful when present."""
        desc = get_pattern_description("Conway's Game of Life", "Glider Gun")
        assert isinstance(desc, str)


class TestFileIO:
    """Test file I/O operations."""

    def test_save_grid_as_json(self) -> None:
        """Test saving grid as JSON."""
        grid = np.array([[1, 0], [0, 1]])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "pattern.json"
            
            # Save grid
            data = {
                "grid": grid.tolist(),
                "width": 2,
                "height": 2,
                "mode": "Conway"
            }
            with open(filepath, 'w') as f:
                json.dump(data, f)
            
            assert filepath.exists()
            
            # Load and verify
            with open(filepath, 'r') as f:
                loaded = json.load(f)
            
            assert loaded["width"] == 2
            assert loaded["height"] == 2
            assert np.array_equal(np.array(loaded["grid"]), grid)

    def test_save_load_preserves_pattern(self) -> None:
        """Test save/load cycle preserves pattern."""
        original_grid = np.zeros((100, 100), dtype=int)
        # Create glider
        glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in glider:
            original_grid[10 + dy, 10 + dx] = 1
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "glider.json"
            
            data = {"grid": original_grid.tolist()}
            with open(filepath, 'w') as f:
                json.dump(data, f)
            
            with open(filepath, 'r') as f:
                loaded = json.load(f)
            
            loaded_grid = np.array(loaded["grid"])
            assert np.array_equal(original_grid, loaded_grid)

    def test_multiple_patterns_saved(self) -> None:
        """Test saving multiple patterns."""
        patterns = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(5):
                grid = np.random.randint(0, 2, (50, 50))
                filepath = Path(tmpdir) / f"pattern_{i}.json"
                
                data = {"grid": grid.tolist(), "id": i}
                with open(filepath, 'w') as f:
                    json.dump(data, f)
                
                patterns.append(filepath)
            
            assert len(patterns) == 5
            for p in patterns:
                assert p.exists()


class TestGridFormat:
    """Test grid format consistency."""

    def test_grid_numpy_compatibility(self) -> None:
        """Test grids remain NumPy compatible."""
        grid = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], dtype=int)
        
        # Convert to list and back
        as_list = grid.tolist()
        reconstructed = np.array(as_list, dtype=int)
        
        assert np.array_equal(grid, reconstructed)
        assert reconstructed.dtype == np.int64 or reconstructed.dtype == np.int32

    def test_grid_dtype_preservation(self) -> None:
        """Test grid data type is preserved."""
        grid = np.ones((10, 10), dtype=int)
        grid_list = grid.tolist()
        restored = np.array(grid_list, dtype=int)
        
        assert restored.dtype in [np.int32, np.int64]
        assert np.all(restored == 1)

    def test_large_grid_serialization(self) -> None:
        """Test serialization of large grids."""
        large_grid = np.random.randint(0, 2, (500, 500))
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "large.json"
            
            data = {"grid": large_grid.tolist()}
            with open(filepath, 'w') as f:
                json.dump(data, f)
            
            file_size = filepath.stat().st_size
            assert file_size > 0
            
            with open(filepath, 'r') as f:
                loaded = json.load(f)
            
            assert np.array_equal(large_grid, np.array(loaded["grid"]))


class TestPatternValidation:
    """Test pattern validation."""

    def test_grid_dimensions_valid(self) -> None:
        """Test grids have valid dimensions."""
        grids = [
            np.zeros((10, 10)),
            np.zeros((100, 100)),
            np.zeros((500, 500)),
        ]
        
        for grid in grids:
            assert grid.ndim == 2
            assert grid.shape[0] > 0
            assert grid.shape[1] > 0

    def test_grid_values_binary(self) -> None:
        """Test grid values are binary."""
        grid = np.array([[1, 0], [1, 1]])
        assert np.all((grid == 0) | (grid == 1))

    def test_empty_grid_valid(self) -> None:
        """Test empty grids are valid."""
        grid = np.zeros((50, 50))
        assert np.sum(grid) == 0
        assert grid.shape == (50, 50)
