"""Tests for Wireworld, Brian's Brain, and Generations automata."""

import numpy as np

from automata.wireworld import Wireworld
from automata.briansbrain import BriansBrain
from automata.generations import GenerationsAutomaton


def test_wireworld_head_advances():
    ww = Wireworld(3, 3)
    ww.grid[1, 1] = Wireworld.HEAD
    ww.step()
    assert ww.grid[1, 1] == Wireworld.TAIL
    ww.step()
    assert ww.grid[1, 1] == Wireworld.CONDUCTOR


def test_wireworld_conductor_becomes_head_with_two_neighbors():
    ww = Wireworld(3, 3)
    ww.grid[:, :] = Wireworld.CONDUCTOR
    ww.grid[1, 0] = Wireworld.HEAD
    ww.grid[0, 1] = Wireworld.HEAD
    ww.step()
    assert ww.grid[1, 1] == Wireworld.HEAD


def test_brians_brain_birth_on_two_neighbors():
    bb = BriansBrain(3, 3)
    bb.grid[0, 1] = BriansBrain.FIRING
    bb.grid[1, 0] = BriansBrain.FIRING
    bb.step()
    assert bb.grid[1, 1] == BriansBrain.FIRING
    bb.step()
    assert bb.grid[1, 1] == BriansBrain.REFRACTORY


def test_generations_decay_and_reset():
    gen = GenerationsAutomaton(3, 3, n_states=4)
    gen.grid[1, 1] = 1
    gen.step()  # without neighbors, should decay
    assert gen.grid[1, 1] == 2
    gen.step()
    assert gen.grid[1, 1] == 3
    gen.step()
    assert gen.grid[1, 1] == 0


def test_generations_birth_and_survival():
    gen = GenerationsAutomaton(3, 3, birth={3}, survival={2, 3}, n_states=4)
    # create 3 neighbors around center
    gen.grid[0, 1] = 1
    gen.grid[1, 0] = 1
    gen.grid[1, 2] = 1
    gen.step()
    assert gen.grid[1, 1] == 1  # birth occurs
    gen.step()
    # with two live neighbors (wrap), should survive as 1
    assert gen.grid[1, 1] in (1, 2, 3)
