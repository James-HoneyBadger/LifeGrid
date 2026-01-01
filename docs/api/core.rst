Core Module API
===============

The core module provides GUI-independent simulation capabilities that can be used in scripts, notebooks, or headless environments.

Simulator
---------

.. automodule:: core.simulator
   :members:
   :undoc-members:
   :show-inheritance:

The Simulator class is the main entry point for running cellular automaton simulations programmatically.

**Example:**

.. code-block:: python

   from core.simulator import Simulator
   
   sim = Simulator()
   sim.initialize("Conway's Game of Life", "Glider")
   sim.step(100)
   metrics = sim.get_metrics_summary()

Configuration
-------------

.. automodule:: core.config
   :members:
   :undoc-members:
   :show-inheritance:

The SimulatorConfig dataclass holds all configuration parameters for the simulator.

**Example:**

.. code-block:: python

   from core.config import SimulatorConfig
   
   config = SimulatorConfig(
       width=100,
       height=100,
       speed=50,
       cell_size=5
   )

Undo Manager
------------

.. automodule:: core.undo_manager
   :members:
   :undoc-members:
   :show-inheritance:

The UndoManager provides undo/redo functionality with configurable history depth.

**Example:**

.. code-block:: python

   from core.undo_manager import UndoManager
   import numpy as np
   
   undo_mgr = UndoManager(max_history=50)
   
   # Push state
   state = {"grid": np.zeros((10, 10)), "generation": 0}
   undo_mgr.push_state(state, "Initial state")
   
   # Undo/redo
   previous_state = undo_mgr.undo()
   restored_state = undo_mgr.redo()
