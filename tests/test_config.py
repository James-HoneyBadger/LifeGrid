"""Tests for configuration and plugin systems."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from config_manager import AppConfig
from plugin_system import PluginManager, AutomatonPlugin
from automata import CellularAutomaton


class TestAppConfig:
    """Test application configuration."""

    def test_default_config(self) -> None:
        """Test default configuration values."""
        config = AppConfig()
        assert config.window_width == 1200
        assert config.window_height == 800
        assert config.grid_width == 100
        assert config.grid_height == 100
        assert config.cell_size == 8

    def test_config_save_load(self) -> None:
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            
            config = AppConfig(
                window_width=1600,
                grid_width=150,
                theme="dark"
            )
            config.save(str(config_file))
            
            loaded_config = AppConfig.load(str(config_file))
            assert loaded_config.window_width == 1600
            assert loaded_config.grid_width == 150
            assert loaded_config.theme == "dark"

    def test_config_to_dict(self) -> None:
        """Test converting config to dictionary."""
        config = AppConfig(window_width=1024, speed=75)
        data = config.to_dict()
        
        assert data["window_width"] == 1024
        assert data["speed"] == 75
        assert isinstance(data, dict)

    def test_config_from_dict(self) -> None:
        """Test creating config from dictionary."""
        data = {
            "window_width": 800,
            "window_height": 600,
            "grid_width": 75,
            "speed": 100,
        }
        config = AppConfig.from_dict(data)
        
        assert config.window_width == 800
        assert config.window_height == 600
        assert config.grid_width == 75
        assert config.speed == 100

    def test_config_load_nonexistent_file(self) -> None:
        """Test loading from nonexistent file returns defaults."""
        config = AppConfig.load("/nonexistent/path/config.json")
        assert config.window_width == 1200
        assert config.theme == "light"

    def test_config_creates_directory(self) -> None:
        """Test saving creates parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "subdir" / "config.json"
            
            config = AppConfig()
            config.save(str(config_file))
            
            assert config_file.exists()
            assert config_file.parent.exists()


class TestPluginManager:
    """Test plugin system."""

    def test_plugin_manager_initialization(self) -> None:
        """Test plugin manager initializes correctly."""
        manager = PluginManager()
        assert len(manager.plugins) == 0
        assert len(manager.list_plugins()) == 0

    def test_register_plugin(self) -> None:
        """Test registering a plugin."""
        manager = PluginManager()
        
        class TestPlugin(AutomatonPlugin):
            @property
            def name(self) -> str:
                return "TestAutomaton"
            
            @property
            def description(self) -> str:
                return "A test automaton"
            
            @property
            def version(self) -> str:
                return "1.0.0"
            
            def create_automaton(self, width: int, height: int) -> CellularAutomaton:
                from automata import ConwayGameOfLife
                return ConwayGameOfLife(width, height)
        
        plugin = TestPlugin()
        manager.register_plugin(plugin)
        
        assert "TestAutomaton" in manager.list_plugins()
        assert manager.get_plugin("TestAutomaton") is not None

    def test_create_automaton_from_plugin(self) -> None:
        """Test creating automaton from plugin."""
        manager = PluginManager()
        
        class SimplePlugin(AutomatonPlugin):
            @property
            def name(self) -> str:
                return "Simple"
            
            @property
            def description(self) -> str:
                return "Simple test"
            
            @property
            def version(self) -> str:
                return "1.0"
            
            def create_automaton(self, width: int, height: int) -> CellularAutomaton:
                from automata import ConwayGameOfLife
                return ConwayGameOfLife(width, height)
        
        manager.register_plugin(SimplePlugin())
        automaton = manager.create_automaton("Simple", 100, 100)
        
        assert automaton is not None
        assert automaton.width == 100
        assert automaton.height == 100

    def test_get_nonexistent_plugin(self) -> None:
        """Test getting nonexistent plugin returns None."""
        manager = PluginManager()
        assert manager.get_plugin("NonExistent") is None

    def test_create_automaton_nonexistent_plugin(self) -> None:
        """Test creating automaton from nonexistent plugin."""
        manager = PluginManager()
        result = manager.create_automaton("NonExistent", 100, 100)
        assert result is None

    def test_load_plugins_from_empty_directory(self) -> None:
        """Test loading from empty directory."""
        manager = PluginManager()
        with tempfile.TemporaryDirectory() as tmpdir:
            count = manager.load_plugins_from_directory(tmpdir)
            assert count == 0

    def test_load_plugins_nonexistent_directory(self) -> None:
        """Test loading from nonexistent directory."""
        manager = PluginManager()
        count = manager.load_plugins_from_directory("/nonexistent/path")
        assert count == 0

    def test_list_plugins(self) -> None:
        """Test listing registered plugins."""
        manager = PluginManager()
        
        class Plugin1(AutomatonPlugin):
            @property
            def name(self) -> str:
                return "Plugin1"
            @property
            def description(self) -> str:
                return "First"
            @property
            def version(self) -> str:
                return "1.0"
            def create_automaton(self, w: int, h: int) -> CellularAutomaton:
                from automata import ConwayGameOfLife
                return ConwayGameOfLife(w, h)
        
        class Plugin2(AutomatonPlugin):
            @property
            def name(self) -> str:
                return "Plugin2"
            @property
            def description(self) -> str:
                return "Second"
            @property
            def version(self) -> str:
                return "1.0"
            def create_automaton(self, w: int, h: int) -> CellularAutomaton:
                from automata import ConwayGameOfLife
                return ConwayGameOfLife(w, h)
        
        manager.register_plugin(Plugin1())
        manager.register_plugin(Plugin2())
        
        plugins = manager.list_plugins()
        assert len(plugins) == 2
        assert "Plugin1" in plugins
        assert "Plugin2" in plugins
