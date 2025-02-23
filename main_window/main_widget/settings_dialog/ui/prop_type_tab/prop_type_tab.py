from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from Enums.PropTypes import PropType
from ...styles.card_frame import CardFrame
from ...ui.prop_type_tab.prop_button import (
    PropButton,
)

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
        """Set up the prop type selection UI."""
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
            "Staff": "images/props/staff.svg",
            "Club": "images/props/club.svg",
            "Fan": "images/props/fan.svg",
            "Triad": "images/props/triad.svg",
            "Minihoop": "images/props/minihoop.svg",
            "Buugeng": "images/props/buugeng.svg",
            "Triquetra": "images/props/triquetra.svg",
        }

        # Create buttons and add them to the layout
        row, col = 0, 0
        for prop, icon_path in props.items():
            button = PropButton(prop, icon_path, self, self._set_current_prop_type)
            self.buttons[prop] = button
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
        """Update the active prop type when a button is clicked."""
        settings_manager = self.main_widget.settings_manager
        self._update_active_button(prop_type)
        QApplication.processEvents()

        # Collect pictographs from MainWidget's PictographCollector
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        settings_manager.global_settings.set_prop_type(prop_type, pictographs)
        QApplication.restoreOverrideCursor()
        # Update button states

    def _update_active_button(self, active_prop: PropType):
        """Ensure only the selected prop is highlighted."""
        if not active_prop:
            return  # Safety check in case settings didn't load properly

        active_prop_name = (
            active_prop.name if isinstance(active_prop, PropType) else str(active_prop)
        )

        for prop, button in self.buttons.items():
            button.set_active(prop == active_prop_name)

    def update_active_prop_type_from_settings(self):
        """Retrieve the currently selected prop from settings and update the UI."""
        current_prop = self.main_widget.settings_manager.global_settings.get_prop_type()
        self._update_active_button(current_prop)

    def resizeEvent(self, event):
        """Dynamically update font size on resize."""
        font = QFont()
        font_size = self.settings_dialog.width() // 30
        font.setPointSize(font_size)
        font.setBold(True)
        self.header.setFont(font)
