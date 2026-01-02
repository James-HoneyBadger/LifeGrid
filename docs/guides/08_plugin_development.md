# Plugin Development Guide

## Overview

LifeGrid's plugin system allows you to extend functionality without modifying core code.

Plugins can:
- Add custom drawing tools
- Create new visualization modes
- Implement custom rules
- Add analysis tools
- Create new menu items
- Listen to simulation events

## Plugin Architecture

### Basic Plugin Structure

```python
from lifegrid.plugin_system import LifeGridPlugin
from typing import Any

class MyPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__(
            name="My Plugin",
            version="1.0.0",
            description="My plugin description"
        )
    
    def on_startup(self, app: Any) -> None:
        """Called when LifeGrid starts."""
        self.app = app
        print(f"{self.name} loaded!")
    
    def on_generation(self, stats: dict) -> None:
        """Called after each generation."""
        pass
    
    def on_shutdown(self) -> None:
        """Called when LifeGrid exits."""
        pass
    
    def get_menu_items(self) -> list:
        """Return menu items to add to LifeGrid."""
        return []
```

## Plugin Lifecycle

### 1. Initialization

```python
def __init__(self):
    super().__init__(
        name="Plugin Name",
        version="1.0.0",
        description="What it does"
    )
    # Initialize plugin state here
    self.enabled = True
```

### 2. Startup

```python
def on_startup(self, app):
    """Called when LifeGrid launches."""
    self.app = app  # Store reference to main app
    self.simulator = app.simulator
    self.ui = app.ui
    # Initialize UI elements
    # Register callbacks
```

### 3. Runtime

```python
def on_generation(self, stats):
    """Called after each simulation generation."""
    generation = stats['generation']
    population = stats['population']
    # Perform per-generation logic
```

### 4. Shutdown

```python
def on_shutdown(self):
    """Called when LifeGrid exits."""
    # Cleanup resources
    # Save state
    # Close files
```

## Creating Your First Plugin

### Step 1: Create Plugin File

Create `plugins/my_first_plugin.py`:

```python
from lifegrid.plugin_system import LifeGridPlugin

class FirstPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("My First Plugin", "1.0.0")
        self.generation_count = 0
    
    def on_startup(self, app):
        self.app = app
        print("✓ FirstPlugin loaded!")
    
    def on_generation(self, stats):
        self.generation_count += 1
        if self.generation_count % 10 == 0:
            print(f"10 generations completed, population: {stats['population']}")
```

### Step 2: Plugin Auto-loads

LifeGrid automatically discovers and loads plugins from the `plugins/` directory.

No additional configuration needed!

### Step 3: Test Your Plugin

```bash
python src/main.py
# Check console output for "✓ FirstPlugin loaded!"
```

## Adding Menu Items

### Simple Menu Action

```python
def get_menu_items(self):
    return [
        ("Tools", [
            ("My Plugin Action", self.on_my_action)
        ])
    ]

def on_my_action(self):
    print("User clicked my menu item!")
    # Perform action here
```

### Menu with Submenu

```python
def get_menu_items(self):
    return [
        ("My Plugin", [
            ("Action 1", self.action1),
            ("Action 2", self.action2),
            ("-", None),  # Separator
            ("Settings...", self.open_settings)
        ])
    ]

def action1(self):
    print("Action 1 triggered")

def action2(self):
    print("Action 2 triggered")

def open_settings(self):
    # Open settings dialog
    pass
```

## Accessing Simulator State

### Reading Grid State

```python
def on_generation(self, stats):
    # Get current grid
    grid = self.app.simulator.get_grid()
    
    # Analyze grid
    live_cells = grid.sum()
    dimensions = grid.shape
    
    print(f"Generation {stats['generation']}: {live_cells} cells alive")
```

### Modifying Grid

```python
def add_pattern(self, pattern_coords):
    """Add cells to grid."""
    sim = self.app.simulator
    
    for x, y in pattern_coords:
        sim.set_cell(x, y, 1)
    
    # Request UI redraw
    self.app.ui.request_update()
```

