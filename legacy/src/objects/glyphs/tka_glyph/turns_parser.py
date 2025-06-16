from typing import Tuple, Union
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME


def parse_turns_tuple_string(
    turns_str: str,
) -> Tuple[Union[str, None], Union[int, float, str], Union[int, float, str]]:
    """Parses a turns tuple string and returns a tuple of direction, top turn, and bottom turn."""
    parts = turns_str.strip("()").split(",")
    turns_list = [
        (
            float(item)
            if item in ["0.5", "1.5", "2.5"]
            else (
                int(item)
                if item in ["0", "1", "2", "3"]
                else (
                    SAME
                    if item == "s"
                    else OPP if item == "o" else "fl" if item == "fl" else item.strip()
                )
            )
        )
        for item in parts
    ]
    if len(turns_list) >= 3 and turns_list[0] in [
        SAME,
        OPP,
        CLOCKWISE,
        COUNTER_CLOCKWISE,
    ]:
        return turns_list[0], turns_list[1], turns_list[2]
    else:
        return None, turns_list[0], turns_list[1]
