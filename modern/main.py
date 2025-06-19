#!/usr/bin/env python3
"""
Kinetic Constructor - Main Application Entry Point

Modern modular architecture with dependency injection and clean separation of concerns.
"""

import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QGuiApplication

# Qt Integration A+ Enhancements - Temporarily disabled due to import issues
# from core.qt_integration import (
#     qt_compat,
#     qt_factory,
#     qt_resources,
#     memory_detector,
#     AutoManagedWidget,
# )

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


from core.dependency_injection.di_container import get_container
from core.interfaces.core_services import (
    IUIStateManagementService,
    ILayoutService,
)

# Import for event system (with fallback for compatibility)
try:
    from core.events import IEventBus
except ImportError:
    IEventBus = None

# 🔥 CHANGED: Removed unused imports - services now imported locally where needed
from presentation.factories.workbench_factory import configure_workbench_services
from presentation.components.ui.splash_screen import SplashScreen
from presentation.components.backgrounds.background_widget import MainBackgroundWidget


class KineticConstructorModern(QMainWindow):
    def __init__(
        self,
        splash_screen: Optional[SplashScreen] = None,
        target_screen=None,
        parallel_mode=False,
        parallel_geometry=None,
        enable_api=True,
    ):
        super().__init__()
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry
        self.enable_api = enable_api

        if parallel_mode:
            self.setWindowTitle("TKA Modern - Parallel Testing")
        else:
            self.setWindowTitle("🚀 Kinetic Constructor")

        self.container = get_container()
        self._configure_services()
        self._set_window_dimensions()  # 🔥 CHANGED: Renamed from legacy method name
        self._setup_ui()
        self._setup_background()

        # Start API server if enabled
        if self.enable_api:
            self._start_api_server()

    def _configure_services(
        self,
    ):  # 🔥 CHANGED: Pure dependency injection - NO manual service creation
        """Configure services using PURE dependency injection patterns."""
        if self.splash:
            self.splash.update_progress(20, "Configuring services...")

        # Register event system and commands first
        self._register_event_system()

        # 🔥 CHANGED: Register service TYPES, not instances - let container handle creation
        self._register_core_services()

        # Register focused domain services
        self._register_motion_services()
        self._register_layout_services()
        self._register_pictograph_services()

        # Configure workbench services
        configure_workbench_services(self.container)

        if self.splash:
            self.splash.update_progress(40, "Services configured")

    def _register_event_system(self):
        """Register event system and command infrastructure."""
        try:
            from core.events import IEventBus, get_event_bus
            from core.commands import CommandProcessor

            # Get or create event bus
            event_bus = get_event_bus()
            self.container.register_instance(IEventBus, event_bus)

            # Register command processor
            command_processor = CommandProcessor(event_bus)
            self.container.register_instance(CommandProcessor, command_processor)

            if self.splash:
                self.splash.update_progress(25, "Event system registered")

        except ImportError as e:
            print(f"⚠️ Event system not available: {e}")
            # Continue without event system for backward compatibility

    def _register_core_services(self):  # 🔥 NEW: Pure DI service registration
        """Register core services using pure dependency injection."""
        from application.services.layout.layout_management_service import (
            LayoutManagementService,
        )
        from application.services.ui.ui_state_management_service import (
            UIStateManagementService,
        )

        # 🔥 CHANGED: Register service types with factory functions for proper DI
        def create_layout_service():
            event_bus = None
            if IEventBus and IEventBus in self.container._singletons:
                event_bus = self.container.resolve(IEventBus)
            return LayoutManagementService(event_bus=event_bus)

        def create_ui_state_service():
            return UIStateManagementService()

        # Register with factory functions for proper dependency resolution
        self.container.register_factory(ILayoutService, create_layout_service)
        self.container.register_factory(
            IUIStateManagementService, create_ui_state_service
        )

    def _register_motion_services(self):  # 🔥 CHANGED: Pure DI registration
        """Register the focused motion services using pure dependency injection."""
        from application.services.motion.motion_validation_service import (
            MotionValidationService,
            IMotionValidationService,
        )
        from application.services.motion.motion_orientation_service import (
            MotionOrientationService,
            IMotionOrientationService,
        )

        # 🔥 CHANGED: Register service types, not instances - pure DI
        self.container.register_singleton(
            IMotionValidationService, MotionValidationService
        )
        self.container.register_singleton(
            IMotionOrientationService, MotionOrientationService
        )

    def _register_layout_services(self):
        """Register the consolidated layout services."""
        # Note: Layout services have been consolidated into LayoutManagementService
        # which is already registered in _configure_services() as ILayoutService
        #
        # The old separate services (BeatLayoutService, ResponsiveLayoutService,
        # ComponentLayoutService) have been consolidated for better maintainability
        pass

    def _register_pictograph_services(self):  # 🔥 CHANGED: Pure DI registration
        """Register the focused pictograph services using pure dependency injection."""
        from application.services.data.pictograph_data_service import (
            PictographDataService,
            IPictographDataService,
        )
        from src.application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        # 🔥 CHANGED: Register service types, not instances - pure DI
        self.container.register_singleton(IPictographDataService, PictographDataService)
        self.container.register_singleton(
            PictographManagementService, PictographManagementService
        )

    def _set_window_dimensions(self):  # 🔥 CHANGED: Renamed from legacy method name
        """Set window dimensions using modern responsive design: 90% of screen size"""
        if self.splash:
            self.splash.update_progress(50, "Setting window dimensions...")

        # Check for parallel testing mode first
        if self.parallel_mode and self.parallel_geometry:
            try:
                x, y, width, height = map(int, self.parallel_geometry.split(","))
                self.setGeometry(x, y, width, height)
                self.setMinimumSize(1400, 900)
                print(f"🔄 Modern positioned at: {x},{y} ({width}x{height})")
                return
            except Exception as e:
                print(f"⚠️ Failed to apply parallel testing geometry: {e}")
                # Fall through to normal positioning

        # Use target screen for consistent positioning with splash
        screen = self.target_screen or QGuiApplication.primaryScreen()

        if not screen:
            self.setGeometry(100, 100, 1400, 900)
            self.setMinimumSize(1400, 900)
            return

        available_geometry = screen.availableGeometry()
        window_width = int(available_geometry.width() * 0.9)
        window_height = int(available_geometry.height() * 0.9)
        x = available_geometry.x() + int(
            (available_geometry.width() - window_width) / 2
        )
        y = available_geometry.y() + int(
            (available_geometry.height() - window_height) / 2
        )

        self.setGeometry(x, y, window_width, window_height)
        self.setMinimumSize(1400, 900)

    def _create_settings_button(self):  # 🔥 NEW: Pure DI component creation
        """Create settings button using dependency injection."""
        from presentation.components.ui.settings.settings_button import SettingsButton

        return SettingsButton()

    def _setup_ui(self):
        if self.splash:
            self.splash.update_progress(60, "Building user interface...")

        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and settings button (like legacy)
        header_layout = QHBoxLayout()

        title = QLabel("🚀 Kinetic Constructor")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin: 20px; background: transparent;")

        # 🔥 CHANGED: Use dependency injection for component creation
        self.settings_button = self._create_settings_button()
        self.settings_button.settings_requested.connect(self._show_settings)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)

        layout.addLayout(header_layout)

        if self.splash:
            self.splash.update_progress(70, "Creating tab interface...")

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setStyleSheet(
            """
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                padding: 8px 16px;
                margin: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-color: transparent;
            }
            QTabBar::tab:selected {
                background: rgba(255, 255, 255, 0.2);
                border-bottom-color: transparent;
            }
            QTabBar::tab:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """
        )
        layout.addWidget(self.tab_widget)

        if self.splash:
            self.splash.update_progress(75, "Initializing construct tab...")

        self._load_construct_tab_with_granular_progress()

        generate_placeholder = QLabel("🚧 Generator tab coming soon...")
        generate_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        generate_placeholder.setStyleSheet(
            "color: white; font-size: 14px; background: transparent;"
        )
        self.tab_widget.addTab(generate_placeholder, "⚡ Generate")

        browse_placeholder = QLabel("🚧 Browse tab coming soon...")
        browse_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        browse_placeholder.setStyleSheet(
            "color: white; font-size: 14px; background: transparent;"
        )
        self.tab_widget.addTab(browse_placeholder, "📚 Browse")

        if self.splash:
            self.splash.update_progress(95, "Finalizing interface...")

    def _load_construct_tab_with_granular_progress(self):
        """Load construct tab with granular progress updates"""
        try:
            # Step 1: Initialize container (76-78%)
            if self.splash:
                self.splash.update_progress(76, "Creating construct tab container...")

            # Basic container creation

            if self.splash:
                self.splash.update_progress(78, "Setting up dependency injection...")

            # Step 2: Initialize core services (78-82%)
            if self.splash:
                self.splash.update_progress(79, "Loading pictograph dataset...")

            # This is where the heavy loading happens - break it down
            from presentation.tabs.construct.construct_tab_widget import (
                ConstructTabWidget,
            )

            if self.splash:
                self.splash.update_progress(81, "Initializing position matching...")

            # Step 3: Create widget with progress callback (82-88%)
            if self.splash:
                self.splash.update_progress(83, "Creating option picker pool...")

            # Pass progress callback to construct tab
            def progress_callback(step: str, progress: float):
                if self.splash:
                    # Map internal progress (0.0-1.0) to our range (83-88%)
                    mapped_progress = 83 + (progress * 5)  # 5% range for internal steps
                    self.splash.update_progress(int(mapped_progress), step)

            if self.splash:
                self.splash.update_progress(85, "Setting up component layout...")

            self.construct_tab = ConstructTabWidget(
                self.container, progress_callback=progress_callback
            )

            if self.splash:
                self.splash.update_progress(88, "Configuring construct tab styling...")

            self.construct_tab.setStyleSheet("background: transparent;")

            if self.splash:
                self.splash.update_progress(90, "Adding construct tab to interface...")

            self.tab_widget.addTab(self.construct_tab, "🔧 Construct")

            if self.splash:
                self.splash.update_progress(92, "Construct tab loaded successfully!")

        except Exception as e:
            print(f"⚠️ Error loading construct tab: {e}")
            if self.splash:
                self.splash.update_progress(
                    85, "Construct tab load failed, using fallback..."
                )  # Create fallback placeholder
            fallback_placeholder = QLabel("🚧 Construct tab loading failed...")
            fallback_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_placeholder.setStyleSheet(
                "color: white; font-size: 14px; background: transparent;"
            )
            self.tab_widget.addTab(fallback_placeholder, "🔧 Construct")

    def _setup_background(self):  # 🔥 CHANGED: Use dependency injection
        """Setup background using dependency injection."""
        if self.splash:
            self.splash.update_progress(95, "Setting up background...")

        # 🔥 CHANGED: Use dependency injection instead of direct service access
        ui_state_service = self.container.resolve(IUIStateManagementService)
        background_type = ui_state_service.get_setting("background_type", "Aurora")

        self.background_widget = MainBackgroundWidget(self, background_type)
        self.background_widget.setGeometry(self.rect())
        self.background_widget.lower()
        self.background_widget.show()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if hasattr(self, "background_widget"):
            self.background_widget.setGeometry(self.rect())

    def _show_settings(self):  # 🔥 CHANGED: Use dependency injection
        """Open the settings dialog using dependency injection."""
        try:
            from src.presentation.components.ui.settings.modern_settings_dialog import (
                ModernSettingsDialog,
            )

            # 🔥 CHANGED: Use dependency injection instead of direct service access
            ui_state_service = self.container.resolve(IUIStateManagementService)
            dialog = ModernSettingsDialog(ui_state_service, self)

            # Connect to settings changes if needed
            dialog.settings_changed.connect(self._on_setting_changed)

            # Show the dialog
            _ = dialog.exec()

            # Clean up dialog resources after it closes
            dialog.deleteLater()

        except Exception as e:
            print(f"⚠️ Failed to open settings dialog: {e}")
            import traceback

            traceback.print_exc()

    def _on_setting_changed(self, key: str, value):
        """Handle settings changes from the dialog"""
        print(f"🔧 Setting changed: {key} = {value}")

        # Handle background changes
        if key == "background_type":
            self._apply_background_change(value)

    def _apply_background_change(self, background_type: str):
        """Apply a background change immediately"""
        try:
            # Remove old background widget with proper cleanup
            if hasattr(self, "background_widget") and self.background_widget:
                if hasattr(self.background_widget, "cleanup"):
                    self.background_widget.cleanup()
                self.background_widget.hide()
                self.background_widget.deleteLater()

            # Create new background widget
            self.background_widget = MainBackgroundWidget(self, background_type)
            self.background_widget.setGeometry(self.rect())
            self.background_widget.lower()
            self.background_widget.show()

            print(f"✅ Background changed to: {background_type}")

        except Exception as e:
            print(f"⚠️ Failed to change background: {e}")

    def _start_api_server(self):
        """Start the API server if dependencies are available."""
        if not self.enable_api:
            print("🚫 API server is disabled")
            return

        try:
            from src.infrastructure.api.api_integration import start_api_server
            import platform

            # Enhanced logging for Windows
            if platform.system() == "Windows":
                print("🪟 Starting API server on Windows...")
                print("   Note: Some ports may require administrator privileges")

            # Pass the enabled parameter to respect the configuration
            success = start_api_server(enabled=self.enable_api, auto_port=True)

            if success:
                print("🌐 TKA API server started successfully")
                from src.infrastructure.api.api_integration import get_api_integration

                api = get_api_integration()
                server_url = api.get_server_url()
                docs_url = api.get_docs_url()
                if server_url:
                    print(f"   📍 Server: {server_url}")
                if docs_url:
                    print(f"   📚 Docs: {docs_url}")
            else:
                print("⚠️ API server startup failed - continuing without API")
                print("   The main application will continue to work normally")

        except ImportError as e:
            print(f"⚠️ API server dependencies not available: {e}")
            print("   To enable API features: pip install fastapi uvicorn")
            print("   Continuing without API server...")
        except PermissionError as e:
            print(f"⚠️ Windows permission error for API server: {e}")
            print("   Possible solutions:")
            print("   1. Run as administrator")
            print("   2. Check Windows Firewall/Antivirus settings")
            print("   3. The application will continue without API server")
        except OSError as e:
            if "10013" in str(e):  # Windows socket permission error
                print(f"⚠️ Windows socket permission error: {e}")
                print("   This is a common Windows security restriction")
                print("   The application will continue without API server")
            else:
                print(f"⚠️ Network error starting API server: {e}")
                print("   Continuing without API server...")
        except Exception as e:
            print(f"⚠️ Unexpected error starting API server: {e}")
            print("   This does not affect the main application functionality")
            print("   Continuing without API server...")

        # Always continue with main application - API is optional
        print("✅ Main application startup continuing...")


