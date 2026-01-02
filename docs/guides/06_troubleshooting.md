# Troubleshooting Guide

## Installation Issues

### "ModuleNotFoundError: No module named 'tkinter'"

**Cause**: Tkinter is not installed on your system.

**Solution**:

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**Fedora/RHEL**:
```bash
sudo dnf install python3-tkinter
```

**macOS (Homebrew)**:
```bash
brew install python-tk@3.13
```

**Windows**: 
- Reinstall Python from python.org, ensuring "tcl/tk and IDLE" is checked during installation
- Or with Conda: `conda install tk`

### "ModuleNotFoundError: No module named 'numpy'" (or scipy/PIL)

**Cause**: Python dependencies are not installed.

**Solution**:

```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt

# Or install individually
pip install numpy scipy pillow
```

### "Python version is too old"

**Cause**: You're running Python < 3.11.

**Solution**:

Check current version:
```bash
python --version
python3 --version
```

Install Python 3.13:
- **Linux**: Use your package manager or pyenv
- **macOS**: `brew install python@3.13`
- **Windows**: Download from python.org

### Wrong Python Version in Virtual Environment

**Cause**: Virtual environment was created with old Python.

**Solution**:

```bash
# Delete and recreate virtual environment
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Startup Issues

### Application Won't Start / Black Window Appears

**Cause**: Various possible causes - needs investigation.

**Solution**:

```bash
# Run with verbose output
python -v src/main.py 2>&1 | head -50

# Check for errors in output
# Common issues: missing display, Tkinter issues, file permissions
```

### "Display Error" or "No Display Available"

**Cause**: Running on remote/headless system or display server not available.

**Solution**:

If running over SSH, enable X11 forwarding:
```bash
ssh -X user@host
python src/main.py
```

For headless systems, use LifeGrid programmatically:
```python
from lifegrid.core.simulator import Simulator
sim = Simulator()
# ... use without GUI
```

### Application Crashes on Startup

**Cause**: Corrupted settings or compatibility issue.

**Solution**:

```bash
# Backup and clear settings
mv ~/.lifegrid ~/.lifegrid.backup
python src/main.py  # Recreates default settings

# If it works, settings were corrupted
# If not, there's a deeper issue
```

## Runtime Issues

### Grid Doesn't Update When Running

**Symptoms**: Clicked Start, but grid doesn't change.

**Diagnostic Steps**:

1. Check if simulation is actually running:
   - Status bar should show changing generation count
   - Try the **Step** button (single generation)

2. Check speed setting:
   - **Speed** slider at far left = paused
   - Move slider right to resume

3. Check if drawing mode is active:
   - Click a non-drawing tool
   - Drawing mode pauses simulation

4. Check if pattern has live cells:
   - Use **Tools → Cell Count**
   - Should show > 0 cells

**Solution**:

```
1. Check Speed slider (should be > 0)
2. Click "Start" button
3. Verify generation counter increases
4. Check status bar shows "Running"
```

### Grid Updates Too Slowly

**Symptoms**: Simulation runs but is very slow.

**Solutions** (in order of impact):

1. **Reduce display size**:
   - Settings → Grid & View Settings
   - Set "Cell Display Size" to 1-3 pixels
   - This is usually the bottleneck

2. **Reduce Speed slider** (counter-intuitive):
   - Lower value = more time between updates = less CPU usage
   - Fewer screen refreshes = smoother performance

3. **Reduce grid size**:
   - Settings → Grid & View Settings
   - Smaller grid = fewer calculations
   - Try 128×128 to test

4. **Check background processes**:
   - Close other CPU-heavy applications
   - Check system monitor
   - Restart computer if needed

5. **Profile the bottleneck**:

```python
import cProfile
import pstats

