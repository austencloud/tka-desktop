from typing import TYPE_CHECKING
from enums.letter.letter_type import LetterType


from enums.letter.letter import Letter

from data.constants import (
    FLOAT,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat
from main_window.main_widget.sequence_workbench.legacy_beat_frame.start_pos_beat import (
    StartPositionBeat,
)


if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class BeatFactory:
    def __init__(self, beat_frame: "LegacyBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget

    def create_start_pos_beat(
        self, pictograph_key: str, pictograph_data=None
    ) -> StartPositionBeat:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_data is not None:
            start_pos_beat = StartPositionBeat(self.beat_frame)
            start_pos_beat.managers.updater.update_pictograph(pictograph_data)

            if letter not in self.beat_frame.main_widget.pictograph_cache:
                self.beat_frame.main_widget.pictograph_cache[letter] = {}
            self.beat_frame.main_widget.pictograph_cache[letter][
                pictograph_key
            ] = start_pos_beat
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            return start_pos_beat

        raise ValueError(
            "BasePictograph dict is required for creating a new pictograph."
        )

    def create_new_beat_and_add_to_sequence(
        self,
        pictograph_data: dict,
        override_grow_sequence=False,
        update_word=True,
        update_level=True,
        reversal_info: dict = None,
        select_beat: bool = True,
        update_image_export_preview: bool = True,
    ) -> None:
        new_beat = Beat(self.beat_frame, duration=pictograph_data.get("duration", 1))
        new_beat.managers.updater.update_pictograph(pictograph_data)

        if reversal_info:
            new_beat.state.blue_reversal = reversal_info.get("blue_reversal", False)
            new_beat.state.red_reversal = reversal_info.get("red_reversal", False)

        self.beat_frame.beat_adder.add_beat_to_sequence(
            new_beat,
            override_grow_sequence=override_grow_sequence,
            update_word=update_word,
            update_level=update_level,
            select_beat=select_beat,
            update_image_export_preview=update_image_export_preview,
        )
        for motion in new_beat.elements.motion_set.values():
            if motion.state.motion_type == FLOAT:
                letter = self.main_widget.letter_determiner.determine_letter(
                    pictograph_data
                )
                new_beat.state.letter = letter
                new_beat.elements.tka_glyph.update_tka_glyph()
        # Update sequence properties with graceful fallback for MainWidgetCoordinator refactoring
        if (
            hasattr(self.main_widget, "sequence_properties_manager")
            and self.main_widget.sequence_properties_manager
        ):
            self.main_widget.sequence_properties_manager.update_sequence_properties()
        else:
            # Graceful fallback if sequence_properties_manager is not available yet
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(
                "sequence_properties_manager not available yet - this is normal during initialization"
            )
        self.beat_frame.sequence_workbench.graph_editor.pictograph_container.update_pictograph(
            new_beat
        )
