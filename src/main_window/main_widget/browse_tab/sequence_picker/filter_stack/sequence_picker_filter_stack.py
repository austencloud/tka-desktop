from typing import TYPE_CHECKING
from enum import Enum
from PyQt6.QtWidgets import QWidget, QStackedWidget

from .author_section import AuthorSection
from .contains_letter_section import ContainsLettersSection
from .initial_filter_choice_widget.initial_filter_choice_widget import (
    InitialFilterChoiceWidget,
)
from .grid_mode_section import GridModeSection
from .filter_by_level_section import FilterByLevelSection
from .sequence_length_section import SequenceLengthSection
from .starting_letter_section import StartingLetterSection
from .starting_position_section import StartingPositionSection

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class BrowseTabSection(Enum):
    FILTER_SELECTOR = "filter_selector"
    STARTING_LETTER = "starting_letter"
    CONTAINS_LETTERS = "contains_letters"
    SEQUENCE_LENGTH = "sequence_length"
    LEVEL = "level"
    STARTING_POSITION = "starting_position"
    AUTHOR = "author"
    GRID_MODE = "grid_mode"
    SEQUENCE_PICKER = "sequence_picker"

    # write a function to get the enum from the string
    @staticmethod
    def from_str(string: str) -> "BrowseTabSection":
        for section in BrowseTabSection:
            if section.value == string:
                return section
        raise ValueError(f"Invalid filter section: {string}")


class SequencePickerFilterStack(QStackedWidget):
    """Widget for initial filter selections in the dictionary browser."""

    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.browse_tab = sequence_picker.browse_tab
        self.selected_letters: set[str] = set()

        # Initialize sections
        self.initial_filter_choice_widget = InitialFilterChoiceWidget(self)
        self.starting_letter_section = StartingLetterSection(self)
        self.contains_letter_section = ContainsLettersSection(self)
        self.length_section = SequenceLengthSection(self)
        self.level_section = FilterByLevelSection(self)
        self.start_pos_section = StartingPositionSection(self)
        self.author_section = AuthorSection(self)
        self.grid_mode_section = GridModeSection(self)

        self.section_map: dict[BrowseTabSection, QWidget] = {
            BrowseTabSection.FILTER_SELECTOR: self.initial_filter_choice_widget,
            BrowseTabSection.STARTING_LETTER: self.starting_letter_section,
            BrowseTabSection.CONTAINS_LETTERS: self.contains_letter_section,
            BrowseTabSection.SEQUENCE_LENGTH: self.length_section,
            BrowseTabSection.LEVEL: self.level_section,
            BrowseTabSection.STARTING_POSITION: self.start_pos_section,
            BrowseTabSection.AUTHOR: self.author_section,
            BrowseTabSection.GRID_MODE: self.grid_mode_section,
        }

        self.section_indexes = {}
        for name, widget in self.section_map.items():
            index = self.addWidget(widget)
            self.section_indexes[name] = index
        self.current_filter_section: BrowseTabSection = BrowseTabSection.FILTER_SELECTOR

    def show_section(self, filter_section_str: str):
        # convert the str to an enum
        try:
            filter_section_enum = BrowseTabSection.from_str(filter_section_str)
            index = self.section_indexes.get(filter_section_enum)
            if index is not None:
                self.sequence_picker.main_widget.fade_manager.stack_fader.fade_stack(
                    self.sequence_picker.filter_stack, index
                )
                self.browse_tab.browse_settings.set_current_section(
                    filter_section_enum.value
                )
                self.current_filter_section = filter_section_enum
            else:
                print(
                    f"Section '{filter_section_str}' not found. Did you spell it correctly?"
                )
        except ValueError as e:
            print(e)
            # Optionally, you can show a default section or keep the current section
            self.show_filter_selection_widget()

    def show_filter_selection_widget(self):
        self.show_section(BrowseTabSection.FILTER_SELECTOR.value)
