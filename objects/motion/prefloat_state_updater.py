from dataclasses import dataclass
from typing import TYPE_CHECKING

from data.constants import PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR

if TYPE_CHECKING:
    from objects.motion.motion_state import MotionState


@dataclass
class PrefloatStateUpdater:
    motion_state: "MotionState"

    def update_prefloat_state(self, data: dict) -> None:
        from data.constants import FLOAT

        SHIFT_MOTIONS = ["pro", "anti", "float"]
        if self.motion_state.motion_type in SHIFT_MOTIONS:
            if PREFLOAT_MOTION_TYPE not in data:
                if self.motion_state.motion_type != FLOAT:
                    self.motion_state.prefloat_motion_type = (
                        self.motion_state.motion_type
                    )
            else:
                if data[PREFLOAT_MOTION_TYPE] != FLOAT:
                    self.motion_state.prefloat_motion_type = data[PREFLOAT_MOTION_TYPE]

            if PREFLOAT_PROP_ROT_DIR in data:
                if data[PREFLOAT_PROP_ROT_DIR] != "no_rot":
                    self.motion_state.prefloat_prop_rot_dir = data[
                        PREFLOAT_PROP_ROT_DIR
                    ]
