from typing import Any, Optional
from data.constants import (
    BLUE,
    BLUE_ATTRIBUTES,
    END_ORI,
    END_POS,
    PROP_ROT_DIR,
    RED,
    RED_ATTRIBUTES,
    START_ORI,
    START_POS,
)
from main_window.settings_manager.global_settings.app_context import AppContext


class OptionGetter:
    def __init__(self, pictograph_dataset: dict[Any, list[dict[str, Any]]]) -> None:
        self.pictograph_dataset = pictograph_dataset
        json_manager = AppContext.json_manager()
        self.ori_calculator = json_manager.ori_calculator
        self.ori_validation_engine = json_manager.ori_validation_engine

    def get_next_options(
        self, sequence: list[dict[str, Any]], selected_filter: Optional[str] = None
    ) -> list[dict[str, Any]]:
        options = self._load_all_next_option_dicts(sequence)
        if selected_filter is not None:
            options = [
                o
                for o in options
                if self._determine_reversal_filter(sequence, o) == selected_filter
            ]
        self.update_orientations(sequence, options)
        return options

    def update_orientations(
        self, sequence: list[dict[str, Any]], options: list[dict[str, Any]]
    ) -> None:
        last = sequence[-1]
        for option in options:
            option[BLUE_ATTRIBUTES][START_ORI] = last[BLUE_ATTRIBUTES][END_ORI]
            option[RED_ATTRIBUTES][START_ORI] = last[RED_ATTRIBUTES][END_ORI]
            option[BLUE_ATTRIBUTES][END_ORI] = self.ori_calculator.calculate_end_ori(
                option, BLUE
            )
            option[RED_ATTRIBUTES][END_ORI] = self.ori_calculator.calculate_end_ori(
                option, RED
            )

    def _load_all_next_option_dicts(
        self, sequence: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        next_opts: list[dict[str, Any]] = []
        last = sequence[-1] if not sequence[-1].get("is_placeholder") else sequence[-2]
        start = last.get(END_POS)
        if start:
            for group in self.pictograph_dataset.values():
                for item in group:
                    if item.get(START_POS) == start:
                        next_opts.append(item)
        for o in next_opts:
            for color in (BLUE, RED):
                o[f"{color}_attributes"][START_ORI] = last[f"{color}_attributes"][
                    END_ORI
                ]
            self.ori_validation_engine.validate_single_pictograph(o, last)
        return next_opts

    def _determine_reversal_filter(
        self, sequence: list[dict[str, Any]], o: dict[str, Any]
    ) -> str:
        blue_cont, red_cont = self._check_continuity(sequence, o)
        if blue_cont and red_cont:
            return "continuous"
        elif blue_cont ^ red_cont:
            return "one_reversal"
        return "two_reversals"

    def _check_continuity(
        self, sequence: list[dict[str, Any]], o: dict[str, Any]
    ) -> tuple[bool, bool]:
        def get_last_rot(seq: list[dict[str, Any]], color: str) -> Optional[str]:
            for item in reversed(seq):
                rot = item.get(f"{color}_attributes", {}).get(PROP_ROT_DIR)
                if rot and rot != "no_rot":
                    return rot
            return None

        last_blue = get_last_rot(sequence[1:], BLUE)
        last_red = get_last_rot(sequence[1:], RED)
        curr_blue = o.get(BLUE_ATTRIBUTES, {}).get(PROP_ROT_DIR, "no_rot")
        curr_red = o.get(RED_ATTRIBUTES, {}).get(PROP_ROT_DIR, "no_rot")
        if curr_blue == "no_rot":
            curr_blue = last_blue
        if curr_red == "no_rot":
            curr_red = last_red
        blue_cont = last_blue is None or curr_blue is None or curr_blue == last_blue
        red_cont = last_red is None or curr_red is None or curr_red == last_red
        return blue_cont, red_cont
