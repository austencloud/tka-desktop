import sys
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.json_manager.json_manager import JsonManager
from main_window.main_widget.json_manager.json_special_placement_handler import (
    JsonSpecialPlacementHandler,
)
from main_window.settings_manager.global_settings.app_context import AppContext
from qt_debug_message_handler import QtDebugMessageHandler
from main_window.settings_manager.settings_manager import SettingsManager
from splash_screen.splash_screen import SplashScreen
from main_window.main_window import MainWindow
from profiler import Profiler


def main() -> None:
    debug_handler = QtDebugMessageHandler()
    debug_handler.install()
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")  # Force Fusion style

    app.setStyle("Fusion")

    settings_manager = SettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()
    profiler = Profiler()
    # 1) Create or load the QSettings-based manager

    # 2) Create your JSON Manager (now no longer requires main_widget)
    json_manager = JsonManager()

    # 3) Optionally create any other "global" managers
    special_placement_handler = JsonSpecialPlacementHandler()

    # 4) Initialize the singleton context
    AppContext.init(settings_manager, json_manager, special_placement_handler)
    main_window = MainWindow(profiler, splash_screen)
    main_window.show()
    main_window.raise_()

    QTimer.singleShot(0, lambda: splash_screen.close())
    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
