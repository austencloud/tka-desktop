from email.policy import default
from typing import TYPE_CHECKING

from base_widgets.pictograph.hotkey_graph_adjuster.special_placement_data_updater.special_placement_data_updater import (
    SpecialPlacementDataUpdater,
)
from placement_managers.arrow_placement_manager.arrow_placement_context import (
    ArrowPlacementContext,
)

from placement_managers.arrow_placement_manager.quadrant_index_handler import (
    QuadrantIndexHandler,
)
from placement_managers.arrow_placement_manager.arrow_adjustment_calculator import (
    ArrowAdjustmentCalculator,
)
from main_window.settings_manager.global_settings.app_context import AppContext
from placement_managers.arrow_placement_manager.strategies.default_placement_strategy import (
    DefaultPlacementStrategy,
)
from placement_managers.arrow_placement_manager.strategies.initial_placement_strategy import (
    InitialPlacementStrategy,
)
from placement_managers.arrow_placement_manager.strategies.quadrant_adjustment_strategy import (
    QuadrantAdjustmentStrategy,
)
from placement_managers.arrow_placement_manager.strategies.special_placement_strategy import (
    SpecialPlacementStrategy,
)

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow

from typing import TYPE_CHECKING
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


def compute_default_adjustment(arrow: "Arrow") -> QPointF:
    """Type-hinted function for default adjustment calculation."""
    return DefaultPlacementStrategy().compute_adjustment(
        arrow.pictograph.state.grid_mode,
        arrow.motion.state.motion_type,
        arrow.motion.state.turns,
    )


class ArrowPlacementManager:
    def __init__(self, pictograph: "Pictograph"):
        self.pictograph = pictograph
        self.quadrant_index_handler = QuadrantIndexHandler(self)
        self.initial_strategy = InitialPlacementStrategy(pictograph)
        self.default_strategy = DefaultPlacementStrategy()
        self.directional_strategy = QuadrantAdjustmentStrategy(
            self.quadrant_index_handler
        )

        self.data_updater = SpecialPlacementDataUpdater(
            self,
            self.pictograph.state,
            compute_default_adjustment,  # ✅ Use function with type hinting
            self.pictograph.managers.get,
            self.pictograph.managers.check,
        )

        self.special_strategy = SpecialPlacementStrategy(
            self.data_updater.ori_key_generator
        )
        self.adjustment_calculator = ArrowAdjustmentCalculator(
            self, AppContext.special_placement_loader()
        )

    def update_arrow_placements(self) -> None:
        """Updates all arrows in the pictograph with quadrant-based adjustments."""
        for arrow in self.pictograph.elements.arrows.values():
            self.update_arrow_position(arrow)

    def update_arrow_position(self, arrow: "Arrow") -> None:
        """Updates the position of a single arrow using initial position, special adjustments, and directional strategy."""
        initial_pos = self.initial_strategy.compute_initial_position(arrow)
        # default_adjustment = self.default_strategy.get_default_adjustment(arrow)
        # new_pos_with_default = initial_pos + default_adjustment
        adjustment = self.adjustment_calculator.get_adjustment(arrow)  # Returns QPointF
        dir_x, dir_y = (
            adjustment.x(),
            adjustment.y(),
        )
        final_x = initial_pos.x() + dir_x - arrow.boundingRect().center().x()
        final_y = initial_pos.y() + dir_y - arrow.boundingRect().center().y()
        arrow.setPos(final_x, final_y)

    def _build_context(self, arrow: "Arrow") -> ArrowPlacementContext:
        """Builds the ArrowPlacementContext object with relevant motion data."""
        return ArrowPlacementContext(
            grid_mode=self.pictograph.state.grid_mode,
            motion_type=arrow.motion.state.motion_type,
            letter=self.pictograph.state.letter,
            arrow_color=arrow.state.color,
            turns=arrow.motion.state.turns,
            start_ori=arrow.motion.state.start_ori,
        )

    def _has_special_placement(self, context: ArrowPlacementContext) -> bool:
        """Checks if a special placement exists for this arrow's context."""
        special_placements = self.special_strategy.get_special_placements()
        ori_key = self.data_updater.ori_key_generator.generate_ori_key_from_context(
            context
        )

        return context.letter.value in special_placements.get(
            context.grid_mode, {}
        ).get(ori_key, {})
