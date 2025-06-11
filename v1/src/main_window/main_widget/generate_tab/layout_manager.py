from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.generate_tab_spacer import GenerateTabSpacer


if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateTabLayoutManager:
    def __init__(self, tab: "GenerateTab"):
        self.tab = tab
        self._setup_spacers()
        self._setup_layout()
        self.tab.freeform_generator_frame.show()

    def _setup_layout(self):
        self.tab.stacked_widget = QStackedWidget()
        self.tab.stacked_widget.addWidget(self.tab.freeform_generator_frame)
        self.tab.stacked_widget.addWidget(self.tab.circular_generator_frame)

        top_hbox = QHBoxLayout()
        top_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_hbox.addWidget(self.tab.customize_sequence_label)

        generate_button_hbox = QHBoxLayout()
        generate_button_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        generate_button_hbox.addWidget(self.tab.generate_sequence_button)

        self.tab.checkbox_layout = QHBoxLayout()
        self.tab.checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab.checkbox_layout.addWidget(self.tab.overwrite_checkbox)

        layout = self.tab.layout = QVBoxLayout(self.tab)
        layout.addLayout(top_hbox)
        layout.addWidget(self.tab.spacer_1)
        layout.addLayout(self.tab.button_layout)
        layout.addWidget(self.tab.stacked_widget)
        layout.addWidget(self.tab.spacer_2)
        layout.addLayout(generate_button_hbox)
        layout.addLayout(self.tab.checkbox_layout)
        layout.addWidget(self.tab.spacer_3)

        self.tab.setLayout(self.tab.layout)

    def _setup_spacers(self):
        spacers: list[GenerateTabSpacer] = []
        for _ in range(3):
            spacer = GenerateTabSpacer(self.tab)
            spacers.append(spacer)
        self.tab.spacer_1, self.tab.spacer_2, self.tab.spacer_3 = spacers
