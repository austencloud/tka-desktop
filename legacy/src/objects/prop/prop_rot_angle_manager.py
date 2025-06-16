from typing import TYPE_CHECKING
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
from data.prop_class_mapping import PropType

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

        # Get orientation with fallback to IN
        key = (
            self.prop.state.ori
            if hasattr(self.prop, "state") and hasattr(self.prop.state, "ori")
            else IN
        )
        # Get location with fallback to NORTH
        loc = (
            self.prop.state.loc
            if hasattr(self.prop, "state")
            and hasattr(self.prop.state, "loc")
            and self.prop.state.loc
            else NORTH
        )
        rotation_angle = angle_map.get(key, {}).get(loc, 0)
        return (
            rotation_angle
            if not hasattr(self.prop, "prop_type_str")
            or self.prop.prop_type_str != "Hand"
            else 0
        )

    def get_box_rotation_angle(self) -> int:
        angle_map = {
            IN: {NORTHEAST: 135, NORTHWEST: 45, SOUTHWEST: 315, SOUTHEAST: 225},
            OUT: {NORTHEAST: 315, NORTHWEST: 225, SOUTHWEST: 135, SOUTHEAST: 45},
            CLOCK: {NORTHEAST: 45, NORTHWEST: 315, SOUTHWEST: 225, SOUTHEAST: 135},
            COUNTER: {NORTHEAST: 225, NORTHWEST: 135, SOUTHWEST: 45, SOUTHEAST: 315},
        }
        # Get orientation with fallback to IN
        key = (
            self.prop.state.ori
            if hasattr(self.prop, "state") and hasattr(self.prop.state, "ori")
            else IN
        )
        # Get location with fallback to NORTHEAST
        loc = (
            self.prop.state.loc
            if hasattr(self.prop, "state")
            and hasattr(self.prop.state, "loc")
            and self.prop.state.loc
            else NORTHEAST
        )
        rotation_angle = angle_map.get(key, {}).get(loc, 0)
        return (
            rotation_angle
            if not hasattr(self.prop, "prop_type_str")
            or self.prop.prop_type_str != "Hand"
            else 0
        )

    def update_prop_rot_angle(self) -> None:
        # Default to DIAMOND grid mode
        grid_mode = DIAMOND

        # Determine grid mode based on location if loc exists
        if (
            hasattr(self.prop, "state")
            and hasattr(self.prop.state, "loc")
            and self.prop.state.loc
        ):
            if self.prop.state.loc in ["n", "e", "s", "w"]:
                grid_mode = DIAMOND
            elif self.prop.state.loc in ["ne", "nw", "se", "sw"]:
                grid_mode = BOX

        # Default rotation angle
        prop_rotation_angle = 0

        # Calculate rotation angle based on grid mode
        if grid_mode == DIAMOND:
            prop_rotation_angle = self.get_diamond_rotation_angle()
        elif grid_mode == BOX:
            prop_rotation_angle = self.get_box_rotation_angle()

        # Apply rotation
        self.prop.setTransformOriginPoint(self.prop.boundingRect().center())
        self.prop.setRotation(prop_rotation_angle)
