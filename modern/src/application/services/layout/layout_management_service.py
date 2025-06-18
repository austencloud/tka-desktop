"""
Layout Management Service - Main Coordinator

This module contains the main layout management service that coordinates
specialized layout classes while maintaining the same external interface.
It preserves all existing functionality by using composition and delegation
to the specialized calculators.
"""

from typing import Dict, Any, Optional, Tuple
import logging

from PyQt6.QtCore import QSize
from domain.models.core_models import SequenceData
from core.interfaces.core_services import ILayoutService

from .layout_types import LayoutConfig, LayoutMode, ScalingMode
from .beat_layout_calculator import BeatLayoutCalculator
from .responsive_scaling_calculator import ResponsiveScalingCalculator
from .component_position_calculator import ComponentPositionCalculator
from .layout_event_handler import LayoutEventHandler
from .ui_layout_provider import UILayoutProvider

# Event-driven architecture imports
try:
    from core.events import get_event_bus
    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    get_event_bus = None
    EVENT_SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class LayoutManagementService(ILayoutService):
    """
    Main layout management service that coordinates specialized layout classes.

    This service delegates to focused classes while maintaining the same
    external interface. It preserves all existing functionality by using
    composition and delegation to the specialized calculators.
    """

    def __init__(self, event_bus: Optional[Any] = None):
        # Basic UI layout configuration (ILayoutService)
        main_window_size = QSize(1400, 900)
        layout_ratio = (10, 10)  # 50/50 split between workbench and picker

        # Initialize specialized calculators and providers
        self._beat_layout_calculator = BeatLayoutCalculator()
        self._scaling_calculator = ResponsiveScalingCalculator()
        self._component_calculator = ComponentPositionCalculator(
            self._beat_layout_calculator
        )
        self._ui_layout_provider = UILayoutProvider(main_window_size, layout_ratio)

        # Initialize event handler
        self._event_handler = LayoutEventHandler(
            self._beat_layout_calculator, main_window_size
        )

        # Layout presets for different contexts
        self._layout_presets = self._load_layout_presets()

        # Default layout configurations
        self._default_configs = self._load_default_configs()

        # Event system integration
        self.event_bus = event_bus or (get_event_bus() if get_event_bus else None)

        # Subscribe to relevant events
        if self.event_bus:
            self._event_handler.setup_event_subscriptions(self.event_bus)

    def calculate_beat_frame_layout(
        self, sequence: SequenceData, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Delegate to beat layout calculator."""
        return self._beat_layout_calculator.calculate_beat_frame_layout(
            sequence, container_size
        )

    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Delegate to scaling calculator."""
        return self._scaling_calculator.calculate_responsive_scaling(
            content_size, container_size
        )

    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Delegate to beat layout calculator."""
        return self._beat_layout_calculator.get_optimal_grid_layout(
            item_count, container_size
        )

    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Delegate to component position calculator."""
        return self._component_calculator.calculate_component_positions(layout_config)

    def calculate_context_aware_scaling(
        self, context: str, base_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Delegate to scaling calculator."""
        return self._scaling_calculator.calculate_context_aware_scaling(
            context, base_size, container_size
        )

    def get_layout_for_screen_size(self, screen_size: Tuple[int, int]) -> LayoutConfig:
        """Delegate to scaling calculator."""
        return self._scaling_calculator.get_layout_for_screen_size(screen_size)

    # Configuration loading methods

    def _load_layout_presets(self) -> Dict[str, LayoutConfig]:
        """Load layout presets for different contexts."""
        return {
            "sequence_editor": LayoutConfig(
                mode=LayoutMode.HORIZONTAL_SCROLL,
                scaling_mode=ScalingMode.MAINTAIN_ASPECT,
                padding=10,
                spacing=5,
            ),
            "dictionary_browser": LayoutConfig(
                mode=LayoutMode.GRID,
                scaling_mode=ScalingMode.FIT_BOTH,
                padding=8,
                spacing=4,
                items_per_row=4,
            ),
            "mobile_view": LayoutConfig(
                mode=LayoutMode.VERTICAL_SCROLL,
                scaling_mode=ScalingMode.FIT_WIDTH,
                padding=5,
                spacing=3,
            ),
        }

    def _load_default_configs(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "min_beat_size": (80, 80),
            "max_beat_size": (200, 200),
            "default_padding": 10,
            "default_spacing": 5,
            "aspect_ratio_tolerance": 0.1,
        }

    # ILayoutService implementation methods - delegate to UILayoutProvider
    def get_main_window_size(self) -> QSize:
        """Delegate to UI layout provider."""
        return self._ui_layout_provider.get_main_window_size()

    def get_workbench_size(self) -> QSize:
        """Delegate to UI layout provider."""
        return self._ui_layout_provider.get_workbench_size()

    def get_picker_size(self) -> QSize:
        """Delegate to UI layout provider."""
        return self._ui_layout_provider.get_picker_size()

    def get_layout_ratio(self) -> Tuple[int, int]:
        """Delegate to UI layout provider."""
        return self._ui_layout_provider.get_layout_ratio()

    def set_layout_ratio(self, ratio: Tuple[int, int]) -> None:
        """Delegate to UI layout provider."""
        self._ui_layout_provider.set_layout_ratio(ratio)

    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        """Delegate to UI layout provider."""
        return self._ui_layout_provider.calculate_component_size(
            component_type, parent_size
        )

    def set_main_window_size(self, size: QSize) -> None:
        """Delegate to UI layout provider."""
        self._ui_layout_provider.set_main_window_size(size)

    def cleanup(self):
        """Delegate cleanup to event handler."""
        self._event_handler.cleanup(self.event_bus)
