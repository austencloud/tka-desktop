from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from data.constants import (
    BOX,
    DIAMOND,
    IN,
    NORTHEAST,
    NORTHWEST,
    OUT,
    CLOCK,
    COUNTER,
    NORTH,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    WEST,
    EAST,
)

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropRotAngleManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def get_diamond_rotation_angle(self) -> int:
        angle_map = {
            IN: {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            OUT: {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            CLOCK: {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            COUNTER: {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }

        key = self.prop.ori
        rotation_angle = angle_map.get(key, {}).get(self.prop.loc, 0)
        return rotation_angle if self.prop.prop_type_str != PropType.Hand else 0

    def get_box_rotation_angle(self) -> int:
        angle_map = {
            IN: {NORTHEAST: 135, NORTHWEST: 45, SOUTHWEST: 315, SOUTHEAST: 225},
            OUT: {NORTHEAST: 315, NORTHWEST: 225, SOUTHWEST: 135, SOUTHEAST: 45},
            CLOCK: {NORTHEAST: 45, NORTHWEST: 315, SOUTHWEST: 225, SOUTHEAST: 135},
            COUNTER: {NORTHEAST: 225, NORTHWEST: 135, SOUTHWEST: 45, SOUTHEAST: 315},
        }
        key = self.prop.ori
        rotation_angle = angle_map.get(key, {}).get(self.prop.loc, 0)
        return rotation_angle if self.prop.prop_type_str != PropType.Hand else 0

    def update_prop_rot_angle(self) -> None:
        if self.prop.loc in ["n", "e", "s", "w"]:
            grid_mode = DIAMOND
        elif self.prop.loc in ["ne", "nw", "se", "sw"]:
            grid_mode = BOX
        if grid_mode == DIAMOND:
            prop_rotation_angle = self.get_diamond_rotation_angle()
        elif grid_mode == BOX:
            prop_rotation_angle = self.get_box_rotation_angle()
        self.prop.setTransformOriginPoint(self.prop.boundingRect().center())
        self.prop.setRotation(prop_rotation_angle)
