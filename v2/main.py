#!/usr/bin/env python3
"""
Kinetic Constructor v2 - Main Application Entry Point

Modern modular architecture with dependency injection and clean separation of concerns.
"""

import sys
from pathlib import Path
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

v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from src.core.dependency_injection.simple_container import get_container
from src.core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from src.application.services.simple_layout_service import SimpleLayoutService
from src.application.services.simple_sequence_service import (
    SequenceService,
    SimpleSequenceDataService,
    SimpleSettingsService,
    SimpleValidationService,
)
from src.application.services.settings_service import SettingsService
from src.application.services.settings_dialog_service import SettingsDialogService
from src.core.interfaces.settings_interfaces import (
    ISettingsService as IModernSettingsService,
    ISettingsDialogService,
)
from src.presentation.components.ui.settings.settings_button import SettingsButton
from src.presentation.factories.workbench_factory import configure_workbench_services
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.presentation.widgets.background_widget import MainBackgroundWidget
from src.presentation.widgets.splash_screen import SplashScreen


class KineticConstructorV2(QMainWindow):
    def __init__(self, splash_screen=None, target_screen=None):
        super().__init__()
        self.splash = splash_screen
        self.target_screen = target_screen
        self.setWindowTitle("🚀 Kinetic Constructor v2")

        self.container = get_container()
        self._configure_services()
        self._set_v1_style_dimensions()
        self._setup_ui()
        self._setup_background()

    def _configure_services(self):
        if self.splash:
            self.splash.update_progress(20, "Configuring services...")

        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        self.container.register_singleton(ISettingsService, SimpleSettingsService)
        self.container.register_singleton(
            ISequenceDataService, SimpleSequenceDataService
        )
        self.container.register_singleton(IValidationService, SimpleValidationService)
        self.container.register_singleton(SequenceService, SequenceService)

        # Register modern settings services
        self.container.register_singleton(IModernSettingsService, SettingsService)

        # Initialize settings dialog service
        settings_service = self.container.resolve(IModernSettingsService)
        self.settings_dialog_service = SettingsDialogService(settings_service, self)

        configure_workbench_services(self.container)

        if self.splash:
            self.splash.update_progress(40, "Services configured")

    def _set_v1_style_dimensions(self):
        """Set window dimensions to match v1: 90% of screen size"""
        if self.splash:
            self.splash.update_progress(50, "Setting window dimensions...")

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

        # Header with title and settings button (like v1)
        header_layout = QHBoxLayout()

        title = QLabel("🚀 Kinetic Constructor v2")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin: 20px; background: transparent;")

        # Settings button positioned in top-right like v1
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
            from src.core.dependency_injection.simple_container import SimpleContainer

            if self.splash:
                self.splash.update_progress(78, "Setting up dependency injection...")

            # Step 2: Initialize core services (78-82%)
            if self.splash:
                self.splash.update_progress(79, "Loading pictograph dataset...")

            # This is where the heavy loading happens - break it down
            from src.presentation.tabs.construct_tab_widget import ConstructTabWidget

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
                )

            # Create fallback placeholder
            fallback_placeholder = QLabel("🚧 Construct tab loading failed...")
            fallback_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_placeholder.setStyleSheet(
                "color: white; font-size: 14px; background: transparent;"
            )
            self.tab_widget.addTab(fallback_placeholder, "🔧 Construct")

    def _setup_background(self):
        if self.splash:
            self.splash.update_progress(95, "Setting up background...")

        self.background_widget = MainBackgroundWidget(self, "Starfield")
        self.background_widget.lower()
        self.background_widget.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "background_widget"):
            self.background_widget.setGeometry(self.rect())

    def _show_settings(self):
        """Open the settings dialog"""
        self.settings_dialog_service.show_settings_dialog()


def main():
    print("🚀 Kinetic Constructor v2 - Starting...")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Determine target screen (dual monitor support)
    screens = QGuiApplication.screens()
    target_screen = screens[1] if len(screens) > 1 else QGuiApplication.primaryScreen()

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
        window = KineticConstructorV2(splash_screen=splash, target_screen=target_screen)

        def complete_startup():
            splash.update_progress(100, "Ready!")
            app.processEvents()

            # Hide splash immediately after reaching 100%
            QTimer.singleShot(200, lambda: splash.hide_animated())

            # Show main window after splash starts hiding
            QTimer.singleShot(300, lambda: window.show())

        QTimer.singleShot(200, complete_startup)

    # Connect to fade-in completion to start initialization
    fade_in_animation.finished.connect(start_initialization)

    print("✅ Application started successfully!")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
