# orientation_setter.py
from typing import TYPE_CHECKING
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import (
    BLUE,
    BLUE_ATTRS,
    RED_ATTRS,
    START_ORI,
    END_ORI,
    BOX,
    DIAMOND,
)

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
        self.beat_frame = self.ori_picker_box.graph_editor.sequence_workbench.beat_frame

    def set_orientation(self, orientation: str) -> None:
        """Apply the orientation to the related pictographs and data structures."""
        self.update_current_orientation_index(orientation)
        self._update_clickable_ori_label(orientation)

        if len(self.json_manager.loader_saver.load_current_sequence()) > 1:
            self._update_start_pos_ori(orientation)
            self._update_start_position_pictographs(orientation)
            self._update_graph_editor_orientation(orientation)
            self._refresh_option_picker()
        else:
            self._update_start_options(orientation)
            self._update_advanced_start_pos_picker(orientation)

        self._update_beats_from_current_sequence_json()

    def _update_graph_editor_orientation(self, orientation: str) -> None:
        self.ori_picker_box.graph_editor.pictograph_container.GE_view.pictograph.managers.updater.update_pictograph(
            {
                f"{self.color}_attributes": {
                    START_ORI: orientation,
                    END_ORI: orientation,
                }
            }
        )

    def update_current_orientation_index(self, orientation: str) -> None:
        self.ori_picker_widget.current_orientation_index = (
            self.ori_picker_widget.orientations.index(orientation)
        )

    def _update_clickable_ori_label(self, orientation: str) -> None:
        self.ori_picker_widget.clickable_ori_label.setText(orientation)

    def _update_start_pos_ori(self, orientation: str) -> None:
        self.json_manager.start_pos_handler.update_start_pos_ori(
            self.color, orientation
        )
        self.json_validation_engine.run(is_current_sequence=True)

    def _update_start_position_pictographs(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        start_position_pictographs = (
            construct_tab.start_pos_picker.pictograph_frame.start_positions
        )
        if start_position_pictographs:
            for pictograph in start_position_pictographs.values():
                pictograph.managers.updater.update_pictograph(
                    {
                        f"{self.color}_attributes": {
                            START_ORI: orientation,
                            END_ORI: orientation,
                        }
                    }
                )

    def _refresh_option_picker(self) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        self.option_picker = construct_tab.option_picker
        self.option_picker.updater.refresh_options()

    def _update_start_options(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        start_pos_picker = construct_tab.start_pos_picker
        for pictograph in start_pos_picker.start_options.values():
            pictograph.managers.updater.update_pictograph(
                {
                    f"{self.color}_attributes": {
                        START_ORI: orientation,
                        END_ORI: orientation,
                    }
                }
            )

    def _update_advanced_start_pos_picker(self, orientation: str) -> None:
        construct_tab = (
            self.ori_picker_box.graph_editor.sequence_workbench.main_widget.construct_tab
        )
        advanced_start_pos_picker = construct_tab.advanced_start_pos_picker
        grid_mode = DIAMOND
        if grid_mode == BOX:
            pictograph_list = advanced_start_pos_picker.box_pictographs
        elif grid_mode == DIAMOND:
            pictograph_list = advanced_start_pos_picker.diamond_pictographs
        else:
            pictograph_list = []
        for pictograph in pictograph_list:
            pictograph.managers.updater.update_pictograph(
                {
                    f"{self.color}_attributes": {
                        START_ORI: orientation,
                        END_ORI: orientation,
                    }
                }
            )

    def _update_beats_from_current_sequence_json(self) -> None:
        self.beat_frame.updater.update_beats_from_current_sequence_json()

    def set_initial_orientation(
        self, start_pos_pictograph: "LegacyPictograph", color: str
    ) -> None:
        initial_orientation = self._get_initial_orientation(start_pos_pictograph, color)
        self.current_orientation_index = self.ori_picker_widget.orientations.index(
            initial_orientation
        )
        self.ori_picker_widget.clickable_ori_label.setText(initial_orientation)

    def _get_initial_orientation(
        self, start_pos_pictograph: "LegacyPictograph", color: str
    ) -> str:
        if color == BLUE:
            return start_pos_pictograph.state.pictograph_data[BLUE_ATTRS][START_ORI]
        else:
            return start_pos_pictograph.state.pictograph_data[RED_ATTRS][START_ORI]
