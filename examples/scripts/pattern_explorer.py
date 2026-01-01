#!/usr/bin/env python3
"""
Pattern Explorer Example
=========================

This example demonstrates how to use the PatternBrowser to discover
and explore the built-in pattern library.

Usage:
    python pattern_explorer.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.pattern_browser import PatternBrowser
from src.core.simulator import Simulator


def main():
    """Explore the pattern library."""
    print("=" * 60)
    print("LifeGrid - Pattern Explorer")
    print("=" * 60)
    print()
    
    browser = PatternBrowser()
    
    # Show statistics
    print("Pattern Library Statistics:")
    print("-" * 60)
    stats = browser.get_statistics()
    for key, value in stats.items():
        print(f"{key:.<40} {value}")
    print()
    
    # Search for patterns
    print("Searching for 'glider' patterns:")
    print("-" * 60)
    results = browser.search_patterns("glider")
    for pattern in results[:5]:  # Show first 5
        print(f"\nPattern: {pattern['name']}")
        print(f"Mode: {pattern['mode']}")
        if pattern.get('description'):
            print(f"Description: {pattern['description']}")
    print()
    
    # Get detailed pattern info
    print("Detailed info for 'Glider':")
    print("-" * 60)
    info = browser.get_pattern_info("Conway's Game of Life", "Glider")
    for key, value in info.items():
        print(f"{key}: {value}")
    print()
    
    # List all Conway's Game of Life patterns
    print("All Conway's Game of Life patterns:")
    print("-" * 60)
    all_patterns = browser.list_all_patterns()
    conway_patterns = [p for p in all_patterns if p['mode'] == "Conway's Game of Life"]
    for i, pattern in enumerate(conway_patterns, 1):
        print(f"{i:2d}. {pattern['name']}")
    print()
    
    # Simulate a pattern
    print("Simulating Gosper Glider Gun for 100 generations:")
    print("-" * 60)
    sim = Simulator()
    sim.initialize("Conway's Game of Life", "Gosper Glider Gun")
    print(f"Initial population: {sim.population}")
    
    sim.step(100)
    print(f"After 100 generations: {sim.population} cells alive")
    print(f"Peak population: {max(h['population'] for h in sim.history)}")
    print()
    
    print("Pattern exploration complete!")


if __name__ == "__main__":
    main()
