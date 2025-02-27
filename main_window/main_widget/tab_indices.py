from enum import IntEnum


class LeftStackIndex(IntEnum):
    WORKBENCH = 0
    LEARN_CODEX = 1
    FILTER_SELECTOR = 2
    SEQUENCE_PICKER = 3


class RightStackIndex(IntEnum):
    START_POS_PICKER = 0
    ADVANCED_START_POS_PICKER = 1
    OPTION_PICKER = 2
    GENERATE_TAB = 3
    LEARN_TAB= 4
    SEQUENCE_VIEWER = 5
