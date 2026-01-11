"""Tool and Stamp management for the GUI."""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Stamp:
    """A reusable pattern stamp."""

    name: str
    points: List[Tuple[int, int]]
    description: str = ""


class ToolManager:
    """Manages the active tool (Draw, Erase, Stamp)."""

    def __init__(self):
        self.active_tool: str = "pencil"  # pencil, eraser, stamp, selection
        self._current_stamp: Optional[Stamp] = None
        self._clipboard: Optional[Stamp] = None
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_end: Optional[Tuple[int, int]] = None

    def set_pencil(self):
        self.active_tool = "pencil"
        self._current_stamp = None
        self.clear_selection()

    def set_eraser(self):
        self.active_tool = "eraser"
        self._current_stamp = None
        self.clear_selection()

    def set_selection(self):
        self.active_tool = "selection"
        self._current_stamp = None

    def clear_selection(self):
        self.selection_start = None
        self.selection_end = None

    def set_stamp(self, stamp: Stamp):
        self.active_tool = "stamp"
        self._current_stamp = stamp
        self.clear_selection()

    def get_stamp(self) -> Optional[Stamp]:
        return self._current_stamp

    def set_clipboard(self, stamp: Stamp):
        self._clipboard = stamp

    def get_clipboard(self) -> Optional[Stamp]:
        return self._clipboard

    def is_stamp_active(self) -> bool:
        return self.active_tool == "stamp" and self._current_stamp is not None

    def get_selection_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """Return (x1, y1, x2, y2) of the selection, normalized."""
        if not (self.selection_start and self.selection_end):
            return None
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
