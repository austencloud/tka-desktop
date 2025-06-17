"""
Core service interfaces for Kinetic Constructor.

These interfaces define the contracts for core services, replacing tightly-coupled dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from PyQt6.QtCore import QSize


class ILayoutService(ABC):
    """
    Unified interface for all layout management operations.

    Consolidates both basic UI layout and advanced layout calculations
    into a single cohesive interface to reduce complexity.
    """

    # Basic UI Layout Methods (formerly ILayoutService)
    @abstractmethod
    def get_main_window_size(self) -> QSize:
        """Get the main window size."""
        pass

    @abstractmethod
    def get_workbench_size(self) -> QSize:
        """Get the workbench area size."""
        pass

    @abstractmethod
    def get_picker_size(self) -> QSize:
        """Get the option picker size."""
        pass

    @abstractmethod
    def get_layout_ratio(self) -> tuple[int, int]:
        """Get the layout ratio (workbench:picker)."""
        pass

    @abstractmethod
    def set_layout_ratio(self, ratio: tuple[int, int]) -> None:
        """Set the layout ratio."""
        pass

    @abstractmethod
    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        """Calculate component size based on parent and type."""
        pass

    # Advanced Layout Methods (formerly ILayoutManagementService)
    @abstractmethod
    def calculate_beat_frame_layout(
        self, sequence: Any, container_size: Tuple[int, int]
    ) -> Dict[str, Any]:
        """Calculate layout for beat frames in a sequence."""
        pass

    @abstractmethod
    def calculate_responsive_scaling(
        self, content_size: Tuple[int, int], container_size: Tuple[int, int]
    ) -> float:
        """Calculate responsive scaling factor."""
        pass

    @abstractmethod
    def get_optimal_grid_layout(
        self, item_count: int, container_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Get optimal grid layout (rows, cols) for items."""
        pass

    @abstractmethod
    def calculate_component_positions(
        self, layout_config: Dict[str, Any]
    ) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for UI components."""
        pass


class ISettingsService(ABC):
    """Interface for settings management."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        pass

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        pass

    @abstractmethod
    def save_settings(self) -> None:
        """Save settings to persistent storage."""
        pass

    @abstractmethod
    def load_settings(self) -> None:
        """Load settings from persistent storage."""
        pass


class ISequenceDataService(ABC):
    """Interface for sequence data management."""

    @abstractmethod
    def get_all_sequences(self) -> List[Dict[str, Any]]:
        """Get all available sequences."""
        pass

    @abstractmethod
    def get_sequence_by_id(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific sequence by ID."""
        pass

    @abstractmethod
    def save_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        """Save sequence data."""
        pass

    @abstractmethod
    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete a sequence."""
        pass

    @abstractmethod
    def create_new_sequence(self, name: str) -> Dict[str, Any]:
        """Create a new empty sequence."""
        pass


class IValidationService(ABC):
    """Interface for validation services."""

    @abstractmethod
    def validate_sequence(self, sequence_data: Dict[str, Any]) -> bool:
        """Validate a sequence."""
        pass

    @abstractmethod
    def validate_beat(self, beat_data: Dict[str, Any]) -> bool:
        """Validate a beat."""
        pass

    @abstractmethod
    def validate_motion(self, motion_data: Dict[str, Any]) -> bool:
        """Validate a motion."""
        pass

    @abstractmethod
    def get_validation_errors(self, data: Dict[str, Any]) -> List[str]:
        """Get validation errors for data."""
        pass


class IArrowManagementService(ABC):
    """Interface for unified arrow management operations."""

    @abstractmethod
    def calculate_arrow_position(
        self, arrow_data: Any, pictograph_data: Any
    ) -> Tuple[float, float, float]:
        """Calculate complete arrow position and rotation."""
        pass

    @abstractmethod
    def should_mirror_arrow(self, arrow_data: Any) -> bool:
        """Determine if arrow should be mirrored based on motion type."""
        pass

    @abstractmethod
    def apply_beta_positioning(self, beat_data: Any) -> Any:
        """Apply beta prop positioning if needed."""
        pass

    @abstractmethod
    def calculate_all_arrow_positions(self, pictograph_data: Any) -> Any:
        """Calculate positions for all arrows in pictograph."""
        pass


# IMotionManagementService removed - bridge service eliminated
# Consumers should use focused services directly:
# - IMotionValidationService for validation
# - IMotionGenerationService for generation
# - IMotionOrientationService for orientation


class ISequenceManagementService(ABC):
    """Interface for unified sequence management operations."""

    @abstractmethod
    def create_sequence(self, name: str, length: int = 16) -> Any:
        """Create a new sequence with specified length."""
        pass

    @abstractmethod
    def add_beat(self, sequence: Any, beat: Any, position: int) -> Any:
        """Add beat to sequence at specified position."""
        pass

    @abstractmethod
    def remove_beat(self, sequence: Any, position: int) -> Any:
        """Remove beat from sequence at specified position."""
        pass

    @abstractmethod
    def generate_sequence(self, sequence_type: str, length: int, **kwargs) -> Any:
        """Generate sequence using specified algorithm."""
        pass

    @abstractmethod
    def apply_workbench_operation(self, sequence: Any, operation: str, **kwargs) -> Any:
        """Apply workbench transformation to sequence."""
        pass


class IPictographManagementService(ABC):
    """Interface for unified pictograph management operations."""

    @abstractmethod
    def create_pictograph(self, grid_mode: Any = None) -> Any:
        """Create a new blank pictograph."""
        pass

    @abstractmethod
    def create_from_beat(self, beat_data: Any) -> Any:
        """Create pictograph from beat data."""
        pass

    @abstractmethod
    def search_dataset(self, query: Dict[str, Any]) -> List[Any]:
        """Search pictograph dataset with query."""
        pass


class IUIStateManagementService(ABC):
    """Interface for unified UI state management operations."""

    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        pass

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        pass

    @abstractmethod
    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get state for a specific tab."""
        pass

    @abstractmethod
    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        pass


# ILayoutManagementService has been consolidated into ILayoutService above
# This removes the duplicate interface definition to reduce complexity
