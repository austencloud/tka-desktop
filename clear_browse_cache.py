#!/usr/bin/env python3
"""
Utility script to clear the browse tab cache.
This will force regeneration of all thumbnails with the new high-quality settings.
"""

import os
import shutil
import sys
from pathlib import Path

def get_cache_directory():
    """Get the cache directory path."""
    try:
        # Try to get the path using the same method as the app
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from utils.path_helpers import get_user_editable_resource_path
        cache_dir = os.path.join(get_user_editable_resource_path(""), "browse_thumbnails")
        return cache_dir
    except Exception:
        # Fallback to common locations
        import tempfile
        fallback_locations = [
            os.path.join(os.environ.get('APPDATA', ''), 'browse_thumbnails'),
            os.path.join(tempfile.gettempdir(), 'kinetic_constructor_browse_cache'),
            os.path.join(os.path.expanduser('~'), '.kinetic_constructor', 'browse_thumbnails')
        ]
        
        for location in fallback_locations:
            if os.path.exists(location):
                return location
        
        return fallback_locations[0]  # Return first as default

def clear_cache():
    """Clear the browse tab cache."""
    cache_dir = get_cache_directory()
    
    print(f"🔍 Looking for cache directory: {cache_dir}")
    
    if not os.path.exists(cache_dir):
        print("✅ No cache directory found - nothing to clear")
        return True
    
    try:
        # Count files before deletion
        cache_files = list(Path(cache_dir).glob("*.png"))
        metadata_file = Path(cache_dir) / "cache_metadata.json"
        
        total_files = len(cache_files)
        if metadata_file.exists():
            total_files += 1
        
        if total_files == 0:
            print("✅ Cache directory is already empty")
            return True
        
        print(f"🗑️  Found {len(cache_files)} cached images and metadata file")
        
        # Remove all .png files
        for cache_file in cache_files:
            cache_file.unlink()
            
        # Remove metadata file
        if metadata_file.exists():
            metadata_file.unlink()
            
        print(f"✅ Successfully cleared {total_files} cache files")
        print("🎯 Next app launch will regenerate thumbnails with high quality settings")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")
        return False

def main():
    """Main function."""
    print("🧹 Browse Tab Cache Cleaner")
    print("=" * 40)
    
    if clear_cache():
        print("\n🎉 Cache cleared successfully!")
        print("\nNext steps:")
        print("1. Launch the application")
        print("2. Navigate to browse tab")
        print("3. Thumbnails will regenerate with crisp, high-quality images")
        print("4. Subsequent loads will use the new high-quality cached versions")
        return 0
    else:
        print("\n⚠️  Cache clearing failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
