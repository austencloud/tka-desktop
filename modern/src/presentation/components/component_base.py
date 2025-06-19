"""
ViewableComponentBase - Foundation for All Modern Components

This provides the missing architectural piece from the implementation plan.
ALL modern components should inherit from this base class to ensure:
- Zero global state access
- Pure dependency injection
- Event-driven communication
- Proper lifecycle management
- Consistent component interface

REPLACES: Direct QObject inheritance with global state access
PROVIDES: Clean component architecture with dependency injection
"""

from abc import ABC, abstractmethod, ABCMeta
from typing import Optional, Any, Dict, List, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal
import logging

# Type imports
from core.dependency_injection.di_container import DIContainer

# A+ Enhancement: Import Qt integration - Temporarily disabled due to import issues
# try:
#     from core.qt_integration import qt_factory, memory_detector, AutoManagedWidget
#     QT_INTEGRATION_AVAILABLE = True
# except ImportError:
#     QT_INTEGRATION_AVAILABLE = False
#     AutoManagedWidget = QWidget  # Fallback

# Temporary fallback
QT_INTEGRATION_AVAILABLE = False
AutoManagedWidget = QWidget

# Event system imports with fallback
try:
    from core.events import IEventBus, BaseEvent

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # Fallback for when event system is not available
    IEventBus = None
    BaseEvent = None
    EVENT_SYSTEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class QObjectABCMeta(type(QObject), ABCMeta):
    """Metaclass that combines QObject's metaclass with ABCMeta."""

    pass


