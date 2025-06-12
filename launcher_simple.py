#!/usr/bin/env python3

import sys
from pathlib import Path

# Add launcher to path
launcher_dir = Path(__file__).parent
sys.path.insert(0, str(launcher_dir))

try:
    from launcher.ui.main_window import main

    sys.exit(main())
except ImportError as e:
    print(f"Import error: {e}")
    print("Falling back to simple launcher...")

    # Simple fallback launcher
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
    import subprocess

    class SimpleLauncher(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Simple Launcher")
            self.setMinimumSize(400, 300)

            layout = QVBoxLayout(self)
            layout.addWidget(QLabel("Kinetic Constructor Launcher"))

            # Essential buttons
            buttons = [
                ("🚀 V1 Main App", "v1/main.py"),
                ("⚡ V2 Demo", "v2/demo_new_architecture.py"),
                ("🎯 System Health", "unified_dev_test.py"),
            ]

            for title, script in buttons:
                btn = QPushButton(title)
                btn.clicked.connect(lambda checked, s=script: self.launch(s))
                layout.addWidget(btn)

        def launch(self, script):
            try:
                subprocess.Popen([sys.executable, script])
            except Exception as e:
                print(f"Failed to launch {script}: {e}")

    app = QApplication(sys.argv)
    window = SimpleLauncher()
    window.show()
    sys.exit(app.exec())
