# main_window/main_widget/settings_dialog/image_export_tab/image_export_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox, QFormLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class ImageExportTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.settings_dialog = settings_dialog
        self.settings_manager = settings_dialog.main_widget.settings_manager
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Export Options Group
        options_group = QGroupBox("Image Export Settings")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.export_options = {
            "include_start_position": QCheckBox("Include Start Position"),
            "add_beat_numbers": QCheckBox("Show Beat Numbers"),
            "add_reversal_symbols": QCheckBox("Show Reversal Symbols"),
            "add_info": QCheckBox("Include User Info"),
            "add_word": QCheckBox("Include Sequence Word"),
            "add_difficulty_level": QCheckBox("Show Difficulty Level"),
            "open_directory_on_export": QCheckBox("Open Folder After Export")
        }

        for option, checkbox in self.export_options.items():
            checkbox.stateChanged.connect(self._save_settings)
            form_layout.addRow(checkbox)

        options_group.setLayout(form_layout)
        layout.addWidget(options_group)
        layout.addStretch()

    def _load_settings(self):
        """Load settings from the settings manager"""
        for option, checkbox in self.export_options.items():
            value = self.settings_manager.image_export.get_image_export_setting(option)
            checkbox.setChecked(value)

    def _save_settings(self):
        """Save current settings to the settings manager"""
        settings = {
            option: checkbox.isChecked()
            for option, checkbox in self.export_options.items()
        }
        for option, value in settings.items():
            self.settings_manager.image_export.set_image_export_setting(option, value)