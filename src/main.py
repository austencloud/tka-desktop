import sys
import os
import logging


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
    from utils.logging_config import configure_logging, get_logger

    # Configure the logging system with INFO level by default
    configure_logging(logging.INFO)

    # Get a logger for the main module
    main_logger = get_logger(__name__)

    # Create a simple trace log file for compatibility with existing code
    trace_log_path = os.path.join(os.getcwd(), "trace_log.txt")
    os.makedirs(os.path.dirname(trace_log_path), exist_ok=True)

    main_logger.debug("Trace log initialized at: %s", trace_log_path)
    return open(trace_log_path, "w")


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
    from utils.logging_config import get_logger
    from utils.startup_silencer import silence_startup_logs

    # Get a logger for the main module
    logger = get_logger(__name__)

    # Log minimal startup information
    logger.info(f"Kinetic Constructor v1.0.0")
    logger.info(f"Python {sys.version.split()[0]}")

    # Use the startup silencer to reduce noise during initialization
    with silence_startup_logs():
        # These detailed logs will only go to the log file, not the console
        detailed_logger = get_logger("startup_details")
        detailed_logger.info(f"Full Python version: {sys.version}")
        detailed_logger.info(f"Current working directory: {os.getcwd()}")

        # Log system information to the log file
        import platform

        detailed_logger.info(f"Platform: {platform.platform()}")
        detailed_logger.info(f"Processor: {platform.processor()}")
        detailed_logger.info(
            f"Python implementation: {platform.python_implementation()}"
        )
        detailed_logger.info(f"Python compiler: {platform.python_compiler()}")

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
