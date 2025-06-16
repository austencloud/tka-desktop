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
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.setup_ui(sequence_card_tab)

    def setup_ui(self, sequence_card_tab: "SequenceCardTab"):
        self.setGeometry(sequence_card_tab.content_area.scroll_area.geometry())
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
