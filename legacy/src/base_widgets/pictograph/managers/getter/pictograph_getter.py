from typing import TYPE_CHECKING, Optional


from base_widgets.pictograph.elements.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from base_widgets.pictograph.managers.getter.lead_state_determiner import (
    LeadStateDeterminer,
)
from data.constants import *
from enums.glyph_enum import Glyph
from enums.letter.letter import Letter
from enums.letter.letter_type import LetterType
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from objects.prop.prop import Prop


class PictographGetter:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph
        self.is_initialized = False

    def initiallize_getter(self):
        self.is_initialized = True
        self.blue_motion = self.pictograph.elements.blue_motion
        self.red_motion = self.pictograph.elements.red_motion
        self.blue_arrow = self.pictograph.elements.blue_arrow
        self.red_arrow = self.pictograph.elements.red_arrow
        self.lead_state_determiner = LeadStateDeterminer(
            self.red_motion, self.blue_motion
        )

    def motion_by_color(self, color: str) -> Motion:
        return self.pictograph.elements.motion_set.get(color)

    def prop_by_color(self, color: str) -> "Prop":
        """Get a prop by its color."""
        return self.pictograph.elements.props.get(color)

    def letter_type(self, letter: Letter) -> Optional[str]:
        letter_type_map = {
            letter: letter_type.description
            for letter_type in LetterType
            for letter in letter_type.letters
        }
        return letter_type_map.get(letter)

    def motions_by_type(self, motion_type: str) -> list[Motion]:
        return [
            motion
            for motion in self.pictograph.elements.motion_set.values()
            if motion.state.motion_type == motion_type
        ]

    def trailing_motion(self) -> Motion:
        return self.lead_state_determiner.trailing_motion()

    def leading_motion(self) -> Motion:
        return self.lead_state_determiner.leading_motion()

    def other_motion(self, motion: Motion) -> Motion:
        other_motion_map = {
            RED: self.pictograph.elements.blue_motion,
            BLUE: self.pictograph.elements.red_motion,
        }
        return other_motion_map.get(motion.state.color)

    def other_arrow(self, arrow: Arrow) -> Arrow:
        other_arrow_map = {RED: self.blue_arrow, BLUE: self.red_arrow}
        return other_arrow_map.get(arrow.state.color)

    def pro(self) -> Motion:
        pro_map = {True: self.red_motion, False: self.blue_motion}
        return pro_map.get(self.red_motion.state.motion_type == PRO)

    def anti(self) -> Motion:
        anti_map = {True: self.red_motion, False: self.blue_motion}
        return anti_map.get(self.red_motion.state.motion_type == ANTI)

    def dash(self) -> Motion:
        dash_map = {True: self.red_motion, False: self.blue_motion}
        return dash_map.get(self.red_motion.check.is_dash())

    def shift(self) -> Motion:
        shift_map = {True: self.red_motion, False: self.blue_motion}
        return shift_map.get(self.red_motion.check.is_shift())

    def static(self) -> Motion:
        static_map = {True: self.red_motion, False: self.blue_motion}
        return static_map.get(self.red_motion.check.is_static())

    def float_motion(self) -> Motion:
        float_map = {True: self.red_motion, False: self.blue_motion}
        return float_map.get(self.red_motion.check.is_float())

    def grid_mode(self) -> str:
        return self.pictograph.elements.grid.grid_mode

    def opposite_location(self, loc: str) -> str:
        opposite_locations = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST,
            NORTHEAST: SOUTHWEST,
            SOUTHWEST: NORTHEAST,
            SOUTHEAST: NORTHWEST,
            NORTHWEST: SOUTHEAST,
        }
        return opposite_locations.get(loc)

    def turns_tuple(self) -> tuple[int, int, int]:
        turns_tuple = TurnsTupleGenerator().generate_turns_tuple(self.pictograph)
        if turns_tuple is None:
            raise ValueError("Turns tuple cannot be None")
        return turns_tuple

    def pictograph_data(self) -> dict:
        return {
            LETTER: (
                self.pictograph.state.pictograph_data[LETTER]
                if not self.pictograph.state.letter
                else self.pictograph.state.letter.value
            ),
            START_POS: self.pictograph.state.start_pos,
            END_POS: self.pictograph.state.end_pos,
            TIMING: self.pictograph.state.timing,
            DIRECTION: self.pictograph.state.direction,
            BLUE_ATTRS: {
                MOTION_TYPE: self.blue_motion.state.motion_type,
                START_ORI: self.blue_motion.state.start_ori,
                PROP_ROT_DIR: self.blue_motion.state.prop_rot_dir,
                START_LOC: self.blue_motion.state.start_loc,
                END_LOC: self.blue_motion.state.end_loc,
                TURNS: self.blue_motion.state.turns,
                END_ORI: self.blue_motion.state.end_ori,
            },
            RED_ATTRS: {
                MOTION_TYPE: self.red_motion.state.motion_type,
                START_ORI: self.red_motion.state.start_ori,
                PROP_ROT_DIR: self.red_motion.state.prop_rot_dir,
                START_LOC: self.red_motion.state.start_loc,
                END_LOC: self.red_motion.state.end_loc,
                TURNS: self.red_motion.state.turns,
                END_ORI: self.red_motion.state.end_ori,
            },
        }

    def glyphs(self) -> list[Glyph]:
        return [
            self.pictograph.elements.tka_glyph,
            self.pictograph.elements.vtg_glyph,
            self.pictograph.elements.elemental_glyph,
            self.pictograph.elements.start_to_end_pos_glyph,
            self.pictograph.elements.reversal_glyph,
        ]

    def non_radial_points(self) -> NonRadialPointsGroup:
        return self.pictograph.elements.grid.items.get(
            f"{self.pictograph.elements.grid.grid_mode}_nonradial"
        )

    def glyph(self, name: str) -> Glyph:
        glyph_map = {
            "TKA": self.pictograph.elements.tka_glyph,
            "VTG": self.pictograph.elements.vtg_glyph,
            "Elemental": self.pictograph.elements.elemental_glyph,
            "Positions": self.pictograph.elements.start_to_end_pos_glyph,
            "Reversals": self.pictograph.elements.reversal_glyph,
        }
        return glyph_map.get(name)

    def motions(self) -> dict[str, Motion]:
        return self.pictograph.elements.motion_set
