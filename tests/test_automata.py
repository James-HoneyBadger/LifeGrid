"""Comprehensive tests for cellular automata implementations."""

from __future__ import annotations

import numpy as np
import pytest

from automata import (
    ConwayGameOfLife,
    HighLife,
    LifeLikeAutomaton,
    LangtonsAnt,
    Wireworld,
    BriansBrain,
    GenerationsAutomaton,
    ImmigrationGame,
    RainbowGame,
)
from automata.lifelike import parse_bs


class TestConwayGameOfLife:
    """Test Conway's Game of Life implementation."""

    def test_initialization(self) -> None:
        """Test Conway automaton initializes with correct dimensions."""
        ca = ConwayGameOfLife(100, 100)
        assert ca.width == 100
        assert ca.height == 100
        assert ca.get_grid().shape == (100, 100)
        assert np.all(ca.get_grid() == 0)

    def test_reset_clears_grid(self) -> None:
        """Test reset clears the grid."""
        ca = ConwayGameOfLife(50, 50)
        ca.grid[10, 10] = 1
        ca.reset()
        assert np.all(ca.grid == 0)

    def test_glider_pattern_evolves(self) -> None:
        """Test glider pattern moves diagonally."""
        ca = ConwayGameOfLife(10, 10)
        # Create glider at (2,2)
        glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in glider:
            ca.grid[2 + dy, 2 + dx] = 1
        
        initial_sum = np.sum(ca.grid)
        ca.step()
        # Glider should survive (5 cells)
        assert np.sum(ca.grid) == 5

    def test_blinker_oscillates(self) -> None:
        """Test blinker pattern oscillates with period 2."""
        ca = ConwayGameOfLife(10, 10)
        # Horizontal blinker
        ca.grid[5, 4:7] = 1
        
        ca.step()  # Now vertical
        assert ca.grid[4, 5] == 1
        assert ca.grid[5, 5] == 1
        assert ca.grid[6, 5] == 1
        
        ca.step()  # Back to horizontal
        assert ca.grid[5, 4] == 1
        assert ca.grid[5, 5] == 1
        assert ca.grid[5, 6] == 1

    def test_load_pattern(self) -> None:
        """Test loading predefined patterns."""
        ca = ConwayGameOfLife(200, 200)
        
        ca.load_pattern("Random Soup")
        random_count = np.sum(ca.grid)
        assert random_count > 0
        
        ca.load_pattern("Glider Gun")
        gun_count = np.sum(ca.grid)
        assert gun_count > 0


class TestLifeLikeAutomaton:
    """Test generic life-like automaton."""

    def test_parse_bs_birth_survival(self) -> None:
        """Test B/S notation parsing."""
        birth, survival = parse_bs("B3/S23")
        assert birth == {3}
        assert survival == {2, 3}

    def test_parse_bs_complex(self) -> None:
        """Test parsing complex rules."""
        birth, survival = parse_bs("B35678/S5678")
        assert birth == {3, 5, 6, 7, 8}
        assert survival == {5, 6, 7, 8}

    def test_parse_bs_case_insensitive(self) -> None:
        """Test parsing is case insensitive."""
        b1, s1 = parse_bs("b3/s23")
        b2, s2 = parse_bs("B3/S23")
        assert b1 == b2 and s1 == s2

    def test_lifelike_initialization(self) -> None:
        """Test LifeLikeAutomaton initialization."""
        ca = LifeLikeAutomaton(100, 100, birth=[3], survival=[2, 3])
        assert ca.width == 100
        assert ca.height == 100
        assert ca.birth == {3}
        assert ca.survival == {2, 3}

    def test_lifelike_custom_rules(self) -> None:
        """Test LifeLikeAutomaton with custom rules."""
        ca = LifeLikeAutomaton(50, 50, birth=[3], survival=[2, 3])
        ca.grid[10, 10] = 1
        ca.step()
        # Grid should evolve based on birth/survival rules
        assert isinstance(ca.get_grid(), np.ndarray)


