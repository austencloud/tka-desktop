#!/usr/bin/env python3
"""
Quick test script to verify image quality test widget functionality.
"""

import sys
import os
from pathlib import Path

# Add src to path if needed
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QPixmap
    from PyQt6.QtCore import QSize, Qt

    print("✅ PyQt6 imports successful")
except ImportError as e:
    print(f"❌ PyQt6 import error: {e}")
    sys.exit(1)

try:
    from PIL import Image as PILImage

    print("✅ PIL/Pillow available")
    PIL_AVAILABLE = True
except ImportError:
    print("⚠️ PIL/Pillow not available - some methods will be disabled")
    PIL_AVAILABLE = False


def test_basic_scaling():
    """Test basic Qt scaling functionality."""
    print("\n🔧 Testing basic Qt scaling...")

    app = QApplication([])

    # Create a test pixmap
    test_pixmap = QPixmap(800, 600)
    test_pixmap.fill()

    if test_pixmap.isNull():
        print("❌ Failed to create test pixmap")
        return False

    print(f"✅ Created test pixmap: {test_pixmap.width()}x{test_pixmap.height()}")

    # Test Qt smooth scaling
    target_size = QSize(200, 150)
    scaled_pixmap = test_pixmap.scaled(
        target_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )

    if scaled_pixmap.isNull():
        print("❌ Failed to scale pixmap")
        return False

    print(f"✅ Scaled pixmap: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
    return True


def test_pil_conversion():
    """Test PIL conversion if available."""
    if not PIL_AVAILABLE:
        print("⚠️ Skipping PIL tests - not available")
        return True

    print("\n🔧 Testing PIL conversion...")

    try:
        # Create a simple PIL image
        pil_image = PILImage.new("RGB", (100, 100), (255, 0, 0))
        print("✅ Created PIL image")

        # Test Lanczos scaling
        scaled_pil = pil_image.resize((50, 50), PILImage.Resampling.LANCZOS)
        print("✅ PIL Lanczos scaling successful")

        return True
    except Exception as e:
        print(f"❌ PIL test failed: {e}")
        return False


def main():
    """Run basic tests."""
    print("🧪 Image Quality Test - Basic Functionality Check")
    print("=" * 50)

    # Test Qt functionality
    qt_ok = test_basic_scaling()

    # Test PIL functionality
    pil_ok = test_pil_conversion()

    print("\n📊 Test Results:")
    print(f"Qt Scaling: {'✅ PASS' if qt_ok else '❌ FAIL'}")
    print(f"PIL Support: {'✅ PASS' if pil_ok else '❌ FAIL'}")

    if qt_ok:
        print("\n🎉 Basic functionality verified!")
        print("You can now run: python image_quality_test_widget.py")
    else:
        print("\n❌ Basic tests failed - check your Qt installation")

    return qt_ok and pil_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
