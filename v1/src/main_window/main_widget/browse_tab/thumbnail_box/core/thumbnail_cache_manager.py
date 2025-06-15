"""
Thumbnail Cache Manager - Handles disk caching with metadata validation.

Extracted from ThumbnailImageLabel to follow Single Responsibility Principle.
"""

import logging
import os
import hashlib
import json
import time  # ← add this at the top
from pathlib import Path
from typing import Optional, Dict, Any
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap


class ThumbnailCacheManager:
    """
    Manages thumbnail disk caching with metadata validation.
    
    Responsibilities:
    - Disk cache storage and retrieval
    - Cache metadata management
    - Cache key generation and validation
    - Cache cleanup and maintenance
    """
    
    # Cache configuration
    CACHE_DIR = Path("browse_thumbnails")
    CACHE_METADATA_FILE = "cache_metadata.json"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cache_metadata: Dict[str, Any] = {}
        
        # Initialize cache system
        self._ensure_cache_directory()
        self._load_cache_metadata()
    
    def get_cached_thumbnail(self, image_path: str, target_size: QSize) -> Optional[QPixmap]:
        """
        Get cached thumbnail if available and valid.
        
        Args:
            image_path: Path to the original image
            target_size: Target size for the thumbnail
            
        Returns:
            Cached QPixmap if found and valid, None otherwise
        """
        try:
            cache_key = self._generate_cache_key(image_path, target_size)
            cache_file_path = self.CACHE_DIR / f"{cache_key}.png"
            
            # Check if cache file exists and metadata is valid
            if cache_file_path.exists() and self._is_cache_valid(cache_key, image_path):
                cached_pixmap = QPixmap(str(cache_file_path))
                if not cached_pixmap.isNull():
                    self.logger.debug(f"Cache hit: {os.path.basename(image_path)}")
                    return cached_pixmap
            
            # Cache miss or invalid
            self.logger.debug(f"Cache miss: {os.path.basename(image_path)}")
            return None
            
        except Exception as e:
            self.logger.warning(f"Error accessing cache for {image_path}: {e}")
            return None
    
    def cache_thumbnail(self, image_path: str, pixmap: QPixmap, target_size: QSize) -> None:
        """
        Cache a processed thumbnail to disk.
        
        Args:
            image_path: Path to the original image
            pixmap: Processed QPixmap to cache
            target_size: Target size used for processing
        """
        try:
            if pixmap.isNull():
                return
            
            cache_key = self._generate_cache_key(image_path, target_size)
            cache_file_path = self.CACHE_DIR / f"{cache_key}.png"
            
            # Save pixmap to cache
            if pixmap.save(str(cache_file_path), "PNG"):
                # Update metadata
                self._update_cache_metadata(cache_key, image_path, target_size)
                self.logger.debug(f"Cached thumbnail: {os.path.basename(image_path)}")
            else:
                self.logger.warning(f"Failed to save thumbnail cache: {cache_file_path}")
                
        except Exception as e:
            self.logger.warning(f"Error caching thumbnail for {image_path}: {e}")
    
    def clear_cache(self) -> None:
        """Clear all cached thumbnails and metadata."""
        try:
            # Remove all cache files
            if self.CACHE_DIR.exists():
                for cache_file in self.CACHE_DIR.glob("*.png"):
                    cache_file.unlink()
            
            # Clear metadata
            self._cache_metadata.clear()
            self._save_cache_metadata()
            
            self.logger.info("Thumbnail cache cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
    
    def _ensure_cache_directory(self) -> None:
        """Ensure cache directory exists."""
        try:
            self.CACHE_DIR.mkdir(exist_ok=True)
        except Exception as e:
            self.logger.warning(f"Failed to create cache directory: {e}")
    
    def _load_cache_metadata(self) -> None:
        """Load cache metadata from disk."""
        metadata_path = self.CACHE_DIR / self.CACHE_METADATA_FILE
        try:
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    self._cache_metadata = json.load(f)
            else:
                self._cache_metadata = {}
        except Exception as e:
            self.logger.warning(f"Failed to load cache metadata: {e}")
            self._cache_metadata = {}
    
    def _save_cache_metadata(self) -> None:
        """Save cache metadata to disk."""
        metadata_path = self.CACHE_DIR / self.CACHE_METADATA_FILE
        try:
            with open(metadata_path, "w") as f:
                json.dump(self._cache_metadata, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Failed to save cache metadata: {e}")
    
    def _generate_cache_key(self, image_path: str, target_size: QSize) -> str:
        """
        Generate cache key based on image path, modification time, and size.
        
        Args:
            image_path: Path to the image file
            target_size: Target size for the thumbnail
            
        Returns:
            Unique cache key string
        """
        try:
            # Get file modification time
            mtime = os.path.getmtime(image_path)
            
            # Create cache key from path, mtime, and target size
            key_data = (
                image_path,
                str(mtime),
                f"{target_size.width()}x{target_size.height()}"
            )
            
            # Generate hash
            key_string = "|".join(key_data)
            return hashlib.md5(key_string.encode()).hexdigest()
            
        except Exception as e:
            self.logger.warning(f"Error generating cache key for {image_path}: {e}")
            # Fallback to simple hash of path and size
            fallback_data = f"{image_path}_{target_size.width()}x{target_size.height()}"
            return hashlib.md5(fallback_data.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str, image_path: str) -> bool:
        """
        Check if cached item is still valid.
        
        Args:
            cache_key: Cache key to check
            image_path: Original image path
            
        Returns:
            True if cache is valid, False otherwise
        """
        try:
            if cache_key not in self._cache_metadata:
                return False
            
            metadata = self._cache_metadata[cache_key]
            cached_mtime = metadata.get("mtime", 0)
            
            # Check if original file still exists and hasn't been modified
            if not os.path.exists(image_path):
                return False
            
            current_mtime = os.path.getmtime(image_path)
            return current_mtime <= cached_mtime
            
        except Exception as e:
            self.logger.debug(f"Error validating cache for {image_path}: {e}")
            return False
    
    def _update_cache_metadata(self, cache_key: str, image_path: str, target_size: QSize) -> None:
        """
        Update cache metadata for a cached item.
        
        Args:
            cache_key: Cache key
            image_path: Original image path
            target_size: Target size used
        """
        try:
            mtime = os.path.getmtime(image_path)
            
            self._cache_metadata[cache_key] = {
                "image_path": image_path,
                "mtime": mtime,
                "target_size": f"{target_size.width()}x{target_size.height()}",
                "cached_at": time.time()  # ← replace os.time.time()
            }
            
            # Save metadata periodically (not every time for performance)
            if len(self._cache_metadata) % 10 == 0:
                self._save_cache_metadata()
                
        except Exception as e:
            self.logger.warning(f"Error updating cache metadata: {e}")

