## LifeGrid Enhancement Quick Reference

Fast lookup guide for new modules and features added in Phases 1-4.

---

## 📦 New Modules

### Core Simulator (`src/core/`)
| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `simulator.py` | Main simulation engine | `Simulator` |
| `config.py` | Simulation configuration | `SimulatorConfig` |
| `undo_manager.py` | Undo/redo history | `UndoManager` |
| `__init__.py` | Package exports | - |

### Application (`src/`)
| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `config_manager.py` | App configuration | `AppConfig` |
| `export_manager.py` | Export functionality | `ExportManager` |
| `pattern_browser.py` | Pattern discovery | `PatternBrowser` |
| `plugin_system.py` | Plugin architecture | `PluginManager`, `AutomatonPlugin` |
| `ui_enhancements.py` | UI improvements | `ThemeManager`, `KeyboardShortcuts`, `Tooltips`, `SpeedPresets` |

### Tests (`tests/`)
| File | Tests | Coverage |
|------|-------|----------|
| `test_automata.py` | 27 | All automata types & patterns |
| `test_state.py` | 8 | State management |
| `test_fileio.py` | 11 | File I/O & patterns |
| `test_core.py` | 22 | Simulator & config |
| `test_config.py` | 14 | Config & plugins |
| `test_phase3.py` | 24 | Export & pattern browser |
| `test_ui_enhancements.py` | 27 | UI features |

---

## 🚀 Quick Start

### Initialize Simulator
```python
from core.simulator import Simulator
from core.config import SimulatorConfig

config = SimulatorConfig(width=100, height=100, speed=50)
sim = Simulator(config)
sim.initialize("Conway's Game of Life", "Glider Gun")
sim.step(5)
print(sim.get_metrics_summary())
```

### Export Simulation
```python
from export_manager import ExportManager

export = ExportManager(theme="dark")
grid = sim.get_grid()
export.export_png(grid, "output.png", cell_size=8)
```

### Browse Patterns
```python
from pattern_browser import PatternBrowser

browser = PatternBrowser()
results = browser.search_patterns("glider")
for mode, patterns in results.items():
    for pattern in patterns:
        info = browser.get_pattern_info(mode, pattern)
        print(f"{pattern}: {info['description']}")
```

### Manage Themes
```python
from ui_enhancements import ThemeManager

theme = ThemeManager()
theme.set_theme("dark")
colors = theme.get_colors()
```

### Create Plugin
```python
from plugin_system import AutomatonPlugin
from automata import CellularAutomaton

class MyCustomAutomaton(AutomatonPlugin):
    @property
    def name(self) -> str:
        return "MyRule"
    
    @property
    def description(self) -> str:
        return "Custom automaton rule"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def create_automaton(self, width: int, height: int) -> CellularAutomaton:
        # Return automaton instance
        pass
```

---

## 🔧 Configuration

### SimulatorConfig
```python
config = SimulatorConfig(
    width=100,
    height=100,
    speed=50,
    cell_size=8,
    automaton_mode="Conway's Game of Life",
    birth_rule={3},
    survival_rule={2, 3}
)
```

### AppConfig
```python
app_config = AppConfig(
    window_width=1200,
    window_height=800,
    theme="dark",
    enable_animations=True,
    export_format="png"
)
app_config.save("settings.json")
```

---

## 🎨 UI Features

### Themes
Available themes: `light`, `dark`
```python
from ui_enhancements import ThemeManager
theme = ThemeManager("dark")
bg_color = theme.get_color("bg")
```

### Speed Presets
Available: `slow` (20), `normal` (50), `fast` (100), `very_fast` (150)
```python
from ui_enhancements import SpeedPresets
speed = SpeedPresets.get_preset("fast")
```

### Keyboard Shortcuts
Default shortcuts:
- Space: play/pause
- S: step forward
- Left: step backward
- C: clear
- G: toggle grid
- Ctrl+O: open
- Ctrl+S: save
- Ctrl+E: export
- Ctrl+Z: undo
- Ctrl+Y: redo

### Tooltips
```python
from ui_enhancements import Tooltips
help_text = Tooltips.get_tooltip("start_button")
```

---

## 📊 Export Features

### PNG Export
```python
export.export_png(grid, "snapshot.png", cell_size=8)
```

### GIF Export
```python
export.add_frame(grid1)
export.add_frame(grid2)
export.add_frame(grid3)
export.export_gif("animation.gif", duration=100, loop=0)
```

### JSON Export
```python
export.export_json("pattern.json", grid, metadata={
    "generation": 100,
    "population": 50,
    "mode": "Conway's Game of Life"
})
```

---

