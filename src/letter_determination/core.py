from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    FLOAT,
    MOTION_TYPE,
    PROP_ROT_DIR,
    RED,
    RED_ATTRS,
    STATIC,
)
from enums.letter.letter import Letter

from main_window.main_widget.json_manager.json_manager import JsonManager

from .models.motion import dict, str
from .models.pictograph import dict
from .determination_result import DeterminationResult
from .services.attribute_manager import AttributeManager
from .services.json_handler import LetterDeterminationJsonHandler
from .services.motion_comparator import MotionComparator

if TYPE_CHECKING:
    from .strategies.base_strategy import BaseDeterminationStrategy


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

        # ✅ Import strategies lazily to break circular import loop
        from .strategies.non_hybrid_shift import NonHybridShiftStrategy
        from .strategies.dual_float import DualFloatStrategy

        self.strategies = [DualFloatStrategy, NonHybridShiftStrategy]

    def determine_letter(
        self, pictograph_data: dict, swap_prop_rot_dir: bool = False
    ) -> Letter:
        """Determine the letter for the given pictograph using strategies or fallback."""
        self.attribute_manager.sync_attributes(pictograph_data)
        # if (
        #     pictograph_data[BLUE_ATTRS][MOTION_TYPE] == FLOAT
        #     and pictograph_data[RED_ATTRS][MOTION_TYPE] == FLOAT
        # ):
        #     self.attribute_manager.update_prefloat_attributes(
        #         pictograph_data[BLUE_ATTRS], pictograph_data[RED_ATTRS]
        #     )

        # If both motions are static, return early
        if (
            pictograph_data[BLUE_ATTRS][MOTION_TYPE] == STATIC
            and pictograph_data[RED_ATTRS][MOTION_TYPE] == STATIC
        ):
            return None

        for strategy_class in self.strategies:
            strategy: "BaseDeterminationStrategy" = strategy_class(
                self.comparator, self.attribute_manager
            )

            if strategy.applies_to(
                pictograph_data
            ):  # Ensure only applicable strategies run
                letter: Letter = strategy.execute(
                    pictograph_data, swap_prop_rot_dir=swap_prop_rot_dir
                )
                if letter is not None:
                    return letter

        return self._fallback_search(pictograph_data, swap_prop_rot_dir)

    def _fallback_search(
        self, pictograph_data: dict, swap_prop_rot_dir: bool
    ) -> Optional[Letter]:
        """Fallback search that ensures prefloat motion attributes are respected."""
        blue_attrs: dict = pictograph_data[BLUE_ATTRS]
        red_attrs: dict = pictograph_data[RED_ATTRS]

        # Ensure prefloat attributes are updated before comparison
        self.attribute_manager.sync_attributes(pictograph_data)

        # Create temporary copies to avoid modifying original data
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
                    return letter

        return None

    def _get_letter_from_pictograph_and_color(
        self, motion_color: str, pictograph_data: dict, swap_prop_rot_dir: bool
    ) -> Optional[Letter]:
        """Fallback search that ensures prefloat motion attributes are respected."""
        blue_attrs: dict = pictograph_data[BLUE_ATTRS]
        red_attrs: dict = pictograph_data[RED_ATTRS]

        # Ensure prefloat attributes are updated before comparison
        self.attribute_manager.sync_attributes(pictograph_data)

        # Create temporary copies to avoid modifying original data
        blue_copy = blue_attrs.copy()
        red_copy = red_attrs.copy()

        # if motion_color == BLUE and swap_prop_rot_dir:
        #     blue_copy[PROP_ROT_DIR] = self.comparator._reverse_prop_rot_dir(
        #         blue_copy[PROP_ROT_DIR]
        #     )
        #     blue_copy[MOTION_TYPE] = self.comparator._reverse_motion_type(
        #         blue_copy[MOTION_TYPE]
        #     )
        # elif motion_color == RED and swap_prop_rot_dir:
        #     red_copy[PROP_ROT_DIR] = self.comparator._reverse_prop_rot_dir(
        #         red_copy[PROP_ROT_DIR]
        #     )
        #     red_copy[MOTION_TYPE] = self.comparator._reverse_motion_type(
        #         red_copy[MOTION_TYPE]
        #     )
        pictograph_data_copy = pictograph_data.copy()
        pictograph_data_copy[RED_ATTRS] = red_copy
        pictograph_data_copy[BLUE_ATTRS] = blue_copy

        for letter, examples in self.pictograph_dataset.items():
            for example in examples:
                if self.comparator.compare(pictograph_data_copy, example):
                    return letter

        return None
