from typing import Optional

from base_widgets.pictograph.pictograph_scene import PictographScene
from base_widgets.pictograph.pictograph_checker import PictographChecker
from base_widgets.pictograph.pictograph_getter import PictographGetter
from base_widgets.pictograph.pictograph_scene import PictographScene
from base_widgets.pictograph.pictograph_updater import PictographUpdater
from base_widgets.pictograph.wasd_adjustment_manager.wasd_adjustment_manager import (
    WASD_AdjustmentManager,
)
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)


class PictographFactory:
    def __init__(self, special_placement_loader, default_arrow_positions):
        self.special_placement_loader = special_placement_loader
        self.default_arrow_positions = default_arrow_positions

    def create_pictograph(
        self, type_: str = "default", view_class: Optional[type] = None
    ) -> PictographScene:
        scene = PictographScene()
        pictograph = PictographScene(scene, type_)

        # Attach managers
        pictograph.updater = PictographUpdater(pictograph)
        pictograph.getter = PictographGetter(pictograph)
        pictograph.checker = PictographChecker(pictograph)

        # Attach view if provided
        if view_class:
            pictograph.view = view_class(pictograph)

        # Initialize scene managers
        scene.arrow_placement_manager = ArrowPlacementManager(
            scene, self.special_placement_loader, self.default_arrow_positions
        )
        scene.prop_placement_manager = PropPlacementManager(scene)
        scene.wasd_manager = WASD_AdjustmentManager(scene)

        return pictograph
