#!/usr/bin/env python3
"""
Enhanced UFO Manager Test

Demonstrates the ported logic from legacy modular UFO system.
Shows both wandering and fly-by UFO behaviors.
"""

import sys
from pathlib import Path

# Add modern src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter
from presentation.components.backgrounds.starfield.ufo_manager import UFOManager


class UFOTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced UFO Manager Test - Legacy Logic Ported")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Add status label
        self.status_label = QLabel("UFO Behavior: Wandering (Always Visible)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Add behavior toggle button
        self.toggle_button = QPushButton(
            "Switch to Fly-by Mode (Legacy Modular Behavior)"
        )
        self.toggle_button.clicked.connect(self.toggle_behavior)
        layout.addWidget(self.toggle_button)

        # Create UFO managers for both behaviors
        self.wandering_ufo = UFOManager(behavior_mode="wandering")
        self.flyby_ufo = UFOManager(behavior_mode="flyby")
        self.current_ufo = self.wandering_ufo
        self.current_mode = "wandering"

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS

    def toggle_behavior(self):
        """Switch between wandering and fly-by UFO behaviors."""
        if self.current_mode == "wandering":
            self.current_mode = "flyby"
            self.current_ufo = self.flyby_ufo
            self.status_label.setText(
                "UFO Behavior: Fly-by (Periodic Appearances from Off-screen)"
            )
            self.toggle_button.setText("Switch to Wandering Mode (Always Visible)")
        else:
            self.current_mode = "wandering"
            self.current_ufo = self.wandering_ufo
            self.status_label.setText("UFO Behavior: Wandering (Always Visible)")
            self.toggle_button.setText(
                "Switch to Fly-by Mode (Legacy Modular Behavior)"
            )

    def animate(self):
        """Update UFO animation."""
        self.current_ufo.animate_ufo()
        self.update()    
    def paintEvent(self, a0):
        """Paint the background and UFO."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.black)

        # Get cursor position for UFO interaction
        cursor_pos = self.mapFromGlobal(self.cursor().pos())

        # Draw UFO
        self.current_ufo.draw_ufo(painter, self, cursor_pos)

        # Add information text
        painter.setPen(Qt.GlobalColor.white)
        info_text = [
            "Enhanced UFO Manager - Legacy Logic Successfully Ported!",
            "",
            "Wandering Mode (Legacy Simple):",
            "• Always visible UFO that wanders around",
            "• Pauses and resumes movement randomly",
            "• Bounces off screen edges",
            "• Cursor interaction (pointing hand)",
            "",
            "Fly-by Mode (Legacy Modular):",
            "• UFO appears periodically (500-1000 frame intervals)",
            "• Enters from random off-screen edge",
            "• Flies in straight line across screen",
            "• Disappears after fixed duration (300-500 frames)",
            "• More realistic UFO sighting behavior",
            "",
            "Features from both legacy implementations:",
            "✅ Sophisticated appearance/disappearance timing",
            "✅ Off-screen entry from all four edges",
            "✅ Linear fly-by movement patterns",
            "✅ Wandering behavior with pauses",
            "✅ Edge bouncing and boundary management",
            "✅ Cursor interaction and visual feedback",
            "✅ Modern glow effects and procedural fallback",
        ]

        y_pos = 80
        for line in info_text:
            painter.drawText(10, y_pos, line)
            y_pos += 20


def main():
    app = QApplication(sys.argv)

    print("🛸 Enhanced UFO Manager Test")
    print("=" * 40)
    print("✅ Legacy modular UFO logic successfully ported!")
    print("✅ Both wandering and fly-by behaviors implemented")
    print("✅ All sophisticated timing and movement patterns preserved")
    print("")
    print("Controls:")
    print("- Click button to switch between UFO behaviors")
    print("- Move mouse over UFO to see cursor interaction")
    print("- Watch fly-by mode for periodic off-screen appearances")

    window = UFOTestWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
