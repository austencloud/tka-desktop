"""
Base class for standalone tab runners.

This provides the common infrastructure needed to run any tab as a standalone application.
"""

import sys
import os
import logging
from typing import TYPE_CHECKING, Optional, Type
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from core.application_context import ApplicationContext


class StandaloneTabWindow(QMainWindow):
    """Main window for standalone tab applications."""

    def __init__(self, tab_widget: QWidget, tab_name: str, coordinator=None):
        super().__init__()
        self.tab_widget = tab_widget
        self.tab_name = tab_name
        self.coordinator = coordinator

        self.setWindowTitle(f"Kinetic Constructor - {tab_name.title()}")

        # Create the proper layout for the tab
        self._setup_tab_layout()

        # Set reasonable default size
        self.resize(1400, 900)  # Larger for construct tab layout

        # Configure window attributes
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Set main_window reference on coordinator for full screen viewer
        if self.coordinator:
            self.coordinator.main_window = self

    def _setup_tab_layout(self):
        """Set up the proper layout for different tab types."""
        if self.tab_name == "construct":
            self._setup_construct_tab_layout()
        else:
            # For other tabs, use simple central widget
            self.setCentralWidget(self.tab_widget)

    def _setup_construct_tab_layout(self):
        """Set up the construct tab with proper left/right layout."""
        from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Get sequence workbench from coordinator
        sequence_workbench = None
        if self.coordinator and hasattr(self.coordinator, "widget_manager"):
            sequence_workbench = self.coordinator.widget_manager.get_widget(
                "sequence_workbench"
            )

        if sequence_workbench:
            # Left side: Sequence workbench (1:1 ratio with picker)
            main_layout.addWidget(sequence_workbench, 1)

        # Right side: Stacked widget for construct tab components (1:1 ratio with workbench)
        right_stack = QStackedWidget()

        # Add construct tab components to right stack
        if hasattr(self.tab_widget, "start_pos_picker"):
            right_stack.addWidget(self.tab_widget.start_pos_picker)  # Index 0
        if hasattr(self.tab_widget, "advanced_start_pos_picker"):
            right_stack.addWidget(self.tab_widget.advanced_start_pos_picker)  # Index 1
        if hasattr(self.tab_widget, "option_picker"):
            right_stack.addWidget(self.tab_widget.option_picker)  # Index 2

        # Start with the start position picker
        right_stack.setCurrentIndex(0)

        main_layout.addWidget(right_stack, 1)

        # Store reference to right stack for fade functionality
        if self.coordinator:
            self.coordinator.right_stack = right_stack

        self.setCentralWidget(main_widget)


