import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock dependencies that require display
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()

# Configure StringVar to return a valid default mode
sys.modules['tkinter'].StringVar.return_value.get.return_value = "Conway's Game of Life"

# Mock PIL if needed (installing requirements included Pillow, so maybe not needed? 
# but it might try to load libraries on import)
# Let's use real PIL if available, or mock if it fails.
# Actually, the app handles missing PIL gracefully.

from src.gui.app import AutomatonApp
from src.gui.config import MODE_FACTORIES, MODE_PATTERNS
import src.plugin_system

class TestPluginFull(unittest.TestCase):
    def setUp(self):
        # Reset global state
        self.original_factories = MODE_FACTORIES.copy()
        self.original_patterns = MODE_PATTERNS.copy()
        
        # Mock Root
        self.root = MagicMock()
        # Mock geometry for ui.build_ui
        self.root.winfo_reqwidth.return_value = 800
        self.root.winfo_reqheight.return_value = 600
        self.root.winfo_screenwidth.return_value = 1920
        self.root.winfo_screenheight.return_value = 1080

    def tearDown(self):
        MODE_FACTORIES.clear()
        MODE_FACTORIES.update(self.original_factories)
        MODE_PATTERNS.clear()
        MODE_PATTERNS.update(self.original_patterns)

    def test_app_loads_day_and_night_plugin(self):
        # Initialize App
        # This triggers _load_plugins -> PluginManager.load_plugins_from_directory
        app = AutomatonApp(self.root)
        
        # Verify Day & Night was registered
        self.assertIn("Day & Night", MODE_FACTORIES)
        
        # Verify we can switch to it
        # This will call switch_mode -> factory() -> automaton creation
        # Since we use real numpy, this should work.
        # However, switch_mode also calls _update_display, which draws to canvas.
        # self.widgets.canvas is a Mock (from build_ui using mocked ttk/tk).
        # Real numpy grid passed to draw_grid -> calls canvas methods on Mock.
        
        # We need to manually invoke switch_mode or verify it works
        # app.switch_mode("Day & Night") 
        # But wait, app.__init__ calls switch_mode(default).
        # Let's call it manually for the plugin.
        
        app.switch_mode("Day & Night")
        
        current_auto = app.state.current_automaton
        self.assertIsNotNone(current_auto)
        # Verify it has the specific rules of Day & Night (B3678/S34678)
        self.assertEqual(current_auto.birth, {3, 6, 7, 8})
        self.assertEqual(current_auto.survival, {3, 4, 6, 7, 8})

if __name__ == '__main__':
    unittest.main()
