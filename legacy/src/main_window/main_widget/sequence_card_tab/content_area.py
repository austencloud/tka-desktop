# src/main_window/main_widget/sequence_card_tab/tab.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt




from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab





class SequenceCardContentArea(QWidget):
    def __init__(self, parent: "SequenceCardTab"):
        super().__init__(parent)
        self.parent = parent
        self._setup_ui()

    def _setup_ui(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(2, 10, 2, 10)

        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }
        """
        )

    def clear_layout(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                while item.layout().count():
                    subitem = item.layout().takeAt(0)
                    if subitem.widget():
                        subitem.widget().setParent(None)

    def show_instruction_label(self):
        instruction_label = QLabel(
            "Select a sequence length from the sidebar to view cards"
        )
        instruction_label.setObjectName("instructionLabel")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet(
            """
            QLabel#instructionLabel {
                color: #bdc3c7;
                font-size: 16px;
                padding: 20px;
                background-color: rgba(44, 62, 80, 0.7);
                border-radius: 10px;
                margin: 40px;
            }
        """
        )
        self.clear_layout()
        self.scroll_layout.addWidget(instruction_label, 0, Qt.AlignmentFlag.AlignCenter)
