from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy
from typing import TYPE_CHECKING


from main_window.main_widget.generate_tab.circular.CAP_type_picker.CAP_picker import (
    CAPPicker,
)
from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager

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

from .freeform.freeform_sequence_builder import FreeFormSequenceBuilder
from .circular.circular_sequence_builder import CircularSequenceBuilder

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
# In your settings manager, ensure CAP_type can handle new values
# Add these to your valid CAP types:


class GenerateTab(QWidget):
    def __init__(
        self,
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.main_widget.splash_screen.updater.update_progress("GenerateTab")
        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.settings = settings_manager.get_generate_tab_settings()
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
        self.generator_type_toggle = GeneratorTypeToggle(self)
        self.level_selector = LevelSelector(self)
        self.length_adjuster = GenerateTabLengthAdjuster(self)
        self.turn_intensity = TurnIntensityAdjuster(self)
        self.prop_continuity_toggle = PropContinuityToggle(self)
        self.letter_picker = LetterTypePickerWidget(self)
        self.slice_size_toggle = SliceSizeToggle(self)
        self.CAP_type_picker = CAPPicker(self)

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
