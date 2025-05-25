from typing import Any, Optional, Protocol, runtime_checkable
from abc import abstractmethod


@runtime_checkable
class ISettingsManager(Protocol):
    """
    Interface for the settings manager with comprehensive type safety.

    This interface defines all methods that a settings manager must implement,
    providing clear contracts for dependency injection and testing.
    """

    @abstractmethod
    def get_setting(self, section: str, key: str, default_value: Any = None) -> Any:
        """
        Get a setting value.

        Args:
            section: Settings section name
            key: Setting key
            default_value: Default value if setting not found

        Returns:
            The setting value or default
        """
        ...

    @abstractmethod
    def set_setting(self, section: str, key: str, value: Any) -> None:
        """
        Set a setting value.

        Args:
            section: Settings section name
            key: Setting key
            value: Value to set
        """
        ...

    @abstractmethod
    def save_settings(self) -> bool:
        """
        Save all settings to persistent storage.

        Returns:
            True if successful, False otherwise
        """
        ...

    @abstractmethod
    def load_settings(self) -> bool:
        """
        Load settings from persistent storage.

        Returns:
            True if successful, False otherwise
        """
        ...

    # Typed property accessors for major setting groups
    @property
    @abstractmethod
    def global_settings(self) -> "IGlobalSettings":
        """Get global settings interface."""
        ...

    @property
    @abstractmethod
    def construct_tab_settings(self) -> "IConstructTabSettings":
        """Get construct tab settings interface."""
        ...

    @property
    @abstractmethod
    def generate_tab_settings(self) -> "IGenerateTabSettings":
        """Get generate tab settings interface."""
        ...

    @property
    @abstractmethod
    def browse_tab_settings(self) -> "IBrowseTabSettings":
        """Get browse tab settings interface."""
        ...

    @property
    @abstractmethod
    def write_tab_settings(self) -> "IWriteTabSettings":
        """Get write tab settings interface."""
        ...

    @property
    @abstractmethod
    def image_export_settings(self) -> "IImageExportSettings":
        """Get image export settings interface."""
        ...

    @property
    @abstractmethod
    def sequence_card_tab_settings(self) -> "ISequenceCardTabSettings":
        """Get sequence card tab settings interface."""
        ...

    @property
    @abstractmethod
    def user_profile_settings(self) -> "IUserProfileSettings":
        """Get user profile settings interface."""
        ...

    @property
    @abstractmethod
    def visibility_settings(self) -> "IVisibilitySettings":
        """Get visibility settings interface."""
        ...


@runtime_checkable
class IGlobalSettings(Protocol):
    """Interface for global application settings."""

    @abstractmethod
    def get_current_tab(self) -> str:
        """Get the current active tab."""
        ...

    @abstractmethod
    def set_current_tab(self, tab_name: str) -> None:
        """Set the current active tab."""
        ...

    @abstractmethod
    def get_grid_mode(self) -> str:
        """Get the current grid mode (diamond/box)."""
        ...

    @abstractmethod
    def set_grid_mode(self, mode: str) -> None:
        """Set the grid mode."""
        ...

    @abstractmethod
    def get_prop_type(self) -> str:
        """Get the current prop type."""
        ...

    @abstractmethod
    def set_prop_type(self, prop_type: str) -> None:
        """Set the prop type."""
        ...


@runtime_checkable
class IConstructTabSettings(Protocol):
    """Interface for construct tab settings."""

    @abstractmethod
    def get_auto_builder_enabled(self) -> bool:
        """Get auto builder enabled state."""
        ...

    @abstractmethod
    def set_auto_builder_enabled(self, enabled: bool) -> None:
        """Set auto builder enabled state."""
        ...


@runtime_checkable
class IGenerateTabSettings(Protocol):
    """Interface for generate tab settings."""

    @abstractmethod
    def get_level(self) -> int:
        """Get generation level."""
        ...

    @abstractmethod
    def set_level(self, level: int) -> None:
        """Set generation level."""
        ...

    @abstractmethod
    def get_length(self) -> int:
        """Get sequence length."""
        ...

    @abstractmethod
    def set_length(self, length: int) -> None:
        """Set sequence length."""
        ...


@runtime_checkable
class IBrowseTabSettings(Protocol):
    """Interface for browse tab settings."""

    @abstractmethod
    def get_sort_method(self) -> str:
        """Get current sort method."""
        ...

    @abstractmethod
    def set_sort_method(self, method: str) -> None:
        """Set sort method."""
        ...


@runtime_checkable
class IWriteTabSettings(Protocol):
    """Interface for write tab settings."""

    @abstractmethod
    def get_auto_save_enabled(self) -> bool:
        """Get auto save enabled state."""
        ...

    @abstractmethod
    def set_auto_save_enabled(self, enabled: bool) -> None:
        """Set auto save enabled state."""
        ...


@runtime_checkable
class IImageExportSettings(Protocol):
    """Interface for image export settings."""

    @abstractmethod
    def get_include_start_position(self) -> bool:
        """Get include start position setting."""
        ...

    @abstractmethod
    def set_include_start_position(self, include: bool) -> None:
        """Set include start position setting."""
        ...


@runtime_checkable
class ISequenceCardTabSettings(Protocol):
    """Interface for sequence card tab settings."""

    @abstractmethod
    def get_columns_per_row(self) -> int:
        """Get columns per row setting."""
        ...

    @abstractmethod
    def set_columns_per_row(self, columns: int) -> None:
        """Set columns per row setting."""
        ...


@runtime_checkable
class IUserProfileSettings(Protocol):
    """Interface for user profile settings."""

    @abstractmethod
    def get_username(self) -> str:
        """Get username."""
        ...

    @abstractmethod
    def set_username(self, username: str) -> None:
        """Set username."""
        ...


@runtime_checkable
class IVisibilitySettings(Protocol):
    """Interface for visibility settings."""

    @abstractmethod
    def get_show_grid(self) -> bool:
        """Get show grid setting."""
        ...

    @abstractmethod
    def set_show_grid(self, show: bool) -> None:
        """Set show grid setting."""
        ...
