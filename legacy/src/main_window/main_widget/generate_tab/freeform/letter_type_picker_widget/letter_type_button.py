from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QMouseEvent
from math import sqrt

from enums.letter.letter_type import LetterType
from .styled_border_overlay_for_button import StyledBorderOverlayForButton


class LetterTypeButton(QWidget):
    clicked = pyqtSignal(LetterType, bool)

    def __init__(self, parent, letter_type: LetterType, index: int):
        super().__init__(parent)
        self.letter_type = letter_type
        self.index = index
        self.is_selected = True
        self._hovered = False

        # Colors
        self.primary_color, self.secondary_color = self._get_border_colors(letter_type)
        self._base_color = QColor("white")
        self._bg_color = QColor("white")  # Used for animations
        self._hover_lighten_factor = 1.15  # 15% lighter on hover

        # UI Elements
        self.label = QLabel(str(self.index), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.overlay = StyledBorderOverlayForButton(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        self.update_colors()
        self.setFixedSize(60, 60)

    def enterEvent(self, event):
        self._hovered = True
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        self._bg_color = self._lighten_color(self._base_color, self._hover_lighten_factor)
        self._update_stylesheet()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        QApplication.restoreOverrideCursor()
        self._bg_color = self._base_color
        self._update_stylesheet()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if not self._click_inside_circle(event.pos()):
                return

            self.is_selected = not self.is_selected
            self.update_colors()
            self.clicked.emit(self.letter_type, self.is_selected)

        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setFixedSize(self.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        super().paintEvent(event)

    def update_colors(self):
        if self.is_selected:
            self._base_color = QColor("white")
            self.label.setStyleSheet("color: black;")
        else:
            dim_color = self._dim_color("#ffffff")
            self._base_color = QColor(dim_color)
            self.label.setStyleSheet("color: lightgray;")

        primary = self.primary_color
        secondary = self.secondary_color
        if not self.is_selected:
            primary = self._dim_color(primary)
            secondary = self._dim_color(secondary)

        self.overlay.update_border_colors(primary, secondary)

        if not self._hovered:
            self._bg_color = self._base_color

        self._update_stylesheet()

    def _update_stylesheet(self):
        self.setStyleSheet(
            f"""
            background-color: {self._bg_color.name()};
            border-radius: 50%;
        """
        )

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

    def _lighten_color(self, color: QColor, factor: float) -> QColor:
        h = color.hslHue()
        s = color.hslSaturation()
        l = color.lightness()
        new_lightness = min(255, int(l * factor))
        return QColor.fromHsl(h, s, new_lightness, alpha=color.alpha())

    def _dim_color(self, hex_color: str) -> str:
        c = QColor(hex_color)
        gray_val = (c.red() + c.green() + c.blue()) // 3
        return QColor(gray_val, gray_val, gray_val).name()

    def _click_inside_circle(self, pos):
        center = self.rect().center()
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        return sqrt(dx * dx + dy * dy) <= (self.width() / 2)
