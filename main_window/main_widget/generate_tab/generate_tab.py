from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QStackedLayout,
)
from typing import TYPE_CHECKING

from .generate_tab_spacer import GenerateTabSpacer
from .button_manager import GenerateTabButtonManager
from .freeform.overwrite_checkbox_widget import OverwriteCheckboxWidget
from .layout_manager import GenerateTabLayoutManager
from .customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import GenerateSequenceButton
from .circular.circular_sequence_generator_frame import CircularSequenceGeneratorFrame
from .freeform.freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTab(QWidget):
    freeform_generator_frame: FreeformSequenceGeneratorFrame
    circular_generator_frame: CircularSequenceGeneratorFrame
    spacer_1: "GenerateTabSpacer"
    spacer_2: "GenerateTabSpacer"
    spacer_3: "GenerateTabSpacer"
    button_layout: QHBoxLayout
    stacked_widget: QStackedLayout
    freeform_button: QPushButton
    circular_button: QPushButton
    generate_sequence_button: GenerateSequenceButton
    dummy_function = lambda: None
    overwrite_checkbox: OverwriteCheckboxWidget
    customize_sequence_label: CustomizeSequenceLabel
    checkbox_layout: QHBoxLayout
    layout: QVBoxLayout
    overwrite_connected = False
    generator_type = "freeform"

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Frames
        self.freeform_generator_frame = FreeformSequenceGeneratorFrame(self)
        self.circular_generator_frame = CircularSequenceGeneratorFrame(self)

        # Widgets
        self.overwrite_checkbox = OverwriteCheckboxWidget(self)
        self.customize_sequence_label = CustomizeSequenceLabel(self)

        # Managers
        self.button_manager = GenerateTabButtonManager(self)
        self.layout_manager = GenerateTabLayoutManager(self)
