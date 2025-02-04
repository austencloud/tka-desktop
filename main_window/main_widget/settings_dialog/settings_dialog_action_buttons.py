from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy, QWidget
from .hover_button import HoverButton

if TYPE_CHECKING:
    from .settings_dialog import SettingsDialog


class SettingsDialogActionButtons(QWidget):
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )

        self.save_button = HoverButton("Save", self.dialog)
        self.close_button = HoverButton("Close", self.dialog)

        layout.addWidget(self.save_button)
        layout.addWidget(self.close_button)

        self.save_button.clicked.connect(self._hide)
        self.close_button.clicked.connect(self._hide)

    def _hide(self):
        self.dialog.hide()

    def resizeEvent(self, event):
        for button in [self.save_button, self.close_button]:
            button_font = button.font()
            button_font.setPointSize(self.dialog.calculate_font_size())
            button.setFont(button_font)
