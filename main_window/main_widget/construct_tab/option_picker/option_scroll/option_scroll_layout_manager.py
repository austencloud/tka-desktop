from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from Enums.Enums import LetterType
from .section_widget.option_picker_section_group_widget import (
    OptionPickerSectionGroupWidget,
)
from .section_widget.option_picker_section_widget import OptionPickerSectionWidget


if TYPE_CHECKING:
    from .option_scroll import OptionScroll


class OptionScrollLayoutManager:
    """Manages the layout of the OptionScroll."""

    def __init__(self, option_scroll: "OptionScroll") -> None:
        self.os = option_scroll
        self._setup_layout()
        self.initialize_sections()

    def initialize_sections(self) -> None:
        self._create_sections()
        self.add_sections_to_layout()

    def _create_sections(self):
        for letter_type in LetterType:
            section = OptionPickerSectionWidget(letter_type, self.os)
            self.os.sections[letter_type] = section
            section.setup_components()

    def add_sections_to_layout(self) -> None:
        grouped_sections = [LetterType.Type4, LetterType.Type5, LetterType.Type6]
        group_widget = None

        for letter_type in list(LetterType):
            section = self.os.sections.get(letter_type)
            if section:
                if letter_type in grouped_sections:
                    if group_widget is None:
                        group_widget = OptionPickerSectionGroupWidget(self.os)
                        group_layout = QHBoxLayout()
                        group_layout.addStretch()
                        group_layout.addWidget(group_widget)
                        group_layout.addStretch()
                        self.os.layout.addLayout(group_layout, 3)
                    group_widget.add_section_widget(section)
                else:
                    self.os.layout.addWidget(section, 3)

    def _setup_layout(self):
        self.os.setWidgetResizable(True)
        self.os.setContentsMargins(0, 0, 0, 0)
        self.os.setStyleSheet("background-color: transparent; border: none;")

        self.os.layout = QVBoxLayout()
        self.os.layout.setContentsMargins(0, 0, 0, 0)
        self.os.layout.setSpacing(0)
        self.os.layout.setContentsMargins(0, 0, 0, 0)

        self.os.container = QWidget()
        self.os.container.setAutoFillBackground(True)
        self.os.container.setStyleSheet("background: transparent;")
        self.os.container.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self.os.container.setLayout(self.os.layout)
        self.os.setWidget(self.os.container)

        self.os.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.os.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.os.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.os.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
