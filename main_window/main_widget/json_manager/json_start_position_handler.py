from typing import TYPE_CHECKING
from data.constants import BLUE_ATTRIBUTES, NO_ROT, RED_ATTRIBUTES
from base_widgets.pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonStartPositionHandler:
    def __init__(self, manager: "JsonManager"):
        self.manager = manager

    def set_start_position_data(self, start_pos_pictograph: Pictograph) -> None:
        red_start_ori = start_pos_pictograph.state.pictograph_data[RED_ATTRIBUTES][
            "start_ori"
        ]
        blue_start_ori = start_pos_pictograph.state.pictograph_data[BLUE_ATTRIBUTES][
            "start_ori"
        ]

        sequence = self.manager.loader_saver.load_current_sequence()

        start_position_dict = {
            "beat": 0,
            "sequence_start_position": self.get_sequence_start_position(
                start_pos_pictograph
            ),
            "letter": start_pos_pictograph.state.letter.name,
            "end_pos": start_pos_pictograph.state.end_pos,
            "timing": start_pos_pictograph.state.timing,
            "direction": start_pos_pictograph.state.direction,
            BLUE_ATTRIBUTES: {
                "start_loc": start_pos_pictograph.elements.blue_motion.state.start_loc,
                "end_loc": start_pos_pictograph.elements.blue_motion.state.end_loc,
                "start_ori": blue_start_ori,
                "end_ori": blue_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.elements.blue_motion.state.motion_type,
            },
            RED_ATTRIBUTES: {
                "start_loc": start_pos_pictograph.elements.red_motion.state.start_loc,
                "end_loc": start_pos_pictograph.elements.red_motion.state.end_loc,
                "start_ori": red_start_ori,
                "end_ori": red_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.elements.red_motion.state.motion_type,
            },
        }

        if len(sequence) == 1:
            sequence.append(start_position_dict)
        else:
            sequence.insert(1, start_position_dict)

        self.manager.loader_saver.save_current_sequence(sequence)

    def update_start_pos_ori(self, color: str, ori: int) -> None:
        sequence = self.manager.loader_saver.load_current_sequence()
        if sequence:
            sequence[1][f"{color}_attributes"]["end_ori"] = ori
            sequence[1][f"{color}_attributes"]["start_ori"] = ori
            self.manager.loader_saver.save_current_sequence(sequence)

    def get_sequence_start_position(self, start_pos_pictograph: Pictograph) -> str:
        return start_pos_pictograph.state.end_pos.rstrip("0123456789")
