from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedWidget

from data.constants import GRID_MODE
from .author_section import AuthorSection
from .contains_letter_section import ContainsLettersSection
from .initial_filter_choice_widget.initial_filter_choice_widget import (
    InitialFilterChoiceWidget,
)
from .grid_mode_section import GridModeSection
from .level_section import LevelSection
from .sequence_length_section import SequenceLengthSection
from .starting_letter_section import StartingLetterSection
from .starting_position_section import StartingPositionSection

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


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
        self.level_section = LevelSection(self)
        self.starting_position_section = StartingPositionSection(self)
        self.author_section = AuthorSection(self)
        self.grid_mode_section = GridModeSection(self)

        self.section_map: dict[str, QWidget] = {
            "filter_selector": self.initial_filter_choice_widget,
            "starting_letter": self.starting_letter_section,
            "contains_letters": self.contains_letter_section,
            "sequence_length": self.length_section,
            "level": self.level_section,
            "starting_position": self.starting_position_section,
            "author": self.author_section,
            GRID_MODE: self.grid_mode_section,
        }

        self.section_indexes = {}
        for name, widget in self.section_map.items():
            index = self.addWidget(widget)
            self.section_indexes[name] = index
        self.current_filter_section: str = "filter_selector"

    def show_section(self, section_name: str):
        index = self.section_indexes.get(section_name)
        if index is not None:
            self.sequence_picker.main_widget.fade_manager.stack_fader.fade_stack(
                self.sequence_picker.filter_stack, index
            )
            self.browse_tab.browse_settings.set_current_section(section_name)
            self.current_filter_section = section_name
        else:
            print(f"Section '{section_name}' not found.")

    def show_filter_choice_widget(self):
        self.show_section("filter_selector")
