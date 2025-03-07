from enum import Enum

class CAPType(Enum):
    STRICT_ROTATED = "strict_rotated"
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_SWAPPED = "strict_swapped"
    STRICT_COMPLEMENTARY = "strict_complementary"
    
    SWAPPED_COMPLIMENTARY = "swapped_complimentary"
    
    ROTATED_COMPLIMENTARY = "rotated_complimentary"
    MIRRORED_COMPLIMENTARY = "mirrored_complimentary"
    
    MIRRORED_SWAPPED = "mirrored_swapped"
    ROTATED_SWAPPED = "rotated_swapped"
    
    MIRRORED_ROTATED = "mirrored_rotated"
    
    MIRRORED_COMPLIMENTARY_ROTATED = "mirrored_complimentary_rotated"
    ROTATED_SWAPPED_COMPLIMENTARY = "rotated_swapped_complimentary"
    MIRRORED_SWAPPED_COMPLIMENTARY = "mirrored_swapped_complimentary"
    MIRRORED_ROTATED_SWAPPED = "mirrored_rotated_swapped"
    MIRRORED_ROTATED_COMPLIMENTARY_SWAPPED = "mirrored_rotated_complimentary_swapped"

    @staticmethod
    def from_str(s: str):
        _lookup_map = {cap_type.value: cap_type for cap_type in CAPType}
        try:
            return _lookup_map[s]
        except KeyError:
            raise ValueError(f"Invalid CAPType string: {s}")
