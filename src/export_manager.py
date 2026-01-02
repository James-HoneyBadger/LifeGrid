"""Export functionality for animations and images."""

from __future__ import annotations

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
            0: (255, 255, 255),      # Dead cell - white
            1: (0, 0, 0),            # Live cell - black
            2: (200, 200, 200),      # Inactive state - light gray
            3: (100, 100, 100),      # Intermediate state - dark gray
        },
        "dark": {
            0: (30, 30, 30),         # Dead cell - dark gray
            1: (0, 255, 0),          # Live cell - green
            2: (100, 100, 100),      # Inactive state - gray
            3: (200, 200, 200),      # Intermediate state - light gray
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

    def export_png(
            self,
            grid: np.ndarray,
            filepath: str,
            cell_size: int = 8) -> bool:
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
            height, width = grid.shape
            img_height = height * cell_size
            img_width = width * cell_size

            # Create image
            image = PILImage.new(
                'RGB', (img_width, img_height), self.COLORS[self.theme][0])
            pixels = image.load()

            # Fill pixels
            for y in range(height):
                for x in range(width):
                    cell_state = int(grid[y, x])
                    color = self.COLORS[self.theme].get(
                        cell_state, self.COLORS[self.theme][0])

                    for dy in range(cell_size):
                        for dx in range(cell_size):
                            px = x * cell_size + dx
                            py = y * cell_size + dy
                            if 0 <= px < img_width and 0 <= py < img_height:
                                pixels[px, py] = color

            image.save(filepath)
            return True
        except Exception:
            return False

    def export_gif(
        self,
        filepath: str,
        cell_size: int = 8,
        duration: int = 100,
        loop: int = 0
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
            images = []

            for grid in self.frames:
                height, width = grid.shape
                img_height = height * cell_size
                img_width = width * cell_size

                image = PILImage.new(
                    'RGB', (img_width, img_height), self.COLORS[self.theme][0])
                pixels = image.load()

                for y in range(height):
                    for x in range(width):
                        cell_state = int(grid[y, x])
                        color = self.COLORS[self.theme].get(
                            cell_state, self.COLORS[self.theme][0])

                        for dy in range(cell_size):
                            for dx in range(cell_size):
                                px = x * cell_size + dx
                                py = y * cell_size + dy
                                in_bounds = (
                                    0 <= px < img_width
                                    and 0 <= py < img_height
                                )
                                if in_bounds:
                                    pixels[px, py] = color

                images.append(image)

            if images:
                images[0].save(
                    filepath,
                    save_all=True,
                    append_images=images[1:],
                    duration=duration,
                    loop=loop,
                    optimize=False
                )
                return True

            return False
        except Exception:
            return False

    def export_json(self, filepath: str, grid: np.ndarray,
                    metadata: Optional[dict] = None) -> bool:
        """Export grid as JSON.

        Args:
            filepath: Path to save JSON file
            grid: 2D numpy array
            metadata: Optional metadata to include

        Returns:
            True if successful
        """
        import json

        try:
            data = {
                "grid": grid.tolist(),
                "width": grid.shape[1],
                "height": grid.shape[0],
            }

            if metadata:
                data.update(metadata)

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception:
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
