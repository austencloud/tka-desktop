from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal


class QuickLaunchBar(QWidget):
    app_launch_requested = pyqtSignal(object)

    def __init__(self, primary_apps, parent=None):
        super().__init__(parent)
        self.primary_apps = primary_apps
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("Quick Launch")
        title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addStretch()

        for app in self.primary_apps:
            btn = QPushButton(f"{app.icon} {app.title}")
            btn.setToolTip(f"{app.description}\n{app.keyboard_shortcut}")
            btn.setMinimumSize(140, 36)
            btn.clicked.connect(
                lambda checked, a=app: self.app_launch_requested.emit(a)
            )
            layout.addWidget(btn)
