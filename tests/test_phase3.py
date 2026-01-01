"""Tests for Phase 3 enhancements: export and pattern browsing."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest

from export_manager import ExportManager
from pattern_browser import PatternBrowser


class TestExportManager:
    """Test export functionality."""

    def test_export_manager_initialization(self) -> None:
        """Test export manager initializes."""
        manager = ExportManager()
        assert manager.theme == "light"
        assert len(manager.frames) == 0

    def test_add_frame(self) -> None:
        """Test adding frames."""
        manager = ExportManager()
        grid = np.zeros((10, 10))
        
        manager.add_frame(grid)
        assert len(manager.frames) == 1

    def test_clear_frames(self) -> None:
        """Test clearing frames."""
        manager = ExportManager()
        grid = np.zeros((10, 10))
        
        manager.add_frame(grid)
        manager.add_frame(grid)
        assert len(manager.frames) == 2
        
        manager.clear_frames()
        assert len(manager.frames) == 0

    def test_export_png(self) -> None:
        """Test exporting PNG."""
        manager = ExportManager()
        grid = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.png"
            result = manager.export_png(grid, str(filepath))
            
            assert result is True
            assert filepath.exists()
            assert filepath.stat().st_size > 0

    def test_export_json(self) -> None:
        """Test exporting JSON."""
        manager = ExportManager()
        grid = np.array([[1, 0], [0, 1]])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.json"
            result = manager.export_json(str(filepath), grid)
            
            assert result is True
            assert filepath.exists()
            
            import json
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data["width"] == 2
            assert data["height"] == 2

    def test_export_json_with_metadata(self) -> None:
        """Test exporting JSON with metadata."""
        manager = ExportManager()
        grid = np.ones((5, 5))
        
        metadata = {
            "generation": 100,
            "population": 25,
            "mode": "Conway's Game of Life",
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.json"
            result = manager.export_json(str(filepath), grid, metadata)
            
            assert result is True
            
            import json
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            assert data["generation"] == 100
            assert data["mode"] == "Conway's Game of Life"

    def test_export_gif(self) -> None:
        """Test exporting GIF."""
        manager = ExportManager()
        
        for i in range(3):
            grid = np.zeros((10, 10))
            grid[i, i] = 1
            manager.add_frame(grid)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.gif"
            result = manager.export_gif(str(filepath))
            
            assert result is True
            assert filepath.exists()

    def test_supported_formats(self) -> None:
        """Test listing supported formats."""
        manager = ExportManager()
        formats = manager.get_supported_formats()
        
        assert "json" in formats
        assert "png" in formats
        assert "gif" in formats

    def test_is_format_supported(self) -> None:
        """Test checking format support."""
        manager = ExportManager()
        
        assert manager.is_format_supported("json")
        assert manager.is_format_supported("png")
        assert manager.is_format_supported("gif")
        assert not manager.is_format_supported("bmp")

    def test_theme_switching(self) -> None:
        """Test switching themes."""
        manager_light = ExportManager(theme="light")
        manager_dark = ExportManager(theme="dark")
        
        assert manager_light.theme == "light"
        assert manager_dark.theme == "dark"


class TestPatternBrowser:
    """Test pattern browsing functionality."""

    def test_pattern_browser_initialization(self) -> None:
        """Test pattern browser initializes."""
        browser = PatternBrowser()
        assert len(browser.get_modes()) > 0

    def test_get_modes(self) -> None:
        """Test getting available modes."""
        browser = PatternBrowser()
        modes = browser.get_modes()
        
        assert isinstance(modes, list)
        assert len(modes) > 0
        assert "Conway's Game of Life" in modes

    def test_get_patterns(self) -> None:
        """Test getting patterns for a mode."""
        browser = PatternBrowser()
        patterns = browser.get_patterns("Conway's Game of Life")
        
        assert isinstance(patterns, list)
        assert len(patterns) > 0

    def test_get_pattern_description(self) -> None:
        """Test getting pattern description."""
        browser = PatternBrowser()
        desc = browser.get_pattern_description("Conway's Game of Life", "Glider Gun")
        
        assert isinstance(desc, str)

    def test_get_pattern_coordinates(self) -> None:
        """Test getting pattern coordinates."""
        browser = PatternBrowser()
        coords = browser.get_pattern_coordinates("Conway's Game of Life", "Beacon")
        
        assert isinstance(coords, list)
        assert len(coords) > 0

    def test_search_patterns_by_name(self) -> None:
        """Test searching patterns by name."""
        browser = PatternBrowser()
        results = browser.search_patterns("gun")
        
        assert isinstance(results, dict)
        if results:
            assert "Conway's Game of Life" in results or "HighLife" in results

    def test_search_patterns_case_insensitive(self) -> None:
        """Test search is case-insensitive."""
        browser = PatternBrowser()
        results_lower = browser.search_patterns("glider")
        results_upper = browser.search_patterns("GLIDER")
        
        assert len(results_lower) == len(results_upper)

    def test_search_patterns_empty_results(self) -> None:
        """Test search with no matches."""
        browser = PatternBrowser()
        results = browser.search_patterns("nonexistent_pattern_xyz")
        
        assert len(results) == 0

    def test_get_patterns_by_description(self) -> None:
        """Test searching by description."""
        browser = PatternBrowser()
        results = browser.get_patterns_by_description("oscillator")
        
        assert isinstance(results, dict)

    def test_get_pattern_info(self) -> None:
        """Test getting complete pattern info."""
        browser = PatternBrowser()
        info = browser.get_pattern_info("Conway's Game of Life", "Beacon")
        
        assert info is not None
        assert info["name"] == "Beacon"
        assert "description" in info
        assert "coordinates" in info

    def test_get_nonexistent_pattern_info(self) -> None:
        """Test getting info for nonexistent pattern."""
        browser = PatternBrowser()
        info = browser.get_pattern_info("Conway's Game of Life", "NonexistentPattern")
        
        assert info is None

    def test_get_most_popular_patterns(self) -> None:
        """Test getting most popular patterns."""
        browser = PatternBrowser()
        patterns = browser.get_most_popular_patterns("Conway's Game of Life", limit=3)
        
        assert isinstance(patterns, list)
        assert len(patterns) <= 3

    def test_get_statistics(self) -> None:
        """Test getting pattern statistics."""
        browser = PatternBrowser()
        stats = browser.get_statistics()
        
        assert "total_modes" in stats
        assert "total_patterns" in stats
        assert "patterns_per_mode" in stats
        assert stats["total_patterns"] > 0

    def test_pattern_cell_count(self) -> None:
        """Test pattern cell count in info."""
        browser = PatternBrowser()
        info = browser.get_pattern_info("Conway's Game of Life", "Beacon")
        
        if info:
            expected_count = len(info["coordinates"])
            assert info["cell_count"] == expected_count
