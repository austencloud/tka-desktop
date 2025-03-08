# models/motion.py
from dataclasses import dataclass
from enum import Enum

class MotionType(Enum):
    FLOAT = "float"
    PRO = "pro"
    ANTI = "anti"
    STATIC = "static"

class RotationDirection(Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NONE = "none"

@dataclass
class MotionAttributes:
    motion_type: MotionType
    start_ori: str
    prop_rot_dir: RotationDirection
    start_loc: str
    end_loc: str
    turns: int
    end_ori: str
    prefloat_motion_type: MotionType = None
    prefloat_prop_rot_dir: RotationDirection = None
    
    @property
    def is_float(self) -> bool:
        return self.motion_type == MotionType.FLOAT
    
    def serialize(self) -> dict:
        return {
            "motion_type": self.motion_type.value,
            "start_ori": self.start_ori,
            "prop_rot_dir": self.prop_rot_dir.value,
            "start_loc": self.start_loc,
            "end_loc": self.end_loc,
            "turns": self.turns,
            "end_ori": self.end_ori,
            "prefloat_motion_type": self.prefloat_motion_type.value if self.prefloat_motion_type else None,
            "prefloat_prop_rot_dir": self.prefloat_prop_rot_dir.value if self.prefloat_prop_rot_dir else None
        }