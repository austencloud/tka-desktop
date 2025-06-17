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

modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


from core.dependency_injection.di_container import get_container
from core.interfaces.core_services import (
    ILayoutManagementService,
    IUIStateManagementService,
    ILayoutService,
)
from application.services.layout.layout_management_service import (
    LayoutManagementService,
)
from application.services.ui.ui_state_management_service import (
    UIStateManagementService,
)
from presentation.components.ui.settings.settings_button import SettingsButton
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
    ):
        super().__init__()
        self.splash = splash_screen
        self.target_screen = target_screen
        self.parallel_mode = parallel_mode
        self.parallel_geometry = parallel_geometry

        if parallel_mode:
            self.setWindowTitle("TKA Modern - Parallel Testing")
        else:
            self.setWindowTitle("🚀 Kinetic Constructor")

        self.container = get_container()
        self._configure_services()
        self._set_legacy_style_dimensions()
        self._setup_ui()
        self._setup_background()

    def _configure_services(self):
        if self.splash:
            self.splash.update_progress(20, "Configuring services...")

        # Register consolidated services
        layout_management_service = LayoutManagementService()
        self.container.register_instance(
            ILayoutManagementService, layout_management_service
        )  # Register the same service instance for ILayoutService interface
        self.container.register_instance(
            ILayoutService, layout_management_service
        )  # Register UI state management service as instance to ensure immediate availability
        ui_state_service = UIStateManagementService()
        self.container.register_instance(IUIStateManagementService, ui_state_service)

        # Register new focused motion services
        self._register_motion_services()

        # Register new focused layout services
        self._register_layout_services()

        # Register new focused pictograph services
        self._register_pictograph_services()  # Get UI state service for settings functionality
        self.ui_state_service = self.container.resolve(IUIStateManagementService)

        # Configure workbench services after UI state service is available
        configure_workbench_services(self.container)

        if self.splash:
            self.splash.update_progress(40, "Services configured")

    def _register_motion_services(self):
        """Register the new focused motion services."""
        from application.services.motion.motion_validation_service import (
            MotionValidationService,
            IMotionValidationService,
        )
        from application.services.motion.motion_generation_service import (
            MotionGenerationService,
            IMotionGenerationService,
        )
        from application.services.motion.motion_orientation_service import (
            MotionOrientationService,
            IMotionOrientationService,
        )

        # Register focused motion services
        validation_service = MotionValidationService()
        self.container.register_instance(IMotionValidationService, validation_service)

        generation_service = MotionGenerationService(
            validation_service=validation_service
        )
        self.container.register_instance(IMotionGenerationService, generation_service)

        orientation_service = MotionOrientationService()
        self.container.register_instance(IMotionOrientationService, orientation_service)

        # Register bridge service for backward compatibility
        from application.services.motion.motion_management_bridge_service import (
            MotionManagementBridgeService,
        )
        from core.interfaces.core_services import IMotionManagementService

        bridge_service = MotionManagementBridgeService(
            validation_service, generation_service, orientation_service
        )
        self.container.register_instance(IMotionManagementService, bridge_service)

    def _register_layout_services(self):
        """Register the new focused layout services."""
        from application.services.layout.beat_layout_service import (
            BeatLayoutService,
            IBeatLayoutService,
        )
        from application.services.layout.responsive_layout_service import (
            ResponsiveLayoutService,
            IResponsiveLayoutService,
        )
        from application.services.layout.component_layout_service import (
            ComponentLayoutService,
            IComponentLayoutService,
        )

        # Register focused layout services
        beat_layout_service = BeatLayoutService()
        self.container.register_instance(IBeatLayoutService, beat_layout_service)

        responsive_layout_service = ResponsiveLayoutService()
        self.container.register_instance(
            IResponsiveLayoutService, responsive_layout_service
        )

        component_layout_service = ComponentLayoutService()
        self.container.register_instance(
            IComponentLayoutService, component_layout_service
        )

        # Note: ILayoutManagementService is already registered in _configure_services()
        # with the consolidated LayoutManagementService that also implements ILayoutService

    def _register_pictograph_services(self):
        """Register the new focused pictograph services."""
        from application.services.data.pictograph_data_service import (
            PictographDataService,
            IPictographDataService,
        )

        # Data conversion is now part of PictographManagementService
        # from application.services.data_conversion_service import (        #     DataConversionService,
        #     IDataConversionService,
        # )

        # Register focused pictograph services
        data_service = PictographDataService()
        self.container.register_instance(IPictographDataService, data_service)

        # Data conversion is now part of PictographManagementService
        # conversion_service = DataConversionService()
        # self.container.register_instance(IDataConversionService, conversion_service)

        # Register pictograph management service directly
        from src.application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        pictograph_management_service = PictographManagementService()
        # Note: PictographManagementService doesn't have an interface yet, so we register the concrete class
        self.container.register_instance(
            PictographManagementService, pictograph_management_service
        )

    def _set_legacy_style_dimensions(self):
        """Set window dimensions to match legacy: 90% of screen size"""
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

        # Settings button positioned in top-right like legacy
        self.settings_button = SettingsButton()
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
            from core.dependency_injection.di_container import DIContainer

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

    def _setup_background(self):
        if self.splash:
            self.splash.update_progress(95, "Setting up background...")
        
        # Get background type from settings
        background_type = self.ui_state_service.get_setting("background_type", "Aurora")
        
        self.background_widget = MainBackgroundWidget(self, background_type)
        self.background_widget.setGeometry(self.rect())
        self.background_widget.lower()
        self.background_widget.show()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if hasattr(self, "background_widget"):
            self.background_widget.setGeometry(self.rect())

    def _show_settings(self):
        """Open the settings dialog"""
        try:
            # Create the settings service
            from src.application.services.settings.settings_service import (
                SettingsService,
            )
            from src.presentation.components.ui.settings.modern_settings_dialog import (
                ModernSettingsDialog,
            )

            settings_service = SettingsService(self.ui_state_service)

            # Create and show the settings dialog
            dialog = ModernSettingsDialog(settings_service, self)

            # Connect to settings changes if needed
            dialog.settings_changed.connect(self._on_setting_changed)

            # Show the dialog
            result = dialog.exec()

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
            # Remove old background widget
            if hasattr(self, "background_widget") and self.background_widget:
                self.background_widget.hide()
                self.background_widget.deleteLater()            # Create new background widget
            self.background_widget = MainBackgroundWidget(self, background_type)
            self.background_widget.setGeometry(self.rect())
            self.background_widget.lower()
            self.background_widget.show()

            print(f"✅ Background changed to: {background_type}")

        except Exception as e:
            print(f"⚠️ Failed to change background: {e}")


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

    # Detect parallel testing mode early
    parallel_mode, monitor, geometry = detect_parallel_testing_mode()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

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
