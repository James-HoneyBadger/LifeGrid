#!/usr/bin/env python3
"""
Undo/Redo Example
=================

This example demonstrates the undo/redo functionality of the simulator.

Usage:
    python undo_redo_example.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.simulator import Simulator


def main():
    """Demonstrate undo/redo functionality."""
    print("=" * 60)
    print("LifeGrid - Undo/Redo Example")
    print("=" * 60)
    print()
    
    # Create simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life", "Glider")
    
    print(f"Initial state:")
    print(f"  Generation: {sim.generation}")
    print(f"  Population: {sim.population}")
    print(f"  Can undo: {sim.can_undo()}")
    print(f"  Can redo: {sim.can_redo()}")
    print()
    
    # Run 10 steps
    print("Running 10 steps...")
    sim.step(10)
    print(f"After 10 steps:")
    print(f"  Generation: {sim.generation}")
    print(f"  Population: {sim.population}")
    print(f"  Can undo: {sim.can_undo()}")
    print(f"  Can redo: {sim.can_redo()}")
    print()
    
    # Undo once
    print("Undoing 1 step...")
    sim.undo()
    print(f"After undo:")
    print(f"  Generation: {sim.generation}")
    print(f"  Population: {sim.population}")
    print(f"  Can undo: {sim.can_undo()}")
    print(f"  Can redo: {sim.can_redo()}")
    print()
    
    # Redo
    print("Redoing 1 step...")
    sim.redo()
    print(f"After redo:")
    print(f"  Generation: {sim.generation}")
    print(f"  Population: {sim.population}")
    print(f"  Can undo: {sim.can_undo()}")
    print(f"  Can redo: {sim.can_redo()}")
    print()
    
    # Run more steps
    print("Running 5 more steps...")
    sim.step(5)
    print(f"After 5 more steps:")
    print(f"  Generation: {sim.generation}")
    print(f"  Population: {sim.population}")
    print()
    
    # Undo multiple times
    print("Undoing 3 times...")
    for i in range(3):
        sim.undo()
        print(f"  After undo {i+1}: Generation {sim.generation}, Population {sim.population}")
    print()
    
    # Get history summary
    print("Undo/Redo History:")
    print("-" * 60)
    history = sim.get_history_summary()
    print(f"Total states in history: {len(history)}")
    print("\nRecent history:")
    for i, state in enumerate(history[-5:], len(history)-4):
        print(f"  {i}. {state.get('action', 'Unknown')}")
    print()
    
    print("Undo/Redo example complete!")


if __name__ == "__main__":
    main()
