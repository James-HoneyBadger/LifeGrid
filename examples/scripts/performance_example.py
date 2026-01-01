"""
Performance Benchmarking and Profiling Example

This example demonstrates how to use the performance benchmarking
and profiling tools to measure and optimize LifeGrid simulations.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

import numpy as np
from automata.conway import ConwayGameOfLife
from automata.highlife import HighLife
from performance.benchmarking import Benchmark, BenchmarkSuite
from performance.profiling import MemoryProfiler, PerformanceProfiler
from performance.optimization import (
    ViewportCuller,
    optimize_grid_dtype,
    calculate_optimal_chunk_size,
    estimate_memory_usage
)


def benchmark_automata():
    """Benchmark different automata types."""
    print("\n" + "="*70)
    print("AUTOMATA PERFORMANCE BENCHMARKING")
    print("="*70 + "\n")
    
    suite = BenchmarkSuite("Automata Comparison")
    
    # Test Conway's Game of Life at different sizes
    for size in [100, 200, 500]:
        automaton = ConwayGameOfLife(size, size)
        
        def benchmark_func():
            for _ in range(50):
                automaton.step()
        
        suite.add_benchmark(Benchmark(
            name=f"Conway_{size}x{size}",
            function=benchmark_func,
            iterations=5,
            metadata={'automaton': 'Conway', 'size': size}
        ))
    
    # Test HighLife automaton
    for size in [100, 200]:
        automaton = HighLife(size, size)
        
        def benchmark_func():
            for _ in range(50):
                automaton.step()
        
        suite.add_benchmark(Benchmark(
            name=f"HighLife_{size}x{size}",
            function=benchmark_func,
            iterations=5,
            metadata={'automaton': 'HighLife', 'size': size}
        ))
    
    # Run all benchmarks
    results = suite.run_all(verbose=True)
    
    # Show summary
    print(suite.get_summary())
    
    # Compare results
    print("\nComparison by Mean Time (fastest to slowest):")
    sorted_results = suite.compare_results(metric='mean_time', ascending=True)
    for i, result in enumerate(sorted_results, 1):
        print(f"  {i}. {result.name}: {result.mean_time*1000:.2f}ms "
              f"({result.throughput:.2f} iter/s)")


def profile_memory_usage():
    """Profile memory usage during simulation."""
    print("\n" + "="*70)
    print("MEMORY PROFILING")
    print("="*70 + "\n")
    
    profiler = MemoryProfiler()
    profiler.start()
    
    # Create various sized automata and measure memory
    profiler.take_snapshot("baseline")
    
    print("Creating 100x100 automaton...")
    small = ConwayGameOfLife(100, 100)
    profiler.take_snapshot("small_automaton")
    
    print("Creating 500x500 automaton...")
    medium = ConwayGameOfLife(500, 500)
    profiler.take_snapshot("medium_automaton")
    
    print("Creating 1000x1000 automaton...")
    large = ConwayGameOfLife(1000, 1000)
    profiler.take_snapshot("large_automaton")
    
    # Run some simulations
    print("Running simulations...")
    with profiler.profile_section("simulations"):
        for _ in range(100):
            small.step()
            medium.step()
            large.step()
    
    profiler.stop()
    
    # Show memory report
    print(profiler.get_report())
    
    # Memory usage estimates
    print("\nEstimated Memory Usage:")
    for size, name in [(100, "small"), (500, "medium"), (1000, "large")]:
        memory_mb = estimate_memory_usage((size, size), np.uint8)
        print(f"  {name.capitalize()} ({size}x{size}): {memory_mb:.2f}MB")


def profile_execution_performance():
    """Profile execution performance of specific operations."""
    print("\n" + "="*70)
    print("EXECUTION PERFORMANCE PROFILING")
    print("="*70 + "\n")
    
    profiler = PerformanceProfiler()
    automaton = ConwayGameOfLife(300, 300)
    
    print("Profiling individual operations...")
    
    # Profile grid updates
    for i in range(50):
        with profiler.profile("grid_update"):
            automaton.step()
    
    # Profile grid retrieval
    for i in range(100):
        with profiler.profile("grid_access"):
            grid = automaton.get_grid()
    
    # Profile cell interactions
    for i in range(20):
        with profiler.profile("cell_interaction"):
            for _ in range(10):
                x, y = np.random.randint(0, 300, size=2)
                automaton.handle_click(x, y)
    
    # Show performance report
    print(profiler.get_report())
    
    # Show individual profile details
    print("\nDetailed Profile Information:")
    for name in ["grid_update", "grid_access", "cell_interaction"]:
        profile = profiler.get_profile(name)
        if profile:
            print(f"\n{name}:")
            print(f"  Total Calls: {profile.call_count}")
            print(f"  Total Time: {profile.duration*1000:.2f}ms")
            print(f"  Average Time: {(profile.duration/profile.call_count)*1000:.2f}ms")
            print(f"  Memory Used: {profile.memory_used:.2f}MB")


def demonstrate_viewport_culling():
    """Demonstrate viewport culling optimization."""
    print("\n" + "="*70)
    print("VIEWPORT CULLING OPTIMIZATION")
    print("="*70 + "\n")
    
    # Create a large grid
    grid_size = (2000, 2000)
    culler = ViewportCuller(grid_size)
    
    print(f"Full Grid Size: {grid_size[0]}x{grid_size[1]} "
          f"({grid_size[0] * grid_size[1]:,} cells)")
    
    # Test different viewport sizes
    viewports = [
        (0, 0, 500, 500, "Small viewport (500x500)"),
        (500, 500, 800, 600, "Medium viewport (800x600)"),
        (0, 0, 1920, 1080, "Full HD viewport (1920x1080)"),
    ]
    
    print("\nViewport Culling Savings:")
    for x, y, width, height, label in viewports:
        culler.set_viewport(x, y, width, height, buffer=50)
        savings = culler.calculate_savings()
        visible_region = culler.get_visible_region()
        visible_width = visible_region[2] - visible_region[0]
        visible_height = visible_region[3] - visible_region[1]
        visible_cells = visible_width * visible_height
        
        print(f"\n  {label}:")
        print(f"    Visible Area: {visible_width}x{visible_height} ({visible_cells:,} cells)")
        print(f"    Culled: {savings:.1f}%")
        print(f"    Processing Reduction: {savings:.1f}% fewer cells")


def demonstrate_grid_optimization():
    """Demonstrate grid dtype optimization."""
    print("\n" + "="*70)
    print("GRID DATA TYPE OPTIMIZATION")
    print("="*70 + "\n")
    
    grid_size = (1000, 1000)
    
    print(f"Grid Size: {grid_size[0]}x{grid_size[1]}")
    print("\nMemory Usage by State Count:")
    
    state_counts = [2, 16, 256, 1000, 70000]
    
    for num_states in state_counts:
        # Create grid with default dtype
        grid = np.random.randint(0, num_states, size=grid_size, dtype=np.int32)
        original_memory = grid.nbytes / (1024 * 1024)
        
        # Optimize dtype
        optimized = optimize_grid_dtype(grid, num_states)
        optimized_memory = optimized.nbytes / (1024 * 1024)
        
        savings = ((original_memory - optimized_memory) / original_memory) * 100
        
        print(f"\n  {num_states} states:")
        print(f"    Original (int32): {original_memory:.2f}MB")
        print(f"    Optimized ({optimized.dtype}): {optimized_memory:.2f}MB")
        print(f"    Savings: {savings:.1f}%")


def demonstrate_parallel_processing():
    """Demonstrate parallel processing recommendations."""
    print("\n" + "="*70)
    print("PARALLEL PROCESSING RECOMMENDATIONS")
    print("="*70 + "\n")
    
    from performance.optimization import ParallelProcessor
    import multiprocessing as mp
    
    print(f"Available CPU Cores: {mp.cpu_count()}")
    print("\nParallel Processing Recommendations:")
    
    grid_sizes = [
        (100, 100),
        (500, 500),
        (1000, 1000),
        (2000, 2000),
        (5000, 5000),
    ]
    
    for size in grid_sizes:
        should_parallel = ParallelProcessor.should_use_parallel(size, threshold=500)
        chunk_size = calculate_optimal_chunk_size(size, mp.cpu_count())
        
        print(f"\n  {size[0]}x{size[1]} grid:")
        print(f"    Use Parallel: {'Yes' if should_parallel else 'No'}")
        if should_parallel:
            print(f"    Optimal Chunk Size: {chunk_size} rows")
            print(f"    Chunks per Core: ~{size[1] // (chunk_size * mp.cpu_count())}")


def run_comprehensive_benchmark():
    """Run a comprehensive benchmark suite."""
    print("\n" + "="*70)
    print("COMPREHENSIVE PERFORMANCE BENCHMARK")
    print("="*70 + "\n")
    
    suite = BenchmarkSuite("Comprehensive Performance Test")
    
    # Different grid sizes
    sizes = [100, 200, 500]
    
    for size in sizes:
        automaton = ConwayGameOfLife(size, size)
        
        # Benchmark different numbers of steps
        for steps in [10, 50, 100]:
            def make_benchmark_func(auto, n_steps):
                def func():
                    for _ in range(n_steps):
                        auto.step()
                return func
            
            suite.add_benchmark(Benchmark(
                name=f"{size}x{size}_{steps}_steps",
                function=make_benchmark_func(automaton, steps),
                iterations=5,
                warmup_iterations=2,
                metadata={'size': size, 'steps': steps}
            ))
    
    print("Running comprehensive benchmark suite...")
    print("This may take a minute...\n")
    
    results = suite.run_all(verbose=False)
    
    # Analyze results
    print("\n" + "="*70)
    print("RESULTS ANALYSIS")
    print("="*70 + "\n")
    
    print("Performance by Grid Size:")
    for size in sizes:
        size_results = [r for r in results if r.metadata['size'] == size]
        avg_time = np.mean([r.mean_time for r in size_results])
        print(f"  {size}x{size}: {avg_time*1000:.2f}ms average")
    
    print("\nPerformance by Step Count:")
    for steps in [10, 50, 100]:
        step_results = [r for r in results if r.metadata['steps'] == steps]
        avg_time = np.mean([r.mean_time for r in step_results])
        print(f"  {steps} steps: {avg_time*1000:.2f}ms average")
    
    # Export results
    output_file = "benchmark_results.json"
    suite.export_results(output_file)
    print(f"\n✅ Results exported to {output_file}")


def main():
    """Run all performance examples."""
    print("\n" + "="*70)
    print("LIFEGRID PERFORMANCE BENCHMARKING & PROFILING")
    print("="*70)
    
    try:
        # Run all demonstrations
        benchmark_automata()
        profile_memory_usage()
        profile_execution_performance()
        demonstrate_viewport_culling()
        demonstrate_grid_optimization()
        demonstrate_parallel_processing()
        run_comprehensive_benchmark()
        
        print("\n" + "="*70)
        print("ALL PERFORMANCE DEMONSTRATIONS COMPLETE")
        print("="*70 + "\n")
        
        print("Key Takeaways:")
        print("  • Benchmarking helps compare automata and grid sizes")
        print("  • Memory profiling identifies memory-intensive operations")
        print("  • Performance profiling pinpoints bottlenecks")
        print("  • Viewport culling reduces processing for large grids")
        print("  • Grid dtype optimization saves significant memory")
        print("  • Parallel processing improves performance for large grids")
        
    except KeyboardInterrupt:
        print("\n\nBenchmarking interrupted by user.")
    except Exception as e:
        print(f"\n\nError during benchmarking: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
