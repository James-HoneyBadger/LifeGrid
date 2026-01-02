# Getting Started with LifeGrid

Welcome! This tutorial will get you up and running with LifeGrid in 10 minutes.

## 1. Installation (2 minutes)

If you haven't installed yet, see [Installation Guide](../guides/01_installation.md).

Quick check - run this to verify everything works:

```bash
python src/main.py
```

You should see the LifeGrid window open with an empty grid.

## 2. Understanding the Interface (2 minutes)

The main window has three sections:

**Left Panel - Controls**:
- Mode dropdown (choose automaton type)
- Pattern dropdown (choose starting pattern)
- Buttons: Start, Stop, Step, Back, Clear
- Speed slider
- Drawing mode selector

**Center - Canvas**:
- Grid where simulation happens
- Click to interact with cells

**Top - Menu**:
- File (save/load patterns)
- Simulation (control play/pause)
- Settings (configure)

## 3. Your First Simulation (3 minutes)

### Running a Classic Pattern

1. **Select Mode**: Click the **Mode** dropdown, select "Conway's Game of Life"
2. **Load Pattern**: Click the **Pattern** dropdown, select "Glider"
   - You'll see a small L-shaped pattern on the canvas
3. **Start Simulation**: Click the **Start** button (or press `Space`)
4. **Watch It Move**: The pattern will repeat every 4 generations, moving diagonally
5. **Pause**: Click **Stop** (or press `Space`) to pause
6. **Step**: Click **Step** (or press `S`) to advance one generation at a time

Congratulations! You've run your first simulation!

### Understanding What You Saw

The **Glider** is a famous 5-cell pattern that:
- Repeats every 4 generations
- Moves diagonally
- Can travel indefinitely
- Is the basis for many complex patterns

## 4. Try Different Patterns (2 minutes)

Experiment with different patterns to see different behaviors:

1. **Clear the grid**: Click **Clear** (or press `C`)
2. **Try a new pattern**:
   - Select "Glider Gun" - produces endless gliders
   - Select "R-Pentomino" - starts chaotic, becomes complex
   - Select "Random Soup" - random initial state

Each behaves differently. Try pausing and stepping to observe details.

## 5. Draw Your Own Pattern

Instead of using presets, create your own:

1. **Clear**: Click **Clear** to start fresh
2. **Select drawing mode**: Click **Pen** tool on the left
3. **Draw on canvas**: Click and drag to draw cells
4. **Start simulation**: Click **Start** to see what happens
5. **Modify**: Use **Back** button to undo generations, adjust, try again

**Tip**: Small asymmetric patterns tend to produce interesting results.

## 6. Explore the Modes

Each mode is a different cellular automaton rule:

- **Conway's Life** (B3/S23): The classic, most stable
- **HighLife** (B36/S23): Similar to Conway's but with replicators
- **Immigration**: Colored variant with interesting interactions
- **Rainbow**: Extended colors with different rules
- **Langton's Ant**: Ant-based rule system
- **Brian's Brain**: Three-state automaton
- **Wireworld**: Logic gates and circuits
- **Custom**: Define your own rules

Try each with "Random Soup" pattern to see different behaviors.

## 7. Understanding Statistics

During simulation, watch the **Info Panel** (usually below controls):

- **Generation**: How many steps have passed
- **Population**: Current number of live cells
- **Birth Rate**: Cells born this generation
- **Death Rate**: Cells died this generation
- **Density**: Percentage of grid alive

These help you understand pattern behavior.

## 8. Save Your Discoveries

Found something interesting?

1. **Stop simulation**: Press `Space` or click **Stop**
2. **Save Pattern**: **File → Save Pattern...**
3. **Name it**: Give your pattern a meaningful name
4. **Load later**: **File → Load Pattern...** to reload

Patterns are saved as JSON files with your pattern name.

## 9. Export as Image

Share your patterns as images:

1. **Arrange pattern**: Position it how you like
2. **Export**: **File → Export to PNG...**
3. **Choose options**:
   - Cell size (bigger = more detail)
   - Include grid lines (optional)
4. **Save**: Choose location and filename

Great for presentations or sharing discoveries!

## 10. Next Steps

You now understand the basics! Here are some paths forward:

### For Visual Exploration
- Read [User Guide](../guides/02_user_guide.md)
- Try all the modes
- Experiment with different patterns
- Build your own patterns

### For Advanced Features
- Read [Advanced Features Guide](../guides/03_advanced_features.md)
- Create custom rules
- Use analysis tools
- Try symmetry drawing modes

### For Developer Integration
- Check [API Reference](../reference/core_api.md)
- Read [Plugin Development Guide](../guides/08_plugin_development.md)
- Build custom plugins

### For Deep Understanding
- Study [System Architecture](../architecture/system_architecture.md)
- Explore the source code
- Try performance optimization

## Quick Reference

| Action | How |
|--------|-----|
| Start/Stop | Click **Start** or press `Space` |
| Single Step | Click **Step** or press `S` |
| Step Backward | Click **Back** or press `Left` |
| Clear Grid | Click **Clear** or press `C` |
| Toggle Grid Lines | Press `G` |
| Save Pattern | **File → Save Pattern...** |
| Load Pattern | **File → Load Pattern...** |
| Export PNG | **File → Export to PNG...** |

## Common Patterns to Find

Try these well-known patterns:

- **Still Lifes**: Patterns that don't change (Block, Beehive, Loaf)
- **Oscillators**: Patterns that repeat (Blinker, Toad, Beacon)
- **Spaceships**: Moving patterns (Glider, LWSS)
- **Methuselahs**: Simple patterns with complex evolution (R-Pentomino)

## Troubleshooting

**Grid not updating?**
- Check **Speed** slider (move right to increase speed)
- Click **Start** button to resume

**Can't draw?**
- Stop simulation first (click **Stop**)
- Select drawing tool (Pen or Eraser)

**Pattern doesn't behave as expected?**
- Try with different mode/rule
- Check it's the right pattern for the rule

See [Troubleshooting Guide](../guides/06_troubleshooting.md) for more help.

## What's Next?

Continue with these tutorials:

1. [Drawing & Editing Patterns](./02_drawing.md) - Master pattern creation
2. [Custom Rules](./03_custom_rules.md) - Define your own automaton rules
3. [Advanced Features](./04_advanced_features.md) - Unlock power-user features
4. [Exporting & Sharing](./05_exporting.md) - Share your discoveries

Have fun exploring the infinite world of cellular automata!
