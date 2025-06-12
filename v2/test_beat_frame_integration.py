#!/usr/bin/env python3
"""
Test Beat Frame Integration in Kinetic Constructor v2

This test verifies that the ModernSequenceWorkbench properly integrates
with the ModernBeatFrame and displays actual pictographs.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.factories.workbench_factory import create_modern_workbench
from src.domain.models.core_models import (
    SequenceData,
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


def create_test_sequence() -> SequenceData:
    """Create a test sequence with actual motion data"""

    # Create test motion data for blue and red
    blue_motion = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.SOUTH,
        turns=0.5,
        start_ori="in",
        end_ori="out",
    )

    red_motion = MotionData(
        motion_type=MotionType.ANTI,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.EAST,
        end_loc=Location.WEST,
        turns=1.0,
        start_ori="out",
        end_ori="in",
    )

    # Create test beat data
    beat1 = BeatData(
        beat_number=1,
        letter="α",
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion,
    )

    beat2 = BeatData(
        beat_number=2,
        letter="β",
        duration=1.0,
        blue_motion=blue_motion,
        red_motion=red_motion,
    )

    # Create sequence with test beats
    sequence = SequenceData(name="Test Sequence", beats=[beat1, beat2])

    return sequence


class TestBeatFrameWindow(QMainWindow):
    """Test window for beat frame integration"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Beat Frame Integration Test")
        self.setGeometry(100, 100, 1200, 800)

        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create the modern workbench
        self.workbench = create_modern_workbench(self.container, parent=self)
        layout.addWidget(self.workbench)

        # Connect signals
        self.workbench.sequence_modified.connect(self.on_sequence_modified)
        self.workbench.operation_completed.connect(self.on_operation_completed)
        self.workbench.error_occurred.connect(self.on_error_occurred)

        # Set up test sequence after a short delay
        QTimer.singleShot(1000, self.load_test_sequence)

    def load_test_sequence(self):
        """Load test sequence into the workbench"""
        print("🔄 Loading test sequence into beat frame...")

        test_sequence = create_test_sequence()
        self.workbench.set_sequence(test_sequence)

        print(f"✅ Test sequence loaded: {test_sequence.name}")
        print(f"   - Beats: {len(test_sequence.beats)}")
        print(f"   - Beat 1: {test_sequence.beats[0].letter}")
        print(f"   - Beat 2: {test_sequence.beats[1].letter}")

    def on_sequence_modified(self, sequence):
        """Handle sequence modification"""
        print(f"🔄 Sequence modified: {sequence.name} ({len(sequence.beats)} beats)")

    def on_operation_completed(self, message):
        """Handle operation completion"""
        print(f"✅ Operation completed: {message}")

    def on_error_occurred(self, error):
        """Handle errors"""
        print(f"❌ Error occurred: {error}")


def main():
    """Run the beat frame integration test"""
    print("🧪 Starting Beat Frame Integration Test...")

    app = QApplication(sys.argv)
    app.setApplicationName("Beat Frame Integration Test")

    # Create and show test window
    window = TestBeatFrameWindow()
    window.show()

    print("🎯 Test window created - check for:")
    print("   1. Beat frame displays with grid layout")
    print("   2. Start position view shows first beat")
    print("   3. Beat views show actual pictographs")
    print("   4. Sequence info displays correctly")
    print("   5. No placeholder text in beat slots")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
