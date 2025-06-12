from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal


class AppCard(QFrame):
    launch_requested = pyqtSignal(object)

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.Box)
        self.setMinimumSize(200, 120)
        self.setMaximumSize(250, 140)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        header_layout = QHBoxLayout()
        icon_label = QLabel(self.app.icon)
        icon_label.setFont(QFont("Segoe UI", 20))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setMinimumSize(32, 32)

        title_label = QLabel(self.app.title)
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_label.setWordWrap(True)

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label, 1)
        layout.addLayout(header_layout)

        desc_label = QLabel(self.app.description)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666;")
        layout.addWidget(desc_label, 1)

        launch_btn = QPushButton("Launch")
        launch_btn.clicked.connect(lambda: self.launch_requested.emit(self.app))
        layout.addWidget(launch_btn)

        if self.app.keyboard_shortcut:
            shortcut_label = QLabel(self.app.keyboard_shortcut)
            shortcut_label.setFont(QFont("Consolas", 8))
            shortcut_label.setStyleSheet(
                "color: #888; background: #f0f0f0; padding: 2px 6px; border-radius: 3px;"
            )
            shortcut_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(shortcut_label)
