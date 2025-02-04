from PyQt6.QtWidgets import (
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.generator_type_button import (
    GeneratorTypeButton,
)

from .generate_sequence_button import GenerateSequenceButton


if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateTabButtonManager:
    def __init__(self, tab: "GenerateTab"):
        self.tab = tab
        self.nav_buttons = {}
        self._setup_buttons()

    def _setup_buttons(self):
        self.tab.button_layout = QHBoxLayout()
        self.tab.button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab.freeform_button = GeneratorTypeButton(
            "Freeform", self.tab.freeform_generator_frame, "freeform"
        )
        self.tab.circular_button = GeneratorTypeButton(
            "Circular", self.tab.circular_generator_frame, "circular"
        )

        for button in [self.tab.freeform_button, self.tab.circular_button]:
            self.tab.button_layout.addWidget(button)

        self.nav_buttons = {
            "freeform": self.tab.freeform_button,
            "circular": self.tab.circular_button,
        }
        self.tab.generate_sequence_button = GenerateSequenceButton(self.tab)
        self.tab.generate_sequence_button.clicked.connect(self.tab.dummy_function)
        self.update_button_styles()

    def update_button_styles(self):
        current_widget = self.tab.generator_type
        for key, button in self.nav_buttons.items():
            active = key == current_widget
            button.update_style(active)