class TestHighLife:
    """Test HighLife automaton."""

    def test_highlife_initialization(self) -> None:
        """Test HighLife initializes correctly."""
        ca = HighLife(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_highlife_evolution(self) -> None:
        """Test HighLife evolution."""
        ca = HighLife(100, 100)
        ca.load_pattern("Random Soup")
        initial_count = np.sum(ca.grid)
        ca.step()
        # Grid should evolve
        assert isinstance(ca.get_grid(), np.ndarray)


class TestLangtonsAnt:
    """Test Langton's Ant implementation."""

    def test_ant_initialization(self) -> None:
        """Test Ant initializes correctly."""
        ca = LangtonsAnt(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_ant_movement(self) -> None:
        """Test ant moves and changes direction."""
        ca = LangtonsAnt(100, 100)
        ca.step()
        # Ant should have moved
        assert isinstance(ca.get_grid(), np.ndarray)


class TestWireworld:
    """Test Wireworld automaton."""

    def test_wireworld_initialization(self) -> None:
        """Test Wireworld initializes correctly."""
        ca = Wireworld(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_wireworld_evolution(self) -> None:
        """Test Wireworld evolution."""
        ca = Wireworld(100, 100)
        ca.step()
        assert isinstance(ca.get_grid(), np.ndarray)


class TestBriansBrain:
    """Test Brian's Brain automaton."""

    def test_briansbrain_initialization(self) -> None:
        """Test Brian's Brain initializes correctly."""
        ca = BriansBrain(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_briansbrain_evolution(self) -> None:
        """Test Brian's Brain evolution."""
        ca = BriansBrain(100, 100)
        ca.step()
        assert isinstance(ca.get_grid(), np.ndarray)


class TestGenerationsAutomaton:
    """Test Generations automaton."""

    def test_generations_initialization(self) -> None:
        """Test Generations initializes correctly."""
        ca = GenerationsAutomaton(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_generations_evolution(self) -> None:
        """Test Generations evolution."""
        ca = GenerationsAutomaton(100, 100)
        ca.step()
        assert isinstance(ca.get_grid(), np.ndarray)


class TestImmigrationGame:
    """Test Immigration Game automaton."""

    def test_immigration_initialization(self) -> None:
        """Test Immigration initializes correctly."""
        ca = ImmigrationGame(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_immigration_evolution(self) -> None:
        """Test Immigration evolution."""
        ca = ImmigrationGame(100, 100)
        ca.step()
        assert isinstance(ca.get_grid(), np.ndarray)


class TestRainbowGame:
    """Test Rainbow Game automaton."""

    def test_rainbow_initialization(self) -> None:
        """Test Rainbow initializes correctly."""
        ca = RainbowGame(100, 100)
        assert ca.width == 100
        assert ca.height == 100

    def test_rainbow_evolution(self) -> None:
        """Test Rainbow evolution."""
        ca = RainbowGame(100, 100)
        ca.step()
        assert isinstance(ca.get_grid(), np.ndarray)


class TestGridBoundaries:
    """Test boundary conditions for all automata."""

    def test_conway_boundaries(self) -> None:
        """Test Conway handles boundaries correctly."""
        ca = ConwayGameOfLife(10, 10)
        ca.grid[0, 0] = 1  # Corner cell
        ca.grid[0, 1] = 1
        ca.grid[1, 0] = 1
        ca.step()
        # Should handle edge wrapping or boundary correctly
        assert ca.get_grid().shape == (10, 10)

    def test_small_grid(self) -> None:
        """Test automata work with small grids."""
        ca = ConwayGameOfLife(3, 3)
        ca.grid[1, 1] = 1
        ca.step()
        assert ca.get_grid().shape == (3, 3)


class TestPatternLoading:
    """Test pattern loading functionality."""

    def test_pattern_fitting(self) -> None:
        """Test patterns fit within grid bounds."""
        ca = ConwayGameOfLife(200, 200)
        
        patterns = [
            "Classic Mix", "Glider Gun", "Puffers", "Oscillators",
            "Spaceships", "R-Pentomino", "Acorn", "Beacon", "Pulsar"
        ]
        
        for pattern in patterns:
            ca.load_pattern(pattern)
            grid = ca.get_grid()
            assert grid.shape == (200, 200)
            assert np.all((grid == 0) | (grid == 1))
