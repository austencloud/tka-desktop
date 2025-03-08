# New domain model for turns logic
from typing import Union


class TurnsValue:
    def __init__(self, value: Union[int, float, str]):
        self._validate(value)
        self.raw_value = value

    @staticmethod
    def _validate(value):
        if not isinstance(value, (int, float, str)):
            raise ValueError("Invalid turns type")
        if isinstance(value, str) and value != "fl":
            raise ValueError("Invalid string value")
        if isinstance(value, (int, float)) and not (0 <= value <= 3):
            raise ValueError("Turns out of range")

    @property
    def display_value(self) -> str:
        return (
            "fl"
            if self.raw_value == "fl"
            else str(float(self.raw_value)).rstrip("0").rstrip(".")
        )

    def adjust(self, delta: Union[int, float]) -> "TurnsValue":
        if self.raw_value == "fl":
            return TurnsValue(0) if delta > 0 else self
        new_value = self.raw_value + delta
        return TurnsValue(max(0, min(3, new_value)))

    def __eq__(self, other: "TurnsValue"):
        return self.raw_value == other.raw_value
