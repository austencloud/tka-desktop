from data.constants import *


start_end_loc_map = {
    NORTHEAST: {
        CLOCKWISE: {
            ANTI: (EAST, NORTH),
            PRO: (NORTH, EAST),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (NORTH, EAST),
            PRO: (EAST, NORTH),
        },
    },
    NORTHWEST: {
        CLOCKWISE: {
            ANTI: (NORTH, WEST),
            PRO: (WEST, NORTH),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (WEST, NORTH),
            PRO: (NORTH, WEST),
        },
    },
    SOUTHEAST: {
        CLOCKWISE: {
            ANTI: (SOUTH, EAST),
            PRO: (EAST, SOUTH),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (EAST, SOUTH),
            PRO: (SOUTH, EAST),
        },
    },
    SOUTHWEST: {
        CLOCKWISE: {
            ANTI: (WEST, SOUTH),
            PRO: (SOUTH, WEST),
        },
        COUNTER_CLOCKWISE: {
            ANTI: (SOUTH, WEST),
            PRO: (WEST, SOUTH),
        },
    },
}


def get_start_end_locs(
    motion_type: str, rot_dir: str, arrow_location: str
) -> tuple[str, str]:
    return (
        start_end_loc_map.get(arrow_location, {})
        .get(rot_dir, {})
        .get(motion_type, (None, None))
    )
