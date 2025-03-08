# services/attribute_manager.py
from typing import Optional

from data.constants import (
    BEAT,
    BLUE,
    BLUE_ATTRS,
    FLOAT,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
)
from ..models.pictograph import PictographData
from ..models.motion import MotionAttributes, str, str
from ..services.json_handler import LetterDeterminationJsonHandler


class AttributeManager:
    def __init__(self, json_handler: "LetterDeterminationJsonHandler"):
        self.json_handler = json_handler

    def sync_attributes(self, pictograph_data: PictographData) -> None:
        """Ensure prefloat attributes are updated in pictograph data and stored in JSON."""
        for color, attrs in [
            ("blue", pictograph_data[BLUE_ATTRS]),
            (RED, pictograph_data[RED_ATTRS]),
        ]:
            if attrs[MOTION_TYPE] == FLOAT:
                other_attrs = (
                    pictograph_data[RED_ATTRS]
                    if color == BLUE
                    else pictograph_data[BLUE_ATTRS]
                )

                # Update prefloat motion type
                attrs[PREFLOAT_MOTION_TYPE] = other_attrs[MOTION_TYPE]
                self.json_handler.update_prefloat_motion_type(
                    pictograph_data[BEAT], color, other_attrs[MOTION_TYPE]
                )

                # Update prefloat prop rotation direction
                attrs[PREFLOAT_PROP_ROT_DIR] = self._get_opposite_rotation_direction(
                    other_attrs[PROP_ROT_DIR]
                )
                self.json_handler.update_prefloat_prop_rot_dir(
                    pictograph_data[BEAT], color, attrs[PREFLOAT_PROP_ROT_DIR]
                )

    def _get_opposite_rotation_direction(self, rotation: str) -> str:
        if rotation == str.CLOCKWISE.value:
            return str.COUNTER_CLOCKWISE.value
        elif rotation == str.COUNTER_CLOCKWISE.value:
            return str.CLOCKWISE.value
        else:
            raise ValueError(f"Invalid rotation direction: {rotation}")

    def _update_prefloat_from_storage(self, pictograph: PictographData) -> None:
        json_index = self._get_json_index(pictograph)

        for color in [BLUE, RED]:
            attr: MotionAttributes = getattr(pictograph, f"{color}_attributes")
            if attr.is_float:
                stored_motion_type = self.json_handler.get_json_prefloat_motion_type(
                    json_index, color
                )
                if stored_motion_type:
                    attr.prefloat_motion_type = str(stored_motion_type)

                stored_rotation = self.json_handler.get_json_prefloat_prop_rot_dir(
                    json_index, color
                )
                if stored_rotation:
                    attr.prefloat_prop_rot_dir = str(stored_rotation)

    def _update_float_attributes(
        self, attr: MotionAttributes, pictograph: PictographData, color: str
    ) -> None:
        other_color = RED if color == BLUE else BLUE
        other_attr: MotionAttributes = getattr(pictograph, f"{other_color}_attributes")

        attr.prefloat_motion_type = other_attr.motion_type
        json_index = self._get_json_index(pictograph)
        self.json_handler.update_prefloat_motion_type(
            json_index, color, other_attr.motion_type
        )

        if other_attr.motion_type in [str.PRO, str.ANTI]:
            new_rotation = self._calculate_prop_rotation(
                other_attr, pictograph.direction
            )
            attr.prefloat_prop_rot_dir = new_rotation
            self.json_handler.update_prefloat_rotation(json_index, color, new_rotation)

    def _calculate_prop_rotation(self, attr: MotionAttributes, direction: str) -> str:
        base_rotation = attr.prop_rot_dir
        if direction == "opp":
            return self._reverse_rotation(base_rotation)
        return base_rotation

    def _reverse_rotation(self, rotation: str) -> str:
        if rotation == str.CLOCKWISE:
            return str.COUNTER_CLOCKWISE
        return str.CLOCKWISE

    def _save_current_state(self, pictograph: PictographData) -> None:
        """Ensure prefloat motion type and rotation direction are stored in JSON."""
        json_index = self._get_json_index(pictograph)

        for color in ["blue", RED]:
            attr: MotionAttributes = getattr(pictograph, f"{color}_attributes")

            if attr.is_float:
                if attr.prefloat_motion_type:
                    self.json_handler.update_prefloat_motion_type(
                        json_index, color, attr.prefloat_motion_type.value
                    )

                if attr.prefloat_prop_rot_dir:
                    self.json_handler.update_prefloat_prop_rot_dir(
                        json_index, color, attr.prefloat_prop_rot_dir.value
                    )

    def _get_json_index(self, pictograph: PictographData) -> int:
        return pictograph.beat + 2

    def update_prefloat_attributes(
        red_attrs: MotionAttributes, blue_attrs: MotionAttributes
    ) -> None:
        """Update prefloat attributes based on the given red and blue attributes."""
        red_attrs.prefloat_motion_type = blue_attrs.motion_type
        red_attrs.prefloat_prop_rot_dir = blue_attrs.prop_rot_dir

    # In letter_determination/services/attribute_manager.py
    def update_json_prefloat_attrs(self, pictograph: PictographData, color: str):
        json_index = self.json_handler.get_current_json_index()

        # Update motion type
        self.json_handler.update_prefloat_motion_type(
            json_index, color, pictograph.get_attributes(color).prefloat_motion_type
        )

        # Update prop rotation direction
        self.json_handler.update_prefloat_prop_rot_dir(
            json_index, color, pictograph.get_attributes(color).prefloat_prop_rot_dir
        )
