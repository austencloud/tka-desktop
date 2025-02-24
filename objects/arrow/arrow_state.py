from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class ArrowState:
    color: Optional[str] = None
    is_svg_mirrored: Optional[bool] = None
    loc: Optional[str] = None
    motion_type: Optional[str] = None
    turns: Optional[Union[int, float]] = None
    initialized: bool = False

    def update_from_dict(self, arrow_data: dict[str, Union[str, int, float]]) -> None:
        for key, value in arrow_data.items():
            if hasattr(self, key):
                setattr(self, key, value)
