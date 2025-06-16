"""
Core components for thumbnail processing using coordinator pattern.

This package contains the refactored components that were extracted from
the monolithic ThumbnailImageLabel class to follow the Single Responsibility Principle.
"""

from .thumbnail_coordinator import ThumbnailCoordinator
from .thumbnail_processor import ThumbnailProcessor
from .thumbnail_cache_manager import ThumbnailCacheManager
from .thumbnail_event_handler import ThumbnailEventHandler
from .thumbnail_size_calculator import ThumbnailSizeCalculator

__all__ = [
    "ThumbnailCoordinator",
    "ThumbnailProcessor", 
    "ThumbnailCacheManager",
    "ThumbnailEventHandler",
    "ThumbnailSizeCalculator",
]
