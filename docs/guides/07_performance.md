# Performance Guide

## Understanding Performance

LifeGrid's performance depends on several factors:

- **Grid size**: Larger grids require more computation
- **Display size**: Rendering impacts CPU usage
- **Rule complexity**: Different rules have different computational demands
- **Pattern sparsity**: Dense grids are slower
- **System hardware**: CPU and RAM availability

## Performance Benchmarks

### Reference Performance

On modern hardware (Intel i7, 16GB RAM):

| Grid Size | Cell Size | FPS | Gen/sec |
|-----------|-----------|-----|---------|
| 256×256 | 4px | 60 | 60 |
| 512×512 | 2px | 30 | 30 |
| 1000×1000 | 1px | 15 | 15 |
| 2000×2000 | 1px | 5 | 5 |
| 5000×5000 | 1px | 1 | 1 |

Times vary based on rule and pattern sparsity.

## Optimization Strategies

### 1. Cell Display Size (Highest Impact)

**Problem**: Rendering is often the bottleneck.

**Solution**: Reduce cell display size.

| Cell Size | Pixels Per Grid | Rendering Cost |
|-----------|-----------------|-----------------|
| 20px | 256×256 = 65K | Base |
| 10px | 512×512 = 260K | 4x |
| 5px | 1024×1024 = 1M | 16x |
| 2px | 2560×2560 = 6.5M | 100x |
| 1px | 5120×5120 = 26M | 400x |

**Recommendation**: 
- Development/exploration: 3-5 pixels
- Final runs/benchmarks: 1-2 pixels
- Large grids: 1 pixel

### 2. Grid Dimensions

**Problem**: Larger grids = more cells to compute.

**Impact on Performance**:
- 256×256 = 65,536 cells → ~1ms per generation
- 512×512 = 262,144 cells → ~4ms per generation
- 1024×1024 = 1,048,576 cells → ~16ms per generation

**Optimization**:

Use appropriate sizes for your task:

```
Discovery/Exploration: 256×256 to 512×512
Detailed Simulation: 512×512 to 1000×1000
Publication/Benchmarks: 1000×1000 to 2000×2000
```

### 3. Speed Slider Configuration

**Counter-intuitive Optimization**:

The "Speed" slider doesn't directly affect computation speed. It controls update frequency:

- **Higher speed**: Updates more frequently, uses more CPU for rendering
- **Lower speed**: Longer delay between updates, allows computation to catch up

**Optimization**:

```
For smooth 60fps display:
Speed = (Target_FPS / Max_Possible_FPS) × 100

Example:
Max 30 FPS possible → Speed 60 for smooth 18 FPS
Max 15 FPS possible → Speed 50 for smooth 7.5 FPS
```

### 4. Pattern Sparsity

**Principle**: Fewer live cells = faster computation.

**Optimization**:

```
Sparse pattern:   1% density → Fast
Normal pattern:   10% density → Normal
Dense pattern:    50%+ density → Slow
Chaotic pattern:  Nearly 50% → Slowest
```

**Recommendation**:
- Test with sparser patterns first
- Dense grids inherently slower
- For benchmarking, control density

### 5. Rule Selection

**Performance by Rule**:

| Rule | Complexity | Speed |
|------|-----------|-------|
| B3/S23 (Conway) | Low | Fast |
| B36/S23 (HighLife) | Low | Fast |
| B1357/S1357 (Replicator) | Very High | Very Slow |
| Custom (depends) | Variable | Variable |

**Optimization**:
- Standard rules are optimized
- Avoid explosive rules (B1/S1, etc.)
- Test custom rules on small grid first

### 6. System Resources

**Check system availability**:

```bash
# Monitor while running
top -p $(pgrep python)

# Check available RAM
free -h

# Monitor thermal state
sensors  # If installed
```

**Optimization**:
- Close other applications
- Monitor temperature (throttling if too hot)
- Ensure adequate RAM available

## Profiling and Benchmarking

### Built-in Benchmarking

Run LifeGrid's performance suite:

```bash
python -m lifegrid.performance.benchmarking
```

Generates report showing:
- Generation times by grid size
- Memory usage patterns
- Optimal settings for hardware

### Custom Benchmarking

```python
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig
import time
import numpy as np

def benchmark_rule(rule_name, grid_size, iterations=100):
    """Benchmark a specific rule."""
    config = SimulatorConfig(width=grid_size, height=grid_size)
    sim = Simulator(config)
    sim.initialize(mode='conway')
    
    # Warm up
    for _ in range(10):
        sim.step()
    
    # Benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        sim.step()
    elapsed = time.perf_counter() - start
    
    gen_time = (elapsed / iterations) * 1000  # ms per generation
    fps = iterations / elapsed
    
    print(f"{rule_name} ({grid_size}×{grid_size}): {gen_time:.2f}ms per gen, {fps:.1f} gen/sec")
    
    return gen_time

# Test multiple sizes
for size in [128, 256, 512, 1000]:
    benchmark_rule('conway', size, iterations=100)
```

### Profiling Specific Operations

```python
import cProfile
import pstats
from lifegrid.core.simulator import Simulator

def run_sim():
    sim = Simulator()
    sim.initialize(mode='conway')
    for _ in range(1000):
        sim.step()

# Profile
profiler = cProfile.Profile()
profiler.enable()

run_sim()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

**Output shows**:
- Function call counts
- Time spent in each function
- Cumulative vs. local time

Look for:
- High call counts
- High cumulative time
- Unexpected hot spots

## Memory Optimization

### Memory Usage Analysis

```python
import psutil
import os
from lifegrid.core.simulator import Simulator

