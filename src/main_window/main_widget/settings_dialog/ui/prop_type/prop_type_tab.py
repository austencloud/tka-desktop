from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from enums.prop_type import PropType
from main_window.main_widget.settings_dialog.card_frame import CardFrame
from main_window.main_widget.settings_dialog.ui.prop_type.prop_button import PropButton
from utils.path_helpers import get_image_path


if TYPE_CHECKING:
    from ...settings_dialog import SettingsDialog


class PropTypeTab(QWidget):
    buttons: dict[str, PropButton] = {}

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self._setup_ui()

    def _setup_ui(self):
        card = CardFrame(self)
        main_layout = QVBoxLayout(card)

        # Title
        self.header = QLabel("Prop Type:")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.header)

        # Grid layout for prop "cells"
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        # Define props and corresponding SVG icons
        props = {
            "Staff": "props/staff.svg",
            "Club": "props/club.svg",
            "Fan": "props/fan.svg",
            "Triad": "props/triad.svg",
            "Minihoop": "props/minihoop.svg",
            "Buugeng": "props/buugeng.svg",
            "Triquetra": "props/triquetra.svg",
            "Sword": "props/sword.svg",
            "Chicken": "props/chicken.png",
            "Hand": "props/hand.svg",
            "Guitar": "props/guitar.svg",
            "Ukulele": "props/ukulele.svg",
        }

        row, col = 0, 0
        for prop, icon_path in props.items():
            # Create the icon‐only button
            button = PropButton(
                prop,
                get_image_path(icon_path),
                self,
                self._set_current_prop_type,
            )
            self.buttons[prop] = button

            # Create a label for the prop name
            label = QLabel(prop, self)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Optionally style the label text color/size:
            # label.setStyleSheet("color: #FFFFFF; margin-top: 5px;")

            # Put the button + label in a vertical layout
            cell_widget = QWidget(self)
            v_layout = QVBoxLayout(cell_widget)
            v_layout.setContentsMargins(0, 0, 0, 0)
            v_layout.setSpacing(5)
            v_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

            # Add that widget to the grid
            grid_layout.addWidget(cell_widget, row, col)

            col += 1
            if col >= 3:  # 3 columns per row
                col = 0
                row += 1

        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card)
        self.setLayout(outer_layout)

    def _set_current_prop_type(self, prop_type: str):
        settings_manager = self.main_widget.settings_manager
        self._update_active_button(prop_type)
        QApplication.processEvents()

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        settings_manager.global_settings.set_prop_type(prop_type, pictographs)
        QApplication.restoreOverrideCursor()

    def _update_active_button(self, active_prop: PropType):
        if not active_prop:
            return

        active_prop_name = (
            active_prop.name if isinstance(active_prop, PropType) else str(active_prop)
        )

        for prop, button in self.buttons.items():
            button.set_active(prop == active_prop_name)

    def update_active_prop_type_from_settings(self):
        current_prop = self.main_widget.settings_manager.global_settings.get_prop_type()
        self._update_active_button(current_prop)

    def resizeEvent(self, event):
        self.update_size()
        super().resizeEvent(event)

    def update_size(self):
        font = QFont()
        font_size = self.settings_dialog.width() // 30
        font.setPointSize(font_size)
        font.setBold(True)
        self.header.setFont(font)
        for prop, button in self.buttons.items():
            button.update_size()
