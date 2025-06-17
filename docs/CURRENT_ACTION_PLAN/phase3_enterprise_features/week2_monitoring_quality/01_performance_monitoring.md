# Performance Monitoring

## Task 3.3: Performance Monitoring System

**Real-time Performance Tracking:**

```python
# FILE: src/infrastructure/monitoring/performance_monitor.py

"""
Comprehensive performance monitoring for TKA modern.
Tracks execution time, memory usage, and system resources.
"""

import time
import psutil
import threading
from functools import wraps
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
import statistics

@dataclass
class PerformanceMetric:
    """Single performance measurement."""
    function_name: str
    execution_time: float
    memory_usage: float
    cpu_percentage: float
    timestamp: datetime
    args_hash: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None

@dataclass
class AggregateMetrics:
    """Aggregated performance metrics."""
    function_name: str
    call_count: int
    avg_execution_time: float
    min_execution_time: float
    max_execution_time: float
    avg_memory_usage: float
    success_rate: float
    last_24h_calls: int
    performance_trend: str  # "improving", "degrading", "stable"

class PerformanceMonitor:
    """Central performance monitoring system."""

    def __init__(self,
                 enable_detailed_logging: bool = True,
                 max_metrics_history: int = 10000):
        self.enable_detailed_logging = enable_detailed_logging
        self.max_metrics_history = max_metrics_history
        self.metrics: List[PerformanceMetric] = []
        self.lock = threading.Lock()
        self.aggregates: Dict[str, AggregateMetrics] = {}
        self.monitoring_active = True

        # Start background cleanup thread
        self._start_cleanup_thread()

    def record_metric(self, metric: PerformanceMetric) -> None:
        """Record a performance metric."""
        if not self.monitoring_active:
            return

        with self.lock:
            self.metrics.append(metric)

            # Update aggregates
            self._update_aggregates(metric)

            # Cleanup old metrics if needed
            if len(self.metrics) > self.max_metrics_history:
                self.metrics = self.metrics[-self.max_metrics_history:]

    def _update_aggregates(self, metric: PerformanceMetric) -> None:
        """Update aggregate metrics."""
        func_name = metric.function_name

        if func_name not in self.aggregates:
            self.aggregates[func_name] = AggregateMetrics(
                function_name=func_name,
                call_count=0,
                avg_execution_time=0.0,
                min_execution_time=float('inf'),
                max_execution_time=0.0,
                avg_memory_usage=0.0,
                success_rate=1.0,
                last_24h_calls=0,
                performance_trend="stable"
            )

        agg = self.aggregates[func_name]

        # Update basic stats
        agg.call_count += 1
        agg.avg_execution_time = (
            (agg.avg_execution_time * (agg.call_count - 1) + metric.execution_time) /
            agg.call_count
        )
        agg.min_execution_time = min(agg.min_execution_time, metric.execution_time)
        agg.max_execution_time = max(agg.max_execution_time, metric.execution_time)
        agg.avg_memory_usage = (
            (agg.avg_memory_usage * (agg.call_count - 1) + metric.memory_usage) /
            agg.call_count
        )

        # Update success rate
        total_success = sum(1 for m in self.metrics
                          if m.function_name == func_name and m.success)
        agg.success_rate = total_success / agg.call_count

        # Update 24h calls
        cutoff = datetime.now() - timedelta(hours=24)
        agg.last_24h_calls = sum(1 for m in self.metrics
                               if m.function_name == func_name and m.timestamp > cutoff)

        # Calculate performance trend
        agg.performance_trend = self._calculate_trend(func_name)

    def _calculate_trend(self, function_name: str) -> str:
        """Calculate performance trend for a function."""
        recent_metrics = [m for m in self.metrics[-100:]
                         if m.function_name == function_name]

        if len(recent_metrics) < 10:
            return "stable"

        # Compare first half vs second half
        mid_point = len(recent_metrics) // 2
        first_half_avg = statistics.mean(m.execution_time for m in recent_metrics[:mid_point])
        second_half_avg = statistics.mean(m.execution_time for m in recent_metrics[mid_point:])

        change_percentage = ((second_half_avg - first_half_avg) / first_half_avg) * 100

        if change_percentage > 10:
            return "degrading"
        elif change_percentage < -10:
            return "improving"
        else:
            return "stable"

    def get_function_stats(self, function_name: str) -> Optional[AggregateMetrics]:
        """Get aggregated stats for a specific function."""
        return self.aggregates.get(function_name)

    def get_slowest_functions(self, limit: int = 10) -> List[AggregateMetrics]:
        """Get the slowest functions by average execution time."""
        return sorted(self.aggregates.values(),
                     key=lambda x: x.avg_execution_time,
                     reverse=True)[:limit]

    def get_most_called_functions(self, limit: int = 10) -> List[AggregateMetrics]:
        """Get the most frequently called functions."""
        return sorted(self.aggregates.values(),
                     key=lambda x: x.call_count,
                     reverse=True)[:limit]

    def export_metrics(self, file_path: Path) -> None:
        """Export metrics to JSON file."""
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_metrics": len(self.metrics),
            "aggregates": {
                name: {
                    "function_name": agg.function_name,
                    "call_count": agg.call_count,
                    "avg_execution_time": agg.avg_execution_time,
                    "min_execution_time": agg.min_execution_time,
                    "max_execution_time": agg.max_execution_time,
                    "avg_memory_usage": agg.avg_memory_usage,
                    "success_rate": agg.success_rate,
                    "last_24h_calls": agg.last_24h_calls,
                    "performance_trend": agg.performance_trend
                }
                for name, agg in self.aggregates.items()
            }
        }

        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)

    def generate_report(self) -> str:
        """Generate a performance report."""
        report_lines = [
            "🔍 TKA modern Performance Report",
            "=" * 40,
            f"📊 Total Metrics Collected: {len(self.metrics)}",
            f"🔢 Functions Monitored: {len(self.aggregates)}",
            "",
            "🐌 Slowest Functions:",
        ]

        for i, agg in enumerate(self.get_slowest_functions(5), 1):
            trend_icon = {"improving": "📈", "degrading": "📉", "stable": "➡️"}[agg.performance_trend]
            report_lines.append(
                f"  {i}. {agg.function_name}: {agg.avg_execution_time:.3f}s avg {trend_icon}"
            )

        report_lines.extend([
            "",
            "🔥 Most Called Functions:",
        ])

        for i, agg in enumerate(self.get_most_called_functions(5), 1):
            report_lines.append(
                f"  {i}. {agg.function_name}: {agg.call_count} calls, {agg.success_rate:.1%} success"
            )

        # Add performance warnings
        warnings = self._generate_warnings()
        if warnings:
            report_lines.extend([
                "",
                "⚠️ Performance Warnings:",
            ])
            for warning in warnings:
                report_lines.append(f"  • {warning}")

        return "\n".join(report_lines)

    def _generate_warnings(self) -> List[str]:
        """Generate performance warnings."""
        warnings = []

        for agg in self.aggregates.values():
            # Slow functions
            if agg.avg_execution_time > 1.0:
                warnings.append(
                    f"{agg.function_name} is averaging {agg.avg_execution_time:.2f}s per call"
                )

            # Degrading performance
            if agg.performance_trend == "degrading" and agg.last_24h_calls > 10:
                warnings.append(
                    f"{agg.function_name} performance is degrading (trend analysis)"
                )

            # Low success rate
            if agg.success_rate < 0.95 and agg.call_count > 5:
                warnings.append(
                    f"{agg.function_name} has low success rate: {agg.success_rate:.1%}"
                )

            # High memory usage
            if agg.avg_memory_usage > 100:  # MB
                warnings.append(
                    f"{agg.function_name} uses high memory: {agg.avg_memory_usage:.1f}MB avg"
                )

        return warnings

    def _start_cleanup_thread(self) -> None:
        """Start background thread for periodic cleanup."""
        def cleanup_worker():
            while self.monitoring_active:
                time.sleep(300)  # 5 minutes
                self._cleanup_old_metrics()

        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()

    def _cleanup_old_metrics(self) -> None:
        """Remove old metrics to prevent memory bloat."""
        cutoff = datetime.now() - timedelta(hours=24)

        with self.lock:
            # Keep recent metrics and a sample of older ones
            recent_metrics = [m for m in self.metrics if m.timestamp > cutoff]
            old_metrics = [m for m in self.metrics if m.timestamp <= cutoff]

            # Keep every 10th old metric for historical trends
            sampled_old = old_metrics[::10]

            self.metrics = recent_metrics + sampled_old

    def stop_monitoring(self) -> None:
        """Stop the monitoring system."""
        self.monitoring_active = False

# Global monitor instance
_monitor = PerformanceMonitor()

def monitor_performance(include_args: bool = False,
                       threshold_ms: float = 0):
    """Decorator to monitor function performance."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not _monitor.monitoring_active:
                return func(*args, **kwargs)

            # Get initial measurements
            start_time = time.time()
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB

            args_hash = None
            if include_args:
                # Create a simple hash of arguments for tracking
                args_hash = str(hash(str(args) + str(sorted(kwargs.items()))))[:8]

            success = True
            error_message = None

            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                # Calculate final measurements
                end_time = time.time()
                execution_time = end_time - start_time

                # Only record if above threshold
                if execution_time * 1000 >= threshold_ms:
                    final_memory = process.memory_info().rss / 1024 / 1024  # MB
                    memory_usage = final_memory - initial_memory
                    cpu_percentage = process.cpu_percent()

                    metric = PerformanceMetric(
                        function_name=f"{func.__module__}.{func.__qualname__}",
                        execution_time=execution_time,
                        memory_usage=memory_usage,
                        cpu_percentage=cpu_percentage,
                        timestamp=datetime.now(),
                        args_hash=args_hash,
                        success=success,
                        error_message=error_message
                    )

                    _monitor.record_metric(metric)

        return wrapper
    return decorator

class PerformanceContext:
    """Context manager for monitoring code blocks."""

    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.initial_memory = None

    def __enter__(self):
        self.start_time = time.time()
        process = psutil.Process()
        self.initial_memory = process.memory_info().rss / 1024 / 1024
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        execution_time = end_time - self.start_time

        process = psutil.Process()
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_usage = final_memory - self.initial_memory
        cpu_percentage = process.cpu_percent()

        success = exc_type is None
        error_message = str(exc_val) if exc_val else None

        metric = PerformanceMetric(
            function_name=self.operation_name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_percentage=cpu_percentage,
            timestamp=datetime.now(),
            success=success,
            error_message=error_message
        )

        _monitor.record_metric(metric)

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    return _monitor

def performance_report() -> str:
    """Get current performance report."""
    return _monitor.generate_report()

# CLI functions
def print_performance_dashboard():
    """Print a real-time performance dashboard."""
    import os
    import time

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🚀 TKA modern Performance Dashboard")
        print("=" * 50)
        print(_monitor.generate_report())
        print("\nPress Ctrl+C to exit...")

        try:
            time.sleep(5)
        except KeyboardInterrupt:
            break

def main():
    """CLI entry point for performance monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="TKA modern Performance Monitor")
    parser.add_argument("--dashboard", action="store_true",
                       help="Show real-time performance dashboard")
    parser.add_argument("--report", action="store_true",
                       help="Generate performance report")
    parser.add_argument("--export", type=str,
                       help="Export metrics to JSON file")

    args = parser.parse_args()

    if args.dashboard:
        print_performance_dashboard()
    elif args.report:
        print(performance_report())
    elif args.export:
        _monitor.export_metrics(Path(args.export))
        print(f"✅ Metrics exported to {args.export}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Usage Examples:**

```python
# Using the decorator
@monitor_performance(threshold_ms=10)
def heavy_computation():
    # This function will be automatically monitored
    time.sleep(1)
    return "result"

# Using context manager
with PerformanceContext("sequence_generation"):
    # Generate sequence
    sequence = create_complex_sequence()

# CLI usage
python src/infrastructure/monitoring/performance_monitor.py --dashboard
python src/infrastructure/monitoring/performance_monitor.py --report
python src/infrastructure/monitoring/performance_monitor.py --export performance.json
```
