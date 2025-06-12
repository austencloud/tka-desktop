# Updated main_window.py - Modular Launcher UI
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
import sys
import subprocess
from pathlib import Path

from .components import QuickLaunchBar, CategoryTabs, StatusBar
from .styles import StyleManager


class HealthChecker(QThread):
    health_updated = pyqtSignal(bool)

    def run(self):
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "unified_dev_test.py",
                ],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=Path.cwd(),
            )

            is_healthy = result.returncode == 0 and "🟢 READY" in result.stdout
            self.health_updated.emit(is_healthy)
        except Exception:
            self.health_updated.emit(False)


class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_shortcuts()
        self.start_health_check()

    def setup_ui(self):
        self.setWindowTitle("🚀 Kinetic Constructor Launcher")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(StyleManager.get_main_style())

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        try:
            from ..data.app_definitions import AppDefinitions, AppCategory

            primary_apps = AppDefinitions.get_primary_apps()
            apps_by_category = {
                category.name: AppDefinitions.get_by_category(category)
                for category in AppCategory
                if AppDefinitions.get_by_category(category)
            }

            self.quick_launch = QuickLaunchBar(primary_apps)
            self.quick_launch.app_launch_requested.connect(self.launch_application)
            layout.addWidget(self.quick_launch)

            self.category_tabs = CategoryTabs(apps_by_category)
            layout.addWidget(self.category_tabs)

            self.status_bar = StatusBar()
            layout.addWidget(self.status_bar)

        except Exception as e:
            QMessageBox.critical(
                self, "Setup Error", f"Failed to initialize launcher: {e}"
            )

    def setup_shortcuts(self):
        try:
            from ..data.app_definitions import AppDefinitions

            for app in AppDefinitions.get_all():
                if app.keyboard_shortcut:
                    shortcut = QShortcut(QKeySequence(app.keyboard_shortcut), self)
                    shortcut.activated.connect(lambda a=app: self.launch_application(a))
        except Exception:
            pass

    def launch_application(self, app):
        self.status_bar.update_status(f"Launching {app.title}...")

        try:
            if app.script_path:
                cmd = [sys.executable, app.script_path]
                if app.args:
                    cmd.extend(app.args)

                env = None
                if app.env:
                    import os

                    env = os.environ.copy()
                    env.update(app.env)

                working_dir = app.working_dir if app.working_dir else None
                subprocess.Popen(cmd, env=env, cwd=working_dir)

            elif app.command:
                working_dir = app.working_dir if app.working_dir else None
                env = None
                if app.env:
                    import os

                    env = os.environ.copy()
                    env.update(app.env)

                subprocess.Popen(app.command, env=env, cwd=working_dir)

            self.status_bar.update_status(f"{app.title} launched successfully")

        except Exception as e:
            self.status_bar.update_status(f"Failed to launch {app.title}: {str(e)}")
            QMessageBox.warning(
                self, "Launch Error", f"Failed to launch {app.title}:\n{str(e)}"
            )

    def start_health_check(self):
        QTimer.singleShot(2000, self.run_health_check)

    def run_health_check(self):
        self.health_checker = HealthChecker()
        self.health_checker.health_updated.connect(self.status_bar.update_health)
        self.health_checker.start()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kinetic Constructor Launcher")

    window = LauncherWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
