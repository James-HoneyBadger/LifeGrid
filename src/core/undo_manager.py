"""Undo/redo system for the simulator."""

from __future__ import annotations

from typing import Any, Deque, List
from collections import deque

import numpy as np


class UndoManager:
    """Manages undo/redo history for simulation state.
    
    Supports arbitrary undo/redo for pattern editing, generation steps,
    and other simulation state changes.
    """

    def __init__(self, max_history: int = 100) -> None:
        """Initialize undo manager.
        
        Args:
            max_history: Maximum number of states to keep in history
        """
        self.max_history = max_history
        self.undo_stack: Deque[tuple[str, Any]] = deque(maxlen=max_history)
        self.redo_stack: Deque[tuple[str, Any]] = deque(maxlen=max_history)

    def push_state(self, action_name: str, state: Any) -> None:
        """Push a new state onto the undo stack.
        
        Args:
            action_name: Description of the action
            state: State object (typically a grid)
        """
        # Copy grid if it's a numpy array
        state_copy = np.copy(state) if isinstance(state, np.ndarray) else state
        self.undo_stack.append((action_name, state_copy))
        self.redo_stack.clear()

    def undo(self) -> tuple[str, Any] | None:
        """Undo the last action.
        
        Returns:
            Tuple of (action_name, state) or None if no undo available
        """
        if not self.undo_stack:
            return None
        
        action_name, state = self.undo_stack.pop()
        self.redo_stack.append((action_name, state))
        return (action_name, state)

    def redo(self) -> tuple[str, Any] | None:
        """Redo the last undone action.
        
        Returns:
            Tuple of (action_name, state) or None if no redo available
        """
        if not self.redo_stack:
            return None
        
        action_name, state = self.redo_stack.pop()
        self.undo_stack.append((action_name, state))
        return (action_name, state)

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self.undo_stack) > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self.redo_stack) > 0

    def clear(self) -> None:
        """Clear all history."""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_history_summary(self) -> dict:
        """Get summary of undo/redo history.
        
        Returns:
            Dict with history info for display
        """
        undo_actions = [name for name, _ in self.undo_stack]
        redo_actions = [name for name, _ in self.redo_stack]
        
        return {
            "undo_count": len(self.undo_stack),
            "redo_count": len(self.redo_stack),
            "last_undo_action": undo_actions[-1] if undo_actions else None,
            "last_redo_action": redo_actions[-1] if redo_actions else None,
        }
