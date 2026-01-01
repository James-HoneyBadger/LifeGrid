#!/usr/bin/env python3
"""
Export Example
==============

This example demonstrates how to export simulations as PNG snapshots,
GIF animations, and JSON patterns.

Usage:
    python export_example.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.core.simulator import Simulator
from src.export_manager import ExportManager


def main():
    """Demonstrate export functionality."""
    print("=" * 60)
    print("LifeGrid - Export Example")
    print("=" * 60)
    print()
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize simulator
    print("Setting up simulation...")
    sim = Simulator()
    sim.initialize("Conway's Game of Life", "Glider")
    
    # Export PNG snapshot (initial state)
    print("\n1. Exporting PNG snapshot...")
    export = ExportManager(theme="dark")
    png_path = os.path.join(output_dir, "glider_initial.png")
    
    try:
        export.export_png(sim.get_grid(), png_path, cell_size=4)
        print(f"   ✓ Saved to {png_path}")
    except ImportError:
        print("   ⚠ PIL/Pillow not installed. Skipping PNG export.")
        print("   Install with: pip install Pillow")
    
    # Create GIF animation
    print("\n2. Creating GIF animation...")
    export.clear_frames()  # Clear any existing frames
    
    # Collect 50 frames
    for i in range(50):
        export.add_frame(sim.get_grid())
        sim.step()
    
    gif_path = os.path.join(output_dir, "glider_animation.gif")
    try:
        export.export_gif(gif_path, duration=100, loop=0)
        print(f"   ✓ Saved to {gif_path}")
        print(f"   Animation: 50 frames at 100ms/frame")
    except ImportError:
        print("   ⚠ PIL/Pillow not installed. Skipping GIF export.")
        print("   Install with: pip install Pillow")
    
    # Export pattern as JSON
    print("\n3. Exporting pattern as JSON...")
    json_path = os.path.join(output_dir, "glider_pattern.json")
    metadata = {
        "name": "Glider",
        "author": "John Conway",
        "description": "A small spaceship that moves diagonally",
        "generation": sim.generation,
        "population": sim.population
    }
    export.export_json(json_path, sim.get_grid(), metadata)
    print(f"   ✓ Saved to {json_path}")
    
    # Export with light theme
    print("\n4. Exporting PNG with light theme...")
    export_light = ExportManager(theme="light")
    png_light_path = os.path.join(output_dir, "glider_light.png")
    
    try:
        export_light.export_png(sim.get_grid(), png_light_path, cell_size=4)
        print(f"   ✓ Saved to {png_light_path}")
    except ImportError:
        print("   ⚠ PIL/Pillow not installed. Skipping PNG export.")
    
    print("\n" + "=" * 60)
    print(f"All exports saved to: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
