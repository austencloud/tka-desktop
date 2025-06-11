"""
Modern application context that replaces the global singleton AppContext.

This module provides a clean, dependency-injected way to access application services
without the tight coupling and testing issues of the original singleton pattern.
"""

from typing import TYPE_CHECKING, Optional
from .dependency_container import get_container, DependencyContainer

if TYPE_CHECKING:
    from interfaces.settings_manager_interface import ISettingsManager
    from interfaces.json_manager_interface import IJsonManager
    from objects.arrow.arrow import Arrow


class ApplicationContext:
    """
    Application context that provides access to core services through dependency injection.

    This replaces the global AppContext singleton with a proper, testable design.
    """

    def __init__(self, container: Optional[DependencyContainer] = None):
        """
        Initialize the application context.

        Args:
            container: Dependency container. If None, uses the global container.
        """
        self._container = container or get_container()
        self._selected_arrow: Optional["Arrow"] = None

    @property
    def settings_manager(self) -> "ISettingsManager":
        """Get the settings manager service."""
        from interfaces.settings_manager_interface import ISettingsManager

        return self._container.resolve(ISettingsManager)

    @property
    def json_manager(self) -> "IJsonManager":
        """Get the JSON manager service."""
        from interfaces.json_manager_interface import IJsonManager

        return self._container.resolve(IJsonManager)

    @property
    def selected_arrow(self) -> Optional["Arrow"]:
        """Get the currently selected arrow."""
        return self._selected_arrow

    @selected_arrow.setter
    def selected_arrow(self, arrow: Optional["Arrow"]) -> None:
        """Set the currently selected arrow."""
        self._selected_arrow = arrow

    def get_service(self, service_type):
        """
        Generic method to get any registered service.

        Args:
            service_type: The type/interface of the service to resolve

        Returns:
            The resolved service instance
        """
        return self._container.resolve(service_type)


# Factory function for creating application context
def create_application_context(
    container: Optional[DependencyContainer] = None,
) -> ApplicationContext:
    """
    Create a new application context.

    Args:
        container: Optional dependency container. If None, uses global container.

    Returns:
        A new ApplicationContext instance
    """
    return ApplicationContext(container)


# For backward compatibility during migration
class LegacyAppContextAdapter:
    """
    Adapter to help migrate from the old AppContext singleton.

    This provides the same interface as the old AppContext but uses
    the new dependency injection system under the hood.
    """

    def __init__(self, app_context: ApplicationContext):
        self._app_context = app_context

    @classmethod
    def settings_manager(cls):
        """Legacy method - use app_context.settings_manager instead."""
        # This would need to be populated during migration
        # For now, it's a placeholder
        raise NotImplementedError("Use dependency injection instead")

    @classmethod
    def json_manager(cls):
        """Legacy method - use app_context.json_manager instead."""
        raise NotImplementedError("Use dependency injection instead")

    @classmethod
    def selected_arrow(cls):
        """Legacy method - use app_context.selected_arrow instead."""
        raise NotImplementedError("Use dependency injection instead")


# Migration helper
def create_legacy_adapter(app_context: ApplicationContext) -> LegacyAppContextAdapter:
    """Create a legacy adapter for gradual migration."""
    return LegacyAppContextAdapter(app_context)
