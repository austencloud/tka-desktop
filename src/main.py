
import sys
import os
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.json_manager.json_manager import JsonManager
from main_window.main_widget.json_manager.special_placement_saver import (
    SpecialPlacementSaver,
)
from main_window.main_window import MainWindow
from settings_manager.global_settings import app_context
from utils.path_helpers import get_data_path
from settings_manager.settings_manager import SettingsManager
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from splash_screen.splash_screen import SplashScreen


from profiler import Profiler
from utils.call_tracer import CallTracer
from settings_manager.global_settings.app_context import AppContext
from utils.paint_event_supressor import PaintEventSuppressor

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILE_PATH = get_data_path("trace_log.txt")
log_file = open(LOG_FILE_PATH, "w")


def main() -> None:
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")

    settings_manager = SettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()

    profiler = Profiler()
    json_manager = JsonManager()
    special_placement_handler = SpecialPlacementSaver()
    special_placement_loader = SpecialPlacementLoader()

    AppContext.init(
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader=special_placement_loader,
    )

    # Explicitly set the MainWindow instance in AppContext before using it
    main_window = MainWindow(profiler, splash_screen)
    AppContext._main_window = main_window  

    main_window.show()
    main_window.raise_()

    QTimer.singleShot(0, lambda: splash_screen.close())

    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    PaintEventSuppressor.install_message_handler()
    tracer = CallTracer(PROJECT_DIR, log_file)
    sys.settrace(tracer.trace_calls)
    main()
