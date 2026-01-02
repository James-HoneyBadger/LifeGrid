# Core API Reference

## Simulator Class

The main interface for cellular automaton simulation.

### Constructor

```python
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig

# With default config
sim = Simulator()

# With custom config
config = SimulatorConfig(width=512, height=512)
sim = Simulator(config)
```

### Initialization

```python
def initialize(self, mode: str = None, pattern: str = None) -> None:
    """Initialize the simulator with specified mode and pattern.
    
    Args:
        mode: Automaton mode (e.g., 'conway', 'highlife', 'custom')
        pattern: Pattern name (e.g., 'glider', 'random_soup')
    """
    sim.initialize(mode='conway', pattern='glider')
```

### Basic Operations

```python
# Execute one generation
sim.step()

# Execute multiple generations
for _ in range(100):
    sim.step()

# Reset to initial state
sim.reset()

# Clear all cells
sim.reset()  # Then set_cell calls as needed
```

### Grid Access

```python
# Get current grid state
grid = sim.get_grid()  # Returns NumPy array

# Set individual cell
sim.set_cell(x=10, y=20, value=1)

# Toggle cell
sim.set_cell(50, 50, 1 - sim.get_grid()[50, 50])

# Access cell value
is_alive = sim.get_grid()[x, y] > 0

# Get grid properties
width, height = sim.config.width, sim.config.height
```

### Metrics and Statistics

```python
# Get current metrics
metrics = sim.step()  # Returns list of stats dicts
# Each dict contains:
# - 'generation': Current step number
# - 'population': Live cell count
# - 'births': Cells born this generation
# - 'deaths': Cells died this generation
# - 'density': Percentage of grid alive

# Get summary
summary = sim.get_metrics_summary()
print(f"Population: {summary['population']}")
print(f"Generation: {summary['generation']}")

# Check if stable
is_stable = summary.get('is_stable', False)
```

### History Management (Undo/Redo)

```python
# Undo previous state
success = sim.undo()

# Redo previous undo
success = sim.redo()

# Check ability
can_undo = sim.undo_manager.can_undo()
can_redo = sim.undo_manager.can_redo()

# Clear history (frees memory)
sim.undo_manager.clear()
```

### Event Handling

```python
# Register callback for each generation
def on_generation(stats):
    print(f"Generation {stats['generation']}: {stats['population']} cells")

sim.set_on_step_callback(on_generation)

# Callback is invoked after each step()
sim.step()  # Calls on_generation
```

## Configuration Class

Manages simulator settings.

### Constructor

```python
from lifegrid.core.config import SimulatorConfig

# Default configuration
config = SimulatorConfig()

# Custom values
config = SimulatorConfig(
    width=512,
    height=512,
    mode='conway',
    seed=42,
    undo_history_limit=100
)
```

### Attributes

```python
config.width: int              # Grid width in cells
config.height: int             # Grid height in cells
config.mode: str               # Default automaton mode
config.seed: int               # Random seed for reproducibility
config.undo_history_limit: int # Max undo steps

# Modification
config.width = 256
config.height = 256

# Reset to defaults
config = SimulatorConfig()
```

### Serialization

```python
# Convert to dictionary
config_dict = config.to_dict()
# Returns: {
#   'width': 512,
#   'height': 512,
#   'mode': 'conway',
#   ...
# }

# Load from dictionary
settings = {'width': 256, 'height': 256}
config = SimulatorConfig.from_dict(settings)
```

## UndoManager Class

Manages undo/redo history.

### Basic Operations

```python
from lifegrid.core.undo_manager import UndoManager

manager = UndoManager(max_history=100)

# Save state
manager.push_state('Draw cells', grid_state)
manager.push_state('Run simulation', new_grid_state)

# Undo
action_name, state = manager.undo()
# Returns: ('Run simulation', previous_grid)

# Redo
action_name, state = manager.redo()
# Returns: ('Run simulation', later_grid)
```

### History Queries

