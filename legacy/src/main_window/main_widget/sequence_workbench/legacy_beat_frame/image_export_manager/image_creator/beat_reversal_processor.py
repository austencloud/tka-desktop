from data.constants import SEQUENCE_START_POSITION
from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from utils.reversal_detector import (
    ReversalDetector,
)


class BeatReversalProcessor:
    """Class to process reversals and update pictographs."""

    @staticmethod
    def process_reversals(
        sequence: list[dict], filled_beats: list["LegacyBeatView"]
    ) -> None:
        """Process reversals and update pictographs before drawing."""
        sequence_so_far = []
        for i, (beat_data, beat_view) in enumerate(zip(sequence[2:], filled_beats)):
            filtered_sequence_so_far = [
                beat
                for beat in sequence_so_far
                if not beat.get(SEQUENCE_START_POSITION)
                and not beat.get("is_placeholder", False)
            ]

            reversal_info = ReversalDetector.detect_reversal(
                filtered_sequence_so_far, beat_data
            )
            pictograph = beat_view.beat
            pictograph.state.blue_reversal = False
            pictograph.state.red_reversal = False
            pictograph.state.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.state.red_reversal = reversal_info.get("red_reversal", False)
            pictograph.elements.reversal_glyph.update_reversal_symbols()

            beat_view.update()
            beat_view.repaint()

            sequence_so_far.append(beat_data)
