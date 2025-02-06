from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.prop_button import PropButton
from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class PropTypeTab(QWidget):
    buttons: list[PropButton] = []

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self._setup_ui()

    def _setup_ui(self):
        # Main layout
        card = CardFrame(self)
        main_layout = QVBoxLayout(card)

        # Title
        self.header = QLabel("Prop Type:")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header)

        # Grid layout for prop buttons
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        # Define props and corresponding SVG icons
        props = {
            # "Hand": "images/props/hand.svg",
            "Staff": "images/props/staff.svg",
            "Club": "images/props/club.svg",
            "Fan": "images/props/fan.svg",
            "Triad": "images/props/triad.svg",
            "Minihoop": "images/props/minihoop.svg",
            "Buugeng": "images/props/buugeng.svg",
            "Triquetra": "images/props/triquetra.svg",
        }

        # Add buttons to grid
        row, col = 0, 0
        for prop, icon_path in props.items():
            button = PropButton(prop, icon_path, self, self._set_current_prop_type)
            self.buttons.append(button)
            grid_layout.addWidget(button, row, col)

            # Move to the next grid cell
            col += 1
            if col >= 3:  # 3 columns per row
                col = 0
                row += 1

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

    def _set_current_prop_type(self, prop_type: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_prop_type(prop_type)
        self.main_widget.settings_manager.global_settings.prop_type_changer.apply_prop_type()

    def resizeEvent(self, event):
        font = QFont()
        font_size = self.settings_dialog.width() // 30
        font.setPointSize(font_size)
        font.setBold(True)
        self.header.setFont(font)
