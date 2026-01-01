#!/usr/bin/env python3
"""
Basic Simulator Example
========================

This example demonstrates the basic usage of the LifeGrid core simulator.
Run a simple Conway's Game of Life simulation and print statistics.

Usage:
    python basic_simulator.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.simulator import Simulator


def main():
    """Run a basic simulation."""
    print("=" * 60)
    print("LifeGrid - Basic Simulator Example")
    print("=" * 60)
    print()
    
    # Create simulator
    print("Creating simulator...")
    sim = Simulator()
    
    # Initialize with Conway's Game of Life and a glider pattern
    print("Initializing Conway's Game of Life with Glider pattern...")
    sim.initialize("Conway's Game of Life", "Glider")
    print(f"Grid size: {sim.config.width}x{sim.config.height}")
    print(f"Initial population: {sim.population}")
    print()
    
    # Run simulation for 100 generations
    print("Running simulation for 100 generations...")
    sim.step(100)
    print(f"Generation: {sim.generation}")
    print(f"Current population: {sim.population}")
    print()
    
    # Get metrics summary
    print("Simulation Metrics:")
    print("-" * 60)
    metrics = sim.get_metrics_summary()
    for key, value in metrics.items():
        print(f"{key:.<40} {value}")
    print()
    
    print("Simulation complete!")


if __name__ == "__main__":
    main()
