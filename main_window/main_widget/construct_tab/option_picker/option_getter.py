from typing import Any, Optional
from data.constants import END_POS, START_POS
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
        for o in options:
            o["blue_attributes"]["start_ori"] = last["blue_attributes"]["end_ori"]
            o["red_attributes"]["start_ori"] = last["red_attributes"]["end_ori"]
            o["blue_attributes"]["end_ori"] = self.ori_calculator.calculate_end_ori(
                o, "blue"
            )
            o["red_attributes"]["end_ori"] = self.ori_calculator.calculate_end_ori(
                o, "red"
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
            for color in ("blue", "red"):
                o[f"{color}_attributes"]["start_ori"] = last[f"{color}_attributes"][
                    "end_ori"
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
                rot = item.get(f"{color}_attributes", {}).get("prop_rot_dir")
                if rot and rot != "no_rot":
                    return rot
            return None

        last_blue = get_last_rot(sequence[1:], "blue")
        last_red = get_last_rot(sequence[1:], "red")
        curr_blue = o.get("blue_attributes", {}).get("prop_rot_dir", "no_rot")
        curr_red = o.get("red_attributes", {}).get("prop_rot_dir", "no_rot")
        if curr_blue == "no_rot":
            curr_blue = last_blue
        if curr_red == "no_rot":
            curr_red = last_red
        blue_cont = last_blue is None or curr_blue is None or curr_blue == last_blue
        red_cont = last_red is None or curr_red is None or curr_red == last_red
        return blue_cont, red_cont
