# src/main_window/main_widget/sequence_card_tab/utils/cache_utils.py
import time
import hashlib
from typing import Dict, Optional, Any
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize


class ThumbnailCache:
    """
    Cache for sequence card thumbnails to improve performance.
    
    This class provides:
    1. In-memory caching of thumbnails
    2. Size-based thumbnail generation
    3. Automatic cache cleanup
    4. Thread-safe operations
    """
    
    def __init__(self, max_size: int = 100):
        """
        Initialize the thumbnail cache.
        
        Args:
            max_size: Maximum number of thumbnails to cache (default: 100)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.access_times: Dict[str, float] = {}
    
    def get(self, path: str, size: QSize) -> Optional[QPixmap]:
        """
        Get a thumbnail from the cache.
        
        Args:
            path: Path to the original image
            size: Desired thumbnail size
            
        Returns:
            QPixmap thumbnail or None if not in cache
        """
        # Create a cache key that includes the path and size
        key = self._create_key(path, size)
        
        # Check if the key exists in the cache
        if key in self.cache:
            # Update access time
            self.access_times[key] = time.time()
            
            # Return the cached thumbnail
            return self.cache[key]["pixmap"]
        
        return None
    
    def put(self, path: str, size: QSize, pixmap: QPixmap) -> None:
        """
        Add a thumbnail to the cache.
        
        Args:
            path: Path to the original image
            size: Thumbnail size
            pixmap: Thumbnail pixmap
        """
        # Create a cache key
        key = self._create_key(path, size)
        
        # Check if we need to clean up the cache
        if len(self.cache) >= self.max_size:
            self._cleanup()
        
        # Add to cache
        self.cache[key] = {
            "path": path,
            "size": size,
            "pixmap": pixmap,
        }
        
        # Set access time
        self.access_times[key] = time.time()
    
    def remove(self, path: str, size: Optional[QSize] = None) -> None:
        """
        Remove a thumbnail from the cache.
        
        Args:
            path: Path to the original image
            size: Optional thumbnail size (if None, removes all sizes for this path)
        """
        if size is None:
            # Remove all sizes for this path
            keys_to_remove = []
            for key in self.cache:
                if self.cache[key]["path"] == path:
                    keys_to_remove.append(key)
            
            # Remove from cache and access times
            for key in keys_to_remove:
                if key in self.cache:
                    del self.cache[key]
                if key in self.access_times:
                    del self.access_times[key]
        else:
            # Remove specific size
            key = self._create_key(path, size)
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
    
    def clear(self) -> None:
        """Clear the entire cache."""
        self.cache.clear()
        self.access_times.clear()
    
    def _create_key(self, path: str, size: QSize) -> str:
        """
        Create a unique cache key for a path and size.
        
        Args:
            path: Path to the original image
            size: Thumbnail size
            
        Returns:
            str: Unique cache key
        """
        # Create a hash of the path to avoid issues with special characters
        path_hash = hashlib.md5(path.encode()).hexdigest()
        
        # Include the size in the key
        return f"{path_hash}_{size.width()}x{size.height()}"
    
    def _cleanup(self) -> None:
        """
        Clean up the cache by removing the least recently accessed items.
        """
        # If cache is empty, nothing to do
        if not self.cache:
            return
        
        # Remove 25% of the cache (least recently accessed items)
        num_to_remove = max(1, len(self.cache) // 4)
        
        # Sort keys by access time
        sorted_keys = sorted(self.access_times.keys(), key=lambda k: self.access_times[k])
        
        # Remove the oldest items
        for key in sorted_keys[:num_to_remove]:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
