"""Cellular Automaton implementations"""

from .base import CellularAutomaton
from .conway import ConwayGameOfLife
from .highlife import HighLife
from .immigration import ImmigrationGame
from .rainbow import RainbowGame
from .ant import LangtonsAnt
from .lifelike import LifeLikeAutomaton, parse_bs

__all__ = [
    "CellularAutomaton",
    "ConwayGameOfLife",
    "HighLife",
    "ImmigrationGame",
    "RainbowGame",
    "LangtonsAnt",
    "LifeLikeAutomaton",
    "parse_bs",
]
