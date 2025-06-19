#!/usr/bin/env python3
"""
Performance Benchmark Runner

This script runs comprehensive performance benchmarks for the TKA Desktop
modern component architecture to validate world-class performance standards.

Usage:
    python run_performance_benchmarks.py [--quick] [--detailed]
    
Options:
    --quick     Run quick benchmarks with reduced iterations
    --detailed  Run detailed benchmarks with extended analysis
"""

import sys
import argparse
import time
from pathlib import Path

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

# Add tests to path
tests_path = Path(__file__).parent.parent / "tests"
sys.path.insert(0, str(tests_path))

from performance.test_component_performance import ComponentPerformanceBenchmarks


def print_system_info():
    """Print system information for benchmark context."""
    import platform
    import psutil
    
    print("SYSTEM INFORMATION")
    print("=" * 60)
    print(f"Platform: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"CPU: {platform.processor()}")
    print(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    
    memory = psutil.virtual_memory()
    print(f"Memory: {memory.total / (1024**3):.1f} GB total, {memory.available / (1024**3):.1f} GB available")
    print()


def run_quick_benchmarks():
    """Run quick performance benchmarks with reduced iterations."""
    print("QUICK PERFORMANCE BENCHMARKS")
    print("=" * 60)
    print("Running reduced iteration benchmarks for rapid validation...")
    print()
    
    class QuickBenchmarks(ComponentPerformanceBenchmarks):
        def run_quick_benchmarks(self):
            """Run quick versions of all benchmarks."""
            self.benchmark_component_initialization(iterations=20)
            print()
            self.benchmark_service_operations(iterations=100)
            print()
            self.benchmark_memory_usage()  # Already quick
            print()
            self.benchmark_concurrent_operations(num_threads=5, operations_per_thread=5)
            print()
            self.benchmark_signal_performance(iterations=1000)
            
            # Quick summary
            print("\n" + "=" * 60)
            print("QUICK BENCHMARK RESULTS")
            print("=" * 60)
            
            total_tests = len(self.results)
            passed_tests = sum(1 for result in self.results.values() if result['passed'])
            
            for test_name, result in self.results.items():
                status = "PASS" if result['passed'] else "FAIL"
                print(f"{test_name.replace('_', ' ').title()}: {status}")
            
            print(f"\nOverall: {passed_tests}/{total_tests} benchmarks passed")
            print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
            
            return passed_tests == total_tests
    
    benchmarks = QuickBenchmarks()
    return benchmarks.run_quick_benchmarks()


def run_detailed_benchmarks():
    """Run detailed performance benchmarks with extended analysis."""
    print("DETAILED PERFORMANCE BENCHMARKS")
    print("=" * 60)
    print("Running comprehensive benchmarks with extended analysis...")
    print()
    
    class DetailedBenchmarks(ComponentPerformanceBenchmarks):
        def run_detailed_benchmarks(self):
            """Run detailed versions of all benchmarks."""
            # Extended iterations for more accurate results
            self.benchmark_component_initialization(iterations=200)
            print()
            self.benchmark_service_operations(iterations=5000)
            print()
            self.benchmark_memory_usage()
            print()
            self.benchmark_concurrent_operations(num_threads=20, operations_per_thread=50)
            print()
            self.benchmark_signal_performance(iterations=50000)
            
            # Detailed analysis
            print("\n" + "=" * 60)
            print("DETAILED BENCHMARK ANALYSIS")
            print("=" * 60)
            
            self._print_detailed_analysis()
            
            total_tests = len(self.results)
            passed_tests = sum(1 for result in self.results.values() if result['passed'])
            
            return passed_tests == total_tests
        
        def _print_detailed_analysis(self):
            """Print detailed analysis of benchmark results."""
            for test_name, result in self.results.items():
                print(f"\n{test_name.replace('_', ' ').title()}:")
                print("-" * 40)
                
                if 'avg_time_ms' in result:
                    print(f"  Average Time: {result['avg_time_ms']:.3f}ms")
                    if 'target_ms' in result:
                        print(f"  Target: <{result['target_ms']}ms")
                        efficiency = (result['target_ms'] - result['avg_time_ms']) / result['target_ms'] * 100
                        print(f"  Efficiency: {efficiency:.1f}% under target")
                
                if 'memory_delta_mb' in result:
                    print(f"  Memory Delta: {result['memory_delta_mb']:.2f}MB")
                
                if 'peak_usage_mb' in result:
                    print(f"  Peak Memory: {result['peak_usage_mb']:.2f}MB")
                    print(f"  Memory Leak: {result['memory_leak_mb']:.2f}MB")
                
                if 'operations_per_second' in result:
                    print(f"  Throughput: {result['operations_per_second']:.1f} ops/sec")
                
                if 'signals_per_second' in result:
                    print(f"  Signal Rate: {result['signals_per_second']:.0f} signals/sec")
                
                status = "PASS" if result['passed'] else "FAIL"
                print(f"  Status: {status}")
    
    benchmarks = DetailedBenchmarks()
    return benchmarks.run_detailed_benchmarks()


def run_standard_benchmarks():
    """Run standard performance benchmarks."""
    benchmarks = ComponentPerformanceBenchmarks()
    return benchmarks.run_all_benchmarks()


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(
        description="Run TKA Desktop performance benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--quick", 
        action="store_true", 
        help="Run quick benchmarks with reduced iterations"
    )
    parser.add_argument(
        "--detailed", 
        action="store_true", 
        help="Run detailed benchmarks with extended analysis"
    )
    
    args = parser.parse_args()
    
    # Print system info
    print_system_info()
    
    # Run appropriate benchmark suite
    start_time = time.time()
    
    try:
        if args.quick:
            success = run_quick_benchmarks()
        elif args.detailed:
            success = run_detailed_benchmarks()
        else:
            success = run_standard_benchmarks()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"\nTotal benchmark time: {total_time:.1f} seconds")
        
        if success:
            print("\n🎉 ALL PERFORMANCE BENCHMARKS PASSED!")
            print("✅ Component architecture meets world-class performance standards")
            print("✅ Ready for production deployment")
            return 0
        else:
            print("\n⚠️ Some performance benchmarks failed")
            print("❌ Architecture performance needs optimization")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nBenchmarks interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\nError running benchmarks: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
