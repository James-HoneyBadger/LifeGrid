# Exporting & Sharing Tutorial

In this final tutorial, you'll learn how to export and share your LifeGrid creations.

## 1. Saving Patterns Locally

### JSON Format

LifeGrid's native format for patterns.

**How to Save**:

1. **Create/load pattern**: Set up pattern on canvas
2. **File → Save Pattern...**
3. **Enter name**: Descriptive name (e.g., "Glider Variant 1")
4. **Choose location**: Default is `~/.lifegrid/patterns/`
5. **Click Save**

**What's Saved**:
- Grid configuration (width, height)
- Cell states
- Pattern metadata (name, date, tags)

### Organizing Pattern Files

Create folder structure:

```
~/.lifegrid/patterns/
├── conway/
│   ├── still_lifes/
│   │   ├── block.json
│   │   ├── beehive.json
│   │   └── loaf.json
│   ├── oscillators/
│   │   ├── blinker.json
│   │   └── toad.json
│   └── spaceships/
│       └── glider.json
├── highlife/
│   └── replicators/
│       └── replicator_1.json
└── custom/
    └── my_discoveries.json
```

**Benefits**:
- Easy to find patterns
- Clear organization
- Follows pattern type
- Easy to share folders

### Backup Important Patterns

```bash
# Backup current patterns
cp -r ~/.lifegrid/patterns ~/.lifegrid/patterns.backup

# Or use Git version control
cd ~/.lifegrid/patterns
git init
git add .
git commit -m "Backup - important patterns"
```

## 2. Exporting to PNG

### Creating Images

Perfect for presentations, papers, or sharing visually.

**How to Export**:

1. **Arrange pattern**: Position it nicely
2. **File → Export to PNG...**
3. **Configure options**:
   - Cell size (1-50 pixels)
   - Include grid lines (usually yes)
   - Choose filename
4. **Click Export**

### PNG Export Settings

| Setting | Small Grid | Large Grid |
|---------|-----------|-----------|
| Cell Size | 3-5px | 1-2px |
| Grid Lines | Yes | Maybe |
| Quality | High | High |

**Guidelines**:
- Cell size 1-2 px: Information-dense, small file
- Cell size 3-5 px: Easy to see, medium file
- Cell size 10+ px: Very clear, large file

### File Size Considerations

```
256×256 grid + 3px cells = 768×768 image = ~100 KB PNG
1000×1000 grid + 1px cells = 1000×1000 image = ~300 KB PNG
5000×5000 grid + 1px cells = 5000×5000 image = ~5 MB PNG
```

Larger PNG files take longer to generate and view.

## 3. Exporting to RLE Format

### Run-Length Encoded Format

Standard format for cellular automata, compatible with other tools.

**How to Export**:

1. **File → Export RLE...**
2. **Choose filename**: `pattern.rle`
3. **LifeGrid generates**: Compact RLE file

**Example RLE**:

```
#N Glider
#O John Conway
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
```

### RLE Advantages

- **Compact**: 90-95% smaller than JSON for sparse patterns
- **Universal**: Works with Golly, WireWorld, other simulators
- **Readable**: Can edit text manually

### RLE Disadvantages

- **Limited metadata**: Name/author only (in comments)
- **Less data**: No color information
- **Standard rule**: Usually B3/S23

## 4. Sharing with Others

### Sharing JSON Files

For LifeGrid users:

1. **Export**: File → Save Pattern
2. **Send file**: Email, Discord, GitHub, etc.
3. **Recipient loads**: File → Load Pattern
4. **Recipient updates**: Click Load, select JSON file

**Advantages**:
- Full metadata preserved
- Works perfectly with LifeGrid
- Includes grid dimensions

### Sharing RLE Files

For any cellular automaton enthusiast:

1. **Export**: File → Export RLE
2. **Send file**: Email, paste online, post on forums
3. **Recipient loads**: Import in their tool:
   - Golly: File → Open
   - LifeGrid: File → Import RLE
   - Others: Depends on tool

**Advantages**:
- Works with many tools
- Small file size
- Widely understood format

### Sharing PNG Images

For visual presentation:

1. **Export**: File → Export to PNG
2. **Post online**: Social media, blog, forums
3. **Anyone can view**: Displays as regular image

**Advantages**:
- Everyone can view
- Great for social media
- Shows pattern visually