### Getting Statistics

```python
def on_generation(self, stats):
    # Available stats
    print(stats['generation'])      # Current generation
    print(stats['population'])      # Live cell count
    print(stats['births'])          # Cells born this gen
    print(stats['deaths'])          # Cells died this gen
    print(stats['density'])         # % of grid occupied
    print(stats['is_stable'])       # Pattern is stable?
```

## Example: Statistics Monitor Plugin

```python
from lifegrid.plugin_system import LifeGridPlugin
import csv
from datetime import datetime

class StatisticsMonitor(LifeGridPlugin):
    """Track and export simulation statistics."""
    
    def __init__(self):
        super().__init__(
            name="Statistics Monitor",
            version="1.0.0",
            description="Track population trends and export data"
        )
        self.stats_file = None
        self.writer = None
    
    def on_startup(self, app):
        self.app = app
        # Open stats file
        filename = f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.stats_file = open(filename, 'w', newline='')
        self.writer = csv.DictWriter(self.stats_file, 
            fieldnames=['generation', 'population', 'births', 'deaths'])
        self.writer.writeheader()
    
    def on_generation(self, stats):
        # Write statistics to file
        self.writer.writerow({
            'generation': stats['generation'],
            'population': stats['population'],
            'births': stats['births'],
            'deaths': stats['deaths']
        })
        self.stats_file.flush()
    
    def on_shutdown(self):
        if self.stats_file:
            self.stats_file.close()
            print("Statistics saved!")
    
    def get_menu_items(self):
        return [
            ("Tools", [
                ("Export Statistics", self.export_stats)
            ])
        ]
    
    def export_stats(self):
        print(f"Statistics exported to {self.stats_file.name}")
```

## Example: Custom Drawing Tool Plugin

```python
from lifegrid.plugin_system import LifeGridPlugin

class PatternStamperPlugin(LifeGridPlugin):
    """Add a stamp tool for placing patterns."""
    
    def __init__(self):
        super().__init__("Pattern Stamper", "1.0.0")
        self.pattern = None
    
    def on_startup(self, app):
        self.app = app
    
    def get_menu_items(self):
        return [
            ("Tools", [
                ("Define Stamp Pattern", self.define_pattern),
                ("Stamp Pattern (Click)", self.enable_stamp_mode)
            ])
        ]
    
    def define_pattern(self):
        """Let user select cells as pattern."""
        print("Draw pattern on grid, then select 'Save Stamp'")
        # Implementation: capture selected cells
    
    def enable_stamp_mode(self):
        """Enable clicking to place pattern."""
        print("Click on grid to place pattern")
        # Implementation: listen for clicks, place pattern at click location
```

## Event System

### Supported Events

```python
def on_startup(self, app):
    """Called once when app starts."""
    pass

def on_generation(self, stats):
    """Called after each generation step."""
    pass

def on_pattern_loaded(self, pattern):
    """Called when pattern is loaded."""
    pass

def on_pattern_saved(self, pattern):
    """Called when pattern is saved."""
    pass

def on_rule_changed(self, rule_name):
    """Called when rule is changed."""
    pass

def on_shutdown(self):
    """Called when app exits."""
    pass
```

## Plugin Configuration

### Storing Plugin Settings

```python
import json
import os

class ConfigurablePlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("Configurable Plugin", "1.0.0")
        self.config = self.load_config()
    
    def load_config(self):
        config_file = os.path.expanduser("~/.lifegrid/plugins/config.json")
        if os.path.exists(config_file):
            with open(config_file) as f:
                return json.load(f)
        return {"enabled": True, "options": {}}
    
    def save_config(self):
        config_file = os.path.expanduser("~/.lifegrid/plugins/config.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
```

## Error Handling

### Graceful Error Handling

