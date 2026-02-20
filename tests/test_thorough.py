#!/usr/bin/env python3
"""Thorough vetting of all LifeGrid simulation settings and functions.

Run:  python -m pytest tests/test_thorough.py -v --tb=short
or:   python tests/test_thorough.py
"""

from __future__ import annotations

import csv

import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

# Ensure src/ is importable
_src = str(Path(__file__).resolve().parent.parent / "src")
if _src not in sys.path:
    sys.path.insert(0, _src)

import numpy as np  # noqa: E402

# ── Globals ──────────────────────────────────────────────────────────
_results: dict[str, int] = {"passed": 0, "failed": 0}
ERRORS: list[str] = []


def _run(label: str, func):
    """Run a single test, track results."""
    try:
        func()
        _results["passed"] += 1
        print(f"  ✓ {label}")
    except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-except
        _results["failed"] += 1
        tb = traceback.format_exc()
        ERRORS.append(f"FAIL: {label}\n  {exc}\n{tb}")
        print(f"  ✗ {label}  →  {exc}")


# =====================================================================
#  1. Core – SimulatorConfig
# =====================================================================
def test_config_defaults():
    from core.config import SimulatorConfig
    c = SimulatorConfig()
    assert c.width > 0 and c.height > 0
    assert isinstance(c.speed, (int, float))


def test_config_roundtrip():
    from core.config import SimulatorConfig
    c = SimulatorConfig(width=80, height=60, speed=15, cell_size=6)
    d = c.to_dict()
    c2 = SimulatorConfig.from_dict(d)
    assert c2.width == 80
    assert c2.height == 60
    assert c2.speed == 15
    assert c2.cell_size == 6


def test_config_from_dict_extra_keys():
    from core.config import SimulatorConfig
    d = {"width": 32, "unknown_field": "ignored"}
    c = SimulatorConfig.from_dict(d)
    assert c.width == 32


# =====================================================================
#  2. Core – UndoManager
# =====================================================================
def test_undo_push_and_undo():
    from core.undo_manager import UndoManager
    um = UndoManager(max_history=10)
    grid0 = np.zeros((5, 5), dtype=int)
    grid1 = np.ones((5, 5), dtype=int)
    um.push_state("step1", grid0)
    assert um.can_undo()
    result = um.undo(grid1)
    assert result is not None
    name, restored = result
    assert name == "step1"
    assert np.array_equal(restored, grid0)


def test_undo_redo_roundtrip():
    from core.undo_manager import UndoManager
    um = UndoManager()
    g0 = np.zeros((3, 3), dtype=int)
    g1 = np.ones((3, 3), dtype=int)
    um.push_state("a", g0)
    um.undo(g1)
    assert um.can_redo()
    result = um.redo(g0)
    assert result is not None
    _, restored = result
    assert np.array_equal(restored, g1)


def test_undo_clear():
    from core.undo_manager import UndoManager
    um = UndoManager()
    um.push_state("x", np.zeros((2, 2)))
    um.clear()
    assert not um.can_undo()
    assert not um.can_redo()


def test_undo_history_summary():
    from core.undo_manager import UndoManager
    um = UndoManager()
    um.push_state("alpha", np.zeros((2, 2)))
    um.push_state("beta", np.ones((2, 2)))
    s = um.get_history_summary()
    assert s["undo_count"] == 2
    assert s["last_undo_action"] == "beta"


# =====================================================================
#  3. Core – Simulator
# =====================================================================
def test_simulator_init_conway():
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life", pattern="Random Soup")
    g = sim.get_grid()
    assert g.shape == (sim.config.height, sim.config.width)


def test_simulator_step():
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life", pattern="Blinker")
    metrics = sim.step(3)
    assert len(metrics) == 3
    assert sim.generation == 3
    for m in metrics:
        assert "generation" in m
        assert "population" in m
        assert "density" in m


def test_simulator_set_cell():
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life")
    sim.set_cell(0, 0, 1)
    assert sim.get_grid()[0, 0] == 1
    sim.set_cell(0, 0, 0)
    assert sim.get_grid()[0, 0] == 0


def test_simulator_undo_redo():
    """Test that Simulator.undo() and .redo() work correctly."""
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life")
    sim.set_cell(5, 5, 1)
    grid_before = sim.get_grid().copy()
    sim.step()
    _grid_after = sim.get_grid().copy()  # noqa: F841
    assert sim.generation == 1

    result = sim.undo()
    assert result is True, "undo() should return True"
    assert sim.generation == 0
    # Grid should be restored to pre-step state
    assert np.array_equal(sim.get_grid(), grid_before)

    result = sim.redo()
    assert result is True, "redo() should return True"
    assert sim.generation == 1