cProfile.run('from lifegrid.core.simulator import Simulator; sim = Simulator(); [sim.step() for _ in range(100)]', 'prof.stats')
stats = pstats.Stats('prof.stats')
stats.sort_stats('cumulative').print_stats(10)
```

### Pattern Drawing is Unresponsive

**Cause**: Canvas is frozen or unresponsive to clicks.

**Solutions**:

1. **Pause simulation first**:
   - Click **Stop** button
   - Allows full computational resources for drawing

2. **Reduce grid size**:
   - Large grids are slower to render
   - Try 100×100 for testing

3. **Reduce display size**:
   - Fewer pixels to render = faster response
   - Settings → Grid & View Settings

4. **Check for infinite loops**:
   - Custom rules might cause hangs
   - Try standard rules first

### High Memory Usage

**Symptoms**: Application uses lots of RAM, system becomes slow.

**Causes**:
- Large grid (5000×5000+ cells)
- Undo history accumulation
- Memory leak in pattern processing

**Solutions**:

1. **Clear undo history**:
   - Edit → Clear History
   - Each undo step stores grid (uses memory)

2. **Reduce grid size**:
   - Smaller grid = less memory
   - 1000×1000 uses ~4 MB, 5000×5000 uses ~100 MB

3. **Restart application**:
   - Clears accumulated history and caches
   - Memory returns to baseline

4. **Monitor memory**:

```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

## File Operations Issues

### "Permission Denied" When Saving

**Cause**: Don't have write permission for the directory.

**Solution**:

```bash
# Check permissions
ls -ld ~/lifegrid/patterns/

# Fix if needed
chmod 755 ~/lifegrid/patterns/

# Or save to different location
# File → Save As → /tmp/pattern.json
```

### JSON File Won't Load

**Symptoms**: File exists but can't open it.

**Diagnostic Steps**:

```bash
# Validate JSON syntax
python -m json.tool pattern.json

# If invalid, shows error
# Common issues: missing quotes, extra commas, bad escaping
```

**Solutions**:

1. **Verify JSON is valid**:

```python
import json
try:
    with open('pattern.json') as f:
        json.load(f)
    print("✓ Valid JSON")
except json.JSONDecodeError as e:
    print(f"✗ Invalid JSON: {e}")
```

2. **Check file permissions**:
```bash
ls -l pattern.json
chmod 644 pattern.json  # If needed
```

