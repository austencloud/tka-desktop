from typing import TYPE_CHECKING, Optional
from data.constants import END_POS, START_POS
from main_window.settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_ori_calculator import (
        JsonOriCalculator,
    )
    from main_window.main_widget.json_manager.json_ori_validation_engine import (
        JsonOriValidationEngine,
    )
    from .option_picker import OptionPicker


class OptionGetter:
    """Fetches and filters next pictograph options based on the current sequence."""

    def __init__(self, pictograph_dataset: dict):
        """Initialize with references to OptionPicker, JsonManager, and MainWidget."""
        self.pictograph_dataset = pictograph_dataset
        json_manager = AppContext.json_manager()
        self.ori_calculator = json_manager.ori_calculator
        self.ori_validation_engine = json_manager.ori_validation_engine

    def get_next_options(
        self, sequence: list, selected_filter: Optional[str] = None
    ) -> list[dict]:
        """Return next possible pictographs for the current sequence, applying filters."""
        all_options = self._load_all_next_option_dicts(sequence)
        filtered_options = (
            self._apply_filter(sequence, all_options, selected_filter)
            if selected_filter is not None
            else all_options
        )

        self.update_orientations(sequence, filtered_options)

        return filtered_options

    def update_orientations(self, sequence, filtered_options):
        for option in filtered_options:
            option["blue_attributes"]["start_ori"] = sequence[-1]["blue_attributes"][
                "end_ori"
            ]
            option["red_attributes"]["start_ori"] = sequence[-1]["red_attributes"][
                "end_ori"
            ]

        for option in filtered_options:
            option["blue_attributes"]["end_ori"] = (
                self.ori_calculator.calculate_end_ori(option, "blue")
            )
            option["red_attributes"]["end_ori"] = self.ori_calculator.calculate_end_ori(
                option, "red"
            )

    def _apply_filter(
        self, sequence: list, options: list, selected_filter: str
    ) -> list[dict]:
        """Apply a reversal-based filter to the given list of options."""
        result = []
        for pictograph_data in options:
            if (
                self._determine_reversal_filter(sequence, pictograph_data)
                == selected_filter
            ):
                result.append(pictograph_data)
        return result

    def _determine_reversal_filter(self, sequence: list, pictograph_data: dict) -> str:
        """Determine if pictograph is 'continuous', 'one_reversal', or 'two_reversals'."""
        blue_cont, red_cont = self._check_continuity(sequence, pictograph_data)
        if blue_cont and red_cont:
            return "continuous"
        elif blue_cont ^ red_cont:  # XOR
            return "one_reversal"
        return "two_reversals"

    def _load_all_next_option_dicts(self, sequence: list) -> list[dict]:
        """Return all possible next pictographs whose start_pos matches the sequence end."""
        next_opts = []
        last_pictograph = (
            sequence[-1] if not sequence[-1].get("is_placeholder") else sequence[-2]
        )
        start_pos = last_pictograph[END_POS]

        if start_pos:
            for dict_list in self.pictograph_dataset.values():
                for pict_dict in dict_list:
                    if pict_dict[START_POS] == start_pos:
                        next_opts.append(pict_dict)

        for opt in next_opts:
            for color in ("blue", "red"):
                opt[f"{color}_attributes"]["start_ori"] = last_pictograph[
                    f"{color}_attributes"
                ]["end_ori"]
            self.ori_validation_engine.validate_single_pictograph(opt, last_pictograph)

        return next_opts

    def _check_continuity(self, sequence: list, pictograph: dict):
        """Check if this pictograph's prop_rot_dir is continuous with the last known directions."""
        last_blue_dir = self._get_last_prop_rot_dir(sequence[1:], "blue")
        last_red_dir = self._get_last_prop_rot_dir(sequence[1:], "red")

        curr_blue_dir = pictograph["blue_attributes"]["prop_rot_dir"]
        curr_red_dir = pictograph["red_attributes"]["prop_rot_dir"]

        if curr_blue_dir == "no_rot":
            curr_blue_dir = last_blue_dir
        if curr_red_dir == "no_rot":
            curr_red_dir = last_red_dir

        blue_cont = (
            last_blue_dir is None
            or curr_blue_dir is None
            or curr_blue_dir == last_blue_dir
        )
        red_cont = (
            last_red_dir is None or curr_red_dir is None or curr_red_dir == last_red_dir
        )
        return blue_cont, red_cont

    def _get_last_prop_rot_dir(self, sequence: list, color: str) -> Optional[str]:
        """Return the most recent prop_rot_dir for the given color, ignoring 'no_rot'."""
        for pictograph in reversed(sequence):
            direction = pictograph[f"{color}_attributes"].get("prop_rot_dir")
            if direction != "no_rot":
                return direction
        return None
