from typing import TYPE_CHECKING
from data.constants import LETTER, SEQUENCE_START_POSITION
from main_window.settings_manager.global_settings.app_context import AppContext
from utilities.reversal_detector import ReversalDetector
from utilities.word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from .sequence_beat_frame import SequenceBeatFrame
from PyQt6.QtCore import QTimer


class BeatFramePopulator:
    loading_text = "Loading sequence..."

    def __init__(self, beat_frame: "SequenceBeatFrame"):
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.sequence_workbench = beat_frame.sequence_workbench
        self.start_pos_view = beat_frame.start_pos_view
        self.selection_overlay = beat_frame.selection_overlay
        self.current_sequence_json = []  # Initialize the instance variable

    def populate_beat_frame_from_json(
        self,
        current_sequence_json: list[dict[str, str]],
        initial_state_load: bool = False,
    ) -> None:
        """
        Populates the beat frame with data from a JSON representation of a sequence.

        This method orchestrates the process of loading a sequence from JSON, updating
        various UI elements, and preparing the beat frame for editing.

        Args:
            current_sequence_json (list[dict[str, str]]): The JSON representation of the sequence.
            initial_state_load (bool, optional): Indicates whether this is an initial load. Defaults to False.
        """
        self.current_sequence_json = current_sequence_json  # Store the sequence JSON
        indicator_label = self.sequence_workbench.indicator_label
        indicator_label.show_message(self.loading_text)
        AppContext.json_manager().loader_saver.clear_current_sequence_file()
        self.construct_tab = self.main_widget.construct_tab

        if not self.current_sequence_json:
            return  # Nothing to do, eh?

        self.beat_frame.updater.reset_beat_frame()
        self._set_start_position()
        self._update_sequence_layout()
        self._update_sequence_word()
        self._update_difficulty_level()
        self._populate_beats(select_beat=False)
        self._finalize_sequence(initial_state_load)

        indicator_label.show_message(
            f"{self.current_word} loaded successfully! Ready to edit."
        )

    def _set_start_position(self):
        """Sets the start position in the UI based on the loaded sequence data."""
        start_pos_picker = self.construct_tab.start_pos_picker
        start_pos_beat = start_pos_picker.convert_current_sequence_json_entry_to_start_pos_pictograph(
            self.current_sequence_json
        )
        AppContext.json_manager().start_pos_handler.set_start_position_data(
            start_pos_beat
        )
        self.start_pos_view.set_start_pos(start_pos_beat)

    def _update_sequence_layout(self):
        """Updates the sequence layout based on the number of beats."""
        length = len(self.current_sequence_json) - 2
        self.modify_layout_for_chosen_number_of_beats(length)

    def _update_difficulty_level(self):
        """Updates the difficulty level label in the UI."""
        if len(self.current_sequence_json) > 2:
            self.sequence_workbench.difficulty_label.update_difficulty_label()
        else:
            self.sequence_workbench.difficulty_label.set_difficulty_level("")

    def _update_sequence_word(self):
        """Updates the sequence word label in the UI."""
        self.current_word = "".join(
            [beat[LETTER] for beat in self.current_sequence_json[2:] if LETTER in beat]
        )
        self.current_word = WordSimplifier.simplify_repeated_word(self.current_word)
        self.sequence_workbench.current_word_label.set_current_word(self.current_word)

    def _populate_beats(self, select_beat=True):
        """Populates the beat frame with beats from the sequence data."""
        for _, pictograph_data in enumerate(self.current_sequence_json[1:]):
            if pictograph_data.get(SEQUENCE_START_POSITION) or pictograph_data.get(
                "is_placeholder", False
            ):
                continue  # Skip start positions and placeholders.  We don't need those.

            reversal_info = ReversalDetector.detect_reversal(
                self.current_sequence_json, pictograph_data
            )
            self.sequence_workbench.sequence_beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                pictograph_data,
                override_grow_sequence=True,
                update_word=False,
                update_level=False,
                reversal_info=reversal_info,
                select_beat=select_beat,
            )

    def _finalize_sequence(self, initial_state_load):
        """Finalizes the sequence loading process, selecting the last beat and updating options."""
        last_beat = (
            self.sequence_workbench.sequence_beat_frame.get.last_filled_beat().beat
        )
        self.construct_tab.last_beat = last_beat
        self.construct_tab.option_picker.updater.update_options()

        # Use a single shot timer to select the last beat after the UI has updated.
        # This avoids potential issues with immediate updates.
        if initial_state_load:
            target_tab = AppContext.settings_manager().global_settings.get_current_tab()
            toggle_animation = (
                target_tab == "construct"
            )  # Only select if on the construct tab.
            QTimer.singleShot(
                0,
                lambda: self.selection_overlay.select_beat_view(
                    last_beat.view, toggle_animation
                ),
            )

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        """Configures the beat frame layout for the specified number of beats."""
        self.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )
