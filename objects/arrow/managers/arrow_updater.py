from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowUpdater:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_arrow(self, arrow_dict=None) -> None:
        if arrow_dict:
            self.arrow.attr_manager.update_attributes(arrow_dict)
        self.arrow.pictograph.main_widget.svg_manager.arrow_manager.update_arrow_svg(
            self.arrow
        )
        self.arrow.mirror_manager.update_mirror()
        self.arrow.location_manager.update_location()
        self.arrow.rot_angle_manager.update_rotation()
        # self.arrow.update()
        # self.arrow.pictograph.update()
