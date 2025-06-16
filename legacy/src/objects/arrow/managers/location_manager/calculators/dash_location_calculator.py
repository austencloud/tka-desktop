from enums.letter.letter import Letter
from enums.letter.letter_type import LetterType
from data.constants import *
from objects.motion.motion import Motion
from .base_location_calculator import BaseLocationCalculator
from typing import TYPE_CHECKING


class DashLocationCalculator(BaseLocationCalculator):
    # Predefined location mappings for different scenarios - because who doesn't love a good lookup table?
    PHI_DASH_PSI_DASH_LOCATION_MAP = {
        (RED, (NORTH, SOUTH)): EAST,
        (RED, (EAST, WEST)): NORTH,
        (RED, (SOUTH, NORTH)): EAST,
        (RED, (WEST, EAST)): NORTH,
        (BLUE, (NORTH, SOUTH)): WEST,
        (BLUE, (EAST, WEST)): SOUTH,
        (BLUE, (SOUTH, NORTH)): WEST,
        (BLUE, (WEST, EAST)): SOUTH,
        (RED, (NORTHWEST, SOUTHEAST)): NORTHEAST,
        (RED, (NORTHEAST, SOUTHWEST)): SOUTHEAST,
        (RED, (SOUTHWEST, NORTHEAST)): SOUTHEAST,
        (RED, (SOUTHEAST, NORTHWEST)): NORTHEAST,
        (BLUE, (NORTHWEST, SOUTHEAST)): SOUTHWEST,
        (BLUE, (NORTHEAST, SOUTHWEST)): NORTHWEST,
        (BLUE, (SOUTHWEST, NORTHEAST)): NORTHWEST,
        (BLUE, (SOUTHEAST, NORTHWEST)): SOUTHWEST,
    }

    LAMBDA_ZERO_TURNS_LOCATION_MAP = {
        ((NORTH, SOUTH), WEST): EAST,
        ((EAST, WEST), SOUTH): NORTH,
        ((NORTH, SOUTH), EAST): WEST,
        ((WEST, EAST), SOUTH): NORTH,
        ((SOUTH, NORTH), WEST): EAST,
        ((EAST, WEST), NORTH): SOUTH,
        ((SOUTH, NORTH), EAST): WEST,
        ((WEST, EAST), NORTH): SOUTH,
        ((NORTHEAST, SOUTHWEST), NORTHWEST): SOUTHEAST,
        ((NORTHWEST, SOUTHEAST), NORTHEAST): SOUTHWEST,
        ((SOUTHWEST, NORTHEAST), SOUTHEAST): NORTHWEST,
        ((SOUTHEAST, NORTHWEST), SOUTHWEST): NORTHEAST,
        ((NORTHEAST, SOUTHWEST), SOUTHEAST): NORTHWEST,
        ((NORTHWEST, SOUTHEAST), SOUTHWEST): NORTHEAST,
        ((SOUTHWEST, NORTHEAST), NORTHWEST): SOUTHEAST,
        ((SOUTHEAST, NORTHWEST), NORTHEAST): SOUTHWEST,
    }

    DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP = {
        (NORTH, SOUTH): EAST,
        (EAST, WEST): SOUTH,
        (SOUTH, NORTH): WEST,
        (WEST, EAST): NORTH,
        (NORTHEAST, SOUTHWEST): SOUTHEAST,
        (NORTHWEST, SOUTHEAST): NORTHEAST,
        (SOUTHWEST, NORTHEAST): NORTHWEST,
        (SOUTHEAST, NORTHWEST): SOUTHWEST,
    }

    NON_ZERO_TURNS_DASH_LOCATION_MAP = {
        CLOCKWISE: {
            NORTH: EAST,
            EAST: SOUTH,
            SOUTH: WEST,
            WEST: NORTH,
            NORTHEAST: SOUTHEAST,
            SOUTHEAST: SOUTHWEST,
            SOUTHWEST: NORTHWEST,
            NORTHWEST: NORTHEAST,
        },
        COUNTER_CLOCKWISE: {
            NORTH: WEST,
            EAST: NORTH,
            SOUTH: EAST,
            WEST: SOUTH,
            NORTHEAST: NORTHWEST,
            SOUTHEAST: NORTHEAST,
            SOUTHWEST: SOUTHEAST,
            NORTHWEST: SOUTHWEST,
        },
    }

    DIAMOND_DASH_LOCATION_MAP = {
        (NORTH, NORTHWEST): EAST,
        (NORTH, NORTHEAST): WEST,
        (NORTH, SOUTHEAST): WEST,
        (NORTH, SOUTHWEST): EAST,
        (EAST, NORTHWEST): SOUTH,
        (EAST, NORTHEAST): SOUTH,
        (EAST, SOUTHEAST): NORTH,
        (EAST, SOUTHWEST): NORTH,
        (SOUTH, NORTHWEST): EAST,
        (SOUTH, NORTHEAST): WEST,
        (SOUTH, SOUTHEAST): WEST,
        (SOUTH, SOUTHWEST): EAST,
        (WEST, NORTHWEST): SOUTH,
        (WEST, NORTHEAST): SOUTH,
        (WEST, SOUTHEAST): NORTH,
        (WEST, SOUTHWEST): NORTH,
    }

    BOX_DASH_LOCATION_MAP = {
        (NORTHEAST, NORTH): SOUTHEAST,
        (NORTHEAST, EAST): NORTHWEST,
        (NORTHEAST, SOUTH): NORTHWEST,
        (NORTHEAST, WEST): SOUTHEAST,
        (SOUTHEAST, NORTH): SOUTHWEST,
        (SOUTHEAST, EAST): SOUTHWEST,
        (SOUTHEAST, SOUTH): NORTHEAST,
        (SOUTHEAST, WEST): NORTHEAST,
        (SOUTHWEST, NORTH): SOUTHEAST,
        (SOUTHWEST, EAST): NORTHWEST,
        (SOUTHWEST, SOUTH): NORTHWEST,
        (SOUTHWEST, WEST): SOUTHEAST,
        (NORTHWEST, NORTH): SOUTHWEST,
        (NORTHWEST, EAST): SOUTHWEST,
        (NORTHWEST, SOUTH): NORTHEAST,
        (NORTHWEST, WEST): NORTHEAST,
    }

    def calculate_location(self) -> str:
        if self.pictograph.state.letter in [Letter.Φ_DASH, Letter.Ψ_DASH]:
            return self._get_Φ_dash_Ψ_dash_location()
        elif (
            self.pictograph.state.letter in [Letter.Λ, Letter.Λ_DASH]
            and self.arrow.motion.state.turns == 0
        ):
            return self._get_Λ_zero_turns_location()
        elif self.arrow.motion.state.turns == 0:
            return self._default_zero_turns_dash_location()
        else:
            return self._dash_location_non_zero_turns()

    def _get_Φ_dash_Ψ_dash_location(self) -> str:
        self.other_motion = self.pictograph.managers.get.other_motion(self.arrow.motion)

        if (
            self.arrow.motion.state.turns == 0
            and self.other_motion.arrow.motion.state.turns == 0
        ):
            arrow_location = self.PHI_DASH_PSI_DASH_LOCATION_MAP.get(
                (
                    self.arrow.state.color,
                    (
                        self.arrow.motion.state.start_loc,
                        self.arrow.motion.state.end_loc,
                    ),
                )
            )
            return arrow_location

        elif self.arrow.motion.state.turns == 0:
            return self.pictograph.managers.get.opposite_location(
                self._dash_location_non_zero_turns(self.other_motion)
            )
        elif self.arrow.motion.state.turns != 0:
            return self._dash_location_non_zero_turns(self.arrow.motion)

    def _get_Λ_zero_turns_location(self) -> str:
        self.other_motion = self.pictograph.managers.get.other_motion(self.arrow.motion)
        arrow_location = self.LAMBDA_ZERO_TURNS_LOCATION_MAP.get(
            (
                (self.arrow.motion.state.start_loc, self.arrow.motion.state.end_loc),
                (self.other_motion.state.end_loc),
            )
        )
        return arrow_location

    def _default_zero_turns_dash_location(self) -> str:
        if self.pictograph.state.letter_type == LetterType.Type3:
            return self._calculate_dash_location_based_on_shift()

        return self.DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP.get(
            (self.arrow.motion.state.start_loc, self.arrow.motion.state.end_loc), ""
        )

    def _dash_location_non_zero_turns(self, motion: Motion = None) -> str:
        motion = motion if motion else self.arrow.motion
        return self.NON_ZERO_TURNS_DASH_LOCATION_MAP[motion.state.prop_rot_dir][
            motion.state.start_loc
        ]

    def _calculate_dash_location_based_on_shift(self) -> str:
        shift_arrow = self.pictograph.managers.get.shift().arrow

        shift_location = shift_arrow.state.loc
        grid_mode = self.pictograph.state.grid_mode
        start_loc = self.arrow.motion.state.start_loc

        if grid_mode == DIAMOND:
            return self.DIAMOND_DASH_LOCATION_MAP.get((start_loc, shift_location))
        elif grid_mode == BOX:
            return self.BOX_DASH_LOCATION_MAP.get((start_loc, shift_location))
