"""Tests for UI enhancements (Phase 4)."""

from __future__ import annotations

import pytest

from ui_enhancements import (
    ThemeManager,
    KeyboardShortcuts,
    Tooltips,
    SpeedPresets,
)


class TestThemeManager:
    """Test theme management."""

    def test_theme_manager_initialization(self) -> None:
        """Test theme manager initializes."""
        manager = ThemeManager()
        assert manager.current_theme == "light"

    def test_set_theme(self) -> None:
        """Test setting theme."""
        manager = ThemeManager()
        result = manager.set_theme("dark")
        
        assert result is True
        assert manager.current_theme == "dark"

    def test_set_invalid_theme(self) -> None:
        """Test setting invalid theme."""
        manager = ThemeManager()
        result = manager.set_theme("nonexistent")
        
        assert result is False
        assert manager.current_theme == "light"

    def test_get_theme(self) -> None:
        """Test getting current theme."""
        manager = ThemeManager("dark")
        assert manager.get_theme() == "dark"

    def test_get_colors(self) -> None:
        """Test getting color palette."""
        manager = ThemeManager("light")
        colors = manager.get_colors()
        
        assert isinstance(colors, dict)
        assert "bg" in colors
        assert "fg" in colors
        assert "accent" in colors

    def test_get_specific_color(self) -> None:
        """Test getting specific color."""
        manager = ThemeManager()
        color = manager.get_color("accent")
        
        assert isinstance(color, str)
        assert color.startswith("#")

    def test_available_themes(self) -> None:
        """Test listing available themes."""
        manager = ThemeManager()
        themes = manager.available_themes()
        
        assert len(themes) >= 2
        assert "light" in themes
        assert "dark" in themes

    def test_theme_callback(self) -> None:
        """Test theme change callback."""
        manager = ThemeManager()
        called_with = []
        
        def callback(theme: str) -> None:
            called_with.append(theme)
        
        manager.set_on_theme_changed(callback)
        manager.set_theme("dark")
        
        assert called_with == ["dark"]

    def test_dark_theme_colors(self) -> None:
        """Test dark theme has appropriate colors."""
        manager = ThemeManager("dark")
        colors = manager.get_colors()
        
        # Dark background
        assert colors["bg"] != colors["fg"]
        assert colors["cell_alive"] != colors["cell_dead"]


class TestKeyboardShortcuts:
    """Test keyboard shortcuts."""

    def test_shortcuts_initialization(self) -> None:
        """Test shortcuts initialize with defaults."""
        shortcuts = KeyboardShortcuts()
        assert shortcuts.get_shortcut("play_pause") == "space"

    def test_get_shortcut(self) -> None:
        """Test getting a shortcut."""
        shortcuts = KeyboardShortcuts()
        shortcut = shortcuts.get_shortcut("save")
        
        assert shortcut == "Ctrl+S"

    def test_set_shortcut(self) -> None:
        """Test setting a shortcut."""
        shortcuts = KeyboardShortcuts()
        result = shortcuts.set_shortcut("save", "Ctrl+Shift+S")
        
        assert result is True
        assert shortcuts.get_shortcut("save") == "Ctrl+Shift+S"

    def test_set_invalid_shortcut(self) -> None:
        """Test setting shortcut for invalid action."""
        shortcuts = KeyboardShortcuts()
        result = shortcuts.set_shortcut("nonexistent_action", "X")
        
        assert result is False

    def test_reset_shortcuts(self) -> None:
        """Test resetting shortcuts to defaults."""
        shortcuts = KeyboardShortcuts()
        shortcuts.set_shortcut("save", "X")
        
        shortcuts.reset_shortcuts()
        assert shortcuts.get_shortcut("save") == "Ctrl+S"

    def test_get_all_shortcuts(self) -> None:
        """Test getting all shortcuts."""
        shortcuts = KeyboardShortcuts()
        all_shortcuts = shortcuts.get_all_shortcuts()
        
        assert isinstance(all_shortcuts, dict)
        assert len(all_shortcuts) > 0
        assert "play_pause" in all_shortcuts


class TestTooltips:
    """Test tooltip system."""

    def test_get_tooltip(self) -> None:
        """Test getting tooltip text."""
        tooltip = Tooltips.get_tooltip("start_button")
        assert isinstance(tooltip, str)
        assert len(tooltip) > 0

    def test_get_nonexistent_tooltip(self) -> None:
        """Test getting nonexistent tooltip."""
        tooltip = Tooltips.get_tooltip("nonexistent")
        assert tooltip is None

    def test_get_all_tooltips(self) -> None:
        """Test getting all tooltips."""
        tooltips = Tooltips.get_all_tooltips()
        
        assert isinstance(tooltips, dict)
        assert len(tooltips) > 0
        assert "start_button" in tooltips

    def test_add_custom_tooltip(self) -> None:
        """Test adding custom tooltip."""
        custom_element = "custom_control"
        Tooltips.add_custom_tooltip(custom_element, "Custom tooltip text")
        
        tooltip = Tooltips.get_tooltip(custom_element)
        assert tooltip == "Custom tooltip text"

    def test_tooltip_completeness(self) -> None:
        """Test that all common elements have tooltips."""
        important_elements = [
            "start_button", "step_button", "clear_button",
            "speed_slider", "pattern_dropdown", "export_button"
        ]
        
        for element in important_elements:
            tooltip = Tooltips.get_tooltip(element)
            assert tooltip is not None
            assert len(tooltip) > 0


class TestSpeedPresets:
    """Test speed presets."""

    def test_get_preset(self) -> None:
        """Test getting speed preset."""
        speed = SpeedPresets.get_preset("normal")
        assert speed == 50

    def test_all_default_presets(self) -> None:
        """Test all default presets exist."""
        presets = ["slow", "normal", "fast", "very_fast"]
        
        for preset in presets:
            speed = SpeedPresets.get_preset(preset)
            assert speed is not None
            assert 1 <= speed <= 255

    def test_preset_ordering(self) -> None:
        """Test presets are in increasing order."""
        slow_speed = SpeedPresets.get_preset("slow")
        normal_speed = SpeedPresets.get_preset("normal")
        fast_speed = SpeedPresets.get_preset("fast")
        
        assert slow_speed < normal_speed < fast_speed

    def test_get_all_presets(self) -> None:
        """Test getting all presets."""
        presets = SpeedPresets.get_all_presets()
        
        assert isinstance(presets, dict)
        assert len(presets) >= 4

    def test_get_nonexistent_preset(self) -> None:
        """Test getting nonexistent preset."""
        speed = SpeedPresets.get_preset("nonexistent")
        assert speed is None

    def test_add_custom_preset(self) -> None:
        """Test adding custom preset."""
        SpeedPresets.add_preset("ultra_fast", 200)
        speed = SpeedPresets.get_preset("ultra_fast")
        
        assert speed == 200

    def test_add_invalid_preset(self) -> None:
        """Test adding invalid preset (out of range)."""
        original_presets = SpeedPresets.get_all_presets()
        
        SpeedPresets.add_preset("invalid", 500)  # Too high
        
        new_presets = SpeedPresets.get_all_presets()
        assert new_presets == original_presets
