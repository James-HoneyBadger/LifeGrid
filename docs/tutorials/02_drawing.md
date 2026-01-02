# Drawing & Editing Patterns Tutorial

In this tutorial, you'll master creating and editing patterns in LifeGrid.

## Drawing Basics

### The Drawing Modes

LifeGrid has three drawing modes in the left panel:

1. **Toggle Mode**: Click individual cells to flip them on/off
2. **Pen Mode**: Click and drag to draw continuous lines
3. **Eraser Mode**: Click and drag to erase cells

### Creating Your First Pattern

1. **Clear the grid**: Press `C` or click **Clear**
2. **Select drawing mode**: Click **Pen** tool
3. **Draw on canvas**: Click and drag to create a shape
4. **Start simulation**: Click **Start**

Watch your pattern evolve! Some patterns die, some stabilize, some grow infinitely.

## Pattern Editing Strategies

### Strategy 1: Build and Test

```
1. Draw a small pattern
2. Run simulation
3. If interesting, save it
4. If not, use Back button to undo
5. Modify and try again
```

### Strategy 2: Symmetry Amplification

Draw symmetric patterns for beauty and predictability:

1. **Enable symmetry**: Select symmetry option (Horizontal, Vertical, Diagonal, or Point)
2. **Draw normally**: Your strokes are automatically mirrored
3. **Result**: Perfect symmetry without manual adjustment

**Symmetry Options**:
- **None**: Standard drawing
- **Horizontal**: Mirror across vertical center line
- **Vertical**: Mirror across horizontal center line
- **Diagonal**: Mirror across both diagonals
- **Point**: 180° rotational symmetry

### Strategy 3: Pattern Composition

Build larger patterns from known building blocks:

```
1. Start with empty grid
2. Place Gliders at strategic locations
3. Add stabilizers (still life objects)
4. Run simulation to see interactions
5. Adjust positions and repeat
```

## Working with the Undo System

LifeGrid tracks all changes (up to 100 by default).

### Undo/Redo

- **Undo**: Backspace or Edit → Undo (Ctrl+Z)
- **Redo**: Edit → Redo (Ctrl+Y)
- **Step backward**: Press `Left` or click **Back** button

**Note**: 
- **Back** button undoes *generations* (steps in simulation)
- **Undo** undoes *drawing actions* (edits to grid)

### Using History Efficiently

1. Make significant modifications
2. Run simulation
3. If interesting, save it
4. If not, use undo to revert
5. Try variations

## Refining Patterns

### Finding the Sweet Spot

Some patterns are too simple (die immediately), others too complex (chaotic forever).

**Example: Creating an Oscillator**

1. Draw a small pattern (3-5 cells)
2. Run for 10 generations
3. If it dies: draw larger
4. If it's chaotic: draw simpler
5. Look for repeating cycles

### Copy and Modify

1. **Save current pattern**: File → Save Pattern
2. **Modify on canvas**
3. **Save as new**: File → Save Pattern (give new name)
4. **Compare**: Load and examine each version

## Working with Grids

### Grid Size Considerations

- **Small (128×128)**: Fast, perfect for quick experiments
- **Medium (512×512)**: Good balance of detail and speed
- **Large (2000×2000)**: For detailed final patterns

**Change grid size**: Settings → Grid & View Settings

### Cell Display Size

Affects how patterns appear visually and rendering speed:

- **Large cells (10+ px)**: Easy to see, slow
- **Medium cells (3-5 px)**: Good balance
- **Small cells (1-2 px)**: Fast, harder to draw precisely

**Change cell size**: Settings → Grid & View Settings → Cell Display Size

## Drawing Techniques

### Creating Common Patterns

#### Still Life (Non-changing)

```
Block (4 cells):       Beehive (6 cells):
X X                    _X X_
X X                    X _ X
                       _X X_
```

Try drawing these and watch them stay stable!

#### Oscillators (Repeating)

```
Blinker (period 2):    Toad (period 2):
X X X          _X X X          X _ X
               X X _          _X X X
```

#### Spaceships (Moving)

```
Glider (moves diagonally):
_ X _
_ _ X
X X X
```

### Efficient Drawing

