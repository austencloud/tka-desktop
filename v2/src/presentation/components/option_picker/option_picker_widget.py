from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QResizeEvent


class ModernOptionPickerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._resize_callback = None

    def set_resize_callback(self, callback):
        self._resize_callback = callback

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        if self._resize_callback:
            self._resize_callback()
