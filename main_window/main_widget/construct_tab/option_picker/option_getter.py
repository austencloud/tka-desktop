from typing import TYPE_CHECKING, Optional
from data.constants import END_POS, START_POS
from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    pass


class OptionGetter:
    def __init__(self, pictograph_dataset: dict):
        self.pictograph_dataset = pictograph_dataset
        json_manager = AppContext.json_manager()
        self.ori_calculator = json_manager.ori_calculator
        self.ori_validation_engine = json_manager.ori_validation_engine

    def get_next_options(
        self, sequence: list, selected_filter: Optional[str] = None
    ) -> list[dict]:
        opts = self._load_all_next_option_dicts(sequence)
        if selected_filter is not None:
            opts = self._apply_filter(sequence, opts, selected_filter)
        self.update_orientations(sequence, opts)
        return opts

    def update_orientations(self, sequence, opts):
        for o in opts:
            o["blue_attributes"]["start_ori"] = sequence[-1]["blue_attributes"][
                "end_ori"
            ]
            o["red_attributes"]["start_ori"] = sequence[-1]["red_attributes"]["end_ori"]
        for o in opts:
            o["blue_attributes"]["end_ori"] = self.ori_calculator.calculate_end_ori(
                o, "blue"
            )
            o["red_attributes"]["end_ori"] = self.ori_calculator.calculate_end_ori(
                o, "red"
            )

    def _apply_filter(
        self, sequence: list, opts: list, selected_filter: str
    ) -> list[dict]:
        return [
            o
            for o in opts
            if self._determine_reversal_filter(sequence, o) == selected_filter
        ]

    def _determine_reversal_filter(self, sequence: list, o: dict) -> str:
        blue, red = self._check_continuity(sequence, o)
        if blue and red:
            return "continuous"
        elif blue ^ red:
            return "one_reversal"
        return "two_reversals"

    def _load_all_next_option_dicts(self, sequence: list) -> list[dict]:
        next_opts = []
        last = sequence[-1] if not sequence[-1].get("is_placeholder") else sequence[-2]
        start = last[END_POS]
        if start:
            for lst in self.pictograph_dataset.values():
                for d in lst:
                    if d[START_POS] == start:
                        next_opts.append(d)
        for o in next_opts:
            for color in ("blue", "red"):
                o[f"{color}_attributes"]["start_ori"] = last[f"{color}_attributes"][
                    "end_ori"
                ]
            self.ori_validation_engine.validate_single_pictograph(o, last)
        return next_opts

    def _check_continuity(self, sequence: list, o: dict):
        def get_last_rot(sequence, color):
            return next(
                (
                    item[f"{color}_attributes"].get("prop_rot_dir")
                    for item in reversed(sequence)
                    if item[f"{color}_attributes"].get("prop_rot_dir") != "no_rot"
                ),
                None,
            )

        blue = get_last_rot(sequence[1:], "blue") == o["blue_attributes"].get(
            "prop_rot_dir", "no_rot"
        )
        red = get_last_rot(sequence[1:], "red") == o["red_attributes"].get(
            "prop_rot_dir", "no_rot"
        )
        return blue, red

    def _get_last_prop_rot_dir(self, sequence: list, color: str) -> Optional[str]:
        for item in reversed(sequence):
            d = item[f"{color}_attributes"].get("prop_rot_dir")
            if d != "no_rot":
                return d
        return None
