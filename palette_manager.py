import sys
from typing import TYPE_CHECKING
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_window import MainWindow

class PaletteManager:
    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window
        self.app = QApplication(sys.argv)
        self.palette = QPalette()
        self._set_colors()
        self.app.setPalette(self.palette)

    def _set_colors(self):
        self.palette.setColor(QPalette.ColorRole.Window, QColor(225, 225, 225))
        self.palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Base, QColor(240, 240, 240))
        self.palette.setColor(QPalette.ColorRole.AlternateBase, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        self.palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        self.palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        self.palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 163, 224))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
