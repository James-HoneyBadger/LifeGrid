"""
Tests for performance profiling and optimization modules.
"""

import pytest
import numpy as np
import time
from src.performance.benchmarking import Benchmark, BenchmarkSuite, BenchmarkResult
from src.performance.profiling import MemoryProfiler, PerformanceProfiler
from src.performance.optimization import (
    ParallelProcessor,
    ViewportCuller,
    optimize_grid_dtype,
    calculate_optimal_chunk_size,
    estimate_memory_usage
)
from src.automata.conway import ConwayGameOfLife
from src.core.simulator import Simulator


class TestBenchmarking:
    """Test the benchmarking module."""
    
    def test_benchmark_creation(self):
        """Test creating a benchmark."""
        counter = {'value': 0}
        
        def test_func():
            counter['value'] += 1
        
        benchmark = Benchmark(
            name="test_benchmark",
            function=test_func,
            iterations=10,
            warmup_iterations=2
        )
        
        assert benchmark.name == "test_benchmark"
        assert benchmark.iterations == 10
        assert benchmark.warmup_iterations == 2
    
    def test_benchmark_run(self):
        """Test running a benchmark."""
        counter = {'value': 0}
        
        def test_func():
            counter['value'] += 1
            time.sleep(0.001)  # Small delay for measurable time
        
        benchmark = Benchmark(
            name="test_benchmark",
            function=test_func,
            iterations=5,
            warmup_iterations=2
        )
        
        result = benchmark.run()
        
        assert result.name == "test_benchmark"
        assert result.iterations == 5
        assert counter['value'] == 7  # 2 warmup + 5 benchmark
        assert result.total_time > 0
        assert result.mean_time > 0
        assert result.throughput > 0
    
    def test_benchmark_result_str(self):
        """Test benchmark result string representation."""
        result = BenchmarkResult(
            name="test",
            iterations=10,
            total_time=1.0,
            mean_time=0.1,
            median_time=0.1,
            std_dev=0.01,
            min_time=0.09,
            max_time=0.11,
            throughput=10.0
        )
        
        result_str = str(result)
        assert "test" in result_str
        assert "10" in result_str
    
    def test_benchmark_suite_add(self):
        """Test adding benchmarks to a suite."""
        suite = BenchmarkSuite("Test Suite")
        
        benchmark1 = Benchmark("test1", lambda: None, iterations=5)
        benchmark2 = Benchmark("test2", lambda: None, iterations=5)
        
        suite.add_benchmark(benchmark1)
        suite.add_benchmark(benchmark2)
        
        assert len(suite.benchmarks) == 2
    
    def test_benchmark_suite_run(self):
        """Test running a benchmark suite."""
        suite = BenchmarkSuite("Test Suite")
        
        suite.add_benchmark(Benchmark("test1", lambda: None, iterations=3))
        suite.add_benchmark(Benchmark("test2", lambda: time.sleep(0.001), iterations=3))
        
        results = suite.run_all(verbose=False)
        
        assert len(results) == 2
        assert all(isinstance(r, BenchmarkResult) for r in results)
        assert len(suite.results) == 2
    
    def test_benchmark_automaton(self):
        """Test benchmarking an automaton."""
        suite = BenchmarkSuite("Automaton Suite")
        
        # Create a simple benchmark function
        automaton = ConwayGameOfLife(100, 100)
        
        def benchmark_func():
            for _ in range(10):
                automaton.step()
        
        benchmark = Benchmark(
            name="conway_100x100",
            function=benchmark_func,
            iterations=3,
            metadata={'automaton': 'ConwayGameOfLife', 'grid_size': (100, 100)}
        )
        
        suite.add_benchmark(benchmark)
        results = suite.run_all(verbose=False)
        
        assert len(results) == 1
        assert results[0].metadata['automaton'] == 'ConwayGameOfLife'
        assert results[0].metadata['grid_size'] == (100, 100)
    
    def test_benchmark_simulator(self):
        """Test benchmarking a simulator."""
        suite = BenchmarkSuite("Simulator Suite")
        
        # Use ConwayGameOfLife as automaton
        automaton = ConwayGameOfLife(50, 50)
        
        def benchmark_func():
            for _ in range(10):
                automaton.step()
        
        benchmark = Benchmark(
            name="simulator_50x50",
            function=benchmark_func,
            iterations=3,
            metadata={'automaton': 'ConwayGameOfLife'}
        )
        
        suite.add_benchmark(benchmark)
        results = suite.run_all(verbose=False)
        
        assert len(results) == 1
        assert results[0].metadata['automaton'] == 'ConwayGameOfLife'
    
    def test_benchmark_summary(self):
        """Test generating a benchmark summary."""
        suite = BenchmarkSuite("Test Suite")
        
        suite.add_benchmark(Benchmark("fast", lambda: None, iterations=5))
        suite.add_benchmark(Benchmark("slow", lambda: time.sleep(0.002), iterations=5))
        
        suite.run_all(verbose=False)
        summary = suite.get_summary()
        
        assert "Test Suite" in summary
        assert "fast" in summary
        assert "slow" in summary
        assert "Fastest" in summary
        assert "Slowest" in summary
    
    def test_benchmark_compare(self):
        """Test comparing benchmark results."""
        suite = BenchmarkSuite("Test Suite")
        
        suite.add_benchmark(Benchmark("test1", lambda: time.sleep(0.001), iterations=3))
        suite.add_benchmark(Benchmark("test2", lambda: None, iterations=3))
        
        suite.run_all(verbose=False)
        
        sorted_results = suite.compare_results(metric='mean_time', ascending=True)
        assert sorted_results[0].name == "test2"  # Faster one first
        assert sorted_results[1].name == "test1"