class ViewableComponentBase(QObject, ABC, metaclass=QObjectABCMeta):
    """
    WORLD-CLASS Component Base Class - The Missing Architectural Foundation

    This is the base class specified in the implementation plan that was missing.
    ALL modern components should inherit from this to ensure architectural purity.

    Features:
    - ZERO global state access (no AppContext, no main widget coupling)
    - Pure dependency injection via container
    - Event-driven communication
    - Proper lifecycle management
    - Standard component signals
    - Resource cleanup

    USAGE PATTERN:
        class MyComponent(ViewableComponentBase):
            def __init__(self, container: DIContainer, parent=None):
                super().__init__(container, parent)
                # Component-specific initialization

            def initialize(self) -> None:
                # Implement component initialization
                self._layout_service = self.container.resolve(ILayoutService)
                # ... other initialization
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self) -> QWidget:
                # Return the main widget for this component
                return self._widget
    """

    # Standard component signals - all components will have these
    component_ready = pyqtSignal()  # Emitted when component is fully initialized
    component_error = pyqtSignal(str)  # Emitted when component encounters an error
    data_changed = pyqtSignal(object)  # Emitted when component data changes
    state_changed = pyqtSignal(str, object)  # Emitted when component state changes

    def __init__(self, container: DIContainer, parent: Optional[QObject] = None):
        """
        Initialize component with dependency injection.

        Args:
            container: Dependency injection container for service resolution
            parent: Qt parent object (optional)
        """
        super().__init__(parent)

        # Core dependencies
        self.container = container
        self.event_bus: Optional[Any] = None

        # Component state
        self._widget: Optional[QWidget] = None
        self._initialized = False
        self._cleanup_handlers: List[callable] = []

        # A+ Enhancement: Register with Qt integration - Temporarily disabled
        # if QT_INTEGRATION_AVAILABLE:
        #     try:
        #         # Register with memory detector for leak detection
        #         memory_detector().register_object(self)
        #         logger.debug(
        #             f"Component registered with Qt integration: {self.__class__.__name__}"
        #         )
        #     except Exception as e:
        #         logger.debug(f"Qt integration registration failed: {e}")

        # Initialize event system if available
        self._initialize_event_system()

        logger.debug(f"Created component {self.__class__.__name__}")

    def _initialize_event_system(self) -> None:
        """Initialize event system integration if available."""
        if EVENT_SYSTEM_AVAILABLE and IEventBus:
            try:
                self.event_bus = self.container.resolve(IEventBus)
                logger.debug(f"Event system initialized for {self.__class__.__name__}")
            except Exception as e:
                logger.debug(
                    f"Event system not available for {self.__class__.__name__}: {e}"
                )
                self.event_bus = None
        else:
            logger.debug(f"Event system not available for {self.__class__.__name__}")

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the component.

        This method MUST be implemented by all components.
        It should:
        1. Resolve dependencies from container
        2. Set up the component's widget
        3. Configure event handlers
        4. Set _initialized = True
        5. Emit component_ready signal

        NEVER access global state or main widget - use dependency injection only.
        """
        pass

    @abstractmethod
    def get_widget(self) -> QWidget:
        """
        Get the main widget for this component.

        This method MUST be implemented by all components.
        It should return the QWidget that represents this component in the UI.

        Returns:
            QWidget: The main widget for this component
        """
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if the component has been initialized."""
        return self._initialized

    @property
    def widget(self) -> Optional[QWidget]:
        """Get the component's widget (read-only property)."""
        return self._widget

    def cleanup(self) -> None:
        """
        Clean up component resources.

        This method is called when the component is being destroyed.
        It handles:
        1. Widget cleanup
        2. Event unsubscription
        3. Resource deallocation
        4. Custom cleanup handlers

        Components can override this to add custom cleanup logic.
        """
        logger.debug(f"Cleaning up component {self.__class__.__name__}")

        # Run custom cleanup handlers
        for handler in reversed(self._cleanup_handlers):
            try:
                handler()
            except Exception as e:
                logger.error(
                    f"Error in cleanup handler for {self.__class__.__name__}: {e}"
                )

        # Clean up widget
        if self._widget:
            try:
                self._widget.deleteLater()
                self._widget = None
            except Exception as e:
                logger.error(
                    f"Error cleaning up widget for {self.__class__.__name__}: {e}"
                )

        # Clear state
        self._initialized = False
        self._cleanup_handlers.clear()

    def add_cleanup_handler(self, handler: callable) -> None:
        """
        Add a custom cleanup handler.

        Args:
            handler: Callable to be executed during cleanup
        """
        self._cleanup_handlers.append(handler)

    def emit_error(self, message: str, exception: Optional[Exception] = None) -> None:
        """
        Emit component error signal with proper logging.

        Args:
            message: Error message
            exception: Optional exception that caused the error
        """
        full_message = f"{self.__class__.__name__}: {message}"
        if exception:
            full_message += f" ({exception})"
            logger.error(full_message, exc_info=exception)
        else:
            logger.error(full_message)

        self.component_error.emit(full_message)

    def publish_event(self, event: Any) -> None:
        """
        Publish an event via the event bus if available.

        Args:
            event: Event to publish
        """
        if self.event_bus and EVENT_SYSTEM_AVAILABLE:
            try:
                self.event_bus.publish(event)
            except Exception as e:
                logger.error(
                    f"Failed to publish event from {self.__class__.__name__}: {e}"
                )
        else:
            logger.debug(f"Event bus not available for {self.__class__.__name__}")

    def resolve_service(self, service_type: type) -> Any:
        """
        Resolve a service from the container with error handling.

        Args:
            service_type: Type of service to resolve

        Returns:
            Resolved service instance

        Raises:
            RuntimeError: If service cannot be resolved
        """
        try:
            return self.container.resolve(service_type)
        except Exception as e:
            error_msg = f"Failed to resolve {service_type.__name__} in {self.__class__.__name__}"
            self.emit_error(error_msg, e)
            raise RuntimeError(error_msg) from e

    def set_enabled(self, enabled: bool) -> None:
        """
        Enable or disable the component.

        Args:
            enabled: Whether the component should be enabled
        """
        if self._widget:
            self._widget.setEnabled(enabled)

    def set_visible(self, visible: bool) -> None:
        """
        Show or hide the component.

        Args:
            visible: Whether the component should be visible
        """
        if self._widget:
            self._widget.setVisible(visible)

    def get_size(self) -> tuple[int, int]:
        """
        Get component size.

        Returns:
            Tuple of (width, height)
        """
        if self._widget:
            return (self._widget.width(), self._widget.height())
        return (0, 0)

    def __str__(self) -> str:
        """String representation of the component."""
        status = "initialized" if self._initialized else "not initialized"
        return f"{self.__class__.__name__}({status})"

    def __repr__(self) -> str:
        """Detailed string representation of the component."""
        return (
            f"{self.__class__.__name__}("
            f"initialized={self._initialized}, "
            f"has_widget={self._widget is not None}, "
            f"has_event_bus={self.event_bus is not None}"
            f")"
        )


class AsyncViewableComponentBase(ViewableComponentBase):
    """
    Async-capable component base for components that need async initialization.

    This extends ViewableComponentBase to support asynchronous operations
    during initialization and cleanup.
    """

    async def async_initialize(self) -> None:
        """
        Async initialization method.

        Components that need async initialization should override this method
        instead of initialize().
        """
        pass

    async def async_cleanup(self) -> None:
        """
        Async cleanup method.

        Components that need async cleanup should override this method.
        """
        pass


# Convenience type aliases
ComponentBase = ViewableComponentBase
IComponent = ViewableComponentBase  # Interface-style alias
