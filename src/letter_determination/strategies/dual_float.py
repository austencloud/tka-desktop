# strategies/dual_float.py
from dataclasses import dataclass

from data.constants import BLUE_ATTRS, FLOAT, MOTION_TYPE, RED_ATTRS, START_LOC
from letter_determination.determination_result import DeterminationResult
from .base_strategy import LetterDeterminationStrategy
from ..services.motion_comparator import MotionComparator
from ..services.attribute_manager import AttributeManager


@dataclass
class DualFloatStrategy(LetterDeterminationStrategy):
    comparator: MotionComparator
    attribute_manager: AttributeManager

    def execute(
        self, data: dict, swap_prop_rot_dir: bool = False
    ) -> DeterminationResult:
        if not self._is_dual_float(data):
            return None

        self.attribute_manager.sync_attributes(data)
        return self._match_exact(data)

    def _is_dual_float(self, pictograph_data: dict) -> bool:
        return (
            pictograph_data[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            and pictograph_data[RED_ATTRS][MOTION_TYPE] == FLOAT
        )

    def _match_exact(self, pictograph_data: dict) -> DeterminationResult:
        """Mirror original example-by-example matching"""
        for letter, examples in self.comparator.dataset.items():
            for example in examples:
                if self.comparator.compare(pictograph_data, example):
                    return letter
        return None

    def applies_to(self, pictograph: dict) -> bool:
        """This strategy only applies when both motions are FLOAT and have valid attributes."""
        return (
            pictograph[BLUE_ATTRS][MOTION_TYPE] == FLOAT
            and pictograph[RED_ATTRS][MOTION_TYPE] == FLOAT
            and pictograph[BLUE_ATTRS][START_LOC] is not None
            and pictograph[RED_ATTRS][START_LOC] is not None
        )