class BaseStandaloneRunner:
    """
    Base class for running individual tabs as standalone applications.

    This handles the common setup needed for any tab to run independently:
    - Application initialization
    - Dependency injection setup
    - Tab creation and display
    """

    def __init__(self, tab_name: str, tab_factory_class: Type):
        self.tab_name = tab_name
        self.tab_factory_class = tab_factory_class
        self.app: Optional[QApplication] = None
        self.app_context: Optional["ApplicationContext"] = None
        self.main_window: Optional[StandaloneTabWindow] = None

    def configure_import_paths(self):
        """Configure Python import paths for standalone execution."""
        if getattr(sys, "frozen", False):
            base_dir = sys._MEIPASS
            src_dir = os.path.join(base_dir, "src")
            if os.path.exists(src_dir) and src_dir not in sys.path:
                sys.path.insert(0, src_dir)
        else:
            # Get the project root (4 levels up from this file)
            project_dir = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            )

            # Add src directory first (this is where our modules are)
            src_dir = os.path.join(project_dir, "src")
            if os.path.exists(src_dir) and src_dir not in sys.path:
                sys.path.insert(0, src_dir)

            # Also add project root for any top-level imports
            if project_dir not in sys.path:
                sys.path.insert(0, project_dir)

    def initialize_logging(self):
        """Initialize logging for standalone execution."""
        from utils.logging_config import configure_logging

        configure_logging(logging.INFO)

    def initialize_application(self) -> QApplication:
        """Initialize the Qt application."""
        app = QApplication(sys.argv)
        QApplication.setStyle("Fusion")
        return app

    def initialize_dependency_injection(self) -> "ApplicationContext":
        """Initialize dependency injection system."""
        from core.dependency_container import configure_dependencies
        from core.application_context import create_application_context
        from core.migration_adapters import setup_legacy_compatibility

        # Configure the dependency injection container
        container = configure_dependencies()

        # Create application context
        app_context = create_application_context(container)

        # Set up legacy compatibility
        setup_legacy_compatibility(app_context)

        # CRITICAL: Also initialize the legacy AppContext singleton
        self._initialize_legacy_appcontext(app_context)

        return app_context

    def _initialize_legacy_appcontext(self, app_context):
        """Initialize the legacy AppContext singleton for backward compatibility."""
        try:
            from src.settings_manager.global_settings.app_context import AppContext

            # Get services from the new dependency injection system
            settings_manager = app_context.settings_manager
            json_manager = app_context.json_manager

            # Create special placement handler and loader (needed for pictographs)
            print("Creating special placement services...")

            try:
                from main_window.main_widget.json_manager.special_placement_saver import (
                    SpecialPlacementSaver,
                )

                special_placement_handler = SpecialPlacementSaver()
                print("Created SpecialPlacementSaver successfully")
            except ImportError as e:
                print(f"Warning: Could not import SpecialPlacementSaver: {e}")
                special_placement_handler = None

            try:
                from main_window.main_widget.special_placement_loader import (
                    SpecialPlacementLoader,
                )

                special_placement_loader = SpecialPlacementLoader()
                print("Created SpecialPlacementLoader successfully")
            except ImportError as e:
                print(f"Warning: Could not import SpecialPlacementLoader: {e}")
                special_placement_loader = None

            # Initialize the legacy AppContext
            AppContext.init(
                settings_manager=settings_manager,
                json_manager=json_manager,
                special_placement_handler=special_placement_handler,
                special_placement_loader=special_placement_loader,
            )

            print("Legacy AppContext initialized successfully")

        except Exception as e:
            print(f"Warning: Could not initialize legacy AppContext: {e}")
            # Continue anyway - some tabs might still work

    def create_minimal_coordinator(self) -> QWidget:
        """
        Create a minimal coordinator that provides the interface expected by tab factories.

        This is a lightweight version that only provides what's needed for the specific tab.
        """
        from PyQt6.QtCore import QSize

        # Create a simple widget that can act as a parent
        coordinator = QWidget()
        coordinator.app_context = self.app_context

        # Add size method that tabs expect
        coordinator.size = lambda: QSize(1200, 800)  # Default reasonable size

        # Add splash screen placeholder (some factories expect this)
        coordinator.splash_screen = self._create_minimal_splash_screen()

        # Create minimal widget manager that provides required widgets
        coordinator.widget_manager = self._create_minimal_widget_manager(coordinator)

        # Add stack placeholders (needed by sequence workbench)
        coordinator.right_stack = None
        coordinator.left_stack = self._create_minimal_left_stack()

        # Add fade functionality for construct tab
        coordinator.fade_to_stack_index = self._create_fade_function(coordinator)

        # Add tab manager for construct tab access
        coordinator.tab_manager = self._create_minimal_tab_manager()

        # Add construct_tab placeholder (will be set after tab creation)
        coordinator.construct_tab = None

        # Add sequence level evaluator (needed for difficulty calculation)
        coordinator.sequence_level_evaluator = self._create_sequence_level_evaluator()

        # Add json_manager reference (needed by sequence workbench)
        coordinator.json_manager = self.app_context.json_manager

        # Add fade_manager reference (needed by beat deleter)
        coordinator.fade_manager = coordinator.widget_manager.get_widget("fade_manager")

        # Add get_tab_widget method (needed by beat deleter)
        coordinator.get_tab_widget = (
            lambda tab_name: coordinator.tab_manager.get_tab_widget(tab_name)
        )

        # Add get_widget method (needed by beat frame updater)
        coordinator.get_widget = (
            lambda widget_name: coordinator.widget_manager.get_widget(widget_name)
        )

        # Add main_window placeholder (will be set by StandaloneTabWindow)
        coordinator.main_window = None

        # Add sequence_workbench reference (needed for image creation)
        coordinator.sequence_workbench = coordinator.widget_manager.get_widget(
            "sequence_workbench"
        )

        # Dictionary service will be available through sequence_workbench.dictionary_service
        # No need to add it separately to coordinator

        # Add a custom full screen overlay creator for standalone environment
        coordinator._create_full_screen_overlay = (
            self._create_standalone_full_screen_overlay
        )

        # Apply full screen viewer patch for standalone environment
        self._apply_full_screen_patch()

        # Apply option picker layout patch for standalone environment
        self._apply_option_picker_layout_patch()

        return coordinator

    def _create_minimal_left_stack(self):
        """Create a minimal left stack that provides width() method."""
        from PyQt6.QtWidgets import QStackedWidget

        class MinimalLeftStack(QStackedWidget):
            def __init__(self):
                super().__init__()
                # Set a reasonable default width
                self.setFixedWidth(800)  # Default width for sequence workbench

        return MinimalLeftStack()

    def _create_minimal_tab_manager(self):
        """Create a minimal tab manager that can provide the construct tab."""

        class MinimalTabManager:
            def __init__(self):
                self._tabs = {}

            def get_tab_widget(self, tab_name: str):
                """Get a tab widget by name."""
                return self._tabs.get(tab_name)

            def set_tab_widget(self, tab_name: str, tab_widget):
                """Set a tab widget."""
                self._tabs[tab_name] = tab_widget

            def get_current_tab(self):
                """Get the current active tab (for standalone, it's always the construct tab)."""
                return self._tabs.get("construct")

        return MinimalTabManager()

    def _create_standalone_full_screen_overlay(self, coordinator):
        """Create a full screen overlay that works properly in standalone environment."""
        from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
        from PyQt6.QtCore import Qt, QRect
        from PyQt6.QtGui import QPixmap

        class StandaloneFullScreenOverlay(QWidget):
            def __init__(self, main_window):
                # Create as a top-level window, not a child widget
                super().__init__()
                self.main_window = main_window

                # Set window flags to make it a full screen overlay that stays on top
                self.setWindowFlags(
                    Qt.WindowType.FramelessWindowHint
                    | Qt.WindowType.WindowStaysOnTopHint
                    | Qt.WindowType.Tool
                    | Qt.WindowType.BypassWindowManagerHint
                )

                # Set window modality to ensure it appears on top
                self.setWindowModality(Qt.WindowModality.ApplicationModal)

                # Set up the image label
                self.image_label = QLabel(self)
                self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.image_label.setContentsMargins(0, 0, 0, 0)
                self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)

                # Set up layout
                layout = QVBoxLayout(self)
                layout.addWidget(self.image_label)
                layout.setSpacing(0)
                layout.setContentsMargins(0, 0, 0, 0)
                self.setContentsMargins(0, 0, 0, 0)

                # Set background
                self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9);")

            def show(self, pixmap: QPixmap):
                """Show the overlay with the given pixmap."""
                # Set geometry to cover the main window (correct for dual screen)
                main_window_geometry = self.main_window.geometry()

                # Debug the geometry
                print(f"   Main window geometry: {main_window_geometry}")

                # Use main window geometry (this is correct for dual screen setup)
                self.setGeometry(main_window_geometry)

                # Scale pixmap to fit window
                window_size = main_window_geometry.size()
                scaled_pixmap = pixmap.scaled(
                    window_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.image_label.setPixmap(scaled_pixmap)

                # Show the overlay with aggressive z-ordering
                super().show()
                self.raise_()  # Bring to front
                self.activateWindow()  # Make it active
                self.setFocus()  # Give it focus

                # Force it to the top with additional methods
                self.showNormal()  # Ensure it's not minimized
                self.setWindowState(Qt.WindowState.WindowActive)  # Set as active window

                print(f"   overlay window state: {self.windowState()}")
                print(f"   overlay is active: {self.isActiveWindow()}")
                print(f"   overlay has focus: {self.hasFocus()}")

            def mousePressEvent(self, event):
                """Close the overlay when clicked."""
                self.close()
                super().mousePressEvent(event)

        return StandaloneFullScreenOverlay

    def _apply_full_screen_patch(self):
        """Apply the full screen viewer patch for standalone environment."""
        try:
            from standalone.core.patches.full_screen_patch import (
                patch_full_screen_viewer_for_standalone,
            )

            patch_full_screen_viewer_for_standalone()
        except Exception as e:
            print(f"Warning: Could not apply full screen patch: {e}")

    def _apply_option_picker_layout_patch(self):
        """Apply the option picker layout patch for standalone environment."""
        try:
            from standalone.core.patches.option_picker_layout_patch import (
                patch_option_picker_layout_for_standalone,
            )

            patch_option_picker_layout_for_standalone()
        except Exception as e:
            print(f"Warning: Could not apply option picker layout patch: {e}")

    def _create_sequence_level_evaluator(self):
        """Create a sequence level evaluator for difficulty calculation."""
        try:
            from main_window.main_widget.sequence_level_evaluator import (
                SequenceLevelEvaluator,
            )

            return SequenceLevelEvaluator()
        except ImportError as e:
            print(f"Warning: Could not import SequenceLevelEvaluator: {e}")

            # Create a minimal fallback
            class MinimalSequenceLevelEvaluator:
                def get_sequence_difficulty_level(self, sequence_json):
                    """Return a default difficulty level."""
                    return 1  # Default to level 1

            return MinimalSequenceLevelEvaluator()

    def _create_fade_function(self, coordinator):
        """Create a fade function that switches stack indices."""

        def fade_to_stack_index(index: int):
            """Switch to the specified stack index."""
            if coordinator.right_stack and hasattr(
                coordinator.right_stack, "setCurrentIndex"
            ):
                coordinator.right_stack.setCurrentIndex(index)
                print(f"Switched to stack index {index}")
            else:
                print(f"Warning: right_stack not available for index {index}")

        return fade_to_stack_index

    def _create_minimal_splash_screen(self):
        """Create a minimal splash screen placeholder."""

        class MinimalSplashScreen:
            class MinimalUpdater:
                def update_progress(self, message):
                    pass

                def start_phase(self, phase_name, steps, message):
                    pass

                def update_phase_progress(self, steps, message):
                    pass

                def complete_phase(self, message):
                    pass

            def __init__(self):
                self.updater = self.MinimalUpdater()

        return MinimalSplashScreen()

    def _create_minimal_widget_manager(self, coordinator):
        """Create a minimal widget manager that provides essential widgets."""

        class MinimalWidgetManager:
            def __init__(self, coordinator, app_context):
                self.coordinator = coordinator
                self.app_context = app_context
                self._widgets = {}

            def get_widget(self, widget_name: str):
                """Get or create a widget on demand."""
                if widget_name in self._widgets:
                    return self._widgets[widget_name]

                # Create widgets as needed
                if widget_name == "sequence_workbench":
                    return self._create_sequence_workbench()
                elif widget_name == "fade_manager":
                    return self._create_fade_manager()
                elif widget_name == "pictograph_collector":
                    return self._create_pictograph_collector()
                else:
                    # Return None for unknown widgets
                    return None

            def _create_sequence_workbench(self):
                """Create a minimal sequence workbench."""
                try:
                    from main_window.main_widget.sequence_workbench.sequence_workbench_factory import (
                        SequenceWorkbenchFactory,
                    )

                    workbench = SequenceWorkbenchFactory.create(
                        self.coordinator, self.app_context
                    )
                    self._widgets["sequence_workbench"] = workbench
                    return workbench
                except Exception as e:
                    print(f"Warning: Could not create sequence workbench: {e}")
                    return None

            def _create_fade_manager(self):
                """Create a minimal fade manager."""
                try:
                    from main_window.main_widget.fade_manager.fade_manager_factory import (
                        FadeManagerFactory,
                    )

                    fade_manager = FadeManagerFactory.create(
                        self.coordinator, self.app_context
                    )
                    self._widgets["fade_manager"] = fade_manager
                    return fade_manager
                except Exception as e:
                    print(f"Warning: Could not create fade manager: {e}")
                    return None

            def _create_pictograph_collector(self):
                """Create a minimal pictograph collector."""
                try:
                    from main_window.main_widget.pictograph_collector_factory import (
                        PictographCollectorFactory,
                    )

                    collector = PictographCollectorFactory.create(
                        self.coordinator, self.app_context
                    )
                    self._widgets["pictograph_collector"] = collector
                    return collector
                except Exception as e:
                    print(f"Warning: Could not create pictograph collector: {e}")
                    return None

        return MinimalWidgetManager(coordinator, self.app_context)

    def create_tab(self) -> QWidget:
        """Create the tab widget using its factory."""
        coordinator = self.create_minimal_coordinator()

        # Use the factory to create the tab
        tab_widget = self.tab_factory_class.create(
            parent=coordinator, app_context=self.app_context
        )

        return tab_widget

    def create_tab_with_coordinator(self, coordinator) -> QWidget:
        """Create the tab widget using its factory with a specific coordinator."""
        # Use the factory to create the tab
        tab_widget = self.tab_factory_class.create(
            parent=coordinator, app_context=self.app_context
        )

        # For construct tab, set up the references that StartPositionAdder expects
        if self.tab_name == "construct" and tab_widget:
            coordinator.construct_tab = tab_widget
            if hasattr(coordinator, "tab_manager"):
                coordinator.tab_manager.set_tab_widget("construct", tab_widget)

        return tab_widget

    def run(self) -> int:
        """
        Run the standalone tab application.

        Returns:
            Exit code from the application
        """
        try:
            # Setup
            self.configure_import_paths()
            self.initialize_logging()

            # Initialize Qt application
            self.app = self.initialize_application()

            # Initialize dependency injection
            self.app_context = self.initialize_dependency_injection()

            # Create the tab
            coordinator = self.create_minimal_coordinator()
            tab_widget = self.create_tab_with_coordinator(coordinator)

            # Create main window and show
            self.main_window = StandaloneTabWindow(
                tab_widget, self.tab_name, coordinator
            )
            self.main_window.show()

            # Run the application
            return self.app.exec()

        except Exception as e:
            print(f"Error running standalone {self.tab_name}: {e}")
            import traceback

            traceback.print_exc()
            return 1


def create_standalone_runner(
    tab_name: str, tab_factory_class: Type
) -> BaseStandaloneRunner:
    """
    Factory function to create a standalone runner for any tab.

    Args:
        tab_name: Name of the tab (e.g., "construct", "generate")
        tab_factory_class: Factory class for creating the tab

    Returns:
        Configured standalone runner
    """
    return BaseStandaloneRunner(tab_name, tab_factory_class)
