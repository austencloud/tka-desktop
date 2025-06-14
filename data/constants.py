import os

current_script_path = os.path.abspath(__file__).replace("\\", "/")
current_script_path = current_script_path[0].upper() + current_script_path[1:]

current_dir = os.path.dirname(current_script_path)
tka_sequence_constructor_dir = os.path.dirname(current_dir)
tka_app_dir = os.path.dirname(tka_sequence_constructor_dir)

special_placements_parent_directory = os.path.join("")

INTEGER_TURNS = [0.0, 1.0, 2.0, 3.0]

BEAT = "beat"
SEQUENCE_START_POSITION = "sequence_start_position"

GRID_MODE = "grid_mode"

NORTH = "n"
EAST = "e"
SOUTH = "s"
WEST = "w"
NORTHEAST = "ne"
SOUTHEAST = "se"
SOUTHWEST = "sw"
NORTHWEST = "nw"

SPLIT = "split"
TOG = "tog"
QUARTER = "quarter"

SAME = "same"
OPP = "opp"

TIMING = "timing"
DIRECTION = "direction"

SPLIT_SAME = "SS"
SPLIT_OPP = "SO"
TOG_SAME = "TS"
TOG_OPP = "TO"
QUARTER_SAME = "QS"
QUARTER_OPP = "QO"

VERTICAL = "vertical"
HORIZONTAL = "horizontal"

CLOCKWISE = "cw"
COUNTER_CLOCKWISE = "ccw"
NO_ROT = "no_rot"

LEADING = "leading"
TRAILING = "trailing"

CW_HANDPATH = "cw_handpath"
CCW_HANDPATH = "ccw_handpath"


# Vtg Directions
SAME = "same"
OPP = "opp"

# Vtg Timings
SPLIT = "split"
TOG = "tog"

# Open Close States
OPENING = "op"
CLOSING = "cl"


START_POS = "start_pos"
END_POS = "end_pos"

BLUE_MOTION_TYPE = "blue_motion_type"
BLUE_PROP_ROT_DIR = "blue_prop_rot_dir"
BLUE_START_LOC = "blue_start_loc"
BLUE_END_LOC = "blue_end_loc"
BLUE_START_ORI = "blue_start_ori"
BLUE_END_ORI = "blue_end_ori"
BLUE_TURNS = "blue_turns"

RED_MOTION_TYPE = "red_motion_type"
RED_PROP_ROT_DIR = "red_prop_rot_dir"
RED_START_LOC = "red_start_loc"
RED_END_LOC = "red_end_loc"
RED_START_ORI = "red_start_ori"
RED_END_ORI = "red_end_ori"
RED_TURNS = "red_turns"

RED = "red"
BLUE = "blue"
GOLD = "gold"

HEX_RED = "#ED1C24"
HEX_BLUE = "#2E3192"

RADIAL = "radial"
NONRADIAL = "nonradial"

IN = "in"
OUT = "out"
CLOCK = "clock"
COUNTER = "counter"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

UPRIGHT = "upright"
UPLEFT = "upleft"
DOWNRIGHT = "downright"
DOWNLEFT = "downleft"

LETTER = "letter"
PRO = "pro"
ANTI = "anti"
FLOAT = "float"
DASH = "dash"
STATIC = "static"
LETTER_TYPE = "letter_type"
DURATION = "duration"

VTG_DIR = "vtg_dir"
VTG_TIMING = "vtg_timing"

LEAD_STATE = "lead_state"
COLOR = "color"
ARROW = "arrow"
PROP = "prop"
LETTER_ITEM = "letter_item"
LOC = "loc"
MOTION_TYPE = "motion_type"
TURNS = "turns"
PROP_TYPE = "prop_type"
PROP_LOC = "prop_loc"
PROP_ORI = "prop_ori"
PROP_ROT_DIR = "prop_rot_dir"
ORI = "ori"
START_ORI = "start_ori"
END_ORI = "end_ori"
AXIS = "axis"
START_LOC = "start_loc"
END_LOC = "end_loc"
LAYER = "layer"
MOTION = "motion"
PRO_TURNS = "pro_turns"
ANTI_TURNS = "anti_turns"

PREFLOAT_MOTION_TYPE = "prefloat_motion_type"
PREFLOAT_PROP_ROT_DIR = "prefloat_prop_rot_dir"

BLUE_ATTRS = "blue_attributes"
RED_ATTRS = "red_attributes"

STATIC_HANDPATH = "static_handpath"
DASH_HANDPATH = "dash_handpath"


PROP_DIR = "props/"
ICON_DIR = "icons/"


STAFF = "staff"
BIGSTAFF = "bigstaff"
CLUB = "club"
BUUGENG = "buugeng"
BIGBUUGENG = "bigbuugeng"
FRACTALGENG = "fractalgeng"
EIGHTRINGS = "eightrings"
BIGEIGHTRINGS = "bigeightrings"
FAN = "fan"
BIGFAN = "bigfan"
TRIAD = "triad"
BIGTRIAD = "bigtriad"
MINIHOOP = "minihoop"
BIGHOOP = "bighoop"
DOUBLESTAR = "doublestar"
BIGDOUBLESTAR = "bigdoublestar"
QUIAD = "quiad"
SWORD = "sword"
GUITAR = "guitar"
UKULELE = "ukulele"
CHICKEN = "chicken"
TRIQUETRA = "triquetra"
TRIQUETRA2 = "triquetra2"

DIAMOND = "diamond"
BOX = "box"
SKEWED = "skewed"
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"

ALPHA1 = "alpha1"
ALPHA2 = "alpha2"
ALPHA3 = "alpha3"
ALPHA4 = "alpha4"
ALPHA5 = "alpha5"
ALPHA6 = "alpha6"
ALPHA7 = "alpha7"
ALPHA8 = "alpha8"

BETA1 = "beta1"
BETA2 = "beta2"
BETA3 = "beta3"
BETA4 = "beta4"
BETA5 = "beta5"
BETA6 = "beta6"
BETA7 = "beta7"
BETA8 = "beta8"

GAMMA1 = "gamma1"
GAMMA2 = "gamma2"
GAMMA3 = "gamma3"
GAMMA4 = "gamma4"
GAMMA5 = "gamma5"
GAMMA6 = "gamma6"
GAMMA7 = "gamma7"
GAMMA8 = "gamma8"
GAMMA9 = "gamma9"
GAMMA10 = "gamma10"
GAMMA11 = "gamma11"
GAMMA12 = "gamma12"
GAMMA13 = "gamma13"
GAMMA14 = "gamma14"
GAMMA15 = "gamma15"
GAMMA16 = "gamma16"

### ICONS ###


DISTANCE = 40
