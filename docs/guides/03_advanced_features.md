# Advanced Features Guide

## Overview

This guide covers advanced features for power users and developers who want to maximize LifeGrid's capabilities.

## Undo/Redo System

LifeGrid maintains a complete history of all grid modifications.

### Using Undo/Redo

- **Undo**: Edit → Undo (Ctrl+Z) or `Backspace`
- **Redo**: Edit → Redo (Ctrl+Y) or `Ctrl+Shift+Z`
- History limit: Last 100 actions (configurable)

### History-based Exploration

1. Make a pattern modification
2. Run simulation
3. Use **Back** button to step backward
4. Undo back to original state with **Edit → Undo**
5. Try different patterns without reloading

## Pattern Analysis Tools

### Finding Oscillators

Oscillators are patterns that repeat after N generations.

1. Load a pattern or create one
2. Use **Tools → Analyze Pattern**
3. View oscillation period if detected

### Detecting Spaceships

Spaceships are moving patterns that repeat.

1. Enable **Tools → Detect Moving Patterns**
2. Run simulation (let it stabilize first)
3. Identified patterns are highlighted

### Statistical Analysis

**Tools → Statistics** provides:
- Population growth/decline trends
- Birth and death rates over time
- Stability metrics
- Periodicity analysis

## Custom Automata Rules

### Life-Like Rules (B/S Notation)

Specify birth and survival conditions:

**Format**: B*birth_digits*/S*survival_digits*

**Rules Table**:
| Rule | Name | Behavior |
|------|------|----------|
| B3/S23 | Conway's Life | Stable, complex |
| B36/S23 | HighLife | Includes replicators |
| B2/S | Seeds | Chaotic growth |
| B1357/S1357 | Replicator | Explosive patterns |
| B45/S345 | Assimilation | Smooth growth |

### Creating Custom Rules

1. **Settings → Custom Rules...**
2. Enter birth conditions (which cell counts create life)
3. Enter survival conditions (which counts keep cells alive)
4. Pattern updates immediately with new rules
5. Save frequently to avoid losing work

### Experimenting Systematically

```
Start with Conway's (B3/S23)
Vary birth conditions: B2/S23, B4/S23, etc.
Vary survival: B3/S2, B3/S4, etc.
Note interesting behaviors
Document discoveries
```

## Performance Optimization

### For Large Grids (1000+ cells)

1. **Reduce Display Size**:
   - Settings → Grid & View Settings
   - Lower "Cell Display Size" to 1-2 pixels
   - Improves rendering speed significantly

2. **Lower Update Frequency**:
   - Reduce Speed slider
   - Fewer updates per second = smoother responsiveness

3. **Use Efficient Patterns**:
   - Sparse patterns run faster
   - Dense grids with chaotic rules are slowest

### Memory Considerations

- Grid memory = width × height × 2 bytes (approximately)
- 2000×2000 grid ≈ 8 MB
- 5000×5000 grid ≈ 50 MB
- Most systems handle up to 10,000×10,000 efficiently

### Benchmarking

LifeGrid includes performance benchmarking:

```bash
python -m lifegrid.performance.benchmarking
```

Generates report showing:
- Generation times for different grid sizes
- Memory usage patterns
- Optimal settings for your hardware

## Pattern Library Management

### Organizing Patterns

Create a folder structure for patterns:

```
patterns/
├── conway/
│   ├── still_lifes/
│   ├── oscillators/
│   └── spaceships/
├── highlife/
│   └── replicators/
└── custom/
```

### Sharing Patterns

Patterns are stored as JSON with metadata:

```json
{
  "version": "3.0",
  "mode": "conway",
  "width": 100,
  "height": 100,
  "grid": [...],
  "metadata": {
    "name": "Glider",
    "period": 4,
    "tags": ["spaceship"]
  }
}
```

### Pattern Exchange Format (RLE)

RLE (Run Length Encoded) format is standard in cellular automata community:

```
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
```

LifeGrid can import/export RLE files for sharing with other simulators.

## Plugin Development

### Basic Plugin Structure

