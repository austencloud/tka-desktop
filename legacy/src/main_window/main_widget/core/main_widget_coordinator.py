"""
Main widget coordinator that orchestrates the different components of the main widget.

This replaces the monolithic MainWidget class with a coordinator that manages
smaller, focused components following the Single Responsibility Principle.
"""

from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import pyqtSignal

from core.application_context import ApplicationContext
from .tab_manager import TabManager
from .widget_manager import WidgetManager
from .state_manager import StateManager
from .image_drag_drop_handler import ImageDragDropHandler
from .image_drop_processor import ImageDropProcessor

if TYPE_CHECKING:
    from main_window.main_window import MainWindow
    from splash_screen.splash_screen import SplashScreen


class MainWidgetCoordinator(QWidget):
    """
    Coordinates the main widget components without violating SRP.

    Responsibilities:
    - Orchestrate tab and widget managers
    - Handle high-level layout
    - Coordinate between different managers
    - Provide clean interface to MainWindow
    """

    # Signals for communication between components
    tab_changed = pyqtSignal(str)  # tab_name
    state_changed = pyqtSignal(dict)  # state_data

    def __init__(
        self,
        main_window: "MainWindow",
        splash_screen: "SplashScreen",
        app_context: ApplicationContext,
    ):
        super().__init__(main_window)

        self.main_window = main_window
        self.splash_screen = splash_screen
        self.app_context = app_context
        self._components_initialized = False

        # Initialize managers with clear responsibilities
        self.tab_manager = TabManager(self, app_context)
        self.widget_manager = WidgetManager(self, app_context)
        self.state_manager = StateManager(self, app_context)

        # Inject essential services for backward compatibility
        self._inject_legacy_services(app_context)

        # Initialize image drag and drop functionality
        self.image_drop_processor = ImageDropProcessor(app_context)
        self.image_drag_drop_handler = ImageDragDropHandler(self, app_context)

        # Setup layout and connections
        self._setup_layout()
        self._connect_signals()
        self._setup_image_drag_drop()

        # NOTE: Components will be initialized separately to avoid circular dependencies
        # Call initialize_components() after dependency injection is fully set up

    def _setup_layout(self) -> None:
        """Setup the main layout structure with hybrid tab support."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create horizontal layout for main content (stack-based tabs)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Add stacked widgets for left and right panels
        self.left_stack = QStackedWidget()
        self.right_stack = QStackedWidget()

        # Add widgets with initial equal stretch ratio
        self.content_layout.addWidget(self.left_stack, 1)  # Left stack
        self.content_layout.addWidget(self.right_stack, 1)  # Right stack

        # Create a stacked widget to hold different layout modes
        self.main_content_stack = QStackedWidget()

        # Create container widget for stack-based layout
        self.stack_container = QWidget()
        self.stack_container.setLayout(self.content_layout)

        # Add the stack container as the first widget (index 0)
        self.main_content_stack.addWidget(self.stack_container)

        # Note: Full-widget tabs will be added to main_content_stack at indices 1+
        # Menu bar will be added to the layout after widgets are initialized
        self.main_layout.addWidget(self.main_content_stack)
        self.setLayout(self.main_layout)

        # Track current layout mode
        self._current_layout_mode = "stack"  # "stack" or "full_widget"

    def _connect_signals(self) -> None:
        """Connect signals between managers."""
        # Tab manager signals
        self.tab_manager.tab_changed.connect(self._on_tab_changed)

        # Widget manager signals
        self.widget_manager.widget_ready.connect(self._on_widget_ready)

        # State manager signals
        self.state_manager.state_changed.connect(self.state_changed.emit)

        # Image drag and drop signals
        self.image_drag_drop_handler.image_dropped.connect(self._on_image_dropped)
        self.image_drag_drop_handler.images_dropped.connect(self._on_images_dropped)
        self.image_drag_drop_handler.drop_error.connect(self._on_drop_error)

    def _inject_legacy_services(self, app_context: ApplicationContext) -> None:
        """
        Inject essential services into the coordinator for backward compatibility.

        Many legacy components expect to access services through main_widget attributes.
        This method provides those services to maintain compatibility.
        """
        # Core services
        self.settings_manager = app_context.settings_manager
        self.json_manager = app_context.json_manager

        # Additional services will be set later in initialize_components()
        # after the dependency injection system is fully ready
        self.letter_determiner = None
        self.fade_manager = None
        self.thumbnail_finder = None
        self.sequence_level_evaluator = None
        self.sequence_properties_manager = None
        self.sequence_workbench = None
        self.pictograph_dataset = None
        self.pictograph_collector = None
        self.pictograph_cache = {}  # Initialize empty cache for backward compatibility

        # Tab widgets for backward compatibility
        self.construct_tab = None
        self.learn_tab = None
        self.settings_dialog = None

    def initialize_components(self) -> None:
        """
        Initialize all components in the correct order.

        This method should be called AFTER the dependency injection system
        and legacy compatibility are fully set up to avoid circular dependencies.
        """
        import logging

        logger = logging.getLogger(__name__)

        logger.info("MainWidgetCoordinator.initialize_components() called")

        if self._components_initialized:
            logger.info("Components already initialized, skipping")
            return  # Already initialized

        try:
            # Initialize widgets first
            logger.info("Initializing widget manager...")
            self.widget_manager.initialize_widgets()
            logger.info("Widget manager initialization completed")

            # Set sequence_properties_manager immediately after widgets are initialized
            # This is needed early for sequence generation functionality
            try:
                from main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import (
                    SequencePropertiesManagerFactory,
                )

                self.sequence_properties_manager = (
                    SequencePropertiesManagerFactory.create(self.app_context)
                )
                logger.info(
                    "Sequence properties manager injected for backward compatibility"
                )
            except Exception as e:
                logger.warning(f"Sequence properties manager not available: {e}")
                self.sequence_properties_manager = None

            # Set additional services after widgets are initialized
            self.fade_manager = self.widget_manager.get_widget("fade_manager")
            if self.fade_manager:
                logger.info("Fade manager injected for backward compatibility")
            else:
                logger.warning("Fade manager not available")

            # Set sequence_workbench for backward compatibility
            self.sequence_workbench = self.widget_manager.get_widget(
                "sequence_workbench"
            )
            if self.sequence_workbench:
                logger.info("Sequence workbench injected for backward compatibility")
            else:
                logger.warning("Sequence workbench not available")

            # Create thumbnail_finder directly (it's not a widget)
            try:
                from main_window.main_widget.thumbnail_finder import ThumbnailFinder

                self.thumbnail_finder = ThumbnailFinder()
                logger.info("Thumbnail finder created for backward compatibility")
            except Exception as e:
                logger.warning(f"Thumbnail finder creation failed: {e}")
                self.thumbnail_finder = None

            # Create sequence_level_evaluator directly (it's not a widget)
            try:
                from main_window.main_widget.sequence_level_evaluator import (
                    SequenceLevelEvaluator,
                )

                self.sequence_level_evaluator = SequenceLevelEvaluator()
                logger.info(
                    "Sequence level evaluator created for backward compatibility"
                )
            except Exception as e:
                logger.warning(f"Sequence level evaluator creation failed: {e}")
                self.sequence_level_evaluator = None

            # Set letter_determiner after dependency injection is fully ready
            try:
                from letter_determination.core import LetterDeterminer

                self.letter_determiner = self.app_context.get_service(LetterDeterminer)
                logger.info("Letter determiner injected for backward compatibility")
            except Exception as e:
                logger.warning(f"Letter determiner not available: {e}")
                self.letter_determiner = None

            # Set pictograph_dataset for backward compatibility
            try:
                from main_window.main_widget.pictograph_data_loader import (
                    PictographDataLoader,
                )

                pictograph_data_loader = self.app_context.get_service(
                    PictographDataLoader
                )
                if pictograph_data_loader and hasattr(
                    pictograph_data_loader, "get_pictograph_dataset"
                ):
                    self.pictograph_dataset = (
                        pictograph_data_loader.get_pictograph_dataset()
                    )
                    logger.info(
                        "Pictograph dataset injected for backward compatibility"
                    )

                    # Update the letter determiner with the loaded dataset
                    if self.letter_determiner and hasattr(
                        self.letter_determiner, "update_pictograph_dataset"
                    ):
                        self.letter_determiner.update_pictograph_dataset(
                            self.pictograph_dataset
                        )
                        logger.info(
                            "Letter determiner dataset updated with loaded data"
                        )
                else:
                    logger.warning("Pictograph dataset not available from data loader")
                    self.pictograph_dataset = {}
            except Exception as e:
                logger.warning(f"Pictograph dataset not available: {e}")
                self.pictograph_dataset = {}

            # Set pictograph_collector for backward compatibility
            try:
                from main_window.main_widget.pictograph_collector_factory import (
                    PictographCollectorFactory,
                )

                self.pictograph_collector = PictographCollectorFactory.create(
                    parent=self, app_context=self.app_context
                )
                logger.info("Pictograph collector created for backward compatibility")

            except ImportError as e:
                logger.warning(f"Could not import PictographCollectorFactory: {e}")
                # Fallback: create basic pictograph collector
                try:
                    from main_window.main_widget.pictograph_collector import (
                        PictographCollector,
                    )

                    self.pictograph_collector = PictographCollector(self)
                    logger.info(
                        "Fallback pictograph collector created for backward compatibility"
                    )
                except ImportError as e2:
                    logger.error(f"Could not create pictograph_collector: {e2}")
                    self.pictograph_collector = None
            except Exception as e:
                logger.error(f"Failed to initialize pictograph_collector: {e}")
                self.pictograph_collector = None

            # Set tab widgets for backward compatibility (needed by pictograph_collector)
            self.construct_tab = self.tab_manager.get_tab_widget("construct")
            if self.construct_tab:
                logger.info("Construct tab injected for backward compatibility")
            else:
                logger.warning("Construct tab not available")

            self.learn_tab = self.tab_manager.get_tab_widget("learn")
            if self.learn_tab:
                logger.info("Learn tab injected for backward compatibility")
            else:
                logger.warning("Learn tab not available")

            self.settings_dialog = self.widget_manager.get_widget("settings_dialog")
            if self.settings_dialog:
                logger.info("Settings dialog injected for backward compatibility")
            else:
                logger.warning("Settings dialog not available")

            # Set up the menu bar layout after widgets are created
            logger.info("Setting up menu bar layout...")
            self._setup_menu_bar_layout()
            logger.info("Menu bar layout setup completed")

            # Initialize tabs (TabManager will populate stacks with essential widgets)
            # Note: TabManager.initialize_tabs() handles stack population
            logger.info("Initializing tab manager...")
            self.tab_manager.initialize_tabs()
            logger.info("Tab manager initialization completed")

            # Finally initialize state
            logger.info("Initializing state manager...")
            self.state_manager.initialize_state()
            logger.info("State manager initialization completed")

            # Load saved sequence into beat frame after all widgets are initialized
            logger.info("Loading saved sequence into beat frame...")
            self._load_saved_sequence()
            logger.info("Saved sequence loading completed")

            self._components_initialized = True
            logger.info(
                "MainWidgetCoordinator component initialization completed successfully"
            )

        except Exception as e:
            logger.error(f"MainWidgetCoordinator component initialization failed: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _setup_menu_bar_layout(self) -> None:
        """Set up the menu bar layout after widgets are initialized."""
        try:
            # Get the menu bar widget
            menu_bar = self.widget_manager.get_widget("menu_bar")
            if not menu_bar:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning("Menu bar widget not available for layout setup")
                return

            # Create top layout for menu bar components (similar to old MainWidgetUI)
            self.top_layout = QHBoxLayout()
            self.top_layout.setContentsMargins(0, 0, 0, 0)
            self.top_layout.setSpacing(0)

            # Add menu bar components with proper proportions
            if hasattr(menu_bar, "social_media_widget"):
                self.top_layout.addWidget(menu_bar.social_media_widget, 1)
            if hasattr(menu_bar, "navigation_widget"):
                self.top_layout.addWidget(menu_bar.navigation_widget, 16)
            if hasattr(menu_bar, "settings_button"):
                self.top_layout.addWidget(menu_bar.settings_button, 1)

            # Insert the top layout at the beginning of the main layout
            self.main_layout.insertLayout(0, self.top_layout)

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to set up menu bar layout: {e}")

    def _load_saved_sequence(self) -> None:
        """Load the saved sequence from current_sequence.json into the beat frame UI."""
        try:
            # Get the sequence workbench
            sequence_workbench = self.widget_manager.get_widget("sequence_workbench")
            if not sequence_workbench or not hasattr(sequence_workbench, "beat_frame"):
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Sequence workbench or beat frame not available for sequence loading"
                )
                return

            beat_frame = sequence_workbench.beat_frame
            if not beat_frame or not hasattr(beat_frame, "populator"):
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Beat frame populator not available for sequence loading"
                )
                return

            # Check if construct tab is available (needed for start position picker)
            construct_tab = self.tab_manager.get_tab_widget("construct")
            if not construct_tab or not hasattr(construct_tab, "start_pos_picker"):
                import logging
                from PyQt6.QtCore import QTimer

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Construct tab or start position picker not available, deferring sequence loading"
                )
                # Defer the sequence loading until the construct tab is ready
                QTimer.singleShot(1000, self._load_saved_sequence)
                return

            # Load the current sequence from JSON
            json_manager = self.app_context.json_manager
            current_sequence = json_manager.loader_saver.load_current_sequence()

            # Only load if there's actual sequence data (more than just the default entry)
            if len(current_sequence) > 1:
                import logging

                logger = logging.getLogger(__name__)
                logger.info(
                    f"Loading sequence with {len(current_sequence)} entries into beat frame"
                )

                # Use the beat frame populator to load the sequence
                beat_frame.populator.populate_beat_frame_from_json(
                    current_sequence, initial_state_load=True
                )
                logger.info("Sequence loaded successfully into beat frame UI")
            else:
                import logging

                logger = logging.getLogger(__name__)
                logger.info(
                    "No saved sequence found or sequence is empty, starting with empty beat frame"
                )

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to load saved sequence: {e}")
            # Don't raise - let the application continue with an empty beat frame

    def _setup_image_drag_drop(self) -> None:
        """Set up image drag and drop functionality."""
        # Set up callbacks for the drag and drop handler
        self.image_drag_drop_handler.set_single_image_callback(
            self.image_drop_processor.process_single_image
        )
        self.image_drag_drop_handler.set_multiple_images_callback(
            self.image_drop_processor.process_multiple_images
        )

    def _on_image_dropped(self, image_path: str) -> None:
        """Handle single image drop events."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Single image dropped: {image_path}")

    def _on_images_dropped(self, image_paths: list) -> None:
        """Handle multiple images drop events."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Multiple images dropped: {len(image_paths)} files")

    def _on_drop_error(self, error_message: str) -> None:
        """Handle drag and drop errors."""
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Drag and drop error: {error_message}")

    def _on_tab_changed(self, tab_name: str) -> None:
        """Handle tab change events."""
        # Update state
        self.state_manager.set_current_tab(tab_name)

        # Update widget visibility
        self.widget_manager.update_for_tab(tab_name)

        # Update navigation widget highlighting
        self._update_navigation_highlighting(tab_name)

        # Emit signal for external listeners
        self.tab_changed.emit(tab_name)

    def _update_navigation_highlighting(self, tab_name: str) -> None:
        """Update the navigation widget to highlight the correct tab."""
        try:
            # Get the menu bar widget
            menu_bar = self.widget_manager.get_widget("menu_bar")
            if menu_bar and hasattr(menu_bar, "navigation_widget"):
                navigation_widget = menu_bar.navigation_widget
                if hasattr(navigation_widget, "on_tab_changed_programmatically"):
                    navigation_widget.on_tab_changed_programmatically(tab_name)
                else:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(
                        "Navigation widget does not have on_tab_changed_programmatically method"
                    )
            else:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Menu bar or navigation widget not available for highlighting update"
                )
        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to update navigation highlighting: {e}")

    def _on_widget_ready(self, widget_name: str) -> None:
        """Handle widget ready events."""
        # Update tab manager when widgets are ready
        self.tab_manager.on_widget_ready(widget_name)

    # Public interface methods
    def get_current_tab(self) -> Optional[str]:
        """Get the currently active tab."""
        return self.state_manager.current_tab

    def switch_to_tab(self, tab_name: str) -> None:
        """Switch to a specific tab."""
        self.tab_manager.switch_to_tab(tab_name)

    def get_tab_widget(self, tab_name: str) -> Optional[QWidget]:
        """Get a specific tab widget."""
        return self.tab_manager.get_tab_widget(tab_name)

    def switch_to_stack_layout(
        self, left_stretch: int = 1, right_stretch: int = 1
    ) -> None:
        """
        Switch to stack-based layout mode for construct/generate/learn tabs.

        Args:
            left_stretch: Stretch factor for left stack
            right_stretch: Stretch factor for right stack
        """
        if self._current_layout_mode != "stack":
            self.main_content_stack.setCurrentIndex(0)  # Show stack container
            self._current_layout_mode = "stack"

        # Apply stretch factors to the content layout
        self.content_layout.setStretch(0, left_stretch)
        self.content_layout.setStretch(1, right_stretch)

        # Clear any fixed width constraints
        self.left_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
        self.left_stack.setMinimumWidth(0)
        self.right_stack.setMaximumWidth(16777215)  # QWIDGETSIZE_MAX
        self.right_stack.setMinimumWidth(0)

    def switch_to_full_widget_layout(self, tab_widget: QWidget) -> None:
        """
        Switch to full-widget layout mode for browse/sequence_card tabs.

        Args:
            tab_widget: The tab widget that should take full control of the layout
        """
        # Check if this tab widget is already in the main content stack
        tab_index = -1
        for i in range(
            1, self.main_content_stack.count()
        ):  # Skip index 0 (stack container)
            if self.main_content_stack.widget(i) is tab_widget:
                tab_index = i
                break

        # If not found, add it to the stack
        if tab_index == -1:
            tab_index = self.main_content_stack.addWidget(tab_widget)

        # Switch to the tab widget
        self.main_content_stack.setCurrentIndex(tab_index)
        self._current_layout_mode = "full_widget"

    def get_current_layout_mode(self) -> str:
        """Get the current layout mode ('stack' or 'full_widget')."""
        return self._current_layout_mode

    def get_widget(self, widget_name: str) -> Optional[QWidget]:
        """Get a specific widget."""
        return self.widget_manager.get_widget(widget_name)

    def show_settings_dialog(self) -> None:
        """Show the settings dialog."""
        settings_dialog = self.widget_manager.get_widget("settings_dialog")
        if settings_dialog:
            settings_dialog.show()

    def show_full_screen_overlay(self, image_data) -> None:
        """Show the full screen image overlay."""
        overlay = self.widget_manager.get_widget("full_screen_overlay")
        if overlay:
            overlay.show_image(image_data)

    def enable_image_drag_drop(self) -> None:
        """Enable image drag and drop functionality."""
        if hasattr(self, "image_drag_drop_handler"):
            self.image_drag_drop_handler.enable()

    def disable_image_drag_drop(self) -> None:
        """Disable image drag and drop functionality."""
        if hasattr(self, "image_drag_drop_handler"):
            self.image_drag_drop_handler.disable()

    # Cleanup methods
    def cleanup(self) -> None:
        """Cleanup resources when shutting down."""
        self.tab_manager.cleanup()
        self.widget_manager.cleanup()
        self.state_manager.cleanup()

        # Cleanup image drag and drop
        if hasattr(self, "image_drag_drop_handler"):
            self.image_drag_drop_handler.cleanup()


class MainWidgetFactory:
    """Factory for creating MainWidget instances with proper dependency injection."""

    @staticmethod
    def create(
        main_window: "MainWindow",
        splash_screen: "SplashScreen",
        app_context: ApplicationContext,
    ) -> MainWidgetCoordinator:
        """
        Create a new MainWidget instance.

        Args:
            main_window: The parent main window
            splash_screen: The splash screen instance
            app_context: The application context with dependencies

        Returns:
            A new MainWidgetCoordinator instance
        """
        return MainWidgetCoordinator(main_window, splash_screen, app_context)
