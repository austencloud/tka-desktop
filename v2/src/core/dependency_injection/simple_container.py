"""
Simple dependency injection container for Kinetic Constructor v2.

This provides a lightweight dependency injection system to replace global state access.
"""

from typing import TypeVar, Type, Dict, Any, Optional, Callable, Union
import logging

T = TypeVar("T")
logger = logging.getLogger(__name__)

# Global container instance
_container: Optional["SimpleContainer"] = None


class SimpleContainer:
    """
    Simple dependency injection container.

    Features:
    - Singleton and transient service lifetimes
    - Constructor injection
    - Interface-based registration
    """

    def __init__(self):
        self._services: Dict[Type, Type] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Type] = {}

    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as singleton (one instance per container)."""
        self._services[interface] = implementation
        logger.debug(
            f"Registered singleton: {interface.__name__} -> {implementation.__name__}"
        )

    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as transient (new instance each time)."""
        self._factories[interface] = implementation
        logger.debug(
            f"Registered transient: {interface.__name__} -> {implementation.__name__}"
        )

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a specific instance."""
        self._singletons[interface] = instance
        logger.debug(f"Registered instance: {interface.__name__}")

    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service instance.

        Args:
            interface: The interface/type to resolve

        Returns:
            An instance of the requested type

        Raises:
            ValueError: If the service is not registered
        """
        # Check for existing singleton instance
        if interface in self._singletons:
            return self._singletons[interface]

        # Check for singleton registration
        if interface in self._services:
            implementation = self._services[interface]
            instance = self._create_instance(implementation)
            self._singletons[interface] = instance
            return instance

        # Check for transient registration
        if interface in self._factories:
            implementation = self._factories[interface]
            return self._create_instance(implementation)

        raise ValueError(f"Service {interface.__name__} is not registered")

    def _create_instance(self, implementation_class: Type) -> Any:
        try:
            return implementation_class()
        except Exception as e:
            logger.error(
                f"Failed to create instance of {implementation_class.__name__}: {e}"
            )
            raise


def get_container() -> SimpleContainer:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = SimpleContainer()
    return _container


def reset_container() -> None:
    """Reset the global container (useful for testing)."""
    global _container
    _container = None
