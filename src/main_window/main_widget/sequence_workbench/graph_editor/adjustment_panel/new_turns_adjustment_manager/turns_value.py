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
        if isinstance(value, (int, float)) and not (-0.5 <= value <= 3):
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
            new_value = 0
        else:
            new_value = self.raw_value + delta

        if new_value < -0.5:
            return TurnsValue("fl")
        if new_value < 0:
            return TurnsValue("fl")
        return TurnsValue(min(3, new_value))

    def __eq__(self, other: "TurnsValue"):
        return self.raw_value == other.raw_value
