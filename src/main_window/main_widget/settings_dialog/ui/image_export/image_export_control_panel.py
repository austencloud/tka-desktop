from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
)
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab_button import (
    ImageExportTabButton,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from settings_manager.settings_manager import SettingsManager


class ImageExportControlPanel(QWidget):
    """
    A control panel for configuring image export settings.
    """

    settingChanged = pyqtSignal()

    def __init__(
        self, settings_manager: "SettingsManager", image_export_tab: "ImageExportTab"
    ):
        super().__init__(image_export_tab)
        self.image_export_tab = image_export_tab
        self.settings_manager = settings_manager
        self.user_combo_box = QComboBox()
        self.note_input = QLineEdit()  # Single text field for notes
        self.buttons = {}
        self.button_settings_keys = {
            "Start Position": "include_start_position",
            "User Info": "add_user_info",
            "Word": "add_word",
            "Difficulty Level": "add_difficulty_level",
            "Beat Numbers": "add_beat_numbers",
            "Reversal Symbols": "add_reversal_symbols",
        }
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the user interface layout."""
        main_layout = QVBoxLayout(self)

        top_layout = self._create_user_notes_layout()
        grid_layout = self._create_buttons_grid_layout()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

        # Load settings
        self._load_user_profiles()
        self._load_saved_note()

    def _create_user_notes_layout(self) -> QHBoxLayout:
        """Creates the horizontal layout for user and custom note field."""
        top_layout = QHBoxLayout()

        # User dropdown
        top_layout.addWidget(QLabel("User:"))
        top_layout.addWidget(self.user_combo_box)

        # Custom note field
        top_layout.addWidget(QLabel("Custom Note:"))
        self.note_input.setPlaceholderText("Enter note to include in exports")
        self.note_input.textChanged.connect(self._save_current_note)
        top_layout.addWidget(self.note_input)

        return top_layout

    def _save_current_note(self):
        """Save the current note to settings."""
        note_text = self.note_input.text()
        self.settings_manager.image_export.set_custom_note(note_text)

    def _load_saved_note(self):
        """Load the saved custom note."""
        saved_note = self.settings_manager.image_export.get_custom_note()
        if saved_note:
            self.note_input.setText(saved_note)

    def _load_user_profiles(self):
        """Loads user profiles into the user combo box."""
        self.user_combo_box.clear()
        user_profiles = self.settings_manager.users.get_user_profiles()
        if user_profiles:
            self.user_combo_box.addItems(user_profiles.keys())

        current_user = self.settings_manager.users.get_current_user()
        if current_user and current_user in user_profiles:
            self.user_combo_box.setCurrentText(current_user)

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
