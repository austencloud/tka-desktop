"""
TKA Desktop Performance Monitoring

This module provides performance monitoring infrastructure for tracking
operation duration, memory usage, and other performance metrics across
the TKA Desktop application.

COMPONENTS:
- PerformanceMonitor: Core monitoring class for metric collection
- monitor_performance: Decorator for automatic performance tracking
- PerformanceReport: Reporting and analysis utilities
"""

import time
import psutil
import logging
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from functools import wraps
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Individual performance metric data."""

    operation: str
    duration_ms: float
    memory_mb: float
    timestamp: float
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationStats:
    """Aggregated statistics for an operation."""

    operation: str
    count: int = 0
    total_duration_ms: float = 0.0
    max_duration_ms: float = 0.0
    min_duration_ms: float = float("inf")
    avg_duration_ms: float = 0.0
    total_memory_mb: float = 0.0
    max_memory_mb: float = 0.0
    avg_memory_mb: float = 0.0
    recent_metrics: deque = field(default_factory=lambda: deque(maxlen=100))

    def update(self, metric: PerformanceMetric):
        """Update statistics with a new metric."""
        self.count += 1
        self.total_duration_ms += metric.duration_ms
        self.max_duration_ms = max(self.max_duration_ms, metric.duration_ms)
        self.min_duration_ms = min(self.min_duration_ms, metric.duration_ms)
        self.avg_duration_ms = self.total_duration_ms / self.count

        self.total_memory_mb += metric.memory_mb
        self.max_memory_mb = max(self.max_memory_mb, metric.memory_mb)
        self.avg_memory_mb = self.total_memory_mb / self.count

        self.recent_metrics.append(metric)


class PerformanceMonitor:
    """
    Performance monitoring system for TKA Desktop.

    Tracks operation performance metrics including duration, memory usage,
    and provides aggregated statistics and reporting capabilities.
    """

    def __init__(self, max_metrics: int = 10000):
        """
        Initialize performance monitor.

        Args:
            max_metrics: Maximum number of metrics to retain in memory
        """
        self.max_metrics = max_metrics
        self.metrics: deque = deque(maxlen=max_metrics)
        self.operation_stats: Dict[str, OperationStats] = {}
        self._lock = threading.Lock()
        self._enabled = True

        # Performance thresholds (adjusted for memory delta measurements)
        self.warning_thresholds = {
            "duration_ms": 1000.0,  # 1 second
            "memory_mb": 50.0,  # 50 MB delta (was 100 MB total)
        }

        self.error_thresholds = {
            "duration_ms": 5000.0,  # 5 seconds
            "memory_mb": 200.0,  # 200 MB delta (was 500 MB total)
        }

    def record_metric(
        self,
        operation: str,
        duration_ms: float,
        memory_mb: float,
        context: Optional[Dict[str, Any]] = None,
    ):
        """
        Record a performance metric.

        Args:
            operation: Name of the operation
            duration_ms: Duration in milliseconds
            memory_mb: Memory usage in megabytes
            context: Additional context information
        """
        if not self._enabled:
            return

        metric = PerformanceMetric(
            operation=operation,
            duration_ms=duration_ms,
            memory_mb=memory_mb,
            timestamp=time.time(),
            context=context or {},
        )

        with self._lock:
            self.metrics.append(metric)

            # Update operation statistics
            if operation not in self.operation_stats:
                self.operation_stats[operation] = OperationStats(operation=operation)

            self.operation_stats[operation].update(metric)

        # Check thresholds and log warnings/errors
        self._check_thresholds(metric)

    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds warning or error thresholds."""
        # Check duration thresholds
        if metric.duration_ms > self.error_thresholds["duration_ms"]:
            logger.error(
                f"Performance ERROR: {metric.operation} took {metric.duration_ms:.1f}ms "
                f"(threshold: {self.error_thresholds['duration_ms']}ms)"
            )
        elif metric.duration_ms > self.warning_thresholds["duration_ms"]:
            logger.warning(
                f"Performance WARNING: {metric.operation} took {metric.duration_ms:.1f}ms "
                f"(threshold: {self.warning_thresholds['duration_ms']}ms)"
            )

        # Check memory thresholds
        if metric.memory_mb > self.error_thresholds["memory_mb"]:
            logger.error(
                f"Memory ERROR: {metric.operation} used {metric.memory_mb:.1f}MB "
                f"(threshold: {self.error_thresholds['memory_mb']}MB)"
            )
        elif metric.memory_mb > self.warning_thresholds["memory_mb"]:
            logger.warning(
                f"Memory WARNING: {metric.operation} used {metric.memory_mb:.1f}MB "
                f"(threshold: {self.warning_thresholds['memory_mb']}MB)"
            )

    def get_operation_stats(self, operation: str) -> Optional[OperationStats]:
        """Get statistics for a specific operation."""
        with self._lock:
            return self.operation_stats.get(operation)

    def get_all_stats(self) -> Dict[str, OperationStats]:
        """Get statistics for all operations."""
        with self._lock:
            return dict(self.operation_stats)

    def get_slowest_operations(self, limit: int = 10) -> List[OperationStats]:
        """Get the slowest operations by average duration."""
        with self._lock:
            stats = list(self.operation_stats.values())
            return sorted(stats, key=lambda s: s.avg_duration_ms, reverse=True)[:limit]

    def get_memory_intensive_operations(self, limit: int = 10) -> List[OperationStats]:
        """Get the most memory-intensive operations."""
        with self._lock:
            stats = list(self.operation_stats.values())
            return sorted(stats, key=lambda s: s.avg_memory_mb, reverse=True)[:limit]

    def clear_metrics(self):
        """Clear all collected metrics and statistics."""
        with self._lock:
            self.metrics.clear()
            self.operation_stats.clear()

    def set_enabled(self, enabled: bool):
        """Enable or disable performance monitoring."""
        self._enabled = enabled

    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        with self._lock:
            total_operations = sum(
                stats.count for stats in self.operation_stats.values()
            )

            return {
                "summary": {
                    "total_operations": total_operations,
                    "unique_operations": len(self.operation_stats),
                    "total_metrics": len(self.metrics),
                    "monitoring_enabled": self._enabled,
                },
                "slowest_operations": [
                    {
                        "operation": stats.operation,
                        "avg_duration_ms": round(stats.avg_duration_ms, 2),
                        "max_duration_ms": round(stats.max_duration_ms, 2),
                        "count": stats.count,
                    }
                    for stats in self.get_slowest_operations(5)
                ],
                "memory_intensive_operations": [
                    {
                        "operation": stats.operation,
                        "avg_memory_mb": round(stats.avg_memory_mb, 2),
                        "max_memory_mb": round(stats.max_memory_mb, 2),
                        "count": stats.count,
                    }
                    for stats in self.get_memory_intensive_operations(5)
                ],
                "thresholds": {
                    "warning": self.warning_thresholds,
                    "error": self.error_thresholds,
                },
            }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(
    operation_name: Optional[str] = None, context: Optional[Dict[str, Any]] = None
):
    """
    Decorator to monitor operation performance.

    Args:
        operation_name: Custom operation name (defaults to class.method)
        context: Additional context to include with metrics

    Returns:
        Decorated function with performance monitoring

    Example:
        @monitor_performance("layout_calculation")
        def calculate_layout(self, data: LayoutData) -> LayoutResult:
            # Implementation here
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine operation name
            if operation_name:
                op_name = operation_name
            elif args and hasattr(args[0], "__class__"):
                op_name = f"{args[0].__class__.__name__}.{func.__name__}"
            else:
                op_name = func.__name__

            # Start monitoring
            start_time = time.perf_counter()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Record metrics
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024

                duration_ms = (end_time - start_time) * 1000
                memory_mb = abs(
                    end_memory - start_memory
                )  # Memory delta used by operation

                # Merge provided context with runtime context
                runtime_context = {
                    "function": func.__name__,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs) if kwargs else 0,
                }

                if context:
                    runtime_context.update(context)

                performance_monitor.record_metric(
                    operation=op_name,
                    duration_ms=duration_ms,
                    memory_mb=memory_mb,
                    context=runtime_context,
                )

        return wrapper

    return decorator


def set_performance_thresholds(
    warning_duration_ms: Optional[float] = None,
    error_duration_ms: Optional[float] = None,
    warning_memory_mb: Optional[float] = None,
    error_memory_mb: Optional[float] = None,
):
    """
    Configure performance monitoring thresholds.

    Args:
        warning_duration_ms: Warning threshold for operation duration
        error_duration_ms: Error threshold for operation duration
        warning_memory_mb: Warning threshold for memory usage
        error_memory_mb: Error threshold for memory usage
    """
    if warning_duration_ms is not None:
        performance_monitor.warning_thresholds["duration_ms"] = warning_duration_ms

    if error_duration_ms is not None:
        performance_monitor.error_thresholds["duration_ms"] = error_duration_ms

    if warning_memory_mb is not None:
        performance_monitor.warning_thresholds["memory_mb"] = warning_memory_mb

    if error_memory_mb is not None:
        performance_monitor.error_thresholds["memory_mb"] = error_memory_mb


def get_performance_report() -> Dict[str, Any]:
    """Get a comprehensive performance report."""
    return performance_monitor.generate_report()


def clear_performance_data():
    """Clear all performance monitoring data."""
    performance_monitor.clear_metrics()


def enable_performance_monitoring(enabled: bool = True):
    """Enable or disable performance monitoring globally."""
    performance_monitor.set_enabled(enabled)