```python
# Check if undo available
if manager.can_undo():
    manager.undo()

# Check if redo available
if manager.can_redo():
    manager.redo()

# Get history summary
summary = manager.get_history_summary()
# Returns: {
#   'history_length': 50,
#   'redo_length': 10,
#   'entries': [...]
# }

# Clear history
manager.clear()  # Frees memory
```

## Automaton Interface

All cellular automaton implementations inherit from `CellularAutomaton`.

### Basic Interface

```python
from lifegrid.automata.base import CellularAutomaton

class MyAutomaton(CellularAutomaton):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        # Initialize state
    
    def reset(self) -> None:
        """Clear all cells."""
        pass
    
    def step(self) -> None:
        """Compute next generation."""
        pass
    
    def get_grid(self) -> np.ndarray:
        """Return current grid state."""
        pass
    
    def handle_click(self, x: int, y: int) -> None:
        """Handle mouse click (optional)."""
        pass
```

### Available Implementations

#### Conway's Life

```python
from lifegrid.automata.conway import ConwaysLife

ca = ConwaysLife(width=512, height=512)
ca.load_pattern('glider')
ca.step()
grid = ca.get_grid()
```

#### HighLife

```python
from lifegrid.automata.highlife import HighLife

ca = HighLife(width=512, height=512)
ca.load_pattern('replicator')
ca.step()
```

#### Custom Rules (Generations)

```python
from lifegrid.automata.generations import GenerationsAutomaton

ca = GenerationsAutomaton(
    width=512,
    height=512,
    birth_conditions=[3],
    survival_conditions=[2, 3],
    num_states=2
)
ca.step()
```

#### Custom B/S Rules

```python
from lifegrid.automata.lifelike import LifeLike

# B3/S23 (Conway's variant)
ca = LifeLike(width=512, height=512)
ca.set_rules(birth=[3], survival=[2, 3])
ca.step()

# B36/S23 (HighLife)
ca.set_rules(birth=[3, 6], survival=[2, 3])
ca.step()
```

## Complete Example

### Basic Simulation

```python
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig

# Configure
config = SimulatorConfig(width=256, height=256)
sim = Simulator(config)

# Initialize
sim.initialize(mode='conway', pattern='glider')

# Run simulation
for generation in range(100):
    stats = sim.step()
    
    if generation % 10 == 0:
        print(f"Gen {stats[0]['generation']}: {stats[0]['population']} cells")

# Get final state
grid = sim.get_grid()
print(f"Final population: {grid.sum()}")
```

### Pattern Analysis

```python
from lifegrid.core.simulator import Simulator

sim = Simulator()
sim.initialize(mode='conway')

# Run until stable
for _ in range(1000):
    sim.step()

# Analyze
grid = sim.get_grid()
metrics = sim.get_metrics_summary()

print(f"Stable: {metrics.get('is_stable', False)}")
print(f"Population: {metrics['population']}")
print(f"Generation: {metrics['generation']}")
```

### Custom Rule Testing

```python
from lifegrid.core.simulator import Simulator

# Test multiple rules
rules = [
    ('B3/S23', 'Conway'),
    ('B36/S23', 'HighLife'),
    ('B4/S34', 'Assimilation')
]

for rule_notation, name in rules:
    sim = Simulator()
    sim.initialize(mode='custom')
    sim.set_custom_rule(rule_notation)
    
    # Run random soup test
    for _ in range(100):
        sim.step()
    
    metrics = sim.get_metrics_summary()
    print(f"{name}: Final population = {metrics['population']}")
```

### Grid Manipulation

```python
from lifegrid.core.simulator import Simulator
import numpy as np

sim = Simulator()
sim.initialize()

# Draw a pattern
sim.set_cell(50, 50, 1)
sim.set_cell(51, 50, 1)
sim.set_cell(52, 50, 1)

# Run
for _ in range(4):
    sim.step()

# Analyze result
grid = sim.get_grid()
live_cells = np.argwhere(grid > 0)  # Get coordinates
print(f"Live cells at: {live_cells}")
```

