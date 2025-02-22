from dataclasses import dataclass, field
from typing import Optional, Union

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

    def update_motion_state(self, data: dict) -> None:
        for key, value in data.items():
            if value is not None:
                if hasattr(self, key):
                    setattr(self, key, value)

        self.prefloat_handler.update_prefloat_state(data)
