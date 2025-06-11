from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from ..components.searchable_grid import SearchableGrid
from ..components.animated_card import AnimatedCard
from ...data.app_definitions import AppDefinitions


class DevToolsTab(QWidget):
    def __init__(self, process_manager, recent_actions_manager, parent=None):
        super().__init__(parent)
        self.process_manager = process_manager
        self.recent_actions_manager = recent_actions_manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 5)

        self.dev_grid = SearchableGrid()

        try:
            for tool_def in AppDefinitions.get_by_category("dev_tools"):
                card = AnimatedCard(
                    tool_def.title,
                    tool_def.description,
                    tool_def.icon,
                    lambda tool=tool_def: self.launch_tool(tool),
                )
                self.dev_grid.add_card(card)
        except Exception:
            dev_tools = [
                ("🧪 Run Tests", "Execute test suite", "🧪"),
                ("📝 Format Code", "Format with black", "📝"),
                ("🔍 Lint Code", "Run flake8 linting", "🔍"),
                ("📦 Build Project", "Build executable", "📦"),
            ]

            for title, desc, icon in dev_tools:
                card = AnimatedCard(title, desc, icon, lambda: None)
                self.dev_grid.add_card(card)

        layout.addWidget(self.dev_grid)

    def launch_tool(self, tool_def):
        if hasattr(self.recent_actions_manager, "add_action"):
            self.recent_actions_manager.add_action(tool_def.title)

        if tool_def.script_path:
            process = self.process_manager.execute_python_script(
                tool_def.script_path, tool_def.args, tool_def.env
            )
        elif tool_def.command:
            process = self.process_manager.execute_command(
                tool_def.command, tool_def.working_dir, tool_def.env
            )

        if not process:
            self.show_error(f"Failed to launch {tool_def.title}")

    def handle_resize(self, size):
        if hasattr(self.dev_grid, "handle_resize"):
            self.dev_grid.handle_resize(size)

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Dev Tool Error")
        msg.setText(message)
        msg.exec()
