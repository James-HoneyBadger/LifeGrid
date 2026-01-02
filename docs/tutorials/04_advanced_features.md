# Advanced Features Tutorial

In this tutorial, you'll learn powerful features that unlock LifeGrid's full potential.

## 1. Statistics & Analysis

### Monitoring Pattern Behavior

As simulation runs, watch the statistics panel:

- **Generation**: Current step number
- **Population**: Count of live cells
- **Birth Rate**: New cells this generation
- **Death Rate**: Cells died this generation
- **Density**: % of grid that's alive

### Understanding Statistics

```
Generation 0: Start with Random Soup (maybe 25% density)
Generation 100: Pattern stabilizes (5-10% density)
Generation 1000: Oscillators or still lifes (stable)
```

### Tracking Trends

Export statistics to track changes:

1. Run a long simulation
2. Save statistics at key points
3. Plot population trend over time
4. Look for patterns:
   - Steady growth = expanding pattern
   - Oscillating = periodic behavior
   - Flat line = stable equilibrium

## 2. Undo/Redo for Exploration

### Non-destructive Experimentation

LifeGrid tracks changes, allowing safe experimentation:

1. Create a pattern
2. Run simulation
3. If interesting: continue
4. If not: Press Backspace (undo) multiple times
5. Return to previous state
6. Try different approach

### History Depth

Default: Last 100 actions stored

Change in Settings → Preferences if needed:

```python
# More history = more memory used
# Less history = faster operations
100 actions = ~50 MB for 1000×1000 grid
```

## 3. Symmetry Drawing

### Creating Symmetric Patterns

Symmetry modes multiply your effort:

```
Manual drawing: 10 cells = 10 clicks
With symmetry: 10 cells = 2-3 clicks (rest auto-mirrored)
```

### Available Symmetries

1. **Horizontal**: Vertical center axis mirror
2. **Vertical**: Horizontal center axis mirror
3. **Diagonal**: Both diagonal mirrors
4. **Point**: 180° rotation around center

### Creating Art

1. Enable symmetry (try Diagonal)
2. Draw in one corner
3. Watch it replicate symmetrically
4. Run simulation
5. Observe how symmetry evolves

**Tip**: Diagonal symmetry creates beautiful kaleidoscopic patterns.

## 4. Grid Resizing

### Working with Different Scales

Small grids for quick exploration:

```
128×128: Instant response, small patterns
256×256: Good balance, medium patterns
512×512: Detailed patterns, slower
1024×1024+: Detailed research, requires optimization
```

### Resizing Workflow

1. **Design on small grid** (128×128)
2. **Test patterns** quickly
3. **Zoom**: Settings → Cell Display Size smaller
4. **Final rendering**: Larger grid, optimized settings

## 5. Pattern Comparison

### A/B Testing Patterns

Discover what makes patterns interesting:

1. **Save Base Pattern**: File → Save Pattern "Base"
2. **Modify one cell**: Use Pen/Eraser
3. **Save Variant**: File → Save Pattern "Variant"
4. **Load each**: Compare behavior
5. **Iterate**: Find optimal variations

### Systematic Exploration

```
Original: Glider at position (50,50)

Test 1: Glider at (50,51) - one cell down
Test 2: Glider at (51,50) - one cell right
Test 3: Glider at (52,51) - diagonal offset

Compare results and document interesting combinations
```

## 6. Performance Optimization

### Finding the Bottleneck

**Is it slow rendering or slow computation?**

1. **Reduce cell size**: Settings → Grid & View
   - If faster: bottleneck was rendering
   - If same: bottleneck was computation

2. **Reduce grid size**: Settings → Grid & View
   - If faster: bottleneck was computation
   - If same: might be rule-dependent

### Optimization Strategies

**For rendering bottleneck**:
- Reduce cell display size (most effective)
- Reduce update frequency (Speed slider lower)

**For computation bottleneck**:
- Reduce grid dimensions
- Use sparser patterns
- Choose faster rules

See [Performance Guide](../guides/07_performance.md) for detailed optimization.

## 7. Advanced Drawing Techniques

### Layered Pattern Creation

Complex patterns built from simple components:

```
1. Draw Glider at (10,10)
2. Draw Glider at (30,20)
3. Draw still life at (50,50)
4. Run and observe interactions
5. Adjust positions until result is interesting
```

### Copy and Modify

Build variations of working patterns:

1. Load successful pattern
2. Save as "Template"
3. Modify slightly
4. Run simulation
5. If interesting, save as new pattern
6. Document changes that helped

## 8. Custom Rule Creation

### Systematic Rule Testing

Explore rule space methodically:

```
Base rule: B3/S23

Iteration 1: B3/S234  (add survival condition)
Result: More stable - GOOD

Iteration 2: B34/S234 (add birth condition)
Result: Chaotic - NOT GOOD

Iteration 3: B3/S23   (revert)
Result: Back to baseline
```

### Rule Effects

Document how rules affect patterns:

- **Adding birth conditions**: More growth
- **Adding survival conditions**: More stability
- **Removing conditions**: Faster extinction

See [Custom Rules Tutorial](./03_custom_rules.md) for detailed exploration.

