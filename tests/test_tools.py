import unittest
from src.gui.tools import ToolManager, Stamp

class TestToolManager(unittest.TestCase):
    def setUp(self):
        self.manager = ToolManager()

    def test_initial_state(self):
        self.assertEqual(self.manager.active_tool, "pencil")
        self.assertIsNone(self.manager.get_stamp())

    def test_set_tool_pencil(self):
        self.manager.set_eraser()
        self.manager.set_pencil()
        self.assertEqual(self.manager.active_tool, "pencil")
        self.assertIsNone(self.manager.get_stamp())

    def test_set_tool_eraser(self):
        self.manager.set_eraser()
        self.assertEqual(self.manager.active_tool, "eraser")
        self.assertIsNone(self.manager.get_stamp())

    def test_set_stamp(self):
        stamp_data = [(0, 0), (1, 0), (0, 1)]
        stamp = Stamp("TestStamp", stamp_data)
        self.manager.set_stamp(stamp)
        
        self.assertEqual(self.manager.active_tool, "stamp")
        self.assertIsNotNone(self.manager.get_stamp())
        self.assertEqual(self.manager.get_stamp().name, "TestStamp")
        self.assertEqual(self.manager.get_stamp().points, stamp_data)

    def test_switch_back_clears_stamp(self):
        stamp = Stamp("Test", [])
        self.manager.set_stamp(stamp)
        self.manager.set_pencil()
        self.assertEqual(self.manager.active_tool, "pencil")
        self.assertIsNone(self.manager.get_stamp())

if __name__ == '__main__':
    unittest.main()
