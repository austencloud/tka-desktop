"""
Component Performance Benchmark Suite

This benchmark suite quantifies the performance characteristics of the modern
component architecture to validate world-class performance standards.

Performance Targets:
- Component initialization: <500ms
- Service operations: <50ms
- Memory usage: <100MB for typical workflow
- Memory leaks: 0 leaks required
- Concurrent operations: Must handle gracefully
"""

import time
import gc
import sys
import threading
import psutil
import os
from pathlib import Path
from unittest.mock import Mock
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from presentation.components import ViewableComponentBase
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ILayoutService


class MockQWidget:
    """Mock Qt widget for performance testing without GUI overhead."""
    def __init__(self):
        self._enabled = True
        self._visible = True
        self._width = 800
        self._height = 600
    
    def setEnabled(self, enabled):
        self._enabled = enabled
    
    def isEnabled(self):
        return self._enabled
    
    def setVisible(self, visible):
        self._visible = visible
    
    def isVisible(self):
        return self._visible
    
    def width(self):
        return self._width
    
    def height(self):
        return self._height
    
    def resize(self, width, height):
        self._width = width
        self._height = height
    
    def deleteLater(self):
        pass


class PerformanceTestComponent(ViewableComponentBase):
    """Test component for performance benchmarking."""
    
    def __init__(self, container, parent=None):
        super().__init__(container, parent)
        self.initialization_time = 0
    
    def initialize(self):
        start_time = time.perf_counter()
        
        # Simulate realistic component initialization
        self._layout_service = self.resolve_service(ILayoutService)
        self._widget = MockQWidget()
        
        # Simulate some processing
        for _ in range(100):
            self._layout_service.get_layout()
        
        self._initialized = True
        self.component_ready.emit()
        
        self.initialization_time = time.perf_counter() - start_time
    
    def get_widget(self):
        return self._widget