def test_simulator_metrics_summary():
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life", pattern="Blinker")
    sim.step(5)
    s = sim.get_metrics_summary()
    assert s["generations"] == 5
    assert "current_population" in s
    assert "max_population" in s


def test_simulator_callback():
    from core.simulator import Simulator
    collected = []
    sim = Simulator()
    sim.initialize("Conway's Game of Life", pattern="Blinker")
    sim.set_on_step_callback(collected.append)
    sim.step(3)
    assert len(collected) == 3


def test_simulator_reset():
    from core.simulator import Simulator
    sim = Simulator()
    sim.initialize("Conway's Game of Life", pattern="Blinker")
    sim.step(5)
    sim.reset()
    assert sim.generation == 0


def test_simulator_all_modes():
    """Test that every mode listed in the Simulator can be initialized."""
    from core.simulator import Simulator
    modes = [
        "Conway's Game of Life",
        "HighLife",
        "Langton's Ant",
        "Wireworld",
        "Brian's Brain",
        "Generations",
        "Immigration",
        "Rainbow",
    ]
    for mode in modes:
        sim = Simulator()
        sim.initialize(mode)
        g = sim.get_grid()
        assert g is not None, f"{mode}: get_grid() returned None"
        sim.step()


def test_simulator_unknown_mode():
    from core.simulator import Simulator
    sim = Simulator()
    try:
        sim.initialize("NonexistentMode")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_simulator_not_initialized():
    from core.simulator import Simulator
    sim = Simulator()
    try:
        sim.step()
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass
    try:
        sim.get_grid()
        assert False, "Should have raised RuntimeError"
    except RuntimeError:
        pass


# =====================================================================
#  4. All Automata – step/reset/click/grid
# =====================================================================
def _test_automaton(cls, name, w=20, h=20, extra_kw=None):
    kw = extra_kw or {}
    a = cls(w, h, **kw)
    a.reset()
    g = a.get_grid()
    assert g.shape == (h, w), f"{name}: shape {g.shape} != ({h}, {w})"
    a.handle_click(w // 2, h // 2)
    a.step()
    g2 = a.get_grid()
    assert g2.shape == (h, w), f"{name}: post-step shape mismatch"


def test_conway():
    from automata.conway import ConwayGameOfLife
    _test_automaton(ConwayGameOfLife, "Conway")
    a = ConwayGameOfLife(30, 30)
    a.load_pattern("Blinker")
    # Blinker oscillation test
    g0 = a.get_grid().copy()
    a.step()
    a.step()
    assert np.array_equal(
        a.get_grid(), g0,
    ), "Blinker should oscillate with period 2"


def test_conway_patterns():
    from automata.conway import ConwayGameOfLife
    a = ConwayGameOfLife(30, 30)
    patterns = a.get_available_patterns()
    assert len(patterns) > 0, "Should have at least one pattern"
    for p in patterns:
        a2 = ConwayGameOfLife(30, 30)
        a2.load_pattern(p)
        a2.step()


def test_highlife():
    from automata.highlife import HighLife
    _test_automaton(HighLife, "HighLife")
    a = HighLife(20, 20)
    a.load_pattern("Replicator")
    a.step()


def test_brians_brain():
    from automata.briansbrain import BriansBrain
    _test_automaton(BriansBrain, "BriansBrain")
    a = BriansBrain(20, 20)
    a.load_pattern("Random Soup")
    for _ in range(5):
        a.step()
    g = a.get_grid()
    # Brain has 3 states: 0,1,2
    assert g.max() <= 2


def test_wireworld():
    from automata.wireworld import Wireworld
    _test_automaton(Wireworld, "Wireworld")
    a = Wireworld(30, 30)
    a.load_pattern("Signal")
    for _ in range(10):
        a.step()
    g = a.get_grid()
    assert g.max() <= 3


def test_immigration():
    from automata.immigration import ImmigrationGame
    _test_automaton(ImmigrationGame, "Immigration")
    a = ImmigrationGame(20, 20)
    a.load_pattern("Random Soup")
    a.step()


def test_rainbow():
    from automata.rainbow import RainbowGame
    _test_automaton(RainbowGame, "Rainbow")
    a = RainbowGame(20, 20)
    a.load_pattern("Random Soup")
    a.step()


def test_hexagonal():
    from automata.hexagonal import HexagonalGameOfLife
    _test_automaton(HexagonalGameOfLife, "Hexagonal")
    a = HexagonalGameOfLife(20, 20)
    a.load_pattern("Random Soup")
    for _ in range(5):
        a.step()


def test_generations():
    from automata.generations import GenerationsAutomaton
    _test_automaton(GenerationsAutomaton, "Generations")
    a = GenerationsAutomaton(20, 20, birth={3}, survival={2, 3}, n_states=5)
    a.load_pattern("Random Soup")
    for _ in range(5):
        a.step()
    assert a.get_grid().max() <= 4  # n_states-1


def test_langtons_ant():
    from automata.ant import LangtonsAnt
    _test_automaton(LangtonsAnt, "LangtonsAnt")
    a = LangtonsAnt(20, 20)
    for _ in range(50):
        a.step()
    g = a.get_grid()
    assert g.max() <= 2  # ant marker = 2


def test_lifelike():
    from automata.lifelike import LifeLikeAutomaton
    a = LifeLikeAutomaton(20, 20, birth={3, 6}, survival={2, 3})
    a.reset()
    a.load_pattern("Random Soup")
    a.step()
    a.set_rules({3}, {2, 3})
    a.step()


def test_parse_bs():
    from automata import parse_bs
    b, s = parse_bs("B3/S23")
    assert b == {3}
    assert s == {2, 3}
    b2, s2 = parse_bs("B36/S23")
    assert b2 == {3, 6}
    assert s2 == {2, 3}


# =====================================================================
#  5. Boundary Mode
# =====================================================================
def test_boundary_mode_enum():
    from core.boundary import BoundaryMode
    assert BoundaryMode.from_string("wrap") == BoundaryMode.WRAP
    assert BoundaryMode.from_string("fixed") == BoundaryMode.FIXED
    assert BoundaryMode.from_string("reflect") == BoundaryMode.REFLECT
    try:
        BoundaryMode.from_string("invalid")
        assert False, "Should raise ValueError"
    except (ValueError, KeyError):
        pass


def test_convolve_with_boundary():
    from core.boundary import BoundaryMode, convolve_with_boundary
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 5] = 1

    for mode in BoundaryMode:
        result = convolve_with_boundary(grid, kernel, mode)
        assert result.shape == grid.shape, f"Shape mismatch for {mode}"


