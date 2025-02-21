from typing import TYPE_CHECKING
from base_widgets.pictograph.pictograph_attr_manager import PictographAttrManager
from .svg_manager import SvgManager
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from .glyphs.reversal_glyph import ReversalGlyph
from .pictograph_checker import PictographChecker
from .pictograph_getter import PictographGetter
from .wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager
from .pictograph_updater.pictograph_updater import PictographUpdater
from .pictograph_initializer import PictographInitializer


if TYPE_CHECKING:
    pass

from dataclasses import dataclass


@dataclass
class PictographManagers:
    """Stores all manager objects to handle logic separately."""

    attr_manager: PictographAttrManager = None
    arrow_placement_manager: ArrowPlacementManager = None
    prop_placement_manager: PropPlacementManager = None
    wasd_manager: WASD_AdjustmentManager = None
    reversal_glyph: ReversalGlyph = None
    check: PictographChecker = None
    get: PictographGetter = None
    initializer: PictographInitializer = None
    updater: PictographUpdater = None
    svg_manager: SvgManager = None
