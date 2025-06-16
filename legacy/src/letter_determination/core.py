from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from data.constants import BLUE_ATTRS, MOTION_TYPE, PROP_ROT_DIR, RED_ATTRS, STATIC
from enums.letter.letter import Letter
from main_window.main_widget.json_manager.json_manager import JsonManager
from .services.attribute_manager import AttributeManager
from .services.json_handler import LetterDeterminationJsonHandler
from .services.motion_comparator import MotionComparator
from .strategies.non_hybrid_shift import NonHybridShiftStrategy
from .strategies.dual_float import DualFloatStrategy

if TYPE_CHECKING:
    from .strategies.base_strategy import LetterDeterminationStrategy


class LetterDeterminer:
    def __init__(
        self,
        pictograph_dataset: dict[Letter, list[dict]],
        json_manager: "JsonManager",
    ):
        self.pictograph_dataset = pictograph_dataset
        self.json_handler = LetterDeterminationJsonHandler(json_manager)
        self.comparator = MotionComparator(pictograph_dataset)
        self.attribute_manager = AttributeManager(self.json_handler)

        self.strategies = [DualFloatStrategy, NonHybridShiftStrategy]

    def update_pictograph_dataset(
        self, pictograph_dataset: dict[Letter, list[dict]]
    ) -> None:
        """Update the pictograph dataset and refresh the comparator."""
        self.pictograph_dataset = pictograph_dataset
        self.comparator = MotionComparator(pictograph_dataset)

    def determine_letter(
        self, pictograph_data: dict, swap_prop_rot_dir: bool = False
    ) -> Letter:
        self.attribute_manager.sync_attributes(pictograph_data)

        if (
            pictograph_data[BLUE_ATTRS][MOTION_TYPE] == STATIC
            and pictograph_data[RED_ATTRS][MOTION_TYPE] == STATIC
        ):
            return None

        for strategy_class in self.strategies:
            strategy: "LetterDeterminationStrategy" = strategy_class(
                self.comparator, self.attribute_manager
            )

            if strategy.applies_to(pictograph_data):
                letter: Letter = strategy.execute(
                    pictograph_data, swap_prop_rot_dir=swap_prop_rot_dir
                )
                if letter is not None:
                    return letter

        letter = self._fallback_search(pictograph_data, swap_prop_rot_dir)
        return letter

    def _fallback_search(
        self, pictograph_data: dict, swap_prop_rot_dir: bool
    ) -> Optional[Letter]:
        import logging

        logger = logging.getLogger(__name__)

        # Debug: Check if dataset is populated
        dataset_size = len(self.pictograph_dataset)
        logger.debug(f"Fallback search: dataset has {dataset_size} letters")
        if dataset_size == 0:
            logger.warning(
                "Pictograph dataset is empty - cannot perform fallback search"
            )
            return None

        blue_attrs: dict = pictograph_data[BLUE_ATTRS]
        red_attrs: dict = pictograph_data[RED_ATTRS]

        self.attribute_manager.sync_attributes(pictograph_data)

        blue_copy = blue_attrs.copy()
        red_copy = red_attrs.copy()

        if swap_prop_rot_dir:
            blue_copy[PROP_ROT_DIR] = self.comparator._reverse_prop_rot_dir(
                blue_copy[PROP_ROT_DIR]
            )
            red_copy[PROP_ROT_DIR] = self.comparator._reverse_prop_rot_dir(
                red_copy[PROP_ROT_DIR]
            )
        pictograph_data_copy = pictograph_data.copy()
        pictograph_data_copy[RED_ATTRS] = red_copy
        pictograph_data_copy[BLUE_ATTRS] = blue_copy

        for letter, examples in self.pictograph_dataset.items():
            for example in examples:
                if self.comparator.compare(pictograph_data, example):
                    logger.debug(f"Fallback search found match: {letter}")
                    return letter

        logger.debug("Fallback search: no matches found")
        return None
