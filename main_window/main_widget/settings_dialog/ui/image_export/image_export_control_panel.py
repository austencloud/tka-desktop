from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QCheckBox, QWidget, QComboBox, QLabel
from PyQt6.QtCore import pyqtSignal, Qt

if TYPE_CHECKING:
    from .image_export_tab import ImageExportTab


class ImageExportControlPanel(QWidget):
    settingChanged = pyqtSignal()

    def __init__(self, tab: "ImageExportTab"):
        super().__init__(tab)
        self.tab = tab
        self.settings_manager = tab.settings_manager
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.user_combo_box = QComboBox()
        self.notes_combo_box = QComboBox()
        self._populate_combos()

        user_label = QLabel("User:")
        notes_label = QLabel("Notes:")

        self.checkboxes = {
            "include_start_position": QCheckBox("Include Start Position"),
            "add_info": QCheckBox("Add User Info"),
            "add_word": QCheckBox("Add Word"),
            "add_difficulty_level": QCheckBox("Add Difficulty Level"),
            "add_beat_numbers": QCheckBox("Add Beat Numbers"),
            "add_reversal_symbols": QCheckBox("Add Reversal Symbols"),
        }

        for key in self.checkboxes:
            self.checkboxes[key].setChecked(
                self.settings_manager.image_export.get_image_export_setting(key)
            )

        layout.addWidget(user_label)
        layout.addWidget(self.user_combo_box)
        layout.addWidget(notes_label)
        layout.addWidget(self.notes_combo_box)

        for cb in self.checkboxes.values():
            layout.addWidget(cb)

    def _populate_combos(self):
        self.settings_manager.users.user_manager.populate_user_profiles_combo_box(
            self.user_combo_box
        )
        self.settings_manager.users.notes_manager.populate_notes(self.notes_combo_box)

    def _connect_signals(self):
        for key, cb in self.checkboxes.items():
            cb.toggled.connect(lambda checked, k=key: self._update_setting(k, checked))
        self.user_combo_box.currentTextChanged.connect(self._update_user)
        self.notes_combo_box.currentTextChanged.connect(self._update_note)

    def _update_setting(self, key: str, value: bool):
        self.settings_manager.image_export.set_image_export_setting(key, value)
        self.settingChanged.emit()

    def _update_user(self, user: str):
        self.settings_manager.users.user_manager.set_current_user(user)
        self.settingChanged.emit()

    def _update_note(self, note: str):
        self.settings_manager.users.notes_manager.set_current_note(note)
        self.settingChanged.emit()
