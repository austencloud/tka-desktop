from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from data.constants import BLUE, RED
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from ..settings_manager import SettingsManager


class PropTypeChanger:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager

    def replace_props(self, new_prop_type: PropType, pictograph: "Pictograph"):
        for color, prop in pictograph.elements.props.items():
            new_prop = pictograph.managers.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type.name
            )
            self._update_pictograph_prop(pictograph, color, new_prop)
        self._finalize_pictograph_update(pictograph)

    def _update_pictograph_prop(
        self, pictograph: "Pictograph", color, new_prop: "Prop"
    ):
        old_prop = pictograph.elements.props[color]
        if hasattr(old_prop, "loc"):
            old_prop.deleteLater()
            old_prop.hide()
            old_prop.prop_data = {
                "color": color,
                "prop_type": new_prop.prop_type,
                "loc": old_prop.loc,
                "ori": old_prop.ori,
            }
            old_prop_data = old_prop.prop_data
            pictograph.elements.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.elements.motions[color].prop = new_prop

            new_prop.updater.update_prop(old_prop_data)

    def _finalize_pictograph_update(self, pictograph: "Pictograph"):
        pictograph.elements.red_prop = pictograph.elements.props[RED]
        pictograph.elements.blue_prop = pictograph.elements.props[BLUE]
        pictograph.managers.updater.update_pictograph()

    def apply_prop_type(self, pictographs: list["Pictograph"]) -> None:
        prop_type = self.settings_manager.global_settings.get_prop_type()
        self.update_props_to_type(prop_type, pictographs)

    def update_props_to_type(
        self, new_prop_type: PropType, pictographs: list["Pictograph"]
    ) -> None:
        for pictograph in pictographs:
            if pictograph.state.letter:
                self.replace_props(new_prop_type, pictograph)
                pictograph.state.prop_type = new_prop_type
                pictograph.managers.updater.update_pictograph()
