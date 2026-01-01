Installation Guide
==================

This guide covers different ways to install and set up LifeGrid.

Requirements
------------

* Python 3.13 or higher
* tkinter (usually included with Python)
* NumPy
* Pillow (optional, for export features)

From Source
-----------

1. **Clone the repository**

   .. code-block:: bash

      git clone https://github.com/James-HoneyBadger/LifeGrid.git
      cd LifeGrid

2. **Create a virtual environment** (recommended)

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

4. **Verify installation**

   .. code-block:: bash

      python -m pytest tests/

   You should see all tests passing.

Optional Dependencies
---------------------

For Export Features
~~~~~~~~~~~~~~~~~~~

To use PNG and GIF export functionality:

.. code-block:: bash

   pip install Pillow

For Development
~~~~~~~~~~~~~~~

To set up a development environment:

.. code-block:: bash

   pip install -r requirements.txt
   pip install pytest pytest-cov mypy sphinx sphinx-rtd-theme

Configuration
-------------

On first run, LifeGrid will create a default configuration file at:

* Linux/Mac: ``~/.lifegrid/config.json``
* Windows: ``%APPDATA%\lifegrid\config.json``

You can customize settings by editing this file or through the GUI.

Troubleshooting
---------------

tkinter Not Found
~~~~~~~~~~~~~~~~~

If you get an error about tkinter:

**On Ubuntu/Debian:**

.. code-block:: bash

   sudo apt-get install python3-tk

**On Fedora:**

.. code-block:: bash

   sudo dnf install python3-tkinter

**On macOS:**

tkinter should be included. If not, reinstall Python from python.org.

**On Windows:**

Reinstall Python and ensure "tcl/tk and IDLE" is checked during installation.

Import Errors
~~~~~~~~~~~~~

If you get import errors when running the application:

.. code-block:: bash

   # Make sure you're in the LifeGrid directory
   cd /path/to/LifeGrid
   
   # Run with Python module syntax
   python -m src.main

NumPy Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

On some systems, NumPy requires additional dependencies:

.. code-block:: bash

   # On Ubuntu/Debian
   sudo apt-get install python3-dev
   
   # Then retry
   pip install numpy

Verification
------------

To verify your installation is working correctly:

1. **Run the test suite:**

   .. code-block:: bash

      pytest tests/ -v

   All 136 tests should pass.

2. **Check module imports:**

   .. code-block:: python

      python -c "from src.core.simulator import Simulator; print('OK')"

3. **Launch the GUI:**

   .. code-block:: bash

      python src/main.py

   The application window should open without errors.

Next Steps
----------

* Read the :doc:`quickstart` guide
* Explore the :doc:`user_guide`
* Check out :doc:`examples` for code samples
