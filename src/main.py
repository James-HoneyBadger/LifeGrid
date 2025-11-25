#!/usr/bin/env python3
"""Application entry point for the cellular automaton simulator."""

from __future__ import annotations

import sys


def check_dependencies() -> None:
    """Verify that all required Python packages are installed."""
    missing = []
    
    try:
        import tkinter
    except ImportError:
        missing.append("tkinter (usually bundled with Python)")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    try:
        import scipy
    except ImportError:
        missing.append("scipy")
    
    try:
        import PIL
    except ImportError:
        missing.append("Pillow")
    
    if missing:
        print("Error: Missing required Python packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install them using:")
        print("  pip install -r requirements.txt")
        print("\nFor tkinter, ensure you have Python with Tk support installed.")
        sys.exit(1)


def main() -> None:
    """Start the Tkinter event loop."""
    check_dependencies()
    from gui.app import launch
    launch()


if __name__ == "__main__":
    main()

