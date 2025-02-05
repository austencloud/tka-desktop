from typing import TYPE_CHECKING
from data.constants import (
    ANTI,
    CCW_HANDPATH,
    CLOCK,
    CLOCKWISE,
    COUNTER,
    COUNTER_CLOCKWISE,
    CW_HANDPATH,
    DASH,
    IN,
    OUT,
    PRO,
    STATIC,
)
from objects.motion.managers.handpath_calculator import HandpathCalculator

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonOriCalculator:
    def __init__(self, json_manager: "JsonManager"):
        self.main_widget = json_manager.main_widget
        self.handpath_calculator = HandpathCalculator()

    def calculate_end_ori(self, pictograph_data, color: str):
        motion_type = pictograph_data[f"{color}_attributes"]["motion_type"]
        if (pictograph_data[f"{color}_attributes"]["turns"]) != "fl":
            turns = float(pictograph_data[f"{color}_attributes"]["turns"])
        else:
            turns = pictograph_data[f"{color}_attributes"]["turns"]
        start_ori = pictograph_data[f"{color}_attributes"]["start_ori"]
        prop_rot_dir = pictograph_data[f"{color}_attributes"]["prop_rot_dir"]
        start_loc = pictograph_data[f"{color}_attributes"]["start_loc"]
        end_loc = pictograph_data[f"{color}_attributes"]["end_loc"]
        if motion_type == "float":
            handpath_direction = self.handpath_calculator.get_hand_rot_dir(
                pictograph_data[f"{color}_attributes"]["start_loc"],
                pictograph_data[f"{color}_attributes"]["end_loc"],
            )
            return self.calculate_float_orientation(start_ori, handpath_direction)
        else:
            return self.calculate_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir, start_loc, end_loc
            )

    def calculate_turn_orientation(
        self, motion_type, turns, start_ori, prop_rot_dir, start_loc, end_loc
    ):
        if turns in [0, 1, 2, 3]:
            return self.calculate_whole_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir
            )
        elif turns == "fl":
            return self.calculate_float_orientation(
                start_ori,
                self.handpath_calculator.get_hand_rot_dir(start_loc, end_loc),
            )
        else:
            return self.calculate_half_turn_orientation(
                motion_type, turns, start_ori, prop_rot_dir
            )

    def calculate_whole_turn_orientation(
        self, motion_type, turns, start_ori, prop_rot_dir
    ):
        if motion_type in ["pro", "static"]:
            if turns % 2 == 0:
                return start_ori
            else:
                return self.switch_orientation(start_ori)
        elif motion_type in ["anti", "dash"]:
            if turns % 2 == 0:
                return self.switch_orientation(start_ori)
            else:
                return start_ori

    def calculate_half_turn_orientation(
        self, motion_type, turns, start_ori, prop_rot_dir
    ):
        if motion_type in [ANTI, DASH]:
            orientation_map = {
                (IN, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (IN, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (CLOCK, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (CLOCK, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
            }
        elif motion_type in [PRO, STATIC]:
            orientation_map = {
                (IN, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (IN, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (CLOCK, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (CLOCK, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
            }

        return orientation_map.get((start_ori, prop_rot_dir))

    def calculate_float_orientation(self, start_ori, handpath_direction):
        orientation_map = {
            (IN, CW_HANDPATH): CLOCK,
            (IN, CCW_HANDPATH): COUNTER,
            (OUT, CW_HANDPATH): COUNTER,
            (OUT, CCW_HANDPATH): CLOCK,
            (CLOCK, CW_HANDPATH): OUT,
            (CLOCK, CCW_HANDPATH): IN,
            (COUNTER, CW_HANDPATH): IN,
            (COUNTER, CCW_HANDPATH): OUT,
        }
        return orientation_map.get((start_ori, handpath_direction), start_ori)

    def switch_orientation(self, ori):
        switch_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        return switch_map.get(ori, ori)
