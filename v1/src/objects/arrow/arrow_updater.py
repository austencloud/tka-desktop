# objects/arrow/arrow_updater.py
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowUpdater:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_arrow(self, arrow_data=None) -> None:
        if arrow_data:
            self.arrow.state.update_from_dict(arrow_data)
        self.arrow.pictograph.managers.svg_manager.arrow_manager.update_arrow_svg(
            self.arrow
        )
        self.arrow.mirror_manager.update_mirror()
        self.arrow.location_manager.update_location()
        self.arrow.rot_angle_manager.update_rotation()

        from base_widgets.base_beat_frame import AppContext

        visible = (
            AppContext()
            .settings_manager()
            .visibility.get_motion_visibility(self.arrow.state.color)
        )
        self.arrow.setVisible(visible)
