from typing import TYPE_CHECKING
from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    pyqtProperty,
    QObject,
)
from PyQt6.QtGui import QColor

if TYPE_CHECKING:
    from .letter_type_button import LetterTypeButton


class LetterTypeButtonAnimator(QObject):
    def __init__(self, button_widget: "LetterTypeButton"):
        super().__init__(button_widget)
        self._bg_color = QColor("white")
        self.color_anim_duration = 300
        self.button_widget = button_widget

        self.color_anim = QPropertyAnimation(self, b"backgroundColor")
        self.color_anim.setDuration(self.color_anim_duration)
        self.color_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.color_anim.setTargetObject(self)

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._bg_color

    @backgroundColor.setter
    def backgroundColor(self, value: QColor):
        self._bg_color = value
        self.button_widget.updater.update_stylesheet()

    def animate_hover(self, entering: bool, base_color: QColor):
        self.color_anim.stop()
        self.color_anim.setStartValue(self._bg_color)

        if entering:
            end_col = QColor("lightgray")
        else:
            end_col = base_color

        self.color_anim.setEndValue(end_col)
        self.color_anim.start()
