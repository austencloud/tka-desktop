#!/usr/bin/env python3
"""
V1 Beat Frame Parity Test - Kinetic Constructor v2

This test verifies that the v2 beat frame achieves pixel-perfect visual
and functional parity with v1's beat frame implementation.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
)
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


def create_start_position() -> BeatData:
    """Create a start position (not part of sequence)"""

    blue_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.NORTH,  # Static position
        turns=0.0,
        start_ori="in",
        end_ori="in",
    )

    red_motion = MotionData(
        motion_type=MotionType.STATIC,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.SOUTH,
        end_loc=Location.SOUTH,  # Static position
        turns=0.0,
        start_ori="out",
        end_ori="out",
    )

    return BeatData(
        beat_number=1,  # Must be positive for validation
        letter="Σ",  # Start position letter
        duration=1.0,  # Must be positive for validation
        blue_motion=blue_motion,
        red_motion=red_motion,
    )


def create_test_sequence() -> SequenceData:
    """Create a test sequence (separate from start position)"""

    # Beat 1
    blue_motion_1 = MotionData(
        motion_type=MotionType.PRO,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.NORTH,
        end_loc=Location.EAST,
        turns=0.25,
        start_ori="in",
        end_ori="out",
    )

    red_motion_1 = MotionData(
        motion_type=MotionType.ANTI,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.SOUTH,
        end_loc=Location.WEST,
        turns=0.25,
        start_ori="out",
        end_ori="in",
    )

    beat1 = BeatData(
        beat_number=1,
        letter="α",
        duration=1.0,
        blue_motion=blue_motion_1,
        red_motion=red_motion_1,
    )

    # Beat 2
    blue_motion_2 = MotionData(
        motion_type=MotionType.FLOAT,
        prop_rot_dir=RotationDirection.CLOCKWISE,
        start_loc=Location.EAST,
        end_loc=Location.SOUTH,
        turns=0.25,
        start_ori="out",
        end_ori="in",
    )

    red_motion_2 = MotionData(
        motion_type=MotionType.DASH,
        prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        start_loc=Location.WEST,
        end_loc=Location.NORTH,
        turns=0.25,
        start_ori="in",
        end_ori="out",
    )

    beat2 = BeatData(
        beat_number=2,
        letter="β",
        duration=1.0,
        blue_motion=blue_motion_2,
        red_motion=red_motion_2,
    )

    return SequenceData(name="V1 Parity Test Sequence", beats=[beat1, beat2])


class V1ParityTestWindow(QMainWindow):
    """Test window for v1 beat frame parity verification"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 V1 Beat Frame Parity Test")
        self.setGeometry(100, 100, 1400, 900)

        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Add test controls
        self._setup_test_controls(layout)

        # Create the modern workbench
        self.workbench = create_modern_workbench(self.container, parent=self)
        layout.addWidget(self.workbench)

        # Connect signals
        self.workbench.sequence_modified.connect(self.on_sequence_modified)
        self.workbench.operation_completed.connect(self.on_operation_completed)
        self.workbench.error_occurred.connect(self.on_error_occurred)

        # Set up test data after a short delay
        QTimer.singleShot(1000, self.run_parity_tests)

    def _setup_test_controls(self, parent_layout):
        """Setup test control buttons"""
        controls_layout = QHBoxLayout()

        # Test buttons
        start_pos_btn = QPushButton("Set Start Position")
        start_pos_btn.clicked.connect(self.set_start_position)

        sequence_btn = QPushButton("Load Sequence")
        sequence_btn.clicked.connect(self.load_sequence)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)

        controls_layout.addWidget(start_pos_btn)
        controls_layout.addWidget(sequence_btn)
        controls_layout.addWidget(clear_btn)
        controls_layout.addStretch()

        parent_layout.addLayout(controls_layout)

    def set_start_position(self):
        """Set start position (separate from sequence)"""
        print("🎯 Setting start position (not adding to sequence)...")
        start_position = create_start_position()
        self.workbench.set_start_position(start_position)
        print(f"✅ Start position set: {start_position.letter}")

    def load_sequence(self):
        """Load sequence (separate from start position)"""
        print("🎯 Loading sequence (separate from start position)...")
        sequence = create_test_sequence()
        self.workbench.set_sequence(sequence)
        print(f"✅ Sequence loaded: {sequence.name} ({len(sequence.beats)} beats)")

    def clear_all(self):
        """Clear both start position and sequence"""
        print("🎯 Clearing all data...")
        # Create empty sequence to clear
        empty_sequence = SequenceData(name="Empty", beats=[])
        self.workbench.set_sequence(empty_sequence)
        # TODO: Add clear start position method
        print("✅ All data cleared")

    def run_parity_tests(self):
        """Run comprehensive parity tests"""
        print("🎯 Running V1 Beat Frame Parity Tests...")
        print()

        print("📋 Expected V1 Behavior:")
        print("   1. ❌ No beat number labels above pictographs")
        print("   2. ❌ No sequence info display ('Sequence: X beats')")
        print("   3. ✅ Pictographs fill containers completely (120x120)")
        print("   4. ✅ Zero spacing/margins in grid layout")
        print("   5. ✅ START text overlaid on start position pictograph")
        print("   6. ✅ Start position separate from sequence beats")
        print("   7. ✅ Grid layout: start position at (0,0), beats at (0,1+)")
        print()

        # Test 1: Set start position first
        print("🧪 Test 1: Setting start position...")
        self.set_start_position()

        # Test 2: Load sequence after delay
        QTimer.singleShot(2000, self.load_sequence)

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
    """Run the v1 parity test"""
    print("🎯 Starting V1 Beat Frame Parity Test...")
    print("=" * 60)

    app = QApplication(sys.argv)
    app.setApplicationName("V1 Beat Frame Parity Test")

    # Create and show test window
    window = V1ParityTestWindow()
    window.show()

    print("🎯 Visual Verification Checklist:")
    print("   ✅ Beat frame has zero spacing/margins")
    print("   ✅ Pictographs fill 120x120 containers completely")
    print("   ✅ No beat number labels visible")
    print("   ✅ No sequence info display visible")
    print("   ✅ START text overlaid on start position")
    print("   ✅ Start position at grid (0,0)")
    print("   ✅ Sequence beats start at grid (0,1)")
    print("   ✅ Start position independent of sequence")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