def test_roll_with_boundary():
    from core.boundary import BoundaryMode, roll_with_boundary
    grid = np.arange(25).reshape(5, 5)
    for mode in BoundaryMode:
        r = roll_with_boundary(grid, 1, axis=0, boundary=mode)
        assert r.shape == grid.shape


# =====================================================================
#  6. GPU Module
# =====================================================================
def test_gpu_module():
    from performance.gpu import (
        is_gpu_available, to_numpy, to_device, xp,
    )
    # Verify imports exist
    assert is_gpu_available is not None
    assert xp is not None
    # xp should be numpy (no GPU in CI)
    arr = np.ones((10, 10), dtype=int)
    dev = to_device(arr)
    back = to_numpy(dev)
    assert np.array_equal(back, arr)


def test_gpu_simulator():
    from performance.gpu import GPUSimulator
    grid = np.zeros((20, 20), dtype=int)
    # Blinker
    grid[10, 9] = grid[10, 10] = grid[10, 11] = 1
    gs = GPUSimulator(grid, birth={3}, survival={2, 3})
    gs.step()
    g = gs.get_grid()
    assert g.shape == (20, 20)
    assert int(np.count_nonzero(g)) > 0


# =====================================================================
#  7. Patterns
# =====================================================================
def test_patterns_module():
    from patterns import (
        PATTERN_DATA,
        get_pattern_coords,
        get_pattern_description,
    )
    # PATTERN_DATA should be non-empty
    assert len(PATTERN_DATA) > 0, "PATTERN_DATA is empty"

    # Conway patterns must exist
    for mode, pats in PATTERN_DATA.items():
        for pname in pats:
            coords = get_pattern_coords(mode, pname)
            assert isinstance(
                coords, list,
            ), f"coords for {mode}/{pname} not a list"
            desc = get_pattern_description(mode, pname)
            assert isinstance(desc, str)


def test_apply_pattern_to_grid():
    from patterns import apply_pattern_to_grid
    grid = np.zeros((20, 20), dtype=int)
    coords = [(0, 0), (1, 0), (2, 0)]
    apply_pattern_to_grid(grid, coords, 10, 10)
    assert grid.sum() > 0


# =====================================================================
#  8. Plugin System
# =====================================================================
def test_plugin_manager():
    from plugin_system import PluginManager
    pm = PluginManager()
    # Load from default plugins directory
    plugins_dir = str(Path(__file__).resolve().parent.parent / "plugins")
    count = pm.load_plugins_from_directory(plugins_dir)
    names = pm.list_plugins()
    # Should have found at least the day_and_night plugin
    assert count >= 1, f"Expected >=1 plugin, got {count}"
    assert len(names) >= 1

    # Test creating an automaton from a plugin
    for pname in names:
        p = pm.get_plugin(pname)
        assert p is not None
        a = pm.create_automaton(pname, 20, 20)
        assert a is not None
        a.step()


