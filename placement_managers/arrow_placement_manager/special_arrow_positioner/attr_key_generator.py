from typing import TYPE_CHECKING
from Enums.letters import LetterConditions
from data.constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .special_arrow_positioner import SpecialArrowPositioner


class AttrKeyGenerator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def get_key(self, arrow: "Arrow") -> str:
        if arrow.pictograph.managers.check.starts_from_mixed_orientation():
            if self.positioner.pictograph.state.letter.value in ["S", "T"]:
                return f"{arrow.motion.lead_state}"
            elif arrow.pictograph.managers.check.starts_from_mixed_orientation():
                if arrow.pictograph.managers.check.has_hybrid_motions():
                    if arrow.motion.start_ori in [IN, OUT]:
                        return f"{arrow.motion.motion_type}_from_layer1"
                    elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                        return f"{arrow.motion.motion_type}_from_layer2"
                else:
                    return arrow.motion.color
            elif (
                self.positioner.pictograph.state.letter
                in self.positioner.pictograph.state.letter.get_letters_by_condition(
                    LetterConditions.NON_HYBRID
                )
            ):
                return arrow.color
            else:
                return arrow.motion.motion_type

        elif arrow.pictograph.managers.check.starts_from_standard_orientation():

            if arrow.pictograph.state.letter.value in ["S", "T"]:
                return f"{arrow.color}_{arrow.motion.lead_state}"
            elif arrow.pictograph.managers.check.has_hybrid_motions():
                return arrow.motion.motion_type
            else:
                return arrow.color

    def _determine_layer(self, arrow: "Arrow") -> int:
        return 1 if arrow.motion.start_ori in [IN, OUT] else 2
