from dataclasses import dataclass, field
from typing import Optional, Union

from Enums.Enums import Letter
from Enums.PropTypes import PropType
from Enums.letters import LetterType
from data.constants import BLUE_ATTRIBUTES, LETTER, RED_ATTRIBUTES


@dataclass
class PictographState:
    pictograph_data: dict[str, Union[str, dict[str, str]]] = field(default_factory=dict)
    is_blank: bool = False
    disable_gold_overlay: bool = False
    blue_reversal: bool = False
    red_reversal: bool = False
    letter: Optional[Letter] = None
    letter_type: Optional[LetterType] = None
    prop_type: Optional[PropType] = None
    open_close_state: str = ""
    vtg_mode: str = ""
    direction: str = ""
    start_pos: str = ""
    end_pos: str = ""
    timing: str = ""
    turns_tuple: str = ""
    grid_mode: str = ""

    def update_pictograph_state(
        self, pictograph_data: dict[str, Union[str, dict[str, str]]]
    ) -> None:
        for key, value in pictograph_data.items():
            if key == LETTER:
                try:
                    letter_obj: Letter = Letter.get_letter(value)
                except KeyError:
                    letter_obj = value
                self.letter = letter_obj
                self.pictograph_data[LETTER] = (
                    letter_obj.value if hasattr(letter_obj, "value") else letter_obj
                )
                self.letter_type = LetterType.get_letter_type(letter_obj)
                self.pictograph_data["letter_type"] = self.letter_type.name
            elif key in (BLUE_ATTRIBUTES, RED_ATTRIBUTES):
                if key not in self.pictograph_data:
                    self.pictograph_data[key] = {}
                if isinstance(value, dict):
                    deep_merge_dict(self.pictograph_data[key], value)
                else:
                    self.pictograph_data[key] = value
            else:
                setattr(self, key, value)
                self.pictograph_data[key] = value


def deep_merge_dict(dest: dict, src: dict) -> dict:
    for key, value in src.items():
        if key in dest and isinstance(dest[key], dict) and isinstance(value, dict):
            deep_merge_dict(dest[key], value)
        else:
            dest[key] = value
    return dest
