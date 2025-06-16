from typing import TypedDict
from enum import Enum
from typing import TYPE_CHECKING, Union
from enums.letter.letter import Letter

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsTextItem


if TYPE_CHECKING:
    from objects.glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
    from objects.glyphs.reversal_glyph import ReversalGlyph
    from objects.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
        StartToEndPosGlyph,
    )
    from objects.glyphs.tka_glyph.tka_glyph import TKA_Glyph
    from objects.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph

    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop

from PyQt6.QtSvgWidgets import QGraphicsSvgItem


Glyph = Union[
    QGraphicsTextItem,
    QGraphicsSvgItem,
    "ReversalGlyph",
    "ElementalGlyph",
    "StartToEndPosGlyph",
    "TKA_Glyph",
    "VTG_Glyph",
    "Prop",
    "Arrow",
]
