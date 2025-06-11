from enum import Enum


class TabName(str, Enum):
    CONSTRUCT = "construct"
    GENERATE = "generate"
    BROWSE = "browse"
    LEARN = "learn"
    WRITE = "write"
    SEQUENCE_CARD = "sequence_card"

    @classmethod
    def from_string(cls, value: str) -> "TabName":
        try:
            return cls(value)
        except ValueError:
            return cls.CONSTRUCT
