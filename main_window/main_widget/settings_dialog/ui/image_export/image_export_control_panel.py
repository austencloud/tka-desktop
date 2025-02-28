from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
)
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab_button import (
    ImageExportTabButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from main_window.settings_manager.settings_manager import SettingsManager


class ImageExportControlPanel(QWidget):
    """
    A control panel for configuring image export settings.
    Lays out the UI elements for user settings, notes, and export options.
    """

    settingChanged = pyqtSignal()

    def __init__(
        self, settings_manager: "SettingsManager", image_export_tab: "ImageExportTab"
    ):
        """
        Initializes the control panel with the given settings manager.

        Args:
            settings_manager: The settings manager instance.
            parent: The parent widget.
        """
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.settings_manager = settings_manager
        self.user_combo_box = QComboBox()
        self.notes_combo_box = QComboBox()
        self.buttons: dict[str, ImageExportTabButton] = {}
        self.button_settings_keys = {
            "Start Position": "include_start_position",
            "User Info": "add_user_info",
            "Word": "add_word",
            "Difficulty Level": "add_difficulty_level",
            "Beat Numbers": "add_beat_numbers",
            "Reversal Symbols": "add_reversal_symbols",
        }
        self._setup_ui()

        self._load_user_profiles()  # Load users from settings on init
        self._load_saved_notes()  # Load custom notes from settings on init

    def _load_user_profiles(self):
        """Loads user profiles into the user combo box on startup."""
        self.user_combo_box.clear()
        user_profiles = self.settings_manager.users.get_user_profiles()
        if user_profiles:
            self.user_combo_box.addItems(user_profiles.keys())

        current_user = self.settings_manager.users.get_current_user()
        if current_user and current_user in user_profiles:
            self.user_combo_box.setCurrentText(current_user)

    def _load_saved_notes(self):
        """Loads custom notes into the notes combo box on startup."""
        self.notes_combo_box.clear()
        custom_notes = self.settings_manager.users.get_saved_notes()
        if custom_notes:
            self.notes_combo_box.addItems(custom_notes)

        current_note = self.settings_manager.users.get_current_note()
        if current_note and current_note in custom_notes:
            self.notes_combo_box.setCurrentText(current_note)

    def _setup_ui(self):
        """Sets up the user interface layout."""
        main_layout = QVBoxLayout(self)

        top_layout = self._create_user_notes_layout()
        grid_layout = self._create_buttons_grid_layout()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def _create_user_notes_layout(self) -> QHBoxLayout:
        """Creates the horizontal layout for user and notes combo boxes."""
        top_layout = QHBoxLayout()

        top_layout.addWidget(QLabel("User:"))
        top_layout.addWidget(self.user_combo_box)
        top_layout.addWidget(QLabel("Notes:"))
        top_layout.addWidget(self.notes_combo_box)

        return top_layout

    def _create_buttons_grid_layout(self) -> QGridLayout:
        """Creates the grid layout for the export option buttons."""
        grid_layout = QGridLayout()

        for i, (label, setting_key) in enumerate(self.button_settings_keys.items()):
            button = ImageExportTabButton(
                label, setting_key, self.settings_manager, self.image_export_tab
            )
            button.clicked.connect(self.emit_setting_changed)
            self.buttons[label] = button
            row, col = divmod(i, 3)
            grid_layout.addWidget(button, row, col)

        return grid_layout

    def emit_setting_changed(self):
        """Emits a signal when a setting is changed."""
        self.settingChanged.emit()