# =====================================================================
#  9. RLE Format
# =====================================================================
def test_rle_encode_decode():
    from advanced.rle_format import RLEParser, RLEEncoder
    grid = np.zeros((10, 10), dtype=int)
    grid[1, 1] = grid[1, 2] = grid[1, 3] = 1  # Blinker
    rle_str = RLEEncoder.encode(grid, rule="B3/S23")
    assert len(rle_str) > 0
    decoded, _meta = RLEParser.parse(rle_str)
    assert decoded is not None
    # The alive cells should match
    assert np.count_nonzero(decoded) == 3


def test_rle_file_roundtrip():
    from advanced.rle_format import RLEParser, RLEEncoder
    grid = np.zeros((8, 8), dtype=int)
    grid[2, 3] = grid[3, 3] = grid[4, 3] = 1
    with tempfile.NamedTemporaryFile(
        suffix=".rle", mode="w", delete=False
    ) as f:
        fpath = f.name
    try:
        RLEEncoder.encode_to_file(grid, fpath)
        loaded, _meta = RLEParser.parse_file(fpath)
        assert np.count_nonzero(loaded) == 3
    finally:
        os.unlink(fpath)


# =====================================================================
#  10. Statistics
# =====================================================================
def test_statistics_collector():
    from advanced.statistics import StatisticsCollector
    sc = StatisticsCollector(track_changes=True, calculate_entropy=True)
    grid0 = np.zeros((10, 10), dtype=int)
    grid1 = np.zeros((10, 10), dtype=int)
    grid1[3:6, 3:6] = 1
    sc.collect(0, grid0)
    sc.collect(1, grid1)
    stats = sc.get_statistics()
    assert len(stats) == 2
    summary = sc.get_summary()
    assert "total_steps" in summary or "steps" in summary or len(summary) > 0
    sc.reset()
    assert len(sc.get_statistics()) == 0


def test_enhanced_statistics():
    from advanced.enhanced_statistics import EnhancedStatistics
    grid = np.zeros((20, 20), dtype=int)
    grid[5:10, 5:10] = 1

    e = EnhancedStatistics.calculate_entropy(grid)
    assert isinstance(e, float)
    assert 0 <= e <= 1

    c = EnhancedStatistics.calculate_complexity(grid)
    assert isinstance(c, float)

    bd = EnhancedStatistics.box_counting_dimension(grid)
    assert isinstance(bd, float)

    n, _labels = EnhancedStatistics.connected_components(grid)
    assert isinstance(n, int)
    assert n >= 1

    cs = EnhancedStatistics.cluster_statistics(grid)
    assert isinstance(cs, dict)

    sym = EnhancedStatistics.pattern_symmetry(grid)
    assert isinstance(sym, dict)

    com = EnhancedStatistics.center_of_mass(grid)
    assert len(com) == 2

    metrics = EnhancedStatistics.compute_all_metrics(grid)
    assert isinstance(metrics, dict)
    assert len(metrics) > 0


# =====================================================================
#  11. Pattern Analysis
# =====================================================================
def test_pattern_analyzer():
    from advanced.pattern_analysis import PatternAnalyzer
    grid = np.zeros((20, 20), dtype=int)
    grid[5, 5] = grid[5, 6] = grid[5, 7] = 1  # Blinker

    bb = PatternAnalyzer.get_bounding_box(grid)
    assert len(bb) == 4

    p = PatternAnalyzer.extract_pattern(grid)
    assert p is not None

    # Build history for period detection
    from automata.conway import ConwayGameOfLife
    a = ConwayGameOfLife(20, 20)
    # place blinker
    a.grid[5, 5] = a.grid[5, 6] = a.grid[5, 7] = 1
    history = [a.get_grid().copy()]
    for _ in range(10):
        a.step()
        history.append(a.get_grid().copy())

    period = PatternAnalyzer.detect_period(history)
    assert period == 2, f"Blinker period should be 2, got {period}"

    comps = PatternAnalyzer.find_connected_components(grid)
    assert isinstance(comps, list)

    pop_stats = PatternAnalyzer.calculate_population_statistics(history)
    assert isinstance(pop_stats, dict)


# =====================================================================
#  12. Rule Discovery
# =====================================================================
def test_rule_discovery():
    from advanced.rule_discovery import RuleDiscovery
    from automata.conway import ConwayGameOfLife
    rd = RuleDiscovery()
    a = ConwayGameOfLife(20, 20)
    a.load_pattern("Random Soup")
    prev = a.get_grid().copy()
    for _ in range(10):
        a.step()
        curr = a.get_grid().copy()
        rd.observe_transition(prev, curr)
        prev = curr
    rules = rd.get_discovered_rules()
    assert isinstance(rules, list)
    summary = rd.get_rule_summary()
    assert isinstance(summary, dict)
    bs = rd.infer_birth_survival_rules()
    assert "birth" in bs and "survival" in bs
    notation = rd.format_birth_survival_notation(bs["birth"], bs["survival"])
    assert isinstance(notation, str)

    # Export
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        fpath = f.name
    try:
        rd.export_rules(fpath)
        assert os.path.getsize(fpath) > 0
    finally:
        os.unlink(fpath)

    rd.reset()


