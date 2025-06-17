from PyQt6.QtWidgets import QApplication
from typing import List

from ..presentation.launcher_window import LauncherWindow


class LauncherApplication(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        self.setStyle("Fusion")
        self.setApplicationName("Kinetic Constructor Launcher")
        self.setOrganizationName("Kinetic Constructor")

    def run(self) -> int:
        window = LauncherWindow()
        window.show()
        return self.exec()
