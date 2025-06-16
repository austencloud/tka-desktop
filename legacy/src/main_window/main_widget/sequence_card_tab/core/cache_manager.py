import os
import json
import time
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
import threading


class SequenceCardCacheManager:
    """
    Manages persistent caching of sequence card data to improve loading performance.

    Features:
    - Saves sequence data to disk cache
    - Loads sequence data from disk cache
    - Validates cache freshness
    - Cleans up old cache files
    - Preloads common sequence lengths
    """

    def __init__(self):
        """Initialize the cache manager with cache directory setup."""
        # Cache directory in AppData
        self.cache_dir = self._get_cache_dir()
        self.cache_version = 1  # Increment when cache format changes
        self.cache_expiry = 60 * 60 * 24 * 7  # 7 days in seconds

        # Common sequence lengths to preload
        self.common_lengths = [4, 8, 16]

        # Ensure cache directory exists
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_dir(self) -> Path:
        """Get the cache directory path in AppData."""
        if os.name == "nt":  # Windows
            app_data = os.getenv("APPDATA")
            if not app_data:
                app_data = os.path.expanduser("~")
            base_dir = Path(app_data)
        else:  # macOS/Linux
            base_dir = Path(os.path.expanduser("~/.config"))

        cache_dir = base_dir / "KineticConstructor" / "sequence_card_cache"
        return cache_dir

    def get_cache_file_path(self, length: int) -> Path:
        """Get the cache file path for a specific sequence length."""
        return (
            self.cache_dir
            / f"sequence_cache_v{self.cache_version}_length_{length}.json"
        )

    def save_to_cache(self, length: int, sequences: List[Dict[str, Any]]) -> bool:
        """
        Save sequence data to cache file.

        Args:
            length: Sequence length (0 for all sequences)
            sequences: List of sequence dictionaries

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cache_file = self.get_cache_file_path(length)

            # Prepare cache data with metadata
            cache_data = {
                "version": self.cache_version,
                "timestamp": time.time(),
                "length": length,
                "count": len(sequences),
                "sequences": sequences,
            }

            # Save to temporary file first to prevent corruption
            temp_file = cache_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f)

            # Rename to final filename
            if os.path.exists(cache_file):
                os.remove(cache_file)
            os.rename(temp_file, cache_file)

            print(f"Saved {len(sequences)} sequences to cache: {cache_file}")
            return True

        except Exception as e:
            print(f"Error saving to cache: {e}")
            return False

    def load_from_cache(self, length: int) -> Optional[List[Dict[str, Any]]]:
        """
        Load sequence data from cache file if it exists and is valid.

        Args:
            length: Sequence length (0 for all sequences)

        Returns:
            List of sequence dictionaries or None if cache is invalid/missing
        """
        try:
            cache_file = self.get_cache_file_path(length)

            # Check if cache file exists
            if not os.path.exists(cache_file):
                print(f"Cache file not found: {cache_file}")
                return None

            # Check if cache file is too old
            file_age = time.time() - os.path.getmtime(cache_file)
            if file_age > self.cache_expiry:
                print(f"Cache file too old ({file_age:.1f} seconds): {cache_file}")
                return None

            # Load cache data
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Validate cache data
            if cache_data.get("version") != self.cache_version:
                print(
                    f"Cache version mismatch: {cache_data.get('version')} != {self.cache_version}"
                )
                return None

            if cache_data.get("length") != length:
                print(f"Cache length mismatch: {cache_data.get('length')} != {length}")
                return None

            sequences = cache_data.get("sequences", [])
            print(f"Loaded {len(sequences)} sequences from cache: {cache_file}")
            return sequences

        except Exception as e:
            print(f"Error loading from cache: {e}")
            return None

    def preload_common_lengths(self, sequences: List[Dict[str, Any]]) -> None:
        """
        Preload cache for common sequence lengths in a background thread.

        Args:
            sequences: List of all sequences to filter and cache
        """
        # Start a background thread to avoid blocking the UI
        thread = threading.Thread(
            target=self._preload_thread, args=(sequences,), daemon=True
        )
        thread.start()

    def _preload_thread(self, sequences: List[Dict[str, Any]]) -> None:
        """
        Background thread for preloading common sequence lengths.

        Args:
            sequences: List of all sequences to filter and cache
        """
        try:
            print(f"Starting preload of common sequence lengths: {self.common_lengths}")

            for length in self.common_lengths:
                # Skip if cache already exists and is fresh
                cache_file = self.get_cache_file_path(length)
                if os.path.exists(cache_file):
                    file_age = time.time() - os.path.getmtime(cache_file)
                    if file_age < self.cache_expiry:
                        print(
                            f"Skipping preload for length {length}, cache is fresh ({file_age:.1f} seconds old)"
                        )
                        continue

                # Filter sequences by length
                filtered_sequences = []
                for sequence in sequences:
                    metadata = sequence.get("metadata", {})
                    sequence_length = metadata.get("sequence_length", 0)

                    if sequence_length == length:
                        filtered_sequences.append(sequence)

                # Save to cache
                if filtered_sequences:
                    self.save_to_cache(length, filtered_sequences)
                    print(
                        f"Preloaded {len(filtered_sequences)} sequences for length {length}"
                    )
                else:
                    print(f"No sequences found for length {length}, skipping preload")

            print("Preloading complete")

        except Exception as e:
            print(f"Error in preload thread: {e}")

    def clean_cache(self) -> None:
        """
        Clean up old cache files in a background thread.
        """
        # Start a background thread to avoid blocking the UI
        thread = threading.Thread(target=self._clean_cache_thread, daemon=True)
        thread.start()

    def _clean_cache_thread(self) -> None:
        """
        Background thread for cleaning up old cache files.
        """
        try:
            # Get all files in cache directory
            cache_files = list(self.cache_dir.glob("sequence_cache_*.json"))

            # Check each file
            deleted_count = 0
            for file_path in cache_files:
                try:
                    # Delete old version cache files
                    if f"_v{self.cache_version}_" not in file_path.name:
                        os.remove(file_path)
                        deleted_count += 1
                        continue

                    # Delete expired cache files
                    file_age = time.time() - os.path.getmtime(file_path)
                    if file_age > self.cache_expiry:
                        os.remove(file_path)
                        deleted_count += 1

                except Exception:
                    # Silently continue on cache file errors
                    pass

        except Exception:
            # Silently handle cache cleanup errors
            pass

    def clear_all_cache(self) -> None:
        """
        Clear all cache files.
        """
        try:
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
                os.makedirs(self.cache_dir, exist_ok=True)

        except Exception:
            # Silently handle cache clearing errors
            pass

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the cache.

        Returns:
            Dictionary with cache statistics
        """
        stats = {
            "cache_dir": str(self.cache_dir),
            "cache_version": self.cache_version,
            "cache_files": 0,
            "total_size_bytes": 0,
            "oldest_file_age": 0,
            "newest_file_age": float("inf"),
            "lengths_cached": [],
        }

        try:
            if os.path.exists(self.cache_dir):
                # Get all cache files
                cache_files = list(self.cache_dir.glob("sequence_cache_*.json"))
                stats["cache_files"] = len(cache_files)

                now = time.time()

                # Process each file
                for file_path in cache_files:
                    # Add file size
                    file_size = os.path.getsize(file_path)
                    stats["total_size_bytes"] += file_size

                    # Check file age
                    file_age = now - os.path.getmtime(file_path)
                    stats["oldest_file_age"] = max(stats["oldest_file_age"], file_age)
                    stats["newest_file_age"] = min(stats["newest_file_age"], file_age)

                    # Extract length from filename
                    try:
                        length_str = file_path.name.split("_length_")[1].split(".")[0]
                        length = int(length_str)
                        stats["lengths_cached"].append(length)
                    except:
                        pass

                # Convert to human-readable format
                stats["total_size_mb"] = stats["total_size_bytes"] / (1024 * 1024)
                stats["oldest_file_age_hours"] = stats["oldest_file_age"] / 3600
                stats["newest_file_age_hours"] = (
                    stats["newest_file_age"] / 3600
                    if stats["newest_file_age"] != float("inf")
                    else 0
                )

        except Exception as e:
            print(f"Error getting cache stats: {e}")

        return stats