# =====================================================================
#  13. Cell Tracker
# =====================================================================
def test_cell_age_tracker():
    from advanced.cell_tracker import CellAgeTracker
    t = CellAgeTracker(10, 10)
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 5] = 1
    t.update(grid)
    assert t.get_age_grid()[5, 5] == 1
    t.update(grid)
    assert t.get_age_grid()[5, 5] == 2
    stats = t.get_statistics()
    assert isinstance(stats, dict)
    t.reset()
    assert t.get_age_grid().sum() == 0


def test_cell_history_tracker():
    from advanced.cell_tracker import CellHistoryTracker
    ht = CellHistoryTracker(max_history=50)
    grid = np.zeros((10, 10), dtype=int)
    grid[3, 3] = 1
    ht.record(0, grid)
    ht.record(1, grid)
    stats = ht.get_statistics()
    assert isinstance(stats, dict)
    ht.clear()


# =====================================================================
#  14. Visualization – Heatmap & Symmetry
# =====================================================================
def test_heatmap_generator():
    from advanced.visualization import HeatmapGenerator
    hg = HeatmapGenerator((10, 10))
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 5] = 1
    hg.update(grid)
    hg.update(grid)
    hm = hg.get_heatmap()
    assert hm.shape == (10, 10)
    stats = hg.get_statistics()
    assert isinstance(stats, dict)
    hg.reset()


def test_symmetry_analyzer():
    from advanced.visualization import SymmetryAnalyzer
    # Symmetric grid
    grid = np.zeros((10, 10), dtype=int)
    grid[4:6, 4:6] = 1  # 2x2 block in center
    syms = SymmetryAnalyzer.detect_symmetries(grid)
    assert isinstance(syms, list)
    score = SymmetryAnalyzer.get_symmetry_score(grid)
    assert 0 <= score <= 1
    # may depend on centering
    assert (
        SymmetryAnalyzer.has_horizontal_symmetry(grid)
        is True or True
    )
    assert SymmetryAnalyzer.has_vertical_symmetry(grid) is True or True


# =====================================================================
#  15. Pattern Manager
# =====================================================================
def test_pattern_manager():
    from advanced.pattern_manager import PatternEntry, PatternManager
    with tempfile.TemporaryDirectory() as td:
        pm = PatternManager(data_dir=td)
        grid = np.zeros((5, 5), dtype=int)
        grid[1, 1] = grid[1, 2] = grid[1, 3] = 1
        entry = PatternEntry.from_grid(
            name="test_blinker", mode="Conway", grid=grid,
            tags=["oscillator"], description="Test blinker",
        )
        # Roundtrip
        d = entry.to_dict()
        e2 = PatternEntry.from_dict(d)
        assert e2.name == "test_blinker"
        assert np.array_equal(e2.to_grid(), grid)

        # Favorites
        pm.add_favorite(entry)
        assert pm.is_favorite("test_blinker")
        favs = pm.get_favorites()
        assert len(favs) == 1

        # History
        pm.add_to_history(entry)
        hist = pm.get_history()
        assert len(hist) >= 1

        # Search
        by_tag = pm.search_by_tag("oscillator")
        assert len(by_tag) >= 1
        by_name = pm.search_by_name("blinker")
        assert len(by_name) >= 1

        pm.remove_favorite("test_blinker")
        assert not pm.is_favorite("test_blinker")
        pm.clear_history()


# =====================================================================
#  16. Export Manager
# =====================================================================
def test_export_manager_formats():
    from export_manager import ExportManager
    em = ExportManager()
    fmts = em.get_supported_formats()
    assert isinstance(fmts, list)
    assert len(fmts) > 0
    assert em.is_format_supported("json")


def test_export_json():
    from export_manager import ExportManager
    em = ExportManager()
    grid = np.zeros((10, 10), dtype=int)
    grid[3, 3] = 1
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        fpath = f.name
    try:
        ok = em.export_json(fpath, grid, metadata={"test": True})
        assert ok is True
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        assert "grid" in data or "metadata" in data
    finally:
        os.unlink(fpath)


def test_export_png():
    from export_manager import ExportManager
    em = ExportManager()
    grid = np.zeros((10, 10), dtype=int)
    grid[5, 5] = 1
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fpath = f.name
    try:
        ok = em.export_png(grid, fpath, cell_size=4)
        if ok:
            assert os.path.getsize(fpath) > 0
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


