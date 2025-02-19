from typing import TYPE_CHECKING
from data.constants import BLUE, RED
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from ..settings_manager import SettingsManager


class PropTypeChanger:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager

    def replace_props(self, new_prop_type, pictograph: "Pictograph"):
        for color, prop in pictograph.props.items():
            new_prop = pictograph.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type
            )
            self._update_pictograph_prop(pictograph, color, new_prop)
        self._finalize_pictograph_update(pictograph)

    def _update_pictograph_prop(
        self, pictograph: "Pictograph", color, new_prop: "Prop"
    ):
        old_prop = pictograph.props[color]
        if hasattr(old_prop, "loc"):
            old_prop.deleteLater()
            old_prop.hide()
            old_prop_data = old_prop.prop_data
            pictograph.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.motions[color].prop = new_prop
            new_prop.motion.attr_manager.update_prop_ori()
            new_prop.updater.update_prop(old_prop_data)

    def _finalize_pictograph_update(self, pictograph: "Pictograph"):
        pictograph.red_prop = pictograph.props[RED]
        pictograph.blue_prop = pictograph.props[BLUE]
        pictograph.updater.update_pictograph()

    def apply_prop_type(self, pictographs: list["Pictograph"]) -> None:
        prop_type = self.settings_manager.global_settings.get_prop_type()
        self.update_props_to_type(prop_type, pictographs)


    def update_props_to_type(self, new_prop_type, pictographs: list["Pictograph"]) -> None:
        for pictograph in pictographs:
            if pictograph:
                self.replace_props(new_prop_type, pictograph)
                pictograph.prop_type = new_prop_type
                pictograph.updater.update_pictograph()


    def _update_start_pos_view(self, new_prop_type):
        start_pos_view = (
            self.main_window.main_widget.sequence_workbench.beat_frame.start_pos_view
        )
        if hasattr(start_pos_view, "start_pos"):
            start_pos = start_pos_view.start_pos
            if start_pos.view.is_filled:
                self.replace_props(new_prop_type, start_pos)

    def _update_json_manager(self, new_prop_type):
        json_manager = self.main_window.main_widget.json_manager
        json_manager.updater.prop_type_updater.update_prop_type_in_json(new_prop_type)
