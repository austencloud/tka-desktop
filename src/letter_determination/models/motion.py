# models/motion.py
from dataclasses import dataclass
from enum import Enum

from data.constants import FLOAT


class str(Enum):
    FLOAT = "float"
    PRO = "pro"
    ANTI = "anti"
    STATIC = "static"


class str(Enum):
    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NONE = "none"


@dataclass
class MotionAttributes:
    motion_type: str
    start_ori: str
    prop_rot_dir: str
    start_loc: str
    end_loc: str
    turns: int
    end_ori: str
    prefloat_motion_type: str = None
    prefloat_prop_rot_dir: str = None

    @property
    def is_float(self) -> bool:
        return self.motion_type == FLOAT

    def serialize(self) -> dict:
        return {
            "motion_type": self.motion_type,
            "start_ori": self.start_ori,
            "prop_rot_dir": self.prop_rot_dir,
            "start_loc": self.start_loc,
            "end_loc": self.end_loc,
            "turns": self.turns,
            "end_ori": self.end_ori,
            "prefloat_motion_type": (
                self.prefloat_motion_type if self.prefloat_motion_type else None
            ),
            "prefloat_prop_rot_dir": (
                self.prefloat_prop_rot_dir if self.prefloat_prop_rot_dir else None
            ),
        }
