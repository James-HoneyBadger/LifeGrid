# Custom Rules Tutorial

In this tutorial, you'll learn to create and experiment with custom cellular automaton rules.

## Understanding B/S Notation

Cellular automaton rules use "Birth/Survival" notation:

**Format**: `B*/S*`

- **B** = Birth conditions (when dead cells become alive)
- **S** = Survival conditions (when live cells stay alive)
- Numbers = Count of live neighbors required

### The Neighborhood

Each cell has 8 neighbors (surrounding cells):

```
X X X
X O X
X X X
```

A cell's neighbor count ranges from 0-8.

### Example: Conway's Life (B3/S23)

- **B3**: Dead cells become alive with exactly 3 neighbors
- **S23**: Live cells survive with 2 or 3 neighbors

This creates stable, complex patterns.

## Your First Custom Rule

### Opening the Rule Editor

1. **Settings → Custom Rules...**
2. You'll see two input fields:
   - Birth conditions (currently "3")
   - Survival conditions (currently "23")
3. These define the current rule

### Modifying a Rule

Let's try a simple variation:

1. **Clear the grid**: Press `C`
2. **Load a pattern**: Pattern dropdown → "Random Soup"
3. **Open settings**: Settings → Custom Rules...
4. **Current rule**: B3/S23 (Conway's Life)
5. **Change survival**: Type "234" instead of "23"
6. **Watch the change**: Pattern evolves differently
7. **If boring**: Try "25" instead of "234"
8. **Revert**: Back to "23" to return to Conway's

Notice how small changes create very different behaviors!

## Exploring Rule Space

### Safe Rules to Try

Here are rules with interesting but safe behaviors:

| Rule | Name | Behavior |
|------|------|----------|
| B3/S23 | Conway's Life | Stable, complex |
| B36/S23 | HighLife | Replicators |
| B3/S234 | 34 | Very stable |
| B4/S34 | Assimilation | Smooth growth |
| B2/S | Seeds | Explosive |
| B45/S345 | Assimilation (variant) | Structured growth |
| B2/S0 | Deadly | Rapid extinction |

### Dangerous Rules to Avoid

These rules can crash or be very slow:

- **B1/S1**: Everything fills in
- **B012345678/S012345678**: Everything fills
- **B/S**: Everything dies (empty rule)
- **B0/S**: Unstable explosive growth

### Systematic Exploration

Explore rules methodically:

```
Start: B3/S23

Vary birth:
- B2/S23
- B4/S23
- B35/S23

Vary survival:
- B3/S2
- B3/S3
- B3/S24
```

For each, run on Random Soup and observe:
- Does it fill the grid?
- Does it create interesting patterns?
- Does it stabilize or grow?

## Rule Categories

### Growth Rules

Rules that cause pattern expansion:

- **B2/S**: Produces growing structures
- **B4/S34**: Structured, manageable growth
- **B45/S345**: Beautiful smooth growth

**Pattern**: Usually fill grid or create fractals

### Stable Rules

Rules that create equilibrium:

- **B3/S23**: Conway's (classic stable)
- **B36/S23**: HighLife (still stable)
- **B3/S234**: Even more stable

**Pattern**: Eventually stabilize or become periodic

### Chaotic Rules

Rules with complex, unpredictable behavior:

- **B2/S1**: Very chaotic
- **B3/S012**: Chaotic turbulence
- **B12/S012**: Sensitive to initial conditions

**Pattern**: Never settle into clear behavior

## Creating Interesting Rules

### Strategy 1: Mix and Match

Take successful rules and modify slightly:

1. Start with Conway's (B3/S23)
2. Add one birth condition: B34/S23
3. Test on Random Soup
4. If interesting, save
5. If not, try different condition

### Strategy 2: Symmetry

Rules with symmetric conditions often interesting:

- **B3/S3**: All neighbor counts equal
- **B12345/S12345**: High symmetry
- **B246/S246**: Even neighbor counts

### Strategy 3: Minimal Rules

Simple rules often produce surprising results:

- **B3/S**: Only birth, no survival
- **B/S23**: No birth, survival only
- **B4/S4**: Single condition for each

## Documenting Your Discoveries

### Creating a Rule Database

Keep track of rules you discover:

```
Favorite Rules:

1. B3/S23 - Conway's Life
   - Classic, stable
   - Great for learning
   - Complex emergent behavior

2. B36/S23 - HighLife
   - Replicator patterns
   - Beautiful fractals
   - More variety than Conway's

3. B45/S345 - Assimilation
   - Smooth, organized growth
   - Creates maze-like structures
   - Visually appealing
```

### Saving Rules

LifeGrid saves custom rules automatically in:
- `~/.lifegrid/custom_rules.json`

You can edit this file to add descriptions or tags.

## Practical Exercises

### Exercise 1: Find a Replicator Rule

Goal: Find a rule where patterns duplicate or multiply.

1. Start with B36/S23 (HighLife - known to have replicators)
2. Load "Random Soup"
3. Run simulation
4. Look for patterns that repeat periodically
5. Try variations: B35/S23, B37/S23, etc.

### Exercise 2: Fastest Extinction

Goal: Find the rule where all patterns die fastest.

1. Start with B/S (no birth, no survival)
2. Load "Random Soup"
3. Check generation count when empty
4. Try B/S1, B/S2, etc.
5. Document which dies fastest

**Result**: Probably B/S (everything dies immediately).

### Exercise 3: Most Stable Rule

Goal: Find rule where patterns most likely stabilize.

1. Start with B3/S234
2. Load "Random Soup"
3. Run for 100 generations
4. Check if pattern stabilized
5. Try B3/S234, B3/S2345, B3/S23456, etc.
6. Compare stability

### Exercise 4: Gallery of Gliders

Goal: Find rules that support moving patterns.

1. Start with Conway's Glider
2. Switch to different modes/rules
3. Note which ones move
4. Save variations
5. Create gallery of gliders in different rules

## Advanced Rule Concepts

### Totalistic Rules

Rules that depend only on total neighbor count (not positions):

- All B/S notation rules are totalistic
- Simplest and most common

### Outer-Totalistic Rules

Rules that consider cell state and neighbors:

- More complex (not in basic LifeGrid)
- More varied behaviors
- See [Architecture Documentation](../architecture/) for details

### Rule Anatomy

```
B3/S23

B = Birth conditions (when dead → live)
  3 = Dead cell becomes alive with 3 neighbors

S = Survival conditions (when live → live)
  2 = Live cell survives with 2 neighbors
  3 = Live cell survives with 3 neighbors

Multiple conditions:
B3/S23 = (3 births) AND (2 OR 3 survival)
```

## Sharing Custom Rules

### Exporting Rules

Custom rules are saved in `~/.lifegrid/custom_rules.json`.

To share:
1. Backup the JSON file
2. Send to others
3. They place in their ~/.lifegrid/ directory

### Creating Rule Collections

Organize rules by category:

```json
{
  "conway_variants": [
    {"rule": "B3/S23", "name": "Conway's Life"},
    {"rule": "B3/S234", "name": "Conway + Stability"},
    {"rule": "B34/S23", "name": "Conway + Birth"}
  ],
  "growth_rules": [
    {"rule": "B4/S34", "name": "Assimilation"},
    {"rule": "B45/S345", "name": "Smooth Growth"}
  ]
}
```

## Rule Predictions

### Predicting Behavior

Some heuristics:

- **More birth conditions** → More growth
- **Fewer survival conditions** → Patterns die faster
- **B3** present → Usually stable
- **B1/S1** → Fill everything

Use these to predict what a rule might do before testing.

### Testing Hypothesis

1. **Predict**: "B2/S23 should cause more growth"
2. **Test**: Load Random Soup with B2/S23
3. **Observe**: Does it grow more?
4. **Conclude**: Confirm or refine hypothesis
5. **Document**: Record findings

## Common Rule Variations

### Variants of Conway's (B3/S23)

```
B3/S23  → Original Conway
B3/S234 → More stable
B34/S23 → More births
B3/S23c → Torus (wraps at edges)
```

### Exploring Birth Variations

```
B3/S23  → Original
B23/S23 → Include 2-neighbor births
B34/S23 → Include 4-neighbor births
B345/S23 → Include 3,4,5-neighbor births
```

### Exploring Survival Variations

```
B3/S23  → Original
B3/S234 → Add 4-survival
B3/S2345 → Add 4,5-survival
B3/S123 → Add 1-survival
```

## Troubleshooting Rule Issues

### Rule Crashes Application

**Cause**: Rule creates infinite fills or extreme growth.

**Solution**:
1. Close LifeGrid
2. Edit `~/.lifegrid/custom_rules.json`
3. Remove problematic rule
4. Restart

### Rule Runs Too Slowly

**Cause**: Rule is computationally expensive.

**Solution**:
1. Reduce grid size (Settings)
2. Use sparser patterns
3. Try simpler rule

### Rule Behaves Unexpectedly

**Cause**: May have misunderstood notation or rule interaction.

**Solution**:
1. Verify rule notation is correct
2. Test on simple known pattern
3. Run step-by-step (use Step button)
4. Compare with standard rules

## Recommended Exploration Order

1. **First**: Stick with B3/S23 (Conway's) for baseline
2. **Second**: Try B36/S23 (HighLife) to see variation
3. **Third**: Try B45/S345 (Assimilation) for growth
4. **Fourth**: Create 5 variations yourself
5. **Fifth**: Try chaotic rules (B2/S1, B12/S012)
6. **Finally**: Find your personal favorite

## Rule Resources

- **Online Rule Explorer**: Golly website has rule database
- **Research Papers**: Search "cellular automaton rules" academic databases
- **Community**: Share discoveries on cellular automata forums
- **LifeGrid Docs**: See API Reference for programmatic rule creation

## Next Steps

- Learn [Advanced Features](./04_advanced_features.md)
- Explore [Plugin Development](../guides/08_plugin_development.md)
- Read [Architecture Documentation](../architecture/system_architecture.md)
- Study cellular automata theory

Remember: Rule exploration is a journey of discovery. What rule will you find next?
