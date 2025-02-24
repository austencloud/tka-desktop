from PyQt6.QtWidgets import QGraphicsScene

from svg_manager.svg_manager import SvgManager
from .pictograph_elements import PictographElements
from .pictograph_managers import PictographManagers
from .pictograph_state import PictographState
from .glyphs.reversal_glyph import ReversalGlyph
from .pictograph_checker import PictographChecker
from .pictograph_getter import PictographGetter
from .pictograph_updater.pictograph_updater import PictographUpdater
from .pictograph_initializer import PictographInitializer
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)


class Pictograph(QGraphicsScene):
    def __init__(self) -> None:
        super().__init__()

        self.state = PictographState()
        self.elements = PictographElements()
        self.managers = PictographManagers()

        self.managers.initializer = PictographInitializer(self)
        self.managers.updater = PictographUpdater(self)
        self.managers.get = PictographGetter(self)
        self.managers.check = PictographChecker(self)
        self.managers.svg_manager = SvgManager(self)
        self.managers.arrow_placement_manager = ArrowPlacementManager(self)
        self.managers.prop_placement_manager = PropPlacementManager(self)
        self.managers.reversal_glyph = ReversalGlyph(self)
