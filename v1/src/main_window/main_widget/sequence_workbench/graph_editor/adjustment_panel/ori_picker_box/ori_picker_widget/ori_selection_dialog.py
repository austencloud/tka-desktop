from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import BLUE, HEX_BLUE, HEX_RED
from .ori_button import OriButton  # Import the new OriButton class
from ..color_utils import ColorUtils

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OriSelectionDialog(QDialog):
    buttons: dict[str, OriButton] = {}

    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(
            ori_picker_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.ori_picker_widget = ori_picker_widget
        self.selected_orientation = None
        self._set_dialog_style()
        self._setup_buttons()
        self._setup_layout()

    def _set_dialog_style(self):
        border_color = HEX_BLUE if self.ori_picker_widget.color == BLUE else HEX_RED
        background_color = ColorUtils.lighten_color(border_color)
        self.setStyleSheet(
            f"background-color: {background_color}; border: 2px solid {border_color};"
        )

    def _setup_buttons(self):
        for orientation in self.ori_picker_widget.orientations:
            button = OriButton(orientation, self)  # Use OriButton
            button.clicked.connect(
                lambda _, ori=orientation: self.select_orientation(ori)
            )
            self.buttons[orientation] = button

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        for button in self.buttons.values():
            layout.addWidget(button)
        self.adjustSize()

    def select_orientation(self, orientation):
        self.selected_orientation = orientation
        self.accept()
