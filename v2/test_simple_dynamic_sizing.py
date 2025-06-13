#!/usr/bin/env python3
"""
Simple test for V1-style dynamic sizing algorithm
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class DynamicFrame(QFrame):
    """Simple frame that implements V1-style dynamic sizing"""
    
    def __init__(self, label_text="Frame", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.container_widget = None
        
        # Setup frame appearance
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setStyleSheet("""
            DynamicFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 6px;
            }
            DynamicFrame:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
                border-width: 3px;
            }
        """)
        
        # Add label
        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout.addWidget(self.label)
        
        # Initial size
        self.setFixedSize(160, 160)
        
    def set_container_widget(self, container_widget):
        """Set container widget for dynamic sizing (V1-style, but decoupled)"""
        self.container_widget = container_widget
    
    def resize_frame(self):
        """Resize frame using V1's dynamic sizing algorithm based on container width"""
        if not self.container_widget:
            return
            
        try:
            # V1's sizing algorithm adapted for container-based sizing
            container_width = self.container_widget.width()
            if container_width <= 0:
                return  # Container not ready yet
            
            # V1's algorithm: Calculate size based on desired columns and available width
            desired_columns = 8  # V1 default
            spacing = 8  # Grid spacing
            margin = 20  # Container margins
            
            # Calculate available width for pictographs
            available_width = container_width - (2 * margin)
            
            # Calculate size per pictograph: (width - spacing) / columns
            total_spacing = spacing * (desired_columns - 1)
            size_per_pictograph = (available_width - total_spacing) / desired_columns
            
            # Apply V1's border width calculation
            border_width = max(1, int(size_per_pictograph * 0.015))
            final_size = int(size_per_pictograph - (2 * border_width))
            
            # Ensure reasonable size bounds
            final_size = max(60, min(final_size, 200))  # Between 60px and 200px
            
            # Apply the calculated size
            self.setFixedSize(final_size, final_size)
            
            # Update label with size info
            self.label.setText(f"{self.label_text}\n{final_size}px")
            
            print(f"🔧 {self.label_text} resized to {final_size}x{final_size} (container_width={container_width}, columns={desired_columns})")
            
        except Exception as e:
            print(f"❌ Error in resize_frame: {e}")


class DynamicSizingTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 V1-Style Dynamic Sizing Test")
        self.setGeometry(100, 100, 1000, 700)
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
            "Resize the window to see frames dynamically resize based on container width.\n"
            "The algorithm calculates size for 8 columns like V1."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(instructions)
        
        # Container for frames
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
        
        # Create grid layout for frames
        container_layout = QHBoxLayout(self.container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create multiple frames to test sizing
        self.frames = []
        for i in range(8):  # 8 frames to test V1's 8-column layout
            frame = DynamicFrame(f"F{i+1}", parent=self.container)
            frame.set_container_widget(self.container)  # Set container for dynamic sizing
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
