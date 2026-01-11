import unittest
import numpy as np
from src.core.undo_manager import UndoManager

class TestUndoManager(unittest.TestCase):
    def setUp(self):
        self.manager = UndoManager()

    def test_push_undo_redo(self):
        # Initial State
        state0 = np.zeros((2, 2))
        
        # Apply Action 1
        state1 = np.ones((2, 2))
        self.manager.push_state("Action1", state0)
        
        # Check UnDoing Action 1 (returning to State 0)
        # undo() takes CURRENT state (State 1) to push to redo
        action, target_state = self.manager.undo(state1)
        self.assertEqual(action, "Action1")
        np.testing.assert_array_equal(target_state, state0)
        
        # Now at State 0. Redo stack should contain State 1.
        
        # Check Redoing Action 1 (returning to State 1)
        # redo() takes CURRENT state (State 0) to push to undo
        action, target_state = self.manager.redo(state0)
        self.assertEqual(action, "Action1")
        np.testing.assert_array_equal(target_state, state1)
        
        # Now at State 1. Undo stack should contain State 0.
        action, target_state = self.manager.undo(state1)
        np.testing.assert_array_equal(target_state, state0)

    def test_stack_clearing_on_push(self):
        state0 = "State0"
        state1 = "State1"
        self.manager.push_state("A1", state0)
        
        # Undo to State 0
        self.manager.undo(state1)
        # Redo stack has State 1
        self.assertTrue(self.manager.can_redo())
        
        # New Action from State 0 -> State 2
        state2 = "State2"
        self.manager.push_state("A2", state0)
        
        # Redo stack should be cleared
        self.assertFalse(self.manager.can_redo())

if __name__ == '__main__':
    unittest.main()
