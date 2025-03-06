from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .CAP_type_button import PermutationTypeButton

PERMUTATION_TYPES = {
    "strict_mirrored": "Strict Mirrored",
    "strict_rotated": "Strict Rotated",
    "strict_swapped": "Strict Swapped",
    "mirrored_swapped": "Mirrored / Swapped",
}
if TYPE_CHECKING:
    from ...generate_tab import GenerateTab


class PermutationTypePicker(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.buttons: dict[str, PermutationTypeButton] = {}
        self._create_layout()
        self._connect_signals()

    def _create_layout(self):
        # Main vertical layout
        self.layout: QVBoxLayout = QVBoxLayout()

        # Create label in its own centered HBox
        label_layout = QHBoxLayout()
        self.label = QLabel("Type:")
        label_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(label_layout)

        # Create grid for buttons
        self.grid_layout = QGridLayout()

        buttons = [
            ("strict_rotated", 0, 0),
            ("strict_mirrored", 0, 1),
            ("strict_swapped", 1, 0),
            ("mirrored_swapped", 1, 1),
        ]

        for perm_type, row, col in buttons:
            btn = PermutationTypeButton(PERMUTATION_TYPES[perm_type], perm_type, self)
            self.buttons[perm_type] = btn
            self.grid_layout.addWidget(btn, row, col)

        # Center the grid in the layout
        grid_container = QHBoxLayout()
        grid_container.addStretch()
        grid_container.addLayout(self.grid_layout)
        grid_container.addStretch()

        self.layout.addLayout(grid_container)
        self.setLayout(self.layout)

    def _connect_signals(self):
        for btn in self.buttons.values():
            btn.toggled.connect(
                lambda checked, b=btn: self._handle_button_toggle(b, checked)
            )

    def _handle_button_toggle(self, button: PermutationTypeButton, checked: bool):
        if checked:
            for other_btn in self.buttons.values():
                if other_btn != button:
                    other_btn.set_active(False)

            self.generate_tab.settings.set_setting("CAP_type", button.perm_type)
            self.generate_tab.controller._update_ui_visibility()

    def set_active_type(self, perm_type: str):
        if perm_type in self.buttons:
            self.buttons[perm_type].set_active(True)

    def resizeEvent(self, event):
        font = self.label.font()
        font.setPointSize(self.generate_tab.height() // 40)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white")
        spacing = self.generate_tab.height() // 80
        self.grid_layout.setSpacing(spacing)
        self.layout.setSpacing(spacing)
        super().resizeEvent(event)
