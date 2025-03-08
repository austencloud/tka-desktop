# models/pictograph.py
from dataclasses import dataclass
from typing import Dict, Any
from ..models.motion import MotionAttributes


@dataclass
class PictographData:
    beat: int
    letter: str
    letter_type: str
    duration: int
    start_pos: str
    end_pos: str
    timing: str
    direction: str
    blue_attributes: MotionAttributes
    red_attributes: MotionAttributes

    def serialized_attributes(self) -> Dict[str, Any]:
        return {
            "blue_attributes": self.blue_attributes.serialize(),
            "red_attributes": self.red_attributes.serialize(),
        }
