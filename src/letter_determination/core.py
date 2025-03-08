from __future__ import annotations
from typing import TYPE_CHECKING
from enums.letter.letter import Letter

from main_window.main_widget.json_manager.json_manager import JsonManager

from .models.motion import MotionAttributes, MotionType
from .models.pictograph import PictographData
from .determination_result import DeterminationResult
from .strategies.non_hybrid_shift import NonHybridShiftStrategy
from .strategies.dual_float import DualFloatStrategy
from .services.attribute_manager import AttributeManager
from .services.json_handler import LetterDeterminationJsonHandler
from .services.motion_comparator import MotionComparator

if TYPE_CHECKING:
    from .strategies.base_strategy import BaseDeterminationStrategy


class LetterDeterminer:
    def __init__(
        self,
        dataset: dict[Letter, list[PictographData]],
        json_manager: "JsonManager",
    ):
        self.dataset = dataset
        self.json_handler = LetterDeterminationJsonHandler(json_manager)
        self.strategies = [DualFloatStrategy, NonHybridShiftStrategy]

        self.comparator = MotionComparator(dataset)
        self.attribute_manager = AttributeManager(self.json_handler)

    def determine_letter(
        self, pictograph: PictographData, swap_prop_rot_dir: bool = False
    ) -> DeterminationResult:
        """Determine the letter for the given pictograph using strategies or fallback."""
        self.attribute_manager.sync_attributes(pictograph)
        if pictograph.blue_attributes.is_float and pictograph.red_attributes.is_float:
            self.attribute_manager.update_prefloat_attributes(
                pictograph.blue_attributes, pictograph.red_attributes
            )

        # If both motions are static, return early
        if (
            pictograph.blue_attributes.motion_type == MotionType.STATIC
            and pictograph.red_attributes.motion_type == MotionType.STATIC
        ):
            return DeterminationResult(None, {})

        for strategy_class in self.strategies:
            strategy: "BaseDeterminationStrategy" = strategy_class(
                self.comparator, self.attribute_manager
            )

            if strategy.applies_to(pictograph):  # Ensure only applicable strategies run
                result: DeterminationResult = strategy.execute(
                    pictograph, swap_prop_rot_dir=swap_prop_rot_dir
                )
                if result.letter is not None:
                    return result

        return self._fallback_search(pictograph, swap_prop_rot_dir)

    def _fallback_search(
        self, pictograph: PictographData, swap_prop_rot_dir: bool
    ) -> DeterminationResult:
        """Fallback search that ensures prefloat motion attributes are respected."""
        blue_attrs = pictograph.blue_attributes
        red_attrs = pictograph.red_attributes

        # Ensure prefloat attributes are updated before comparison
        self.attribute_manager.sync_attributes(pictograph)

        # Create temporary copies to avoid modifying original data
        blue_copy = blue_attrs.serialize()
        red_copy = red_attrs.serialize()

        if swap_prop_rot_dir:
            blue_copy["prop_rot_dir"], red_copy["prop_rot_dir"] = (
                red_copy["prop_rot_dir"],
                blue_copy["prop_rot_dir"],
            )

        for letter, examples in self.dataset.items():
            for example in examples:
                if self.comparator.compare(
                    MotionAttributes(**blue_copy), MotionAttributes(**red_copy), example
                ):
                    return DeterminationResult(letter, example.serialized_attributes())

        return DeterminationResult(None, {})
