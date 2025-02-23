from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QPushButton
from ..hover_button import HoverButton

if TYPE_CHECKING:
    from ..settings_dialog import SettingsDialog


class SettingsDialogActionButtons(QWidget):
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.dialog = dialog

        layout = QHBoxLayout(self)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.close_button = QPushButton("Close", self.dialog)
        layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self._hide)
        self.setLayout(layout)

    def _hide(self):
        self.dialog.hide()

    def resizeEvent(self, event):
        button_font = self.close_button.font()
        button_font.setPointSize(self.width() // 50)
        self.close_button.setFont(button_font)
