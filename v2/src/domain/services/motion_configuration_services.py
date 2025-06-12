from typing import Dict, Any, List
from ...infrastructure.config.constants import MOTION_TYPES, DIRECTIONS, PROPS


class VtgConfigurationService:
    def __init__(self):
        self.vtg_combinations = self._generate_vtg_combinations()

    def _generate_vtg_combinations(self) -> Dict[str, Any]:
        return {
            "split_same": {"timing": "split", "direction": "same"},
            "split_opp": {"timing": "split", "direction": "opp"},
            "tog_same": {"timing": "tog", "direction": "same"},
            "tog_opp": {"timing": "tog", "direction": "opp"},
        }

    def get_vtg_data(self, vtg_type: str) -> Dict[str, Any]:
        return self.vtg_combinations.get(vtg_type, {})


class PositionMappingService:
    def __init__(self):
        self.position_maps = self._initialize_position_maps()

    def _initialize_position_maps(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        return {
            "start_end_loc_map": {
                "alpha1": {"start": "ne", "end": "sw"},
                "alpha2": {"start": "se", "end": "nw"},
                "beta1": {"start": "n", "end": "s"},
                "beta2": {"start": "e", "end": "w"},
            }
        }

    def get_position_mapping(self, mapping_type: str) -> Dict[str, Dict[str, str]]:
        return self.position_maps.get(mapping_type, {})


class PropClassMappingService:
    def __init__(self):
        self.prop_mappings = self._initialize_prop_mappings()

    def _initialize_prop_mappings(self) -> Dict[str, str]:
        return {prop: f"{prop}_class" for prop in PROPS.values()}

    def get_prop_class(self, prop_type: str) -> str:
        return self.prop_mappings.get(prop_type, "default_class")
