from typing import TYPE_CHECKING
from data.constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .rotation_angle_override_manager import RotationAngleOverrideManager


class RotationAngleOverrideKeyGenerator:
    def __init__(self, manager: "RotationAngleOverrideManager"):
        self.manager = manager

    def get_start_ori_layer(self, arrow: Arrow) -> str:
        if arrow.motion.start_ori in [IN, OUT]:
            return "layer1"
        elif arrow.motion.start_ori in [CLOCK, COUNTER]:
            return "layer2"

    def get_end_ori_layer(self, arrow: Arrow) -> str:
        if arrow.motion.end_ori in [IN, OUT]:
            return "layer1"
        elif arrow.motion.end_ori in [CLOCK, COUNTER]:
            return "layer2"

    def generate_rotation_angle_override_key(self, arrow: Arrow) -> str:
        motion_type = arrow.motion.motion_type
        if arrow.pictograph.state.letter.value in ["α", "β", "Γ", "Φ-", "Ψ-", "Λ-"]:
            return f"{arrow.motion.color}_rot_angle_override"
        elif arrow.pictograph.managers.check.starts_from_mixed_orientation():
            start_ori_layer = self.get_start_ori_layer(arrow)
            return f"{motion_type}_from_{start_ori_layer}_rot_angle_override"
        elif (
            arrow.pictograph.managers.check.starts_from_standard_orientation()
            and arrow.pictograph.managers.check.ends_in_mixed_orientation()
        ):
            end_ori_layer = self.get_end_ori_layer(arrow)
            return f"{motion_type}_to_{end_ori_layer}_rot_angle_override"
        else:
            return f"{motion_type}_rot_angle_override"
