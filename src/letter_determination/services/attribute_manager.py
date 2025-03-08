from typing import Optional
from data.constants import (
    ANTI,
    BEAT,
    BLUE,
    BLUE_ATTRS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    FLOAT,
    MOTION_TYPE,
    NO_ROT,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
)
from ..services.json_handler import LetterDeterminationJsonHandler


class AttributeManager:
    def __init__(self, json_handler: "LetterDeterminationJsonHandler"):
        self.json_handler = json_handler

    def sync_attributes(self, pictograph_data: dict) -> None:
        for color, attrs in [
            (BLUE, pictograph_data[BLUE_ATTRS]),
            (RED, pictograph_data[RED_ATTRS]),
        ]:
            if attrs[MOTION_TYPE] == FLOAT:
                other_attrs = (
                    pictograph_data[RED_ATTRS]
                    if color == BLUE
                    else pictograph_data[BLUE_ATTRS]
                )

                self._update_prefloat_attributes(attrs, other_attrs, pictograph_data[BEAT], color)

    def _update_prefloat_attributes(self, attrs: dict, other_attrs: dict, beat: int, color: str) -> None:
        prefloat_motion_type = self._determine_prefloat_motion_type(attrs, other_attrs)
        attrs[PREFLOAT_MOTION_TYPE] = prefloat_motion_type
        self.json_handler.update_prefloat_motion_type(beat, color, prefloat_motion_type)

        if other_attrs[MOTION_TYPE] in [PRO, ANTI]:
            prefloat_prop_rot_dir = self._get_opposite_rotation_direction(
                other_attrs[PROP_ROT_DIR]
                if other_attrs[PROP_ROT_DIR] != NO_ROT
                else other_attrs.get(PREFLOAT_PROP_ROT_DIR, NO_ROT)
            )
            attrs[PREFLOAT_PROP_ROT_DIR] = prefloat_prop_rot_dir
            self.json_handler.update_prefloat_prop_rot_dir(beat, color, prefloat_prop_rot_dir)

    def _determine_prefloat_motion_type(self, attrs: dict, other_attrs: dict) -> Optional[str]:
        if other_attrs[MOTION_TYPE] in [PRO, ANTI]:
            return other_attrs[MOTION_TYPE]
        if other_attrs[MOTION_TYPE] in [PRO, ANTI]:
            return other_attrs[PREFLOAT_MOTION_TYPE]
        if attrs[MOTION_TYPE] in [PRO, ANTI]:
            return attrs[MOTION_TYPE]
        return None

    def _get_opposite_rotation_direction(self, rotation: str) -> str:
        if rotation == CLOCKWISE:
            return COUNTER_CLOCKWISE
        elif rotation == COUNTER_CLOCKWISE:
            return CLOCKWISE
        else:
            raise ValueError(f"Invalid rotation direction: {rotation}")

    def _get_json_index(self, pictograph_data: dict) -> int:
        return pictograph_data[BEAT] + 1
