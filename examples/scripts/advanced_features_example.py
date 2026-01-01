#!/usr/bin/env python3
"""
Advanced Features Example

This script demonstrates all advanced features in Phase 8:
- Statistics collection and export
- Rule discovery from observations
- RLE format import/export
- Heatmap generation
- Symmetry analysis
- Pattern analysis
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np

# Import advanced features
from src.advanced import (
    StatisticsCollector, StatisticsExporter,
    RuleDiscovery,
    RLEParser, RLEEncoder,
    HeatmapGenerator, SymmetryAnalyzer,
    PatternAnalyzer
)

# Import simulation
from src.automata.conway import ConwayGameOfLife
from src.automata.highlife import HighLife


def demo_statistics():
    """Demonstrate statistics collection and export."""
    print("\n" + "="*60)
    print("DEMO 1: Statistics Collection and Export")
    print("="*60)
    
    # Create automaton
    automaton = ConwayGameOfLife(width=50, height=50)
    
    # Load a preset pattern
    automaton.load_pattern("Oscillators")
    
    # Collect statistics
    collector = StatisticsCollector()
    
    print("\nSimulating 50 steps and collecting statistics...")
    for step in range(50):
        grid = automaton.get_grid()
        collector.collect(step, grid)
        automaton.step()
    
    # Get summary
    summary = collector.get_summary()
    print(f"\nSimulation Summary:")
    print(f"  Total steps: {summary['total_steps']}")
    print(f"  Final population: {summary['final_alive']}")
    print(f"  Average density: {summary['avg_density']:.3f}")
    print(f"  Average births per step: {summary['avg_births']:.1f}")
    print(f"  Average deaths per step: {summary['avg_deaths']:.1f}")
    
    # Export to CSV
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    csv_file = output_dir / "simulation_stats.csv"
    StatisticsExporter.export_csv(collector.get_statistics(), str(csv_file))
    print(f"\n✓ Statistics exported to {csv_file}")
    
    # Export summary
    summary_file = output_dir / "simulation_summary.csv"
    StatisticsExporter.export_summary(collector.get_statistics(), str(summary_file))
    print(f"✓ Summary exported to {summary_file}")
    
    # Try to generate plots (requires matplotlib)
    try:
        plot_file = output_dir / "simulation_plots.png"
        StatisticsExporter.generate_plots(
            collector.get_statistics(),
            str(plot_file)
        )
        print(f"✓ Plots generated at {plot_file}")
    except ImportError:
        print("! Matplotlib not installed - skipping plot generation")


def demo_rule_discovery():
    """Demonstrate rule discovery."""
    print("\n" + "="*60)
    print("DEMO 2: Rule Discovery")
    print("="*60)
    
    # Create Conway's Game of Life
    automaton = ConwayGameOfLife(width=30, height=30)
    automaton.load_pattern("Oscillators")
    
    # Create rule discovery
    discovery = RuleDiscovery(neighborhood_type='moore')
    
    print("\nObserving Conway's Life for 20 steps...")
    for _ in range(20):
        grid_before = automaton.get_grid().copy()
        automaton.step()
        grid_after = automaton.get_grid()
        discovery.observe_transition(grid_before, grid_after)
    
    # Get discovered rules
    rules = discovery.infer_birth_survival_rules(min_confidence=0.8)
    birth_rules = rules.get('birth', set())
    survival_rules = rules.get('survival', set())
    
    print(f"\nDiscovered Rules:")
    print(f"  Birth rules: {sorted(birth_rules)}")
    print(f"  Survival rules: {sorted(survival_rules)}")
    
    notation = discovery.format_birth_survival_notation(birth_rules, survival_rules)
    print(f"  B/S Notation: {notation}")
    print(f"  (Conway's Life is B3/S23)")
    
    # Export rules
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    rules_file = output_dir / "discovered_rules.txt"
    discovery.export_rules(str(rules_file))
    print(f"\n✓ Rules exported to {rules_file}")
    
    # Get rule summary
    summary = discovery.get_rule_summary()
    print(f"\nRule Discovery Summary:")
    print(f"  Total observations: {summary['total_observations']}")
    print(f"  Unique patterns: {summary['unique_patterns']}")
    print(f"  High confidence rules: {summary['high_confidence_rules']}")
    print(f"  Medium confidence rules: {summary['medium_confidence_rules']}")


def demo_rle_format():
    """Demonstrate RLE format parsing and encoding."""
    print("\n" + "="*60)
    print("DEMO 3: RLE Format Import/Export")
    print("="*60)
    
    # Define a glider in RLE format
    glider_rle = """#N Glider
