from typing import TYPE_CHECKING
from PyQt6.QtGui import QTransform
from data.constants import ANTI, CLOCKWISE, COUNTER_CLOCKWISE

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowMirrorManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow

    def update_mirror(self) -> None:
        self._set_mirror_conditions()
        self._set_svg_mirror(self.arrow)

    def _set_mirror_conditions(self) -> None:
        mirror_conditions = {
            ANTI: {
                CLOCKWISE: True,
                COUNTER_CLOCKWISE: False,
            },
            "other": {
                CLOCKWISE: False,
                COUNTER_CLOCKWISE: True,
            },
        }

        motion_type = self.arrow.motion.state.motion_type
        prop_rot_dir = self.arrow.motion.state.prop_rot_dir
        if motion_type in mirror_conditions:
            is_svg_mirrored = mirror_conditions[motion_type].get(prop_rot_dir)
        else:
            is_svg_mirrored = mirror_conditions["other"].get(prop_rot_dir, False)

        self.arrow.state.is_svg_mirrored = is_svg_mirrored

    def _set_svg_mirror(self, arrow: "Arrow") -> None:
        center_x = arrow.boundingRect().center().x()
        center_y = arrow.boundingRect().center().y()
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(-1 if arrow.state.is_svg_mirrored else 1, 1)
        transform.translate(-center_x, -center_y)
        arrow.setTransform(transform)
