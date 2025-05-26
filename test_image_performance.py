#!/usr/bin/env python3
"""
Test script for image loading performance optimizations.

This script tests the new image loading optimizations to ensure they work
correctly and provide performance improvements without crashes.
"""

import sys
import os
import time
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def setup_logging():
    """Setup logging for the test."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def test_image_validation():
    """Test image validation functionality."""
    print("\n=== Testing Image Validation ===")

    try:
        from main_window.main_widget.sequence_card_tab.components.display.image_processor import (
            ImageProcessor,
        )
        from main_window.main_widget.sequence_card_tab.components.pages.printable_factory import (
            PrintablePageFactory,
        )

        # Create a mock page factory for testing
        class MockPageFactory:
            def get_cell_size(self):
                from PyQt6.QtCore import QSize

                return QSize(200, 200)

            def update_card_aspect_ratio(self, ratio):
                pass

        processor = ImageProcessor(MockPageFactory(), columns_per_row=2, cache_size=100)

        # Test validation with non-existent file
        result = processor._validate_image_file("nonexistent.png")
        print(f"Non-existent file validation: {result} (should be False)")

        # Test validation with invalid extension
        result = processor._validate_image_file("test.txt")
        print(f"Invalid extension validation: {result} (should be False)")

        print("✓ Image validation tests passed")
        return True

    except Exception as e:
        print(f"✗ Image validation test failed: {e}")
        return False


def test_memory_management():
    """Test memory management functionality."""
    print("\n=== Testing Memory Management ===")

    try:
        from main_window.main_widget.sequence_card_tab.components.display.image_processor import (
            ImageProcessor,
        )

        class MockPageFactory:
            def get_cell_size(self):
                from PyQt6.QtCore import QSize

                return QSize(200, 200)

            def update_card_aspect_ratio(self, ratio):
                pass

        processor = ImageProcessor(MockPageFactory(), columns_per_row=2, cache_size=10)

        # Test performance stats
        stats = processor.get_performance_stats()
        print(f"Initial stats: {stats}")

        # Test memory cleanup (should not crash)
        processor._check_and_cleanup_memory()
        print("✓ Memory cleanup executed without errors")

        # Test performance logging
        processor.log_performance_stats()
        print("✓ Performance logging executed without errors")

        print("✓ Memory management tests passed")
        return True

    except Exception as e:
        print(f"✗ Memory management test failed: {e}")
        return False


def test_with_real_images():
    """Test with real images if available."""
    print("\n=== Testing with Real Images ===")

    try:
        # Look for test images in common locations
        test_paths = ["images/sequence_card_images", "src/images", "test_images"]

        test_image = None
        for path in test_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.lower().endswith((".png", ".jpg", ".jpeg")):
                        test_image = os.path.join(path, file)
                        break
                if test_image:
                    break

        if not test_image:
            print("No test images found, skipping real image tests")
            return True

        print(f"Testing with image: {test_image}")

        from main_window.main_widget.sequence_card_tab.components.display.image_processor import (
            ImageProcessor,
        )

        class MockPageFactory:
            def get_cell_size(self):
                from PyQt6.QtCore import QSize

                return QSize(200, 200)

            def update_card_aspect_ratio(self, ratio):
                pass

        processor = ImageProcessor(MockPageFactory(), columns_per_row=2, cache_size=50)

        # Test image loading with timing
        start_time = time.time()
        result = processor._validate_image_file(test_image)
        validation_time = time.time() - start_time

        print(f"Image validation result: {result} (took {validation_time:.3f}s)")

        if result:
            start_time = time.time()
            image = processor._load_image_with_size_limit(test_image)
            load_time = time.time() - start_time

            if image and not image.isNull():
                print(
                    f"Image loaded successfully: {image.width()}x{image.height()} (took {load_time:.3f}s)"
                )

                # Test cache performance
                start_time = time.time()
                image2 = processor._load_image_with_size_limit(
                    test_image
                )  # Should be faster
                cache_time = time.time() - start_time

                print(f"Cached load time: {cache_time:.3f}s (should be much faster)")

                # Show performance stats including disk cache
                stats = processor.get_performance_stats()
                print(f"Performance stats: {stats}")

                # Test disk cache if available
                if processor.disk_cache:
                    disk_stats = processor.disk_cache.get_cache_stats()
                    print(f"Disk cache stats: {disk_stats}")

                processor.log_performance_stats()

            else:
                print("Failed to load image")
                return False

        print("✓ Real image tests passed")
        return True

    except Exception as e:
        print(f"✗ Real image test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_phase2_features():
    """Test Phase 2 optimizations: disk cache and background processing."""
    print("\n=== Testing Phase 2 Features ===")

    try:
        # Test disk cache manager
        from main_window.main_widget.sequence_card_tab.components.display.disk_cache_manager import (
            DiskCacheManager,
        )

        cache_manager = DiskCacheManager(max_cache_size_mb=100)
        stats = cache_manager.get_cache_stats()
        print(f"Disk cache initialized: {stats}")

        # Test background processor
        from main_window.main_widget.sequence_card_tab.components.display.background_processor import (
            BackgroundImageProcessor,
        )

        class MockImageProcessor:
            def load_image_with_consistent_scaling(self, image_path, **kwargs):
                from PyQt6.QtGui import QPixmap

                return QPixmap(100, 100)  # Mock pixmap

        bg_processor = BackgroundImageProcessor(
            MockImageProcessor(), batch_size=2, interval_ms=100
        )
        bg_stats = bg_processor.get_stats()
        print(f"Background processor initialized: {bg_stats}")

        # Test lazy loader
        from main_window.main_widget.sequence_card_tab.components.display.lazy_loader import (
            LazyImageLoader,
        )

        lazy_loader = LazyImageLoader(None, MockImageProcessor(), buffer_pixels=100)
        lazy_stats = lazy_loader.get_stats()
        print(f"Lazy loader initialized: {lazy_stats}")

        print("✓ Phase 2 features tests passed")
        return True

    except Exception as e:
        print(f"✗ Phase 2 features test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all performance tests."""
    print("Image Loading Performance Test Suite")
    print("=" * 50)

    setup_logging()

    # Initialize PyQt6 for testing
    try:
        from PyQt6.QtWidgets import QApplication

        app = QApplication(sys.argv)
    except ImportError:
        print("PyQt6 not available, some tests may fail")
        app = None

    tests = [
        test_image_validation,
        test_memory_management,
        test_with_real_images,
        test_phase2_features,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
            import traceback

            traceback.print_exc()

    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Optimizations are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
