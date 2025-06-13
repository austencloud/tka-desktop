from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from typing import TYPE_CHECKING, Optional, Union
import logging

from main_window.main_widget.generate_tab.circular.CAP_type_picker.CAP_picker import (
    CAPPicker,
)
from interfaces.settings_manager_interface import ISettingsManager  # ensure import
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.generate_tab.circular.circular_sequence_builder import (
    CircularSequenceBuilder,
)
from main_window.main_widget.generate_tab.freeform.freeform_sequence_builder import (
    FreeFormSequenceBuilder,
)
from main_window.main_widget.sequence_workbench.sequence_workbench import (
    SequenceWorkbench,
)

from .generate_tab_layout_manager import GenerateTabLayoutManager
from .generate_tab_controller import GenerateTabController

from .widgets.generator_type_toggle import GeneratorTypeToggle
from .widgets.level_selector.level_selector import LevelSelector
from .widgets.generate_tab_length_adjuster import GenerateTabLengthAdjuster
from .widgets.turn_intensity_adjuster import TurnIntensityAdjuster
from .widgets.prop_continuity_toggle import PropContinuityToggle
from .widgets.slice_size_toggle import SliceSizeToggle
from .freeform.letter_type_picker_widget.letter_type_picker_widget import (
    LetterTypePickerWidget,
)
from .customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import GenerateSequenceButton

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from main_window.main_widget.core.tab_manager import TabManager
    from main_window.main_widget.json_manager.json_manager import JsonManager


class GenerateTab(QWidget):
    def __init__(
        self,
        main_widget: "MainWidget",
        settings_manager: Optional[ISettingsManager] = None,
        json_manager: Optional[IJsonManager] = None,
        main_tab_manager: Optional["TabManager"] = None,
    ):
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Settings manager with proper error handling
        if settings_manager:
            self.settings_manager = settings_manager
        elif hasattr(self.main_widget, "settings_manager"):
            self.settings_manager = self.main_widget.settings_manager
        else:
            try:
                from src.settings_manager.global_settings.app_context import AppContext

                self.settings_manager = AppContext.settings_manager()
            except (AttributeError, ImportError):
                raise RuntimeError("No settings manager available")

        # Get generate tab settings using the correct interface
        if hasattr(self.settings_manager, "generate_tab_settings"):
            self.settings = self.settings_manager.generate_tab_settings
        else:
            self.settings = self.settings_manager

        # JSON manager with proper typing
        if json_manager:
            self.json_manager: Union[IJsonManager, "JsonManager"] = json_manager
        elif hasattr(self.main_widget, "json_manager"):
            self.json_manager = self.main_widget.json_manager
        else:
            try:
                from src.settings_manager.global_settings.app_context import AppContext

                self.json_manager = AppContext.json_manager()
            except (AttributeError, ImportError):
                raise RuntimeError("No JSON manager available")

        # Tab manager - make it truly optional since it doesn't exist on MainWidget
        self.main_tab_manager = main_tab_manager

        self.logger = logging.getLogger(__name__)

        # Initialize with current application state
        self.sequence_workbench: "SequenceWorkbench" = (
            self.main_widget.sequence_workbench
        )

        # Store original state with proper typing
        self.original_sequence_workbench: "SequenceWorkbench" = self.sequence_workbench
        self.original_json_manager: Union[IJsonManager, "JsonManager"] = (
            self.json_manager
        )

        self._init_builders()
        self._init_ui()
        self.logger.info("GenerateTab initialized")

    def _init_builders(self) -> None:
        self.freeform_builder = FreeFormSequenceBuilder(self)
        self.circular_builder = CircularSequenceBuilder(self)

    def _init_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.top_spacer = self._create_spacer()
        self.bottom_spacer = self._create_spacer()
        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.auto_complete_button = GenerateSequenceButton(self, "Auto-Complete", False)
        self.generate_button = GenerateSequenceButton(self, "Generate New", True)
        self.generator_type_toggle = GeneratorTypeToggle(self)
        self.level_selector = LevelSelector(self)
        self.length_adjuster = GenerateTabLengthAdjuster(self)
        self.turn_intensity = TurnIntensityAdjuster(self)
        self.prop_continuity_toggle = PropContinuityToggle(self)
        self.letter_picker = LetterTypePickerWidget(self)
        self.slice_size_toggle = SliceSizeToggle(self)
        self.CAP_type_picker = CAPPicker(self)
        self.layout_manager = GenerateTabLayoutManager(self)
        self.controller = GenerateTabController(self)

        self.layout_manager.arrange_layout()
        self.controller.init_from_settings()

    def resizeEvent(self, event):
        available_height = self.height() // 24
        self._resize_spacer(self.top_spacer, available_height)
        self._resize_spacer(self.bottom_spacer, available_height)
        self.main_layout.update()

    def _create_spacer(self):
        return QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    def _resize_spacer(self, spacer: QSpacerItem, height: int):
        spacer.changeSize(
            0, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )

    def reinitialize_builders(self) -> None:
        """Re-initializes the sequence builders, typically after context changes."""
        self._init_builders()
        self.logger.info("Sequence builders re-initialized.")

    def set_isolated_generation_context(
        self,
        isolated_workbench: "SequenceWorkbench",
        isolated_json_manager: Union[IJsonManager, "JsonManager"],
    ) -> None:
        """Sets the context for isolated generation."""
        self.original_sequence_workbench = self.sequence_workbench
        self.original_json_manager = self.json_manager
        self.sequence_workbench = isolated_workbench
        self.json_manager = isolated_json_manager
        self.reinitialize_builders()
        self.logger.info("GenerateTab context switched to isolated generation.")

    def restore_main_context(self) -> None:
        """Restores the main application context after isolated generation."""
        self.sequence_workbench = self.original_sequence_workbench
        self.json_manager = self.original_json_manager
        self.reinitialize_builders()
        self.logger.info("GenerateTab context restored to main application.")

    def __getattr__(self, name):
        if name == "settings":
            return self.settings_manager
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )
