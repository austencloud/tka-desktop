from typing import TYPE_CHECKING
from enums.prop_type import PropType
from data.constants import BLUE, RED
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from ..legacy_settings_manager import LegacySettingsManager


class PropTypeChanger:
    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings_manager = settings_manager

    def replace_props(self, new_prop_type: PropType, pictograph: "LegacyPictograph"):
        for color, prop in pictograph.elements.props.items():
            new_prop = pictograph.managers.initializer.prop_factory.create_prop_of_type(
                prop, new_prop_type.name
            )
            self._update_pictograph_prop(pictograph, color, new_prop)
        pictograph.state.prop_type_enum = new_prop_type
        self._finalize_pictograph_update(pictograph)

    def _update_pictograph_prop(
        self, pictograph: "LegacyPictograph", color, new_prop: "Prop"
    ):
        old_prop = pictograph.elements.props[color]
        if hasattr(old_prop.state, "loc"):
            if not old_prop.state.loc:
                return
            old_prop.deleteLater()
            old_prop.hide()
            old_prop.prop_data = {
                "color": color,
                "prop_type": new_prop.prop_type_str,
                "loc": old_prop.state.loc,
                "ori": old_prop.state.ori,
            }
            old_prop_data = old_prop.prop_data
            pictograph.elements.props[color] = new_prop
            pictograph.addItem(new_prop)
            pictograph.elements.motion_set[color].prop = new_prop
            new_prop.updater.update_prop(old_prop_data)

    def _finalize_pictograph_update(self, pictograph: "LegacyPictograph"):
        pictograph.elements.red_prop = pictograph.elements.props[RED]
        pictograph.elements.blue_prop = pictograph.elements.props[BLUE]
        pictograph.managers.updater.update_pictograph()

    def apply_prop_type(self, pictographs: list["LegacyPictograph"]) -> None:
        prop_type = self.settings_manager.global_settings.get_prop_type()
        self.update_props_to_type(prop_type, pictographs)

    def update_props_to_type(
        self, new_prop_type: PropType, pictographs: list["LegacyPictograph"]
    ) -> None:
        for pictograph in pictographs:
            self.replace_props(new_prop_type, pictograph)
            pictograph.state.prop_type_enum = new_prop_type
            pictograph.managers.updater.update_pictograph()
