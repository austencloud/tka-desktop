# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/types.py
from typing import TypedDict
from enums.letter.letter import Letter


# types.py
from typing import NotRequired


class PlacementDataEntry(TypedDict):
    turns_tuple: dict[str, dict[str, bool]]


class OrientationData(TypedDict):
    letters: dict[str, PlacementDataEntry]


class GridModeData(TypedDict):
    orientations: dict[str, OrientationData]


class PlacementData(TypedDict):
    grid_modes: dict[str, GridModeData]


class OverrideData(TypedDict):
    letter: Letter
    ori_key: str
    turns_tuple: str
    rot_angle_key: str
    placement_data: PlacementData
    validation_hash: NotRequired[str]  # Example of optional field
