"""
TKA Desktop Qt Integration Module

A+ Enhancement: Comprehensive Qt integration with version detection,
automatic lifecycle management, resource pooling, and memory leak prevention.

ARCHITECTURE: Provides enterprise-grade Qt integration patterns including:
- Qt Version Detection and Compatibility Layer
- Automatic Object Lifecycle Management
- Qt Resource Pooling for Performance
- Smart Pointer Management for Qt Objects
- Memory Leak Detection and Prevention
- Threading Bridge for Async/Await Support

EXPORTS:
- QtCompatibilityManager: Qt version detection and adaptation
- AutoManagedWidget: Smart widget base with automatic cleanup
- QtResourceManager: Resource pooling for expensive Qt objects
- QtMemoryLeakDetector: Automatic memory leak detection
- SmartQtPointer: Smart pointer for Qt object management
- QtAsyncBridge: Threading bridge for async operations
"""

# Qt Compatibility Layer
from .qt_compatibility import (
    QtCompatibilityManager,
    QtEnvironment,
    QtVersion,
    QtVariant,
    qt_compat,
)

# Automatic Lifecycle Management
from .lifecycle_management import (
    AutoManagedWidget,
    QtObjectFactory,
    qt_factory,
)

# Resource Management
from .resource_management import (
    QtResourceManager,
    ResourcePool,
    PooledResource,
    pooled_pen,
    pooled_brush,
    pooled_font,
    qt_resources,
)

# Memory Management
from .memory_management import (
    QtMemoryLeakDetector,
    SmartQtPointer,
    MemorySnapshot,
    LeakReport,
    memory_detector,
)

# Threading Integration
from .threading_integration import (
    QtAsyncBridge,
    AsyncQtWidget,
    qt_async_bridge,
)

__all__ = [
    # Compatibility
    "QtCompatibilityManager",
    "QtEnvironment",
    "QtVersion",
    "QtVariant",
    "qt_compat",
    # Lifecycle Management
    "AutoManagedWidget",
    "QtObjectFactory",
    "qt_factory",
    # Resource Management
    "QtResourceManager",
    "ResourcePool",
    "PooledResource",
    "pooled_pen",
    "pooled_brush",
    "pooled_font",
    "qt_resources",
    # Memory Management
    "QtMemoryLeakDetector",
    "SmartQtPointer",
    "MemorySnapshot",
    "LeakReport",
    "memory_detector",
    # Threading Integration
    "QtAsyncBridge",
    "AsyncQtWidget",
    "qt_async_bridge",
]
