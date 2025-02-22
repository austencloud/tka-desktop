from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsTextItem


from base_widgets.pictograph.bordered_pictograph_view import BorderedPictographView
from main_window.main_widget.construct_tab.option_picker.option_view import OptionView
from main_window.main_widget.construct_tab.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)
from main_window.main_widget.learn_tab.lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)
from main_window.main_widget.codex.codex_pictograph_view import (
    CodexPictographView,
)
from objects.arrow.arrow import Arrow
from .grid.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from .glyphs.reversal_glyph import ReversalGlyph
from .glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
from .glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import StartToEndPosGlyph
from .glyphs.tka_glyph.tka_glyph import TKA_Glyph
from .glyphs.vtg_glyph.vtg_glyph import VTG_Glyph
from .pictograph_view import PictographView


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.graph_editor.GE_pictograph_view import (
        GE_PictographView,
    )


from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class PictographElements:
    """Stores all elements within the pictograph."""

    view: Union[
        PictographView,
        BorderedPictographView,
        LessonPictographView,
        StartPosPickerPictographView,
        CodexPictographView,
        "GE_PictographView",
        "OptionView",
    ] = None

    arrows: dict[str, Arrow] = None
    motions: dict[str, Motion] = None
    props: dict[str, Prop] = None
    motion_dict_list: list = None
    pictograph_dict: dict[str, Union[str, dict[str, str]]] = None
    locations: dict[str, tuple[int, int, int, int]] = None
    grid: Optional[Grid] = None

    # Symbols
    blue_reversal_symbol: Optional[QGraphicsTextItem] = None
    red_reversal_symbol: Optional[QGraphicsTextItem] = None

    # Items
    selected_arrow: Optional[Arrow] = None
    blue_arrow: Optional[Arrow] = None
    red_arrow: Optional[Arrow] = None
    blue_motion: Optional[Motion] = None
    red_motion: Optional[Motion] = None
    blue_prop: Optional[Prop] = None
    red_prop: Optional[Prop] = None

    tka_glyph: Optional[TKA_Glyph] = None
    vtg_glyph: Optional[VTG_Glyph] = None
    elemental_glyph: Optional[ElementalGlyph] = None
    start_to_end_pos_glyph: Optional[StartToEndPosGlyph] = None
    reversal_glyph: Optional[ReversalGlyph] = None
