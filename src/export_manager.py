"""Export functionality for animations and images."""

from __future__ import annotations

import json
from typing import Optional

import numpy as np

try:
    from PIL import Image as PILImage

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ExportManager:
    """Manages exporting simulations in various formats.

    Supports PNG snapshots, GIF animations, and other formats.
    """

    # Color mapping for different cell states
    COLORS = {
        "light": {
            0: (255, 255, 255),  # Dead cell - white
            1: (0, 0, 0),  # Live cell - black
            2: (200, 200, 200),  # Inactive state - light gray
            3: (100, 100, 100),  # Intermediate state - dark gray
        },
        "dark": {
            0: (30, 30, 30),  # Dead cell - dark gray
            1: (0, 255, 0),  # Live cell - green
            2: (100, 100, 100),  # Inactive state - gray
            3: (200, 200, 200),  # Intermediate state - light gray
        },
    }

    def __init__(self, theme: str = "light") -> None:
        """Initialize export manager.

        Args:
            theme: Color theme to use ("light" or "dark")
        """
        if not PIL_AVAILABLE:
            raise RuntimeError("Pillow is required for export functionality")

        self.theme = theme
        self.frames: list[np.ndarray] = []

    def add_frame(self, grid: np.ndarray) -> None:
        """Add a grid frame to animation.

        Args:
            grid: 2D numpy array representing the grid
        """
        self.frames.append(np.copy(grid))

    def clear_frames(self) -> None:
        """Clear all stored frames."""
        self.frames.clear()

    def _grid_to_image(
        self, grid: np.ndarray, cell_size: int
    ) -> PILImage.Image:
        """Convert grid to PIL Image.

        Args:
            grid: 2D numpy array
            cell_size: Size of each cell in pixels

        Returns:
            PIL Image object
        """
        height, width = grid.shape

        # Create small image first
        image = PILImage.new(
            "RGB", (width, height), self.COLORS[self.theme][0]
        )
        pixels = image.load()
        if pixels is None:
            raise ValueError("Failed to obtain pixel access")

        # Fill pixels (only live ones need update if background is set)
        live_indices = np.argwhere(grid > 0)
        for y, x in live_indices:
            color = self.COLORS[self.theme].get(
                int(grid[y, x]), self.COLORS[self.theme][0]
            )
            pixels[x, y] = color

        # Scale up if needed
        if cell_size > 1:
            img_width = width * cell_size
            img_height = height * cell_size
            # pylint: disable=no-member
            image = image.resize(
                (img_width, img_height), resample=PILImage.Resampling.NEAREST
            )

        return image

    def export_png(
        self, grid: np.ndarray, filepath: str, cell_size: int = 8
    ) -> bool:
        """Export a single grid as PNG.

        Args:
            grid: 2D numpy array
            filepath: Path to save PNG file
            cell_size: Size of each cell in pixels

        Returns:
            True if successful
        """
        if not PIL_AVAILABLE or not PILImage:
            return False

        try:
            image = self._grid_to_image(grid, cell_size)
            image.save(filepath)
            return True
        except (OSError, ValueError):
            return False

    def export_gif(
        self,
        filepath: str,
        cell_size: int = 8,
        duration: int = 100,
        loop: int = 0,
    ) -> bool:
        """Export frames as animated GIF.

        Args:
            filepath: Path to save GIF file
            cell_size: Size of each cell in pixels
            duration: Duration per frame in milliseconds
            loop: Number of loops (0 = infinite)

        Returns:
            True if successful
        """
        if not PIL_AVAILABLE or not PILImage or not self.frames:
            return False

        try:
            images = [
                self._grid_to_image(grid, cell_size) for grid in self.frames
            ]

            if images:
                images[0].save(
                    filepath,
                    save_all=True,
                    append_images=images[1:],
                    duration=duration,
                    loop=loop,
                    optimize=False,
                )
                return True
            return False
        except (OSError, ValueError):
            return False

    def export_json(
        self, filepath: str, grid: np.ndarray, metadata: Optional[dict] = None
    ) -> bool:
        """Export grid as JSON.

        Args:
            filepath: Path to save JSON file
            grid: 2D numpy array
            metadata: Optional metadata to include

        Returns:
            True if successful
        """

        try:
            data = {
                "grid": grid.tolist(),
                "width": grid.shape[1],
                "height": grid.shape[0],
            }

            if metadata:
                data.update(metadata)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True
        except (OSError, TypeError):
            return False

    def get_supported_formats(self) -> list[str]:
        """Get list of supported export formats.

        Returns:
            List of format strings
        """
        formats = ["json"]
        if PIL_AVAILABLE:
            formats.extend(["png", "gif"])
        return formats

    def is_format_supported(self, format_str: str) -> bool:
        """Check if a format is supported.

        Args:
            format_str: Format identifier

        Returns:
            True if supported
        """
        return format_str.lower() in self.get_supported_formats()
