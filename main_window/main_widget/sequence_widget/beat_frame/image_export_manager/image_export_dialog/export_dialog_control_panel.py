from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QCheckBox,
    QWidget,
    QComboBox,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt

from main_window.settings_manager.user_profile_settings.notes_manager.notes_manager import NotesManager

if TYPE_CHECKING:
    from .image_export_dialog import ImageExportDialog


class ExportDialogControlPanel(QWidget):
    notesChanged = pyqtSignal(str)

    def __init__(self, export_dialog: "ImageExportDialog"):
        super().__init__()
        self.export_dialog = export_dialog
        self.settings_manager = export_dialog.export_manager.settings_manager
        self.user_manager = self.settings_manager.users.user_manager
        self.notes_manager = self.settings_manager.users.notes_manager

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup UI components and layout."""
        # ComboBoxes for user and notes
        self.user_combo_box = QComboBox(self)
        self.user_manager.populate_user_profiles_combo_box(self.user_combo_box)
        self.notes_combo_box = QComboBox(self)
        self.notes_manager.populate_notes(self.notes_combo_box)

        self.previous_note = self.notes_manager.get_current_note()
        self.previous_user = self.user_manager.get_current_user()

        # Setup checkboxes
        self.checkboxes = {
            "include_start_position": self._create_checkbox(
                "Add Start Position", "include_start_position"
            ),
            "add_info": self._create_checkbox("Add Info", "add_info"),
            "add_word": self._create_checkbox("Add Word to Image", "add_word"),
            "add_difficulty_level": self._create_checkbox(
                "Include Difficulty Level", "add_difficulty_level"
            ),
            "add_beat_numbers": self._create_checkbox(
                "Add Beat Numbers", "add_beat_numbers"
            ),
            "add_reversal_symbols": self._create_checkbox(
                "Add Reversal Symbols", "add_reversal_symbols"
            ),
            "open_directory_on_export": self._create_checkbox(
                "Open file location after export", "open_directory_on_export"
            ),
        }
        self.include_start_pos_check = self.checkboxes["include_start_position"]
        self.add_info_check = self.checkboxes["add_info"]
        self.add_word_check = self.checkboxes["add_word"]
        self.include_difficulty_level_check = self.checkboxes["add_difficulty_level"]
        self.add_beat_numbers_check = self.checkboxes["add_beat_numbers"]
        self.add_reversal_symbols_check = self.checkboxes["add_reversal_symbols"]
        self.open_directory_check = self.checkboxes["open_directory_on_export"]
        
        # Set up the layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self._add_combo_boxes_to_layout()
        self._add_checkboxes_to_layout()

    def _create_checkbox(self, label: str, setting_key: str) -> QCheckBox:
        """Create a checkbox and set its initial state based on the provided setting."""
        checkbox = QCheckBox(label, self)
        checkbox.setChecked(
            self.settings_manager.image_export.get_image_export_setting(setting_key)
        )
        checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        checkbox.toggled.connect(lambda: self._toggle_setting(checkbox, setting_key))
        return checkbox

    def _add_combo_boxes_to_layout(self):
        """Add user and notes combo boxes to the layout."""
        user_label = QLabel("User:", self)
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        notes_label = QLabel("Note:", self)
        notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        user_layout = QVBoxLayout()
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_combo_box)
        user_layout.addWidget(notes_label)
        user_layout.addWidget(self.notes_combo_box)

        self.layout.addLayout(user_layout)

    def _add_checkboxes_to_layout(self):
        """Add all checkboxes to the layout."""
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for checkbox in self.checkboxes.values():
            checkbox_layout.addWidget(checkbox)

        self.layout.addLayout(checkbox_layout)

    def _toggle_setting(self, checkbox: QCheckBox, setting_key: str):
        """Toggle the setting based on the checkbox state and update the preview."""
        self.settings_manager.image_export.set_image_export_setting(
            setting_key, checkbox.isChecked()
        )
        self.export_dialog.preview_panel.update_preview(
            self.checkboxes["include_start_position"].isChecked(),
            self.checkboxes["add_info"].isChecked(),
            self.export_dialog.sequence,
            self.checkboxes["add_word"].isChecked(),
            self.checkboxes["add_difficulty_level"].isChecked(),
            self.checkboxes["add_beat_numbers"].isChecked(),
            self.checkboxes["add_reversal_symbols"].isChecked(),
        )

    def _connect_signals(self):
        """Connect signals for combo boxes."""
        self.user_combo_box.currentIndexChanged.connect(self._handle_user_selection)
        self.notes_combo_box.currentIndexChanged.connect(self._handle_note_selection)

    def _handle_user_selection(self):
        """Handle the selection of a user from the combo box."""
        selected_user = self.user_combo_box.currentText()
        if selected_user == "Edit Users":
            self._open_edit_dialog(
                self.user_manager, self.previous_user, self.user_combo_box
            )
        else:
            self.previous_user = selected_user
            self._update_preview()

    def _handle_note_selection(self):
        """Handle the selection of a note from the combo box."""
        selected_note = self.notes_combo_box.currentText()
        if selected_note == "Edit Notes":
            self._open_edit_dialog(
                self.notes_manager, self.previous_note, self.notes_combo_box
            )
        else:
            self.previous_note = selected_note
            self._update_preview()

    def _open_edit_dialog(self, manager: "NotesManager", previous_value, combo_box: QComboBox):
        """Open the edit dialog for users or notes."""
        manager.open_edit_notes_dialog()
        index = combo_box.findText(previous_value)
        if index != -1:
            combo_box.setCurrentIndex(index)

    def _update_preview(self):
        """Update the preview panel with the current settings."""
        self.export_dialog.preview_panel.update_preview(
            self.checkboxes["include_start_position"].isChecked(),
            self.checkboxes["add_info"].isChecked(),
            self.export_dialog.sequence,
            self.checkboxes["add_word"].isChecked(),
            self.checkboxes["add_difficulty_level"].isChecked(),
            self.checkboxes["add_beat_numbers"].isChecked(),
            self.checkboxes["add_reversal_symbols"].isChecked(),
        )
