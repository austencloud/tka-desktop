from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys


class LauncherApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setup_application()

    def setup_application(self):
        self.setStyle("Fusion")
        self.setApplicationName("Kinetic Constructor Launcher")
        self.setApplicationVersion("2.0")
        self.setOrganizationName("Kinetic Constructor")

        try:
            self.setWindowIcon(QIcon("icon.png"))
        except:
            pass

    def run(self):
        from ..ui.main_window import LauncherWindow
        from .config import Config
        from .process_manager import ProcessManager
        from ..data.recent_actions import RecentActionsManager
        from ..data.favorites_manager import FavoritesManager
        from ..monitoring.process_monitor import ProcessMonitor

        config = Config()
        process_manager = ProcessManager()
        recent_actions_manager = RecentActionsManager()
        favorites_manager = FavoritesManager()
        process_monitor = ProcessMonitor(process_manager)

        window = LauncherWindow(
            config,
            process_manager,
            recent_actions_manager,
            favorites_manager,
            process_monitor,
        )
        window.show()

        return self.exec()
