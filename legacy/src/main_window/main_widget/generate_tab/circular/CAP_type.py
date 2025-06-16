from enum import Enum


class CAPType(Enum):
    STRICT_ROTATED = "strict_rotated"
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_SWAPPED = "strict_swapped"
    STRICT_COMPLEMENTARY = "strict_complementary"

    SWAPPED_COMPLEMENTARY = "swapped_complementary"

    ROTATED_COMPLEMENTARY = "rotated_complementary"
    MIRRORED_SWAPPED = "mirrored_swapped"
    
    MIRRORED_COMPLEMENTARY = "mirrored_complementary"
    ROTATED_SWAPPED = "rotated_swapped"

    MIRRORED_ROTATED = "mirrored_rotated"
    MIRRORED_COMPLEMENTARY_ROTATED = "mirrored_complementary_rotated"
    # ROTATED_SWAPPED_COMPLEMENTARY = "rotated_swapped_complementary"
    # MIRRORED_SWAPPED_COMPLEMENTARY = "mirrored_swapped_complementary"
    # MIRRORED_ROTATED_SWAPPED = "mirrored_rotated_swapped"
    # MIRRORED_ROTATED_COMPLEMENTARY_SWAPPED = "mirrored_rotated_complementary_swapped"
    # TIME REVERSAL = "time_reversal"
    
    @staticmethod
    def from_str(s: str):
        _lookup_map = {cap_type.value: cap_type for cap_type in CAPType}
        try:
            return _lookup_map[s]
        except KeyError:
            raise ValueError(f"Invalid CAPType string: {s}")
