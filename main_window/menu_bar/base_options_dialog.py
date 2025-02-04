# options_dialog.py
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from typing import Callable, TYPE_CHECKING

from main_window.menu_bar.base_selector import BaseSelector

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class BaseOptionsDialog(QDialog):
    def __init__(
        self,
        selector: "BaseSelector",
        options: list[str],
        callback: Callable[[str], None],
    ):
        super().__init__(
            selector, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.selector = selector
        self.callback = callback
        self.options = options
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        for option in self.options:
            button = QPushButton(option)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _, o=option: self.select_option(o))
            button.setStyleSheet(
                """
                QPushButton {
                    padding: 5px 10px;
                }
                """
            )
            layout.addWidget(button)
        self.setLayout(layout)
        self.adjustSize()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)

    def select_option(self, option: str):
        self.callback(option)
        self.accept()

    def show_dialog(self, widget: "QWidget"):
        # Position the dialog below the widget
        self.resize_dialog()
        global_pos = widget.mapToGlobal(widget.rect().bottomLeft())
        self.move(global_pos)
        self.exec()

    def resize_dialog(self):
        font_size = self.selector.menu_bar.height() // 3
        font = self.font()
        font.setPointSize(font_size)
        for button in self.findChildren(QPushButton):
            button.setFont(font)
            button.adjustSize()
        self.setFont(font)
        self.adjustSize()
        self.update()
