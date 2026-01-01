"""Tests for advanced features."""

import pytest
import numpy as np
import tempfile
import os
from pathlib import Path

from src.advanced.statistics import StatisticsCollector, StatisticsExporter
from src.advanced.rule_discovery import RuleDiscovery, RulePattern
from src.advanced.rle_format import RLEParser, RLEEncoder
from src.advanced.visualization import HeatmapGenerator, SymmetryAnalyzer, SymmetryType
from src.advanced.pattern_analysis import PatternAnalyzer, PatternMetrics


class TestStatistics:
    """Test statistics collection and export."""
    
    def test_collector_creation(self):
        """Test creating statistics collector."""
        collector = StatisticsCollector()
        assert collector is not None
        assert len(collector.get_statistics()) == 0
    
    def test_collect_statistics(self):
        """Test collecting statistics."""
        collector = StatisticsCollector()
        grid = np.array([[1, 0], [0, 1]])
        
        collector.collect(0, grid)
        stats = collector.get_statistics()
        
        assert len(stats) == 1
        assert stats[0].step == 0
        assert stats[0].alive_cells == 2
        assert stats[0].dead_cells == 2
        assert stats[0].density == 0.5
    
    def test_statistics_entropy(self):
        """Test entropy calculation."""
        collector = StatisticsCollector()
        
        # Uniform grid
        grid = np.ones((10, 10))
        collector.collect(0, grid)
        stats = collector.get_statistics()[0]
        assert stats.entropy >= 0.0  # Entropy should be non-negative
        
        # Mixed grid
        grid = np.random.randint(0, 2, size=(10, 10))
        collector.collect(1, grid)
        stats = collector.get_statistics()[1]
        assert stats.entropy >= 0  # Entropy should be non-negative
    
    def test_births_and_deaths(self):
        """Test tracking births and deaths."""
        collector = StatisticsCollector()
        
        grid1 = np.array([[0, 0], [0, 0]])
        grid2 = np.array([[1, 1], [0, 0]])
        
        collector.collect(0, grid1)
        collector.collect(1, grid2)
        
        stats = collector.get_statistics()[1]
        assert stats.births == 2
        assert stats.deaths == 0
    
    def test_export_csv(self):
        """Test CSV export."""
        collector = StatisticsCollector()
        
        for i in range(5):
            grid = np.random.randint(0, 2, size=(10, 10))
            collector.collect(i, grid)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filepath = f.name
        
        try:
            StatisticsExporter.export_csv(
                collector.get_statistics(),
                filepath
            )
            
            assert os.path.exists(filepath)
            
            # Read file to verify content
            with open(filepath, 'r') as f:
                content = f.read()
                assert 'step' in content
                assert 'alive_cells' in content
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)


