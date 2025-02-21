import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt

from main_window.palette_manager import PaletteManager


from .settings_manager.settings_manager import SettingsManager
from .main_widget.main_widget import MainWidget
from main_window.main_window_geometry_manager import MainWindowGeometryManager

if TYPE_CHECKING:
    from profiler import Profiler
    from splash_screen.splash_screen import SplashScreen


class MainWindow(QMainWindow):
    def __init__(self, profiler: "Profiler", splash_screen: "SplashScreen") -> None:
        super().__init__()
        self.profiler = profiler
        self.main_widget = None  # Initialize main_widget to None
        self.palette_manager = PaletteManager(self)

        self.geometry_manager = MainWindowGeometryManager(self)
        self.main_widget = MainWidget(self, splash_screen)  # Set main_widget here
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle("The Kinetic Constructor")
        self.geometry_manager.set_dimensions()

    def exec(self, app: QApplication) -> int:
        self.profiler.enable()
        result = app.exec()
        self.profiler.disable()
        self.profiler.write_profiling_stats_to_file("profiling_output.txt", os.getcwd())
        return result

    def closeEvent(self, event):
        super().closeEvent(event)
        QApplication.instance().installEventFilter(self)

