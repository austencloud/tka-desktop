"""
Enhanced dependency injection container for Kinetic Constructor v2.

This provides a modern dependency injection system with automatic constructor injection,
type validation, and Protocol compliance verification.
"""

from typing import (
    TypeVar,
    Type,
    Dict,
    Any,
    Optional,
    Callable,
    Union,
    get_type_hints,
    Protocol,
    List,
    Set,
)
import logging
import inspect
from pathlib import Path
from datetime import datetime, timedelta

T = TypeVar("T")
logger = logging.getLogger(__name__)

# Global container instance
_container: Optional["DIContainer"] = None


class DIContainer:
    """
    Enhanced dependency injection container with automatic constructor injection.

    Features:
    - Singleton and transient service lifetimes
    - Automatic constructor injection with type resolution
    - Protocol compliance validation
    - Circular dependency detection
    - Type safety validation
    - Service lifecycle management
    - Enhanced error reporting
    """

    def __init__(self):
        self._services: Dict[Type, Type] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Type] = {}
        self._resolution_stack: Set[Type] = set()
        self._cleanup_handlers: List[Callable[[], None]] = (
            []
        )  # For lifecycle management
        self._creation_stack: List[Type] = (
            []
        )  # For enhanced circular dependency detection

    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as singleton (one instance per container)."""
        self._validate_registration(interface, implementation)
        self._services[interface] = implementation
        logger.debug(
            f"Registered singleton: {interface.__name__} -> {implementation.__name__}"
        )

    def register_transient(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register a service as transient (new instance each time)."""
        self._validate_registration(interface, implementation)
        self._factories[interface] = implementation
        logger.debug(
            f"Registered transient: {interface.__name__} -> {implementation.__name__}"
        )

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """Register a specific instance."""
        self._singletons[interface] = instance
        logger.debug(f"Registered instance: {interface.__name__}")

    def auto_register(self, interface: Type[T], implementation: Type[T]) -> None:
        """Register with automatic Protocol validation."""
        self._validate_protocol_implementation(interface, implementation)
        self.register_singleton(interface, implementation)

    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service instance with automatic constructor injection.

        Args:
            interface: The interface/type to resolve

        Returns:
            An instance of the requested type

        Raises:
            ValueError: If the service is not registered
            RuntimeError: If circular dependency is detected
        """

        # Check for circular dependencies
        if interface in self._resolution_stack:
            raise RuntimeError(f"Circular dependency detected for {interface.__name__}")

        # Check for existing singleton instance
        if interface in self._singletons:
            return self._singletons[interface]

        # Check for singleton registration
        if interface in self._services:
            implementation = self._services[interface]
            self._resolution_stack.add(interface)
            try:
                instance = self._create_instance(implementation)
                self._singletons[interface] = instance
                return instance
            finally:
                self._resolution_stack.discard(interface)

        # Check for transient registration
        if interface in self._factories:
            implementation = self._factories[interface]
            self._resolution_stack.add(interface)
            try:
                return self._create_instance(implementation)
            finally:
                self._resolution_stack.discard(interface)

        raise ValueError(f"Service {interface.__name__} is not registered")

    def _create_instance(self, implementation_class: Type) -> Any:
        """Create instance with comprehensive automatic constructor injection."""
        try:
            signature = inspect.signature(implementation_class.__init__)
            type_hints = get_type_hints(implementation_class.__init__)
            dependencies = {}

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                param_type = type_hints.get(param_name, param.annotation)

                # Enhanced dependency resolution
                if param.default != inspect.Parameter.empty:
                    # Has default value - use it and skip dependency resolution
                    dependencies[param_name] = param.default
                    continue

                # Skip if no type annotation
                if not param_type or param_type == inspect.Parameter.empty:
                    continue

                # Skip primitive types
                if self._is_primitive_type(param_type):
                    continue

                # Enhanced error handling for dependency resolution
                try:
                    dependencies[param_name] = self.resolve(param_type)
                except ValueError as e:
                    available_services = list(self._services.keys()) + list(
                        self._factories.keys()
                    )
                    available_names = [svc.__name__ for svc in available_services]
                    raise ValueError(
                        f"Cannot resolve dependency {param_type.__name__} for parameter "
                        f"'{param_name}' in {implementation_class.__name__}. "
                        f"Original error: {e}. "
                        f"Available registrations: {available_names}"
                    )

            return implementation_class(**dependencies)

        except Exception as e:
            available_services = list(self._services.keys()) + list(
                self._factories.keys()
            )
            available_names = [svc.__name__ for svc in available_services]
            logger.error(
                f"Failed to create instance of {implementation_class.__name__}: {e}"
            )
            logger.error(f"Available services: {available_names}")
            raise RuntimeError(
                f"Dependency injection failed for {implementation_class.__name__}: {e}"
            )

    def _validate_registration(self, interface: Type, implementation: Type) -> None:
        """Validate that implementation can fulfill interface contract."""
        if not inspect.isclass(implementation):
            raise ValueError(f"Implementation {implementation} must be a class")

        # Basic validation - implementation should be a subclass or implement interface
        if hasattr(interface, "__origin__") and interface.__origin__ is not None:
            # Handle generic types
            return

        # Skip Protocol validation in basic registration - only validate in auto_register
        if hasattr(interface, "_is_protocol") and interface._is_protocol:
            return  # Protocol validation handled separately

        if inspect.isclass(interface) and not issubclass(implementation, interface):
            # For concrete classes, check inheritance
            if not hasattr(interface, "__annotations__"):
                logger.warning(
                    f"No inheritance relationship between {interface} and {implementation}"
                )

    def _validate_protocol_implementation(
        self, protocol: Type, implementation: Type
    ) -> None:
        """Validate implementation fulfills Protocol contract."""
        if not hasattr(protocol, "_is_protocol") or not protocol._is_protocol:
            return  # Not a Protocol, skip validation

        # Get protocol methods from annotations
        protocol_methods = getattr(protocol, "__annotations__", {})

        # Also check for methods defined in the protocol
        for attr_name in dir(protocol):
            if not attr_name.startswith("_") and attr_name not in protocol_methods:
                attr = getattr(protocol, attr_name)
                if callable(attr):
                    protocol_methods[attr_name] = attr

        # Check implementation has all required methods
        for method_name in protocol_methods:
            if not hasattr(implementation, method_name):
                raise ValueError(
                    f"{implementation.__name__} doesn't implement {method_name} from {protocol.__name__}"
                )

    def get_registrations(self) -> Dict[Type, Type]:
        """Get all registered services for testing/debugging."""
        # Include singletons (instances), services, and factories
        registrations = {}

        # Add singleton instances
        for interface in self._singletons.keys():
            registrations[interface] = type(self._singletons[interface])

        # Add service registrations
        registrations.update(self._services)

        # Add factory registrations
        registrations.update(self._factories)

        return registrations

    def _is_primitive_type(self, param_type: Type) -> bool:
        """Check if a type is a primitive type that should not be resolved as a dependency."""
        primitive_types = {
            str,
            int,
            float,
            bool,
            bytes,
            type(None),
            list,
            dict,
            tuple,
            set,
            frozenset,
            # Add common standard library types
            Path,
            datetime,
            timedelta,
        }

        # Handle Union types (like Optional[str] which is Union[str, None])
        if hasattr(param_type, "__origin__"):
            origin = param_type.__origin__
            if origin is Union:
                # Check if it's Optional[T] (Union[T, None])
                args = getattr(param_type, "__args__", ())
                if len(args) == 2 and type(None) in args:
                    # It's Optional[T], check the non-None type
                    non_none_type = next(arg for arg in args if arg is not type(None))
                    return self._is_primitive_type(non_none_type)
                # For other Union types, check if all args are primitive
                return all(arg in primitive_types for arg in args)
            # Other generic types like List[str], Dict[str, int] are considered primitive
            if origin in primitive_types:
                return True

        # Check if it's a builtin type
        if hasattr(param_type, "__module__") and param_type.__module__ == "builtins":
            return True

        return param_type in primitive_types

    def auto_register_with_validation(
        self, interface: Type[T], implementation: Type[T]
    ) -> None:
        """Register service with comprehensive validation."""
        # Step 1: Validate Protocol implementation
        self._validate_protocol_implementation(interface, implementation)

        # Step 2: Validate dependency chain can be resolved
        self._validate_dependency_chain(implementation)

        # Step 3: Register if validation passes
        self.register_singleton(interface, implementation)

        logger.info(
            f"✅ Successfully registered {interface.__name__} -> {implementation.__name__}"
        )

    def _validate_dependency_chain(self, implementation: Type) -> None:
        """Validate that all constructor dependencies can be resolved."""
        signature = inspect.signature(implementation.__init__)
        type_hints = get_type_hints(implementation.__init__)

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue

            # Skip if has default value
            if param.default != inspect.Parameter.empty:
                continue

            param_type = type_hints.get(param_name, param.annotation)

            # Skip if no type annotation
            if not param_type or param_type == inspect.Parameter.empty:
                continue

            # Skip primitives
            if self._is_primitive_type(param_type):
                continue

            # Check if dependency is registered
            if param_type not in self._services and param_type not in self._factories:
                raise ValueError(
                    f"Dependency {param_type.__name__} for {implementation.__name__} "
                    f"is not registered. Register it first or make parameter optional."
                )

    def validate_all_registrations(self) -> None:
        """Validate that all registered services can be instantiated."""
        errors = []

        for interface, implementation in self._services.items():
            try:
                self.resolve(interface)
                logger.info(f"✅ {interface.__name__} -> {implementation.__name__}")
            except Exception as e:
                errors.append(f"❌ {interface.__name__}: {e}")

        if errors:
            logger.error("Registration validation failed:")
            for error in errors:
                logger.error(f"  {error}")
            raise ValueError(
                f"Service registration validation failed: {len(errors)} errors"
            )

        logger.info(
            f"✅ All {len(self._services)} service registrations validated successfully"
        )

    def _get_constructor_dependencies(self, implementation: Type) -> List[Type]:
        """Get list of constructor dependencies for a class."""
        try:
            signature = inspect.signature(implementation.__init__)
            type_hints = get_type_hints(implementation.__init__)
            dependencies = []

            for param_name, param in signature.parameters.items():
                if param_name == "self":
                    continue

                # Skip if has default value
                if param.default != inspect.Parameter.empty:
                    continue

                param_type = type_hints.get(param_name, param.annotation)

                # Skip if no type annotation
                if not param_type or param_type == inspect.Parameter.empty:
                    continue

                # Skip primitive types
                if self._is_primitive_type(param_type):
                    continue

                dependencies.append(param_type)

            return dependencies

        except Exception:
            return []

    def _detect_circular_dependencies(
        self, start_type: Type, visited: Optional[Set[Type]] = None
    ) -> None:
        """Detect circular dependencies in the service graph."""
        if visited is None:
            visited = set()

        if start_type in visited:
            cycle_path = (
                " -> ".join(t.__name__ for t in visited) + f" -> {start_type.__name__}"
            )
            raise ValueError(f"Circular dependency detected: {cycle_path}")

        visited.add(start_type)

        # Get implementation for this type
        implementation = self._services.get(start_type) or self._factories.get(
            start_type
        )
        if implementation:
            dependencies = self._get_constructor_dependencies(implementation)
            for dep in dependencies:
                self._detect_circular_dependencies(dep, visited.copy())

    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Generate dependency graph for debugging."""
        graph = {}

        for interface, implementation in self._services.items():
            deps = self._get_constructor_dependencies(implementation)
            graph[f"{interface.__name__} -> {implementation.__name__}"] = [
                dep.__name__ for dep in deps if not self._is_primitive_type(dep)
            ]

        for interface, implementation in self._factories.items():
            deps = self._get_constructor_dependencies(implementation)
            graph[f"{interface.__name__} -> {implementation.__name__} (transient)"] = [
                dep.__name__ for dep in deps if not self._is_primitive_type(dep)
            ]

        return graph

    def _create_with_lifecycle(self, implementation_class: Type) -> Any:
        """Create instance with proper lifecycle management."""
        instance = self._create_instance(implementation_class)

        # Call initialization method if it exists
        if hasattr(instance, "initialize") and callable(
            getattr(instance, "initialize")
        ):
            instance.initialize()

        # Register for cleanup if it has cleanup method
        if hasattr(instance, "cleanup") and callable(getattr(instance, "cleanup")):
            self._cleanup_handlers.append(instance.cleanup)

        return instance

    def cleanup_all(self) -> None:
        """Cleanup all registered services."""
        for cleanup_handler in reversed(self._cleanup_handlers):
            try:
                cleanup_handler()
            except Exception as e:
                logger.error(f"Error during service cleanup: {e}")

        self._cleanup_handlers.clear()


def get_container() -> DIContainer:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = DIContainer()
    return _container


def reset_container() -> None:
    """Reset the global container (useful for testing)."""
    global _container
    _container = None


# Backward compatibility alias
DIContainer = DIContainer
