# LifeGrid Examples

This directory contains example scripts, patterns, and usage examples for LifeGrid.

## Directory Structure

```
examples/
├── scripts/          # Python example scripts
│   ├── basic_simulator.py     # Basic simulator usage
│   ├── pattern_explorer.py    # Pattern browsing
│   ├── export_example.py      # Export PNG/GIF/JSON
│   ├── custom_plugin.py       # Create custom automata
│   └── undo_redo_example.py   # Undo/redo functionality
├── output/           # Generated exports (created automatically)
└── README.md         # This file
```

## Running the Examples

All examples are designed to be run from the examples/scripts directory:

```bash
cd examples/scripts
python basic_simulator.py
```

Or from the project root:

```bash
python examples/scripts/basic_simulator.py
```

## Example Scripts

### 1. Basic Simulator (`basic_simulator.py`)

Demonstrates fundamental simulator usage:
- Creating a simulator instance
- Initializing with a pattern
- Running simulations
- Collecting metrics

**Run:**
```bash
python examples/scripts/basic_simulator.py
```

**Concepts covered:**
- Simulator initialization
- Pattern loading
- Step execution
- Metrics retrieval

### 2. Pattern Explorer (`pattern_explorer.py`)

Shows how to use the pattern browser:
- Searching patterns by name
- Getting pattern statistics
- Listing all patterns
- Simulating discovered patterns

**Run:**
```bash
python examples/scripts/pattern_explorer.py
```

**Concepts covered:**
- PatternBrowser API
- Pattern search
- Pattern metadata
- Pattern simulation

### 3. Export Example (`export_example.py`)

Demonstrates export functionality:
- PNG snapshot export
- GIF animation export
- JSON pattern export
- Theme-aware rendering

**Run:**
```bash
python examples/scripts/export_example.py
```

**Output:** Creates files in `examples/output/`:
- `glider_initial.png` - Initial state snapshot
- `glider_animation.gif` - 50-frame animation
- `glider_pattern.json` - Pattern with metadata
- `glider_light.png` - Light theme snapshot

**Requirements:** Install Pillow for image export:
```bash
pip install Pillow
```

**Concepts covered:**
- ExportManager usage
- Multiple format export
- Theme customization
- Frame collection

### 4. Custom Plugin (`custom_plugin.py`)

Shows how to create custom cellular automata:
- Defining plugin classes
- Implementing step logic
- Registering plugins
- Using custom automata

**Run:**
```bash
python examples/scripts/custom_plugin.py
```

**Plugins demonstrated:**
- **InvertAutomaton** - Inverts all cells each step
- **MajorityRuleAutomaton** - Cells adopt majority neighbor state
- **RandomWalkAutomaton** - Living cells randomly walk

**Concepts covered:**
- AutomatonPlugin interface
- Plugin registration
- Custom rule implementation
- PluginManager usage

### 5. Undo/Redo Example (`undo_redo_example.py`)

Demonstrates state management:
- Running simulations
- Undoing steps
- Redoing steps
- History inspection

**Run:**
```bash
python examples/scripts/undo_redo_example.py
```

**Concepts covered:**
- Undo/redo operations
- State history
- History navigation
- Can-undo/can-redo checks

## Code Snippets

### Minimal Simulator

```python
from src.core.simulator import Simulator

sim = Simulator()
sim.initialize("Conway's Game of Life", "Glider")
sim.step(100)
print(f"Generation {sim.generation}: {sim.population} cells")
```

### Pattern Search

```python
from src.pattern_browser import PatternBrowser

browser = PatternBrowser()
gliders = browser.search_patterns("glider")
for pattern in gliders:
    print(pattern['name'])
```

### Quick Export

```python
from src.export_manager import ExportManager

export = ExportManager(theme="dark")
export.export_png(grid, "output.png", cell_size=4)
```

### Custom Automaton

```python
from src.plugin_system import AutomatonPlugin
import numpy as np

class MyAutomaton(AutomatonPlugin):
    def __init__(self):
        super().__init__("My Rule", "My description")
    
    def step(self, grid: np.ndarray) -> np.ndarray:
        # Your logic here
        return modified_grid
```

## Additional Resources

- **Full Documentation:** See `docs/` directory
- **Quick Reference:** See `QUICK_REFERENCE.md`
- **API Documentation:** Build with `cd docs && make html`
- **Contributing Guide:** See `CONTRIBUTING.md`

## Questions?

- Check the main [README.md](../README.md)
- Read [QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
- See full [documentation](../docs/)
- Open an issue on GitHub

---

Happy coding with LifeGrid! 🎮
