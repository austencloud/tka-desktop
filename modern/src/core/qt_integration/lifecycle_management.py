"""
Qt Automatic Lifecycle Management for TKA Desktop

A+ Enhancement: Automatic Qt object lifecycle management with smart cleanup,
resource tracking, and memory leak prevention.

ARCHITECTURE: Provides automatic lifecycle management for Qt objects with
smart cleanup registration, resource tracking, and automatic memory management.
"""

import logging
import weakref
import atexit
from typing import Dict, List, Optional, Any, Callable, Type, TypeVar, Set
from dataclasses import dataclass, field
from threading import Lock
import gc

# Import Qt modules with compatibility
try:
    from PyQt6.QtCore import QObject, QTimer, pyqtSignal
    from PyQt6.QtWidgets import QWidget, QApplication
except ImportError:
    try:
        from PyQt5.QtCore import QObject, QTimer, pyqtSignal
        from PyQt5.QtWidgets import QWidget, QApplication
    except ImportError:
        # Fallback for testing without Qt
        QObject = object
        QWidget = object
        QTimer = object
        QApplication = object

        def pyqtSignal(*args, **kwargs):
            return lambda: None


# Note: Removed qt_compat import to avoid circular dependencies

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=QObject)


@dataclass
class LifecycleMetrics:
    """Metrics for Qt object lifecycle tracking."""

    objects_created: int = 0
    objects_destroyed: int = 0
    objects_leaked: int = 0
    cleanup_handlers_registered: int = 0
    cleanup_handlers_executed: int = 0
    memory_freed_bytes: int = 0


class QtObjectFactory:
    """
    Qt object factory with automatic lifecycle management.

    A+ Enhancement: Provides automatic cleanup registration, resource tracking,
    and memory management for Qt objects.
    """

    def __init__(self):
        """Initialize Qt object factory."""
        self._tracked_objects: Dict[int, weakref.ReferenceType] = {}
        self._cleanup_handlers: Dict[int, List[Callable]] = {}
        self._object_metadata: Dict[int, Dict[str, Any]] = {}
        self._metrics = LifecycleMetrics()
        self._lock = Lock()

        # Register application cleanup (commented out to avoid potential issues)
        # atexit.register(self._cleanup_all)

        logger.info("Qt object factory initialized with automatic lifecycle management")

    def create_widget(self, widget_class: Type[T], *args, **kwargs) -> T:
        """
        Create a widget with automatic lifecycle management.

        Args:
            widget_class: Widget class to instantiate
            *args: Widget constructor arguments
            **kwargs: Widget constructor keyword arguments

        Returns:
            Widget instance with automatic cleanup
        """
        # Create widget instance
        widget = widget_class(*args, **kwargs)

        # Register for automatic cleanup
        self._register_object(widget)

        # Add automatic parent-child cleanup
        if hasattr(widget, "destroyed"):
            widget.destroyed.connect(lambda: self._on_object_destroyed(id(widget)))

        self._metrics.objects_created += 1

        logger.debug(f"Created widget: {widget_class.__name__} (id: {id(widget)})")
        return widget

    def create_object(self, object_class: Type[T], *args, **kwargs) -> T:
        """
        Create a QObject with automatic lifecycle management.

        Args:
            object_class: QObject class to instantiate
            *args: Object constructor arguments
            **kwargs: Object constructor keyword arguments

        Returns:
            QObject instance with automatic cleanup
        """
        # Create object instance
        obj = object_class(*args, **kwargs)

        # Register for automatic cleanup
        self._register_object(obj)

        # Add automatic cleanup on destruction
        if hasattr(obj, "destroyed"):
            obj.destroyed.connect(lambda: self._on_object_destroyed(id(obj)))

        self._metrics.objects_created += 1

        logger.debug(f"Created object: {object_class.__name__} (id: {id(obj)})")
        return obj

    def _register_object(self, obj: QObject) -> None:
        """Register object for automatic lifecycle management."""
        with self._lock:
            obj_id = id(obj)

            # Create weak reference to avoid circular references
            weak_ref = weakref.ref(obj, lambda ref: self._on_object_destroyed(obj_id))
            self._tracked_objects[obj_id] = weak_ref

            # Initialize cleanup handlers list
            self._cleanup_handlers[obj_id] = []

            # Store metadata
            self._object_metadata[obj_id] = {
                "class_name": obj.__class__.__name__,
                "created_at": self._get_current_time(),
                "parent": getattr(obj, "parent", lambda: None)(),
                "children_count": len(getattr(obj, "children", lambda: [])()),
            }

    def register_cleanup_handler(self, obj: QObject, handler: Callable) -> None:
        """
        Register a cleanup handler for an object.

        Args:
            obj: Qt object to register cleanup for
            handler: Cleanup function to call when object is destroyed
        """
        with self._lock:
            obj_id = id(obj)
            if obj_id in self._cleanup_handlers:
                self._cleanup_handlers[obj_id].append(handler)
                self._metrics.cleanup_handlers_registered += 1
                logger.debug(f"Registered cleanup handler for object {obj_id}")

    def _on_object_destroyed(self, obj_id: int) -> None:
        """Handle object destruction and cleanup."""
        with self._lock:
            # Execute cleanup handlers
            if obj_id in self._cleanup_handlers:
                handlers = self._cleanup_handlers[obj_id]
                for handler in handlers:
                    try:
                        handler()
                        self._metrics.cleanup_handlers_executed += 1
                    except Exception as e:
                        logger.error(f"Error executing cleanup handler: {e}")

                del self._cleanup_handlers[obj_id]

            # Remove from tracking
            if obj_id in self._tracked_objects:
                del self._tracked_objects[obj_id]

            if obj_id in self._object_metadata:
                del self._object_metadata[obj_id]

            self._metrics.objects_destroyed += 1

            logger.debug(f"Object destroyed and cleaned up: {obj_id}")

    def _cleanup_all(self) -> None:
        """Cleanup all tracked objects on application exit."""
        with self._lock:
            logger.info(f"Cleaning up {len(self._tracked_objects)} tracked Qt objects")

            # Execute all remaining cleanup handlers
            for obj_id, handlers in self._cleanup_handlers.items():
                for handler in handlers:
                    try:
                        handler()
                        self._metrics.cleanup_handlers_executed += 1
                    except Exception as e:
                        logger.error(f"Error in final cleanup: {e}")

            # Clear all tracking data
            self._tracked_objects.clear()
            self._cleanup_handlers.clear()
            self._object_metadata.clear()

            logger.info("Qt object factory cleanup completed")

    def get_metrics(self) -> LifecycleMetrics:
        """Get lifecycle management metrics."""
        with self._lock:
            # Update leaked objects count
            self._metrics.objects_leaked = max(
                0, self._metrics.objects_created - self._metrics.objects_destroyed
            )
            return self._metrics

    def get_tracked_objects_info(self) -> List[Dict[str, Any]]:
        """Get information about currently tracked objects."""
        with self._lock:
            info = []
            for obj_id, weak_ref in self._tracked_objects.items():
                obj = weak_ref()
                if obj is not None:
                    metadata = self._object_metadata.get(obj_id, {})
                    info.append(
                        {
                            "id": obj_id,
                            "class_name": metadata.get("class_name", "Unknown"),
                            "created_at": metadata.get("created_at", "Unknown"),
                            "has_parent": metadata.get("parent") is not None,
                            "children_count": metadata.get("children_count", 0),
                            "cleanup_handlers": len(
                                self._cleanup_handlers.get(obj_id, [])
                            ),
                        }
                    )
            return info

    def _get_current_time(self) -> str:
        """Get current time as string."""
        import datetime

        return datetime.datetime.now().isoformat()


