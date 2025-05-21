from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class ISettingsManager(Protocol):
    """Interface for the settings manager.

    Using Protocol instead of ABC to avoid metaclass conflicts with QObject.
    """

    def get_setting(self, section: str, key: str, default_value: Any = None) -> Any:
        """Get a setting value from the specified section."""
        ...

    def set_setting(self, section: str, key: str, value: Any) -> None:
        """Set a setting value in the specified section."""
        ...

    def get_global_settings(self):
        """Get the global settings object."""
        ...

    def get_construct_tab_settings(self):
        """Get the construct tab settings object."""
        ...

    def get_generate_tab_settings(self):
        """Get the generate tab settings object."""
        ...

    @property
    def browse_settings(self):
        """Get the browse tab settings object."""
        ...
