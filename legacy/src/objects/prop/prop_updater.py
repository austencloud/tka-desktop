from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropUpdater:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop
        self.prop.setFlag(self.prop.GraphicsItemFlag.ItemIsSelectable, False)

    def update_prop(self, prop_data: dict[str, Union[str, str, str]] = None) -> None:
        if prop_data:
            self.prop.attr_manager.update_attributes(prop_data)
        self.prop.pictograph.managers.svg_manager.prop_manager.update_prop_image(
            self.prop
        )
        self.prop.rot_angle_manager.update_prop_rot_angle()

        from base_widgets.base_beat_frame import AppContext

        if not hasattr(self.prop.pictograph, "example_data"):
            self.prop.setVisible(
                (
                    AppContext()
                    .settings_manager()
                    .visibility.get_motion_visibility(self.prop.state.color)
                )
            )