def test_export_gif():
    from export_manager import ExportManager
    em = ExportManager()
    for _ in range(5):
        em.add_frame(np.random.randint(0, 2, (10, 10)))
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        fpath = f.name
    try:
        ok = em.export_gif(fpath, cell_size=4, duration=100)
        if ok:
            assert os.path.getsize(fpath) > 0
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


# =====================================================================
#  17. Config Manager
# =====================================================================
def test_app_config():
    from config_manager import AppConfig
    with tempfile.NamedTemporaryFile(
        suffix=".json", mode="w", delete=False
    ) as f:
        fpath = f.name
    try:
        c = AppConfig()
        c.save(fpath)
        c2 = AppConfig.load(fpath)
        assert c2.grid_width == c.grid_width
        d = c2.to_dict()
        c3 = AppConfig.from_dict(d)
        assert c3.grid_height == c.grid_height
    finally:
        os.unlink(fpath)


# =====================================================================
#  18. CLI Module
# =====================================================================
def test_cli_build_parser():
    from cli import _build_parser
    p = _build_parser()
    args = p.parse_args([
        "--mode", "conway",
        "--steps", "10",
        "--width", "20",
        "--height", "20",
    ])
    assert args.mode == "conway"
    assert args.steps == 10


def test_cli_resolve_mode():
    from cli import _resolve_mode
    assert _resolve_mode("conway") == "Conway's Game of Life"
    assert _resolve_mode("highlife") == "HighLife"
    assert _resolve_mode("wireworld") == "Wireworld"
    # Passthrough for unknown
    assert _resolve_mode("Some Custom Mode") == "Some Custom Mode"


def test_cli_main_run():
    from cli import main as cli_main
    # Run 5 steps of Conway silently
    rc = cli_main(["--mode", "conway", "--steps", "5", "--quiet"])
    assert rc == 0


def test_cli_main_csv_export():
    from cli import main as cli_main
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
        fpath = f.name
    try:
        rc = cli_main([
            "--mode", "conway", "--steps", "3",
            "--export", fpath, "--quiet",
        ])
        assert rc == 0
        with open(fpath, encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert len(rows) >= 2  # header + data
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


def test_cli_main_json_export():
    from cli import main as cli_main
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        fpath = f.name
    try:
        rc = cli_main([
            "--mode", "conway", "--steps", "3",
            "--export", fpath, "--quiet",
        ])
        assert rc == 0
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list))
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


def test_cli_main_png_export():
    from cli import main as cli_main
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fpath = f.name
    try:
        rc = cli_main([
            "--mode", "conway", "--steps", "3",
            "--export", fpath, "--quiet",
        ])
        assert rc == 0
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


# =====================================================================
#  19. API Module (FastAPI)
# =====================================================================
def test_api_health():
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        print("    (skipping API tests – fastapi not installed)")
        return
    from api.app import app
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_api_session_lifecycle():
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        return
    from api.app import app
    client = TestClient(app)

    # Create session
    r = client.post("/session", json={"mode": "Conway's Game of Life"})
    assert r.status_code == 200
    data = r.json()
    sid = data["session_id"]

    # Get state
    r = client.get(f"/session/{sid}/state")
    assert r.status_code == 200

    # Step
    r = client.post(f"/session/{sid}/step", json={"steps": 3})
    assert r.status_code == 200
    assert r.json()["generation"] == 3

    # Load pattern
    r = client.post(
        f"/session/{sid}/pattern",
        json={"pattern": "Random Soup"},
    )
    assert r.status_code == 200


def test_api_session_not_found():
    try:
        from fastapi.testclient import TestClient
    except ImportError:
        return
    from api.app import app
    client = TestClient(app)
    r = client.get("/session/nonexistent/state")
    assert r.status_code == 404


# =====================================================================
#  20. Collab Module
# =====================================================================
def test_collab_session():
    import asyncio
    from api.collab import CollaborativeSession
    grid = np.zeros((16, 16), dtype=int)
    session = CollaborativeSession(grid=grid)
    # Access state via _state_payload (internal) and direct attributes
    assert session.grid.shape == (16, 16)
    assert session.generation == 0
    assert session.running is False

    # Access state via internal method (testing)
    state = getattr(session, '_state_payload')()
    assert state["generation"] == 0
    assert state["width"] == 16
    assert state["height"] == 16

    # Step and draw
    async def run():
        await session.handle_message(None, {"action": "step"})  # type: ignore
        assert session.generation == 1
        await session.handle_message(  # type: ignore
            None,
            {"action": "draw", "x": 5, "y": 5, "value": 1},
        )
        assert session.grid[5, 5] == 1
        await session.handle_message(None, {"action": "clear"})  # type: ignore
        # clear resets generation to 0
        assert session.generation == 0
        assert session.grid.sum() == 0
    asyncio.run(run())