#C A small spaceship that moves diagonally
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!"""
    
    print("\nParsing RLE pattern (Glider)...")
    grid, metadata = RLEParser.parse(glider_rle)
    
    print(f"  Grid size: {metadata['x']} x {metadata['y']}")
    print(f"  Rule: {metadata['rule']}")
    print(f"  Cell count: {np.sum(grid)}")
    
    print("\nGlider pattern:")
    for row in grid:
        print("  " + "".join("■" if cell else "·" for cell in row))
    
    # Encode a different pattern
    print("\nEncoding a blinker pattern to RLE...")
    blinker_grid = np.array([
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ])
    
    blinker_rle = RLEEncoder.encode(
        blinker_grid,
        rule='B3/S23',
        comments=['Blinker', 'A period-2 oscillator']
    )
    
    print(blinker_rle)
    
    # Save and load from file
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    rle_file = output_dir / "blinker.rle"
    RLEEncoder.encode_to_file(blinker_grid, str(rle_file), rule='B3/S23')
    print(f"\n✓ Blinker saved to {rle_file}")
    
    # Load it back
    loaded_grid, loaded_metadata = RLEParser.parse_file(str(rle_file))
    print(f"✓ Loaded back: {loaded_metadata['x']}x{loaded_metadata['y']} grid")
    
    # Verify round-trip
    if np.array_equal(blinker_grid, loaded_grid):
        print("✓ Round-trip successful!")


def demo_heatmaps():
    """Demonstrate heatmap generation."""
    print("\n" + "="*60)
    print("DEMO 4: Heatmap Generation")
    print("="*60)
    
    # Create automaton
    automaton = HighLife(width=40, height=40)
    automaton.load_pattern("Random Soup")
    
    # Create heatmaps for different modes
    heatmap_activity = HeatmapGenerator((40, 40), mode='activity')
    heatmap_age = HeatmapGenerator((40, 40), mode='age')
    heatmap_births = HeatmapGenerator((40, 40), mode='births')
    
    print("\nSimulating 30 steps and tracking heatmaps...")
    for _ in range(30):
        grid = automaton.get_grid()
        heatmap_activity.update(grid)
        heatmap_age.update(grid)
        heatmap_births.update(grid)
        automaton.step()
    
    # Get statistics
    print("\nActivity Heatmap Statistics:")
    stats = heatmap_activity.get_statistics()
    print(f"  Max activity: {stats['max']:.2f}")
    print(f"  Mean activity: {stats['mean']:.2f}")
    print(f"  Steps tracked: {stats['steps']}")
    
    print("\nAge Heatmap Statistics:")
    stats = heatmap_age.get_statistics()
    print(f"  Max age: {stats['max']:.2f}")
    print(f"  Mean age: {stats['mean']:.2f}")
    
    print("\nBirths Heatmap Statistics:")
    stats = heatmap_births.get_statistics()
    print(f"  Max births: {stats['max']:.2f}")
    print(f"  Total birth tracking: {stats['mean']:.2f}")
    
    # Get colormaps
    colormap_hot = heatmap_activity.get_colormap_data(heatmap='hot')
    colormap_cool = heatmap_age.get_colormap_data(heatmap='cool')
    
    print(f"\n✓ Generated RGB colormaps: {colormap_hot.shape}, {colormap_cool.shape}")


def demo_symmetry():
    """Demonstrate symmetry analysis."""
    print("\n" + "="*60)
    print("DEMO 5: Symmetry Analysis")
    print("="*60)
    
    # Test various symmetric patterns
    patterns = {
        "Cross": np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ]),
        "Diagonal": np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]),
        "Square": np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]),
        "Random": np.random.randint(0, 2, size=(5, 5))
    }
    
    for name, pattern in patterns.items():
        print(f"\n{name} Pattern:")
        for row in pattern:
            print("  " + "".join("■" if cell else "·" for cell in row))
        
        # Detect symmetries
        symmetries = SymmetryAnalyzer.detect_symmetries(pattern)
        if symmetries:
            print(f"  Symmetries: {', '.join(s.value for s in symmetries)}")
        else:
            print("  Symmetries: None")
        
        # Get symmetry score
        score = SymmetryAnalyzer.get_symmetry_score(pattern)
        print(f"  Symmetry score: {score:.2f}")


def demo_pattern_analysis():
    """Demonstrate pattern analysis."""
    print("\n" + "="*60)
    print("DEMO 6: Pattern Analysis")
    print("="*60)
    
    # Create automaton with block pattern
    print("\n1. Analyzing Still Life (Block):")
    automaton = ConwayGameOfLife(width=20, height=20)
    
    # Manually create a block (still life)
    automaton.grid[5, 5] = 1
    automaton.grid[5, 6] = 1
    automaton.grid[6, 5] = 1
    automaton.grid[6, 6] = 1
    
    history = [automaton.get_grid().copy()]
    for _ in range(5):
        automaton.step()
        history.append(automaton.get_grid().copy())
    
    metrics = PatternAnalyzer.analyze_pattern(history)
    print(f"  Bounding box: {metrics.bounding_box}")
    print(f"  Cell count: {metrics.cell_count}")
    print(f"  Density: {metrics.density:.2f}")
    print(f"  Period: {metrics.period}")
    print(f"  Still life: {metrics.is_still_life}")
    print(f"  Oscillator: {metrics.is_oscillator}")
    
    # Test oscillator (blinker)
    print("\n2. Analyzing Oscillator (Blinker):")
    automaton = ConwayGameOfLife(width=20, height=20)
    
    # Manually create a blinker (period-2 oscillator)
    automaton.grid[5, 6] = 1
    automaton.grid[6, 6] = 1
    automaton.grid[7, 6] = 1
    
    history = [automaton.get_grid().copy()]
    for _ in range(10):
        automaton.step()
        history.append(automaton.get_grid().copy())
    
    metrics = PatternAnalyzer.analyze_pattern(history)
    print(f"  Period: {metrics.period}")
    print(f"  Oscillator: {metrics.is_oscillator}")
    print(f"  Spaceship: {metrics.is_spaceship}")
    
    # Find connected components
    print("\n3. Finding Connected Components:")
    automaton = ConwayGameOfLife(width=30, height=30)
    # Place multiple patterns by setting cells
    # Block 1
    automaton.grid[5, 5] = 1
    automaton.grid[5, 6] = 1
    automaton.grid[6, 5] = 1
    automaton.grid[6, 6] = 1
    # Blinker
    automaton.grid[15, 15] = 1
    automaton.grid[15, 16] = 1
    automaton.grid[15, 17] = 1
    # Block 2
    automaton.grid[5, 20] = 1
    automaton.grid[5, 21] = 1
    automaton.grid[6, 20] = 1
    automaton.grid[6, 21] = 1
    
    components = PatternAnalyzer.find_connected_components(automaton.get_grid())
    print(f"  Found {len(components)} separate components")
    for i, comp in enumerate(components, 1):
        print(f"  Component {i}: {comp.shape}, {np.sum(comp)} cells")
    
    # Population statistics
    print("\n4. Population Statistics:")
    stats = PatternAnalyzer.calculate_population_statistics(history)
    print(f"  Initial population: {stats['initial_population']}")
    print(f"  Final population: {stats['final_population']}")
    print(f"  Min population: {stats['min_population']}")
    print(f"  Max population: {stats['max_population']}")
    print(f"  Mean population: {stats['mean_population']:.1f}")
    print(f"  Population change: {stats['population_change']}")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("LifeGrid - Advanced Features Demo")
    print("Phase 8: Advanced Features")
    print("="*60)
    
    try:
        demo_statistics()
        demo_rule_discovery()
        demo_rle_format()
        demo_heatmaps()
        demo_symmetry()
        demo_pattern_analysis()
        
        print("\n" + "="*60)
        print("All demos completed successfully!")
        print("="*60)
        print("\nCheck the 'output' directory for exported files:")
        print("  - simulation_stats.csv")
        print("  - simulation_summary.csv")
        print("  - discovered_rules.txt")
        print("  - blinker.rle")
        print("  - simulation_plots.png (if matplotlib available)")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