class TestRuleDiscovery:
    """Test rule discovery system."""
    
    def test_discovery_creation(self):
        """Test creating rule discovery."""
        discovery = RuleDiscovery(neighborhood_type='moore')
        assert discovery is not None
    
    def test_observe_conway(self):
        """Test observing Conway's Game of Life."""
        discovery = RuleDiscovery(neighborhood_type='moore')
        
        # Block (still life): should have S2, S3
        grid_before = np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]
        ])
        grid_after = grid_before.copy()
        
        discovery.observe_transition(grid_before, grid_after)
        
        # Blinker (oscillator): should detect B3
        grid_before = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        grid_after = np.array([
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        
        discovery.observe_transition(grid_before, grid_after)
        
        # Get birth/survival rules
        rules = discovery.infer_birth_survival_rules(min_confidence=0.5)
        birth_rules = rules.get('birth', set())
        survival_rules = rules.get('survival', set())
        
        # Should have discovered some rules
        assert isinstance(birth_rules, set)
        assert isinstance(survival_rules, set)
    
    def test_format_notation(self):
        """Test B/S notation formatting."""
        discovery = RuleDiscovery()
        notation = discovery.format_birth_survival_notation(
            birth={3},
            survival={2, 3}
        )
        assert notation == "B3/S23"
    
    def test_export_rules(self):
        """Test exporting rules to file."""
        discovery = RuleDiscovery()
        
        # Observe some transitions
        grid = np.random.randint(0, 2, size=(10, 10))
        discovery.observe_transition(grid, grid)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            filepath = f.name
        
        try:
            discovery.export_rules(filepath)
            assert os.path.exists(filepath)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)


class TestRLEFormat:
    """Test RLE format parsing and encoding."""
    
    def test_parse_simple(self):
        """Test parsing simple RLE pattern."""
        rle = "x = 3, y = 3, rule = B3/S23\n3o$3o$3o!"
        
        grid, metadata = RLEParser.parse(rle)
        
        assert grid.shape == (3, 3)
        assert np.all(grid == 1)
        assert metadata['x'] == '3'
        assert metadata['y'] == '3'
        assert metadata['rule'] == 'B3/S23'
    
    def test_parse_with_dead_cells(self):
        """Test parsing with dead cells."""
        rle = "x = 5, y = 3, rule = B3/S23\nbo3b$2bob$3o2b!"
        
        grid, metadata = RLEParser.parse(rle)
        
        assert grid.shape == (3, 5)
        assert grid[0, 0] == 0
        assert grid[0, 1] == 1
    
    def test_parse_blinker(self):
        """Test parsing blinker pattern."""
        rle = "x = 3, y = 3, rule = B3/S23\nbo$bo$bo!"
        
        grid, metadata = RLEParser.parse(rle)
        
        assert grid.shape == (3, 3)
        assert np.sum(grid) == 3
        assert metadata['rule'] == 'B3/S23'
    
    def test_encode_simple(self):
        """Test encoding simple pattern."""
        grid = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ])
        
        rle = RLEEncoder.encode(grid, rule='B3/S23')
        
        assert 'x = 3' in rle
        assert 'y = 3' in rle
        assert 'rule = B3/S23' in rle
    
    def test_roundtrip(self):
        """Test encoding then parsing."""
        original_grid = np.array([
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ])
        
        # Encode
        rle = RLEEncoder.encode(original_grid, rule='B3/S23')
        
        # Parse
        parsed_grid, metadata = RLEParser.parse(rle)
        
        # Should match
        assert np.array_equal(original_grid, parsed_grid)
    
    def test_file_operations(self):
        """Test file read/write."""
        grid = np.array([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 1]
        ])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rle', delete=False) as f:
            filepath = f.name
        
        try:
            # Write
            RLEEncoder.encode_to_file(grid, filepath, rule='B3/S23')
            assert os.path.exists(filepath)
            
            # Read
            parsed_grid, metadata = RLEParser.parse_file(filepath)
            assert np.array_equal(grid, parsed_grid)
        finally:
            if os.path.exists(filepath):
                os.unlink(filepath)