```python
from lifegrid.plugin_system import LifeGridPlugin

class MyPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("My Plugin", "1.0")
    
    def on_startup(self, app):
        """Called when LifeGrid starts"""
        pass
    
    def on_generation(self, stats):
        """Called each generation"""
        print(f"Generation {stats['generation']}")
    
    def get_menu_items(self):
        """Add menu items"""
        return [("My Tools", [("Action", self.my_action)])]
    
    def my_action(self):
        print("Plugin action executed")
```

### Installing Plugins

1. Create plugin in `plugins/` directory
2. Inherit from `LifeGridPlugin`
3. Plugin auto-loads on startup
4. Access app state via plugin interface

See [Plugin Development Guide](../guides/plugin_development.md) for details.

## API Integration

### Using LifeGrid as a Library

```python
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig

# Configure
config = SimulatorConfig(width=100, height=100, mode="conway")
sim = Simulator(config)

# Initialize and run
sim.initialize()
for _ in range(1000):
    sim.step()
    stats = sim.get_metrics_summary()
    print(f"Generation {stats['generation']}: {stats['population']} cells")

# Access grid
grid = sim.get_grid()
```

### Headless Operation

Run simulations without GUI:

```bash
python -c "
from lifegrid.core.simulator import Simulator

sim = Simulator()
sim.initialize(mode='conway')

for i in range(100):
    sim.step()

grid = sim.get_grid()
print(f'Final population: {grid.sum()}')
"
```

## Batch Processing

### Analyzing Multiple Patterns

```python
import glob
from lifegrid.core.simulator import Simulator

for pattern_file in glob.glob("patterns/*.json"):
    sim = Simulator()
    sim.initialize(pattern_file=pattern_file)
    
    # Run for 1000 generations
    for _ in range(1000):
        sim.step()
    
    stats = sim.get_metrics_summary()
    print(f"{pattern_file}: {stats['population']} cells, stable={stats['is_stable']}")
```

### Exporting Results

```python
# Export grid as PNG
from lifegrid.advanced.visualization import export_png
export_png(grid, "output.png", cell_size=2, show_grid=True)

# Export statistics
import csv
with open("stats.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=stats.keys())
    writer.writeheader()
    writer.writerow(stats)
```

## Advanced Visualization

### Heatmaps

Visualize cell lifespan or activity:

```python
from lifegrid.advanced.visualization import create_heatmap
heatmap = create_heatmap(sim, metric='lifespan')
heatmap.show()
```

### Population Graphs

Plot population trends:

```python
from lifegrid.advanced.statistics import plot_population_trend
sim.run(1000)
plot_population_trend(sim.get_history())
```

### Rule Space Exploration

Compare behaviors across rule variants:

```python
from lifegrid.advanced.rule_discovery import explore_rule_space

rules = ["B3/S23", "B36/S23", "B2/S", "B4/S34"]
for rule in rules:
    sim = Simulator()
    sim.set_rule(rule)
    sim.run(500)
    print(f"{rule}: stability={sim.is_stable()}")
```

## Troubleshooting Performance Issues

### Slow Rendering

- Reduce cell size
- Disable grid lines
- Reduce window size
- Check system resource usage

### Slow Simulation

- Reduce grid size
- Use sparser patterns
- Check if rule is inherently slow
- Profile with `cProfile`

### Memory Leaks

- Monitor memory usage
- Check for accumulated pattern history
- Clear unused undo history periodically
- Restart app if memory grows indefinitely

## Best Practices

1. **Save Frequently**: Use File → Save Pattern regularly
2. **Test Rules Carefully**: Some rules can crash with large grids
3. **Use Version Control**: Track pattern discoveries
4. **Document Discoveries**: Add metadata to interesting patterns
5. **Profile Before Optimizing**: Measure to find real bottlenecks
6. **Use Appropriate Grid Size**: Balance detail vs. performance

## Next Steps

- Read [Plugin Development Guide](../guides/plugin_development.md)
- Try [API Examples](../reference/api_examples.md)
- Explore [Architecture Documentation](../architecture/)
