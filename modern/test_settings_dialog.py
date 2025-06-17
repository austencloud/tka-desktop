#!/usr/bin/env python3
"""
Test script to verify the settings dialog with background tab works correctly.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# Add modern src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from src.application.services.ui.ui_state_management_service import UIStateManagementService
from src.application.services.settings.settings_service import SettingsService
from src.presentation.components.ui.settings.modern_settings_dialog import ModernSettingsDialog


class SettingsTestWindow(QMainWindow):
    """Test window to verify settings dialog functionality."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Settings Dialog Test")
        self.setGeometry(100, 100, 400, 200)
        
        # Create services
        self.ui_state_service = UIStateManagementService()
        self.settings_service = SettingsService(self.ui_state_service)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        # Test button
        test_button = QPushButton("🎨 Open Settings Dialog")
        test_button.setFixedHeight(50)
        test_button.clicked.connect(self._open_settings)
        layout.addWidget(test_button)
        
        # Status label
        from PyQt6.QtWidgets import QLabel
        self.status_label = QLabel("Click the button to test the settings dialog")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
    
    def _open_settings(self):
        """Open the settings dialog for testing."""
        try:
            print("🧪 Opening settings dialog...")
            
            # Create and show the settings dialog
            dialog = ModernSettingsDialog(self.settings_service, self)
            
            # Connect to settings changes
            dialog.settings_changed.connect(self._on_setting_changed)
            
            # Show the dialog
            result = dialog.exec()
            
            print(f"🔧 Settings dialog closed with result: {result}")
            
            # Clean up dialog resources after it closes
            dialog.deleteLater()
            
            self.status_label.setText("Settings dialog test completed!")
            
        except Exception as e:
            print(f"❌ Failed to open settings dialog: {e}")
            import traceback
            traceback.print_exc()
            self.status_label.setText(f"Error: {e}")
    
    def _on_setting_changed(self, key: str, value):
        """Handle settings changes from the dialog."""
        print(f"🔧 Setting changed: {key} = {value}")
        self.status_label.setText(f"Setting changed: {key} = {value}")


def main():
    """Run the settings dialog test."""
    print("🧪 Starting Settings Dialog Test...")
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = SettingsTestWindow()
    window.show()
    
    print("✨ Test window opened!")
    print("🖱️ Click the button to test the settings dialog")
    print("🎨 Look for the Background tab with animated tiles")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
