# FAQ - Frequently Asked Questions

## Getting Started

### Q: How do I install LifeGrid?

A: See the [Installation Guide](./01_installation.md). Quick version:

```bash
git clone https://github.com/James-HoneyBadger/LifeGrid.git
cd LifeGrid
pip install -r requirements.txt
python src/main.py
```

### Q: What are the system requirements?

A: Python 3.11+, Tkinter, NumPy 1.24+, SciPy 1.11+. Pillow 10+ is optional for PNG export. See [Installation Guide](./01_installation.md#system-requirements) for details.

### Q: Can I run LifeGrid on Windows/macOS/Linux?

A: Yes! LifeGrid is cross-platform and runs on all three. Some dependency installation steps differ slightly. See [Installation Guide](./01_installation.md) for OS-specific instructions.

## Usage Questions

### Q: How do I start a simulation?

A: 
1. Select an automaton mode from the **Mode** dropdown
2. Choose a **Pattern** or draw on the canvas
3. Click **Start** (or press `Space`)

### Q: What's the difference between the drawing modes?

A:
- **Toggle**: Click to flip individual cells on/off
- **Pen**: Click and drag to draw continuous patterns
- **Eraser**: Click and drag to erase cells

### Q: How do I save my patterns?

A: Use **File → Save Pattern...** to save as JSON. This preserves all settings and can be loaded later.

### Q: Can I export my patterns to other simulators?

A: Yes! Use **File → Export RLE...** to save in RLE format, which is compatible with Golly, WireWorld, and other cellular automata tools.

### Q: How do I create a custom rule?

A: Go to **Settings → Custom Rules...**. Specify birth conditions (B) and survival conditions (S) in standard notation (e.g., B3/S23 for Conway's Life).

### Q: What's this B3/S23 notation?

A:
- **B3**: A dead cell becomes alive if it has exactly 3 live neighbors
- **S23**: A live cell survives if it has 2 or 3 live neighbors

This is the standard "birth/survival" notation for life-like rules.

## Pattern & Rules

### Q: What are some interesting patterns to try?

A: Load one of the built-in patterns:
- **Glider**: Simple moving pattern (4-cell period)
- **Glider Gun**: Continuously creates gliders
- **R-Pentomino**: Small unstable pattern with complex behavior
- **Random Soup**: Random starting configuration

### Q: How do I find oscillators?

A: 
1. Load "Random Soup" pattern
2. Let it run for 100+ generations to stabilize
3. Pause and look for repeating patterns
4. Use **Tools → Analyze Pattern** to detect periods

### Q: Can I import patterns from other sources?

A: If you have RLE files from other tools, use **File → Import RLE...**. Otherwise, paste coordinates and recreate the pattern.

### Q: What makes a good starting pattern?

A: Small, asymmetrical patterns tend to produce interesting behavior. Try:
- R-Pentomino (5 cells)
- Acorn (7 cells)
- Bi-Pond (8 cells)
- Random dense seeds

## Performance & Optimization

### Q: Why is the simulation slow?

A: Several factors:
1. Grid size (larger grids are slower)
2. Cell display size (display is CPU intensive)
3. Rule complexity (some rules are naturally slower)
4. System resources (check if other apps are using CPU)

See [Performance Guide](./performance.md) for optimization tips.

### Q: What's the maximum grid size?

A: Depends on your hardware, but typically:
- 1000×1000: No issues
- 5000×5000: Slower but usable
- 10000×10000: May need optimization

Use **Settings → Grid & View Settings...** to adjust.

### Q: How do I make simulations run faster?

A: 
1. Reduce cell display size
2. Lower speed slider (fewer updates/second)
3. Reduce grid dimensions
4. Use sparser patterns
5. Upgrade hardware

### Q: Does LifeGrid support GPU acceleration?

A: Not currently, but it's planned for a future release. Simulations use NumPy/SciPy which are already optimized for CPU.

## Files & Data

### Q: What format should I save patterns in?

A: 
- **Personal use**: JSON (preserves metadata)
- **Sharing with others**: RLE (universal compatibility)
- **Visual sharing**: PNG (image format)

### Q: Can I convert between JSON and RLE?

A: LifeGrid can import/export both. Load a JSON, then export as RLE or vice versa.

### Q: How large can pattern files be?

A: JSON files scale with grid size. A 1000×1000 grid is typically 100-500 KB. RLE is usually more compact (90-95% smaller for sparse patterns).

### Q: Where are my settings and patterns saved?

A: 
- Windows: `%APPDATA%\lifegrid\`
- macOS: `~/Library/Application Support/lifegrid/`
- Linux: `~/.lifegrid/` or `~/.config/lifegrid/`

## Automata Questions

### Q: What's the difference between Life modes?

A:
- **Conway's Life**: B3/S23 - stable, complex
- **HighLife**: B36/S23 - includes replicators
- **Immigration**: Multi-colored variant
- **Rainbow**: Extended color mixing
- **Brian's Brain**: Three-state rule
- **Wireworld**: Logic circuit simulation
- **Langton's Ant**: Ant-based symbol manipulation

### Q: Can I mix multiple rules?

A: Currently, simulations use one rule. But you can save states between rules or use custom rules that approximate multiple behaviors.

### Q: Are there other well-known rules to try?

A: Yes! Popular life-like rules:
- B2/S: Seeds (explosive)
- B4/S34: Assimilation (smooth growth)
- B1357/S1357: Replicator (very explosive)
- B45/S345: Assimilation (variant)

See [Advanced Features Guide](./03_advanced_features.md#life-like-rules-bs-notation) for more.

## Development & Plugins

### Q: Can I add my own rules as a plugin?

A: Yes! See [Plugin Development Guide](./plugin_development.md) for instructions.

### Q: Can I use LifeGrid programmatically?

A: Yes! LifeGrid can be used as a library:

```python
from lifegrid.core.simulator import Simulator
sim = Simulator()
sim.initialize(mode='conway')
sim.step()
grid = sim.get_grid()
```

See [API Reference](../reference/core_api.md) for details.

### Q: How do I contribute to LifeGrid?

A: See [Contributing Guide](../../CONTRIBUTING.md) in the repository root. 

### Q: Is LifeGrid open source?

A: Yes! MIT licensed. See [LICENSE](../../LICENSE).

## Troubleshooting

### Q: LifeGrid won't start

A: 
1. Check Python version: `python --version` (need 3.11+)
2. Install dependencies: `pip install -r requirements.txt`
3. Try running with verbose output: `python -v src/main.py`
4. See [Troubleshooting Guide](./troubleshooting.md)

### Q: Grid doesn't update when I click Start

A:
1. Check the **Speed** slider (not at 0)
2. Verify drawing mode isn't enabled (pauses simulation)
3. Try stepping manually with **Step** button
4. See [Troubleshooting Guide](./troubleshooting.md)

### Q: Patterns won't save/load

A:
1. Check file permissions
2. Verify disk has space
3. Ensure JSON files are valid
4. Try different location
5. See [Troubleshooting Guide](./troubleshooting.md)

### Q: Tkinter issues on Linux

A: Install Tkinter:
```bash
sudo apt-get install python3-tk     # Ubuntu/Debian
sudo dnf install python3-tkinter    # Fedora
```

See [Installation Guide](./01_installation.md#troubleshooting-installation) for more OS-specific help.

## I Have More Questions!

- Check the [User Guide](./02_user_guide.md)
- Read [Advanced Features](./03_advanced_features.md)
- See [Troubleshooting Guide](./troubleshooting.md)
- Review [API Documentation](../reference/)
- Check [GitHub Issues](https://github.com/James-HoneyBadger/LifeGrid/issues)
- Create a new issue with your question
