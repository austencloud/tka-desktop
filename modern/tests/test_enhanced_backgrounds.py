#!/usr/bin/env python3
"""
Test script to verify all enhanced background features are working correctly.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer

# Add modern src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from src.application.services.ui.ui_state_management_service import UIStateManagementService
from src.application.services.settings.settings_service import SettingsService
from src.presentation.components.backgrounds.background_widget import MainBackgroundWidget


class BackgroundTestWindow(QMainWindow):
    """Test window to verify enhanced background functionality."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Enhanced Background System Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create services
        self.ui_state_service = UIStateManagementService()
        self.settings_service = SettingsService(self.ui_state_service)
        
        # Background widget
        self.background_widget = None
        self.current_background = "Aurora"
        
        # Test cycle
        self.test_backgrounds = ["Aurora", "AuroraBorealis", "Starfield", "Snowfall", "Bubbles"]
        self.test_index = 0
        
        self._setup_ui()
        self._setup_background()
        self._setup_auto_cycle()
    
    def _setup_ui(self):
        """Set up the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎨 Enhanced Background System Test")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background: rgba(0,0,0,100); padding: 10px; border-radius: 5px;")
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Testing enhanced backgrounds with animations...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: white; background: rgba(0,0,0,100); padding: 10px; border-radius: 5px;")
        layout.addWidget(self.status_label)
        
        # Test buttons
        button_layout = QVBoxLayout()
        
        for bg_type in self.test_backgrounds:
            button = QPushButton(f"🎭 Test {bg_type}")
            button.setFixedHeight(40)
            button.clicked.connect(lambda checked, bg=bg_type: self._test_background(bg))
            button_layout.addWidget(button)
        
        # Auto cycle button
        self.cycle_button = QPushButton("🔄 Start Auto Cycle (5s intervals)")
        self.cycle_button.setFixedHeight(50)
        self.cycle_button.clicked.connect(self._toggle_auto_cycle)
        button_layout.addWidget(self.cycle_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def _setup_background(self):
        """Set up the initial background."""
        self._test_background("Aurora")
    
    def _setup_auto_cycle(self):
        """Set up auto cycling timer."""
        self.cycle_timer = QTimer(self)
        self.cycle_timer.timeout.connect(self._cycle_next_background)
        self.cycling = False
    
    def _test_background(self, background_type: str):
        """Test a specific background type."""
        try:
            print(f"🧪 Testing {background_type} background...")
            
            # Clean up old background
            if self.background_widget:
                if hasattr(self.background_widget, 'cleanup'):
                    self.background_widget.cleanup()
                self.background_widget.hide()
                self.background_widget.deleteLater()
            
            # Create new background
            self.background_widget = MainBackgroundWidget(self, background_type)
            self.background_widget.setGeometry(self.rect())
            self.background_widget.lower()
            self.background_widget.show()
            
            self.current_background = background_type
            self.status_label.setText(f"✨ Currently testing: {background_type}")
            
            # Test specific features
            self._test_background_features(background_type)
            
            print(f"✅ {background_type} background test completed!")
            
        except Exception as e:
            print(f"❌ Failed to test {background_type}: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"❌ Error testing {background_type}: {e}")
    
    def _test_background_features(self, background_type: str):
        """Test specific features of each background type."""
        features = {
            "Aurora": ["Sparkle animation", "Blob movement", "Color gradients"],
            "AuroraBorealis": ["Light wave animation", "Color transitions", "Flowing effects"],
            "Starfield": ["Star twinkling", "Comet trails", "Moon rendering", "UFO movement"],
            "Snowfall": ["Falling snowflakes", "Santa animation", "Shooting stars"],
            "Bubbles": ["Rising bubbles", "Fish swimming", "Underwater effects"]
        }
        
        bg_features = features.get(background_type, ["Basic animation"])
        print(f"   🔍 Expected features: {', '.join(bg_features)}")
    
    def _toggle_auto_cycle(self):
        """Toggle auto cycling through backgrounds."""
        if self.cycling:
            self.cycle_timer.stop()
            self.cycling = False
            self.cycle_button.setText("🔄 Start Auto Cycle (5s intervals)")
            self.status_label.setText(f"⏸️ Auto cycle stopped on: {self.current_background}")
        else:
            self.cycle_timer.start(5000)  # 5 second intervals
            self.cycling = True
            self.cycle_button.setText("⏹️ Stop Auto Cycle")
            self.status_label.setText(f"🔄 Auto cycling backgrounds every 5 seconds...")
    
    def _cycle_next_background(self):
        """Cycle to the next background in the test sequence."""
        self.test_index = (self.test_index + 1) % len(self.test_backgrounds)
        next_bg = self.test_backgrounds[self.test_index]
        self._test_background(next_bg)
    
    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)
        if self.background_widget:
            self.background_widget.setGeometry(self.rect())
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.background_widget and hasattr(self.background_widget, 'cleanup'):
            self.background_widget.cleanup()
        super().closeEvent(event)


def main():
    """Run the enhanced background test."""
    print("🧪 Starting Enhanced Background System Test...")
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = BackgroundTestWindow()
    window.show()
    
    print("✨ Test window opened!")
    print("🎭 Click buttons to test individual backgrounds")
    print("🔄 Use auto cycle to test all backgrounds automatically")
    print("🎨 Look for:")
    print("   - Aurora: Sparkles and flowing blobs")
    print("   - AuroraBorealis: Flowing light waves")
    print("   - Starfield: Twinkling stars, comets, moon, UFOs")
    print("   - Snowfall: Falling snow, Santa, shooting stars")
    print("   - Bubbles: Rising bubbles and swimming fish")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