3. **Verify file not corrupted**:
   - Try oldest backup
   - Check file size (shouldn't be 0 bytes)

### PNG Export Creates Blank Image

**Symptoms**: Exported PNG is all white/black, no pattern visible.

**Causes**:
- Grid has no live cells
- Cell size too small
- Color settings wrong

**Solutions**:

1. **Verify grid has cells**:
   - Check generation counter > 0
   - Click to place some cells
   - Use **Tools → Cell Count**

2. **Adjust cell size**:
   - File → Export to PNG
   - Set "Cell Size" to 2-5 pixels
   - Avoid size=1 (too small to see)

3. **Check color settings**:
   - Settings → Preferences
   - Verify color scheme is not all white
   - Try default colors

4. **Test with simple pattern**:
   - Load built-in pattern (Glider)
   - Export that
   - If it works, your pattern issue is grid size

## Custom Rules Issues

### Custom Rule Causes Crash

**Symptoms**: App hangs or crashes when using custom rule.

**Cause**: Rule logic creates infinite loops or too many births.

**Solutions**:

1. **Switch to standard rule first**:
   - Mode dropdown → Conway's Life
   - Restart if needed

2. **Test rules carefully**:
   - Start with small grid (50×50)
   - Use sparse patterns
   - Monitor generation time

3. **Avoid explosive rules**:
   - B1/S1 (all cells alive) = crash
   - B012345678/S012345678 (chaotic) = very slow

4. **Safe rule templates**:

```
B3/S23      # Conway's (stable)
B3/S23      # Start from Conway
B36/S23     # Try variations carefully
B3/S234     # Slightly different survival
```

5. **Profile to find slow rule**:

```python
from lifegrid.core.simulator import Simulator
import time

sim = Simulator()
sim.initialize(mode='custom')
sim.set_rule("B3/S23")

start = time.time()
for _ in range(10):
    sim.step()
elapsed = time.time() - start
print(f"10 steps took {elapsed:.2f}s")
```

## Pattern Issues

### Pattern Doesn't Behave as Expected

**Symptoms**: Pattern doesn't evolve as anticipated, or dies immediately.

**Causes**:
- Wrong rule selected
- Pattern is dead for this rule
- Rule is incompatible

**Solutions**:

1. **Verify correct rule**:
   - Mode dropdown shows active rule
   - Check pattern requirements
   - Switch rules and retry

2. **Test with different rules**:
   - Some patterns only work with specific rules
   - Try Conway's Life (B3/S23) as baseline

3. **Start with built-in patterns**:
   - Known to work correctly
   - Use as reference

4. **Check pattern source**:
   - Ensure pattern is for right rule
   - Golly patterns specify rule in RLE header

### Pattern Generates Boring Results

**Symptoms**: Pattern quickly reaches equilibrium or dies.

**Solutions**:

1. **Try different patterns**:
   - Some are boring in selected rule
   - "Random Soup" usually more interesting

2. **Try different rules**:
   - Rule determines behavior
   - Try B36/S23 (HighLife) for variety

3. **Make pattern larger/denser**:
   - More cells = more potential interaction
   - Try "Random Soup" with different density

4. **Let it run longer**:
   - Some patterns take 100+ generations
   - Look for periodic or chaotic regions

### Lost Important Pattern

**Prevention/Recovery**:

1. **Check backup locations**:
```bash
ls -la ~/.lifegrid/
ls -la ~/.lifegrid/patterns/
ls -la ~/.lifegrid/patterns.backup/
```

2. **Check recycle bin/trash**:
   - Deleted files might be recoverable

3. **Search for file**:
```bash
find ~ -name "*.json" -mtime -7  # Files modified in last 7 days
```

4. **Prevent in future**:
   - Save frequently during work
   - Use version control: `git add patterns/`
   - Maintain backup: `cp patterns patterns.backup`

## Performance Profiling

### General Performance Issues

**Collect diagnostic data**:

```python
import sys
import numpy as np

# Basic info
print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")

# Test simulation speed
from lifegrid.core.simulator import Simulator
import time

sim = Simulator()
sim.initialize(mode='conway')

for size in [100, 200, 500]:
    sim.config.width = size
    sim.config.height = size
    sim.reset()
    
    start = time.time()
    for _ in range(100):
        sim.step()
    elapsed = time.time() - start
    
    print(f"{size}×{size}: {elapsed:.2f}s for 100 steps")
```

## When All Else Fails

### Gather Diagnostic Information

```bash
# Create diagnostic report
echo "=== System Info ===" > diagnostic.txt
python --version >> diagnostic.txt
uname -a >> diagnostic.txt

echo "=== Python Packages ===" >> diagnostic.txt
pip list >> diagnostic.txt

echo "=== Tkinter Test ===" >> diagnostic.txt
python -m tkinter >> diagnostic.txt 2>&1

# Send this file when reporting issues
cat diagnostic.txt
```

### Reporting Bugs

When reporting issues on GitHub:

1. **Include diagnostic info** from above
2. **Describe steps to reproduce**
3. **Include error message/traceback**
4. **Mention your OS and Python version**
5. **Include grid size and rule being used**

### Getting Support

- **GitHub Issues**: https://github.com/James-HoneyBadger/LifeGrid/issues
- **Check existing issues** before reporting
- **Provide minimal reproducible example**
- **Include relevant files** (patterns, settings)

## Performance Optimization Checklist

- [ ] Grid size reasonable (< 5000×5000)
- [ ] Cell display size > 1 pixel
- [ ] Speed slider not at minimum
- [ ] No background heavy processes
- [ ] Undo history cleared if large
- [ ] Custom rule tested for efficiency
- [ ] Using sparse patterns for testing
- [ ] Running on adequate hardware

## Getting Good Performance

**Priority order** (biggest impact first):
1. Cell display size (most impact)
2. Grid dimensions
3. Speed slider value
4. Background processes
5. Rule complexity
6. Pattern sparsity
7. Hardware capabilities

See [Performance Guide](./performance.md) for detailed optimization.

## Useful Commands

```bash
# Check system resources
top                              # Real-time resource monitor
free -h                         # Memory usage
df -h                           # Disk usage

# Check Python info
python -c "import sys; print(sys.executable)"
python -c "import tkinter; print('Tkinter OK')"

# Test specific module
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
```
