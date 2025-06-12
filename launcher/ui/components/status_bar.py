from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont


class StatusBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)

        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.health_indicator = QLabel("🟢 System Healthy")
        self.health_indicator.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.health_indicator)

    def update_status(self, message):
        self.status_label.setText(message)

    def update_health(self, is_healthy):
        status = "🟢 System Healthy" if is_healthy else "🔴 Issues Detected"
        self.health_indicator.setText(status)
