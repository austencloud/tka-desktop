from enums.letter.letter_type import LetterType
from data.constants import (
    PRO,
    ANTI,
    FLOAT,
    DASH,
    STATIC,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NO_ROT,
    DIAMOND,
    BOX,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    BLUE,
    RED,
    CW_HANDPATH,
    CCW_HANDPATH,
)
from objects.motion.motion import Motion
from objects.motion.managers.handpath_calculator import HandpathCalculator  # RESTORED!


class DirectionalTupleGenerator:
    """Handles directional tuple generation for all motion types, exactly preserving original behavior."""

    _handpath_calculator = HandpathCalculator()  # RESTORED!

    # Special cases for Type5 motions
    _special_type5_cases = {
        DIAMOND: {
            (NORTH, SOUTH): lambda x, y: [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (SOUTH, NORTH): lambda x, y: [(x, -y), (-y, x), (-x, y), (y, x)],
            (EAST, WEST): lambda x, y: [(x, y), (-y, -x), (x, -y), (y, x)],
            (WEST, EAST): lambda x, y: [(-x, y), (-y, -x), (-x, -y), (y, x)],
        },
        BOX: {
            (NORTHEAST, SOUTHWEST): lambda x, y: [
                (x, y),
                (y, x),
                (-x, -y),
                (y, x),
            ],
            (NORTHWEST, SOUTHEAST): lambda x, y: [
                (x, -y),
                (-y, -x),
                (x, -y),
                (y, x),
            ],
            (SOUTHEAST, NORTHWEST): lambda x, y: [
                (-x, y),
                (-y, -x),
                (-x, y),
                (y, x),
            ],
        },
    }

    # Grid quadrant mappings
    _quadrant_map = {
        DIAMOND: {NORTHEAST: 0, SOUTHEAST: 1, SOUTHWEST: 2, NORTHWEST: 3},
        BOX: {NORTH: 0, EAST: 1, SOUTH: 2, WEST: 3},
    }

    # Mappings for PRO and ANTI motions
    _shift_mapping_diamond = {
        PRO: {
            CLOCKWISE: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
            COUNTER_CLOCKWISE: lambda x, y: [(-y, -x), (x, -y), (y, x), (-x, y)],
        },
        ANTI: {
            CLOCKWISE: lambda x, y: [(-y, -x), (x, -y), (y, x), (-x, y)],
            COUNTER_CLOCKWISE: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
        },
    }
    _shift_mapping_box = {
        PRO: {
            CLOCKWISE: lambda x, y: [(-x, y), (-y, -x), (x, -y), (y, x)],
            COUNTER_CLOCKWISE: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
        },
        ANTI: {
            CLOCKWISE: lambda x, y: [(-x, y), (-y, -x), (x, -y), (y, x)],
            COUNTER_CLOCKWISE: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
        },
    }

    _dash_mapping = {
        DIAMOND: {
            CLOCKWISE: lambda x, y: [(x, -y), (y, x), (-x, y), (-y, -x)],
            COUNTER_CLOCKWISE: lambda x, y: [(-x, -y), (y, -x), (x, y), (-y, x)],
            NO_ROT: lambda x, y: [(x, y), (-y, -x), (x, -y), (y, x)],
        },
        BOX: {
            CLOCKWISE: lambda x, y: [(-y, x), (-x, -y), (y, -x), (x, y)],
            COUNTER_CLOCKWISE: lambda x, y: [(-x, y), (-y, -x), (x, -y), (y, x)],
            NO_ROT: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
        },
    }

    _static_mapping = {
        DIAMOND: {
            CLOCKWISE: lambda x, y: [(x, -y), (y, x), (-x, y), (-y, -x)],
            COUNTER_CLOCKWISE: lambda x, y: [(-x, -y), (y, -x), (x, y), (-y, x)],
        },
        BOX: {
            CLOCKWISE: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
            COUNTER_CLOCKWISE: lambda x, y: [(-y, -x), (x, -y), (y, x), (-x, y)],
        },
    }

    def __init__(self, motion: Motion):
        self.motion = motion
        self.grid_mode = self._get_grid_mode()

    def _get_grid_mode(self) -> str:
        """Determines the grid mode based on motion location."""
        return (
            BOX
            if self.motion.prop.state.loc
            in [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
            else DIAMOND
        )

    def _handle_type5_zero_turns(self, x: int, y: int) -> list[tuple[int, int]]:
        """Handles special cases where Type5 letters require unique rotations."""
        start_loc, end_loc = self.motion.state.start_loc, self.motion.state.end_loc
        return self._special_type5_cases.get(self.grid_mode, {}).get(
            (start_loc, end_loc), lambda x, y: [(x, y)] * 4
        )(x, y)

    def get_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        """Retrieves the directional tuples based on motion properties, accounting for all edge cases."""
        motion_type = self.motion.state.motion_type
        rotation = self.motion.state.prop_rot_dir

        if (
            self.motion.pictograph.state.letter_type == LetterType.Type5
            and self.motion.state.turns == 0
        ):
            return self._handle_type5_zero_turns(x, y)

        if motion_type == DASH:
            return self._handle_dash_tuples(x, y)

        if motion_type == STATIC:
            return self._handle_static_tuples(x, y)

        return self._handle_shift_tuples(x, y)

    def _handle_shift_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        """Handles PRO, ANTI, and FLOAT directional tuples."""
        if self.motion.state.motion_type == FLOAT:
            handpath_direction = self._handpath_calculator.get_hand_rot_dir(
                self.motion.state.start_loc, self.motion.state.end_loc
            )
            float_mapping = {
                CW_HANDPATH: lambda x, y: [(x, y), (-y, x), (-x, -y), (y, -x)],
                CCW_HANDPATH: lambda x, y: [(-y, -x), (x, -y), (y, x), (-x, y)],
            }
            return float_mapping.get(handpath_direction, lambda x, y: [(x, y)] * 4)(
                x, y
            )

        # Choose the correct mapping based on grid mode.
        if self.grid_mode == DIAMOND:
            mapping = self._shift_mapping_diamond.get(self.motion.state.motion_type, {})
        elif self.grid_mode == BOX:
            mapping = self._shift_mapping_box.get(self.motion.state.motion_type, {})
        else:
            mapping = {}

        return mapping.get(self.motion.state.prop_rot_dir, lambda x, y: [(x, y)] * 4)(
            x, y
        )

    def _handle_dash_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        """Handles DASH motion types."""

        dash_motion_tuples = self._dash_mapping.get(self.grid_mode, {}).get(
            self.motion.state.prop_rot_dir, lambda x, y: [(x, y)] * 4
        )(x, y)

        return dash_motion_tuples

    def _handle_static_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        """Handles STATIC motion types."""
        if self.motion.state.prop_rot_dir == NO_ROT:
            return [(x, y), (-x, -y), (-y, x), (y, -x)]

        return self._static_mapping.get(self.grid_mode, {}).get(
            self.motion.state.prop_rot_dir, lambda x, y: [(x, y)] * 4
        )(x, y)
