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
        from .config import Paths

        Paths.ensure_directories()
        window = LauncherWindow()
        window.show()

        return self.exec()