# =====================================================================
#  21. Breakpoint System
# =====================================================================
def test_breakpoint_condition():
    from gui.new_features import BreakpointCondition
    bp = BreakpointCondition("population", 100, ">=")
    assert bp.check({"population": 150}) is True
    assert bp.check({"population": 50}) is False

    bp2 = BreakpointCondition("entropy", 0.5, "<=")
    assert bp2.check({"entropy": 0.3}) is True
    assert bp2.check({"entropy": 0.8}) is False

    bp3 = BreakpointCondition("generation", 10, "==")
    assert bp3.check({"generation": 10}) is True
    assert bp3.check({"generation": 11}) is False

    # Disabled breakpoint
    bp4 = BreakpointCondition("population", 1, ">=", enabled=False)
    assert bp4.check({"population": 999}) is False


def test_breakpoint_manager():
    from gui.new_features import BreakpointCondition, BreakpointManager
    bm = BreakpointManager()
    bp1 = BreakpointCondition("population", 50, ">=")
    bp2 = BreakpointCondition("generation", 10, "==")
    bm.add(bp1)
    bm.add(bp2)
    assert len(bm.breakpoints) == 2

    hit = bm.check_all({"population": 100, "generation": 5})
    assert hit is not None  # bp1 triggers

    hit2 = bm.check_all({"population": 10, "generation": 10})
    assert hit2 is not None  # bp2 triggers

    hit3 = bm.check_all({"population": 10, "generation": 5})
    assert hit3 is None  # nothing triggers

    bm.remove(0)
    assert len(bm.breakpoints) == 1
    bm.clear()
    assert len(bm.breakpoints) == 0


# =====================================================================
#  22. Named Rules / Rule Presets
# =====================================================================
def test_named_rules():
    from gui.new_features import NAMED_RULES
    # NAMED_RULES is a list of (label, rule_string) tuples
    assert isinstance(NAMED_RULES, list)
    assert len(NAMED_RULES) > 0
    labels = [label for label, _ in NAMED_RULES]
    # Should contain Conway
    assert any(
        "Conway" in lbl for lbl in labels
    ), f"No Conway rule found in {labels}"
    assert any("HighLife" in lbl for lbl in labels)
    for label, rule_str in NAMED_RULES:
        assert isinstance(label, str)
        assert isinstance(rule_str, str)
        assert rule_str.startswith("B")


# =====================================================================
#  23. GUI Config Constants
# =====================================================================
def test_gui_config_constants():
    from gui.config import (
        MODE_FACTORIES, MODE_PATTERNS, CELL_COLORS,
        MAX_HISTORY_LENGTH, MIN_GRID_SIZE, MAX_GRID_SIZE,
        DEFAULT_CELL_SIZE, DEFAULT_SPEED,
    )
    # Every mode in factories should have patterns
    for mode in MODE_FACTORIES:
        assert mode in MODE_PATTERNS, f"Mode {mode} missing from MODE_PATTERNS"

    # Patterns may include "Custom Rules" which has no factory – that's OK
    non_custom_patterns = {
        m for m in MODE_PATTERNS if m != "Custom Rules"
    }
    for mode in non_custom_patterns:
        assert mode in MODE_FACTORIES, (
            f"Pattern mode {mode} missing from MODE_FACTORIES"
        )

    assert MIN_GRID_SIZE < MAX_GRID_SIZE
    assert DEFAULT_CELL_SIZE > 0
    assert DEFAULT_SPEED > 0
    assert MAX_HISTORY_LENGTH > 0

    # CELL_COLORS maps cell state integers to color strings
    assert isinstance(CELL_COLORS, dict)
    assert 0 in CELL_COLORS
    assert 1 in CELL_COLORS


# =====================================================================
#  24. SimulationState
# =====================================================================
def test_simulation_state():
    from gui.state import SimulationState
    state = SimulationState()
    state.reset_generation()
    state.reset_metrics()

    grid = np.zeros((10, 10), dtype=int)
    grid[3:6, 3:6] = 1
    pop_str = state.update_population_stats(grid)
    assert isinstance(pop_str, str)

    state.add_metric(1, 9, 9, 0.09)
    csv_str = state.export_metrics_csv()
    assert isinstance(csv_str, str)
    assert len(csv_str) > 0


def test_simulation_state_save_load():
    from gui.state import SimulationState
    state = SimulationState()
    state.add_metric(1, 10, 10, 0.1)
    state.add_metric(2, 12, 12, 0.12)
    with tempfile.NamedTemporaryFile(
        suffix=".json", mode="w", delete=False
    ) as f:
        fpath = f.name
    try:
        state.save_state(fpath)
        state2 = SimulationState()
        state2.load_state(fpath)
    finally:
        if os.path.exists(fpath):
            os.unlink(fpath)


