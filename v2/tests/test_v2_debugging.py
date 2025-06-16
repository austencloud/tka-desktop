"""
Test Modern dimension debugging functionality.

This test validates that the Modern debugging system works correctly.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeyEvent

# Add Modern source path
current_dir = os.path.dirname(os.path.abspath(__file__))
v2_src_path = os.path.join(current_dir, "..", "src")
sys.path.insert(0, v2_src_path)

print(f"Modern path: {v2_src_path}")
print(f"Modern exists: {os.path.exists(v2_src_path)}")


def test_v2_debugging():
    """Test Modern pictograph debugging functionality."""
    print("🚀 Testing Modern Debugging Functionality")

    try:
        # Create QApplication
        app = QApplication(sys.argv)

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
        )

        # Create test widget
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Create pictograph component
        pictograph = PictographComponent()
        pictograph.setFixedSize(400, 400)
        layout.addWidget(pictograph)

        # Create test beat data
        from domain.models.core_models import RotationDirection

        blue_motion = MotionData(
            motion_type=MotionType.PRO,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.0,
            prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        glyph_data = GlyphData(
            letter_type=LetterType.Type1,
            show_tka=True,
            show_vtg=False,
            show_elemental=False,
            show_positions=False,
        )

        beat_data = BeatData(letter="A", blue_motion=blue_motion, glyph_data=glyph_data)

        # Update pictograph with test data
        pictograph.update_from_beat(beat_data)

        # Show widget
        widget.show()
        widget.setFocus()

        print("✅ Modern pictograph created successfully")
        print("📝 Testing debug functionality...")

        # Test debug toggle
        pictograph.toggle_dimension_debugging()

        # Process events to trigger debug output
        app.processEvents()

        # Wait a bit for debug timer
        QTimer.singleShot(200, app.quit)
        app.exec()

        print("✅ Modern debugging test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Modern debugging test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_v2_key_events():
    """Test Modern key event handling for debugging."""
    print("\n🔑 Testing Modern Key Event Handling")

    try:
        app = QApplication(sys.argv)

        from presentation.components.pictograph.pictograph_component import (
            PictographComponent,
        )

        pictograph = PictographComponent()
        pictograph.setFixedSize(400, 400)
        pictograph.show()
        pictograph.setFocus()

        # Simulate Ctrl+D key press
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_D, Qt.KeyboardModifier.ControlModifier
        )

        print("📝 Simulating Ctrl+D key press...")
        pictograph.keyPressEvent(key_event)

        # Process events
        app.processEvents()

        # Wait for debug timer
        QTimer.singleShot(200, app.quit)
        app.exec()

        print("✅ Key event test completed")
        return True

    except Exception as e:
        print(f"❌ Key event test failed: {e}")
        return False


def run_all_tests():
    """Run all Modern debugging tests."""
    print("🧪 Running Modern Debugging Tests")
    print("=" * 50)

    success = True

    # Test basic debugging functionality
    if not test_v2_debugging():
        success = False

    # Test key event handling
    if not test_v2_key_events():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 All Modern debugging tests passed!")
    else:
        print("❌ Some Modern debugging tests failed")

    return success


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
