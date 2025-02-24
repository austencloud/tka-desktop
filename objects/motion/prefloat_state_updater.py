from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion_state import MotionState


@dataclass
class PrefloatStateUpdater:
    motion_state: "MotionState"

    def update_prefloat_state(self, data: dict) -> None:
        from data.constants import FLOAT

        SHIFT_MOTIONS = ["pro", "anti", "float"]
        if self.motion_state.motion_type in SHIFT_MOTIONS:
            if "prefloat_motion_type" not in data:
                if self.motion_state.motion_type != FLOAT:
                    self.motion_state.prefloat_motion_type = (
                        self.motion_state.motion_type
                    )
            else:
                if data["prefloat_motion_type"] != FLOAT:
                    self.motion_state.prefloat_motion_type = data[
                        "prefloat_motion_type"
                    ]

            if "prefloat_prop_rot_dir" in data:
                if data["prefloat_prop_rot_dir"] != "no_rot":
                    self.motion_state.prefloat_prop_rot_dir = data[
                        "prefloat_prop_rot_dir"
                    ]
