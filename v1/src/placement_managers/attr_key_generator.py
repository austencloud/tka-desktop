from data.constants import CLOCK, COUNTER, IN, OUT
from enums.letter.letter import Letter, LetterCondition
from placement_managers.arrow_placement_manager.arrow_placement_context import (
    ArrowPlacementContext,
)
from objects.arrow.arrow import Arrow


class AttrKeyGenerator:
    def __init__(self):
        pass  # No dependency on `SpecialArrowPositioner` needed anymore

    def get_key_from_arrow(self, arrow: "Arrow") -> str:
        """Original method for getting key from Arrow (kept for compatibility)."""
        return self.generate_key(
            motion_type=arrow.motion.state.motion_type,
            letter=arrow.pictograph.state.letter,
            start_ori=arrow.motion.state.start_ori,
            color=arrow.state.color,
            lead_state=arrow.motion.state.lead_state,
            has_hybrid_motions=arrow.pictograph.managers.check.has_hybrid_motions(),
            starts_from_mixed_orientation=arrow.pictograph.managers.check.starts_from_mixed_orientation(),
            starts_from_standard_orientation=arrow.pictograph.managers.check.starts_from_standard_orientation(),
        )

    def get_key_from_context(self, context: ArrowPlacementContext) -> str:
        """New method to get key from ArrowPlacementContext instead of Arrow object."""
        return self.generate_key(
            motion_type=context.motion_type,
            letter=context.letter,
            start_ori=None,  # No equivalent in ArrowPlacementContext, assume None
            color=context.arrow_color,
            lead_state=None,  # Not available in context, assume None
            has_hybrid_motions=False,  # Need a better check here if hybrid motions are relevant
            starts_from_mixed_orientation=False,  # Context lacks a direct check for this
            starts_from_standard_orientation=True,  # Assume standard unless explicitly hybrid
        )

    def generate_key(
        self,
        motion_type: str,
        letter: Letter,
        start_ori: str,
        color: str,
        lead_state: str,
        has_hybrid_motions: bool,
        starts_from_mixed_orientation: bool,
        starts_from_standard_orientation: bool,
    ) -> str:
        """Core key generation logic used by both `get_key` and `get_key_from_context`."""
        if starts_from_mixed_orientation:
            if letter in ["S", "T"]:
                return f"{lead_state}"
            elif has_hybrid_motions:
                if start_ori in [IN, OUT]:
                    return f"{motion_type}_from_layer1"
                elif start_ori in [CLOCK, COUNTER]:
                    return f"{motion_type}_from_layer2"
                else:
                    return color
            elif letter in letter.get_letters_by_condition(LetterCondition.NON_HYBRID):
                return color
            else:
                return motion_type

        elif starts_from_standard_orientation:
            if letter in ["S", "T"]:
                return f"{color}_{lead_state}"
            elif has_hybrid_motions:
                return motion_type
            else:
                return color

        return motion_type  # Default fallback
