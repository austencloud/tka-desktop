from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MotionState:
    color: Optional[str] = None
    motion_type: Optional[str] = None
    turns: float = 0
    start_loc: Optional[str] = None
    end_loc: Optional[str] = None
    start_ori: Optional[str] = None
    end_ori: Optional[str] = None
    prop_rot_dir: Optional[str] = None
    lead_state: Optional[str] = None
    prefloat_motion_type: Optional[str] = None
    prefloat_prop_rot_dir: Optional[str] = None
