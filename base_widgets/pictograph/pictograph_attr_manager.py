from typing import TYPE_CHECKING, Union
from Enums.Enums import Letter
from Enums.letters import LetterType

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class PictographAttrManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def load_from_dict(self, data: dict[str, Union[str, dict[str, str]]]) -> None:
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
                value = data[data_key]
                setattr(self.pictograph.state, attr_name, value)
                self.pictograph.state.pictograph_data[attr_name] = value

        if "letter" in data:
            letter = self._convert_letter(data["letter"])
            self.pictograph.state.letter = letter
            self.pictograph.state.pictograph_data["letter"] = letter.value

        for color_key in ["blue_attributes", "red_attributes"]:
            if color_key in data:
                self.pictograph.state.pictograph_data.setdefault(color_key, {}).update(
                    data[color_key]
                )

    def _convert_letter(self, letter_str: str) -> Union[LetterType, str]:
        try:
            return Letter.get_letter(letter_str)
        except KeyError:
            return letter_str
