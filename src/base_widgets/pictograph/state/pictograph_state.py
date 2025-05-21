from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, Union

from enums.letter.letter import Letter
from enums.letter.letter_type import LetterType
from data.constants import BLUE_ATTRS, LETTER, RED_ATTRS
from enums.prop_type import PropType


@dataclass
class PictographState:
    pictograph_data: dict[str, Union[str, dict[str, str]]] = field(default_factory=dict)
    is_blank: bool = False
    disable_gold_overlay: bool = False
    disable_borders: bool = False  # Added flag to disable borders
    blue_reversal: bool = False
    red_reversal: bool = False
    hide_tka_glyph: bool = False
    letter: Optional[Letter] = None
    letter_type: Optional[LetterType] = None
    prop_type_enum: Optional[PropType] = None
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
        copied_data = deepcopy(pictograph_data)  # Deep copy the entire structure

        for key, value in copied_data.items():
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

            elif key in (BLUE_ATTRS, RED_ATTRS):
                if key not in self.pictograph_data:
                    self.pictograph_data[key] = {}

                # Ensure deep copy for attributes
                self.pictograph_data[key] = deepcopy(value)

            elif key == "letter_type":
                self.letter_type = LetterType.from_string(value)
                self.pictograph_data[key] = self.letter_type.name

            else:
                setattr(self, key, value)
                self.pictograph_data[key] = value


def deep_merge_dict(dest: dict, src: dict) -> dict:
    merged = deepcopy(dest)  # Ensure we don't modify the original dictionary

    for key, value in src.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge_dict(merged[key], value)
        else:
            merged[key] = deepcopy(value)  # Ensure deep copy of values

    return merged
