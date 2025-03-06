from enum import Enum


class CAPType(Enum):
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_ROTATED = "strict_rotated"
    STRICT_SWAPPED = "strict_swapped"
    MIRRORED_SWAPPED = "mirrored_swapped"

    @staticmethod
    def from_str(s: str):
        """Fast lookup instead of iterating over the enum."""
        _lookup_map = {cap_type.value: cap_type for cap_type in CAPType}
        try:
            return _lookup_map[s]
        except KeyError:
            raise ValueError(f"Invalid CAPType string: {s}")
