"""
Qt Resource Management for TKA Desktop

A+ Enhancement: Advanced Qt resource pooling and management for optimal
performance and memory usage.

ARCHITECTURE: Provides resource pooling for expensive Qt objects (brushes, pens,
fonts, graphics items) with automatic lifecycle management and performance optimization.
"""

import logging
import weakref
from typing import Dict, List, Optional, Any, Callable, TypeVar, Generic, Tuple, Union
from dataclasses import dataclass, field
from threading import Lock
from collections import defaultdict
import hashlib

# Import Qt modules with compatibility
try:
    from PyQt6.QtGui import QPen, QBrush, QFont, QColor, QPainter
    from PyQt6.QtCore import Qt, QObject
    from PyQt6.QtWidgets import QGraphicsItem
except ImportError:
    try:
        from PyQt5.QtGui import QPen, QBrush, QFont, QColor, QPainter
        from PyQt5.QtCore import Qt, QObject
        from PyQt5.QtWidgets import QGraphicsItem
    except ImportError:
        # Fallback for testing without Qt
        QPen = object
        QBrush = object
        QFont = object
        QColor = object
        QPainter = object
        Qt = object
        QObject = object
        QGraphicsItem = object

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class ResourcePoolMetrics:
    """Metrics for resource pool performance."""

    total_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    objects_created: int = 0
    objects_reused: int = 0
    memory_saved_bytes: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        if self.total_requests == 0:
            return 0.0
        return self.cache_hits / self.total_requests

    @property
    def reuse_rate(self) -> float:
        """Calculate object reuse rate."""
        if self.objects_created == 0:
            return 0.0
        return self.objects_reused / (self.objects_created + self.objects_reused)


class ResourcePool(Generic[T]):
    """
    Generic resource pool for Qt objects.

    A+ Enhancement: Provides efficient resource pooling with automatic
    cleanup, size management, and performance optimization.
    """

    def __init__(
        self, resource_type: type, max_size: int = 100, cleanup_threshold: int = 150
    ):
        """
        Initialize resource pool.

        Args:
            resource_type: Type of resource to pool
            max_size: Maximum pool size
            cleanup_threshold: Size threshold for automatic cleanup
        """
        self.resource_type = resource_type
        self.max_size = max_size
        self.cleanup_threshold = cleanup_threshold

        # Pool storage
        self._available: List[T] = []
        self._in_use: Dict[int, T] = {}
        self._resource_cache: Dict[str, T] = {}

        # Metrics and management
        self._metrics = ResourcePoolMetrics()
        self._lock = Lock()
        self._creation_count = 0

        logger.debug(
            f"Resource pool created for {resource_type.__name__} (max_size: {max_size})"
        )

    def get_or_create(
        self, factory: Callable[[], T], cache_key: Optional[str] = None
    ) -> T:
        """
        Get resource from pool or create new one.

        Args:
            factory: Factory function to create new resource
            cache_key: Optional cache key for resource reuse

        Returns:
            Resource instance from pool or newly created
        """
        with self._lock:
            self._metrics.total_requests += 1

            # Try cache first if key provided
            if cache_key and cache_key in self._resource_cache:
                resource = self._resource_cache[cache_key]
                self._metrics.cache_hits += 1
                self._metrics.objects_reused += 1
                logger.debug(f"Resource cache hit: {cache_key}")
                return resource

            # Try to reuse from available pool
            if self._available:
                resource = self._available.pop()
                self._in_use[id(resource)] = resource
                self._metrics.objects_reused += 1

                # Cache if key provided
                if cache_key:
                    self._resource_cache[cache_key] = resource

                logger.debug(
                    f"Resource reused from pool: {self.resource_type.__name__}"
                )
                return resource

            # Create new resource
            resource = factory()
            self._in_use[id(resource)] = resource
            self._creation_count += 1
            self._metrics.objects_created += 1
            self._metrics.cache_misses += 1

            # Cache if key provided
            if cache_key:
                self._resource_cache[cache_key] = resource

            logger.debug(f"New resource created: {self.resource_type.__name__}")
            return resource

    def return_resource(self, resource: T) -> None:
        """
        Return resource to pool for reuse.

        Args:
            resource: Resource to return to pool
        """
        with self._lock:
            resource_id = id(resource)

            if resource_id in self._in_use:
                del self._in_use[resource_id]

                # Add to available pool if not full
                if len(self._available) < self.max_size:
                    self._available.append(resource)
                    logger.debug(
                        f"Resource returned to pool: {self.resource_type.__name__}"
                    )
                else:
                    # Pool is full, let resource be garbage collected
                    logger.debug(
                        f"Pool full, resource discarded: {self.resource_type.__name__}"
                    )

                # Cleanup if threshold exceeded
                if len(self._available) > self.cleanup_threshold:
                    self._cleanup_excess()

    def _cleanup_excess(self) -> None:
        """Cleanup excess resources from pool."""
        excess_count = len(self._available) - self.max_size
        if excess_count > 0:
            # Remove oldest resources
            for _ in range(excess_count):
                if self._available:
                    self._available.pop(0)

            logger.debug(f"Cleaned up {excess_count} excess resources")

    def clear(self) -> None:
        """Clear all resources from pool."""
        with self._lock:
            self._available.clear()
            self._in_use.clear()
            self._resource_cache.clear()
            logger.debug(f"Resource pool cleared: {self.resource_type.__name__}")

    def get_metrics(self) -> ResourcePoolMetrics:
        """Get resource pool metrics."""
        with self._lock:
            return ResourcePoolMetrics(
                total_requests=self._metrics.total_requests,
                cache_hits=self._metrics.cache_hits,
                cache_misses=self._metrics.cache_misses,
                objects_created=self._metrics.objects_created,
                objects_reused=self._metrics.objects_reused,
                memory_saved_bytes=self._estimate_memory_saved(),
            )

    def _estimate_memory_saved(self) -> int:
        """Estimate memory saved by resource pooling."""
        # Rough estimate: assume each reused object saves ~100 bytes
        return self._metrics.objects_reused * 100

    def get_pool_info(self) -> Dict[str, Any]:
        """Get detailed pool information."""
        with self._lock:
            return {
                "resource_type": self.resource_type.__name__,
                "max_size": self.max_size,
                "available_count": len(self._available),
                "in_use_count": len(self._in_use),
                "cached_count": len(self._resource_cache),
                "creation_count": self._creation_count,
                "metrics": self.get_metrics().__dict__,
            }


