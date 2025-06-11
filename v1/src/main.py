import sys
import os
import logging


def configure_import_paths():
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", "")
        src_dir = os.path.join(base_dir, "src")
        if os.path.exists(src_dir) and src_dir not in sys.path:
            sys.path.insert(0, src_dir)
    else:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)


def initialize_logging():
    from src.utils.logging_config import configure_logging

    # Configure logging for DEBUG mode with full output
    configure_logging(logging.DEBUG)


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
        logger.info("Initializing dependency injection container...")

        # Configure the dependency injection container
        container = configure_dependencies()

        # Create application context with the container
        app_context = create_application_context(container)

        # CRITICAL: Set up legacy compatibility IMMEDIATELY after creating app_context
        # This must happen before any services are resolved to avoid circular dependency
        logger.info("Setting up legacy compatibility immediately...")
        setup_legacy_compatibility(app_context)
        logger.info("Legacy compatibility established during initialization")

        logger.info("Dependency injection system initialized successfully")
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
        from src.settings_manager.global_settings.app_context import AppContext
        from src.utils.logging_config import get_logger

        logger = get_logger(__name__)
        logger.info("Initializing legacy AppContext singleton...")

        # Get services from the new dependency injection system
        settings_manager = app_context.settings_manager
        json_manager = app_context.json_manager

        # Create special placement handler and loader directly
        # (Skip the fancy interface checking since those don't exist yet)
        logger.info("Creating special placement services...")

        try:
            from main_window.main_widget.json_manager.special_placement_saver import (
                SpecialPlacementSaver,
            )

            special_placement_handler = SpecialPlacementSaver()
            logger.info("Created SpecialPlacementSaver successfully")
        except ImportError as e:
            logger.warning(f"Could not import SpecialPlacementSaver: {e}")
            special_placement_handler = None

        try:
            from main_window.main_widget.special_placement_loader import (
                SpecialPlacementLoader,
            )

            special_placement_loader = SpecialPlacementLoader()
            logger.info("Created SpecialPlacementLoader successfully")
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

        logger.info("Legacy AppContext singleton initialized successfully")

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
        logger.info("Creating MainWindow with dependency injection...")

        # Create the main window with dependency injection
        main_window = MainWindow(profiler, splash_screen, app_context)

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
    initialize_logging()

    from src.splash_screen.splash_screen import SplashScreen
    from src.profiler import Profiler
    from src.settings_manager.settings_manager import SettingsManager
    from src.utils.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info(f"Kinetic Constructor v1.0.0")
    logger.info(f"Python {sys.version.split()[0]}")

    app = initialize_application()
    settings_manager = SettingsManager()

    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()

    splash_screen.updater.start_phase("pre_initialization", 1, "Starting...")

    logger.info("Pre-initializing Browse Tab v2 performance systems...")
    try:
        from src.browse_tab.startup.performance_preinitialization import (
            initialize_browse_tab_performance_systems,
        )

        def performance_progress_callback(step_increment: int, message: str):
            splash_screen.updater.update_phase_progress(step_increment, message)

        preinitialization_results = initialize_browse_tab_performance_systems(
            progress_callback=performance_progress_callback
        )

        if preinitialization_results["overall_success"]:
            logger.info(
                f"✅ Browse Tab v2 pre-initialization successful in {preinitialization_results['overall_duration_ms']:.1f}ms"
            )
        else:
            logger.warning(f"⚠️ Browse Tab v2 pre-initialization partially failed")
    except Exception as e:
        logger.error(f"❌ Browse Tab v2 pre-initialization failed: {e}")

    logger.info("Starting optimized startup preloading...")
    splash_screen.updater.start_phase("optimized_startup", 10, "Loading...")

    try:
        import asyncio
        from src.browse_tab.startup.optimized_startup_preloader import (
            OptimizedStartupPreloader,
        )

        preloader = OptimizedStartupPreloader(silent_mode=False)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            data_preloading_results = loop.run_until_complete(
                preloader.preload_for_instant_startup()
            )

            if data_preloading_results["overall_success"]:
                logger.info(
                    f"✅ Optimized startup completed in {data_preloading_results['overall_duration_ms']:.1f}ms"
                )
                logger.info(
                    f"   Ready: {data_preloading_results['total_sequences']} sequences, {data_preloading_results['preloaded_thumbnails']} thumbnails"
                )
            else:
                logger.warning(f"⚠️ Optimized startup partially failed")
        finally:
            logger.info("Event loop kept alive for browse tab async operations")
    except Exception as e:
        logger.error(f"❌ Optimized startup preloading failed: {e}")

    logger.info("Starting dependency injection initialization...")
    splash_screen.updater.start_phase("dependency_injection", 3, "Initializing...")
    app_context = initialize_dependency_injection()
    splash_screen.updater.update_phase_progress(1, "Dependency injection ready")
    logger.info("Dependency injection initialization completed")

    logger.info("Initializing legacy AppContext singleton...")
    initialize_legacy_appcontext(app_context)
    splash_screen.updater.update_phase_progress(1, "Legacy AppContext ready")
    logger.info("Legacy AppContext initialization completed")

    logger.info("Starting MainWindow creation...")
    splash_screen.updater.start_phase(
        "main_window_creation", 2, "Creating interface..."
    )
    profiler = Profiler()
    main_window = create_main_window(profiler, splash_screen, app_context)
    splash_screen.updater.complete_phase("Main window created")
    logger.info("MainWindow creation completed")

    logger.info("Starting widget initialization...")
    splash_screen.updater.start_phase("widget_initialization", 8, "Finalizing...")
    main_window.initialize_widgets()
    splash_screen.updater.complete_phase("Widget initialization completed")
    logger.info("Widget initialization completed")

    logger.info("Showing main window...")
    splash_screen.updater.start_phase("finalization", 3, "Ready!")
    main_window.show()
    main_window.raise_()
    logger.info("Main window shown successfully")

    install_handlers()
    splash_screen.close()
    logger.info("Starting application event loop...")

    exit_code = main_window.exec(app)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
