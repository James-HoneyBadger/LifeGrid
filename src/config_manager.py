"""Configuration management for the application.

This replaces hardcoded settings with a proper dataclass-based approach.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class AppConfig:
    """Main application configuration.

    Centralizes configuration management without depending on the GUI layer.
    """

    # Window settings
    window_width: int = 1200
    window_height: int = 800
    window_title: str = "LifeGrid"

    # Grid settings
    grid_width: int = 100
    grid_height: int = 100

    # Display settings
    cell_size: int = 8
    show_grid: bool = True
    show_stats: bool = True

    # Simulation settings
    speed: int = 50
    automaton_mode: str = "Conway's Game of Life"
    default_pattern: str = "Random Soup"

    # Export settings
    export_format: str = "png"
    export_quality: int = 95

    # Theme settings
    theme: str = "light"

    # Feature flags
    enable_animations: bool = True
    enable_shortcuts: bool = True
    enable_tooltips: bool = True

    # Paths
    patterns_dir: str = "patterns"
    exports_dir: str = "exports"

    @classmethod
    def load(cls, filepath: Optional[str] = None) -> AppConfig:
        """Load configuration from file.

        Args:
            filepath: Path to config file, or use default settings.json

        Returns:
            AppConfig instance
        """
        if filepath is None:
            filepath = "settings.json"

        config_path = Path(filepath)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                return cls(**{k: v for k, v in data.items()
                           if k in cls.__dataclass_fields__})
            except (json.JSONDecodeError, KeyError):
                return cls()

        return cls()

    def save(self, filepath: Optional[str] = None) -> None:
        """Save configuration to file.

        Args:
            filepath: Path to config file, or use default settings.json
        """
        if filepath is None:
            filepath = "settings.json"

        config_path = Path(filepath)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            json.dump(asdict(self), f, indent=2)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> AppConfig:
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items()
                   if k in cls.__dataclass_fields__})
