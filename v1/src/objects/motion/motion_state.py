from dataclasses import dataclass, field
from typing import Optional, Union

from data.constants import PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR, PRO, ANTI, FLOAT
from objects.motion.prefloat_state_updater import PrefloatStateUpdater


@dataclass
class MotionState:
    color: Optional[str] = None
    motion_type: Optional[str] = None
    turns: Union[int, float, str] = 0
    start_loc: Optional[str] = None
    end_loc: Optional[str] = None
    start_ori: Optional[str] = None
    end_ori: Optional[str] = None
    prop_rot_dir: Optional[str] = None
    lead_state: Optional[str] = None
    prefloat_motion_type: Optional[str] = None
    prefloat_prop_rot_dir: Optional[str] = None

    def __post_init__(self):
        self.prefloat_handler = PrefloatStateUpdater(self)

    def update_motion_state(self, motion_data: dict) -> None:
        SHIFT_MOTIONS = [PRO, ANTI, FLOAT]

        for key, value in motion_data.items():
            if value is not None:
                if key in [PREFLOAT_MOTION_TYPE, PREFLOAT_PROP_ROT_DIR]:
                    if self.motion_type in SHIFT_MOTIONS:
                        setattr(self, key, value)
                else:
                    if hasattr(self, key):
                        setattr(self, key, value)

        self.prefloat_handler.update_prefloat_state(motion_data)
