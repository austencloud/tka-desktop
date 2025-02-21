from typing import TYPE_CHECKING, Union
from Enums.Enums import Letter
from Enums.letters import LetterType


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class PictographAttrManager:
    """Manages attribute assignment for the PictographScene."""

    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def load_from_dict(self, data: dict[str, Union[str, dict[str, str]]]) -> None:
        """Loads pictograph attributes from a dictionary and assigns them to the right subcomponent."""

        # ==== STATE ATTRIBUTES ====
        state_mapping = {
            "sequence_start_position": "sequence_start_pos",
            "letter": "letter",
            "start_pos": "start_pos",
            "end_pos": "end_pos",
            "timing": "timing",
            "direction": "direction",
        }

        for data_key, attr_name in state_mapping.items():
            if data_key in data:
                setattr(self.pictograph.state, attr_name, data[data_key])

        # Handle Enums separately
        if "letter" in data:
            self.pictograph.state.letter = self._convert_letter(data["letter"])

    def _convert_letter(self, letter_str: str) -> Union[LetterType, str]:
        """Converts a letter string into a LetterType enum if possible, otherwise returns it as a string."""
        try:
            return Letter.get_letter(letter_str)
        except KeyError:
            return letter_str  # Fallback to raw string if not found in LetterType