class QtResourceManager:
    """
    Qt resource manager with specialized pools for different Qt objects.

    A+ Enhancement: Provides centralized resource management with specialized
    pools for pens, brushes, fonts, and other expensive Qt objects.
    """

    def __init__(self):
        """Initialize Qt resource manager."""
        # Create specialized pools
        self.pen_pool = ResourcePool(QPen, max_size=50)
        self.brush_pool = ResourcePool(QBrush, max_size=50)
        self.font_pool = ResourcePool(QFont, max_size=30)

        # Resource creation counters
        self._creation_stats = defaultdict(int)
        self._lock = Lock()

        logger.info("Qt resource manager initialized with specialized pools")

    def get_pen(self, color: Any, width: int = 1, style: Any = None) -> Any:
        """
        Get pen from pool with specified properties.

        Args:
            color: Pen color
            width: Pen width
            style: Pen style

        Returns:
            QPen instance from pool or newly created
        """
        # Use default style if none provided
        pen_style = (
            style
            if style is not None
            else getattr(Qt, "SolidLine", 1) if hasattr(Qt, "SolidLine") else 1
        )

        # Create cache key from pen properties
        cache_key = self._create_pen_cache_key(color, width, pen_style)

        def create_pen():
            try:
                pen = QPen(color, width, pen_style)
            except:
                # Fallback for compatibility
                pen = QPen()
                if hasattr(pen, "setColor"):
                    pen.setColor(color)
                if hasattr(pen, "setWidth"):
                    pen.setWidth(width)
            self._creation_stats["pen"] += 1
            return pen

        return self.pen_pool.get_or_create(create_pen, cache_key)

    def get_brush(self, color: Any, style: Any = None) -> Any:
        """
        Get brush from pool with specified properties.

        Args:
            color: Brush color
            style: Brush style

        Returns:
            QBrush instance from pool or newly created
        """
        # Use default style if none provided
        brush_style = (
            style
            if style is not None
            else getattr(Qt, "SolidPattern", 1) if hasattr(Qt, "SolidPattern") else 1
        )

        # Create cache key from brush properties
        cache_key = self._create_brush_cache_key(color, brush_style)

        def create_brush():
            try:
                brush = QBrush(color, brush_style)
            except:
                # Fallback for compatibility
                brush = QBrush()
                if hasattr(brush, "setColor"):
                    brush.setColor(color)
            self._creation_stats["brush"] += 1
            return brush

        return self.brush_pool.get_or_create(create_brush, cache_key)

    def get_font(
        self, family: str, size: int, weight: int = 50, italic: bool = False
    ) -> Any:
        """
        Get font from pool with specified properties.

        Args:
            family: Font family name
            size: Font size
            weight: Font weight
            italic: Whether font is italic

        Returns:
            QFont instance from pool or newly created
        """
        # Create cache key from font properties
        cache_key = self._create_font_cache_key(family, size, weight, italic)

        def create_font():
            font = QFont(family, size, weight, italic)
            self._creation_stats["font"] += 1
            return font

        return self.font_pool.get_or_create(create_font, cache_key)

    def _create_pen_cache_key(
        self, color: QColor, width: int, style: Qt.PenStyle
    ) -> str:
        """Create cache key for pen properties."""
        key_data = f"pen_{color.name()}_{width}_{style.value if hasattr(style, 'value') else style}"
        return hashlib.md5(key_data.encode()).hexdigest()[:8]

    def _create_brush_cache_key(self, color: QColor, style: Qt.BrushStyle) -> str:
        """Create cache key for brush properties."""
        key_data = (
            f"brush_{color.name()}_{style.value if hasattr(style, 'value') else style}"
        )
        return hashlib.md5(key_data.encode()).hexdigest()[:8]

    def _create_font_cache_key(
        self, family: str, size: int, weight: int, italic: bool
    ) -> str:
        """Create cache key for font properties."""
        key_data = f"font_{family}_{size}_{weight}_{italic}"
        return hashlib.md5(key_data.encode()).hexdigest()[:8]

    def return_pen(self, pen: QPen) -> None:
        """Return pen to pool."""
        self.pen_pool.return_resource(pen)

    def return_brush(self, brush: QBrush) -> None:
        """Return brush to pool."""
        self.brush_pool.return_resource(brush)

    def return_font(self, font: QFont) -> None:
        """Return font to pool."""
        self.font_pool.return_resource(font)

    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for all resource pools."""
        with self._lock:
            return {
                "pen_pool": self.pen_pool.get_pool_info(),
                "brush_pool": self.brush_pool.get_pool_info(),
                "font_pool": self.font_pool.get_pool_info(),
                "creation_stats": dict(self._creation_stats),
                "total_memory_saved": (
                    self.pen_pool.get_metrics().memory_saved_bytes
                    + self.brush_pool.get_metrics().memory_saved_bytes
                    + self.font_pool.get_metrics().memory_saved_bytes
                ),
            }

    def clear_all_pools(self) -> None:
        """Clear all resource pools."""
        self.pen_pool.clear()
        self.brush_pool.clear()
        self.font_pool.clear()
        self._creation_stats.clear()
        logger.info("All Qt resource pools cleared")


# ============================================================================
# CONVENIENCE DECORATORS AND FUNCTIONS - A+ Enhancement
# ============================================================================


class PooledResource:
    """Context manager for pooled Qt resources."""

    def __init__(self, resource: Any, pool: ResourcePool, return_func: Callable):
        self.resource = resource
        self.pool = pool
        self.return_func = return_func

    def __enter__(self):
        return self.resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.return_func(self.resource)


def pooled_pen(
    color: QColor, width: int = 1, style: Qt.PenStyle = Qt.PenStyle.SolidLine
) -> PooledResource:
    """Get pooled pen with automatic return."""
    pen = qt_resources().get_pen(color, width, style)
    return PooledResource(pen, qt_resources().pen_pool, qt_resources().return_pen)


def pooled_brush(
    color: QColor, style: Qt.BrushStyle = Qt.BrushStyle.SolidPattern
) -> PooledResource:
    """Get pooled brush with automatic return."""
    brush = qt_resources.get_brush(color, style)
    return PooledResource(brush, qt_resources.brush_pool, qt_resources.return_brush)


def pooled_font(
    family: str, size: int, weight: int = 50, italic: bool = False
) -> PooledResource:
    """Get pooled font with automatic return."""
    font = qt_resources.get_font(family, size, weight, italic)
    return PooledResource(font, qt_resources.font_pool, qt_resources.return_font)


# Global Qt resource manager instance
_qt_resources: Optional[QtResourceManager] = None


def qt_resources() -> QtResourceManager:
    """Get global Qt resource manager instance."""
    global _qt_resources
    if _qt_resources is None:
        _qt_resources = QtResourceManager()
    return _qt_resources
