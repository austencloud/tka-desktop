#!/usr/bin/env python3
"""
Advanced cache performance debugging utility for browse tab.
This script provides detailed analysis of cache performance and image quality.
"""

import os
import sys
import time
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging():
    """Set up detailed logging for cache debugging."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('cache_debug.log')
        ]
    )

def test_cache_directory():
    """Test cache directory and contents."""
    print("🔍 CACHE DIRECTORY ANALYSIS")
    print("=" * 50)
    
    try:
        from utils.path_helpers import get_user_editable_resource_path
        cache_dir = os.path.join(get_user_editable_resource_path(""), "browse_thumbnails")
    except Exception:
        cache_dir = "browse_thumbnails"
    
    print(f"Cache directory: {cache_dir}")
    print(f"Directory exists: {os.path.exists(cache_dir)}")
    
    if os.path.exists(cache_dir):
        cache_files = list(Path(cache_dir).glob("*.png"))
        metadata_file = Path(cache_dir) / "cache_metadata.json"
        
        print(f"Cached images: {len(cache_files)}")
        print(f"Metadata file exists: {metadata_file.exists()}")
        
        if cache_files:
            total_size = sum(f.stat().st_size for f in cache_files)
            print(f"Total cache size: {total_size / (1024*1024):.2f} MB")
            
            # Show sample cache files
            print("\nSample cache files:")
            for i, cache_file in enumerate(cache_files[:5]):
                size_kb = cache_file.stat().st_size / 1024
                print(f"  {cache_file.name} ({size_kb:.1f} KB)")
        
        if metadata_file.exists():
            try:
                import json
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                print(f"Metadata entries: {len(metadata)}")
                
                # Show sample metadata
                if metadata:
                    sample_key = list(metadata.keys())[0]
                    sample_data = metadata[sample_key]
                    print(f"\nSample metadata entry:")
                    print(f"  Key: {sample_key}")
                    print(f"  Word: {sample_data.get('word', 'N/A')}")
                    print(f"  Variation: {sample_data.get('variation', 'N/A')}")
                    print(f"  Size: {sample_data.get('target_width', 'N/A')}x{sample_data.get('target_height', 'N/A')}")
                    
            except Exception as e:
                print(f"Error reading metadata: {e}")
    
    return cache_dir

def test_cache_performance():
    """Test cache performance with timing."""
    print("\n🚀 CACHE PERFORMANCE TEST")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import QSize
        from main_window.main_widget.browse_tab.cache import BrowseThumbnailCache
        
        app = QApplication(sys.argv)
        
        # Create cache instance
        cache = BrowseThumbnailCache(max_cache_size_mb=100)
        
        # Test image path (use a common test image)
        test_image_path = "test_image.png"
        if not os.path.exists(test_image_path):
            # Create a test image
            test_pixmap = QPixmap(800, 600)
            test_pixmap.fill()
            test_pixmap.save(test_image_path)
            print(f"Created test image: {test_image_path}")
        
        test_size = QSize(200, 150)
        test_word = "test_word"
        test_variation = 1
        
        # Test cache miss (first load)
        print("\n📊 Testing cache miss (first load)...")
        start_time = time.time()
        cached_result = cache.get_cached_thumbnail(test_image_path, test_size, test_word, test_variation)
        miss_time = time.time() - start_time
        
        print(f"Cache miss time: {miss_time*1000:.2f}ms")
        print(f"Cache miss result: {'Found' if cached_result else 'Not found'} (expected: Not found)")
        
        # Create and cache a test image
        print("\n💾 Caching test image...")
        test_pixmap = QPixmap(test_image_path)
        scaled_pixmap = test_pixmap.scaled(test_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        start_time = time.time()
        cache_success = cache.cache_thumbnail(test_image_path, scaled_pixmap, test_size, test_word, test_variation)
        cache_time = time.time() - start_time
        
        print(f"Cache save time: {cache_time*1000:.2f}ms")
        print(f"Cache save success: {cache_success}")
        
        # Test cache hit (second load)
        print("\n⚡ Testing cache hit (second load)...")
        start_time = time.time()
        cached_result = cache.get_cached_thumbnail(test_image_path, test_size, test_word, test_variation)
        hit_time = time.time() - start_time
        
        print(f"Cache hit time: {hit_time*1000:.2f}ms")
        print(f"Cache hit result: {'Found' if cached_result else 'Not found'} (expected: Found)")
        
        # Performance comparison
        if cached_result:
            speedup = miss_time / hit_time if hit_time > 0 else float('inf')
            print(f"\n🎯 Performance improvement: {speedup:.1f}x faster")
        
        # Get cache statistics
        stats = cache.get_cache_stats()
        print(f"\n📈 Cache Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Cleanup
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Cache performance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_quality():
    """Test image quality scaling methods."""
    print("\n🎨 IMAGE QUALITY TEST")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtCore import QSize, Qt
        
        app = QApplication(sys.argv)
        
        # Create test image
        test_pixmap = QPixmap(800, 600)
        test_pixmap.fill()
        
        target_size = QSize(200, 150)
        
        # Test FastTransformation
        start_time = time.time()
        fast_scaled = test_pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        fast_time = time.time() - start_time
        
        # Test SmoothTransformation
        start_time = time.time()
        smooth_scaled = test_pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        smooth_time = time.time() - start_time
        
        print(f"FastTransformation time: {fast_time*1000:.2f}ms")
        print(f"SmoothTransformation time: {smooth_time*1000:.2f}ms")
        print(f"Quality overhead: {(smooth_time/fast_time - 1)*100:.1f}% slower for better quality")
        
        # Test multi-step scaling
        start_time = time.time()
        intermediate_size = QSize(400, 300)  # 50% intermediate
        intermediate_scaled = test_pixmap.scaled(intermediate_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        multi_step_scaled = intermediate_scaled.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        multi_step_time = time.time() - start_time
        
        print(f"Multi-step scaling time: {multi_step_time*1000:.2f}ms")
        print(f"Multi-step vs single: {(multi_step_time/smooth_time - 1)*100:.1f}% time difference")
        
        return True
        
    except Exception as e:
        print(f"❌ Image quality test failed: {e}")
        return False

def analyze_cache_keys():
    """Analyze cache key generation and consistency."""
    print("\n🔑 CACHE KEY ANALYSIS")
    print("=" * 50)
    
    try:
        from main_window.main_widget.browse_tab.cache import BrowseThumbnailCache
        from PyQt6.QtCore import QSize
        
        cache = BrowseThumbnailCache()
        
        # Test cache key generation
        test_cases = [
            ("test_image.png", QSize(200, 150), "word1", 1),
            ("test_image.png", QSize(200, 150), "word1", 2),
            ("test_image.png", QSize(300, 225), "word1", 1),
            ("test_image.png", QSize(200, 150), "word2", 1),
        ]
        
        print("Cache key generation test:")
        for image_path, size, word, variation in test_cases:
            key = cache._get_cache_key(image_path, size, word, variation)
            print(f"  {word}_{variation} ({size.width()}x{size.height()}): {key[:16]}...")
        
        # Test key uniqueness
        keys = [cache._get_cache_key(path, size, word, var) for path, size, word, var in test_cases]
        unique_keys = set(keys)
        
        print(f"\nKey uniqueness: {len(unique_keys)}/{len(keys)} unique keys")
        if len(unique_keys) != len(keys):
            print("⚠️  Warning: Duplicate cache keys detected!")
        else:
            print("✅ All cache keys are unique")
        
        return True
        
    except Exception as e:
        print(f"❌ Cache key analysis failed: {e}")
        return False

def main():
    """Run comprehensive cache debugging."""
    print("🔧 BROWSE TAB CACHE PERFORMANCE DEBUGGER")
    print("=" * 60)
    
    setup_logging()
    
    tests = [
        ("Cache Directory", test_cache_directory),
        ("Cache Performance", test_cache_performance),
        ("Image Quality", test_image_quality),
        ("Cache Keys", analyze_cache_keys),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_name == "Cache Directory":
                cache_dir = test_func()
                results[test_name] = cache_dir
            else:
                results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*20} SUMMARY {'='*20}")
    for test_name, result in results.items():
        if test_name == "Cache Directory":
            print(f"{test_name}: {result}")
        else:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
    
    print(f"\n📝 Detailed logs saved to: cache_debug.log")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
