from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent
from Enums.Enums import LetterType
from utilities.letter_type_text_painter import LetterTypeTextPainter

if TYPE_CHECKING:
    from .option_picker_section_widget import OptionPickerSectionWidget


class OptionPickerSectionTypeLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section_widget = section_widget
        self.setContentsMargins(0, 0, 0, 0)
        self._paint_text(section_widget.letter_type)
        self._set_styles()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _paint_text(self, letter_type: LetterType) -> None:
        letter_type_str = letter_type.name
        styled_type_name = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )

        styled_text = f"{letter_type_str[0:4]} {letter_type_str[4]}: {styled_type_name}"
        self.setText(styled_text)

    def _set_styles(self):
        font = QFont()
        font.setBold(True)
        self.setFont(font)

        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 200);
                font-weight: bold;
                border: none;
                border-radius: {self.height() // 2}px;
                padding: 5px;
            }}
            QLabel:hover {{
                border: 2px solid black;
            }}
            """
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def resizeEvent(self, event) -> None:
        # Set alignment to center
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Calculate font size based on parent widget's height
        parent_height = (
            self.section_widget.option_scroll.construct_tab.option_picker.construct_tab.main_widget.height()
        )
        font_size = max(parent_height // 70, 10)  # Ensure minimum font size
        label_height = max(int(font_size * 3), 20)  # Ensure minimum label height
        label_width = max(int(label_height * 6), 100)  # Ensure minimum label width

        self.setFixedSize(QSize(label_width, label_height))

        # Update font size
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

        # Update border radius based on new height
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 200);
                font-weight: bold;
                border: none;
                border-radius: {label_height // 2}px;
                padding: 5px;
            }}
            QLabel:hover {{
                border: 2px solid black;
            }}
            """
        )
        super().resizeEvent(event)
