import sys
import os


def configure_import_paths():
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
        src_dir = os.path.join(base_dir, "src")
        if os.path.exists(src_dir) and src_dir not in sys.path:
            sys.path.insert(0, src_dir)
    else:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)


def initialize_logging():
    import os

    # Create a simple log file in the current directory
    log_file_path = os.path.join(os.getcwd(), "trace_log.txt")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    return open(log_file_path, "w")


def initialize_application():
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    return app


def initialize_context(
    settings_manager, json_manager, special_placement_handler, special_placement_loader
):
    from settings_manager.global_settings.app_context import AppContext

    AppContext.init(
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader=special_placement_loader,
    )


def create_main_window(profiler, splash_screen):
    from main_window.main_window import MainWindow

    main_window = MainWindow(profiler, splash_screen)
    from settings_manager.global_settings.app_context import AppContext

    AppContext._main_window = main_window
    return main_window


def install_handlers_and_tracers(project_dir, log_file):
    from utils.paint_event_supressor import PaintEventSuppressor
    from utils.call_tracer import CallTracer

    PaintEventSuppressor.install_message_handler()
    tracer = CallTracer(project_dir, log_file)
    sys.settrace(tracer.trace_calls)


def main():
    configure_import_paths()

    from PyQt6.QtCore import QTimer
    from main_window.main_widget.json_manager.json_manager import JsonManager
    from main_window.main_widget.json_manager.special_placement_saver import (
        SpecialPlacementSaver,
    )
    from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
    from splash_screen.splash_screen import SplashScreen
    from profiler import Profiler
    from settings_manager.settings_manager import SettingsManager

    print("Python version:", sys.version)
    print("Running main.py main()")
    print("Current working directory:", os.getcwd())

    project_dir = os.path.abspath(os.path.dirname(__file__))
    log_file = initialize_logging()

    app = initialize_application()

    settings_manager = SettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()

    profiler = Profiler()
    json_manager = JsonManager()
    special_placement_handler = SpecialPlacementSaver()
    special_placement_loader = SpecialPlacementLoader()

    initialize_context(
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader,
    )

    main_window = create_main_window(profiler, splash_screen)
    main_window.show()
    main_window.raise_()

    QTimer.singleShot(0, lambda: splash_screen.close())

    install_handlers_and_tracers(project_dir, log_file)

    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
