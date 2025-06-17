INTEGER_TURNS = [0.0, 1.0, 2.0, 3.0]

BEAT = "beat"
SEQUENCE_START_POSITION = "sequence_start_position"
GRID_MODE = "grid_mode"

DIRECTIONS = {
    "NORTH": "n",
    "EAST": "e",
    "SOUTH": "s",
    "WEST": "w",
    "NORTHEAST": "ne",
    "SOUTHEAST": "se",
    "SOUTHWEST": "sw",
    "NORTHWEST": "nw",
}

MOTION_TYPES = {"SPLIT": "split", "TOG": "tog", "QUARTER": "quarter"}

TIMING_RELATIONS = {"SAME": "same", "OPP": "opp"}

SPLIT_SAME = "SS"
SPLIT_OPP = "SO"
TOG_SAME = "TS"
TOG_OPP = "TO"
QUARTER_SAME = "QS"
QUARTER_OPP = "QO"

ORIENTATIONS = {"VERTICAL": "vertical", "HORIZONTAL": "horizontal"}

ROTATIONS = {"CLOCKWISE": "cw", "COUNTER_CLOCKWISE": "ccw", "NO_ROT": "no_rot"}

POSITIONS = {"LEADING": "leading", "TRAILING": "trailing"}

HANDPATHS = {
    "CW_HANDPATH": "cw_handpath",
    "CCW_HANDPATH": "ccw_handpath",
    "STATIC_HANDPATH": "static_handpath",
    "DASH_HANDPATH": "dash_handpath",
}

OPEN_CLOSE_STATES = {"OPENING": "op", "CLOSING": "cl"}

COLORS = {
    "RED": "red",
    "BLUE": "blue",
    "GOLD": "gold",
    "HEX_RED": "#ED1C24",
    "HEX_BLUE": "#2E3192",
}

MOTION_PROPERTIES = {
    "RADIAL": "radial",
    "NONRADIAL": "nonradial",
    "IN": "in",
    "OUT": "out",
    "CLOCK": "clock",
    "COUNTER": "counter",
}

BASIC_DIRECTIONS = {
    "LEFT": "left",
    "RIGHT": "right",
    "UP": "up",
    "DOWN": "down",
    "UPRIGHT": "upright",
    "UPLEFT": "upleft",
    "DOWNRIGHT": "downright",
    "DOWNLEFT": "downleft",
}

LETTER_TYPES = {
    "LETTER": "letter",
    "PRO": "pro",
    "ANTI": "anti",
    "FLOAT": "float",
    "DASH": "dash",
    "STATIC": "static",
}

PICTOGRAPH_TYPES = {"DIAMOND": "diamond", "BOX": "box", "SKEWED": "skewed"}

BEAT_FRAME_TYPES = {"ALPHA": "alpha", "BETA": "beta", "GAMMA": "gamma"}

PROPS = {
    "STAFF": "staff",
    "BIGSTAFF": "bigstaff",
    "CLUB": "club",
    "BUUGENG": "buugeng",
    "BIGBUUGENG": "bigbuugeng",
    "FRACTALGENG": "fractalgeng",
    "EIGHTRINGS": "eightrings",
    "BIGEIGHTRINGS": "bigeightrings",
    "FAN": "fan",
    "BIGFAN": "bigfan",
    "TRIAD": "triad",
    "BIGTRIAD": "bigtriad",
    "MINIHOOP": "minihoop",
    "BIGHOOP": "bighoop",
    "DOUBLESTAR": "doublestar",
    "BIGDOUBLESTAR": "bigdoublestar",
    "QUIAD": "quiad",
    "SWORD": "sword",
    "GUITAR": "guitar",
    "UKULELE": "ukulele",
    "CHICKEN": "chicken",
    "TRIQUETRA": "triquetra",
    "TRIQUETRA2": "triquetra2",
}

ASSET_DIRECTORIES = {"PROP_DIR": "props/", "ICON_DIR": "icons/"}

DISTANCE = 40