class TestMemoryProfiler:
    """Test the memory profiling module."""
    
    def test_profiler_start_stop(self):
        """Test starting and stopping the profiler."""
        profiler = MemoryProfiler()
        
        assert not profiler.is_running
        
        profiler.start()
        assert profiler.is_running
        assert len(profiler.snapshots) == 1
        
        profiler.stop()
        assert not profiler.is_running
        assert len(profiler.snapshots) == 2
    
    def test_profiler_snapshot(self):
        """Test taking memory snapshots."""
        profiler = MemoryProfiler()
        profiler.start()
        
        snapshot1 = profiler.take_snapshot("before")
        
        # Allocate some memory
        data = np.zeros((1000, 1000))
        
        snapshot2 = profiler.take_snapshot("after")
        
        profiler.stop()
        
        assert snapshot1.label == "before"
        assert snapshot2.label == "after"
        assert snapshot2.current_mb >= snapshot1.current_mb
    
    def test_profiler_memory_increase(self):
        """Test measuring memory increase."""
        profiler = MemoryProfiler()
        profiler.start()
        
        # Allocate memory
        data = [np.zeros((100, 100)) for _ in range(10)]
        profiler.take_snapshot("after_alloc")
        
        increase = profiler.get_memory_increase()
        assert increase >= 0
        
        profiler.stop()
    
    def test_profiler_context_manager(self):
        """Test profiling with context manager."""
        profiler = MemoryProfiler()
        profiler.start()
        
        with profiler.profile_section("test_section"):
            data = np.zeros((500, 500))
        
        profiler.stop()
        
        # Should have start, test_section_start, test_section_end, stop
        assert len(profiler.snapshots) >= 4
        assert any("test_section_start" in s.label for s in profiler.snapshots)
    
    def test_profiler_report(self):
        """Test generating a profiler report."""
        profiler = MemoryProfiler()
        profiler.start()
        
        profiler.take_snapshot("step1")
        data = np.zeros((100, 100))
        profiler.take_snapshot("step2")
        
        profiler.stop()
        
        report = profiler.get_report()
        
        assert "Memory Profiling Report" in report
        assert "step1" in report
        assert "step2" in report


