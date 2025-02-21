from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent
from Enums.Enums import LetterType
from utilities.letter_type_text_painter import LetterTypeTextPainter

if TYPE_CHECKING:
    from .option_picker_section_widget import OptionPickerSectionWidget


class OptionPickerSectionTypeButton(QPushButton):
    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSectionWidget"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self._bg_color = "rgba(255, 255, 255, 200)"
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self._paint_text(section_widget.letter_type)
        self._set_initial_styles()

    def _paint_text(self, letter_type: LetterType) -> None:
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: LetterType) -> str:
        letter_type_str = letter_type.name
        styled_type_name = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )
        return f"{letter_type_str[0:4]} {letter_type_str[4]}: {styled_type_name}"

    def _set_initial_styles(self) -> None:
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self._update_style()

    def _update_style(self, bg_color: str = None) -> None:
        bg_color = bg_color or self._bg_color
        style = (
            f"QPushButton {{"
            f"  background-color: {bg_color};"
            f"  font-weight: bold;"
            f"  border: none;"
            f"  border-radius: {self.height() // 2}px;"
            f"  padding: 5px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  border: 2px solid black;"
            f"}}"
        )
        self.setStyleSheet(style)

    def enterEvent(self, event) -> None:
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(bg_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(bg_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._update_style()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        parent_height = self.section_widget.mw_size_provider().height()
        font_size = max(parent_height // 70, 10)
        label_height = max(int(font_size * 3), 20)
        label_width = max(int(label_height * 6), 100)
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)
        self.setFixedSize(QSize(label_width, label_height))
        self._update_style()
