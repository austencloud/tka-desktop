# === turns_box/domain/turns_value.py ===
from dataclasses import dataclass
from typing import Union, Optional, Literal


@dataclass
class TurnsValue:
    """Represents a turns value which can be a number or 'fl' (float)"""

    raw_value: Union[int, float, Literal["fl"]]

    def __post_init__(self):
        # Validate the value
        if not (isinstance(self.raw_value, (int, float)) or self.raw_value == "fl"):
            raise ValueError(f"Invalid turns value: {self.raw_value}")

    @property
    def is_float(self) -> bool:
        """Check if this is a float ('fl') value"""
        return self.raw_value == "fl"

    @property
    def is_zero(self) -> bool:
        """Check if the value is zero"""
        return self.raw_value == 0

    @property
    def display_text(self) -> str:
        """Get the display text for this value"""
        if self.is_float:
            return "fl"
        # Format with no decimal for whole numbers
        if isinstance(self.raw_value, float) and self.raw_value.is_integer():
            return str(int(self.raw_value))
        return str(self.raw_value)

    def add(self, amount: Union[int, float]) -> "TurnsValue":
        """Add a value and return a new TurnsValue"""
        if self.is_float:
            # Can't add to float type
            return self
        return TurnsValue(self.raw_value + amount)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TurnsValue):
            return False
        return self.raw_value == other.raw_value
