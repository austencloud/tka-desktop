from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSize, Qt, pyqtSignal

if TYPE_CHECKING:
    pass


class SettingsButton(QPushButton):
    settings_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("⚙️", parent)
        self.setToolTip("Settings")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedSize(QSize(40, 40))

        self.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.2),
                    stop:1 rgba(255, 255, 255, 0.1));
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3),
                    stop:1 rgba(255, 255, 255, 0.2));
                border: 2px solid rgba(255, 255, 255, 0.5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.1),
                    stop:1 rgba(255, 255, 255, 0.05));
            }
        """
        )

        self.clicked.connect(self.settings_requested.emit)
