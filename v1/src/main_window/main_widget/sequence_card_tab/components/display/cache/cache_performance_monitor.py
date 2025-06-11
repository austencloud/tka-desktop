"""
Cache Performance Monitor - Handles performance monitoring and memory management.

Extracted from the monolithic ImageProcessor class to follow SRP.
"""

import logging
import gc
from typing import Optional, Dict, Any


class CachePerformanceMonitor:
    """
    Handles cache performance monitoring and memory management.

    Responsibilities:
    - Memory usage monitoring
    - Performance statistics tracking
    - Memory cleanup operations
    - Performance logging
    """

    def __init__(self, max_memory_mb: int = 500, check_interval: int = 10):
        self.max_memory_mb = max_memory_mb
        self.check_interval = check_interval
        self.logger = logging.getLogger(__name__)

        # Statistics
        self.cache_operations = 0
        self.memory_cleanups = 0
        self.disk_cache_hits = 0
        self.disk_cache_misses = 0

        # Try to import psutil for memory monitoring
        try:
            import psutil

            self.psutil = psutil
            self.memory_monitoring_available = True
        except ImportError:
            self.psutil = None
            self.memory_monitoring_available = False
            self.logger.warning("psutil not available - memory monitoring disabled")

    def record_cache_operation(self) -> None:
        """Record a cache operation and check memory if needed."""
        self.cache_operations += 1
        if self.cache_operations % self.check_interval == 0:
            self.check_and_cleanup_memory()

    def record_disk_cache_hit(self) -> None:
        """Record a disk cache hit."""
        self.disk_cache_hits += 1

    def record_disk_cache_miss(self) -> None:
        """Record a disk cache miss."""
        self.disk_cache_misses += 1

    def check_and_cleanup_memory(self) -> bool:
        """
        Check memory usage and cleanup if necessary.

        Returns:
            True if cleanup was performed, False otherwise
        """
        if not self.memory_monitoring_available:
            return False

        try:
            # Get current memory usage
            process = self.psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)

            if memory_mb > self.max_memory_mb:
                self.logger.info(
                    f"Memory usage high ({memory_mb:.1f}MB), cleanup recommended"
                )

                # Force garbage collection
                gc.collect()

                # Check memory after cleanup
                new_memory_mb = process.memory_info().rss / (1024 * 1024)
                self.logger.info(
                    f"Memory cleanup completed: {memory_mb:.1f}MB -> {new_memory_mb:.1f}MB"
                )

                self.memory_cleanups += 1
                return True

        except Exception as e:
            self.logger.warning(f"Error during memory cleanup: {e}")

        return False

    def get_current_memory_mb(self) -> float:
        """
        Get current memory usage in MB.

        Returns:
            Memory usage in MB, or 0 if monitoring unavailable
        """
        if not self.memory_monitoring_available:
            return 0.0

        try:
            process = self.psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0.0

    def get_performance_stats(
        self, disk_cache_stats: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive performance statistics.

        Args:
            disk_cache_stats: Optional disk cache statistics

        Returns:
            Dictionary with performance metrics
        """
        disk_hit_rate = 0
        if self.disk_cache_hits + self.disk_cache_misses > 0:
            disk_hit_rate = (
                self.disk_cache_hits / (self.disk_cache_hits + self.disk_cache_misses)
            ) * 100

        stats = {
            "memory_monitoring_available": self.memory_monitoring_available,
            "current_memory_mb": round(self.get_current_memory_mb(), 1),
            "max_memory_mb": self.max_memory_mb,
            "cache_operations": self.cache_operations,
            "memory_cleanups": self.memory_cleanups,
            "disk_cache_hits": self.disk_cache_hits,
            "disk_cache_misses": self.disk_cache_misses,
            "disk_hit_rate_percent": round(disk_hit_rate, 1),
        }

        if disk_cache_stats:
            stats["disk_cache_stats"] = disk_cache_stats

        return stats

    def log_performance_stats(self, cache_stats: Dict[str, Any]) -> None:
        """
        Log current performance statistics.

        Args:
            cache_stats: Cache statistics to include in log
        """
        stats = self.get_performance_stats()

        self.logger.info(
            f"Performance Stats - "
            f"Memory: {stats['current_memory_mb']}MB, "
            f"Operations: {stats['cache_operations']}, "
            f"Cleanups: {stats['memory_cleanups']}, "
            f"Disk Hit Rate: {stats['disk_hit_rate_percent']}%"
        )

    def reset_stats(self) -> None:
        """Reset all performance statistics."""
        self.cache_operations = 0
        self.memory_cleanups = 0
        self.disk_cache_hits = 0
        self.disk_cache_misses = 0
        self.logger.debug("Performance statistics reset")
