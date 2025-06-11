from PyQt6.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING


class BaseBackground(QObject):
    update_required = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0

    def animate_background(self):
        self.update_required.emit()

    def paint_background(self, widget, painter):
        pass
