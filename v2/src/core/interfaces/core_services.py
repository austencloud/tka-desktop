"""
Core service interfaces for Kinetic Constructor v2.

These interfaces define the contracts for core services, replacing tightly-coupled dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
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
    def calculate_component_size(self, component_type: str, parent_size: QSize) -> QSize:
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
