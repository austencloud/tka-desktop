from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsTextItem


from base_widgets.pictograph.elements.grid.grid import Grid
from base_widgets.pictograph.elements.views.bordered_pictograph_view import (
    BorderedPictographView,
)
from base_widgets.pictograph.elements.views.option_view import OptionView
from base_widgets.pictograph.elements.views.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)
from base_widgets.pictograph.elements.views.lesson_pictograph_view import (
    LessonPictographView,
)
from base_widgets.pictograph.elements.views.codex_pictograph_view import (
    CodexPictographView,
)

from objects.arrow.arrow import Arrow
from objects.glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
from objects.glyphs.reversal_glyph import ReversalGlyph
from objects.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from objects.glyphs.tka_glyph.tka_glyph import TKA_Glyph
from objects.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph
from objects.motion.motion import Motion
from objects.prop.prop import Prop

from .views.base_pictograph_view import BasePictographView


if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
        VisibilityPictographView,
    )

    from base_widgets.pictograph.elements.views.GE_pictograph_view import (
        GE_PictographView,
    )


from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class PictographElements:
    """Stores all elements within the pictograph."""

    view: Union[
        BasePictographView,
        BorderedPictographView,
        LessonPictographView,
        StartPosPickerPictographView,
        CodexPictographView,
        "GE_PictographView",
        "OptionView",
        "VisibilityPictographView",
    ] = None

    arrows: dict[str, Arrow] = None
    motion_set: dict[str, Motion] = None
    props: dict[str, Prop] = None
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