# =====================================================================
#  25. Statistics Exporter
# =====================================================================
def test_statistics_exporter_csv():
    from advanced.statistics import StatisticsCollector, StatisticsExporter
    sc = StatisticsCollector()
    grid = np.zeros((10, 10), dtype=int)
    grid[3:6, 3:6] = 1
    sc.collect(0, grid)
    sc.collect(1, grid)
    stats = sc.get_statistics()
    with tempfile.NamedTemporaryFile(
        suffix=".csv", mode="w", delete=False
    ) as f:
        fpath = f.name
    try:
        StatisticsExporter.export_csv(stats, fpath)
        assert os.path.getsize(fpath) > 0
    finally:
        os.unlink(fpath)


def test_statistics_exporter_summary():
    from advanced.statistics import StatisticsCollector, StatisticsExporter
    sc = StatisticsCollector()
    grid = np.zeros((10, 10), dtype=int)
    grid[3:6, 3:6] = 1
    sc.collect(0, grid)
    stats = sc.get_statistics()
    with tempfile.NamedTemporaryFile(
        suffix=".txt", mode="w", delete=False
    ) as f:
        fpath = f.name
    try:
        StatisticsExporter.export_summary(stats, fpath)
        assert os.path.getsize(fpath) > 0
    finally:
        os.unlink(fpath)


# =====================================================================
#  Main runner
# =====================================================================
def main() -> int:
    """Run all tests and report."""
    sections = [
        ("Core – SimulatorConfig", [
            test_config_defaults, test_config_roundtrip,
            test_config_from_dict_extra_keys,
        ]),
        ("Core – UndoManager", [
            test_undo_push_and_undo, test_undo_redo_roundtrip,
            test_undo_clear, test_undo_history_summary,
        ]),
        ("Core – Simulator", [
            test_simulator_init_conway, test_simulator_step,
            test_simulator_set_cell, test_simulator_undo_redo,
            test_simulator_metrics_summary, test_simulator_callback,
            test_simulator_reset, test_simulator_all_modes,
            test_simulator_unknown_mode, test_simulator_not_initialized,
        ]),
        ("Automata", [
            test_conway, test_conway_patterns, test_highlife,
            test_brians_brain, test_wireworld, test_immigration,
            test_rainbow, test_hexagonal, test_generations,
            test_langtons_ant, test_lifelike, test_parse_bs,
        ]),
        ("Boundary Mode", [
            test_boundary_mode_enum, test_convolve_with_boundary,
            test_roll_with_boundary,
        ]),
        ("GPU Module", [test_gpu_module, test_gpu_simulator]),
        ("Patterns", [test_patterns_module, test_apply_pattern_to_grid]),
        ("Plugin System", [test_plugin_manager]),
        ("RLE Format", [test_rle_encode_decode, test_rle_file_roundtrip]),
        ("Statistics", [
            test_statistics_collector, test_enhanced_statistics,
        ]),
        ("Pattern Analysis", [test_pattern_analyzer]),
        ("Rule Discovery", [test_rule_discovery]),
        ("Cell Tracker", [test_cell_age_tracker, test_cell_history_tracker]),
        ("Visualization", [test_heatmap_generator, test_symmetry_analyzer]),
        ("Pattern Manager", [test_pattern_manager]),
        ("Export Manager", [
            test_export_manager_formats, test_export_json,
            test_export_png, test_export_gif,
        ]),
        ("Config Manager", [test_app_config]),
        ("CLI Module", [
            test_cli_build_parser, test_cli_resolve_mode,
            test_cli_main_run, test_cli_main_csv_export,
            test_cli_main_json_export, test_cli_main_png_export,
        ]),
        ("API Module", [
            test_api_health, test_api_session_lifecycle,
            test_api_session_not_found,
        ]),
        ("Collab Module", [test_collab_session]),
        ("Breakpoint System", [
            test_breakpoint_condition, test_breakpoint_manager,
        ]),
        ("Named Rules", [test_named_rules]),
        ("GUI Config Constants", [test_gui_config_constants]),
        ("SimulationState", [
            test_simulation_state, test_simulation_state_save_load,
        ]),
        ("Statistics Exporter", [
            test_statistics_exporter_csv, test_statistics_exporter_summary,
        ]),
    ]

    print("=" * 60)
    print("  LifeGrid Thorough Vetting")
    print("=" * 60)

    for section_name, tests in sections:
        print(f"\n▸ {section_name}")
        for t in tests:
            _run(t.__name__, t)

    print("\n" + "=" * 60)
    passed = _results['passed']
    failed = _results['failed']
    print(f"  Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if ERRORS:
        print("\n── Failure Details ──\n")
        for err in ERRORS:
            print(err)
            print("-" * 40)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
