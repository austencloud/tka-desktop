#!/usr/bin/env python3
"""
Test V1-style dynamic sizing for pictograph frames
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from domain.models.core_models import BeatData, MotionData, MotionType, Location, RotationDirection
from presentation.components.option_picker.clickable_pictograph_frame import ClickablePictographFrame


class DynamicSizingTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 V1-Style Dynamic Sizing Test")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create test beat data
        self.test_beat = BeatData(
            letter="A",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
            red_motion=MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.NORTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
        )
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔧 V1-Style Dynamic Sizing Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Resize the window to see pictographs dynamically resize based on container width.\n"
            "The algorithm calculates size for 8 columns like V1."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(instructions)
        
        # Container for pictographs
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        layout.addWidget(self.container, 1)
        
        # Create grid layout for pictographs
        container_layout = QHBoxLayout(self.container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create multiple pictograph frames to test sizing
        self.frames = []
        for i in range(8):  # 8 frames to test V1's 8-column layout
            frame = ClickablePictographFrame(self.test_beat, parent=self.container)
            frame.set_container_widget(self.container)  # Set container for dynamic sizing
            frame.clicked.connect(lambda beat_id, idx=i: self.on_frame_clicked(idx, beat_id))
            container_layout.addWidget(frame)
            self.frames.append(frame)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        resize_button = QPushButton("🔄 Trigger Resize")
        resize_button.clicked.connect(self.trigger_resize)
        button_layout.addWidget(resize_button)
        
        info_button = QPushButton("📊 Show Size Info")
        info_button.clicked.connect(self.show_size_info)
        button_layout.addWidget(info_button)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready - Resize window to test dynamic sizing")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #28a745; font-weight: bold; margin: 10px;")
        layout.addWidget(self.status_label)
        
    def trigger_resize(self):
        """Manually trigger resize on all frames"""
        for frame in self.frames:
            frame.resize_frame()
        self.status_label.setText("✅ Manual resize triggered")
        
    def show_size_info(self):
        """Show current size information"""
        container_width = self.container.width()
        if self.frames:
            frame_size = self.frames[0].size()
            info = f"Container: {container_width}px | Frame: {frame_size.width()}x{frame_size.height()}px"
            self.status_label.setText(info)
        
    def on_frame_clicked(self, index, beat_id):
        """Handle frame clicks"""
        self.status_label.setText(f"🎯 Clicked frame {index + 1}: {beat_id}")
        
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        # Trigger resize on all frames when window resizes
        for frame in self.frames:
            frame.resize_frame()
        
        # Update status
        container_width = self.container.width()
        self.status_label.setText(f"🔄 Window resized - Container width: {container_width}px")


def main():
    print("🔧 Starting V1-Style Dynamic Sizing Test...")
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    test_widget = DynamicSizingTestWidget()
    test_widget.show()
    
    print("✅ Test widget created. Resize the window to test dynamic sizing!")
    print("   - Frames should resize based on container width")
    print("   - Algorithm targets 8 columns like V1")
    print("   - Size bounds: 60px - 200px")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
