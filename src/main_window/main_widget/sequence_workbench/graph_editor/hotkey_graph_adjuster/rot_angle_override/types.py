# src/main_window/main_widget/sequence_workbench/graph_editor/hotkey_graph_adjuster/rot_angle_override/types.py
from typing import TypedDict, NewType
from enums.letter.letter import Letter

# Type-safe string aliases
OriKey = NewType("OriKey", str)
RotationKey = NewType("RotationKey", str)
GridMode = NewType("GridMode", str)
TurnsTuple = NewType("TurnsTuple", str)


class OverrideData(TypedDict):
    letter: Letter
    ori_key: OriKey
    turns_tuple: TurnsTuple
    rot_angle_key: RotationKey
    placement_data: dict[
        GridMode, dict[OriKey, dict[str, dict[TurnsTuple, dict[RotationKey, bool]]]]
    ]
