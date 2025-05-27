"""
Memory Cache Manager - Handles in-memory LRU caching with single responsibility.

Extracted from the monolithic ImageProcessor class to follow SRP.
"""

import logging
import collections
from typing import Optional, OrderedDict as OrderedDictType, TypeVar, Generic

T = TypeVar('T')


class MemoryCacheManager(Generic[T]):
    """
    Handles in-memory LRU caching operations.
    
    Responsibilities:
    - LRU cache management
    - Cache size enforcement
    - Cache statistics tracking
    - Memory-aware operations
    """
    
    def __init__(self, cache_size: int, cache_name: str = "cache"):
        self.cache_size = cache_size
        self.cache_name = cache_name
        self.cache: OrderedDictType[str, T] = collections.OrderedDict()
        self.logger = logging.getLogger(__name__)
        
        # Statistics
        self.hits = 0
        self.misses = 0
        
    def get(self, key: str) -> Optional[T]:
        """
        Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached item if found, None otherwise
        """
        if key in self.cache:
            # Mark as recently used
            self.cache.move_to_end(key)
            self.hits += 1
            self.logger.debug(f"{self.cache_name} cache hit: {key}")
            return self.cache[key]
        else:
            self.misses += 1
            self.logger.debug(f"{self.cache_name} cache miss: {key}")
            return None
            
    def put(self, key: str, value: T) -> None:
        """
        Put item in cache.
        
        Args:
            key: Cache key
            value: Item to cache
        """
        # Add to cache
        self.cache[key] = value
        self.cache.move_to_end(key)
        
        # Enforce cache size limit
        if len(self.cache) > self.cache_size:
            removed_item = self.cache.popitem(last=False)  # Remove least recently used
            self.logger.debug(f"{self.cache_name} cache full. Removed: {removed_item[0]}")
            
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of items cleared
        """
        count = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.logger.debug(f"{self.cache_name} cache cleared: {count} items removed")
        return count
        
    def remove_oldest(self, count: int) -> int:
        """
        Remove oldest cache entries.
        
        Args:
            count: Number of entries to remove
            
        Returns:
            Number of entries actually removed
        """
        removed = 0
        for _ in range(min(count, len(self.cache))):
            if self.cache:
                removed_item = self.cache.popitem(last=False)
                removed += 1
                self.logger.debug(f"{self.cache_name} removed oldest: {removed_item[0]}")
        return removed
        
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_name": self.cache_name,
            "size": len(self.cache),
            "max_size": self.cache_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 1),
            "total_requests": total_requests,
        }
        
    def __len__(self) -> int:
        """Get current cache size."""
        return len(self.cache)
        
    def __contains__(self, key: str) -> bool:
        """Check if key exists in cache."""
        return key in self.cache
