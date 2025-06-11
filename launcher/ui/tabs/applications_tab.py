from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QMainWindow
from PyQt6.QtCore import QObject
from typing import Optional
from ..components.searchable_grid import SearchableGrid
from ..components.animated_card import AnimatedCard
from ...data.app_definitions import AppDefinitions


class ApplicationsTab(QWidget):
    def __init__(self, process_manager, recent_actions_manager, parent=None):
        super().__init__(parent)
        self.process_manager = process_manager
        self.recent_actions_manager = recent_actions_manager
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 5)

        self.apps_grid = SearchableGrid()

        try:
            for app_def in AppDefinitions.get_by_category("applications"):
                card = AnimatedCard(
                    app_def.title,
                    app_def.description,
                    app_def.icon,
                    lambda app=app_def: self.launch_application(app),
                )
                self.apps_grid.add_card(card)
        except Exception:
            pass

        layout.addWidget(self.apps_grid)

    def connect_signals(self):
        if hasattr(self.process_manager, "process_started"):
            self.process_manager.process_started.connect(self.on_process_started)
        if hasattr(self.process_manager, "process_error"):
            self.process_manager.process_error.connect(self.on_process_error)
        if hasattr(self.process_manager, "process_finished"):
            self.process_manager.process_finished.connect(self.on_process_finished)

    def launch_application(self, app_def):
        if hasattr(self.recent_actions_manager, "add_action"):
            self.recent_actions_manager.add_action(app_def.title)

        if app_def.script_path:
            process = self.process_manager.execute_python_script(
                app_def.script_path, app_def.args, app_def.env
            )
        elif app_def.command:
            process = self.process_manager.execute_command(
                app_def.command, app_def.working_dir, app_def.env
            )

        if not process:
            self.show_error(f"Failed to launch {app_def.title}")

    def handle_resize(self, size):
        if hasattr(self.apps_grid, "handle_resize"):
            self.apps_grid.handle_resize(size)

    def get_main_window(self) -> Optional[QMainWindow]:
        widget: Optional[QObject] = self
        while widget is not None:
            parent_widget = widget.parent()
            if parent_widget is None:
                break
            widget = parent_widget
            if isinstance(widget, QMainWindow):
                return widget
        return None

    def on_process_started(self, command):
        main_window = self.get_main_window()
        if main_window is not None:
            status_bar = main_window.statusBar()
            if status_bar is not None:
                status_bar.showMessage(f"Started: {command}", 3000)

    def on_process_error(self, process_name, error_message):
        if not self._is_minor_issue(error_message):
            self.show_error(f"{process_name}: {error_message}")

    def _is_minor_issue(self, message: str) -> bool:
        minor_patterns = ["- INFO -", "version", "Python 3.", "Starting", "Initialized"]
        return any(pattern in message for pattern in minor_patterns)

    def on_process_finished(self, process_name, exit_code):
        main_window = self.get_main_window()
        if exit_code == 0:
            if main_window is not None:
                status_bar = main_window.statusBar()
                if status_bar is not None:
                    status_bar.showMessage(f"Completed: {process_name}", 2000)
        else:
            self.show_error(f"{process_name} exited with code {exit_code}")

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Application Launch Error")
        msg.setText(message)
        msg.exec()
