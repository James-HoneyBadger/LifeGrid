Automata API
============

This module contains implementations of various cellular automata types.

Base Automaton
--------------

.. automodule:: automata.base
   :members:
   :undoc-members:
   :show-inheritance:

All automata inherit from the BaseAutomaton abstract class.

Conway's Game of Life
---------------------

.. automodule:: automata.conway
   :members:
   :undoc-members:
   :show-inheritance:

The classic cellular automaton with rules B3/S23.

**Example:**

.. code-block:: python

   from automata.conway import ConwayAutomaton
   import numpy as np
   
   ca = ConwayAutomaton(width=50, height=50)
   grid = np.random.randint(0, 2, (50, 50))
   next_grid = ca.step(grid)

Brian's Brain
-------------

.. automodule:: automata.briansbrain
   :members:
   :undoc-members:
   :show-inheritance:

A three-state automaton with interesting oscillator patterns.

Wireworld
---------

.. automodule:: automata.wireworld
   :members:
   :undoc-members:
   :show-inheritance:

A cellular automaton designed to simulate electronic circuits.

HighLife
--------

.. automodule:: automata.highlife
   :members:
   :undoc-members:
   :show-inheritance:

Similar to Conway's Game of Life but with B36/S23 rules.

Langton's Ant
-------------

.. automodule:: automata.ant
   :members:
   :undoc-members:
   :show-inheritance:

A two-dimensional Turing machine with simple rules.

Immigration
-----------

.. automodule:: automata.immigration
   :members:
   :undoc-members:
   :show-inheritance:

A variant of Life where there are two types of living cells.

Rainbow
-------

.. automodule:: automata.rainbow
   :members:
   :undoc-members:
   :show-inheritance:

A colorful multi-state cellular automaton.

Generations
-----------

.. automodule:: automata.generations
   :members:
   :undoc-members:
   :show-inheritance:

A family of automata where cells gradually die over multiple generations.

Life-like Automata
------------------

.. automodule:: automata.lifelike
   :members:
   :undoc-members:
   :show-inheritance:

Customizable automata with configurable birth/survival rules.

**Example:**

.. code-block:: python

   from automata.lifelike import LifeLikeAutomaton
   
   # Create custom rules (e.g., HighLife)
   ca = LifeLikeAutomaton(
       width=50,
       height=50,
       birth_rule={3, 6},
       survival_rule={2, 3}
   )
