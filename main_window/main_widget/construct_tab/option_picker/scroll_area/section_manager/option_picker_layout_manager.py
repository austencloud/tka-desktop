from typing import TYPE_CHECKING
from Enums.Enums import LetterType
from Enums.letters import Letter
from .option_picker_section_group_widget import OptionPickerSectionGroupWidget
from .option_picker_section_widget import OptionPickerSectionWidget
from PyQt6.QtWidgets import QHBoxLayout

if TYPE_CHECKING:

    from ..option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerLayoutManager:
    """
    Manages all of the sections in the scroll area.
    Individual sections are managed by the OptionPickerSectionWidget class.
    """

    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        self.scroll_area = scroll_area
        self.construct_tab = scroll_area.construct_tab
        self.sections: dict[LetterType, OptionPickerSectionWidget] = {}
        self.pictograph_cache: dict[Letter, list[LetterType]] = {}
        self.ordered_section_types: list[LetterType] = []
        self.initialize_sections()

    def initialize_sections(self) -> None:
        self._create_sections()
        self.add_sections_to_layout()

    def _create_sections(self):
        for letter_type in LetterType:
            section = OptionPickerSectionWidget(letter_type, self.scroll_area)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()

    def add_sections_to_layout(self) -> None:
        grouped_sections = [LetterType.Type4, LetterType.Type5, LetterType.Type6]
        group_widget = None

        for letter_type in list(LetterType):
            section = self.sections.get(letter_type)
            if section:
                if letter_type in grouped_sections:
                    if group_widget is None:
                        group_widget = OptionPickerSectionGroupWidget(self.scroll_area)
                        group_layout = QHBoxLayout()
                        group_layout.addStretch()
                        group_layout.addWidget(group_widget)
                        group_layout.addStretch()
                        self.scroll_area.layout.addLayout(group_layout, 3)
                    group_widget.add_section_widget(section)
                elif letter_type == LetterType.Type1:
                    self.scroll_area.layout.addWidget(section, 3)
                else:
                    self.scroll_area.layout.addWidget(section, 3)
