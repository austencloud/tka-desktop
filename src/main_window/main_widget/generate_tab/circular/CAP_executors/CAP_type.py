from enum import Enum


class CAPType(Enum):
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_ROTATED = "strict_rotated"
    STRICT_SWAPPED = "strict_swapped"
    MIRRORED_SWAPPED = "mirrored_swapped"

    @staticmethod
    def from_str(s):
        for cap_type in CAPType:
            if cap_type.value == s:
                return cap_type
        raise ValueError(f"Invalid CAPType string: {s}")