## 🔍 Pattern Browser Features

### Search
```python
browser = PatternBrowser()
results = browser.search_patterns("gun")  # By name
results = browser.get_patterns_by_description("oscillator")  # By description
```

### Info
```python
info = browser.get_pattern_info("Conway's Game of Life", "Glider Gun")
# Returns: {name, mode, description, cell_count, coordinates}
```

### Statistics
```python
stats = browser.get_statistics()
# Returns: {total_modes, total_patterns, patterns_per_mode}
```

---

## ↩️ Undo/Redo

### Basic Usage
```python
manager = UndoManager(max_history=100)
manager.push_state("Step 1", grid)
manager.push_state("Step 2", grid)

if manager.can_undo():
    name, state = manager.undo()
```

### History Info
```python
summary = manager.get_history_summary()
# Returns: {undo_count, redo_count, last_undo_action, last_redo_action}
```

---

## 🧩 Plugin System

### Register Plugin
```python
from plugin_system import PluginManager

manager = PluginManager()
manager.register_plugin(my_plugin_instance)
```

### Load from Directory
```python
count = manager.load_plugins_from_directory("./plugins/")
print(f"Loaded {count} plugins")
```

### Create Automaton
```python
automaton = manager.create_automaton("CustomRule", 100, 100)
```

### List Plugins
```python
for name in manager.list_plugins():
    plugin = manager.get_plugin(name)
    print(f"{plugin.name} v{plugin.version}: {plugin.description}")
```

---

## 📈 Metrics & Statistics

### Get Metrics
```python
sim.step(10)
summary = sim.get_metrics_summary()
# Returns: {generations, current_population, max_population, avg_density, ...}
```

### Export Metrics
```python
from gui.state import SimulationState

state = SimulationState()
state.add_metric(generation=1, population=50, peak=100, density=0.1)
csv_data = state.export_metrics_csv()
with open("metrics.csv", "w") as f:
    f.write(csv_data)
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_core.py -v
```

### Run Single Test
```bash
pytest tests/test_core.py::TestSimulator::test_initialize_conway -v
```

### Test Coverage
```bash
pytest tests/ --cov=src
```

---

## 📚 Module Dependencies

```
core/
├── simulator ─── config, undo_manager, automata
├── config ────── dataclasses
└── undo_manager ── numpy

export_manager ──── PIL/Pillow, numpy
pattern_browser ─── patterns
plugin_system ───── automata, importlib
ui_enhancements ── (none)
config_manager ──── dataclasses, json
```

---

## 💡 Common Patterns

### Persistent Configuration
```python
config = AppConfig.load("settings.json")
# ... modify config ...
config.save("settings.json")
```

### Custom Theme
```python
theme = ThemeManager("light")
# Access colors
grid_color = theme.get_color("grid_line")
alive_color = theme.get_color("cell_alive")
```

### Pattern Discovery Workflow
```python
browser = PatternBrowser()
for mode in browser.get_modes():
    for pattern in browser.get_patterns(mode):
        info = browser.get_pattern_info(mode, pattern)
        if "oscillator" in info["description"]:
            print(f"Found oscillator: {pattern}")
```

### Full Simulation Workflow
```python
config = SimulatorConfig()
sim = Simulator(config)
sim.initialize("Conway's Game of Life")

for gen in range(100):
    sim.step(1)
    metrics = sim.get_metrics_summary()
    if metrics["current_population"] == 0:
        break

export = ExportManager()
export.export_json("final_state.json", sim.get_grid(), 
                  metadata={"generations": gen})
```

---

## 🐛 Debugging

### Check Plugin Status
```python
manager = PluginManager()
print(f"Loaded plugins: {manager.list_plugins()}")
for name in manager.list_plugins():
    plugin = manager.get_plugin(name)
    print(f"  {name}: {plugin.version}")
```

### Inspect Configuration
```python
config = SimulatorConfig()
print(config.to_dict())
```

### Monitor Metrics
```python
metrics = sim.get_metrics_summary()
for key, value in metrics.items():
    print(f"{key}: {value}")
```

---

## 📖 Documentation

- **Full Summary:** See `ENHANCEMENT_SUMMARY.md`
- **Test Examples:** See `tests/` directory
- **API Docstrings:** Each module has Google-style docstrings
- **Code Comments:** Complex logic is well-commented

---

## ✅ Compatibility

- **Python:** 3.13+
- **Dependencies:** numpy, scipy, Pillow (optional)
- **Operating Systems:** Linux, macOS, Windows
- **GUI:** Tkinter (unchanged)

---

**Last Updated:** Phase 4 Complete (136 tests passing)
