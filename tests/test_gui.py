# pylint: disable=duplicate-code

"""GUI-related smoke tests.

These tests exercise the Tk UI at a basic level. They will be skipped
automatically if Tk cannot initialize (e.g., no DISPLAY on Linux).
"""

from __future__ import annotations

import os

import pytest


def _can_init_tk() -> bool:
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception:
        return False


tk_available = _can_init_tk()


@pytest.mark.skipif(not tk_available, reason="Tkinter not available or no display")
def test_app_launch_and_quit() -> None:
    import tkinter as tk
    from gui.app import AutomatonApp

    root = tk.Tk()
    root.withdraw()  # don't show window during test
    app = AutomatonApp(root)
    assert app.widgets.start_button is not None
    assert app.widgets.population_canvas is not None
    assert app.widgets.cycle_label is not None
    # Close cleanly
    app._on_close()


@pytest.mark.skipif(not tk_available, reason="Tkinter not available or no display")
def test_mode_switch_updates_patterns() -> None:
    import tkinter as tk
    from gui.app import AutomatonApp

    root = tk.Tk()
    root.withdraw()
    app = AutomatonApp(root)
    app.switch_mode("Wireworld")
    # Ensure pattern combo values updated
    values = list(app.widgets.pattern_combo["values"])  # type: ignore[index]
    assert "Random Soup" in values
    app._on_close()


@pytest.mark.skipif(not tk_available, reason="Tkinter not available or no display")
def test_export_metrics_collects_rows() -> None:
    import tkinter as tk
    from gui.app import AutomatonApp

    root = tk.Tk()
    root.withdraw()
    app = AutomatonApp(root)
    # Run a few steps to populate metrics
    app.step_once()
    app.step_once()
    assert len(app.state.metrics_log) >= 2
    app._on_close()
