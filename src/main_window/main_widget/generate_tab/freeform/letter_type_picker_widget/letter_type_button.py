from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QMouseEvent
from math import sqrt

from enums.letter.letter_type import LetterType
from .styled_border_overlay_for_button import StyledBorderOverlayForButton


class LetterTypeButton(QWidget):
    """
    A circular, animated button for selecting letter types.
    - Supports hover and press animations.
    - Toggles selection state on click.
    - Uses a two-tone border.
    """

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

        # Scaling Animation
        self._scale = 1.0
        self.press_scale = 0.9
        self.anim_duration = 150

        # UI Elements
        self.label = QLabel(str(self.index), self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.overlay = StyledBorderOverlayForButton(self)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

        # Animations
        self._setup_animations()
        self.update_colors()
        self.setFixedSize(60, 60)

    # -----------------------------------------------------------------
    # Animations
    # -----------------------------------------------------------------
    def _setup_animations(self):
        """Creates property animations for hover effect and click effect."""
        self.anim_group = QPropertyAnimation(self, b"backgroundColor")
        self.anim_group.setDuration(self.anim_duration)
        self.anim_group.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.scale_anim = QPropertyAnimation(self, b"clickScale")
        self.scale_anim.setDuration(self.anim_duration)
        self.scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    @pyqtProperty(float)
    def clickScale(self):
        return self._scale

    @clickScale.setter
    def clickScale(self, value):
        self._scale = value
        self.update()  # Triggers paintEvent

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._bg_color

    @backgroundColor.setter
    def backgroundColor(self, value: QColor):
        self._bg_color = value
        self._update_stylesheet()

    def _animate_hover(self, entering: bool):
        """Fades button color on hover."""
        self.anim_group.stop()
        self.anim_group.setStartValue(self._bg_color)

        if entering:
            end_col = self._lighten_color(self._base_color, self._hover_lighten_factor)
        else:
            end_col = self._base_color

        self.anim_group.setEndValue(end_col)
        self.anim_group.start()

    def _animate_press(self):
        """Shrinks button slightly when clicked."""
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(self.press_scale)
        self.scale_anim.start()

    def _animate_release(self):
        """Restores button size after release."""
        self.scale_anim.stop()
        self.scale_anim.setStartValue(self._scale)
        self.scale_anim.setEndValue(1.0)
        self.scale_anim.start()

    # -----------------------------------------------------------------
    # Event Handling
    # -----------------------------------------------------------------
    def enterEvent(self, event):
        """Handles hover-in event."""
        self._hovered = True
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        self._animate_hover(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handles hover-out event."""
        self._hovered = False
        QApplication.restoreOverrideCursor()
        self._animate_hover(False)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Handles button click."""
        if event.button() == Qt.MouseButton.LeftButton:
            if not self._click_inside_circle(event.pos()):
                return

            self.is_selected = not self.is_selected
            self.update_colors()
            self.clicked.emit(self.letter_type, self.is_selected)
            self._animate_press()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handles button release."""
        if event.button() == Qt.MouseButton.LeftButton:
            if not self._click_inside_circle(event.pos()):
                return
            self._animate_release()

        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        """Adjusts layout when resized."""
        super().resizeEvent(event)
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setFixedSize(self.size())

    def paintEvent(self, event):
        """Handles drawing with scaling."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)

        super().paintEvent(event)

    # -----------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------
    def update_colors(self):
        """Updates button colors based on selection state."""
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
        """Applies styles dynamically."""
        self.setStyleSheet(
            f"""
            background-color: {self._bg_color.name()};
            border-radius: 50%;
        """
        )

    def _get_border_colors(self, letter_type: LetterType):
        """Returns primary and secondary colors for letter types."""
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
        """Returns a color lightened by a given factor (>1.0 => lighter)."""
        h = color.hslHue()
        s = color.hslSaturation()
        l = color.lightness()
        new_lightness = min(255, int(l * factor))
        return QColor.fromHsl(h, s, new_lightness, alpha=color.alpha())

    def _dim_color(self, hex_color: str) -> str:
        """Converts a color to a dimmed version."""
        c = QColor(hex_color)
        gray_val = (c.red() + c.green() + c.blue()) // 3
        return QColor(gray_val, gray_val, gray_val).name()

    def _click_inside_circle(self, pos):
        """Checks if the click was inside the circular region."""
        center = self.rect().center()
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        return sqrt(dx * dx + dy * dy) <= (self.width() / 2)
