"""Cellular Automaton implementations"""

from .base import CellularAutomaton
from .conway import ConwayGameOfLife
from .highlife import HighLife
from .immigration import ImmigrationGame
from .rainbow import RainbowGame
from .ant import LangtonsAnt
from .lifelike import LifeLikeAutomaton, parse_bs
from .wireworld import Wireworld
from .briansbrain import BriansBrain
from .generations import GenerationsAutomaton

__all__ = [
    "CellularAutomaton",
    "ConwayGameOfLife",
    "HighLife",
    "ImmigrationGame",
    "RainbowGame",
    "LangtonsAnt",
    "LifeLikeAutomaton",
    "parse_bs",
    "Wireworld",
    "BriansBrain",
    "GenerationsAutomaton",
]
