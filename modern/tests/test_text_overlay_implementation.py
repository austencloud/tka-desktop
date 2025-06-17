#!/usr/bin/env python3
"""
Test Text Overlay Implementation

Quick test to verify the permanent text overlay implementation works correctly
in the actual V2 beat frame components.
"""

import sys
import os

# Add the modern directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Test V2 imports
try:
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from application.services.layout.layout_management_service import (
        LayoutManagementService,
    )
    from domain.models.core_models import (
        SequenceData,
        BeatData,
        MotionData,
        MotionType,
        RotationDirection,
        Location,
    )

    V2_IMPORTS_AVAILABLE = True
    print("✅ V2 imports successful - testing actual implementation")
except ImportError as e:
    V2_IMPORTS_AVAILABLE = False
    print(f"❌ V2 imports failed: {e}")


class TextOverlayImplementationTest(QMainWindow):
    """Test the actual V2 text overlay implementation"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Text Overlay Implementation Test - V2")
        self.setMinimumSize(1200, 800)

        self.beat_frame = None
        self.sequence_data = None

        self._setup_ui()

        if V2_IMPORTS_AVAILABLE:
            self._create_test_sequence()
            # Delay beat frame creation to allow UI to render
            QTimer.singleShot(100, self._create_beat_frame)
        else:
            self.status_label.setText(
                "❌ V2 imports unavailable - cannot test implementation"
            )

    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Text Overlay Implementation Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: #2c3e50; padding: 10px; background-color: #ecf0f1; border-radius: 5px; margin: 10px;"
        )
        layout.addWidget(title)

        # Status
        self.status_label = QLabel("Initializing test...")
        self.status_label.setStyleSheet(
            "color: #3498db; font-size: 12px; padding: 8px; background-color: #ebf3fd; border-radius: 4px; margin: 5px;"
        )
        layout.addWidget(self.status_label)

        # Beat frame container
        self.beat_frame_container = QWidget()
        self.beat_frame_container.setStyleSheet(
            "background-color: #f8f9fa; border: 2px solid #dee2e6; border-radius: 8px; margin: 10px;"
        )
        self.beat_frame_layout = QVBoxLayout(self.beat_frame_container)
        layout.addWidget(self.beat_frame_container)

    def _create_test_sequence(self):
        """Create a simple test sequence"""
        try:
            # Create simple motion data
            static_motion = MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori="in",
                end_ori="in",
            )

            pro_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.5,
                start_ori="in",
                end_ori="in",
            )

            # Create test beats
            beats = [
                BeatData(
                    beat_number=1,
                    letter="A",
                    blue_motion=pro_motion,
                    red_motion=pro_motion,
                ),
                BeatData(
                    beat_number=2,
                    letter="A",
                    blue_motion=pro_motion,
                    red_motion=pro_motion,
                ),
                BeatData(
                    beat_number=3,
                    letter="B",
                    blue_motion=static_motion,
                    red_motion=static_motion,
                ),
            ]

            # Create sequence
            self.sequence_data = SequenceData(
                name="Text Overlay Test",
                word="AAB",
                beats=beats,
                start_position="alpha1",
            )

            # Create start position data
            self.start_position_data = BeatData(
                beat_number=1,  # Must be positive
                letter="α",
                blue_motion=static_motion,
                red_motion=static_motion,
            )

            self.status_label.setText(
                f"✅ Test sequence created: {self.sequence_data.word} ({len(beats)} beats)"
            )
            print(
                f"✅ Created test sequence: {self.sequence_data.word} with {len(beats)} beats"
            )

        except Exception as e:
            self.status_label.setText(f"❌ Error creating test sequence: {e}")
            print(f"Error creating test sequence: {e}")

    def _create_beat_frame(self):
        """Create the V2 beat frame and test text overlays"""
        if not V2_IMPORTS_AVAILABLE or not self.sequence_data:
            return

        try:
            # Create layout service
            layout_service = LayoutManagementService()

            # Create V2 beat frame
            self.beat_frame = SequenceBeatFrame(layout_service)
            self.beat_frame_layout.addWidget(self.beat_frame)

            # Set start position data
            self.beat_frame.set_start_position(self.start_position_data)

            # Load the sequence (this should trigger text overlays)
            self.beat_frame.set_sequence(self.sequence_data)

            self.status_label.setText("✅ Beat frame created with text overlays!")
            self.status_label.setStyleSheet(
                "color: #27ae60; font-size: 12px; font-weight: bold; padding: 8px; background-color: #d5f4e6; border: 2px solid #27ae60; border-radius: 4px; margin: 5px;"
            )

            print("✅ Beat frame created successfully!")
            print("✅ Text overlays should now be visible:")
            print("   - START text on start position view")
            print("   - Beat numbers 1, 2, 3 on sequence beat views")
            print("   - Using widget overlay approach with transparent styling")

        except Exception as e:
            self.status_label.setText(f"❌ Error creating beat frame: {e}")
            print(f"Error creating beat frame: {e}")
            import traceback

            traceback.print_exc()


def main():
    """Main function to run the text overlay implementation test"""
    print("🧪 Starting Text Overlay Implementation Test")
    print("=" * 60)
    print("This test verifies the permanent text overlay implementation:")
    print("- Widget overlay approach (not scene-based)")
    print("- 'Start' text (sentence case) on start position")
    print("- Beat numbers on sequence beats")
    print("- Transparent styling for natural integration")
    print("- Mutual exclusivity between START text and beat numbers")
    print()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = TextOverlayImplementationTest()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