## 9. Export & Visualization

### PNG Export

Create publication-quality images:

```
Settings:
- Cell size: 2-5 pixels (depends on grid size)
- Grid lines: Yes (easier to understand)
- Colors: Default
- Quality: Maximum
```

### PNG Optimization

```
Large grid (2000×2000), large cells (5px):
- 10,000×10,000 pixel image
- ~500 KB PNG file

Small grid (512×512), small cells (1px):
- 512×512 pixel image
- ~10 KB PNG file

Find balance for your use case
```

### Creating Sequence

Export key generations to show evolution:

1. Save pattern as "base"
2. Run to generation 10 → Export "gen_10.png"
3. Continue to generation 50 → Export "gen_50.png"
4. Continue to generation 100 → Export "gen_100.png"
5. Create animated GIF from sequence

## 10. Batch Operations

### Running Multiple Simulations

If using LifeGrid programmatically:

```python
from lifegrid.core.simulator import Simulator

patterns = ["glider", "blinker", "glider_gun"]
for pattern_name in patterns:
    sim = Simulator()
    sim.initialize(mode='conway')
    # sim.load_pattern(pattern_name)  # If available
    
    for _ in range(100):
        sim.step()
    
    print(f"{pattern_name}: final population = {sim.get_grid().sum()}")
```

See [Advanced Features Guide](../guides/03_advanced_features.md) for code examples.

## 11. Pattern Discovery

### Systematic Pattern Hunting

Find interesting patterns in rule variants:

```
For each rule (B3/S23, B36/S23, B45/S345, ...):
  1. Load Random Soup
  2. Run 500+ generations
  3. Look for stable regions
  4. Isolate stable patterns
  5. Save if interesting
```

### Oscillator Detection

Find repeating patterns:

1. Run simulation until stable
2. Count generations between same state
3. If repeats: oscillator found
4. Document period (repeat count)

### Spaceship Classification

Identify moving patterns:

1. Mark position of pattern
2. Note generation count
3. Mark new position
4. Calculate: displacement per period
5. Classify: glider (diagonal), LWSS (horizontal), etc.

## 12. Performance Benchmarking

### Measuring Your Hardware

```python
from lifegrid.core.simulator import Simulator
import time

for grid_size in [256, 512, 1000, 2000]:
    sim = Simulator()
    sim.config.width = grid_size
    sim.config.height = grid_size
    sim.initialize()
    
    start = time.time()
    for _ in range(100):
        sim.step()
    elapsed = time.time() - start
    
    print(f"{grid_size}×{grid_size}: {elapsed:.2f}s for 100 steps")
```

### Using Results

Use benchmark data to:
- Estimate grid size for target speed
- Plan computation time
- Understand hardware limits

## Practical Advanced Exercises

### Exercise 1: Rule Optimization

Goal: Find the best rule for interesting patterns in 60 seconds.

1. Define "interesting": moving, oscillating, complex
2. Systematically test 10-15 rules
3. Time each test (10 generations)
4. Rank by interest level
5. Document top 3 rules

### Exercise 2: Pattern Art

Goal: Create a visually interesting pattern.

1. Start with symmetric drawing
2. Use Diagonal symmetry
3. Create intricate pattern
4. Run simulation to watch evolution
5. Export as PNG

### Exercise 3: Behavior Classification

Goal: Classify pattern behaviors across rules.

1. Create test pattern
2. For each mode/rule:
   - Run simulation
   - Note: dies/stable/oscillates/grows
3. Create table of behaviors
4. Share findings

### Exercise 4: Methuselah Discovery

Goal: Find a small pattern with long lifespan.

1. Manually design 3-5 cell patterns
2. For each:
   - Run until stable or dies
   - Note generation count
3. Find longest-lasting pattern
4. Try to extend it (larger variants)

## Tips for Advanced Usage

### Productive Workflow

```
1. Exploration Phase (10-15 min)
   - Try multiple patterns/rules
   - Look for interesting behaviors
   
2. Refinement Phase (10-15 min)
   - Take promising candidates
   - Optimize through modification
   - Save good results
   
3. Documentation Phase (5 min)
   - Export interesting results
   - Save patterns with descriptions
   - Create comparison notes
```

### Record Keeping

Keep notes while exploring:

```
Session Date: 2025-01-15

Pattern: Modified Glider Gun
Mode: Conway's (B3/S23)
Grid: 256×256
Observations:
  - Generates gliders regularly
  - Interesting collision with still life
  - Saved as "glidergun_variant_1"

Rule Experiment: B34/S23
Result: Too chaotic, not interesting
```

### Avoiding Redundant Work

- Document discoveries
- Name patterns descriptively
- Use version numbers for iterations
- Backup important patterns

## Next Steps

You've mastered LifeGrid's advanced features! Continue with:

1. **Exporting & Sharing** (next tutorial)
2. **API Integration** (see [API Reference](../reference/core_api.md))
3. **Plugin Development** (see [Plugin Guide](../guides/08_plugin_development.md))
4. **Performance Optimization** (see [Performance Guide](../guides/07_performance.md))

Your LifeGrid mastery continues!
