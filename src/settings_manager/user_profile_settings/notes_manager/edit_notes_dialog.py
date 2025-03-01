from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QLineEdit,
    QMessageBox,
    QDialogButtonBox,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from settings_manager.user_profile_settings.notes_manager.notes_manager import (
        NotesManager,
    )


class EditNotesDialog(QDialog):
    def __init__(self, notes_manager: "NotesManager"):
        super().__init__()
        self.notes_manager = notes_manager
        self.original_notes = self.notes_manager.get_all_notes().copy()
        self.setWindowTitle("Edit Notes")
        self.setModal(True)
        self.setMinimumWidth(300)

        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.notes_list = QListWidget(self)
        self.notes_list.addItems(self.original_notes)
        self.layout.addWidget(self.notes_list)

        self.new_note_field = QLineEdit(self)
        self.new_note_field.setPlaceholderText("Enter new note")
        self.layout.addWidget(self.new_note_field)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Note", self)
        self.remove_button = QPushButton("Remove Selected Note", self)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.button_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.layout.addWidget(self.button_box)

        self.add_button.clicked.connect(self.add_note)
        self.remove_button.clicked.connect(self.remove_selected_note)
        self.button_box.accepted.connect(self.apply_changes)
        self.button_box.rejected.connect(self.reject)

        self.new_note_field.returnPressed.connect(self.add_note)
        self.notes_list.itemSelectionChanged.connect(self.update_selection_highlight)

        self.set_initial_selection()

    def set_initial_selection(self):
        previous_note = self.notes_manager.get_current_note()
        items = self.notes_list.findItems(previous_note, Qt.MatchFlag.MatchExactly)
        if items:
            item = items[0]
            self.notes_list.setCurrentItem(item)
            self.update_selection_highlight()

    def add_note(self):
        new_note = self.new_note_field.text()
        if new_note.strip():
            if self.notes_manager.add_new_note(new_note.strip()):
                self.notes_list.addItem(new_note.strip())
                self.notes_list.setCurrentRow(self.notes_list.count() - 1)
                self.new_note_field.clear()
            else:
                QMessageBox.warning(
                    self, "Warning", f"Note '{new_note.strip()}' already exists."
                )
        else:
            self.apply_changes()

    def remove_selected_note(self):
        selected_items = self.notes_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No note selected.")
            return

        for item in selected_items:
            note_text = item.text()
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete note '{note_text}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.notes_manager.remove_note(note_text):
                    self.notes_list.takeItem(self.notes_list.row(item))
                else:
                    QMessageBox.warning(
                        self, "Warning", f"Failed to remove note '{note_text}'."
                    )

    def update_selection_highlight(self):
        for index in range(self.notes_list.count()):
            item = self.notes_list.item(index)
            item.setBackground(Qt.GlobalColor.white)
        selected_items = self.notes_list.selectedItems()
        if selected_items:
            selected_items[0].setBackground(Qt.GlobalColor.cyan)

    def apply_changes(self):
        selected_items = self.notes_list.selectedItems()
        if selected_items:
            selected_note = selected_items[0].text()
            self.notes_manager.set_current_note(selected_note)
        self.notes_manager.save_notes()
        self.accept()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if not self.new_note_field.hasFocus():
                self.apply_changes()
        elif event.key() == Qt.Key.Key_Delete:
            self.remove_selected_note()
        else:
            super().keyPressEvent(event)
