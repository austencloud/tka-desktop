from dataclasses import dataclass
from typing import TYPE_CHECKING

from data.constants import (
    ANTI,
    NO_ROT,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
)

if TYPE_CHECKING:
    from objects.motion.motion_state import MotionState


@dataclass
class PrefloatStateUpdater:
    motion_state: "MotionState"

    def update_prefloat_state(self, data: dict) -> None:
        from data.constants import FLOAT

        SHIFT_MOTIONS = [PRO, ANTI, FLOAT]
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
                if data[PREFLOAT_PROP_ROT_DIR] != NO_ROT:
                    self.motion_state.prefloat_prop_rot_dir = data[
                        PREFLOAT_PROP_ROT_DIR
                    ]
