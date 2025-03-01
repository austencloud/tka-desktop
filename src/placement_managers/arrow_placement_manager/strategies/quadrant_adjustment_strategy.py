from PyQt6.QtCore import QPointF
from placement_managers.arrow_placement_manager.directional_tuple_generator import (
    DirectionalTupleGenerator,
)
from objects.arrow.arrow import Arrow
from placement_managers.arrow_placement_manager.quadrant_index_handler import (
    QuadrantIndexHandler,
)


class QuadrantAdjustmentStrategy:
    def __init__(self, quadrant_index_handler: QuadrantIndexHandler) -> None:
        self.quadrant_index_handler = quadrant_index_handler

    def compute_adjustment(self, arrow: Arrow, base_adjustment: QPointF) -> QPointF:
        """Applies quadrant-based directional adjustments to the base position."""
        directional_manager = DirectionalTupleGenerator(arrow.motion)
        directional_adjustments = directional_manager.generate_directional_tuples(
            base_adjustment.x(), base_adjustment.y()
        )

        quadrant_index = self.quadrant_index_handler.get_quadrant_index(arrow)

        if directional_adjustments and 0 <= quadrant_index < len(
            directional_adjustments
        ):
            return QPointF(*directional_adjustments[quadrant_index])

        return QPointF(0, 0)
