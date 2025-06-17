#!/usr/bin/env python3
"""
Demo script to show the animated background tiles in action.
Run this to see the new animated preview functionality.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from unittest.mock import Mock

# Add modern src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from src.application.services.settings.background_service import BackgroundService
from src.presentation.components.ui.settings.tabs.background_tab import BackgroundTab


class BackgroundDemoWindow(QMainWindow):
    """Demo window to showcase animated background tiles."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎨 Animated Background Tiles Demo")
        self.setGeometry(100, 100, 900, 700)

        # Create mock UI state service
        self.ui_state_service = Mock()
        self.ui_state_service.get_setting.return_value = "Aurora"

        # Create background service
        self.background_service = BackgroundService(self.ui_state_service)

        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Set up the demo UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Title
        title = QLabel("🎨 Animated Background Tiles Demo")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(title)

        # Description
        description = QLabel(
            "This demo shows the new animated background preview tiles.\n"
            "Each tile shows a live animated preview of the background.\n"
            "Click on any tile to select that background!"
        )
        description.setFont(QFont("Arial", 12))
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("color: #ccc; margin-bottom: 20px;")
        layout.addWidget(description)

        # Background tab
        self.background_tab = BackgroundTab(self.background_service)
        self.background_tab.background_changed.connect(self._on_background_changed)
        layout.addWidget(self.background_tab)

        # Status label
        self.status_label = QLabel("Current selection: Aurora")
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #0078d4; margin-top: 20px;")
        layout.addWidget(self.status_label)

    def _on_background_changed(self, setting_name: str, background_type: str):
        """Handle background selection change."""
        self.status_label.setText(f"Current selection: {background_type}")
        print(f"🎨 Background changed to: {background_type}")

    def closeEvent(self, event):
        """Handle window close event to clean up resources."""
        if hasattr(self, "background_tab") and self.background_tab:
            self.background_tab.cleanup()
        super().closeEvent(event)

    def _apply_styling(self):
        """Apply dark theme styling."""
        self.setStyleSheet(
            """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 1.0),
                    stop:1 rgba(15, 23, 42, 1.0));
            }
            QWidget {
                background: transparent;
            }
        """
        )


def main():
    """Run the animated background tiles demo."""
    print("🎨 Starting Animated Background Tiles Demo...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create and show demo window
    window = BackgroundDemoWindow()
    window.show()

    print("✨ Demo window opened! You should see:")
    print("   🌌 Aurora - Flowing colors with sparkles")
    print("   ⭐ Starfield - Twinkling stars")
    print("   ❄️ Snowfall - Falling snowflakes")
    print("   🫧 Bubbles - Floating bubbles")
    print("\n🖱️ Click on any tile to select that background!")
    print("🔄 Each tile shows a live animated preview")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