process = psutil.Process(os.getpid())

def get_memory_mb():
    return process.memory_info().rss / 1024 / 1024

# Baseline
baseline = get_memory_mb()
print(f"Baseline: {baseline:.1f} MB")

# Create simulator
sim = Simulator()
sim.initialize(mode='conway')

after_init = get_memory_mb()
print(f"After init: {after_init:.1f} MB ({after_init-baseline:.1f} MB overhead)")

# Run for 1000 generations
for i in range(1000):
    sim.step()
    if i % 100 == 0:
        current = get_memory_mb()
        print(f"After {i} gens: {current:.1f} MB ({current-after_init:.1f} MB accumulation)")
```

### Memory Optimization Techniques

1. **Clear undo history**:
```python
sim.undo_manager.clear()  # Free memory from stored states
```

2. **Use appropriate grid size**:
```
Memory = width × height × 2 bytes (approximately)
1000×1000 = ~2 MB
5000×5000 = ~50 MB
10000×10000 = ~200 MB
```

3. **Reduce history depth**:
```python
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig

config = SimulatorConfig()
config.undo_history_limit = 50  # Reduce from default 100
sim = Simulator(config)
```

## Distributed/Batch Processing

### Running Multiple Simulations

```python
import multiprocessing as mp
from lifegrid.core.simulator import Simulator
from lifegrid.core.config import SimulatorConfig

def run_simulation(rule_name):
    config = SimulatorConfig(width=512, height=512)
    sim = Simulator(config)
    sim.initialize(mode=rule_name)
    
    for _ in range(100):
        sim.step()
    
    return f"{rule_name}: {sim.get_metrics_summary()['population']} cells"

if __name__ == '__main__':
    with mp.Pool(4) as pool:  # 4 parallel simulations
        results = pool.map(run_simulation, ['conway', 'highlife', 'immigration', 'rainbow'])
    
    for result in results:
        print(result)
```

### GPU Acceleration (Future)

Currently not implemented, but planned. Would provide:
- 10-100x speedup for large grids
- Parallel cellular computation
- Faster pattern analysis

## Performance Bottleneck Analysis

### Step 1: Identify the Bottleneck

```python
import time
from lifegrid.core.simulator import Simulator

sim = Simulator()
sim.initialize(mode='conway')

# Measure computation
comp_start = time.perf_counter()
for _ in range(100):
    sim.step()
comp_time = time.perf_counter() - comp_start
print(f"Computation: {comp_time*10:.2f}ms per generation")

# Measure rendering (GUI only)
# This depends on display backend
# Generally: rendering >> computation for small-medium grids
```

### Step 2: Apply Targeted Optimization

**If computation is slow**:
- Reduce grid size
- Use sparse patterns
- Profile rule complexity

**If rendering is slow**:
- Reduce cell display size (biggest impact)
- Reduce update frequency
- Use lower resolution display

## Advanced Optimizations

### Caching Patterns

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_neighborhood_pattern(cell_state, neighbor_count):
    """Cache neighbor pattern lookups."""
    # Implementation here
    pass
```

### Vectorization

LifeGrid uses NumPy/SciPy for vectorized operations, which are already optimized.

### Rule Compilation

For custom rules, pre-compile lookup tables:

```python
# Instead of computing rules each step,
# Pre-compute 512-entry lookup table
# Maps (current_state, neighbor_count) → next_state
```

## Monitoring Tools

### Built-in Monitoring

Enable in settings:
- Frame time display
- Generation time display
- Memory usage indicator
- CPU usage percentage

### External Tools

**Linux/macOS**:
```bash
# Real-time monitoring
top

# Detailed process info
ps aux | grep python

# Memory profiling
pip install memory-profiler
python -m memory_profiler script.py
```

**Windows**:
- Task Manager (Performance tab)
- Resource Monitor
- Performance Profiler

## Optimization Checklist

When experiencing performance issues:

- [ ] Cell display size optimized (reduce first)
- [ ] Grid size appropriate for task
- [ ] Speed slider set reasonably
- [ ] No background heavy processes
- [ ] Pattern sparsity checked
- [ ] Rule complexity examined
- [ ] Undo history cleared if large
- [ ] System resources available
- [ ] GPU not available (future feature)
- [ ] Thermal throttling not happening

## Guidelines by Use Case

### Interactive Exploration
- Grid: 256×256 to 512×512
- Cell size: 3-5 pixels
- Speed: Medium (50-70)
- Goal: Responsive interface

### Research/Benchmarking
- Grid: 1000×1000 to 5000×5000
- Cell size: 1 pixel
- Speed: Optimize for computation
- Goal: Accurate measurements

### Large-scale Simulation
- Grid: 5000×5000 or larger
- Cell size: 1 pixel
- Speed: Low (let computation catch up)
- Goal: Complete simulation

## Performance FAQ

**Q: Why is it slower than Golly?**
A: Golly is written in C++. LifeGrid in Python. Python adds overhead but is more flexible.

**Q: Can I use LifeGrid on old hardware?**
A: Yes, with smaller grids (128×128) and larger cell sizes (10px+).

**Q: What limits grid size?**
A: Mostly RAM. A 20,000×20,000 grid uses ~800 MB.

**Q: Why lower speed slider helps?**
A: It's not "slower," it's "less frequent rendering," giving computation time.

**Q: Should I always optimize?**
A: Only if you notice slowness. For exploration, responsiveness matters more.

## Further Reading

- See [API Reference](../reference/core_api.md) for programmatic options
- Check [Advanced Features](./03_advanced_features.md) for batch processing
- Review [System Architecture](../architecture/system_architecture.md) for design details
