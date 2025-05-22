# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QLabel,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab


class TransitionOverlay(QLabel):
    def __init__(self, parent_widget: "SequenceCardTab"):
        super().__init__(parent_widget)
        self.setup_ui(parent_widget)

    def setup_ui(self, parent_widget: "SequenceCardTab"):
        self.setGeometry(parent_widget.scroll_area.geometry())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("Updating layout...")
        self.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
        """
        )

    def show_with_timer(self, duration: int = 300):
        self.show()
        QApplication.processEvents()
        QTimer.singleShot(duration, self.deleteLater)
