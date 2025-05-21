from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QSizePolicy,
    QFrame,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QFont
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.sequence_card_tab import (
        SequenceCardTab,
    )

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
        # Add a header label with improved styling
        header_label = QLabel("Sequence Length")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_font = QFont()
        header_font.setBold(True)
        header_font.setPointSize(10)
        header_label.setFont(header_font)
        header_label.setStyleSheet(
            """
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #444444, stop:1 #333333);
            padding: 12px 8px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid #555555;
        """
        )
        self.layout.addWidget(header_label)

        # Add length option labels
        for length in [4, 8, 16]:
            # Create a frame for each label for better styling
            label_frame = QFrame()
            label_frame.setObjectName(f"lengthFrame_{length}")
            label_frame.setStyleSheet(
                """
                border-radius: 4px;
                margin: 2px 0;
            """
            )

            label_layout = QHBoxLayout(label_frame)
            label_layout.setContentsMargins(5, 5, 5, 5)

            label = QLabel(f"{length}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            label.mousePressEvent = self.create_label_click_handler(length)

            label_layout.addWidget(label)
            self.layout.addWidget(label_frame)
            self.labels[length] = label

        # Add spacer at the bottom
        self.layout.addStretch()

        # Initialize styles
        self._update_label_styles()

    def create_label_click_handler(self, length):
        def handler(_):  # Use underscore to indicate unused parameter
            self.selected_length = length
            self._update_label_styles()
            self.sequence_card_tab.refresher.refresh_sequence_cards()

        return handler

    def _update_label_styles(self):
        """Update the styles of the sidebar labels based on selection state."""
        font_size = max(14, self.width() // 6)  # Ensure minimum font size

        for length, label in self.labels.items():
            # Get the parent frame
            frame = label.parent().parent()

            if length == self.selected_length:
                # Selected label style with modern gradient and shadow effect
                frame.setStyleSheet(
                    f"""
                    #lengthFrame_{length} {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #3a92ea, stop:1 #2a82da);
                        border-radius: 8px;
                        border: none;
                        margin: 4px;
                    }}
                """
                )

                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        font-weight: bold;
                        color: white;
                        padding: 8px;
                    }}
                """
                )
            else:
                # Unselected label style with hover and active states
                frame.setStyleSheet(
                    f"""
                    #lengthFrame_{length} {{
                        background-color: rgba(60, 60, 60, 0.3);
                        border-radius: 8px;
                        border: none;
                        margin: 4px;
                    }}
                    #lengthFrame_{length}:hover {{
                        background-color: rgba(80, 80, 80, 0.5);
                    }}
                """
                )

                label.setStyleSheet(
                    f"""
                    QLabel {{
                        font-size: {font_size}px;
                        color: #dddddd;
                        font-weight: bold;
                        padding: 8px;
                    }}
                    QLabel:hover {{
                        color: white;
                    }}
                """
                )

    def resizeEvent(self, event):
        self._set_styles()
        super().resizeEvent(event)

    def _set_styles(self):
        # Just call update_label_styles which now handles all styling
        self._update_label_styles()