```python
class RobustPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("Robust Plugin", "1.0.0")
    
    def on_generation(self, stats):
        try:
            # Risky operation
            grid = self.app.simulator.get_grid()
            result = grid[0, 0]
        except Exception as e:
            # Log error but don't crash
            print(f"Plugin error (non-fatal): {e}")
    
    def on_my_action(self):
        try:
            # Perform action
            pass
        except Exception as e:
            # Inform user
            self.app.ui.show_error(f"Plugin error: {e}")
```

## Testing Your Plugin

### Unit Test

```python
# test_my_plugin.py
from my_first_plugin import FirstPlugin

def test_plugin_init():
    plugin = FirstPlugin()
    assert plugin.name == "My First Plugin"
    assert plugin.version == "1.0.0"

def test_plugin_startup(mock_app):
    plugin = FirstPlugin()
    plugin.on_startup(mock_app)
    assert plugin.generation_count == 0

def test_plugin_generation():
    plugin = FirstPlugin()
    stats = {'generation': 1, 'population': 100}
    plugin.on_generation(stats)
    assert plugin.generation_count == 1
```

### Integration Test

```python
# Run with LifeGrid
python src/main.py
# Check console for plugin output
# Test menu items
# Run through simulation
```

## Distribution

### Packaging Your Plugin

```
my_plugin/
├── __init__.py
├── plugin.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Sharing Plugins

1. Create GitHub repository
2. Document usage in README
3. List in LifeGrid plugin registry (if available)
4. Users can install: `cp -r my_plugin ~/.lifegrid/plugins/`

## Advanced Topics

### Custom Drawing Tool

```python
class CustomToolPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("Custom Drawing Tool", "1.0.0")
    
    def on_startup(self, app):
        self.app = app
        # Register custom drawing tool
        self.app.register_drawing_tool(
            name="My Tool",
            handler=self.on_canvas_click
        )
    
    def on_canvas_click(self, x, y):
        """Handle canvas clicks in custom tool mode."""
        # Implement custom drawing logic
        pass
```

### Analysis Tools

```python
class AnalyzerPlugin(LifeGridPlugin):
    def __init__(self):
        super().__init__("Pattern Analyzer", "1.0.0")
    
    def on_generation(self, stats):
        grid = self.app.simulator.get_grid()
        
        # Analyze patterns
        oscillators = self.find_oscillators(grid)
        spaceships = self.find_spaceships(grid)
        
        if oscillators:
            print(f"Found {len(oscillators)} oscillators")
    
    def find_oscillators(self, grid):
        # Implementation here
        pass
    
    def find_spaceships(self, grid):
        # Implementation here
        pass
```

## Plugin Best Practices

1. **Keep it simple**: Do one thing well
2. **Fail gracefully**: Catch and handle errors
3. **Don't block UI**: Use threading for long operations
4. **Document**: Clear docstrings and README
5. **Test**: Unit and integration tests
6. **Version**: Follow semantic versioning
7. **Lazy load**: Initialize only what's needed
8. **Clean up**: Properly release resources

## API Reference Summary

### LifeGridPlugin Base Class

```python
class LifeGridPlugin:
    def __init__(self, name: str, version: str, description: str = "")
    def on_startup(self, app: Any) -> None
    def on_generation(self, stats: dict) -> None
    def on_shutdown(self) -> None
    def get_menu_items(self) -> list
```

### App Interface

```python
app.simulator          # Simulator instance
app.ui                 # UI controller
app.simulator.get_grid()
app.simulator.set_cell(x, y, value)
app.simulator.step()
app.ui.request_update()
app.ui.show_error(message)
```

## Getting Help

- Check examples in `plugins/` directory
- Review [Architecture Documentation](../architecture/)
- See [API Reference](../reference/)
- Create issue with code example

## Next Steps

- Look at [System Architecture](../architecture/system_architecture.md)
- Read [Advanced Features Guide](./03_advanced_features.md)
- Explore [API Reference](../reference/core_api.md)
