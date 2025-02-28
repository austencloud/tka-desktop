from PyQt6.QtWidgets import QGraphicsScene

from base_widgets.pictograph.elements.pictograph_elements import PictographElements
from base_widgets.pictograph.managers.getter.pictograph_getter import PictographGetter
from base_widgets.pictograph.managers.pictograph_checker import PictographChecker
from base_widgets.pictograph.managers.pictograph_data_copier import PictographDataCopier
from base_widgets.pictograph.managers.pictograph_initializer import (
    PictographInitializer,
)
from base_widgets.pictograph.managers.pictograph_managers import PictographManagers
from base_widgets.pictograph.managers.updater.pictograph_updater import (
    PictographUpdater,
)
from base_widgets.pictograph.state.pictograph_state import PictographState
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from svg_manager.svg_manager import SvgManager


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
        self.managers.data_copier = PictographDataCopier(self)
