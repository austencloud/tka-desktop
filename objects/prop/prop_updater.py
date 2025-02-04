from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropUpdater:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop
        self.prop.setFlag(self.prop.GraphicsItemFlag.ItemIsSelectable, False)

    def update_prop(self, prop_dict: dict[str, Union[str, str, str]] = None) -> None:

        if prop_dict:
            self.prop.attr_manager.update_attributes(prop_dict)
        self.prop.pictograph.main_widget.svg_manager.prop_manager.update_prop_svg(
            self.prop
        )
        self.prop.rot_angle_manager.update_prop_rot_angle()
