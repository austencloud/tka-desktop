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
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Add the src directory to Python path for clean relative imports
        src_dir = os.path.join(current_dir, "src")
        if os.path.exists(src_dir) and src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        # Add the root directory to Python path for data imports
        root_dir = os.path.join(current_dir, "..")
        if os.path.exists(root_dir) and root_dir not in sys.path:
            sys.path.insert(0, root_dir)


def initialize_logging():
    from src.utils.logging_config import configure_logging

    # Configure the logging system with WARNING level to reduce startup noise
    configure_logging(logging.WARNING)


def initialize_application():
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    return app


def initialize_dependency_injection():
    """Initialize the modern dependency injection system.

    This replaces the old AppContext singleton with proper dependency injection.
    """
    try:
        from src.core.dependency_container import configure_dependencies
        from src.core.application_context import create_application_context
        from src.core.migration_adapters import setup_legacy_compatibility
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)

        # Configure the dependency injection container
        container = configure_dependencies()

        # Create application context with the container
        app_context = create_application_context(container)

        # CRITICAL: Set up legacy compatibility IMMEDIATELY after creating app_context
        # This must happen before any services are resolved to avoid circular dependency
        setup_legacy_compatibility(app_context)

        return app_context

    except ImportError as e:
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.error(f"Error initializing dependency injection: {e}")
        raise


def initialize_legacy_appcontext(app_context):
    """Initialize the legacy AppContext singleton with services from dependency injection.

    This bridges the gap between the new DI system and legacy code that still uses AppContext.
    """
    try:
        from src.legacy_settings_manager.global_settings.app_context import AppContext
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)

        # Get services from the new dependency injection system
        settings_manager = app_context.settings_manager
        json_manager = app_context.json_manager

        # Create special placement handler and loader directly
        try:
            from main_window.main_widget.json_manager.special_placement_saver import (
                SpecialPlacementSaver,
            )

            special_placement_handler = SpecialPlacementSaver()
        except ImportError as e:
            logger.warning(f"Could not import SpecialPlacementSaver: {e}")
            special_placement_handler = None

        try:
            from main_window.main_widget.special_placement_loader import (
                SpecialPlacementLoader,
            )

            special_placement_loader = SpecialPlacementLoader()
        except ImportError as e:
            logger.warning(f"Could not import SpecialPlacementLoader: {e}")
            special_placement_loader = None

        # Initialize the legacy AppContext
        AppContext.init(
            settings_manager=settings_manager,
            json_manager=json_manager,
            special_placement_handler=special_placement_handler,
            special_placement_loader=special_placement_loader,
        )

    except Exception as e:
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.error(f"Failed to initialize legacy AppContext: {e}")
        logger.error("This will cause issues with widgets that still use AppContext")
        # Don't raise - let the app continue, some things might still work


def create_main_window(profiler, splash_screen, app_context):
    """Create the main window with dependency injection.

    This function creates the MainWindow using the new dependency injection system.
    """
    try:
        from src.main_window.main_window import MainWindow
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)

        # Create the main window with dependency injection
        main_window = MainWindow(profiler, splash_screen, app_context)

        return main_window

    except ImportError as e:
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.error(f"Error importing in create_main_window: {e}")
        raise


def install_handlers():
    from src.utils.paint_event_supressor import PaintEventSuppressor
    from PyQt6.QtCore import qInstallMessageHandler, QtMsgType

    # Install paint event suppressor
    PaintEventSuppressor.install_message_handler()

    # Install Qt message handler to suppress Qt warnings
    def qt_message_handler(msg_type, context, message):
        # Suppress "Unknown property" warnings completely
        if "unknown property" in message.lower() or "transform" in message.lower():
            return

        # Suppress other Qt noise during startup
        noise_patterns = ["qml", "opengl", "shader", "texture"]

        if any(pattern in message.lower() for pattern in noise_patterns):
            return

        # Only show critical Qt errors
        if msg_type == QtMsgType.QtCriticalMsg or msg_type == QtMsgType.QtFatalMsg:
            print(f"Qt {msg_type.name}: {message}")

    qInstallMessageHandler(qt_message_handler)


def detect_parallel_testing_mode():
    """Detect if we're running in parallel testing mode."""
    import argparse

    # Check command line arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--parallel-testing", action="store_true")
    parser.add_argument("--monitor", choices=["primary", "secondary", "left", "right"])
    args, _ = parser.parse_known_args()

    # Check environment variable
    env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
    env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
    env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

    parallel_mode = args.parallel_testing or env_parallel
    monitor = args.monitor or env_monitor

    if parallel_mode:
        print(f"🔄 Legacy Parallel Testing Mode: {monitor} monitor")
        if env_geometry:
            print(f"   📐 Target geometry: {env_geometry}")

    return parallel_mode, monitor, env_geometry


def main():
    configure_import_paths()

    from PyQt6.QtCore import QTimer
    from src.splash_screen.splash_screen import SplashScreen
    from src.profiler import Profiler
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager
    from src.utils.logging_config import get_logger
    from src.utils.startup_silencer import silence_startup_logs

    # Detect parallel testing mode early
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()

    # Get a logger for the main module
    logger = get_logger(__name__)

    # Log minimal startup information
    logger.info(f"Kinetic Constructor legacy.0.0")
    logger.info(f"Python {sys.version.split()[0]}")

    if parallel_mode:
        logger.info(f"Parallel testing mode: {monitor} monitor")

    # Use the startup silencer to reduce noise during initialization
    with silence_startup_logs():
        pass

    # Initialize logging without creating log files
    initialize_logging()

    app = initialize_application()

    settings_manager = LegacySettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()

    profiler = Profiler()

    # Initialize dependency injection and legacy compatibility
    app_context = initialize_dependency_injection()
    initialize_legacy_appcontext(app_context)

    # Create and initialize main window
    main_window = create_main_window(profiler, splash_screen, app_context)
    main_window.initialize_widgets()

    # Apply parallel testing positioning if enabled
    if parallel_mode and geometry:
        try:
            x, y, width, height = map(int, geometry.split(","))
            main_window.setGeometry(x, y, width, height)
            main_window.setWindowTitle("TKA Legacy - Parallel Testing")
            print(f"🔄 Legacy positioned at: {x},{y} ({width}x{height})")
        except Exception as e:
            logger.warning(f"Failed to apply parallel testing geometry: {e}")

    try:
        main_window.show()
        main_window.raise_()

        QTimer.singleShot(0, lambda: splash_screen.close())

        # Install message handlers
        install_handlers()

        exit_code = main_window.exec(app)
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Error showing main window: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
