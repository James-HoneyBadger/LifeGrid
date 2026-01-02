# User Guide

## Overview

LifeGrid is an interactive cellular automaton simulator with a graphical user interface. This guide covers all the main features and how to use them.

## Starting LifeGrid

After installation, launch the application:

```bash
python src/main.py
```

The main window displays:
- **Canvas**: Central area for simulation display
- **Control Panel**: Left side with simulation controls
- **Mode Selector**: Choose which automaton to simulate
- **Menu Bar**: File, Simulation, Settings, Help menus

## Main Interface

### Control Buttons

- **Start**: Begin the simulation (keyboard: `Space`)
- **Stop**: Pause the simulation
- **Step**: Execute one generation (keyboard: `S`)
- **Back**: Undo one generation (keyboard: `Left`)
- **Clear**: Clear the entire grid (keyboard: `C`)
- **Speed**: Slider to control simulation speed (generations per second)

### Drawing Tools

Located in the left panel:

1. **Toggle Mode**: Click to toggle cells on/off
2. **Pen Mode**: Click and drag to draw patterns
3. **Eraser Mode**: Click and drag to erase cells
4. **Symmetry Options**:
   - None: No symmetry
   - Horizontal: Mirror across vertical axis
   - Vertical: Mirror across horizontal axis
   - Diagonal: Mirror across diagonals
   - Point: 180° rotational symmetry

### Mode Selection

The **Mode** dropdown offers different cellular automaton rules:

- **Conway's Game of Life**: The classic automaton (B3/S23)
- **HighLife**: Similar to Conway's with replicator patterns (B36/S23)
- **Immigration Game**: Multi-color variant of Life
- **Rainbow Game**: Extended color mixing rules
- **Langton's Ant**: Ant-based symbol manipulation
- **Brian's Brain**: Three-state rule with decay
- **Wireworld**: Logic circuit simulation
- **Custom Rules**: Define your own B/S rules

### Pattern Presets

Select a **Pattern** from the dropdown to quickly load initial configurations:

- **Conway's Life**: Classic Mix, Glider Gun, Spaceships, Oscillators, Puffers, R-Pentomino, Acorn, Random Soup
- **HighLife**: Replicator, Random Soup
- **Immigration**: Color Mix, Random Soup
- **Rainbow**: Rainbow Mix, Random Soup
- **Langton's Ant**: Empty grid
- **Custom**: Random Soup

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Start/Stop | `Space` |
| Step Forward | `S` |
| Step Backward | `Left` |
| Clear Grid | `C` |
| Toggle Grid Lines | `G` |

## Drawing on the Canvas

### Basic Drawing

1. Select drawing mode (Toggle, Pen, or Eraser)
2. Click on cells to modify them:
   - **Toggle**: Click to flip cell state
   - **Pen**: Click and drag to draw
   - **Eraser**: Click and drag to erase
3. Use symmetry options to mirror your strokes

### Symmetry Drawing

Enable symmetry to create mirrored patterns:

1. Select symmetry mode (Horizontal, Vertical, Diagonal, or Point)
2. Draw normally - your strokes are automatically mirrored

This is useful for creating symmetric patterns quickly.

## Simulating

### Basic Workflow

1. Select automaton **Mode** from dropdown
2. Choose a **Pattern** or draw on canvas
3. Click **Start** (or press `Space`)
4. Adjust **Speed** slider as needed
5. Watch the simulation evolve

### Pausing and Stepping

- Click **Stop** to pause mid-simulation
- Click **Step** to advance one generation
- Click **Back** to go back one generation
- Resume with **Start**

### Monitoring Statistics

The info panel displays:
- **Generation**: Current simulation step
- **Population**: Number of live cells
- **Birth Rate**: Cells born this generation
- **Death Rate**: Cells died this generation
- **Density**: Percentage of grid occupied

## File Operations

### Save Pattern

**File → Save Pattern...**

Save the current grid state as a JSON file for later loading.

Patterns are stored with:
- Grid dimensions
- Cell configuration
- Automaton mode information

### Load Pattern

**File → Load Pattern...**

Load a previously saved pattern. The grid size and mode are restored.

### Export to PNG

**File → Export to PNG...** (requires Pillow)

Create a high-quality image of the current grid. Export options include:
- Cell size (pixels per cell)
- Include grid lines
- Color scheme

## Settings

### Grid & View Settings

**Settings → Grid & View Settings...**

- **Grid Width**: Number of columns
- **Grid Height**: Number of rows
- **Cell Display Size**: Pixels per cell (1-50)
- **Show Grid Lines**: Toggle grid overlay

### Custom Rules

**Settings → Custom Rules...**

Define your own life-like automaton:

1. Specify **Birth** conditions (B)
2. Specify **Survival** conditions (S)
3. Rules are applied immediately

**Example Rules:**
- B3/S23 = Conway's Game of Life
- B36/S23 = HighLife
- B2/S = Replicator
- B1357/S1357 = Replicator (variant)

### Preferences

**Settings → Preferences...**

Adjust application behavior:
- Auto-save patterns
- Default grid size
- Initial speed setting
- Theme preferences

## Tips & Tricks

### Finding Interesting Patterns

1. Load "Random Soup" pattern
2. Run for several hundred generations
3. Look for stable patterns or oscillators

### Creating Oscillators

1. Draw a small pattern
2. Use **Back** to step backward if it dies out
3. Refine manually until it oscillates

### Generating Spaceships

1. Start with "Glider Gun" pattern
2. Pause periodically to examine new spaceships
3. Save interesting patterns using **File → Save Pattern**

### Custom Rules Exploration

1. Go to **Settings → Custom Rules**
2. Try different B/S combinations
3. Start with random patterns to see behavior

## Working with Large Grids

For grids larger than 500×500 cells:
- Reduce display cell size for better performance
- Lower simulation speed
- Use zoom features if available
- Consider using faster hardware

## Performance

If the simulation runs slowly:

1. Reduce **Cell Display Size** in settings
2. Lower **Speed** slider
3. Reduce grid dimensions
4. Close other applications

For detailed performance analysis, see [Performance Guide](./performance.md).

## Troubleshooting

**Grid not updating?**
- Ensure simulation is running (click **Start**)
- Check that **Speed** slider isn't at minimum
- Try stepping manually with **Step** button

**Can't draw on canvas?**
- Pause simulation first (click **Stop**)
- Ensure a drawing tool is selected
- Check that grid isn't too zoomed out

**File won't save?**
- Ensure you have write permissions in the directory
- Check that disk has free space
- Try a different location

See [Troubleshooting Guide](./troubleshooting.md) for more help.

## Next Steps

- Learn advanced features in [Advanced Features Guide](./advanced_features.md)
- Explore [Custom Rules Tutorial](../tutorials/03_custom_rules.md)
- Try [Exporting & Sharing](../tutorials/05_exporting.md)
