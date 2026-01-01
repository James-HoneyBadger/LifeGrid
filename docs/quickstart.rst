Quick Start Guide
=================

This guide will get you up and running with LifeGrid in minutes.

Running the GUI
---------------

The simplest way to use LifeGrid is through the graphical interface:

.. code-block:: bash

   python src/main.py

This opens the main application window where you can:

* Select different cellular automata types
* Load pre-defined patterns
* Draw your own patterns
* Control simulation speed
* Export snapshots and animations

Using the Core Simulator
-------------------------

For programmatic use, scripts, or notebooks:

Basic Example
~~~~~~~~~~~~~

.. code-block:: python

   from src.core.simulator import Simulator
   
   # Create simulator
   sim = Simulator()
   
   # Initialize with Conway's Game of Life
   sim.initialize("Conway's Game of Life")
   
   # Run 100 generations
   sim.step(100)
   
   # Get statistics
   metrics = sim.get_metrics_summary()
   print(f"Population: {metrics['population']}")
   print(f"Peak: {metrics['peak_population']}")

With Configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.core.simulator import Simulator
   from src.core.config import SimulatorConfig
   
   # Create custom configuration
   config = SimulatorConfig(
       width=100,
       height=100,
       speed=50,
       cell_size=5
   )
   
   # Initialize with config
   sim = Simulator(config)
   sim.initialize("Conway's Game of Life", "Glider")
   
   # Run simulation
   for generation in range(100):
       sim.step()
       if generation % 10 == 0:
           print(f"Generation {generation}: {sim.population} cells alive")

Working with Patterns
---------------------

Browse Available Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.pattern_browser import PatternBrowser
   
   browser = PatternBrowser()
   
   # Search for patterns
   results = browser.search_patterns("glider")
   for pattern in results:
       print(f"{pattern['name']}: {pattern['description']}")
   
   # Get pattern info
   info = browser.get_pattern_info("Conway's Game of Life", "Glider")
   print(info)

Load a Pattern
~~~~~~~~~~~~~~

.. code-block:: python

   from src.core.simulator import Simulator
   
   sim = Simulator()
   sim.initialize("Conway's Game of Life", "Gosper Glider Gun")
   sim.step(100)

Exporting Simulations
---------------------

Export as PNG
~~~~~~~~~~~~~

.. code-block:: python

   from src.export_manager import ExportManager
   from src.core.simulator import Simulator
   
   # Run simulation
   sim = Simulator()
   sim.initialize("Conway's Game of Life", "Glider")
   sim.step(50)
   
   # Export snapshot
   export = ExportManager(theme="dark")
   export.export_png(sim.get_grid(), "snapshot.png", cell_size=2)

Export as GIF
~~~~~~~~~~~~~

.. code-block:: python

   from src.export_manager import ExportManager
   from src.core.simulator import Simulator
   
   # Run simulation and collect frames
   sim = Simulator()
   sim.initialize("Conway's Game of Life", "Glider")
   
   export = ExportManager(theme="light")
   
   # Add frames
   for _ in range(50):
       export.add_frame(sim.get_grid())
       sim.step()
   
   # Export animation
   export.export_gif("animation.gif", duration=100, loop=0)

Export Pattern as JSON
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.export_manager import ExportManager
   
   export = ExportManager()
   metadata = {
       "name": "My Pattern",
       "author": "Your Name",
       "description": "A cool pattern"
   }
   export.export_json("pattern.json", grid, metadata)

Using Undo/Redo
---------------

.. code-block:: python

   from src.core.simulator import Simulator
   
   sim = Simulator()
   sim.initialize("Conway's Game of Life", "Glider")
   
   # Run some steps
   sim.step(10)
   print(f"Generation 10: {sim.generation}")
   
   # Undo
   sim.undo()
   print(f"After undo: {sim.generation}")
   
   # Redo
   sim.redo()
   print(f"After redo: {sim.generation}")

Creating Custom Automata
-------------------------

Create a Plugin
~~~~~~~~~~~~~~~

.. code-block:: python

   from src.plugin_system import AutomatonPlugin
   import numpy as np
   
   class MyAutomaton(AutomatonPlugin):
       """A custom cellular automaton."""
       
       def __init__(self):
           super().__init__("My Automaton", "Custom rules")
       
       def step(self, grid: np.ndarray) -> np.ndarray:
           """Implement your rule logic here."""
           # Example: invert all cells
           return 1 - grid
       
       def get_color(self, state: int) -> tuple:
           """Return RGB color for cell state."""
           return (255, 255, 255) if state == 1 else (0, 0, 0)

Register and Use
~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.plugin_system import PluginManager
   
   manager = PluginManager()
   manager.register_plugin(MyAutomaton())
   
   # Create instance
   automaton = manager.create_automaton("My Automaton")
   grid = automaton.step(current_grid)

UI Customization
----------------

Apply a Theme
~~~~~~~~~~~~~

.. code-block:: python

   from src.ui_enhancements import ThemeManager
   
   theme = ThemeManager("dark")
   colors = theme.get_colors()
   
   # Use colors in your UI
   background_color = colors["background"]
   alive_color = colors["alive"]

Keyboard Shortcuts
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.ui_enhancements import KeyboardShortcuts
   
   shortcuts = KeyboardShortcuts()
   
   # Get a shortcut
   play_key = shortcuts.get_shortcut("play_pause")  # "space"
   
   # Customize
   shortcuts.set_shortcut("play_pause", "p")

Speed Presets
~~~~~~~~~~~~~

.. code-block:: python

   from src.ui_enhancements import SpeedPresets
   
   presets = SpeedPresets()
   
   # Get preset speed
   speed = presets.get_preset("fast")  # 100
   
   # Use custom speed
   presets.set_custom_speed(75)

Next Steps
----------

* Explore the full :doc:`user_guide`
* Read the :doc:`api/core` documentation
* Check out more :doc:`examples`
* Learn about :doc:`developer/plugins`