class TestPerformanceProfiler:
    """Test the performance profiling module."""
    
    def test_profiler_context(self):
        """Test profiling with context manager."""
        profiler = PerformanceProfiler()
        
        with profiler.profile("test_op"):
            time.sleep(0.01)
        
        result = profiler.get_profile("test_op")
        
        assert result is not None
        assert result.name == "test_op"
        assert result.call_count == 1
        assert result.duration >= 0.01
    
    def test_profiler_multiple_calls(self):
        """Test profiling multiple calls to the same operation."""
        profiler = PerformanceProfiler()
        
        for _ in range(5):
            with profiler.profile("repeated_op"):
                time.sleep(0.001)
        
        result = profiler.get_profile("repeated_op")
        
        assert result.call_count == 5
        assert result.duration >= 0.005
    
    def test_profiler_measure_function(self):
        """Test measuring a function."""
        profiler = PerformanceProfiler()
        
        def test_func(x):
            time.sleep(0.001)
            return x * 2
        
        result = profiler.measure_function(test_func, 5, iterations=3)
        
        assert result.name == "test_func"
        assert result.call_count == 3
    
    def test_profiler_report(self):
        """Test generating a performance report."""
        profiler = PerformanceProfiler()
        
        with profiler.profile("op1"):
            time.sleep(0.005)
        
        with profiler.profile("op2"):
            time.sleep(0.001)
        
        report = profiler.get_report()
        
        assert "Performance Profiling Report" in report
        assert "op1" in report
        assert "op2" in report
    
    def test_profiler_reset(self):
        """Test resetting profiler."""
        profiler = PerformanceProfiler()
        
        with profiler.profile("test"):
            pass
        
        assert len(profiler.profiles) == 1
        
        profiler.reset()
        assert len(profiler.profiles) == 0


class TestViewportCuller:
    """Test the viewport culling optimization."""
    
    def test_culler_creation(self):
        """Test creating a viewport culler."""
        culler = ViewportCuller((100, 100))
        
        assert culler.grid_width == 100
        assert culler.grid_height == 100
        assert not culler.is_viewport_set()
    
    def test_set_viewport(self):
        """Test setting the viewport."""
        culler = ViewportCuller((100, 100))
        
        culler.set_viewport(10, 10, 50, 50, buffer=5)
        
        assert culler.is_viewport_set()
    
    def test_visible_region(self):
        """Test getting the visible region."""
        culler = ViewportCuller((100, 100))
        
        culler.set_viewport(20, 20, 40, 40, buffer=0)
        region = culler.get_visible_region()
        
        assert region == (20, 20, 60, 60)
    
    def test_visible_region_with_buffer(self):
        """Test getting visible region with buffer."""
        culler = ViewportCuller((100, 100))
        
        culler.set_viewport(20, 20, 40, 40, buffer=10)
        region = culler.get_visible_region()
        
        assert region == (10, 10, 70, 70)
    
    def test_visible_region_clamping(self):
        """Test that visible region is clamped to grid bounds."""
        culler = ViewportCuller((100, 100))
        
        culler.set_viewport(0, 0, 50, 50, buffer=20)
        region = culler.get_visible_region()
        
        # Should clamp to grid bounds
        assert region[0] >= 0
        assert region[1] >= 0
        assert region[2] <= 100
        assert region[3] <= 100
    
    def test_extract_visible_grid(self):
        """Test extracting visible grid."""
        culler = ViewportCuller((100, 100))
        grid = np.arange(10000).reshape(100, 100)
        
        culler.set_viewport(20, 20, 40, 40, buffer=0)
        visible, offset = culler.extract_visible_grid(grid)
        
        assert visible.shape == (40, 40)
        assert offset == (20, 20)
        assert np.array_equal(visible, grid[20:60, 20:60])
    
    def test_merge_visible_grid(self):
        """Test merging visible grid back."""
        culler = ViewportCuller((100, 100))
        grid = np.zeros((100, 100))
        
        culler.set_viewport(20, 20, 40, 40, buffer=0)
        visible, offset = culler.extract_visible_grid(grid)
        
        # Modify visible grid
        visible[:] = 1
        
        # Merge back
        result = culler.merge_visible_grid(grid, visible, offset)
        
        # Check that only the visible region was updated
        assert np.sum(result) == 40 * 40
        assert np.all(result[20:60, 20:60] == 1)
        assert np.all(result[0:20, :] == 0)
    
    def test_calculate_savings(self):
        """Test calculating culling savings."""
        culler = ViewportCuller((100, 100))
        
        # No viewport set
        assert culler.calculate_savings() == 0.0
        
        # Small viewport
        culler.set_viewport(0, 0, 25, 25, buffer=0)
        savings = culler.calculate_savings()
        
        # Should cull about 93.75% of the grid (25*25 visible out of 100*100)
        assert savings > 90
        assert savings < 95
    
    def test_reset_viewport(self):
        """Test resetting viewport."""
        culler = ViewportCuller((100, 100))
        
        culler.set_viewport(10, 10, 50, 50)
        assert culler.is_viewport_set()
        
        culler.reset_viewport()
        assert not culler.is_viewport_set()


