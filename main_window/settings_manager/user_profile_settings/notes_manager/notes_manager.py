from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QObject
from .edit_notes_dialog import EditNotesDialog

if TYPE_CHECKING:
    from ..user_profile_settings import UserProfileSettings


class NotesManager(QObject):
    def __init__(self, user_profile_settings: "UserProfileSettings"):
        super().__init__()
        self.user_profile_settings = user_profile_settings
        self.notes_combo_box = None

    def populate_notes(self, notes_combo_box: QComboBox):
        self.notes_combo_box = notes_combo_box
        notes_combo_box.clear()
        notes = self.user_profile_settings.get_saved_notes()

        for note in notes:
            notes_combo_box.addItem(note)
        notes_combo_box.addItem("Edit Notes")
        current_note = self.user_profile_settings.get_current_note()
        if current_note in notes:
            index = notes_combo_box.findText(current_note)
            if index != -1:
                notes_combo_box.setCurrentIndex(index)
        else:
            notes_combo_box.setCurrentIndex(0)

    def open_edit_notes_dialog(self):
        dialog = EditNotesDialog(self)
        if dialog.exec():
            self.populate_notes(self.notes_combo_box)

    def get_all_notes(self):
        return self.user_profile_settings.get_saved_notes()

    def add_new_note(self, note):
        notes = self.user_profile_settings.get_saved_notes()
        if note in notes:
            return False
        notes.append(note)
        self.user_profile_settings.set_saved_notes(notes)
        return True

    def remove_note(self, note):
        notes = self.user_profile_settings.get_saved_notes()
        if note in notes:
            notes.remove(note)
            self.user_profile_settings.set_saved_notes(notes)
            return True
        return False

    def save_notes(self):
        # Notes are saved directly with set_saved_notes, no additional save needed
        pass

    def get_current_note(self):
        return self.user_profile_settings.get_current_note()

    def set_current_note(self, note):
        self.user_profile_settings.set_current_note(note)
        index = self.notes_combo_box.findText(note)
        if index != -1:
            self.notes_combo_box.setCurrentIndex(index)

    def get_previous_note(self):
        return self.user_profile_settings.get_current_note()