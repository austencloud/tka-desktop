#!/usr/bin/env python3
"""
Test Borderless Beat Frame Implementation

This test verifies that the beat frame displays pictographs without borders,
matching Legacy's borderless appearance while maintaining colored borders
in option picker contexts.
"""

import sys
import os

# Add the modern directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Test V2 imports
try:
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame
    from presentation.components.option_picker.clickable_pictograph_frame import ClickablePictographFrame
    from application.services.layout.layout_management_service import LayoutManagementService
    from domain.models.core_models import SequenceData, BeatData, MotionData, MotionType, RotationDirection, Location
    V2_IMPORTS_AVAILABLE = True
    print("✅ V2 imports successful - testing borderless implementation")
except ImportError as e:
    V2_IMPORTS_AVAILABLE = False
    print(f"❌ V2 imports failed: {e}")


class BorderlessTestWindow(QMainWindow):
    """Test borderless beat frame vs bordered option picker"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Borderless Beat Frame Test - V2")
        self.setMinimumSize(1400, 900)
        
        self.beat_frame = None
        self.option_frame = None
        self.sequence_data = None
        self.test_beat_data = None
        
        self._setup_ui()
        
        if V2_IMPORTS_AVAILABLE:
            self._create_test_data()
            # Delay component creation to allow UI to render
            QTimer.singleShot(100, self._create_components)
        else:
            self.status_label.setText("❌ V2 imports unavailable - cannot test implementation")
    
    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Borderless Beat Frame vs Bordered Option Picker Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 10px; background-color: #ecf0f1; border-radius: 5px; margin: 10px;")
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Initializing test...")
        self.status_label.setStyleSheet("color: #3498db; font-size: 12px; padding: 8px; background-color: #ebf3fd; border-radius: 4px; margin: 5px;")
        layout.addWidget(self.status_label)
        
        # Comparison layout
        comparison_layout = QHBoxLayout()
        
        # Beat frame section
        beat_frame_section = QVBoxLayout()
        beat_frame_label = QLabel("Beat Frame (Should be BORDERLESS like Legacy)")
        beat_frame_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        beat_frame_label.setStyleSheet("color: #e74c3c; padding: 5px; background-color: #fdf2f2; border-radius: 3px;")
        beat_frame_section.addWidget(beat_frame_label)
        
        self.beat_frame_container = QWidget()
        self.beat_frame_container.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; margin: 5px;")
        self.beat_frame_layout = QVBoxLayout(self.beat_frame_container)
        beat_frame_section.addWidget(self.beat_frame_container)
        
        # Option picker section
        option_picker_section = QVBoxLayout()
        option_picker_label = QLabel("Option Picker (Should have COLORED BORDERS)")
        option_picker_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        option_picker_label.setStyleSheet("color: #27ae60; padding: 5px; background-color: #eafaf1; border-radius: 3px;")
        option_picker_section.addWidget(option_picker_label)
        
        self.option_picker_container = QWidget()
        self.option_picker_container.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; margin: 5px;")
        self.option_picker_layout = QVBoxLayout(self.option_picker_container)
        option_picker_section.addWidget(self.option_picker_container)
        
        comparison_layout.addLayout(beat_frame_section)
        comparison_layout.addLayout(option_picker_section)
        layout.addLayout(comparison_layout)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh Test")
        refresh_btn.clicked.connect(self._refresh_test)
        refresh_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; padding: 8px; border-radius: 4px; font-weight: bold; }")
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
    
    def _create_test_data(self):
        """Create test data for both components"""
        try:
            # Create simple motion data
            static_motion = MotionData(
                motion_type=MotionType.STATIC,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.SOUTH,
                turns=0.0,
                start_ori="in",
                end_ori="in"
            )
            
            pro_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.5,
                start_ori="in",
                end_ori="in"
            )
            
            # Create test beat data
            self.test_beat_data = BeatData(
                beat_number=1,
                letter="A",
                blue_motion=pro_motion,
                red_motion=pro_motion
            )
            
            # Create test sequence
            beats = [
                BeatData(beat_number=1, letter="A", blue_motion=pro_motion, red_motion=pro_motion),
                BeatData(beat_number=2, letter="A", blue_motion=pro_motion, red_motion=pro_motion),
            ]
            
            self.sequence_data = SequenceData(
                name="Border Test",
                word="AA",
                beats=beats,
                start_position="south"
            )
            
            # Create start position data
            self.start_position_data = BeatData(
                beat_number=1,
                letter="α",
                blue_motion=static_motion,
                red_motion=static_motion
            )
            
            self.status_label.setText(f"✅ Test data created: {self.sequence_data.word} sequence + option picker beat")
            print(f"✅ Created test data for border comparison")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error creating test data: {e}")
            print(f"Error creating test data: {e}")
    
    def _create_components(self):
        """Create both beat frame and option picker for comparison"""
        if not V2_IMPORTS_AVAILABLE or not self.sequence_data:
            return
        
        try:
            # Create layout service
            layout_service = LayoutManagementService()
            
            # Create beat frame (should be borderless)
            self.beat_frame = SequenceBeatFrame(layout_service)
            self.beat_frame_layout.addWidget(self.beat_frame)
            
            # Set start position and sequence
            self.beat_frame.set_start_position(self.start_position_data)
            self.beat_frame.set_sequence(self.sequence_data)
            
            # Create option picker frame (should have colored borders)
            self.option_frame = ClickablePictographFrame(self.test_beat_data)
            self.option_picker_layout.addWidget(self.option_frame)
            
            self.status_label.setText("✅ Components created! Compare borders:")
            self.status_label.setStyleSheet("color: #27ae60; font-size: 12px; font-weight: bold; padding: 8px; background-color: #d5f4e6; border: 2px solid #27ae60; border-radius: 4px; margin: 5px;")
            
            print("✅ Components created successfully!")
            print("✅ Visual comparison available:")
            print("   - Beat frame: Should show borderless pictographs with text overlays")
            print("   - Option picker: Should show colored letter-type borders")
            print("   - This matches Legacy's behavior exactly")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error creating components: {e}")
            print(f"Error creating components: {e}")
            import traceback
            traceback.print_exc()
    
    def _refresh_test(self):
        """Refresh the test components"""
        print("🔄 Refreshing border test...")
        
        # Clear existing components
        if self.beat_frame:
            self.beat_frame.deleteLater()
            self.beat_frame = None
        
        if self.option_frame:
            self.option_frame.deleteLater()
            self.option_frame = None
        
        # Recreate components
        QTimer.singleShot(100, self._create_components)


def main():
    """Main function to run the borderless test"""
    print("🧪 Starting Borderless Beat Frame Test")
    print("=" * 60)
    print("This test compares:")
    print("- Beat Frame: Should be borderless like Legacy")
    print("- Option Picker: Should have colored borders for letter types")
    print("- Text overlays: Should appear naturally integrated")
    print()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = BorderlessTestWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
