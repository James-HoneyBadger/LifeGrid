# File Formats Guide

## Pattern Files

### JSON Format

LifeGrid uses JSON for pattern persistence.

**Example Pattern File**:

```json
{
  "version": "3.0",
  "metadata": {
    "name": "Glider",
    "author": "John Conway",
    "mode": "conway",
    "created": "2025-01-01",
    "tags": ["spaceship", "period-4", "minimal"]
  },
  "config": {
    "width": 100,
    "height": 100,
    "cell_size": 8
  },
  "grid": {
    "width": 100,
    "height": 100,
    "cells": [
      [0, 1],
      [1, 2],
      [2, 0],
      [2, 1],
      [2, 2]
    ]
  }
}
```

**Fields**:
- `version`: LifeGrid version (usually "3.0")
- `metadata`: Name, author, tags for organization
- `config`: Grid dimensions and display settings
- `grid`: Cell coordinates in [x, y] format

### RLE Format

Run-Length Encoded format (standard in cellular automata):

**Example**:

```
#N Glider
#O John Conway
#C A spaceshift spaceship.
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
```

**Syntax**:
- `#N`: Pattern name
- `#O`: Creator/author
- `#C`: Comment line (multiple allowed)
- `x = width, y = height, rule = B3/S23`: Header
- `b`: Dead cell
- `o`: Live cell
- Number prefix: Run length (e.g., `3b` = `bbb`)
- `$`: End of row
- `!`: End of pattern

**Common Abbreviations**:
- `2o` = `oo` (two live cells)
- `3b` = `bbb` (three dead cells)
- `2$` = `$$` (two blank rows)

### CSV Format (Statistics)

Exported simulation statistics:

```csv
generation,population,births,deaths,density
0,40,0,0,0.004
1,35,2,7,0.0035
2,38,6,3,0.0038
3,42,8,4,0.0042
```

### PNG Format (Exports)

High-quality image exports with options:

**Settings**:
- **Cell Size**: 1-50 pixels per cell
- **Grid Lines**: Optional overlay
- **Color Scheme**: Default, monochrome, custom
- **Background**: White or transparent

**Usage**:
```
File → Export to PNG...
Select dimensions and options
Choose output file location
```

## Configuration Files

### Application Settings

Located in `~/.lifegrid/settings.json`:

```json
{
  "appearance": {
    "theme": "light",
    "cell_size": 8,
    "grid_lines": true,
    "grid_color": "#cccccc"
  },
  "simulation": {
    "default_width": 100,
    "default_height": 100,
    "speed": 10,
    "mode": "conway"
  },
  "performance": {
    "max_history": 100,
    "enable_vsync": true,
    "render_optimization": true
  },
  "export": {
    "default_format": "png",
    "quality": 95,
    "background_color": "white"
  }
}
```

### Custom Rules File

If saved to `~/.lifegrid/custom_rules.json`:

```json
{
  "rules": [
    {
      "name": "My Custom Rule",
      "birth": [3],
      "survival": [2, 3],
      "states": 2,
      "description": "Conway's Game of Life variant"
    }
  ]
}
```

## Import/Export Workflows

### Importing from Other Simulators

Most cellular automata simulators support RLE:

1. Export pattern as RLE from other tool
2. In LifeGrid: File → Import RLE
3. Pattern loads with appropriate rule

**Compatible Tools**:
- Golly
- WireWorld
- Cellular Automata Explorer
- Conway's Game of Life online players

### Exporting for Sharing

**To share with other LifeGrid users**:
1. File → Save Pattern (JSON format)
2. Share JSON file

**To share with other tools**:
1. File → Export RLE
2. Share RLE file (compatible with most tools)

**To share visually**:
1. File → Export PNG
2. Share PNG image

## Batch File Processing

### Converting Multiple Patterns

```python
import json
import glob

# Convert JSON patterns to RLE
for json_file in glob.glob("patterns/*.json"):
    with open(json_file) as f:
        pattern = json.load(f)
    
    # Process and export as RLE
    rle_file = json_file.replace(".json", ".rle")
    # ... conversion logic
```

### Creating Pattern Collections

Organize patterns in folders:

```
my_patterns/
├── conway/
│   ├── still_lifes.json
│   └── spaceships.json
├── highlife/
│   └── replicators.json
└── metadata.json
```

**metadata.json**:

```json
{
  "collection_name": "My Pattern Library",
  "version": "1.0",
  "patterns": [
    {"file": "conway/still_lifes.json", "count": 24},
    {"file": "conway/spaceships.json", "count": 15}
  ]
}
```

## Data Preservation

### Backing Up Patterns

Important patterns should be backed up:

```bash
# Backup all patterns
cp -r ~/.lifegrid/patterns ~/.lifegrid/patterns.backup

# Or use version control
git add patterns/
git commit -m "Backup important patterns"
```

### Version Control

Track patterns in Git:

```bash
git init patterns/
git add .
git commit -m "Pattern library v1.0"
```

### Format Considerations

**JSON Benefits**:
- Human-readable
- Includes metadata
- Preserves grid dimensions
- Includes color information

**RLE Benefits**:
- Compact format
- Widely compatible
- Standard format
- Efficient for sparse patterns

**Choose based on your needs**:
- Personal use: JSON (keeps metadata)
- Sharing with others: RLE (wide compatibility)
- Publishing: PNG (visual + RLE (data))

## Troubleshooting Format Issues

### Can't Open JSON Pattern

1. Verify JSON is valid: `python -m json.tool file.json`
2. Check version compatibility
3. Look for encoding issues (should be UTF-8)

### RLE Import Fails

1. Verify RLE syntax (look for missing `!`)
2. Check rule compatibility (B3/S23 is default)
3. Ensure pattern dimensions match grid

### Export Creates Blank Image

1. Verify pattern has live cells
2. Check cell size setting
3. Ensure export path is writable
4. Try different cell size (1-5 pixels recommended)

## File Size Optimization

### Reducing Pattern File Size

For large patterns:

```python
import json

# Remove unnecessary metadata
pattern = {"grid": {...}}
with open("minimal.json", "w") as f:
    json.dump(pattern, f, separators=(',', ':'))
```

### RLE Compression

RLE is already compressed. For very large patterns:

```
# Original with runs
oooooooooo (10 cells) = 10 characters
10o = 3 characters
```

RLE files are typically 90-95% smaller than pixel images.

## Next Steps

- See [User Guide](./02_user_guide.md) for file operations
- Read [Advanced Features](./03_advanced_features.md) for batch processing
- Check [API Reference](../reference/core_api.md) for programmatic access
