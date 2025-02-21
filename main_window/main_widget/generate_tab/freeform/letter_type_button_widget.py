from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QMouseEvent

from Enums.letters import LetterType
from main_window.main_widget.generate_tab.freeform.styled_border_overlay_for_button import StyledBorderOverlayForButton


if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.freeform.letter_type_picker_widget import (
        LetterTypePickerWidget,
    )


class LetterTypeButtonWidget(QWidget):
    clicked = pyqtSignal(LetterType, bool)

    def __init__(
        self,
        letter_type_picker: "LetterTypePickerWidget",
        letter_type: LetterType,
        index: int,
    ):
        super().__init__()
        self.letter_type = letter_type
        self.letter_type_picker = letter_type_picker
        self.index = index
        self.is_selected = True
        self.primary_color, self.secondary_color = self._get_border_colors(letter_type)

        self.label = QLabel(str(self.index), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setMouseTracking(True)

        self.overlay = StyledBorderOverlayForButton(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.update_colors()
        self.setFixedSize(60, 60)

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()

    def _get_border_colors(self, letter_type: LetterType):
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),
            LetterType.Type3: ("#26e600", "#6F2DA8"),
            LetterType.Type4: ("#26e600", "#26e600"),
            LetterType.Type5: ("#00b3ff", "#26e600"),
            LetterType.Type6: ("#eb7d00", "#eb7d00"),
        }
        return border_colors_map.get(letter_type, ("black", "black"))

    def mousePressEvent(self, event: "QMouseEvent"):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_selected = not self.is_selected
            self.update_colors()
            self.clicked.emit(self.letter_type, self.is_selected)
        super().mousePressEvent(event)

    def update_colors(self):
        p = self.primary_color
        s = self.secondary_color
        if not self.is_selected:
            p = self._dim_color(p)
            s = self._dim_color(s)
            self.label.setStyleSheet("color: lightgray;")

        else:
            self.label.setStyleSheet("color: black;")
        self.overlay.update_border_colors(p, s)
        self.setStyleSheet("background-color: white; color: black;")

    def _dim_color(self, hex_color: str) -> str:
        c = QColor(hex_color)
        gray_val = (c.red() + c.green() + c.blue()) // 3
        return QColor(gray_val, gray_val, gray_val).name()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setFixedSize(self.size())
        # font = self.label.font()
        # self.label.setFont(font)
