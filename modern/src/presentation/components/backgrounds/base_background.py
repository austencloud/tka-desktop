from PyQt6.QtCore import QObject, pyqtSignal
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtGui import QPainter
    from PyQt6.QtWidgets import QWidget


class BaseBackground(QObject):
    update_required = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0

    @abstractmethod
    def animate_background(self):
        """Override this method to implement background animation logic"""
        self.update_required.emit()

    @abstractmethod
    def paint_background(self, widget: "QWidget", painter: "QPainter"):
        """Override this method to implement background painting logic"""
        pass
