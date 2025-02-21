from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, QSize
from typing import TYPE_CHECKING, Callable

from Enums.Enums import Letter
from base_widgets.pictograph.pictograph_scene import PictographScene
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
    SequenceBeatFrame,
)


from .start_pos_picker.start_pos_picker import StartPosPicker
from .advanced_start_pos_picker.advanced_start_pos_picker import AdvancedStartPosPicker
from .add_to_sequence_manager import AddToSequenceManager
from .option_picker.option_picker import OptionPicker

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager
    from main_window.main_widget.json_manager.json_manager import JsonManager


class ConstructTab(QFrame):
    start_position_selected = pyqtSignal(object)

    start_pos_picker_index = 0
    advanced_start_pos_picker_index = 1
    option_picker_index = 2

    def __init__(
        self,
        settings_manager: "SettingsManager",
        json_manager: "JsonManager",
        beat_frame: "SequenceBeatFrame",
        pictograph_dataset: dict,
        size_provider: Callable[[], QSize],
        fade_to_stack_index: Callable[[int], None],
        fade_manager: "FadeManager",
    ) -> None:
        super().__init__()

        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.beat_frame = beat_frame
        self.pictograph_dataset = pictograph_dataset
        self.mw_size_provider = size_provider
        self.fade_to_stack_index = fade_to_stack_index
        self.fade_manager = fade_manager
        self.last_beat: "PictographScene" = None
        self.start_position_picked = False

        self.pictograph_cache: dict[Letter, dict[str, PictographScene]] = {
            letter: {} for letter in Letter
        }

        self.add_to_sequence_manager = AddToSequenceManager(
            json_manager=self.json_manager,
            beat_frame=self.beat_frame,
            last_beat=self.last_beat,
        )

        self.option_picker = OptionPicker(
            add_to_sequence_manager=self.add_to_sequence_manager,
            pictograph_dataset=self.pictograph_dataset,
            beat_frame=self.beat_frame,
            mw_size_provider=self.mw_size_provider,
            fade_manager=self.fade_manager,
        )

        self.start_pos_picker = StartPosPicker(
            self.pictograph_dataset,
            self.beat_frame,
            self.mw_size_provider,
            option_click_handler=self.option_picker.option_click_handler,
            advnaced_transition_handler=self.transition_to_advanced_start_pos_picker,
        )
        self.advanced_start_pos_picker = AdvancedStartPosPicker(
            self.pictograph_dataset, self.beat_frame, self.mw_size_provider
        )

        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

    def transition_to_option_picker(self):
        """Transition to the option picker view."""
        self.fade_to_stack_index(self.option_picker_index)

    def transition_to_advanced_start_pos_picker(self) -> None:
        """Transition to the advanced start position picker."""
        self.fade_to_stack_index(self.advanced_start_pos_picker_index)
        self.advanced_start_pos_picker.display_variations()

    def transition_to_start_pos_picker(self) -> None:
        """Reset the view back to the start position picker."""
        self.fade_to_stack_index(self.start_pos_picker_index)