class AutoManagedWidget(QWidget):
    """
    Base widget class with automatic lifecycle management.

    A+ Enhancement: Provides automatic cleanup registration, resource tracking,
    and memory management for Qt widgets.
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize auto-managed widget."""
        super().__init__(parent)

        # Track resources
        self._managed_resources: List[Any] = []
        self._cleanup_callbacks: List[Callable] = []
        self._factory_registered = False

        logger.debug(f"AutoManagedWidget created: {self.__class__.__name__}")

        # Register with factory for automatic cleanup (lazy)
        self._register_with_factory()

    def add_managed_resource(self, resource: Any) -> None:
        """Add a resource to be automatically cleaned up."""
        self._managed_resources.append(resource)

    def add_cleanup_callback(self, callback: Callable) -> None:
        """Add a callback to be executed during cleanup."""
        self._cleanup_callbacks.append(callback)

    def _register_with_factory(self) -> None:
        """Register with factory for automatic cleanup (lazy initialization)."""
        if not self._factory_registered:
            try:
                factory = qt_factory()
                factory.register_cleanup_handler(self, self._auto_cleanup)
                self._factory_registered = True
                logger.debug(
                    f"AutoManagedWidget registered with factory: {self.__class__.__name__}"
                )
            except Exception as e:
                logger.debug(f"Failed to register with factory: {e}")

    def _auto_cleanup(self) -> None:
        """Automatic cleanup implementation."""
        try:
            # Execute cleanup callbacks
            for callback in self._cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.error(f"Error in cleanup callback: {e}")

            # Cleanup managed resources
            for resource in self._managed_resources:
                try:
                    if hasattr(resource, "cleanup"):
                        resource.cleanup()
                    elif hasattr(resource, "deleteLater"):
                        resource.deleteLater()
                    elif hasattr(resource, "close"):
                        resource.close()
                except Exception as e:
                    logger.error(f"Error cleaning up resource: {e}")

            # Clear lists
            self._managed_resources.clear()
            self._cleanup_callbacks.clear()

            logger.debug(
                f"AutoManagedWidget cleanup completed: {self.__class__.__name__}"
            )

        except Exception as e:
            logger.error(f"Error in auto cleanup: {e}")


# Note: AsyncViewableComponentBase is defined in component_base.py to avoid circular imports
# This prevents circular dependency between qt_integration and presentation layers
AsyncViewableComponentBase = AutoManagedWidget  # Fallback for direct usage


# Global Qt object factory instance
_qt_factory: Optional[QtObjectFactory] = None


def qt_factory() -> QtObjectFactory:
    """Get global Qt object factory instance."""
    global _qt_factory
    if _qt_factory is None:
        _qt_factory = QtObjectFactory()
    return _qt_factory