### Sharing on GitHub

Create pattern repository:

```
my-patterns/
├── README.md          # Description
├── LICENSE            # MIT, CC0, etc.
├── patterns/
│   ├── glider.json
│   ├── glider.rle
│   ├── glider.png
│   └── ...
└── images/
    ├── glider_evolution.gif
    └── ...
```

**In README.md**:

```markdown
# My Cellular Automata Patterns

Collection of interesting patterns for LifeGrid.

## Patterns

### Glider Variant
- Mode: Conway's Life
- Dimensions: 50×50
- Features: Moving spaceship
- Files: `glider.json`, `glider.rle`, `glider.png`

## Usage

1. Download `glider.json`
2. In LifeGrid: File → Load Pattern
3. Select file and click Load

## License

CC0 (public domain) - use freely!
```

## 5. Creating Pattern Collections

### Themed Collections

Organize patterns by theme:

**"Oscillators Collection"**:
```
oscillators/
├── period_1/
│   └── still_lifes.json  # "Period 1" = non-moving
├── period_2/
│   ├── blinker.json
│   ├── toad.json
│   └── clock.json
├── period_3/
│   ├── pulsar.json
│   └── beehive_clock.json
└── period_4+/
    └── long_period.json
```

**"Learning Collection"**:
```
learning/
├── 01_basics/
│   ├── block.json          # Still life
│   ├── blinker.json        # Oscillator
│   └── glider.json         # Spaceship
├── 02_intermediate/
│   ├── glider_gun.json
│   ├── r_pentomino.json
│   └── acorn.json
└── 03_advanced/
    └── methuselah.json
```

### Creating a Catalog

Document your collection:

```markdown
# Pattern Catalog

## Still Lifes
- **Block**: 2×2 square (most stable)
- **Beehive**: 6-cell shape
- **Loaf**: 8-cell pattern

## Oscillators
- **Blinker**: Period 2 (flip flops)
- **Toad**: Period 2 (more complex)
- **Pulsar**: Period 3 (symmetric)

## Spaceships
- **Glider**: Period 4 (slow)
- **LWSS**: Period 4 (faster)
- **HWSS**: Period 4 (heaviest)
```

## 6. Creating Animated Sequences

### Capturing Evolution

Show pattern change over time:

**Method 1: Manual Screenshots**

1. Set pattern
2. Run to generation 0
3. Export as "gen_0.png"
4. Run to generation 10
5. Export as "gen_10.png"
6. Repeat every 10-50 generations

**Method 2: Programmatic**

```python
from lifegrid.core.simulator import Simulator
import os

sim = Simulator()
sim.initialize(mode='conway')
# Load your pattern

os.makedirs('sequence', exist_ok=True)

for gen in range(0, 200, 10):
    # Run to generation
    while sim.get_metrics_summary()['generation'] < gen:
        sim.step()
    
    # Export current state
    grid = sim.get_grid()
    # Save as PNG (requires visualization module)
    filename = f'sequence/gen_{gen:04d}.png'
    print(f'Exported {filename}')
```

### Creating GIFs

Combine PNGs into animated GIF:

```bash
# Install ImageMagick if needed
# sudo apt-get install imagemagick

# Create GIF from PNG sequence
convert -delay 20 sequence/gen_*.png animation.gif

# Optimize GIF size
gifsicle -O3 animation.gif -o animation_small.gif
```

**Delay settings**:
- 10: Very fast
- 20: Fast
- 50: Normal
- 100: Slow

## 7. Documentation & Presentation

### Writing Pattern Descriptions

For each pattern, document:

```markdown
# Glider Variant 1

## Basic Info
- **Rule**: B3/S23 (Conway's Life)
- **Grid Size**: 50×50
- **Period**: 4 (repeats every 4 generations)
- **Type**: Spaceship (moving pattern)

## Description
A variant of the classic glider spaceship.
Moves diagonally at 1 cell per 4 generations.

## Starting Configuration
The pattern consists of 5 cells arranged in:
```
_X_
__X
XXX
```

## Evolution
- Gen 0: Initial L-shape
- Gen 1: Changes to rotated shape
- Gen 2: Another rotation
- Gen 3: Another rotation
- Gen 4: Back to original, shifted diagonally

## Properties
- **Speed**: Slow (1 cell/4 generations)
- **Stability**: Stable indefinitely
- **Interaction**: Collides with solid objects
- **Uses**: Component in larger patterns

## Files
- `glider.json` - LifeGrid format
- `glider.rle` - RLE format (compatible with Golly)
- `glider.png` - Visual representation

## References
- Classic glider pattern
- Derived from John Conway's Game of Life
- Basis for Glider Guns and other constructions
```