## API Patterns

### Callback Pattern

```python
def handle_generation(stats):
    generation = stats['generation']
    population = stats['population']
    # React to generation event
    if population == 0:
        print("Pattern died!")

sim.set_on_step_callback(handle_generation)

# Callback invoked each step
for _ in range(100):
    sim.step()
```

### Context Manager Pattern

```python
# Save state
original_grid = sim.get_grid().copy()

try:
    # Experiment
    for _ in range(100):
        sim.step()
except Exception as e:
    # Restore on error
    sim.reset()
    # Set back to original...
```

### Generator Pattern

```python
def simulate_generations(count):
    """Generator yielding each generation."""
    for _ in range(count):
        stats = sim.step()
        yield stats

for stats in simulate_generations(1000):
    if stats['population'] == 0:
        print(f"Died at generation {stats['generation']}")
        break
```

## Error Handling

### Exception Types

```python
# Invalid grid size
try:
    sim = Simulator(SimulatorConfig(width=0, height=0))
except ValueError as e:
    print(f"Invalid size: {e}")

# Invalid mode
try:
    sim.initialize(mode='nonexistent')
except ValueError as e:
    print(f"Invalid mode: {e}")

# Invalid coordinates
try:
    sim.set_cell(-1, -1, 1)
except IndexError as e:
    print(f"Out of bounds: {e}")
```

### Safe Operations

```python
# Safe check before operation
if (0 <= x < sim.config.width and 
    0 <= y < sim.config.height):
    sim.set_cell(x, y, 1)

# Safe undo
if sim.undo_manager.can_undo():
    sim.undo()
```

## Type Hints

LifeGrid uses Python type hints throughout:

```python
from typing import Optional, Dict, List
import numpy as np

def initialize(self, 
               mode: Optional[str] = None,
               pattern: Optional[str] = None) -> None:
    pass

def set_cell(self, x: int, y: int, 
             value: int = 1) -> None:
    pass

def get_grid(self) -> np.ndarray:
    pass

def get_metrics_summary(self) -> Dict[str, any]:
    pass
```

## Performance Considerations

### Grid Operations

```python
# Fast: NumPy array access
grid = sim.get_grid()
value = grid[x, y]

# Slower: repeated get_grid() calls
for _ in range(100):
    grid = sim.get_grid()  # Re-fetches each time

# Better: cache grid reference
grid = sim.get_grid()
for _ in range(100):
    # Work with cached grid
```

### Memory Usage

```python
# Monitor memory
import sys
grid = sim.get_grid()
memory_bytes = sys.getsizeof(grid)

# Large grids use significant memory
# 5000×5000 grid ≈ 50 MB
```

### Callback Performance

```python
# Keep callbacks fast
def quick_callback(stats):
    """Keep processing minimal."""
    if stats['generation'] % 10 == 0:
        # Only process every 10 generations
        process_data(stats)

# Slow callbacks block simulation
def slow_callback(stats):
    analyze_entire_grid()  # Too slow!
    export_png()  # Too slow!
```

## Advanced Usage

### Extending Simulator

```python
class MySimulator(Simulator):
    def step(self):
        super().step()
        # Custom processing after each step
        self.custom_analysis()
```

### Custom Automaton

```python
from lifegrid.automata.base import CellularAutomaton

class MyRule(CellularAutomaton):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.grid = np.zeros((width, height), dtype=np.uint8)
    
    def step(self):
        # Custom rule implementation
        new_grid = np.zeros_like(self.grid)
        # ... rule logic ...
        self.grid = new_grid
```

## Next Steps

- See [Automata API Reference](./automata_api.md) for cellular automaton details
- Read [GUI API Reference](./gui_api.md) for UI integration
- Check [Advanced Modules](./advanced_api.md) for analysis tools
- Review [Architecture Documentation](../architecture/) for system design
