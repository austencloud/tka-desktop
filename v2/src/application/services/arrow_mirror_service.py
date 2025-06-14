"""
Arrow mirroring service for handling SVG transformations based on motion type.
"""

from typing import TYPE_CHECKING
from PyQt6.QtGui import QTransform
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from domain.models.core_models import MotionType, RotationDirection

if TYPE_CHECKING:
    from domain.models.pictograph_models import ArrowData


class ArrowMirrorService:
    def __init__(self):
        self.mirror_conditions = {
            "anti": {
                "cw": True,
                "ccw": False,
            },
            "other": {
                "cw": False,
                "ccw": True,
            },
        }

    def should_mirror_arrow(self, arrow_data: "ArrowData") -> bool:
        if not arrow_data.motion_data:
            return False

        motion_type = arrow_data.motion_data.motion_type.value.lower()
        prop_rot_dir = arrow_data.motion_data.prop_rot_dir.value.lower()

        if motion_type == "anti":
            return self.mirror_conditions["anti"].get(prop_rot_dir, False)
        else:
            return self.mirror_conditions["other"].get(prop_rot_dir, False)

    def apply_mirror_transform(
        self, arrow_item: QGraphicsSvgItem, should_mirror: bool
    ) -> None:
        center_x = arrow_item.boundingRect().center().x()
        center_y = arrow_item.boundingRect().center().y()

        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(-1 if should_mirror else 1, 1)
        transform.translate(-center_x, -center_y)

        arrow_item.setTransform(transform)

    def update_arrow_mirror(
        self, arrow_item: QGraphicsSvgItem, arrow_data: "ArrowData"
    ) -> None:
        should_mirror = self.should_mirror_arrow(arrow_data)
        self.apply_mirror_transform(arrow_item, should_mirror)
