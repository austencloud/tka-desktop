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
    from legacy_settings_manager.user_profile_settings.user_manager.user_manager import (
        UserManager,
    )


class EditUserProfilesDialog(QDialog):
    def __init__(self, user_manager: "UserManager"):
        super().__init__()
        self.user_manager = user_manager
        self.original_users = self.user_manager.get_all_users().copy()
        self.setWindowTitle("Edit Users")
        self.setModal(True)
        self.setMinimumWidth(300)

        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.user_list = QListWidget(self)
        self.user_list.addItems(self.original_users)
        self.layout.addWidget(self.user_list)

        self.new_user_field = QLineEdit(self)
        self.new_user_field.setPlaceholderText("Enter new user name")
        self.layout.addWidget(self.new_user_field)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add User", self)
        self.remove_button = QPushButton("Remove Selected User", self)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.remove_button)

        self.layout.addLayout(self.button_layout)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.layout.addWidget(self.button_box)

        self.add_button.clicked.connect(self.add_user)
        self.remove_button.clicked.connect(self.remove_selected_user)
        self.button_box.accepted.connect(self.apply_changes)
        self.button_box.rejected.connect(self.reject)

        self.new_user_field.returnPressed.connect(self.add_user)
        self.user_list.itemSelectionChanged.connect(self.update_selection_highlight)

        self.set_initial_selection()

    def set_initial_selection(self):
        current_user = self.user_manager.get_current_user()
        items = self.user_list.findItems(current_user, Qt.MatchFlag.MatchExactly)
        if items:
            item = items[0]
            self.user_list.setCurrentItem(item)
            self.update_selection_highlight()

    def add_user(self):
        new_user = self.new_user_field.text()
        if new_user.strip():
            if self.user_manager.add_new_user(new_user.strip()):
                self.user_list.addItem(new_user.strip())
                self.user_list.setCurrentRow(self.user_list.count() - 1)
                self.new_user_field.clear()
            else:
                QMessageBox.warning(
                    self, "Warning", f"User '{new_user.strip()}' already exists."
                )
        else:
            self.apply_changes()

    def remove_selected_user(self):
        selected_items = self.user_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No user selected.")
            return

        for item in selected_items:
            user_name = item.text()
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete user '{user_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.Yes:
                if self.user_manager.remove_user(user_name):
                    self.user_list.takeItem(self.user_list.row(item))
                else:
                    QMessageBox.warning(
                        self, "Warning", f"Failed to remove user '{user_name}'."
                    )

    def update_selection_highlight(self):
        for index in range(self.user_list.count()):
            item = self.user_list.item(index)
            item.setBackground(Qt.GlobalColor.white)
        selected_items = self.user_list.selectedItems()
        if selected_items:
            selected_items[0].setBackground(Qt.GlobalColor.cyan)

    def apply_changes(self):
        self.user_manager.save_users()
        self.accept()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if not self.new_user_field.hasFocus():
                self.apply_changes()
        elif event.key() == Qt.Key.Key_Delete:
            self.remove_selected_user()
        else:
            super().keyPressEvent(event)
