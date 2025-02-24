from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_view import (
    BeatView,
)
from utilities.reversal_detector import (
    ReversalDetector,
)


class BeatReversalProcessor:
    """Class to process reversals and update pictographs."""

    @staticmethod
    def process_reversals(sequence: list[dict], filled_beats: list["BeatView"]) -> None:
        """Process reversals and update pictographs before drawing."""
        sequence_so_far = []
        for i, (beat_dict, beat_view) in enumerate(zip(sequence[2:], filled_beats)):
            filtered_sequence_so_far = [
                beat
                for beat in sequence_so_far
                if not beat.get("sequence_start_position")
                and not beat.get("is_placeholder", False)
            ]

            reversal_info = ReversalDetector.detect_reversal(
                filtered_sequence_so_far, beat_dict
            )
            pictograph = beat_view.beat
            pictograph.blue_reversal = False
            pictograph.red_reversal = False
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)
            pictograph.elements.reversal_glyph.update_reversal_symbols()

            beat_view.update()
            beat_view.repaint()

            sequence_so_far.append(beat_dict)