1. **Use Toggle mode for precision**: Click individual cells for exact placement
2. **Use Pen mode for large areas**: Drag to quickly fill regions
3. **Use symmetry for symmetric patterns**: Reduces drawing time
4. **Use grid visual**: Helps align patterns

## Advanced Drawing

### Combining Patterns

Create complex patterns from simpler ones:

```python
# Mentally:
1. Draw one Glider
2. Draw another Glider offset by 5 cells
3. Watch them interact
4. Adjust positions for desired effect
```

### Designing Methuselahs

Methuselahs are small patterns with extremely long lifespans:

1. Start with 5-10 cells
2. Run for 1000+ generations
3. Adjust if pattern dies out
4. Document generation count to stability

**R-Pentomino** is a famous methuselah:
```
_ X _
X X _
_ X _
_ X _
```
Takes 1103 generations to stabilize!

## Practical Exercises

### Exercise 1: Still Life Gallery

Create a collection of still lifes:

1. Draw a simple pattern (3-5 cells)
2. Run simulation
3. If it stabilizes: save it
4. If not: modify and try again
5. Build a collection of 5+ different still lifes

**Tip**: Study known still lifes first, then recreate them from memory.

### Exercise 2: Oscillator Hunt

Find oscillators with different periods:

1. Load "Random Soup"
2. Run for 100+ generations
3. Pause and look for repeating patterns
4. Isolate and save interesting ones
5. Document their period (repetition frequency)

### Exercise 3: Spaceship Design

Create variations of the Glider:

1. Start with standard Glider
2. Modify one cell at a time
3. Run simulation
4. If it moves, you've found a spaceship!
5. Document its movement pattern

### Exercise 4: Symmetric Art

Create beautiful symmetric patterns:

1. Enable symmetry (Diagonal recommended)
2. Draw a pattern on one quadrant
3. Watch symmetry replicate your strokes
4. Run simulation
5. Observe how symmetry evolves

## Collaboration & Sharing

### Sharing Patterns with Others

1. **Save pattern**: File → Save Pattern
2. **Send JSON file**: Email or post online
3. **Others load it**: File → Load Pattern

Patterns are stored as JSON, readable and portable.

### Converting to RLE

For sharing with other simulators:

1. Load your pattern
2. **File → Export RLE**
3. Send .rle file
4. Others can load in Golly or other tools

## Tips & Tricks

### Quick Fixes

- **Oops! Drew too much?** Press Backspace (undo)
- **Need to restart?** Press `C` (clear)
- **Want to see better?** Reduce Speed, let simulation run

### Performance While Drawing

- Use smaller grid when designing (128×128)
- Switch to larger grid when done
- Reduce cell size for faster rendering

### Finding Inspiration

- Study the built-in patterns
- Check out Golly pattern library online
- Read about cellular automata theory
- Experiment with random patterns

## Common Pitfalls

### Pattern Draws Weirdly

**Problem**: Pattern doesn't look right when drawing.

**Cause**: Grid lines might be confusing.

**Solution**: Toggle grid with `G` key to see cells clearly.

### Symmetry Not Working

**Problem**: Enabled symmetry but strokes aren't mirrored.

**Cause**: Wrong symmetry mode selected.

**Solution**: Try different symmetry options to find desired mirror effect.

### Can't Select Drawing Mode

**Problem**: Clicking drawing tools doesn't enable them.

**Cause**: Simulation might be running.

**Solution**: Stop simulation first (press `Space`).

## Practice Patterns

Here are patterns to recreate by hand:

### Easy (2 min)
```
Blinker:
X
X
X

Block:
X X
X X
```

### Medium (5 min)
```
Glider:
_ X _
_ _ X
X X X

Toad:
_ X X X
X X X _
```

### Hard (10 min)
```
Lightweight Spaceship (LWSS):
X _ _ X _
_ _ _ _ X
X _ _ _ X
_ X X X X
```

## Next Steps

- Learn [Custom Rules](./03_custom_rules.md) to make patterns behave differently
- Explore [Advanced Features](./04_advanced_features.md) for tools
- Read [User Guide](../guides/02_user_guide.md) for complete reference

Remember: Cellular automata are about experimentation. Draw, test, modify, repeat!
