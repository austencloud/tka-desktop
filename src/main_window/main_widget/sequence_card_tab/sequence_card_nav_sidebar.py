from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab

DEFAULT_SEQUENCE_LENGTH = 16


class SequenceCardNavSidebar(QWidget):
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab
        self.selected_length = DEFAULT_SEQUENCE_LENGTH
        self.labels: dict[int, QLabel] = {}
        self._setup_scroll_area()
        self._create_labels()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self._set_styles()

    def _setup_scroll_area(self):
        self.scroll_content = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")

    def _create_labels(self):
        for length in [4, 8, 16]:
            label = QLabel(f"{length}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            label.mousePressEvent = self.create_label_click_handler(length)
            self.layout.addWidget(label)
            self.labels[length] = label
        self._update_label_styles()

    def create_label_click_handler(self, length):
        def handler(event):
            self.selected_length = length
            self._update_label_styles()
            self.sequence_card_tab.refresher.refresh_sequence_cards()

        return handler

    def _update_label_styles(self):
        font_size = self.width() // 5

        for length, label in self.labels.items():
            if length == self.selected_length:
                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        font-weight: bold;
                        padding: 5px;
                        background-color: #333;
                        color: white;
                        border-radius: 5px;
                    }}
                    """
                )
            else:
                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        background-color: transparent;
                        padding: 5px;
                        color: #333;
                        font-weight: bold;
                    }}
                    QLabel:hover {{
                        background-color: #f0f0f0;
                    }}
                    """
                )

    def resizeEvent(self, event):
        self._set_styles()
        super().resizeEvent(event)

    def _set_styles(self):
        font_size = self.width() // 5
        for label in self.labels.values():
            label.setStyleSheet(
                f"""
                QLabel {{
                    font-size: {font_size}px;
                    padding: 5px;
                    font-weight: bold;
                }}
                QLabel:hover {{
                    background-color: #f0f0f0;
                }}
                """
            )
