import os
import logging
from typing import TYPE_CHECKING, Callable

from base_widgets.pictograph.pictograph_getter import PictographGetter
from base_widgets.pictograph.pictograph_state import PictographState
from main_window.main_widget.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from main_window.settings_manager.global_settings.app_context import AppContext
from placement_managers.arrow_placement_manager.mirrored_entry_manager.mirrored_entry_manager import (
    MirroredEntryManager,
)
from placement_managers.arrow_placement_manager.special_arrow_positioner.attr_key_generator import (
    AttrKeyGenerator,
)


from .special_placement_entry_remover import SpecialPlacementEntryRemover
from data.constants import (
    BLUE,
    CLOCK,
    COUNTER,
    IN,
    OUT,
    RED,
)
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from Enums.Enums import Letter

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SpecialPlacementDataUpdater:
    def __init__(
        self,
        positioner: "SpecialArrowPositioner",
        attr_key_generator: "AttrKeyGenerator",
        state: "PictographState",
        get_default_adjustment_callback: callable,
        get: "PictographGetter",
    ) -> None:
        self.positioner = positioner
        self.state = state
        self.attr_key_generator = attr_key_generator
        self.get_default_adjustment_callback = get_default_adjustment_callback
        self.get = get
        self.get_grid_mode = get.grid_mode()

        self.turns_tuple_generator = TurnsTupleGenerator()

        self.entry_remover = SpecialPlacementEntryRemover(self)
        self.mirrored_entry_manager = MirroredEntryManager(self)

    def _get_letter_data(self, letter: Letter, ori_key: str) -> dict:
        letter_data = (
            AppContext.special_placement_loader()
            .load_special_placements()[self.state.grid_mode][ori_key]
            .get(letter.value, {})
        )

        return letter_data

    def _update_or_create_turn_data(
        self,
        letter_data: dict,
        turns_tuple: str,
        arrow: Arrow,
        adjustment: tuple[int, int],
    ) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        key = self.attr_key_generator.get_key(arrow)

        if key in turn_data and turn_data[key] != {}:
            turn_data[key][0] += adjustment[0]
            turn_data[key][1] += adjustment[1]
        else:
            default_adjustment = self.get_default_adjustment_callback(arrow)
            turn_data[key] = [
                default_adjustment[0] + adjustment[0],
                default_adjustment[1] + adjustment[1],
            ]

        letter_data[turns_tuple] = turn_data

    def _generate_ori_key(self, motion: Motion) -> str:
        other_motion: Motion = self.get.other_motion(motion)
        if motion.state.start_ori in [IN, OUT] and other_motion.state.start_ori in [
            IN,
            OUT,
        ]:
            return "from_layer1"
        elif motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ] and other_motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ]:
            return "from_layer2"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def get_other_layer3_ori_key(self, ori_key: str) -> str:
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"

    def _update_placement_json_data(
        self, letter: Letter, letter_data: dict, ori_key: str
    ) -> None:
        grid_mode = self.state.grid_mode
        file_path = os.path.join(
            "data",
            "arrow_placement",
            grid_mode,
            "special",
            ori_key,
            f"{letter.value}_placements.json",
        )
        existing_data = AppContext.special_placement_handler().load_json_data(file_path)
        existing_data[letter.value] = letter_data
        AppContext.special_placement_handler().write_json_data(existing_data, file_path)

    def update_arrow_adjustments_in_json(
        self, adjustment: tuple[int, int], arrow: Arrow, turns_tuple: str
    ) -> None:
        if not arrow:
            return

        letter = self.state.letter

        ori_key = self._generate_ori_key(arrow.motion)

        letter_data = self._get_letter_data(letter, ori_key)
        self._update_or_create_turn_data(letter_data, turns_tuple, arrow, adjustment)
        self._update_placement_json_data(letter, letter_data, ori_key)

    def update_specific_entry_in_json(
        self, letter: Letter, letter_data: dict, ori_key
    ) -> None:
        try:
            self._update_placement_json_data(letter, letter_data, ori_key)
        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")