### Creating Presentation Slides

```markdown
# Interesting Patterns in Conway's Life

## Slide 1: Glider
[Image: glider_evolution.gif]
- Moving pattern (spaceship)
- Most basic non-still-life pattern
- Period 4

## Slide 2: Glider Gun
[Image: glider_gun.png]
- Produces infinite gliders
- Complex interaction of patterns
- Period 30

## Slide 3: R-Pentomino
[Image: r_pentomino_evolution.gif]
- Only 5 cells!
- Takes 1103 generations to stabilize
- Beautiful example of emergent complexity
```

## 8. Academic & Research Use

### Publishing Patterns

If presenting research:

1. **Document thoroughly**:
   - Initial configuration
   - Rule used
   - Grid size
   - Evolution description

2. **Provide files**:
   - RLE (for universal compatibility)
   - PNG (for publications)
   - JSON (for LifeGrid users)

3. **Include metadata**:
   - Discovery date
   - Author information
   - Relevant research citations

### Citing Patterns

If using known patterns:

```bibtex
@misc{glider,
  author = {Conway, John Horton},
  title = {Glider},
  journal = {Game of Life Patterns},
  year = {1970}
}
```

## 9. Community Sharing

### Online Communities

Share discoveries on:

- **GitHub**: Create public repository
- **Golly Forums**: Post RLE files
- **Reddit**: r/cellular_automata
- **Conwaylife.com**: Pattern database
- **Medium/Blogs**: Write articles about discoveries

### Contributing to Databases

Many communities maintain pattern databases:

1. **Check existing databases**: Avoid duplicates
2. **Document thoroughly**: Clear descriptions
3. **Provide multiple formats**: RLE + PNG
4. **Test with multiple tools**: Ensure compatibility

## Practical Exercises

### Exercise 1: Create a Pattern Portfolio

Goal: Document 5 interesting patterns.

For each pattern:
1. Save JSON in organized folder
2. Export PNG with good settings
3. Write description
4. Note the rule and dimensions
5. Save to portfolio folder

### Exercise 2: Share on GitHub

Goal: Create public GitHub repository.

1. Create GitHub account
2. Create new repository
3. Upload:
   - Patterns as JSON/RLE
   - Images as PNG
   - README.md with descriptions
4. Share link!

### Exercise 3: Create a GIF Sequence

Goal: Show pattern evolution visually.

1. Create interesting pattern
2. Export PNG every 5 generations
3. Create 10-20 frame GIF
4. Share on social media or include in blog

### Exercise 4: Write a Pattern Guide

Goal: Educate others.

1. Choose 3 patterns (different types)
2. Document each:
   - What it is
   - Why it's interesting
   - How to use it
3. Create guide with images
4. Share with others

## Best Practices

### File Organization

```
✓ Named descriptively: "glider_variant_1.json"
✗ Generic names: "pattern1.json"

✓ In organized folders by type
✗ All in one flat directory

✓ Backup important discoveries
✗ Only digital copy, no backup
```

### Documentation

```
✓ Include metadata: rule, dimensions, date
✗ Just file name

✓ Clear descriptions of what it does
✗ No explanation

✓ Multiple formats: JSON + RLE + PNG
✗ Single format only
```

### Sharing

```
✓ Credit original discoverer
✗ Claim credit for others' work

✓ Document modifications you made
✗ Pass off as original

✓ Include license/copyright info
✗ Unclear usage rights

✓ Test compatibility before sharing
✗ Assume it works in other tools
```

## Next Steps

You've completed all tutorials! Now:

1. **Explore on your own**: Create, save, share patterns
2. **Join communities**: Connect with other enthusiasts
3. **Contribute**: Share discoveries online
4. **Learn more**: Study [Architecture Documentation](../architecture/)
5. **Develop**: Check [Plugin Development Guide](../guides/08_plugin_development.md)

Happy discovering! 🎉
