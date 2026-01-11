import unittest
from src.gui.tools import ToolManager, Stamp

class TestToolManagerSelection(unittest.TestCase):
    def setUp(self):
        self.manager = ToolManager()

    def test_selection_tool_activation(self):
        self.manager.set_selection()
        self.assertEqual(self.manager.active_tool, "selection")
        self.assertIsNone(self.manager.get_stamp())

    def test_selection_coordinates(self):
        self.manager.set_selection()
        self.manager.selection_start = (10, 10)
        self.manager.selection_end = (20, 20)
        
        rect = self.manager.get_selection_rect()
        self.assertEqual(rect, (10, 10, 20, 20))

    def test_selection_rect_normalization(self):
        self.manager.set_selection()
        # Dragging backwards (right-bottom to top-left)
        self.manager.selection_start = (20, 20)
        self.manager.selection_end = (10, 10)
        
        rect = self.manager.get_selection_rect()
        # Should be normalized to min_x, min_y, max_x, max_y
        self.assertEqual(rect, (10, 10, 20, 20))

    def test_clipboard(self):
        stamp = Stamp("Clip", [(0,0)])
        self.manager.set_clipboard(stamp)
        self.assertEqual(self.manager.get_clipboard(), stamp)

    def test_switching_tool_clears_selection(self):
        self.manager.set_selection()
        self.manager.selection_start = (5, 5)
        self.manager.selection_end = (10, 10)
        
        self.manager.set_pencil()
        self.assertIsNone(self.manager.selection_start)
        self.assertIsNone(self.manager.selection_end)
        self.assertEqual(self.manager.active_tool, "pencil")

if __name__ == '__main__':
    unittest.main()
