# System Architecture

## Overview

LifeGrid is built with a modular, layered architecture that separates concerns and allows independent evolution of components.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                  GUI Layer (Tkinter)                │
│         ┌─────────────────────────────────────┐     │
│         │  Main Window, Menus, Canvas, Controls   │
│         └─────────────────────────────────────┘     │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                 Application Layer                   │
│    ┌──────────────┐  ┌──────────────────────────┐  │
│    │ App Manager  │  │ Plugin System Interface  │  │
│    └──────────────┘  └──────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                   Core Layer                        │
│    ┌──────────────┐  ┌──────────────────────────┐  │
│    │  Simulator   │  │ Configuration Manager    │  │
│    │  Undo/Redo   │  │                          │  │
│    └──────────────┘  └──────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Automata Layer                         │
│    ┌──────────────┐  ┌──────────────────────────┐  │
│    │   Base CA    │  │  Specific Implementations│  │
│    │  (Abstract)  │  │ (Conway, HighLife, etc) │  │
│    └──────────────┘  └──────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│           Advanced Modules                          │
│    ┌────────────────────────────────────────────┐  │
│    │ Analysis, Visualization, Statistics, etc   │  │
│    └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. GUI Layer (`src/gui/`)

**Purpose**: User interface and visualization

**Key Components**:
- `app.py`: Main application window
- `ui.py`: UI components (buttons, menus)
- `rendering.py`: Canvas rendering engine
- `state.py`: UI state management

**Responsibilities**:
- Display grid
- Handle user input (mouse, keyboard)
- Render graphics
- Manage menu interactions
- Update UI state

**Dependencies**:
- Tkinter (display framework)
- NumPy (for grid data)

### 2. Core Layer (`src/core/`)

**Purpose**: Simulation engine and state management

**Key Components**:
- `simulator.py`: Main simulation orchestrator
- `config.py`: Configuration data structures
- `undo_manager.py`: History tracking

**Simulator Responsibilities**:
- Manages automaton instance
- Executes generation steps
- Tracks metrics (population, births, deaths)
- Provides grid access/modification
- Integrates undo/redo system

**Configuration**:
- Grid dimensions
- Default mode/rule
- Performance settings
- Undo history limit

**Undo Manager**:
- Stores state history
- Provides undo/redo operations
- Manages history depth

### 3. Automata Layer (`src/automata/`)

**Purpose**: Cellular automaton implementations

**Architecture**:
```
CellularAutomaton (ABC)
├── ConwaysLife
├── HighLife
├── Immigration
├── Rainbow
├── BriansBrain
├── Wireworld
├── LangtonsAnt
├── Generations (customizable)
└── LifeLike (custom B/S rules)
```

**Base Class**: `CellularAutomaton`
- Abstract interface
- Defines contract for implementations

**Implementation Pattern**:
```python
class RuleImplementation(CellularAutomaton):
    def __init__(self, width, height):
        # Initialize state
    
    def reset(self):
        # Clear grid
    
    def step(self):
        # Compute next generation
    
    def get_grid(self):
        # Return current state
```

**Computation**:
- Uses NumPy for fast grid operations
- Uses SciPy for convolutions (neighbor counting)
- Custom rules via birth/survival conditions

### 4. Advanced Layer (`src/advanced/`)

**Purpose**: Analysis and visualization tools

**Modules**:
- `pattern_analysis.py`: Oscillator/spaceship detection
- `rule_discovery.py`: Rule exploration utilities
- `visualization.py`: Image export and rendering
- `statistics.py`: Metric tracking and analysis
- `rle_format.py`: RLE file I/O

## Data Flow

### Simulation Loop

```
1. User clicks "Start"
   ├─ GUI → Simulator.start()
   
2. Each frame (at Speed frequency):
   ├─ Simulator.step()
   │  ├─ Automaton.step()
   │  │  ├─ Compute neighbors (SciPy)
   │  │  ├─ Apply rules
   │  │  └─ Update grid
   │  ├─ Track metrics
   │  └─ Push to UndoManager
   │
   ├─ Notify GUI
   │  ├─ Update canvas
   │  └─ Update statistics panel
   
3. User clicks "Stop"
   └─ Simulator.stop()
```

### Grid Representation

```
Grid (NumPy array)
  Type: uint8 (0-255 for multi-state)
  Shape: (width, height)
  Memory: width × height × 1 byte
  
Example (4×4 grid):
  [[0 1 0 1]
   [1 1 0 0]
   [0 0 1 1]
   [1 0 0 0]]
```

### Neighbor Calculation

Uses SciPy's `convolve2d` for efficiency:

```
Kernel:
  [[1 1 1]
   [1 0 1]
   [1 1 1]]

Operation: Convolve grid with kernel
Result: Each cell contains neighbor count (0-8)
```

## File Organization

