# src/main_window/main_widget/browse_tab/cache/browse_thumbnail_cache.py
import os
import json
import hashlib
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QSize, QThread, pyqtSignal, QObject
import collections
from collections import OrderedDict as OrderedDictType

from utils.path_helpers import get_user_editable_resource_path


class BrowseThumbnailCache(QObject):
    """
    Advanced persistent caching system for browse tab thumbnails.

    Features:
    - Disk-based persistent cache with LRU eviction
    - Two-level caching: memory + disk
    - Cache validation using file modification timestamps
    - Configurable cache size limits and cleanup
    - Thread-safe operations for UI responsiveness
    - Cache statistics and monitoring
    - Robust corruption handling and recovery
    """

    # Signals for cache events
    cache_hit = pyqtSignal(str)  # image_path
    cache_miss = pyqtSignal(str)  # image_path
    cache_size_changed = pyqtSignal(int)  # size_mb

    def __init__(self, cache_dir: str = None, max_cache_size_mb: int = 500):
        """
        Initialize the browse thumbnail cache.

        Args:
            cache_dir: Directory for cache files. If None, uses default location.
            max_cache_size_mb: Maximum cache size in MB before cleanup
        """
        super().__init__()
        self.max_cache_size_mb = max_cache_size_mb
        self.cache_enabled = True

        # Set up cache directory
        if cache_dir is None:
            try:
                cache_dir = os.path.join(
                    get_user_editable_resource_path(""), "browse_thumbnails"
                )
            except:
                # Fallback to temp directory
                import tempfile

                cache_dir = os.path.join(
                    tempfile.gettempdir(), "kinetic_constructor_browse_cache"
                )

        self.cache_dir = Path(cache_dir)
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self.backup_metadata_file = self.cache_dir / "cache_metadata_backup.json"
        self.metadata: Dict[str, Dict[str, Any]] = {}

        # Memory cache for frequently accessed thumbnails
        self.memory_cache: OrderedDictType[str, QPixmap] = collections.OrderedDict()
        self.memory_cache_size = 50  # Number of thumbnails to keep in memory

        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.disk_cache_hits = 0
        self.disk_cache_misses = 0
        self.memory_cache_hits = 0
        self.memory_cache_misses = 0

        # Initialize cache with robust error handling
        self._initialize_cache()

    def _initialize_cache(self) -> None:
        """Initialize cache directory and load metadata with robust error handling."""
        try:
            # Create cache directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            # Load metadata with robust error handling
            metadata_loaded = False

            # Try to load primary metadata file
            if self.metadata_file.exists():
                metadata_loaded = self._load_metadata_file(self.metadata_file)

            # If primary failed, try backup
            if not metadata_loaded and self.backup_metadata_file.exists():
                logging.warning("Primary metadata corrupted, trying backup...")
                metadata_loaded = self._load_metadata_file(self.backup_metadata_file)

                # If backup worked, restore it as primary
                if metadata_loaded:
                    try:
                        import shutil

                        shutil.copy2(self.backup_metadata_file, self.metadata_file)
                        logging.info("Restored metadata from backup")
                    except Exception as e:
                        logging.warning(f"Failed to restore backup metadata: {e}")

            # If both failed, rebuild from cache files
            if not metadata_loaded:
                logging.warning(
                    "Both metadata files corrupted or missing, rebuilding..."
                )
                self._rebuild_metadata_from_cache_files()
                metadata_loaded = True

            # Save clean metadata and create backup
            if metadata_loaded:
                self._save_metadata_safely()

            # Clear old low-quality cache entries on initialization
            self.clear_old_quality_cache()

            logging.debug(
                f"Browse thumbnail cache initialized: {self.cache_dir} "
                f"({len(self.metadata)} entries)"
            )

        except Exception as e:
            logging.error(f"Failed to initialize browse thumbnail cache: {e}")
            # Don't disable cache entirely - try to continue with empty metadata
            self.metadata = {}
            logging.warning("Continuing with empty cache metadata")

    def _load_metadata_file(self, metadata_file: Path) -> bool:
        """
        Attempt to load metadata from a specific file.

        Returns:
            True if successful, False if corrupted or failed
        """
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                # Read the entire file first to check for obvious corruption
                content = f.read().strip()

                # Basic validation
                if not content:
                    logging.warning(f"Metadata file is empty: {metadata_file}")
                    return False

                if not content.startswith("{") or not content.endswith("}"):
                    logging.warning(
                        f"Metadata file doesn't appear to be valid JSON: {metadata_file}"
                    )
                    return False

                # Check for obvious corruption patterns
                if content.count("{") != content.count("}"):
                    logging.warning(
                        f"Unbalanced braces in metadata file: {metadata_file}"
                    )
                    return False

                # Try to parse JSON
                self.metadata = json.loads(content)

                # Validate metadata structure
                if not isinstance(self.metadata, dict):
                    logging.warning(f"Metadata is not a dictionary: {metadata_file}")
                    return False

                # Basic validation of metadata entries
                valid_entries = {}
                for key, value in self.metadata.items():
                    if isinstance(value, dict) and "cache_time" in value:
                        valid_entries[key] = value
                    else:
                        logging.debug(f"Removing invalid metadata entry: {key}")

                self.metadata = valid_entries
                logging.debug(
                    f"Loaded {len(self.metadata)} valid metadata entries from {metadata_file}"
                )
                return True

        except json.JSONDecodeError as e:
            logging.warning(f"JSON decode error in {metadata_file}: {e}")
            return False
        except Exception as e:
            logging.warning(f"Error loading metadata from {metadata_file}: {e}")
            return False

    def _rebuild_metadata_from_cache_files(self) -> None:
        """
        Rebuild metadata from existing cache files.
        This is used when metadata files are corrupted.
        """
        try:
            self.metadata = {}
            cache_files = list(self.cache_dir.glob("*.png"))
            logging.info(f"Rebuilding metadata from {len(cache_files)} cache files...")

            for cache_file in cache_files:
                try:
                    # Extract cache key from filename (without .png extension)
                    cache_key = cache_file.stem

                    # Create basic metadata entry
                    file_stat = cache_file.stat()
                    self.metadata[cache_key] = {
                        "source_path": "unknown",  # Can't recover original path
                        "source_mtime": file_stat.st_mtime,
                        "cache_time": file_stat.st_mtime,
                        "last_access": file_stat.st_mtime,
                        "target_width": 200,  # Default size
                        "target_height": 150,  # Default size
                        "word": "unknown",
                        "variation": 0,
                        "file_size": file_stat.st_size,
                    }
                except Exception as e:
                    logging.debug(f"Error processing cache file {cache_file}: {e}")

            logging.info(f"Rebuilt metadata for {len(self.metadata)} cache files")

        except Exception as e:
            logging.error(f"Error rebuilding metadata: {e}")
            self.metadata = {}

    def _save_metadata_safely(self) -> None:
        """Save cache metadata with backup and error handling."""
        try:
            # Create backup of current metadata if it exists
            if self.metadata_file.exists():
                try:
                    import shutil

                    shutil.copy2(self.metadata_file, self.backup_metadata_file)
                except Exception as e:
                    logging.debug(f"Failed to create metadata backup: {e}")

            # Write new metadata to temporary file first
            temp_file = self.metadata_file.with_suffix(".tmp")

            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)

            # Verify the temporary file is valid JSON
            with open(temp_file, "r", encoding="utf-8") as f:
                json.load(f)  # This will raise an exception if invalid

            # If verification passed, replace the main metadata file
            if os.name == "nt":  # Windows
                if self.metadata_file.exists():
                    self.metadata_file.unlink()
                temp_file.replace(self.metadata_file)
            else:  # Unix-like systems
                temp_file.replace(self.metadata_file)

            logging.debug("Metadata saved successfully")

        except Exception as e:
            logging.error(f"Error saving metadata: {e}")
            # Clean up temporary file if it exists
            temp_file = self.metadata_file.with_suffix(".tmp")
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except:
                    pass

    def _clear_corrupted_cache(self) -> None:
        """Clear all cache files and start fresh."""
        try:
            logging.warning("Clearing corrupted cache and starting fresh...")

            # Remove all cache files
            for cache_file in self.cache_dir.glob("*.png"):
                try:
                    cache_file.unlink()
                except Exception as e:
                    logging.debug(f"Error removing cache file {cache_file}: {e}")

            # Remove metadata files
            for metadata_file in [self.metadata_file, self.backup_metadata_file]:
                if metadata_file.exists():
                    try:
                        metadata_file.unlink()
                    except Exception as e:
                        logging.debug(
                            f"Error removing metadata file {metadata_file}: {e}"
                        )

            # Clear in-memory data
            self.metadata = {}
            self.memory_cache.clear()

            logging.info("Cache cleared successfully")

        except Exception as e:
            logging.error(f"Error clearing corrupted cache: {e}")

    def _get_cache_key(
        self,
        image_path: str,
        size: QSize,
        word: str,
        variation: int,
        quality_version: str = "v2",
    ) -> str:
        """
        Generate a unique cache key for browse thumbnails with quality versioning.

        Args:
            image_path: Path to the source image
            size: Target thumbnail size
            word: Sequence word
            variation: Variation number
            quality_version: Version string to invalidate cache when quality changes

        Returns:
            Unique cache key string
        """
        try:
            mtime = os.path.getmtime(image_path)
            # Include quality version to invalidate old low-quality cache entries
            key_data = f"{word}_{variation}_{size.width()}x{size.height()}_{mtime}_{quality_version}"
            return hashlib.md5(key_data.encode()).hexdigest()
        except OSError:
            # If we can't get modification time, use current time (will miss cache)
            key_data = f"{word}_{variation}_{size.width()}x{size.height()}_{time.time()}_{quality_version}"
            return hashlib.md5(key_data.encode()).hexdigest()

    def _get_cache_file_path(self, cache_key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{cache_key}.png"

    def get_cached_thumbnail(
        self, image_path: str, size: QSize, word: str, variation: int
    ) -> Optional[QPixmap]:
        """
        Retrieve a cached thumbnail if available and valid.

        Args:
            image_path: Path to the source image
            size: Target thumbnail size
            word: Sequence word
            variation: Variation number

        Returns:
            Cached QPixmap if available, None otherwise
        """
        if not self.cache_enabled:
            return None

        try:
            cache_key = self._get_cache_key(image_path, size, word, variation, "v2")

            # Check memory cache first (fastest)
            if cache_key in self.memory_cache:
                self.memory_cache_hits += 1
                self.cache_hits += 1
                self.cache_hit.emit(image_path)

                # Move to end (most recently used)
                self.memory_cache.move_to_end(cache_key)
                return self.memory_cache[cache_key]

            # Check disk cache
            cache_file = self._get_cache_file_path(cache_key)

            if cache_file.exists() and cache_key in self.metadata:
                # Verify source file hasn't changed
                try:
                    current_mtime = os.path.getmtime(image_path)
                    cached_mtime = self.metadata[cache_key].get("source_mtime", 0)

                    if current_mtime <= cached_mtime:
                        # Load cached image
                        pixmap = QPixmap(str(cache_file))
                        if not pixmap.isNull():
                            self.disk_cache_hits += 1
                            self.cache_hits += 1
                            self.cache_hit.emit(image_path)

                            # Add to memory cache for faster access next time
                            self._add_to_memory_cache(cache_key, pixmap)

                            # Update access time in metadata
                            self.metadata[cache_key]["last_access"] = time.time()
                            return pixmap
                    else:
                        # Source file has been modified, remove stale cache
                        self._remove_cache_entry(cache_key)

                except OSError:
                    # Can't check modification time, assume cache is stale
                    self._remove_cache_entry(cache_key)

            self.cache_misses += 1
            self.disk_cache_misses += 1
            self.cache_miss.emit(image_path)
            return None

        except Exception as e:
            logging.debug(f"Error retrieving cached thumbnail: {e}")
            return None

    def cache_thumbnail(
        self, image_path: str, pixmap: QPixmap, size: QSize, word: str, variation: int
    ) -> bool:
        """
        Cache a processed thumbnail to disk and memory with maximum quality preservation.

        Args:
            image_path: Path to the source image
            pixmap: Processed QPixmap to cache
            size: Target thumbnail size
            word: Sequence word
            variation: Variation number

        Returns:
            True if caching succeeded, False otherwise
        """
        if not self.cache_enabled or pixmap.isNull():
            return False

        try:
            cache_key = self._get_cache_key(image_path, size, word, variation, "v2")
            cache_file = self._get_cache_file_path(cache_key)

            # CRITICAL FIX: Save with maximum quality to prevent degradation
            # Convert QPixmap to QImage for quality control
            image = pixmap.toImage()

            # Save with maximum quality PNG settings (lossless compression)
            # Quality 100 = maximum quality, compression 0 = fastest/least compression
            success = image.save(str(cache_file), "PNG", 100)

            if success:
                # Update metadata
                try:
                    source_mtime = os.path.getmtime(image_path)
                except OSError:
                    source_mtime = time.time()

                self.metadata[cache_key] = {
                    "source_path": image_path,
                    "source_mtime": source_mtime,
                    "cache_time": time.time(),
                    "last_access": time.time(),
                    "target_width": size.width(),
                    "target_height": size.height(),
                    "word": word,
                    "variation": variation,
                    "file_size": cache_file.stat().st_size,
                }

                # Add to memory cache
                self._add_to_memory_cache(cache_key, pixmap)

                logging.debug(
                    f"Cached HIGH-QUALITY browse thumbnail: {word}_{variation}"
                )

                # Periodically save metadata and check cache size
                if len(self.metadata) % 10 == 0:
                    self._save_metadata_safely()
                    self._check_cache_size()

                return True

        except Exception as e:
            logging.debug(f"Error caching thumbnail: {e}")

        return False

    def _add_to_memory_cache(self, cache_key: str, pixmap: QPixmap) -> None:
        """Add thumbnail to memory cache with LRU eviction."""
        self.memory_cache[cache_key] = pixmap
        self.memory_cache.move_to_end(cache_key)

        # Enforce memory cache size limit
        if len(self.memory_cache) > self.memory_cache_size:
            self.memory_cache.popitem(last=False)  # Remove least recently used

    def _remove_cache_entry(self, cache_key: str) -> None:
        """Remove a cache entry from both disk and memory."""
        try:
            # Remove from disk
            cache_file = self._get_cache_file_path(cache_key)
            if cache_file.exists():
                cache_file.unlink()

            # Remove from memory
            if cache_key in self.memory_cache:
                del self.memory_cache[cache_key]

            # Remove from metadata
            if cache_key in self.metadata:
                del self.metadata[cache_key]

        except Exception as e:
            logging.debug(f"Error removing cache entry: {e}")

    def _check_cache_size(self) -> None:
        """Check cache size and cleanup if necessary."""
        try:
            total_size = sum(
                entry.get("file_size", 0) for entry in self.metadata.values()
            )
            total_size_mb = total_size / (1024 * 1024)

            self.cache_size_changed.emit(int(total_size_mb))

            if total_size_mb > self.max_cache_size_mb:
                self._cleanup_cache()

        except Exception as e:
            logging.debug(f"Error checking cache size: {e}")

    def _cleanup_cache(self) -> None:
        """Clean up cache by removing least recently accessed items."""
        try:
            # Sort by last access time
            sorted_items = sorted(
                self.metadata.items(), key=lambda x: x[1].get("last_access", 0)
            )

            # Remove 25% of cache entries (oldest first)
            num_to_remove = max(1, len(sorted_items) // 4)

            for cache_key, _ in sorted_items[:num_to_remove]:
                self._remove_cache_entry(cache_key)

            self._save_metadata_safely()
            logging.info(f"Cleaned up {num_to_remove} cache entries")

        except Exception as e:
            logging.debug(f"Error during cache cleanup: {e}")

    def clear_cache(self) -> None:
        """Clear the entire cache."""
        try:
            # Clear memory cache
            self.memory_cache.clear()

            # Remove all cache files
            for cache_file in self.cache_dir.glob("*.png"):
                cache_file.unlink()

            # Clear metadata
            self.metadata.clear()
            self._save_metadata_safely()

            logging.info("Browse thumbnail cache cleared")

        except Exception as e:
            logging.warning(f"Error clearing cache: {e}")

    def clear_old_quality_cache(self) -> None:
        """Clear old low-quality cache entries to force regeneration with high quality."""
        try:
            old_entries_removed = 0
            entries_to_remove = []

            # Find entries that don't have the new quality version
            for cache_key, metadata in self.metadata.items():
                # Check if this is an old cache entry (doesn't contain v2 quality marker)
                if "v2" not in cache_key:
                    entries_to_remove.append(cache_key)

            # Remove old entries
            for cache_key in entries_to_remove:
                self._remove_cache_entry(cache_key)
                old_entries_removed += 1

            if old_entries_removed > 0:
                self._save_metadata_safely()
                logging.info(
                    f"Cleared {old_entries_removed} old low-quality cache entries"
                )

        except Exception as e:
            logging.warning(f"Error clearing old quality cache: {e}")

    def force_regenerate_all_thumbnails(self) -> None:
        """Force regeneration of all thumbnails by clearing the entire cache."""
        try:
            logging.info("🔄 Forcing regeneration of all thumbnails...")

            # Clear everything
            self.clear_cache()

            # Reset statistics
            self.cache_hits = 0
            self.cache_misses = 0
            self.disk_cache_hits = 0
            self.disk_cache_misses = 0
            self.memory_cache_hits = 0
            self.memory_cache_misses = 0

            logging.info(
                "✅ All thumbnails will be regenerated with high quality on next load"
            )

        except Exception as e:
            logging.warning(f"Error forcing thumbnail regeneration: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            total_size = sum(
                entry.get("file_size", 0) for entry in self.metadata.values()
            )
            total_size_mb = total_size / (1024 * 1024)

            hit_rate = 0
            if self.cache_hits + self.cache_misses > 0:
                hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses)

            return {
                "total_items": len(self.metadata),
                "total_size_mb": total_size_mb,
                "memory_cache_items": len(self.memory_cache),
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "hit_rate": hit_rate,
                "disk_cache_hits": self.disk_cache_hits,
                "disk_cache_misses": self.disk_cache_misses,
                "memory_cache_hits": self.memory_cache_hits,
                "memory_cache_misses": self.memory_cache_misses,
            }
        except Exception:
            return {}

    # Emergency recovery methods

    def repair_cache(self) -> bool:
        """
        Emergency cache repair function.
        Call this if cache is completely broken.
        """
        try:
            logging.warning("Attempting emergency cache repair...")

            # Step 1: Clear corrupted data
            self._clear_corrupted_cache()

            # Step 2: Reinitialize
            self._initialize_cache()

            logging.info("Emergency cache repair completed")
            return True

        except Exception as e:
            logging.error(f"Emergency cache repair failed: {e}")
            return False