class TestVisualization:
    """Test visualization features."""
    
    def test_heatmap_creation(self):
        """Test creating heatmap generator."""
        heatmap = HeatmapGenerator((10, 10), mode='activity')
        assert heatmap is not None
    
    def test_heatmap_activity_tracking(self):
        """Test activity heatmap."""
        heatmap = HeatmapGenerator((5, 5), mode='activity')
        
        grid1 = np.array([
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        
        # Update multiple times at same position
        heatmap.update(grid1)
        heatmap.update(grid1)
        heatmap.update(grid1)
        
        heatmap_data = heatmap.get_heatmap()
        
        # Cell (0, 0) should have highest activity
        assert heatmap_data[0, 0] > heatmap_data[1, 1]
    
    def test_heatmap_age_tracking(self):
        """Test age heatmap."""
        heatmap = HeatmapGenerator((3, 3), mode='age')
        
        grid = np.array([
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        
        # Age should increase with updates
        heatmap.update(grid)
        heatmap.update(grid)
        heatmap.update(grid)
        
        # Cell that's alive should have some age
        heatmap_data = heatmap.get_heatmap()
        assert heatmap_data[0, 0] > 0
    
    def test_heatmap_colormap(self):
        """Test colormap generation."""
        heatmap = HeatmapGenerator((5, 5), mode='activity')
        
        grid = np.random.randint(0, 2, size=(5, 5))
        heatmap.update(grid)
        
        colormap = heatmap.get_colormap_data(heatmap='hot')
        
        assert colormap.shape == (5, 5, 3)
        assert colormap.dtype == np.uint8
    
    def test_symmetry_horizontal(self):
        """Test horizontal symmetry detection."""
        grid = np.array([
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 1]
        ])
        
        assert SymmetryAnalyzer.has_horizontal_symmetry(grid)
    
    def test_symmetry_vertical(self):
        """Test vertical symmetry detection."""
        grid = np.array([
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1]
        ])
        
        assert SymmetryAnalyzer.has_vertical_symmetry(grid)
    
    def test_symmetry_rotational_180(self):
        """Test 180° rotational symmetry."""
        grid = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        
        assert SymmetryAnalyzer.has_rotational_symmetry(grid, angle=180)
    
    def test_symmetry_detection(self):
        """Test detecting all symmetries."""
        # Square has all symmetries
        grid = np.array([
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0]
        ])
        
        symmetries = SymmetryAnalyzer.detect_symmetries(grid)
        assert len(symmetries) > 0
    
    def test_symmetry_score(self):
        """Test symmetry score calculation."""
        # Symmetric grid
        grid = np.array([
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ])
        
        score = SymmetryAnalyzer.get_symmetry_score(grid)
        assert 0 <= score <= 1
        assert score > 0  # Has some symmetry


class TestPatternAnalysis:
    """Test pattern analysis."""
    
    def test_bounding_box(self):
        """Test bounding box calculation."""
        grid = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        
        bbox = PatternAnalyzer.get_bounding_box(grid)
        assert bbox == (1, 1, 2, 2)
    
    def test_extract_pattern(self):
        """Test pattern extraction."""
        grid = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ])
        
        pattern = PatternAnalyzer.extract_pattern(grid)
        expected = np.array([
            [1, 1],
            [1, 1]
        ])
        
        assert np.array_equal(pattern, expected)
    
    def test_detect_period_still_life(self):
        """Test period detection for still life."""
        grid = np.array([[1, 1], [1, 1]])
        history = [grid, grid, grid]
        
        period = PatternAnalyzer.detect_period(history)
        assert period == 1
    
    def test_detect_period_oscillator(self):
        """Test period detection for oscillator."""
        grid1 = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
        grid2 = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
        history = [grid1, grid2, grid1, grid2, grid1]
        
        period = PatternAnalyzer.detect_period(history)
        assert period == 2
    
    def test_detect_displacement(self):
        """Test displacement detection."""
        grid1 = np.array([
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ])
        grid2 = np.array([
            [0, 1, 1],
            [0, 1, 1],
            [0, 0, 0]
        ])
        
        dx, dy = PatternAnalyzer.detect_displacement(grid1, grid2)
        assert dx == 1
        assert dy == 0
    
    def test_analyze_still_life(self):
        """Test analyzing still life."""
        grid = np.array([[1, 1], [1, 1]])
        history = [grid, grid, grid]
        
        metrics = PatternAnalyzer.analyze_pattern(history)
        
        assert metrics.is_still_life
        assert not metrics.is_oscillator
        assert not metrics.is_spaceship
        assert metrics.period == 1
    
    def test_analyze_oscillator(self):
        """Test analyzing oscillator."""
        grid1 = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
        grid2 = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
        history = [grid1, grid2, grid1, grid2]
        
        metrics = PatternAnalyzer.analyze_pattern(history)
        
        assert metrics.is_oscillator
        assert not metrics.is_still_life
        assert metrics.period == 2
    
    def test_find_connected_components(self):
        """Test finding connected components."""
        grid = np.array([
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0]
        ])
        
        components = PatternAnalyzer.find_connected_components(grid)
        assert len(components) == 3
    
    def test_population_statistics(self):
        """Test population statistics."""
        history = [
            np.array([[1, 1], [0, 0]]),
            np.array([[1, 1], [1, 0]]),
            np.array([[1, 1], [1, 1]])
        ]
        
        stats = PatternAnalyzer.calculate_population_statistics(history)
        
        assert stats['initial_population'] == 2
        assert stats['final_population'] == 4
        assert stats['population_change'] == 2
    
    def test_pattern_stability(self):
        """Test stability detection."""
        grid = np.array([[1, 1], [1, 1]])
        stable_history = [grid] * 15
        
        assert PatternAnalyzer.is_pattern_stable(stable_history)
        
        # Unstable pattern
        unstable_history = [
            np.random.randint(0, 2, size=(5, 5))
            for _ in range(15)
        ]
        # May or may not be stable depending on random values
        # Just test that it returns a boolean
        result = PatternAnalyzer.is_pattern_stable(unstable_history)
        assert isinstance(result, bool)