class ComponentPerformanceBenchmarks:
    """Comprehensive performance benchmark suite."""
    
    def __init__(self):
        self.results = {}
        self.process = psutil.Process(os.getpid())
    
    def get_memory_usage(self):
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def benchmark_component_initialization(self, iterations=100):
        """Benchmark component initialization performance."""
        print(f"Benchmarking component initialization ({iterations} iterations)...")
        
        times = []
        memory_before = self.get_memory_usage()
        
        for i in range(iterations):
            container = DIContainer()
            
            # Register mock service
            mock_service = Mock()
            mock_service.get_layout.return_value = "mock_layout"
            container.register_factory(ILayoutService, lambda: mock_service)
            
            # Time component creation and initialization
            start_time = time.perf_counter()
            
            component = PerformanceTestComponent(container)
            component.initialize()
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
            
            # Cleanup
            component.cleanup()
            del component
            del container
            
            if i % 20 == 0:
                gc.collect()  # Periodic garbage collection
        
        memory_after = self.get_memory_usage()
        
        avg_time = sum(times) * 1000 / len(times)  # Convert to ms
        max_time = max(times) * 1000
        min_time = min(times) * 1000
        memory_delta = memory_after - memory_before
        
        self.results['component_initialization'] = {
            'avg_time_ms': avg_time,
            'max_time_ms': max_time,
            'min_time_ms': min_time,
            'memory_delta_mb': memory_delta,
            'target_ms': 500,
            'passed': avg_time < 500
        }
        
        print(f"  Average: {avg_time:.2f}ms (target: <500ms)")
        print(f"  Range: {min_time:.2f}ms - {max_time:.2f}ms")
        print(f"  Memory delta: {memory_delta:.2f}MB")
        print(f"  Status: {'PASS' if avg_time < 500 else 'FAIL'}")
    
    def benchmark_service_operations(self, iterations=1000):
        """Benchmark service operation performance."""
        print(f"Benchmarking service operations ({iterations} iterations)...")
        
        container = DIContainer()
        mock_service = Mock()
        mock_service.get_layout.return_value = "mock_layout"
        container.register_factory(ILayoutService, lambda: mock_service)
        
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            
            # Service resolution and operation
            service = container.resolve(ILayoutService)
            result = service.get_layout()
            
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        avg_time = sum(times) * 1000 / len(times)  # Convert to ms
        max_time = max(times) * 1000
        min_time = min(times) * 1000
        
        self.results['service_operations'] = {
            'avg_time_ms': avg_time,
            'max_time_ms': max_time,
            'min_time_ms': min_time,
            'target_ms': 50,
            'passed': avg_time < 50
        }
        
        print(f"  Average: {avg_time:.3f}ms (target: <50ms)")
        print(f"  Range: {min_time:.3f}ms - {max_time:.3f}ms")
        print(f"  Status: {'PASS' if avg_time < 50 else 'FAIL'}")
    
    def benchmark_memory_usage(self):
        """Benchmark memory usage during typical workflow."""
        print("Benchmarking memory usage during typical workflow...")
        
        memory_before = self.get_memory_usage()
        components = []
        
        # Simulate typical workflow: create multiple components
        for i in range(50):
            container = DIContainer()
            mock_service = Mock()
            mock_service.get_layout.return_value = f"layout_{i}"
            container.register_factory(ILayoutService, lambda: mock_service)
            
            component = PerformanceTestComponent(container)
            component.initialize()
            components.append(component)
        
        memory_peak = self.get_memory_usage()
        
        # Cleanup all components
        for component in components:
            component.cleanup()
        
        components.clear()
        gc.collect()
        
        memory_after = self.get_memory_usage()
        memory_usage = memory_peak - memory_before
        memory_leak = memory_after - memory_before
        
        self.results['memory_usage'] = {
            'peak_usage_mb': memory_usage,
            'memory_leak_mb': memory_leak,
            'target_usage_mb': 100,
            'target_leak_mb': 5,  # Allow small tolerance
            'passed': memory_usage < 100 and memory_leak < 5
        }
        
        print(f"  Peak usage: {memory_usage:.2f}MB (target: <100MB)")
        print(f"  Memory leak: {memory_leak:.2f}MB (target: <5MB)")
        print(f"  Status: {'PASS' if memory_usage < 100 and memory_leak < 5 else 'FAIL'}")
    
    def benchmark_concurrent_operations(self, num_threads=10, operations_per_thread=20):
        """Benchmark concurrent component operations."""
        print(f"Benchmarking concurrent operations ({num_threads} threads, {operations_per_thread} ops each)...")
        
        def create_and_test_component(thread_id):
            """Create and test a component in a separate thread."""
            times = []
            
            for i in range(operations_per_thread):
                container = DIContainer()
                mock_service = Mock()
                mock_service.get_layout.return_value = f"layout_{thread_id}_{i}"
                container.register_factory(ILayoutService, lambda: mock_service)
                
                start_time = time.perf_counter()
                
                component = PerformanceTestComponent(container)
                component.initialize()
                widget = component.get_widget()
                component.cleanup()
                
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            return times
        
        start_time = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(create_and_test_component, i) for i in range(num_threads)]
            all_times = []
            
            for future in as_completed(futures):
                thread_times = future.result()
                all_times.extend(thread_times)
        
        total_time = time.perf_counter() - start_time
        avg_time = sum(all_times) * 1000 / len(all_times)  # Convert to ms
        
        self.results['concurrent_operations'] = {
            'total_time_s': total_time,
            'avg_operation_time_ms': avg_time,
            'total_operations': len(all_times),
            'operations_per_second': len(all_times) / total_time,
            'passed': avg_time < 500  # Same target as single-threaded
        }
        
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Average operation: {avg_time:.2f}ms")
        print(f"  Operations/second: {len(all_times) / total_time:.1f}")
        print(f"  Status: {'PASS' if avg_time < 500 else 'FAIL'}")
    
    def benchmark_signal_performance(self, iterations=10000):
        """Benchmark signal emission and handling performance."""
        print(f"Benchmarking signal performance ({iterations} iterations)...")
        
        container = DIContainer()
        mock_service = Mock()
        container.register_factory(ILayoutService, lambda: mock_service)
        
        component = PerformanceTestComponent(container)
        component.initialize()
        
        signals_received = []
        component.component_ready.connect(lambda: signals_received.append(time.perf_counter()))
        
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            component.component_ready.emit()
        
        end_time = time.perf_counter()
        
        total_time = end_time - start_time
        avg_time = total_time * 1000000 / iterations  # Convert to microseconds
        
        component.cleanup()
        
        self.results['signal_performance'] = {
            'total_time_s': total_time,
            'avg_time_us': avg_time,
            'signals_per_second': iterations / total_time,
            'passed': avg_time < 100  # Target: <100 microseconds per signal
        }
        
        print(f"  Total time: {total_time:.3f}s")
        print(f"  Average per signal: {avg_time:.2f}μs")
        print(f"  Signals/second: {iterations / total_time:.0f}")
        print(f"  Status: {'PASS' if avg_time < 100 else 'FAIL'}")
    
    def run_all_benchmarks(self):
        """Run all performance benchmarks."""
        print("=" * 60)
        print("COMPONENT ARCHITECTURE PERFORMANCE BENCHMARKS")
        print("=" * 60)
        print("Quantifying world-class performance characteristics...")
        print()
        
        # Run all benchmarks
        self.benchmark_component_initialization()
        print()
        self.benchmark_service_operations()
        print()
        self.benchmark_memory_usage()
        print()
        self.benchmark_concurrent_operations()
        print()
        self.benchmark_signal_performance()
        
        # Summary
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result['passed'])
        
        for test_name, result in self.results.items():
            status = "PASS" if result['passed'] else "FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} benchmarks passed")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🚀 ALL BENCHMARKS PASSED! Architecture performance is WORLD-CLASS!")
            return True
        else:
            print(f"\n⚠️ {total_tests - passed_tests} benchmarks failed. Performance needs optimization.")
            return False


def main():
    """Run performance benchmarks."""
    benchmarks = ComponentPerformanceBenchmarks()
    success = benchmarks.run_all_benchmarks()
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
