"""
Layout Management Bridge Service - Temporary Compatibility Layer

This is a temporary bridge service that delegates to the new focused layout services
while maintaining the original LayoutManagementService interface.

This allows existing consumers to continue working while we update them
to use the new focused layout services directly.

TEMPORARY: This service should be removed once all consumers are updated.
"""

from typing import Dict, Any, Tuple
from application.services.layout.beat_layout_service import IBeatLayoutService
from application.services.layout.responsive_layout_service import IResponsiveLayoutService
from application.services.layout.component_layout_service import IComponentLayoutService
from domain.models.core_models import SequenceData


class LayoutManagementBridgeService:
    """
    Temporary bridge service that delegates to focused layout services.
    
    This maintains compatibility with the original LayoutManagementService
    interface while using the new focused services internally.
    """

    def __init__(
        self,
        beat_layout_service: IBeatLayoutService,
        responsive_layout_service: IResponsiveLayoutService,
        component_layout_service: IComponentLayoutService,
    ):
        self._beat_layout_service = beat_layout_service
        self._responsive_layout_service = responsive_layout_service
        self._component_layout_service = component_layout_service

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames in a sequence."""
        return self._beat_layout_service.calculate_beat_frame_layout(
            sequence, container_size
        )

    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""
        return self._responsive_layout_service.calculate_responsive_scaling(
            content_size, container_size
        )

    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        return self._beat_layout_service.get_optimal_grid_layout(
            item_count, container_size
        )

    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for UI components."""
        return self._component_layout_service.calculate_component_positions(
            layout_config
        )

    def calculate_context_aware_scaling(
        self, context: str, base_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate scaling based on context."""
        return self._responsive_layout_service.calculate_context_aware_scaling(
            context, base_size, container_size
        )

    def get_layout_for_screen_size(self, screen_size: Tuple[int, int]):
        """Get appropriate layout configuration for screen size."""
        return self._responsive_layout_service.get_layout_for_screen_size(screen_size)
