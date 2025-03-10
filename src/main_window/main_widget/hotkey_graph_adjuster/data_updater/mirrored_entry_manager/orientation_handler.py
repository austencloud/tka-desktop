import logging
from typing import List
from enums.letter.letter import Letter
from enums.letter.letter_condition import LetterCondition
from data.constants import BLUE, RED, IN, OUT
from objects.arrow.arrow import Arrow
from .turns_pattern_manager import TurnsPatternManager

logger = logging.getLogger(__name__)

class OrientationHandler:
    def __init__(self, arrow: Arrow, turns_manager: TurnsPatternManager):
        self.arrow = arrow
        self.pictograph = arrow.pictograph
        self.motion = arrow.motion
        self.turns_manager = turns_manager

    def is_mixed_orientation(self) -> bool:
        return self.pictograph.managers.check.starts_from_mixed_orientation()

    def get_hybrid_letters(self) -> List[Letter]:
        return Letter.get_letters_by_condition(LetterCondition.HYBRID)

    def get_mixed_attribute_key(self) -> str:
        letter = self.pictograph.state.letter
        layer = "1" if self.motion.state.start_ori in [IN, OUT] else "2"

        if letter.value in ["S", "T"]:
            attr = self.motion.state.lead_state
            return f"{attr}_from_layer{layer}"
        elif self.pictograph.managers.check.has_hybrid_motions():
            attr = self.motion.state.motion_type
            return f"{attr}_from_layer{layer}"
        else:
            return BLUE if self.arrow.state.color == RED else RED

    def get_standard_attribute_key(self, other_arrow: Arrow) -> str:
        letter = self.pictograph.state.letter

        if letter.value in ["S", "T"]:
            return self.motion.state.lead_state
        elif self.pictograph.managers.check.has_hybrid_motions():
            return self.motion.state.motion_type
        else:
            return BLUE if self.arrow.state.color == RED else RED

    def should_create_standard_mirror(self, other_arrow: "Arrow"):
        turns = self.motion.state.turns
        other_turns = other_arrow.motion.state.turns
        motion_type = self.motion.state.motion_type
        other_motion_type = other_arrow.motion.state.motion_type

        if turns != other_turns and motion_type == other_motion_type:
            return True

        if (
            turns != other_turns
            and motion_type != other_motion_type
            and not self.pictograph.managers.check.has_one_float()
        ):
            return True

        if (
            turns != other_turns
            and motion_type != other_motion_type
            and self.pictograph.managers.check.has_one_float()
        ):
            return True

        return False

    def determine_layer(self) -> str:
        return "1" if self.motion.state.start_ori in [IN, OUT] else "2"

    def get_other_attr_key(self, attribute_key: str) -> str:
        return RED if attribute_key == BLUE else BLUE