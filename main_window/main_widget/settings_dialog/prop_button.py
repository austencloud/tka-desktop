from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QSize

from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.prop_type_tab import PropTypeTab


class PropButton(QPushButton):

    def __init__(
        self, prop: str, icon_path: str, prop_type_tab: "PropTypeTab", callback
    ):
        super().__init__(prop_type_tab)
        self.prop_type_tab = prop_type_tab
        self.setIcon(QIcon(icon_path))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(prop)
        self.clicked.connect(lambda: callback(PropType.get_prop_type(prop)))

        # Set the initial stylesheet
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """
        )

        self._hover_color = QColor("#f0f0f0")
        self._press_color = QColor("#f0f0f0")

        # Create animations for hover and press effects
        self.hover_animation = QPropertyAnimation(self, b"hover_color")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.press_animation = QPropertyAnimation(self, b"press_color")
        self.press_animation.setDuration(100)
        self.press_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def enterEvent(self, event):
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self._hover_color)
        self.hover_animation.setEndValue(QColor("#e0e0e0"))
        self.hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hover_animation.stop()
        self.hover_animation.setStartValue(self._hover_color)
        self.hover_animation.setEndValue(QColor("#f0f0f0"))
        self.hover_animation.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.press_animation.stop()
        self.press_animation.setStartValue(self._press_color)
        self.press_animation.setEndValue(QColor("#d0d0d0"))
        self.press_animation.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.press_animation.stop()
        self.press_animation.setStartValue(self._press_color)
        self.press_animation.setEndValue(QColor("#e0e0e0"))
        self.press_animation.start()
        super().mouseReleaseEvent(event)

    def get_hover_color(self):
        return self._hover_color

    def set_hover_color(self, color):
        self._hover_color = color
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }}
        """
        )

    hover_color = pyqtProperty(QColor, get_hover_color, set_hover_color)

    def get_press_color(self):
        return self._press_color

    def set_press_color(self, color):
        self._press_color = color
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {color.name()};
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }}
        """
        )

    press_color = pyqtProperty(QColor, get_press_color, set_press_color)

    def resizeEvent(self, event):
        size = self.prop_type_tab.width() // 4
        icon_size = int(size * 0.75)
        self.setFixedSize(QSize(size, size))
        self.setIconSize(QSize(icon_size, icon_size))
