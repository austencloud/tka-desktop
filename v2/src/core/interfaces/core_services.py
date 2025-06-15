"""
Core service interfaces for Kinetic Constructor v2.

These interfaces define the contracts for core services, replacing tightly-coupled dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from PyQt6.QtCore import QSize


class ILayoutService(ABC):
    """Interface for layout management services."""

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


class IMotionManagementService(ABC):
    """Interface for unified motion management operations."""

    @abstractmethod
    def validate_motion_combination(self, blue_motion: Any, red_motion: Any) -> bool:
        """Validate that two motions can be combined in a beat."""
        pass

    @abstractmethod
    def get_valid_motion_combinations(
        self, motion_type: Any, location: Any
    ) -> List[Any]:
        """Get all valid motion combinations for a given type and location."""
        pass

    @abstractmethod
    def calculate_motion_orientation(
        self, motion: Any, start_orientation: Any = None
    ) -> Any:
        """Calculate end orientation for a motion."""
        pass

    @abstractmethod
    def get_motion_validation_errors(
        self, blue_motion: Any, red_motion: Any
    ) -> List[str]:
        """Get detailed validation errors for motion combination."""
        pass


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


class ILayoutManagementService(ABC):
    """Interface for unified layout management operations."""

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
