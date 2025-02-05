from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from Enums.Enums import Letter, OpenCloseStates, VTG_Modes
from Enums.PropTypes import PropType
from Enums.letters import LetterType
from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView
from base_widgets.base_pictograph.svg_manager import SvgManager
from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

from main_window.main_widget.learn_tab.codex.codex_pictograph_view import (
    CodexPictographView,
)
from main_window.main_widget.construct_tab.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)

from objects.arrow.arrow import Arrow
from base_widgets.base_pictograph.grid.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from .glyphs.beat_reversal_group import BeatReversalGroup
from .glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
from .glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import StartToEndPosGlyph
from .glyphs.tka.tka_glyph import TKA_Glyph
from .glyphs.vtg.vtg_glyph import VTG_Glyph
from .pictograph_data_updater import PictographDataUpdater
from .pictograph_checker import PictographChecker
from .pictograph_getter import PictographGetter
from .pictograph_view import PictographView
from .wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager
from .pictograph_updater import PictographUpdater
from .pictograph_initializer import PictographInitializer


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph_view import (
        GE_PictographView,
    )
    from main_window.main_widget.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    # dicts
    arrows: dict[str, Arrow]
    locations: dict[str, tuple[int, int, int, int]]
    motions: dict[str, Motion]
    motion_data_list: list[dict]
    pictograph_data: dict[str, Union[str, dict[str, str]]] = {}
    props: dict[str, Prop]

    # managers
    attr_manager: PictographDataUpdater
    arrow_placement_manager: ArrowPlacementManager
    prop_placement_manager: PropPlacementManager
    reversal_glyph: BeatReversalGroup
    wasd_manager: WASD_AdjustmentManager

    # bool
    blue_reversal = False
    disable_gold_overlay: bool = False
    image_loaded: bool
    is_blank: bool = False
    quiz_mode: bool = False
    red_reversal = False

    # str
    direction: str
    end_pos: str
    start_pos: str
    timing: str
    turns_tuple: str = None
    grid_mode: str

    # enums
    letter: Letter = None
    letter_type: LetterType = None
    open_close_state: OpenCloseStates
    prop_type: PropType = None
    vtg_mode: VTG_Modes = None

    # items
    blue_arrow: Arrow
    blue_motion: Motion
    blue_prop: Prop
    dragged_arrow: Arrow
    dragged_prop: Prop
    red_arrow: Arrow
    red_motion: Motion
    red_prop: Prop
    selected_arrow: Arrow = None
    grid: Grid

    # symbols
    blue_reversal_symbol: "QGraphicsTextItem" = None
    red_reversal_symbol: "QGraphicsTextItem" = None

    # glyphs
    elemental_glyph: ElementalGlyph
    start_to_end_pos_glyph: StartToEndPosGlyph
    tka_glyph: TKA_Glyph
    vtg_glyph: VTG_Glyph

    # components
    check: PictographChecker
    get: PictographGetter
    initializer: PictographInitializer
    updater: PictographUpdater

    # others
    main_widget: "MainWidget"
    pixmap: QGraphicsPixmapItem
    view: Union[
        PictographView,
        BorderedPictographView,
        LessonPictographView,
        StartPosPickerPictographView,
        CodexPictographView,
        "GE_PictographView",
    ]

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.initializer = PictographInitializer(self)
        self.updater = PictographUpdater(self)
        self.get = PictographGetter(self)
        self.check = PictographChecker(self)
        self.initializer.init_all_components()
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.wasd_manager = WASD_AdjustmentManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.attr_manager = PictographDataUpdater(self)
        self.reversal_glyph = BeatReversalGroup(self)
        self.svg_manager = SvgManager(self)
