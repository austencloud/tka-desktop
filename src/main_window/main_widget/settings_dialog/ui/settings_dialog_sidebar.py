from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog



class SettingsDialogSidebar(QListWidget):
    tab_selected = pyqtSignal(int)

    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.setFixedWidth(220)
        self.setSpacing(10)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.currentRowChanged.connect(self.tab_selected)

    def add_item(self, name: str):
        """Adds an item to the sidebar only if it doesn't exist."""
        for i in range(self.count()):
            if self.item(i).text() == name:
                print(f"[WARNING] Sidebar already contains '{name}', skipping duplicate.")
                return  # Prevent duplicates

        item = QListWidgetItem(name)
        self.addItem(item)
