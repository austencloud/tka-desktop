"""
Component Initialization Manager - Handles complex component initialization sequence.

This manager extracts the massive initialization logic from MainWidgetCoordinator
following the Single Responsibility Principle.
"""

import logging
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QTimer

if TYPE_CHECKING:
    from core.application_context import ApplicationContext
    from ..widget_manager import WidgetManager
    from ..tab_manager import TabManager
    from ..main_widget_coordinator import MainWidgetCoordinator


class ComponentInitializationManager:
    """
    Manages the complex component initialization sequence.

    Responsibilities:
    - Handle multi-stage initialization process
    - Manage initialization dependencies/ordering
    - Handle initialization error recovery
    - Load saved sequences
    - Set up menu bar layout
    """

    def __init__(
        self,
        app_context: "ApplicationContext",
        widget_manager: "WidgetManager",
        tab_manager: "TabManager",
        coordinator: "MainWidgetCoordinator",
    ):
        self.app_context = app_context
        self.widget_manager = widget_manager
        self.tab_manager = tab_manager
        self.coordinator = coordinator
        self.logger = logging.getLogger(__name__)

        self._components_initialized = False

        # Initialize AppContextAdapter early to prevent warnings
        self._setup_legacy_compatibility()

    def _setup_legacy_compatibility(self) -> None:
        """Set up legacy compatibility adapter early to prevent warnings."""
        try:
            from core.migration_adapters import setup_legacy_compatibility

            setup_legacy_compatibility(self.app_context)
            self.logger.info("Legacy compatibility adapter initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize legacy compatibility: {e}")

    def initialize_all_components(self) -> None:
        """
        Initialize all components in the correct order.

        This method should be called AFTER the dependency injection system
        and legacy compatibility are fully set up to avoid circular dependencies.
        """
        self.logger.info(
            "ComponentInitializationManager.initialize_all_components() called"
        )

        if self._components_initialized:
            self.logger.info("Components already initialized, skipping")
            return

        try:
            # Phase 1: Initialize widgets first
            self._initialize_widgets()

            # Phase 2: Set up essential services
            self._initialize_services()

            # Phase 3: Set up UI layout
            self._setup_menu_bar_layout()

            # Phase 4: Initialize tabs
            self._initialize_tabs()

            # Phase 5: Initialize state
            self._initialize_state()

            # Phase 6: Load saved sequence
            self._load_saved_sequence()

            self._components_initialized = True
            self.logger.info("Component initialization completed successfully")

        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            import traceback

            traceback.print_exc()
            raise

    def _initialize_widgets(self) -> None:
        """Initialize widget manager and core widgets."""
        self.logger.info("Initializing widget manager...")
        self.widget_manager.initialize_widgets()
        self.logger.info("Widget manager initialization completed")

    def _initialize_services(self) -> None:
        """Initialize essential services for backward compatibility."""
        self.logger.info("Initializing essential services...")

        # Just verify services are available without storing them
        self._setup_sequence_properties_manager()
        self._setup_fade_manager()
        self._setup_sequence_workbench()
        self._setup_thumbnail_finder()
        self._setup_sequence_level_evaluator()
        self._setup_letter_determiner()
        self._setup_pictograph_dataset()
        self._setup_pictograph_collector()
        self._setup_tab_widgets()

        self.logger.info("Essential services initialization completed")

    def _setup_sequence_properties_manager(self) -> None:
        """Set up sequence properties manager."""
        try:
            from main_window.main_widget.sequence_properties_manager.sequence_properties_manager_factory import (
                SequencePropertiesManagerFactory,
            )

            SequencePropertiesManagerFactory.create(self.app_context)
            self.logger.info("Sequence properties manager available")
        except Exception as e:
            self.logger.warning(f"Sequence properties manager not available: {e}")

    def _setup_fade_manager(self) -> None:
        """Set up fade manager."""
        fade_manager = self.widget_manager.get_widget("fade_manager")
        if fade_manager:
            self.logger.info("Fade manager available")
        else:
            self.logger.warning("Fade manager not available")

    def _setup_sequence_workbench(self) -> None:
        """Set up sequence workbench."""
        sequence_workbench = self.widget_manager.get_widget("sequence_workbench")
        if sequence_workbench:
            self.logger.info("Sequence workbench available")
        else:
            self.logger.warning("Sequence workbench not available")

    def _setup_thumbnail_finder(self) -> None:
        """Set up thumbnail finder."""
        try:
            from main_window.main_widget.thumbnail_finder import ThumbnailFinder

            ThumbnailFinder()
            self.logger.info("Thumbnail finder available")
        except Exception as e:
            self.logger.warning(f"Thumbnail finder creation failed: {e}")

    def _setup_sequence_level_evaluator(self) -> None:
        """Set up sequence level evaluator."""
        try:
            from main_window.main_widget.sequence_level_evaluator import (
                SequenceLevelEvaluator,
            )

            SequenceLevelEvaluator()
            self.logger.info("Sequence level evaluator available")
        except Exception as e:
            self.logger.warning(f"Sequence level evaluator creation failed: {e}")

    def _setup_letter_determiner(self) -> None:
        """Set up letter determiner."""
        try:
            from letter_determination.core import LetterDeterminer

            letter_determiner = self.app_context.get_service(LetterDeterminer)
            if letter_determiner:
                self.logger.info("Letter determiner available")
        except Exception as e:
            self.logger.warning(f"Letter determiner not available: {e}")

    def _setup_pictograph_dataset(self) -> None:
        """Set up pictograph dataset."""
        try:
            from main_window.main_widget.pictograph_data_loader import (
                PictographDataLoader,
            )

            pictograph_data_loader = self.app_context.get_service(PictographDataLoader)
            if pictograph_data_loader and hasattr(
                pictograph_data_loader, "get_pictograph_dataset"
            ):
                pictograph_dataset = pictograph_data_loader.get_pictograph_dataset()
                self.logger.info("Pictograph dataset available")
            else:
                self.logger.warning("Pictograph dataset not available from data loader")
        except Exception as e:
            self.logger.warning(f"Pictograph dataset not available: {e}")

    def _setup_pictograph_collector(self) -> None:
        """Set up pictograph collector."""
        try:
            from main_window.main_widget.pictograph_collector_factory import (
                PictographCollectorFactory,
            )

            PictographCollectorFactory.create(
                parent=self.coordinator, app_context=self.app_context
            )
            self.logger.info("Pictograph collector available")
        except ImportError:
            self.logger.info("Using fallback pictograph collector approach")
        except Exception as e:
            self.logger.error(f"Failed to initialize pictograph_collector: {e}")

    def _setup_tab_widgets(self) -> None:
        """Set up tab widgets for backward compatibility."""
        construct_tab = self.tab_manager.get_tab_widget("construct")
        if construct_tab:
            self.logger.info("Construct tab available")
        else:
            self.logger.warning("Construct tab not available")

        learn_tab = self.tab_manager.get_tab_widget("learn")
        if learn_tab:
            self.logger.info("Learn tab available")
        else:
            self.logger.warning("Learn tab not available")

        settings_dialog = self.widget_manager.get_widget("settings_dialog")
        if settings_dialog:
            self.logger.info("Settings dialog available")
        else:
            self.logger.warning("Settings dialog not available")

    def _setup_menu_bar_layout(self) -> None:
        """Set up the menu bar layout after widgets are initialized."""
        self.logger.info("Setting up menu bar layout...")
        try:
            menu_bar = self.widget_manager.get_widget("menu_bar")
            if not menu_bar:
                self.logger.warning("Menu bar widget not available for layout setup")
                return

            from PyQt6.QtWidgets import QHBoxLayout

            top_layout = QHBoxLayout()
            top_layout.setContentsMargins(0, 0, 0, 0)
            top_layout.setSpacing(0)

            # Add menu bar components with safe attribute access
            social_media_widget = getattr(menu_bar, "social_media_widget", None)
            if social_media_widget:
                top_layout.addWidget(social_media_widget, 1)

            navigation_widget = getattr(menu_bar, "navigation_widget", None)
            if navigation_widget:
                top_layout.addWidget(navigation_widget, 16)

            settings_button = getattr(menu_bar, "settings_button", None)
            if settings_button:
                top_layout.addWidget(settings_button, 1)

            # Insert into main layout if it exists
            if hasattr(self.coordinator, "main_layout"):
                self.coordinator.main_layout.insertLayout(0, top_layout)

        except Exception as e:
            self.logger.error(f"Failed to set up menu bar layout: {e}")

        self.logger.info("Menu bar layout setup completed")

    def _initialize_tabs(self) -> None:
        """Initialize tab manager."""
        self.logger.info("Initializing tab manager...")
        self.tab_manager.initialize_tabs()
        self.logger.info("Tab manager initialization completed")

    def _initialize_state(self) -> None:
        """Initialize state manager."""
        self.logger.info("Initializing state manager...")
        self.coordinator.state_manager.initialize_state()
        self.logger.info("State manager initialization completed")

    def _load_saved_sequence(self) -> None:
        """Load the saved sequence from current_sequence.json into the beat frame UI."""
        self.logger.info("Loading saved sequence into beat frame...")
        try:
            sequence_workbench = self.widget_manager.get_widget("sequence_workbench")
            if not sequence_workbench:
                self.logger.warning("Sequence workbench not available")
                return

            beat_frame = getattr(sequence_workbench, "beat_frame", None)
            if not beat_frame:
                self.logger.warning("Beat frame not available on sequence workbench")
                return

            if not hasattr(beat_frame, "populator"):
                self.logger.warning("Beat frame populator not available")
                return

            construct_tab = self.tab_manager.get_tab_widget("construct")
            if not construct_tab or not hasattr(construct_tab, "start_pos_picker"):
                self.logger.info(
                    "Construct tab not available during startup - will load on-demand"
                )
                return

            json_manager = self.app_context.json_manager
            loader_saver = getattr(json_manager, "loader_saver", None)
            if not loader_saver:
                self.logger.warning("JSON manager loader_saver not available")
                return

            current_sequence = loader_saver.load_current_sequence()

            if len(current_sequence) > 1:
                self.logger.info(
                    f"Loading sequence with {len(current_sequence)} entries"
                )
                beat_frame.populator.populate_beat_frame_from_json(
                    current_sequence, initial_state_load=True
                )
                self.logger.info("Sequence loaded successfully")
            else:
                self.logger.info(
                    "No saved sequence found, starting with empty beat frame"
                )

        except Exception as e:
            self.logger.error(f"Failed to load saved sequence: {e}")

        self.logger.info("Saved sequence loading completed")

    def handle_initialization_error(self, error: Exception) -> None:
        """Handle initialization errors with recovery strategies."""
        self.logger.error(f"Initialization error occurred: {error}")

        # Could implement recovery strategies here:
        # - Retry initialization
        # - Skip problematic components
        # - Fallback to minimal initialization
        # - User notification

        # For now, just log and re-raise
        raise error
