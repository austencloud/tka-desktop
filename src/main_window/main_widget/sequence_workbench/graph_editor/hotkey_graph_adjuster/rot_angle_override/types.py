# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/types.py
from typing import TypeGuard, TypedDict, NewType
from data.constants import BOX, DIAMOND, SKEWED
from enums.letter.letter import Letter

# Type-safe string aliases
OriKey = NewType("OriKey", str)
RotationKey = NewType("RotationKey", str)
GridMode = NewType("GridMode", str)
TurnsTuple = NewType("TurnsTuple", str)


# types.py
from typing import NotRequired


class PlacementDataEntry(TypedDict):
    turns_tuple: dict[TurnsTuple, dict[RotationKey, bool]]


class OrientationData(TypedDict):
    letters: dict[str, PlacementDataEntry]


class GridModeData(TypedDict):
    orientations: dict[OriKey, OrientationData]


class PlacementData(TypedDict):
    grid_modes: dict[GridMode, GridModeData]


class OverrideData(TypedDict):
    letter: Letter
    ori_key: OriKey
    turns_tuple: TurnsTuple
    rot_angle_key: RotationKey
    placement_data: PlacementData
    validation_hash: NotRequired[str]  # Example of optional field


# types.py


def is_valid_grid_mode(value: str) -> TypeGuard[GridMode]:
    return value in [DIAMOND, BOX, SKEWED]


def is_valid_ori_key(value: str) -> TypeGuard[OriKey]:
    return value.startswith("from_layer")  # Match your key patterns
