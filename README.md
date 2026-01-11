# LifeGrid

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.0.0-green.svg)](https://github.com/James-HoneyBadger/LifeGrid)

**LifeGrid** is an extensible cellular automaton simulator featuring a graphical user interface, robust pattern management, and a plugin system. Built with Python and Tkinter, it offers a rich environment for exploring Conway's Game of Life and many other automata variations.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## About

LifeGrid provides a powerful platform for simulating, analyzing, and visualizing cellular automata. Whether you are a student exploring emergence, a researcher testing new rules, or a hobbyist creating intricate patterns, LifeGrid offers the tools you need.

## Features

- **Multiple Automata Modes**: 
  - Conway's Game of Life
  - HighLife
  - Immigration Game
  - Rainbow Game
  - Brian's Brain
  - Wireworld
  - Langton's Ant
  - Custom Rule Support (B/S notation)
- **Interactive GUI**:
  - Drawing tools (Pen, Eraser, Toggle)
  - Symmetry modes (Horizontal, Vertical, Diagonal, Point)
  - Zoom and Pan controls
  - Real-time speed adjustment
- **Pattern Management**:
  - Built-in library of diverse patterns
  - Load/Save functionality (supports RLE and JSON)
  - Pattern Browser with previews
- **Advanced Capabilities**:
  - Undo/Redo history
  - Statistics tracking (Population, Density, Births/Deaths)
  - Export to Image (PNG) or Animation (GIF)
  - Plugin system for extensions

## Installation

### Prerequisites

- Python 3.11 or higher
- Git (optional, for cloning)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/James-HoneyBadger/LifeGrid.git
   cd LifeGrid
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Running the GUI Application

To launch the main simulator interface:

```bash
python src/main.py
```

### Using as a Library

LifeGrid's core can be used in your own scripts for headless simulation:

```python
from src.core.simulator import Simulator
from src.core.config import SimulatorConfig

# Initialize simulator
config = SimulatorConfig(width=100, height=100)
sim = Simulator(config)

# Setup a pattern (e.g., a Glider)
sim.initialize(mode='conway', pattern='glider')

# Run for 100 generations
for _ in range(100):
    stats = sim.step()
    print(f"Gen {stats[0]['generation']}: Pop {stats[0]['population']}")
```

## Documentation

Full documentation is available in the `docs/` directory.

- **[User Guide](docs/guides/02_user_guide.md)**: Detailed instructions on using the GUI and features.
- **[Installation Guide](docs/guides/01_installation.md)**: Comprehensive installation options.
- **[API Reference](docs/reference/01_core_api.md)**: Technical specifics for developers.
- **[Pattern Formats](docs/guides/04_file_formats.md)**: Understanding supported file types.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Honey Badger Universe
