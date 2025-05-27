from typing import TYPE_CHECKING, Optional
from letter_determination.core import LetterDeterminer
from main_window.main_widget.pictograph_collector import PictographCollector
from main_window.main_widget.pictograph_data_loader import PictographDataLoader

from .sequence_properties_manager.sequence_properties_manager_factory import (
    SequencePropertiesManagerFactory,
)
from .sequence_level_evaluator import SequenceLevelEvaluator
from .thumbnail_finder import ThumbnailFinder

if TYPE_CHECKING:
    from .main_widget import MainWidget
    from core.application_context import ApplicationContext
    from interfaces.settings_manager_interface import ISettingsManager


class MainWidgetManagers:
    def __init__(
        self,
        main_widget: "MainWidget",
        app_context: Optional["ApplicationContext"] = None,
    ):
        """
        Initialize the MainWidgetManagers with dependency injection.

        Args:
            main_widget: The main widget instance
            app_context: Application context with dependencies. If None, uses legacy adapter.
        """
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.splash_screen = main_widget.splash_screen

        # Set up dependencies
        if app_context:
            self.app_context = app_context
            self.settings_manager = app_context.settings_manager
        else:
            # Legacy compatibility - use adapter
            from core.migration_adapters import AppContextAdapter

            self.app_context = None
            self.settings_manager = AppContextAdapter.settings_manager()

        self._setup_pictograph_cache()
        self._set_prop_type()
        self._initialize_managers()
        self._setup_letters()

    def _initialize_managers(self):
        """Setup all the managers and helper components."""
        mw = self.main_widget

        mw.sequence_level_evaluator = SequenceLevelEvaluator()

        # Use factory to create sequence properties manager with dependency injection
        if self.app_context:
            mw.sequence_properties_manager = SequencePropertiesManagerFactory.create(
                self.app_context
            )
        else:
            mw.sequence_properties_manager = (
                SequencePropertiesManagerFactory.create_legacy()
            )

        mw.thumbnail_finder = ThumbnailFinder()
        mw.pictograph_collector = PictographCollector(mw)

        # mw.special_placements = mw.special_placement_loader.load_special_placements()

    def _setup_pictograph_cache(self) -> None:
        from enums.glyph_enum import Letter

        self.main_widget.pictograph_cache = {}
        for letter in Letter:
            self.main_widget.pictograph_cache[letter] = {}

    def _set_prop_type(self) -> None:
        prop_type = self.settings_manager.global_settings.get_prop_type()
        self.main_widget.prop_type = prop_type

    def _setup_letters(self) -> None:
        try:
            # Get PictographDataLoader from dependency injection
            pictograph_data_loader = self.main_widget.app_context.get_service(
                PictographDataLoader
            )
            # Store reference for backward compatibility
            self.main_widget.pictograph_data_loader = pictograph_data_loader
            pictograph_dataset = pictograph_data_loader.load_pictograph_dataset()
        except (AttributeError, KeyError):
            # Fallback: create directly if dependency injection not available
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "PictographDataLoader not available via dependency injection, creating directly"
            )
            self.main_widget.pictograph_data_loader = PictographDataLoader(
                self.main_widget
            )
            pictograph_dataset = (
                self.main_widget.pictograph_data_loader.load_pictograph_dataset()
            )

        self.main_widget.pictograph_dataset = pictograph_dataset

        # Check if letter_determiner already exists from dependency injection
        if (
            hasattr(self.main_widget, "letter_determiner")
            and self.main_widget.letter_determiner
        ):
            # Update existing letter determiner with the loaded dataset
            if hasattr(self.main_widget.letter_determiner, "update_pictograph_dataset"):
                self.main_widget.letter_determiner.update_pictograph_dataset(
                    pictograph_dataset
                )
                import logging

                logger = logging.getLogger(__name__)
                logger.info(
                    "Updated existing letter determiner with loaded pictograph dataset"
                )
            else:
                # Fallback: create new letter determiner
                try:
                    json_manager = self.main_widget.app_context.json_manager
                    self.main_widget.letter_determiner = LetterDeterminer(
                        pictograph_dataset=pictograph_dataset,
                        json_manager=json_manager,
                    )
                except AttributeError:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(
                        "json_manager not available during letter determiner setup"
                    )
                    self.main_widget.letter_determiner = LetterDeterminer(
                        pictograph_dataset=pictograph_dataset,
                        json_manager=None,
                    )
        else:
            # Create new letter determiner
            try:
                json_manager = self.main_widget.app_context.json_manager
                self.main_widget.letter_determiner = LetterDeterminer(
                    pictograph_dataset=pictograph_dataset,
                    json_manager=json_manager,
                )
            except AttributeError:
                # Fallback for cases where app_context is not available
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "json_manager not available during letter determiner setup"
                )
                self.main_widget.letter_determiner = LetterDeterminer(
                    pictograph_dataset=pictograph_dataset,
                    json_manager=None,
                )
