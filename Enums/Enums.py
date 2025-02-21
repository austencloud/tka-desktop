from typing import TypedDict
from enum import Enum
from Enums.letters import *
from typing import TYPE_CHECKING, Union
from Enums.letters import Letter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsTextItem

if TYPE_CHECKING:
    from base_widgets.pictograph.glyphs.elemental_glyph.elemental_glyph import (
        ElementalGlyph,
    )
    from base_widgets.pictograph.glyphs.reversal_glyph import (
        ReversalGlyph,
    )
    from base_widgets.pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
        StartToEndPosGlyph,
    )
    from base_widgets.pictograph.glyphs.tka_glyph.tka_glyph import TKA_Glyph
    from base_widgets.pictograph.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph
    from base_widgets.pictograph.pictograph_scene import PictographScene
    from main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


Glyph = Union[
    QGraphicsTextItem,
    QGraphicsSvgItem,
    "ReversalGlyph",
    "ElementalGlyph",
    "StartToEndPosGlyph",
    "TKA_Glyph",
    "VTG_Glyph",
]


class Turns(Enum):
    ZERO = 0
    ZERO_POINT_FIVE = 0.5
    ONE = 1
    ONE_POINT_FIVE = 1.5
    TWO = 2
    TWO_POINT_FIVE = 2.5
    THREE = 3


