from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence


class CommandPalette(QDialog):
    command_selected = pyqtSignal(str, dict)

    def __init__(self, app_definitions, parent=None):
        super().__init__(parent)
        self.app_definitions = app_definitions
        self.all_commands = self.build_command_list()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Command Palette")
        self.setModal(True)
        self.setFixedSize(600, 400)
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:0.3 #1a1a1e, stop:0.7 #16213e, stop:1 #0f0f23);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                font-size: 14px;
                padding: 10px;
            }
            QListWidget {
                background: transparent;
                border: none;
                color: white;
                font-size: 12px;
            }
            QListWidget::item {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background: rgba(102, 126, 234, 0.4);
                border: 1px solid rgba(102, 126, 234, 0.8);
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )

        layout = QVBoxLayout(self)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search commands...")
        self.search_input.textChanged.connect(self.filter_commands)
        layout.addWidget(self.search_input)

        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.execute_command)
        layout.addWidget(self.results_list)

        self.populate_commands()
        self.search_input.setFocus()

    def build_command_list(self):
        commands = []
        for app_def in self.app_definitions:
            commands.append(
                {
                    "title": f"Launch: {app_def.title}",
                    "description": app_def.description,
                    "action": "launch_app",
                    "data": app_def,
                }
            )

        commands.extend(
            [
                {
                    "title": "Toggle Theme",
                    "description": "Switch between light and dark theme",
                    "action": "toggle_theme",
                },
                {
                    "title": "Clear Cache",
                    "description": "Clear application cache",
                    "action": "clear_cache",
                },
                {
                    "title": "Show Settings",
                    "description": "Open settings dialog",
                    "action": "show_settings",
                },
                {
                    "title": "Minimize to Tray",
                    "description": "Hide launcher to system tray",
                    "action": "minimize",
                },
                {
                    "title": "Exit Application",
                    "description": "Close the launcher completely",
                    "action": "exit",
                },
            ]
        )

        return commands

    def filter_commands(self, text):
        self.results_list.clear()
        if not text:
            self.populate_commands()
            return

        filtered = [
            cmd
            for cmd in self.all_commands
            if text.lower() in cmd["title"].lower()
            or text.lower() in cmd["description"].lower()
        ]

        for cmd in filtered:
            item = QListWidgetItem(f"{cmd['title']} - {cmd['description']}")
            item.setData(Qt.ItemDataRole.UserRole, cmd)
            self.results_list.addItem(item)

    def populate_commands(self):
        for cmd in self.all_commands:
            item = QListWidgetItem(f"{cmd['title']} - {cmd['description']}")
            item.setData(Qt.ItemDataRole.UserRole, cmd)
            self.results_list.addItem(item)

    def execute_command(self, item):
        cmd_data = item.data(Qt.ItemDataRole.UserRole)
        self.command_selected.emit(cmd_data["action"], cmd_data.get("data", {}))
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            current_item = self.results_list.currentItem()
            if current_item:
                self.execute_command(current_item)
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Down:
            self.results_list.setFocus()
            if self.results_list.currentRow() < self.results_list.count() - 1:
                self.results_list.setCurrentRow(self.results_list.currentRow() + 1)
        elif event.key() == Qt.Key.Key_Up:
            self.results_list.setFocus()
            if self.results_list.currentRow() > 0:
                self.results_list.setCurrentRow(self.results_list.currentRow() - 1)
        else:
            super().keyPressEvent(event)
