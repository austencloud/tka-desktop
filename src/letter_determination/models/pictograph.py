# models/pictograph.py
from dataclasses import dataclass
from typing import Dict, Any
from ..models.motion import dict


@dataclass
class dict:
    beat: int
    letter: str
    letter_type: str
    duration: int
    start_pos: str
    end_pos: str
    timing: str
    direction: str
    blue_attributes: dict
    red_attributes: dict

    def serialized_attributes(self) -> Dict[str, Any]:
        return {
            "blue_attributes": self.blue_attributes.serialize(),
            "red_attributes": self.red_attributes.serialize(),
        }
