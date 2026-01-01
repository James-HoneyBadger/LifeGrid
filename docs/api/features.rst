Features API
============

This module contains additional features like export, pattern browsing, plugins, and UI enhancements.

Export Manager
--------------

.. automodule:: export_manager
   :members:
   :undoc-members:
   :show-inheritance:

Export simulations in multiple formats (PNG, GIF, JSON).

**Example:**

.. code-block:: python

   from export_manager import ExportManager
   import numpy as np
   
   export = ExportManager(theme="dark")
   grid = np.random.randint(0, 2, (50, 50))
   
   # PNG export
   export.export_png(grid, "snapshot.png", cell_size=2)
   
   # GIF export
   for _ in range(50):
       export.add_frame(grid)
       grid = automaton.step(grid)
   export.export_gif("animation.gif", duration=100)
   
   # JSON export
   export.export_json("pattern.json", grid, {"name": "My Pattern"})

Pattern Browser
---------------

.. automodule:: pattern_browser
   :members:
   :undoc-members:
   :show-inheritance:

Search and discover built-in patterns.

**Example:**

.. code-block:: python

   from pattern_browser import PatternBrowser
   
   browser = PatternBrowser()
   
   # Search patterns
   results = browser.search_patterns("glider")
   
   # Get pattern info
   info = browser.get_pattern_info("Conway's Game of Life", "Glider")
   
   # Get statistics
   stats = browser.get_statistics()
   print(f"Total patterns: {stats['total_patterns']}")

Plugin System
-------------

.. automodule:: plugin_system
   :members:
   :undoc-members:
   :show-inheritance:

Create and register custom cellular automata.

**Example:**

.. code-block:: python

   from plugin_system import AutomatonPlugin, PluginManager
   import numpy as np
   
   class MyAutomaton(AutomatonPlugin):
       def __init__(self):
           super().__init__("My Automaton", "Custom rules")
       
       def step(self, grid: np.ndarray) -> np.ndarray:
           # Implement your logic
           return modified_grid
       
       def get_color(self, state: int) -> tuple:
           return (255, 255, 255) if state else (0, 0, 0)
   
   # Register and use
   manager = PluginManager()
   manager.register_plugin(MyAutomaton())
   automaton = manager.create_automaton("My Automaton")

Configuration Manager
---------------------

.. automodule:: config_manager
   :members:
   :undoc-members:
   :show-inheritance:

Manage application configuration with persistence.

**Example:**

.. code-block:: python

   from config_manager import AppConfig
   
   # Load configuration
   config = AppConfig.load("config.json")
   
   # Modify settings
   config.theme = "dark"
   config.window_width = 1200
   
   # Save
   config.save("config.json")

UI Enhancements
---------------

.. automodule:: ui_enhancements
   :members:
   :undoc-members:
   :show-inheritance:

Theme management, keyboard shortcuts, tooltips, and speed presets.

Theme Manager
~~~~~~~~~~~~~

**Example:**

.. code-block:: python

   from ui_enhancements import ThemeManager
   
   theme = ThemeManager("dark")
   colors = theme.get_colors()
   
   # Apply callback
   def on_theme_changed(theme_name):
       print(f"Theme changed to {theme_name}")
   
   theme.on_theme_change(on_theme_changed)
   theme.set_theme("light")

Keyboard Shortcuts
~~~~~~~~~~~~~~~~~~

**Example:**

.. code-block:: python

   from ui_enhancements import KeyboardShortcuts
   
   shortcuts = KeyboardShortcuts()
   
   # Get shortcut
   key = shortcuts.get_shortcut("play_pause")
   
   # Customize
   shortcuts.set_shortcut("step", "s")

Tooltips
~~~~~~~~

**Example:**

.. code-block:: python

   from ui_enhancements import Tooltips
   
   tooltips = Tooltips()
   help_text = tooltips.get_tooltip("play_pause")

Speed Presets
~~~~~~~~~~~~~

**Example:**

.. code-block:: python

   from ui_enhancements import SpeedPresets
   
   presets = SpeedPresets()
   speed = presets.get_preset("fast")
   presets.set_custom_speed(75)
