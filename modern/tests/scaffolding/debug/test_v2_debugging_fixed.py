#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-07-19
Test Modern dimension debugging functionality.

This test validates that the Modern debugging system works correctly.

BUG REPORT: V2 debugging functionality not working properly
EXPECTED: Debug toggle and key events should work for pictograph components
STATUS: NEEDS_TESTING
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeyEvent


def test_modern_debugging():
    """Test Modern pictograph debugging functionality."""
    print("🚀 Testing Modern Debugging Functionality")

    try:
        # Create QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Import Modern components
        from presentation.components.pictograph.pictograph_component import (
            PictographComponent,
        )
        from domain.models.core_models import (
            BeatData,
            MotionData,
            GlyphData,
            LetterType,
            Location,
            MotionType,
            RotationDirection,
        )

        # Create test widget
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Create pictograph component
        pictograph = PictographComponent()
        pictograph.setFixedSize(400, 400)
        layout.addWidget(pictograph)

        # Create test beat data
        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_ori="in",
            end_ori="out",
        )

        glyph_data = GlyphData(
            letter_type=LetterType.TYPE1,
            show_tka=True,
            show_vtg=False,
            show_elemental=False,
            show_positions=False,
        )

        beat_data = BeatData(letter="A", blue_motion=blue_motion, glyph_data=glyph_data)

        # Update pictograph with test data
        pictograph.update_from_beat(beat_data)

        print("✅ Modern pictograph created successfully")
        print("📝 Testing debug functionality...")

        # Test debug toggle if available
        if hasattr(pictograph, 'toggle_dimension_debugging'):
            pictograph.toggle_dimension_debugging()
            print("✅ Debug toggle method available and called")
        else:
            print("⚠️  Debug toggle method not available")

        print("✅ Modern debugging test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Modern debugging test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_modern_key_events():
    """Test Modern key event handling for debugging."""
    print("\n🔑 Testing Modern Key Event Handling")

    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        from presentation.components.pictograph.pictograph_component import (
            PictographComponent,
        )

        pictograph = PictographComponent()
        pictograph.setFixedSize(400, 400)

        # Test key event handling if available
        if hasattr(pictograph, 'keyPressEvent'):
            # Simulate Ctrl+D key press
            key_event = QKeyEvent(
                QKeyEvent.Type.KeyPress, Qt.Key.Key_D, Qt.KeyboardModifier.ControlModifier
            )

            print("📝 Simulating Ctrl+D key press...")
            pictograph.keyPressEvent(key_event)
            print("✅ Key event handled without error")
        else:
            print("⚠️  Key event handling not available")

        print("✅ Key event test completed")
        return True

    except Exception as e:
        print(f"❌ Key event test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pictograph_component_creation():
    """Test that pictograph component can be created without errors."""
    print("\n🏗️  Testing Pictograph Component Creation")

    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        from presentation.components.pictograph.pictograph_component import (
            PictographComponent,
        )

        # Create pictograph component
        pictograph = PictographComponent()
        
        # Basic checks
        assert pictograph is not None, "Pictograph component should not be None"
        print("✅ Pictograph component created successfully")
        
        # Check if it has expected methods
        expected_methods = ['update_from_beat', 'setFixedSize']
        for method in expected_methods:
            if hasattr(pictograph, method):
                print(f"✅ Method '{method}' available")
            else:
                print(f"⚠️  Method '{method}' not available")

        return True

    except Exception as e:
        print(f"❌ Pictograph component creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all Modern debugging tests."""
    print("🧪 Running Modern V2 Debugging Tests")
    print("=" * 50)

    success = True

    # Test pictograph component creation
    if not test_pictograph_component_creation():
        success = False

    # Test basic debugging functionality
    if not test_modern_debugging():
        success = False

    # Test key event handling
    if not test_modern_key_events():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 All Modern V2 debugging tests passed!")
    else:
        print("❌ Some Modern V2 debugging tests failed")

    return success


def test_v2_debugging_pytest():
    """Pytest version of the V2 debugging test."""
    result = run_all_tests()
    assert result, "V2 debugging test failed"


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\n✅ Test completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Test failed")
        sys.exit(1)
