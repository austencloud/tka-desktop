# orientation_setter.py
from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import BLUE, START_ORI, END_ORI, BOX, DIAMOND

if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class OrientationSetter:
    def __init__(self, ori_picker_widget: "OriPickerWidget") -> None:
        self.ori_picker_widget = ori_picker_widget
        self.color = ori_picker_widget.color
        self.json_manager = ori_picker_widget.json_manager
        self.json_validation_engine = ori_picker_widget.json_validation_engine
        self.ori_picker_box = ori_picker_widget.ori_picker_box
        self.ori_adjusted = ori_picker_widget.ori_adjusted
        self.option_picker = ori_picker_widget.option_picker
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_widget.beat_frame

    def set_orientation(self, orientation: str) -> None:
        """Apply the orientation to the related pictographs and data structures."""
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_widget.main_widget.construct_tab
        )
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.orientations.index(orientation)
        )
        start_pos_picker = construct_tab.start_pos_picker
        advanced_start_pos_picker = construct_tab.advanced_start_pos_picker
        
        self.ori_picker_widget.clickable_ori_label.setText(orientation)
        if len(self.json_manager.loader_saver.load_current_sequence_json()) > 1:
            self.json_manager.start_pos_handler.update_start_pos_ori(
                self.color, orientation
            )
            self.json_validation_engine.run(is_current_sequence=True)
            start_position_pictographs = (
                construct_tab.start_pos_picker.pictograph_frame.start_positions
            )
            if start_position_pictographs:
                for pictograph in start_position_pictographs.values():
                    pictograph.updater.update_pictograph(
                        {
                            f"{self.color}_attributes": {
                                START_ORI: orientation,
                                END_ORI: orientation,
                            }
                        }
                    )
            self.option_picker = construct_tab.option_picker
            self.option_picker.update_option_picker()
        else:
            for pictograph in start_pos_picker.start_options.values():
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

            grid_mode = DIAMOND
            if grid_mode == BOX:
                pictograph_list = advanced_start_pos_picker.box_pictographs
            elif grid_mode == DIAMOND:
                pictograph_list = advanced_start_pos_picker.diamond_pictographs
            else:
                pictograph_list = []
            for pictograph in pictograph_list:
                pictograph.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

        self.beat_frame.updater.update_beats_from_current_sequence_json()

    def set_initial_orientation(
        self, start_pos_pictograph: "BasePictograph", color: str
    ) -> None:
        if color == BLUE:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "blue_attributes"
            ][START_ORI]
        else:
            initial_orientation = start_pos_pictograph.pictograph_dict[
                "red_attributes"
            ][START_ORI]
        self.current_orientation_index = self.ori_picker_widget.orientations.index(
            initial_orientation
        )
        self.ori_picker_widget.clickable_ori_label.setText(initial_orientation)
