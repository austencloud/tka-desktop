from typing import TYPE_CHECKING


from base_widgets.pictograph.managers.pictograph_data_copier import dictCopier
from objects.glyphs.reversal_glyph import ReversalGlyph
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from svg_manager.svg_manager import SvgManager
from .pictograph_checker import PictographChecker
from .getter.pictograph_getter import PictographGetter
from .updater.pictograph_updater import PictographUpdater
from .pictograph_initializer import PictographInitializer

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

from PyQt6.QtWidgets import QGraphicsScene
from dataclasses import dataclass


@dataclass
class PictographManagers:
    """Stores all manager objects to handle logic separately."""

    arrow_placement_manager: "ArrowPlacementManager" = None
    prop_placement_manager: "PropPlacementManager" = None
    check: "PictographChecker" = None
    get: "PictographGetter" = None
    initializer: "PictographInitializer" = None
    updater: "PictographUpdater" = None
    svg_manager: "SvgManager" = None
    data_copier: "dictCopier" = None