```
LifeGrid/
├── src/
│   ├── gui/               # User interface
│   │   ├── app.py        # Main window
│   │   ├── ui.py         # UI components
│   │   ├── rendering.py  # Graphics
│   │   └── state.py      # State management
│   │
│   ├── core/             # Simulation engine
│   │   ├── simulator.py  # Main orchestrator
│   │   ├── config.py     # Configuration
│   │   └── undo_manager.py  # History
│   │
│   ├── automata/         # Automaton rules
│   │   ├── base.py       # Abstract base
│   │   ├── conway.py     # Conway's Life
│   │   ├── highlife.py   # HighLife variant
│   │   ├── immigration.py # Multi-color
│   │   ├── rainbow.py    # Color mixing
│   │   ├── ant.py        # Langton's Ant
│   │   ├── briansbrain.py # Three-state
│   │   ├── wireworld.py  # Logic circuits
│   │   ├── generations.py # Customizable
│   │   └── lifelike.py   # Custom B/S
│   │
│   ├── advanced/         # Advanced tools
│   │   ├── pattern_analysis.py
│   │   ├── rule_discovery.py
│   │   ├── visualization.py
│   │   ├── statistics.py
│   │   └── rle_format.py
│   │
│   ├── api/              # REST API (optional)
│   │   ├── app.py
│   │   └── routes.py
│   │
│   ├── plugin_system.py  # Plugin interface
│   ├── main.py           # Entry point
│   ├── export_manager.py # Export handler
│   ├── pattern_browser.py # Pattern library
│   ├── config_manager.py # Settings
│   └── version.py        # Version info
│
├── docs/                 # Documentation
├── tests/               # Test suite (deleted)
├── examples/            # Examples (partial)
└── plugins/             # Plugin directory
```

## Communication Patterns

### GUI ↔ Simulator

```python
# GUI starts simulation
self.simulator.start()

# Simulator calls callback each generation
self.simulator.set_on_step_callback(self.on_generation)

# GUI updates display
def on_generation(self, stats):
    population = stats['population']
    self.update_canvas()
```

### Plugin Integration

```python
# Plugins register with system
plugin.on_startup(app)

# App calls plugin hooks
plugin.on_generation(stats)

# Plugins interact with simulator
grid = app.simulator.get_grid()
```

### Configuration

```python
# Load configuration
config = SimulatorConfig.from_dict(settings)

# Create simulator with config
simulator = Simulator(config)

# Apply runtime changes
simulator.config.width = 200
simulator.reset()
```

## Extension Points

### Adding a New Automaton

1. Create class in `automata/` directory
2. Inherit from `CellularAutomaton`
3. Implement required methods
4. Register in mode selector
5. Add default patterns

```python
# Example: src/automata/custom.py
from .base import CellularAutomaton

class MyRule(CellularAutomaton):
    def __init__(self, width, height):
        super().__init__(width, height)
    
    def step(self):
        # Implement rule logic
        pass
```

### Creating a Plugin

1. Create class in `plugins/` directory
2. Inherit from `LifeGridPlugin`
3. Implement event hooks
4. Plugin auto-loads on startup

See [Plugin Development Guide](../guides/08_plugin_development.md).

### Custom Visualization

1. Add module to `advanced/visualization.py`
2. Access simulator via app interface
3. Generate visualization output

## Performance Considerations

### Bottlenecks

1. **Rendering** (usually): Display updates
2. **Computation** (sometimes): Generation calculation
3. **Memory** (rarely): Grid storage

### Optimization Strategies

- **NumPy/SciPy**: Already optimized for speed
- **Display caching**: Only update changed cells
- **History pruning**: Limit undo depth
- **Sparse representation**: Could optimize (future)

See [Performance Guide](../guides/07_performance.md) for details.

## Design Patterns Used

### Model-View-Separation

```
Model (Core):
├── Simulator
├── CellularAutomaton
└── Configuration

View (GUI):
├── Main Window
├── Canvas
└── UI Components

Controller:
└── Application (bridges Model and View)
```

### Strategy Pattern

CellularAutomaton implementations as strategies:
- Each rule is independent
- Easy to add new rules
- Runtime rule switching

### Observer Pattern

Plugin system observation:
- Plugins observe simulation events
- Simulator notifies on generation
- Decoupled architecture

### Singleton-ish

Simulator manages single grid state:
- Global access via app reference
- Prevents multiple instances
- Simplifies integration

## Dependencies

### Core Dependencies

- **NumPy**: Grid computation (required)
- **SciPy**: Fast convolutions (required)
- **Tkinter**: GUI (standard library, required)

### Optional Dependencies

- **Pillow**: PNG export
- **Matplotlib**: Advanced visualization
- **SciPy.signal**: Custom convolution kernels

### Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatting
- **pylint**: Code quality
- **mypy**: Type checking

## Future Architecture Improvements

### Planned

1. **GPU Acceleration**: CUDA/OpenCL for faster computation
2. **Web UI**: HTML/JavaScript interface
3. **Network Play**: Multi-user simulations
4. **Rule Presets**: Searchable database
5. **Advanced Analysis**: Machine learning integration

### Considered

1. **Event System**: More comprehensive event hooks
2. **Worker Threads**: Background computation
3. **Caching Layer**: Memoized patterns
4. **Rule Compilation**: JIT-compiled rules
5. **Distributed**: Cloud-based simulation

## Development Workflow

### Adding a Feature

1. **Design**: Update architecture doc
2. **Implement**: Create feature in appropriate layer
3. **Test**: Write unit tests
4. **Integrate**: Connect to GUI/API
5. **Document**: Add to user guides
6. **Optimize**: Profile and improve

### Code Organization Principles

- **Modularity**: Each component has single responsibility
- **Layering**: Clear dependency direction
- **Abstraction**: Hide implementation details
- **Testability**: Mockable dependencies
- **Extensibility**: Plugin/strategy patterns

## Conclusion

LifeGrid's architecture provides:

✓ Clear separation of concerns
✓ Easy to extend (new rules, plugins)
✓ Good performance
✓ Maintainable codebase
✓ Testable components

The modular design allows independent development of UI, core simulation, and advanced features while maintaining compatibility.

See [API Reference](../reference/) for detailed interface documentation.
