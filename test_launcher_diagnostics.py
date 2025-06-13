#!/usr/bin/env python3
"""
Launcher Diagnostic Test - Multiple Monitor Detection

This test will:
1. Check which launcher files exist and are being executed
2. Test dual monitor detection logic
3. Verify the positioning code is actually running
4. Show current screen configuration
"""

import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QGuiApplication


class DiagnosticWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher Diagnostic Test")
        self.setup_ui()
        self.test_monitor_detection()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setSpacing(10)

        title = QLabel("🔍 Launcher Diagnostic Results")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title)

    def add_result(self, text, color="white"):
        label = QLabel(text)
        label.setStyleSheet(
            f"color: {color}; background: rgba(0,0,0,0.1); padding: 8px; border-radius: 4px;"
        )
        label.setWordWrap(True)
        self.main_layout.addWidget(label)

    def test_monitor_detection(self):
        app = QApplication.instance()
        if app is None:
            self.add_result("❌ No QApplication instance found", "red")
            return
        screens = QGuiApplication.screens()

        self.add_result(f"📺 Total Screens Detected: {len(screens)}", "lightgreen")

        for i, screen in enumerate(screens):
            geo = screen.geometry()
            available = screen.availableGeometry()
            is_primary = screen == QGuiApplication.primaryScreen()

            self.add_result(
                f"Screen {i}: {'[PRIMARY]' if is_primary else '[SECONDARY]'}\n"
                f"  Resolution: {geo.width()}x{geo.height()}\n"
                f"  Position: ({geo.x()}, {geo.y()})\n"
                f"  Available: {available.width()}x{available.height()}",
                "cyan" if is_primary else "yellow",
            )

        # Test V1 logic
        frozen_state = getattr(sys, "frozen", False)
        self.add_result(f"🔒 Frozen State: {frozen_state}", "orange")

        if frozen_state:
            selected_screen = screens[0] if screens else None
            reason = "Using primary screen (frozen/compiled mode)"
        else:
            selected_screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
            reason = f"Using {'secondary' if len(screens) > 1 else 'primary'} screen (development mode)"

        self.add_result(f"🎯 V1 Logic Result: {reason}", "lightblue")

        # Test positioning calculation
        if selected_screen is None:
            self.add_result("❌ No screen available for positioning", "red")
            return
        
        available_geometry = selected_screen.availableGeometry()
        window_width = int(available_geometry.width() * 0.9)
        window_height = int(available_geometry.height() * 0.9)
        x = available_geometry.x() + int(
            (available_geometry.width() - window_width) / 2
        )
        y = available_geometry.y() + int(
            (available_geometry.height() - window_height) / 2
        )

        self.add_result(
            f"📐 Calculated Position:\n"
            f"  Size: {window_width}x{window_height}\n"
            f"  Position: ({x}, {y})",
            "lightgreen",
        )

        # Apply the positioning to this test window
        self.setGeometry(x, y, min(800, window_width), min(600, window_height))


def test_launcher_files():
    """Test which launcher files exist and their entry points"""
    launcher_files = [
        "main.py",
        "launcher/ui/main_window.py",
        "debug_launcher.py",
        "v1/src/standalone/core/launcher.py",
    ]

    print("🔍 LAUNCHER FILE ANALYSIS")
    print("=" * 50)

    for file_path in launcher_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ Found: {file_path}")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "move_to_secondary_monitor" in content:
                        print(f"   📱 Has dual monitor code")
                    if "def main()" in content:
                        print(f"   🚀 Has main() function")
                    if '__name__ == "__main__"' in content:
                        print(f"   ⚡ Is executable")
            except Exception as e:
                print(f"   ❌ Error reading: {e}")
        else:
            print(f"❌ Missing: {file_path}")
    print()


def test_main_py_execution():
    """Test what main.py actually executes"""
    print("🚀 TESTING MAIN.PY EXECUTION")
    print("=" * 50)

    try:
        with open("main.py", "r") as f:
            content = f.read()
            print("Main.py content preview:")
            lines = content.split("\n")[:20]
            for i, line in enumerate(lines, 1):
                print(f"{i:2}: {line}")

            if "launcher" in content.lower():
                print("✅ main.py references launcher")
            else:
                print("❌ main.py does NOT reference launcher")

    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
    print()


def main():
    print("🔍 COMPREHENSIVE LAUNCHER DIAGNOSTIC")
    print("=" * 60)

    # Test 1: File analysis
    test_launcher_files()

    # Test 2: Main.py analysis
    test_main_py_execution()

    # Test 3: Visual monitor test
    app = QApplication(sys.argv)

    window = DiagnosticWindow()
    window.show()

    print("📺 Visual diagnostic window opened - check which monitor it appears on!")
    print("🎯 If it opens on your second monitor, the positioning logic works")
    print("❌ If it opens on your primary monitor, there's an issue")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