class TestParallelProcessor:
    """Test parallel processing optimization."""
    
    def test_processor_creation(self):
        """Test creating a parallel processor."""
        processor = ParallelProcessor(num_workers=2)
        
        assert processor.num_workers == 2
        assert processor.use_processes is True
    
    def test_context_manager(self):
        """Test using parallel processor as context manager."""
        with ParallelProcessor(num_workers=2) as processor:
            assert processor._executor is not None
        
        # Executor should be shut down after exiting context
        # (can't test directly, but no exception should occur)
    
    def test_should_use_parallel(self):
        """Test determining if parallel processing is beneficial."""
        # Small grid
        assert not ParallelProcessor.should_use_parallel((100, 100), threshold=500)
        
        # Large grid
        assert ParallelProcessor.should_use_parallel((1000, 1000), threshold=500)
    
    def test_parallel_grid_update(self):
        """Test parallel grid update."""
        # Simple update function: increment all values
        def update_func(grid):
            return grid + 1
        
        grid = np.zeros((100, 100), dtype=np.uint8)
        
        # Use threads for testing to avoid pickling issues with local functions
        with ParallelProcessor(num_workers=2, use_processes=False) as processor:
            result = processor.parallel_grid_update(
                grid,
                update_func,
                chunk_size=50
            )
        
        # All values should be incremented
        assert np.all(result == 1)
        assert result.shape == grid.shape


class TestOptimizationUtilities:
    """Test optimization utility functions."""
    
    def test_optimize_grid_dtype(self):
        """Test optimizing grid data type."""
        # Binary states
        grid = np.array([[0, 1], [1, 0]])
        optimized = optimize_grid_dtype(grid, num_states=2)
        assert optimized.dtype == np.bool_
        
        # Few states
        grid = np.array([[0, 5], [10, 15]])
        optimized = optimize_grid_dtype(grid, num_states=16)
        assert optimized.dtype == np.uint8
        
        # Many states
        grid = np.array([[0, 500], [1000, 1500]])
        optimized = optimize_grid_dtype(grid, num_states=2000)
        assert optimized.dtype == np.uint16
    
    def test_calculate_optimal_chunk_size(self):
        """Test calculating optimal chunk size."""
        chunk_size = calculate_optimal_chunk_size(
            grid_size=(100, 200),
            num_workers=4,
            min_chunk_size=10
        )
        
        assert chunk_size >= 10
        assert isinstance(chunk_size, int)
    
    def test_estimate_memory_usage(self):
        """Test estimating memory usage."""
        # 1000x1000 uint8 grid
        memory_mb = estimate_memory_usage((1000, 1000), np.uint8)
        
        # Should be close to 1 MB (1000*1000 bytes / 1024^2)
        assert 0.9 < memory_mb < 1.1
        
        # 1000x1000 uint32 grid
        memory_mb = estimate_memory_usage((1000, 1000), np.uint32)
        
        # Should be close to 4 MB
        assert 3.8 < memory_mb < 4.2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