def detect_parallel_testing_mode():
    """Detect if we're running in parallel testing mode."""
    import argparse
    import os

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
        print(f"🔄 Modern Parallel Testing Mode: {monitor} monitor")
        if env_geometry:
            print(f"   📐 Target geometry: {env_geometry}")

    return parallel_mode, monitor, env_geometry


def create_application():
    """Create Modern application for external use (like parallel testing)."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

    # Detect parallel testing mode
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()

    # Determine target screen
    screens = QGuiApplication.screens()
    if parallel_mode and monitor == "secondary" and len(screens) > 1:
        target_screen = screens[1]
    elif parallel_mode and monitor == "primary":
        target_screen = screens[0]
    else:
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    # Create window without splash for external use
    window = KineticConstructorModern(
        splash_screen=None,
        target_screen=target_screen,
        parallel_mode=parallel_mode,
        parallel_geometry=geometry,
    )

    return app, window


def main():
    print("🚀 Kinetic Constructor - Starting...")

    # A+ Enhancement: Qt Environment Detection and Optimization - Temporarily disabled
    # print("📋 Detecting Qt environment...")
    # compat_manager = qt_compat()
    # qt_env = compat_manager.get_environment()
    # print(f"   Detected: {qt_env.version} with {len(qt_env.features)} features")
    # print(f"   High DPI support: {qt_env.high_dpi_support}")
    # print(f"   OpenGL support: {qt_env.opengl_support}")

    # Start memory leak detection - Temporarily disabled
    # print("🔍 Starting memory leak detection...")
    # detector = memory_detector()
    # detector.start_monitoring()

    # Detect parallel testing mode early
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # A+ Enhancement: Apply Qt compatibility optimizations - Temporarily disabled
    # recommended_settings = compat_manager.get_recommended_settings()
    # if recommended_settings.get("high_dpi_scaling"):
    #     app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    #     print("✅ High DPI scaling enabled")

    # Determine target screen (dual monitor support)
    screens = QGuiApplication.screens()

    # Override screen selection for parallel testing
    if parallel_mode and len(screens) > 1:
        if monitor in ["secondary", "right"]:
            # Determine which screen is physically on the right
            primary_screen = screens[0]
            secondary_screen = screens[1]

            # If secondary has higher X coordinate, it's on the right
            if secondary_screen.geometry().x() > primary_screen.geometry().x():
                target_screen = secondary_screen
                print(
                    f"🔄 Modern forced to RIGHT monitor (secondary) for parallel testing"
                )
            else:
                target_screen = primary_screen
                print(
                    f"🔄 Modern forced to RIGHT monitor (primary) for parallel testing"
                )

        elif monitor in ["primary", "left"]:
            # Determine which screen is physically on the left
            primary_screen = screens[0]
            secondary_screen = screens[1]

            # If secondary has lower X coordinate, it's on the left
            if secondary_screen.geometry().x() < primary_screen.geometry().x():
                target_screen = secondary_screen
                print(
                    f"🔄 Modern forced to LEFT monitor (secondary) for parallel testing"
                )
            else:
                target_screen = primary_screen
                print(
                    f"🔄 Modern forced to LEFT monitor (primary) for parallel testing"
                )
        else:
            target_screen = screens[1]  # Default to secondary
    else:
        # Normal behavior: prefer secondary monitor if available
        target_screen = (
            screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()
        )

    # Create and show splash screen on target screen
    splash = SplashScreen(target_screen=target_screen)
    fade_in_animation = splash.show_animated()

    # Wait for fade-in to complete before starting app initialization
    def start_initialization():
        splash.update_progress(5, "Initializing application...")
        app.processEvents()

        # Set application icon if available
        icon_path = Path(__file__).parent / "images" / "icons" / "app_icon.png"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))

        splash.update_progress(15, "Creating main window...")
        window = KineticConstructorModern(
            splash_screen=splash,
            target_screen=target_screen,
            parallel_mode=parallel_mode,
            parallel_geometry=geometry,
        )

        def complete_startup():
            splash.update_progress(100, "Ready!")
            app.processEvents()

            # Hide splash immediately after reaching 100%
            QTimer.singleShot(200, lambda: splash.hide_animated())

            # Show main window after splash starts hiding
            QTimer.singleShot(300, lambda: window.show())

        QTimer.singleShot(
            200, complete_startup
        )  # Connect to fade-in completion to start initialization

    fade_in_animation.finished.connect(start_initialization)

    print("✅ Application started successfully!")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
