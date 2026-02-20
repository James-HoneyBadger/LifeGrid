"""Rendering utilities for drawing grids and applying symmetry."""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

import numpy as np

from .config import CELL_COLORS

try:
    from PIL import Image as _PILImage, ImageTk as _ImageTk

    _PIL_AVAILABLE = True
except ImportError:
    _PILImage = None  # type: ignore[assignment]
    _ImageTk = None  # type: ignore[assignment]
    _PIL_AVAILABLE = False

# Module-level cache so we don't recreate the PhotoImage every frame
_photo_cache: Optional[object] = None


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    """Convert a '#rrggbb' or '#rgb' string to an (R, G, B) tuple."""
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join(c * 2 for c in color)
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def _draw_pil_fast(
    canvas,
    grid: np.ndarray,
    cell_size: int,
    colors: dict[int, str],
) -> None:
    """Fast single-image render via Pillow (one canvas.create_image call)."""
    global _photo_cache  # pylint: disable=global-statement

    height, width = grid.shape
    img_w = width * cell_size
    img_h = height * cell_size

    # Build an RGB pixel array from the grid
    rgb = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    for state, hex_color in colors.items():
        try:
            r, g, b = _hex_to_rgb(hex_color)
        except (ValueError, AttributeError):
            continue
        mask = grid == state
        if not mask.any():
            continue
        # Expand to pixel space using numpy repeat
        mask_pixels = np.repeat(
            np.repeat(mask, cell_size, axis=0), cell_size, axis=1
        )
        rgb[mask_pixels] = (r, g, b)

    image = _PILImage.fromarray(rgb, mode="RGB")
    _photo_cache = _ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=_photo_cache)


def draw_grid(
    canvas,
    grid: np.ndarray,
    cell_size: int,
    show_grid: bool,
    colors: dict[int, str] | None = None,
    grid_line_color: str = "gray",
    geometry: str = "square",
) -> None:
    """Render the automaton grid to the canvas.

    Uses a fast Pillow-based path when PIL is available and grid-lines are
    disabled, falling back to per-cell Tkinter rectangles otherwise.
    """

    if geometry == "hexagonal":
        _draw_hex_grid(
            canvas, grid, cell_size, show_grid, colors, grid_line_color
        )
        return

    height, width = grid.shape
    canvas.delete("all")
    scroll_region = (0, 0, width * cell_size, height * cell_size)
    canvas.configure(scrollregion=scroll_region)

    active_colors: dict[int, str] = colors if colors else CELL_COLORS

    # Fast path: Pillow composite image (no grid lines)
    if _PIL_AVAILABLE and not show_grid and cell_size >= 1:
        try:
            _draw_pil_fast(canvas, grid, cell_size, active_colors)
            return
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Fall through to slow path on any PIL error

    # Slow path: one Tkinter rectangle per cell
    outline = grid_line_color if show_grid else ""
    for y in range(height):
        for x in range(width):
            x1 = x * cell_size
            y1 = y * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            color = active_colors.get(int(grid[y, x]), "white")
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=outline,
                width=1,
            )


def _draw_hex_grid(
    canvas,
    grid: np.ndarray,
    cell_size: int,
    show_grid: bool,
    colors: dict[int, str] | None,
    grid_line_color: str,
) -> None:
    """Render a hexagonal grid (pointy-topped, odd-r)."""
    height, width = grid.shape
    canvas.delete("all")

    # Calculate geometric constants
    # Assume cell_size is the "width" of the hexagon (flat to flat)
    # Radius (center to corner)
    radius = cell_size / math.sqrt(3)
    hex_height = 2 * radius

    # Spacing
    col_spacing = cell_size
    row_spacing = 1.5 * radius

    scroll_width = width * col_spacing + (cell_size / 2)
    scroll_height = height * row_spacing + (hex_height / 4)
    canvas.configure(scrollregion=(0, 0, scroll_width, scroll_height))

    active_colors = colors if colors else CELL_COLORS
    outline = grid_line_color if show_grid else ""
    width_opts = {"width": 1} if show_grid else {"width": 0}

    # Pre-calculate vertex offsets
    angles = [math.radians(30 + 60 * i) for i in range(6)]
    offsets = [(radius * math.cos(a), radius * math.sin(a)) for a in angles]

    for y in range(height):
        y_pos = y * row_spacing + radius  # +radius to center vertically

        # Odd-r offset: shift odd rows right by half width
        x_shift = (cell_size / 2) if (y % 2) else 0

        for x in range(width):
            if grid[y, x] == 0 and not show_grid:
                continue

            x_pos = (
                x * col_spacing + x_shift + (cell_size / 2)
            )  # +half width center

            # Calculate vertices
            points = []
            for dx, dy in offsets:
                points.extend([x_pos + dx, y_pos + dy])

            color = active_colors.get(int(grid[y, x]), "white")

            # Only draw dead cells if grid is shown (optimization)
            if grid[y, x] != 0 or show_grid:
                canvas.create_polygon(
                    points, fill=color, outline=outline, **width_opts
                )


def symmetry_positions(
    x: int,
    y: int,
    grid_width: int,
    grid_height: int,
    symmetry: str,
) -> List[Tuple[int, int]]:
    """Return the list of coordinates affected by the symmetry mode."""

    positions = {(x, y)}
    if symmetry in ("Horizontal", "Both"):
        positions.add((grid_width - 1 - x, y))
    if symmetry in ("Vertical", "Both"):
        positions.add((x, grid_height - 1 - y))
    if symmetry == "Both":
        positions.add((grid_width - 1 - x, grid_height - 1 - y))
    if symmetry == "Radial":
        cx, cy = grid_width // 2, grid_height // 2
        dx, dy = x - cx, y - cy
        radial = {
            (cx + dx, cy + dy),
            (cx - dx, cy - dy),
            (cx - dy, cy + dx),
            (cx + dy, cy - dx),
        }
        positions.update(radial)
    return list(positions)