class MotionCombinationType(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class ArrowAttribute(Enum):
    COLOR = "color"
    LOC = "loc"
    MOTION_TYPE = "motion_type"
    TURNS = "turns"


class PropAttribute(Enum):
    COLOR = "color"
    PROP_TYPE = "prop_type"
    LOC = "loc"
    ORI = "ori"


class MotionAttribute(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    PROP_ROT_DIR = "prop_rot_dir"
    TURNS = "turns"
    START_LOC = "start_loc"
    START_ORI = "start_ori"
    END_LOC = "end_loc"
    END_ORI = "end_ori"


class OrientationCombination(Enum):
    IN_VS_IN = "in_vs_in"
    IN_VS_CLOCK_IN = "in_vs_clock-in"
    IN_VS_CLOCK = "in_vs_clock"
    IN_VS_CLOCK_OUT = "in_vs_clock-out"
    IN_VS_OUT = "in_vs_out"
    IN_VS_COUNTER_OUT = "in_vs_counter-out"
    IN_VS_COUNTER = "in_vs_counter"
    IN_VS_COUNTER_IN = "in_vs_counter-in"
    CLOCK_IN_VS_CLOCK_IN = "clock-in_vs_clock-in"
    CLOCK_IN_VS_CLOCK = "clock-in_vs_clock"
    CLOCK_IN_VS_CLOCK_OUT = "clock-in_vs_clock-out"
    CLOCK_IN_VS_OUT = "clock-in_vs_out"
    CLOCK_IN_VS_COUNTER_OUT = "clock-in_vs_counter-out"
    CLOCK_IN_VS_COUNTER = "clock-in_vs_counter"
    CLOCK_IN_VS_COUNTER_IN = "clock-in_vs_counter-in"
    CLOCK_VS_CLOCK = "clock_vs_clock"
    CLOCK_VS_CLOCK_OUT = "clock_vs_clock-out"
    CLOCK_VS_OUT = "clock_vs_out"
    CLOCK_VS_COUNTER_OUT = "clock_vs_counter-out"
    CLOCK_VS_COUNTER = "clock_vs_counter"
    CLOCK_VS_COUNTER_IN = "clock_vs_counter-in"
    CLOCK_OUT_VS_CLOCK_OUT = "clock-out_vs_clock-out"
    CLOCK_OUT_VS_OUT = "clock-out_vs_out"
    CLOCK_OUT_VS_COUNTER_OUT = "clock-out_vs_counter-out"
    CLOCK_OUT_VS_COUNTER = "clock-out_vs_counter"
    CLOCK_OUT_VS_COUNTER_IN = "clock-out_vs_counter-in"
    OUT_VS_OUT = "out_vs_out"
    OUT_VS_COUNTER_OUT = "out_vs_counter-out"
    OUT_VS_COUNTER = "out_vs_counter"
    OUT_VS_COUNTER_IN = "out_vs_counter-in"
    COUNTER_OUT_VS_COUNTER_OUT = "counter-out_vs_counter-out"
    COUNTER_OUT_VS_COUNTER = "counter-out_vs_counter"
    COUNTER_OUT_VS_COUNTER_IN = "counter-out_vs_counter-in"
    COUNTER_VS_COUNTER = "counter_vs_counter"
    COUNTER_VS_COUNTER_IN = "counter_vs_counter-in"
    COUNTER_IN_VS_COUNTER_IN = "counter-in_vs_counter-in"


### LETTER GROUPS ###
class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class MotionTypeLetterGroups(Enum):
    PRO_VS_PRO = "ADGJMPS"
    ANTI_VS_ANTI = "BEHKNQT"
    STATIC_VS_STATIC = "αβΓ"
    PRO_VS_ANTI = "CFILORUV"
    STATIC_VS_PRO = "WYΣθ"
    STATIC_VS_ANTI = "XZΔΩ"
    DASH_VS_PRO = "W-Y-Σ-θ-"
    DASH_VS_ANTI = "X-Z-Δ-Ω-"
    DASH_VS_STATIC = "ΦΨΛ"
    DASH_VS_DASH = "Φ-Ψ-Λ-"


class VTG_Modes(Enum):
    TOG_SAME = "TS"
    TOG_OPP = "TO"
    SPLIT_SAME = "SS"
    SPLIT_OPP = "SO"
    QUARTER_SAME = "QTS"
    QUARTER_OPP = "QTO"


class TKAHandpathMode(Enum):
    ALPHA_TO_ALPHA = "α→α"  # ABC
    BETA_TO_ALPHA = "β→α"  # DEF
    BETA_TO_BETA = "β→β"  # GHI
    ALPHA_TO_BETA = "α→β"  # JKL
    GAMMA_TO_GAMMA_OPP_ANTIPARALLEL = "Γ→Γ_opp_antiparallel"  # MNO
    GAMMA_TO_GAMMA_OPP_PARALLEL = "Γ→Γ_opp_parallel"  # PQR
    GAMMA_TO_GAMMA_SAME_DIR = "Γ→Γ_same"  # STUV

    GAMMACLOCK_TO_GAMMACLOCK = "Γclock→Γclock"
    GAMMACLOCK_TO_GAMMACOUNTER = "Γclock→Γcounter"
    GAMMACOUNTER_TO_GAMMACOUNTER = "Γcounter→Γcounter"
    GAMMACOUNTER_TO_GAMMACLOCK = "Γcounter→Γclock"


class PictographType(Enum):
    MAIN = "main"
    OPTION = "option"
    BEAT = "beat"
    START_POS = "start_pos"
    CODEX_PICTOGRAPH = "letterbook_pictograph"


class MotionTypeCombination(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class LetterGroupsByMotionType(Enum):
    ADGJMPS = "ADGJMPS"
    BEHKNQT = "BEHKNQT"
    αβΓ = "αβΓ"
    CFILORUV = "CFILORUV"
    WYΣθ = "WYΣθ"
    XZΔΩ = "XZΔΩ"
    X_Z_Δ_Ω_ = "X-Z-Δ-Ω-"
    ΦΨΛ = "ΦΨΛ"
    Φ_Ψ_Λ_ = "Φ-Ψ-Λ-"


class TurnsTabAttribute(Enum):
    MOTION_TYPE = "motion_type"
    COLOR = "color"
    LEAD_STATE = "lead_state"


class ParallelCombinationsSet(Enum):
    SET = "set"


class Handpaths(Enum):
    DASH_HANDPATH = "dash_handpath"
    STATIC_HANDPATH = "static_handpath"
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class RotationAngles(Enum):
    ANGLE_0 = 0
    ANGLE_90 = 90
    ANGLE_180 = 180
    ANGLE_270 = 270


class OptimalLocationEntries(Enum):
    X = "x"
    Y = "y"


class StartEndLocationTuple(Enum):
    LOCATIONS = "Locations"


class OptimalLocationDicts(Enum):
    DICT = "dict"


class Positions(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


class SpecificPosition(Enum):
    ALPHA1 = "alpha1"
    ALPHA2 = "alpha3"
    ALPHA3 = "alpha5"
    ALPHA7 = "alpha7"
    BETA1 = "beta1"
    BETA3 = "beta3"
    BETA5 = "beta5"
    BETA7 = "beta7"
    GAMMA1 = "gamma1"
    GAMMA3 = "gamma3"
    GAMMA5 = "gamma5"
    GAMMA7 = "gamma7"
    GAMMA9 = "gamma9"
    GAMMA11 = "gamma11"
    GAMMA13 = "gamma13"
    GAMMA15 = "gamma15"


class ShiftHandpaths(Enum):
    CW_HANDPATH = "cw_handpath"
    CCW_HANDPATH = "ccw_handpath"


class HexColors(Enum):
    COLOR_1 = "#ED1C24"
    COLOR_2 = "#2E3192"


class GridModes(Enum):
    DIAMOND = "diamond"
    BOX = "box"


class RadialOrientations(Enum):
    IN = "in"
    OUT = "out"


class NonRadialOrientations(Enum):
    CLOCK = "clock"
    COUNTER = "counter"


class OrientationTypes(Enum):
    RADIAL = "radial"
    NONRADIAL = "nonradial"


class Axes(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class MotionTypeCombinations(Enum):
    PRO_VS_PRO = "pro_vs_pro"
    ANTI_VS_ANTI = "anti_vs_anti"
    STATIC_VS_STATIC = "static_vs_static"
    PRO_VS_ANTI = "pro_vs_anti"
    STATIC_VS_PRO = "static_vs_pro"
    STATIC_VS_ANTI = "static_vs_anti"
    DASH_VS_PRO = "dash_vs_pro"
    DASH_VS_ANTI = "dash_vs_anti"
    DASH_VS_STATIC = "dash_vs_static"
    DASH_VS_DASH = "dash_vs_dash"


class VTG_Timings(Enum):
    SPLIT = "split"
    TOGETHER = "together"


class str(Enum):
    SAME = "same"
    OPP = "opp"


class OpenCloseStates(Enum):
    OPEN = "open"
    CLOSE = "close"


class AdjustmentStrs(Enum):
    MINUS_1 = "-1"
    MINUS_0_5 = "-0.5"
    PLUS_1 = "+1"
    PLUS_0_5 = "+0.5"


class AdjustmentNums(Enum):
    FLOAT = float
    INT = int


class LetterTypeDescriptions(Enum):
    DUAL_SHIFT = "Dual-Shift"
    SHIFT = "Shift"
    CROSS_SHIFT = "Cross-Shift"
    DASH = "Dash"
    DUAL_DASH = "Dual-Dash"
    STATIC = "Static"


class MotionAttributes(Enum):
    COLOR = "color"
    ARROW = "arrow"
    PROP = "prop"
    MOTION_TYPE = "motion_type"
    PROP_ROT_DIR = "prop_rot_dir"
    TURNS = "turns"
    START_LOC = "start_loc"
    START_ORI = "start_ori"
    END_LOC = "end_loc"
    END_ORI = "end_ori"
    LEAD_STATE = "lead_state"


class Pictograph_Key(Enum):
    KEY = str


class PictographAttributesDict(TypedDict):
    letter: Letter
    start_pos: str
    end_pos: str
    blue_motion_type: str
    blue_prop_rot_dir: str
    blue_start_loc: str
    blue_end_loc: str
    blue_turns: Turns
    blue_start_ori: str
    blue_end_ori: str
    red_motion_type: str
    red_prop_rot_dir: str
    red_start_loc: str
    red_end_loc: str
    red_turns: Turns
    red_start_ori: str
    red_end_ori: str
