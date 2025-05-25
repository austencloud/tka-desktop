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
    from src.utils.logging_config import configure_logging

    # Configure the logging system with INFO level by default
    configure_logging(logging.INFO)


def initialize_application():
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    return app


def initialize_context(
    settings_manager, json_manager, special_placement_handler, special_placement_loader
):
    """Initialize the AppContext with required dependencies.

    This function ensures that the AppContext is properly initialized before
    any components try to access it.
    """
    try:
        # Use a consistent import path - always use the src-prefixed version
        from src.settings_manager.global_settings.app_context import AppContext
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.info("Initializing AppContext...")

        # Initialize the AppContext
        AppContext.init(
            settings_manager,
            json_manager,
            special_placement_handler,
            special_placement_loader=special_placement_loader,
        )

        # Verify initialization worked
        if AppContext._settings_manager is None:
            logger.error(
                "AppContext initialization failed! _settings_manager is still None"
            )
            raise RuntimeError("AppContext initialization failed")
        else:
            logger.info("AppContext initialized successfully")

    except ImportError as e:
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.error(f"Error importing AppContext: {e}")
        raise


def create_main_window(profiler, splash_screen):
    """Create the main window after AppContext is initialized.

    This function ensures that the AppContext is properly initialized before
    creating the MainWindow.
    """
    try:
        # Use a consistent import path - always use the src-prefixed version
        from src.settings_manager.global_settings.app_context import AppContext
        from src.main_window.main_window import MainWindow
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.info("Creating MainWindow...")

        # Verify AppContext is initialized before creating MainWindow
        if AppContext._settings_manager is None:
            logger.error("AppContext not initialized before creating MainWindow!")
            raise RuntimeError("AppContext not initialized before creating MainWindow")

        # Create the main window
        main_window = MainWindow(profiler, splash_screen)

        # Set the main window in AppContext
        AppContext._main_window = main_window
        logger.info("MainWindow created successfully")

        return main_window
    except ImportError as e:
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.error(f"Error importing in create_main_window: {e}")
        raise


def install_handlers():
    from src.utils.paint_event_supressor import PaintEventSuppressor

    # Only install the paint event suppressor, no more call tracing
    PaintEventSuppressor.install_message_handler()


def main():
    configure_import_paths()

    from PyQt6.QtCore import QTimer
    from src.main_window.main_widget.json_manager.json_manager import JsonManager
    from src.main_window.main_widget.json_manager.special_placement_saver import (
        SpecialPlacementSaver,
    )
    from src.main_window.main_widget.special_placement_loader import (
        SpecialPlacementLoader,
    )
    from src.splash_screen.splash_screen import SplashScreen
    from src.profiler import Profiler
    from src.settings_manager.settings_manager import SettingsManager
    from src.utils.logging_config import get_logger
    from src.utils.startup_silencer import silence_startup_logs

    # Get a logger for the main module
    logger = get_logger(__name__)

    # Log minimal startup information
    logger.info(f"Kinetic Constructor v1.0.0")
    logger.info(f"Python {sys.version.split()[0]}")

    # Use the startup silencer to reduce noise during initialization
    with silence_startup_logs():
        pass

    # Initialize logging without creating log files
    initialize_logging()

    app = initialize_application()

    settings_manager = SettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()

    profiler = Profiler()
    json_manager = JsonManager()
    special_placement_handler = SpecialPlacementSaver()
    special_placement_loader = SpecialPlacementLoader()

    # Initialize the AppContext before creating the main window
    # This ensures that AppContext.settings_manager() is available when MainWindow is constructed
    logger.info("Starting AppContext initialization...")
    initialize_context(
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader,
    )
    logger.info("AppContext initialization completed")

    # Now create the main window after AppContext is initialized
    logger.info("Starting MainWindow creation...")
    main_window = create_main_window(profiler, splash_screen)
    logger.info("MainWindow creation completed")

    main_window.show()
    main_window.raise_()

    QTimer.singleShot(0, lambda: splash_screen.close())

    # Install message handlers (no more tracing)
    install_handlers()

    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
