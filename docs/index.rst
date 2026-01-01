LifeGrid Documentation
======================

Welcome to LifeGrid's documentation! LifeGrid is a powerful and extensible cellular automaton simulator with support for multiple automaton types, pattern exploration, and advanced features.

.. image:: https://img.shields.io/badge/python-3.13+-blue.svg
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: License

Features
--------

* **Multiple Automata**: Conway's Game of Life, Brian's Brain, Wireworld, and more
* **GUI-Independent Core**: Use the simulator in scripts, notebooks, or headless environments
* **Pattern Library**: 40+ built-in patterns with searchable browser
* **Export Capabilities**: PNG snapshots, GIF animations, JSON patterns
* **Undo/Redo System**: Full state recovery with configurable history
* **Plugin Architecture**: Create custom automata without modifying core code
* **Theme Support**: Light and dark modes with customizable colors
* **Comprehensive Testing**: 136+ tests with 100% pass rate

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/James-HoneyBadger/LifeGrid.git
   cd LifeGrid
   pip install -r requirements.txt

Basic Usage
~~~~~~~~~~~

Run the GUI application:

.. code-block:: bash

   python src/main.py

Or use the core simulator in your code:

.. code-block:: python

   from core.simulator import Simulator
   
   sim = Simulator()
   sim.initialize("Conway's Game of Life")
   sim.step(100)
   print(sim.get_metrics_summary())

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   installation
   quickstart
   user_guide
   patterns
   export

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/core
   api/automata
   api/gui
   api/features

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide
   
   developer/architecture
   developer/plugins
   developer/contributing
   developer/testing

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources
   
   examples
   changelog
   license

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
