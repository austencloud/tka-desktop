# strategies/dual_float.py
from dataclasses import dataclass
from ..core import DeterminationResult
from .base_strategy import BaseDeterminationStrategy
from ..services.motion_comparator import MotionComparator
from ..services.attribute_manager import AttributeManager
from ..models.pictograph import PictographData


@dataclass
class DualFloatStrategy(BaseDeterminationStrategy):
    comparator: MotionComparator
    attribute_manager: AttributeManager

    def execute(
        self, data: PictographData, swap_prop_rot_dir: bool = False
    ) -> DeterminationResult:
        if not self._is_dual_float(data):
            return DeterminationResult(
                letter=None, matched_attributes={}
            )  # ✅ Correct fields

        self.attribute_manager.sync_attributes(data)
        return self._match_exact(data)

    def _is_dual_float(self, data: PictographData) -> bool:
        return data.blue_attributes.is_float and data.red_attributes.is_float

    def _match_exact(self, data: PictographData) -> DeterminationResult:
        """Mirror original example-by-example matching"""
        for letter, examples in self.comparator.dataset.items():
            for example in examples:
                if self.comparator.compare(data, example):
                    return DeterminationResult(
                        success=True,
                        letter=letter,
                        matched_attributes=example.serialized_attributes(),
                    )
        return DeterminationResult(success=False)

    def applies_to(self, pictograph: PictographData) -> bool:
        """This strategy only applies when both motions are FLOAT and have valid attributes."""
        return (
            pictograph.blue_attributes.is_float
            and pictograph.red_attributes.is_float
            and pictograph.blue_attributes.start_loc is not None
            and pictograph.red_attributes.start_loc is not None
        )
