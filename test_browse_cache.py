#!/usr/bin/env python3
"""
Test script to verify browse tab cache system functionality.
Run this script to test the cache improvements.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cache_settings():
    """Test cache settings functionality."""
    print("🧪 Testing cache settings...")
    
    try:
        from settings_manager.browse_tab_settings import BrowseTabSettings
        from PyQt6.QtCore import QSettings
        
        # Create a test settings instance
        settings = QSettings("test_cache", "test")
        browse_settings = BrowseTabSettings(type('MockSettingsManager', (), {'settings': settings})())
        
        # Test default values
        assert browse_settings.get_cache_mode() == "Balanced"
        assert browse_settings.get_cache_max_size_mb() == 500
        assert browse_settings.get_enable_disk_cache() == True
        assert browse_settings.get_cache_quality_mode() == "two_stage"
        
        # Test setting values
        browse_settings.set_cache_mode("High Performance")
        assert browse_settings.get_cache_max_size_mb() == 1000  # Should auto-update
        
        browse_settings.set_cache_quality_mode("smooth_only")
        assert browse_settings.get_cache_quality_mode() == "smooth_only"
        
        print("✅ Cache settings test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Cache settings test failed: {e}")
        return False

def test_cache_class():
    """Test BrowseThumbnailCache class."""
    print("🧪 Testing BrowseThumbnailCache class...")
    
    try:
        from main_window.main_widget.browse_tab.cache import BrowseThumbnailCache
        from PyQt6.QtCore import QSize
        from PyQt6.QtGui import QPixmap
        import tempfile
        
        # Create cache with temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = BrowseThumbnailCache(temp_dir, 100)  # 100MB limit
            
            # Test cache initialization
            assert cache.cache_enabled == True
            assert cache.max_cache_size_mb == 100
            
            # Test cache stats
            stats = cache.get_cache_stats()
            assert isinstance(stats, dict)
            assert 'total_items' in stats
            assert 'total_size_mb' in stats
            
            print("✅ BrowseThumbnailCache test passed!")
            return True
            
    except Exception as e:
        print(f"❌ BrowseThumbnailCache test failed: {e}")
        return False

def test_quality_modes():
    """Test quality mode functionality."""
    print("🧪 Testing quality modes...")
    
    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap
        
        # Create a test pixmap
        pixmap = QPixmap(100, 100)
        pixmap.fill()
        
        # Test different transformation modes
        fast_scaled = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)
        smooth_scaled = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        assert not fast_scaled.isNull()
        assert not smooth_scaled.isNull()
        
        print("✅ Quality modes test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Quality modes test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting browse tab cache system tests...\n")
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize PyQt6 application for testing
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    tests = [
        test_cache_settings,
        test_cache_class,
        test_quality_modes,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Cache system is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the cache implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
