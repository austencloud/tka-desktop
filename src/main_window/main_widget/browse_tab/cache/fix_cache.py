#!/usr/bin/env python3
"""
Immediate Cache Corruption Fix Script

This script will fix the corrupted cache metadata that's preventing your app from starting.
Run this script first to get your app working again, then apply the full ultra quality fix.
"""

import os
import json
import shutil
from pathlib import Path


def find_cache_directory():
    """Find the cache directory."""
    possible_paths = [
        # Common cache locations
        Path.home() / "AppData" / "Local" / "kinetic_constructor_browse_cache",
        Path.home() / ".cache" / "kinetic_constructor_browse_cache",
        Path("/tmp") / "kinetic_constructor_browse_cache",
        # Project relative paths
        Path("the-kinetic-constructor-desktop") / "browse_thumbnails",
        Path("browse_thumbnails"),
        # User editable resource paths
        Path.home() / "Documents" / "kinetic_constructor" / "browse_thumbnails",
    ]

    for path in possible_paths:
        if path.exists() and (path / "cache_metadata.json").exists():
            return path

    # Search more broadly
    for root in [Path.home(), Path("/tmp"), Path.cwd()]:
        for cache_dir in root.rglob("*browse*cache*"):
            if cache_dir.is_dir() and (cache_dir / "cache_metadata.json").exists():
                return cache_dir

    return None


def backup_corrupted_metadata(cache_dir):
    """Backup the corrupted metadata file."""
    metadata_file = cache_dir / "cache_metadata.json"
    backup_file = cache_dir / f"cache_metadata_corrupted_{int(time.time())}.json"

    try:
        shutil.copy2(metadata_file, backup_file)
        print(f"✅ Backed up corrupted metadata to: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"⚠️  Failed to backup corrupted metadata: {e}")
        return None


def fix_cache_corruption(cache_dir):
    """Fix the corrupted cache by rebuilding metadata."""
    print(f"🔧 Fixing cache corruption in: {cache_dir}")

    metadata_file = cache_dir / "cache_metadata.json"
    backup_metadata_file = cache_dir / "cache_metadata_backup.json"

    # Step 1: Backup corrupted file
    if metadata_file.exists():
        backup_corrupted_metadata(cache_dir)

    # Step 2: Remove corrupted metadata files
    for file in [metadata_file, backup_metadata_file]:
        if file.exists():
            try:
                file.unlink()
                print(f"🗑️  Removed corrupted file: {file}")
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")

    # Step 3: Rebuild metadata from existing cache files
    cache_files = list(cache_dir.glob("*.png"))
    print(f"📁 Found {len(cache_files)} cache files to rebuild metadata for")

    new_metadata = {}
    import time

    for cache_file in cache_files:
        try:
            cache_key = cache_file.stem
            file_stat = cache_file.stat()

            new_metadata[cache_key] = {
                "source_path": "unknown",
                "source_mtime": file_stat.st_mtime,
                "cache_time": file_stat.st_mtime,
                "last_access": file_stat.st_mtime,
                "target_width": 200,
                "target_height": 150,
                "word": "unknown",
                "variation": 0,
                "file_size": file_stat.st_size,
            }
        except Exception as e:
            print(f"⚠️  Error processing {cache_file}: {e}")

    # Step 4: Save new clean metadata
    try:
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(new_metadata, f, indent=2, ensure_ascii=False)

        print(f"✅ Rebuilt metadata with {len(new_metadata)} entries")
        print(f"💾 Saved to: {metadata_file}")

        # Create duplicate as backup
        shutil.copy2(metadata_file, backup_metadata_file)
        print(f"💾 Created backup: {backup_metadata_file}")

        return True

    except Exception as e:
        print(f"❌ Failed to save new metadata: {e}")
        return False


def clear_cache_completely(cache_dir):
    """Completely clear the cache if rebuild fails."""
    print(f"🗑️  Completely clearing cache: {cache_dir}")

    try:
        # Remove all cache files
        for cache_file in cache_dir.glob("*.png"):
            cache_file.unlink()

        # Remove metadata files
        for metadata_file in cache_dir.glob("*.json"):
            metadata_file.unlink()

        print("✅ Cache cleared completely")
        print("ℹ️  Cache will be rebuilt when you run the app")
        return True

    except Exception as e:
        print(f"❌ Failed to clear cache: {e}")
        return False


def main():
    """Main function to fix cache corruption."""
    print("🔥 KINETIC CONSTRUCTOR CACHE CORRUPTION FIX")
    print("=" * 50)

    # Find cache directory
    print("🔍 Searching for cache directory...")
    cache_dir = find_cache_directory()

    if not cache_dir:
        print("❓ Cache directory not found. This might be the first run.")
        print("✅ Your app should work normally on next startup.")
        return

    print(f"📁 Found cache directory: {cache_dir}")

    # Check if metadata is actually corrupted
    metadata_file = cache_dir / "cache_metadata.json"
    if not metadata_file.exists():
        print("ℹ️  No metadata file found - this is normal for first run")
        return

    # Try to parse the metadata to confirm corruption
    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            json.load(f)
        print("✅ Metadata file is actually valid - no corruption detected")
        return
    except json.JSONDecodeError as e:
        print(f"💥 Confirmed JSON corruption: {e}")
    except Exception as e:
        print(f"💥 Metadata file error: {e}")

    # Attempt to fix the corruption
    print("\n🔧 ATTEMPTING AUTOMATIC REPAIR...")
    success = fix_cache_corruption(cache_dir)

    if not success:
        print("\n🗑️  REPAIR FAILED - CLEARING CACHE COMPLETELY...")
        success = clear_cache_completely(cache_dir)

    if success:
        print("\n✅ CACHE CORRUPTION FIXED!")
        print("🚀 Your app should now start normally.")
        print("\n📋 NEXT STEPS:")
        print("1. Start your Kinetic Constructor app")
        print("2. Navigate to Browse tab to verify it works")
        print("3. Apply the Ultra Quality thumbnail fix for better image quality")
    else:
        print("\n❌ AUTOMATIC FIX FAILED")
        print("🔧 MANUAL FIX REQUIRED:")
        print(f"1. Delete the entire cache directory: {cache_dir}")
        print("2. Restart your app - it will create a new clean cache")


if __name__ == "__main__":
    import time

    main()
