from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.widgets.permutation_type_toggle import (
    PermutationTypeToggle,
)

from .generate_tab_layout_manager import GenerateTabLayoutManager
from .generate_tab_controller import GenerateTabController

from .widgets.generator_type_toggle import GeneratorTypeToggle
from .widgets.level_selector.level_selector import LevelSelector
from .widgets.length_adjuster import LengthAdjuster
from .widgets.turn_intensity_adjuster import TurnIntensityAdjuster
from .widgets.prop_continuity_toggle import PropContinuityToggle
from .widgets.slice_size_toggle import SliceSizeToggle
from .freeform.letter_type_picker_widget import LetterTypePickerWidget
from .customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import GenerateSequenceButton

from .freeform.freeform_sequence_builder import FreeFormSequenceBuilder
from .circular.circular_sequence_builder import CircularSequenceBuilder

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash.updater.update_progress("GenerateTab")
        self.setObjectName("GenerateTab")
        self.settings = main_widget.main_window.settings_manager.generate_tab_settings
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.controller = GenerateTabController(self)
        self.layout_manager = GenerateTabLayoutManager(self)
        self.freeform_builder = FreeFormSequenceBuilder(self)
        self.circular_builder = CircularSequenceBuilder(self)

        self._create_widgets()
        self.layout_manager.arrange_layout()
        self.controller.init_from_settings()

    def _create_widgets(self):
        self.top_spacer = self._create_spacer()
        self.bottom_spacer = self._create_spacer()
        self.customize_sequence_label = CustomizeSequenceLabel(self)
        self.auto_complete_button = GenerateSequenceButton(self, "Auto-Complete", False)
        self.generate_button = GenerateSequenceButton(self, "Generate New", True)
        self.mode_toggle = GeneratorTypeToggle(self)
        self.level_selector = LevelSelector(self)
        self.length_adjuster = LengthAdjuster(self)
        self.turn_intensity = TurnIntensityAdjuster(self)
        self.prop_continuity_toggle = PropContinuityToggle(self)
        self.letter_picker = LetterTypePickerWidget(self)
        self.slice_size_toggle = SliceSizeToggle(self)
        self.permutation_type_toggle = PermutationTypeToggle(self)

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
