from PyQt6.QtWidgets import QGraphicsScene

from .elements.pictograph_elements import PictographElements
from .managers.getter.pictograph_getter import PictographGetter
from .managers.pictograph_checker import PictographChecker
from .managers.pictograph_data_copier import dictCopier
from .managers.pictograph_initializer import PictographInitializer
from .managers.pictograph_managers import PictographManagers
from .managers.updater.pictograph_updater import PictographUpdater
from .state.pictograph_state import PictographState
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from svg_manager.svg_manager import SvgManager


from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)


class LegacyPictograph(QGraphicsScene):
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
        self.managers.data_copier = dictCopier(self)
