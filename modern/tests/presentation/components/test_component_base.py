"""
Comprehensive Tests for ViewableComponentBase

This test suite validates the foundational component architecture that enables
world-class software design patterns.

Tests cover:
- Abstract method enforcement
- Dependency injection integration
- Component lifecycle management
- Signal system functionality
- Error handling and recovery
- Memory management
- Event-driven communication
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from presentation.components import ViewableComponentBase, AsyncViewableComponentBase
from core.dependency_injection.di_container import DIContainer


# Mock Qt classes to avoid DLL issues in testing
class MockQWidget:
    def __init__(self):
        self._enabled = True
        self._visible = True
        self._width = 800
        self._height = 600

    def setEnabled(self, enabled):
        self._enabled = enabled

    def isEnabled(self):
        return self._enabled

    def setVisible(self, visible):
        self._visible = visible

    def isVisible(self):
        return self._visible

    def width(self):
        return self._width

    def height(self):
        return self._height

    def resize(self, width, height):
        self._width = width
        self._height = height

    def deleteLater(self):
        pass


class MockQApplication:
    @staticmethod
    def instance():
        return MockQApplication()


# Patch Qt imports
sys.modules["PyQt6.QtWidgets"] = Mock()
sys.modules["PyQt6.QtWidgets"].QWidget = MockQWidget
sys.modules["PyQt6.QtWidgets"].QApplication = MockQApplication
sys.modules["PyQt6.QtCore"] = Mock()


class TestViewableComponentBase:
    """Test suite for ViewableComponentBase functionality."""

    @pytest.fixture
    def app(self):
        """Create mock QApplication for Qt widget tests."""
        app = MockQApplication.instance()
        yield app

    @pytest.fixture
    def container(self):
        """Create a fresh DI container for each test."""
        return DIContainer()

    @pytest.fixture
    def mock_service(self):
        """Create a mock service for dependency injection testing."""

        class MockService:
            def get_data(self):
                return "mock_data"

        return MockService

    def test_abstract_class_cannot_be_instantiated(self, container):
        """Test that ViewableComponentBase cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            ViewableComponentBase(container)

    def test_concrete_implementation_requires_abstract_methods(self, container):
        """Test that concrete implementations must implement abstract methods."""

        # Missing both abstract methods
        class IncompleteComponent(ViewableComponentBase):
            pass

        with pytest.raises(TypeError):
            IncompleteComponent(container)

        # Missing get_widget method
        class PartialComponent(ViewableComponentBase):
            def initialize(self):
                pass

        with pytest.raises(TypeError):
            PartialComponent(container)

    def test_complete_implementation_works(self, app, container):
        """Test that complete implementation can be instantiated."""

        class CompleteComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockMockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

        component = CompleteComponent(container)
        assert component is not None
        assert not component.is_initialized
        assert component.container is container

    def test_component_lifecycle(self, app, container):
        """Test complete component lifecycle: create -> initialize -> cleanup."""

        class TestComponent(ViewableComponentBase):
            def __init__(self, container, parent=None):
                super().__init__(container, parent)
                self.initialize_called = False
                self.cleanup_called = False

            def initialize(self):
                self.initialize_called = True
                self._widget = MockMockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                if not self._widget:
                    raise RuntimeError("Component not initialized")
                return self._widget

            def cleanup(self):
                self.cleanup_called = True
                super().cleanup()

        # Test creation
        component = TestComponent(container)
        assert not component.is_initialized
        assert not component.initialize_called

        # Test initialization
        component.initialize()
        assert component.is_initialized
        assert component.initialize_called

        # Test widget access
        widget = component.get_widget()
        assert widget is not None
        assert isinstance(widget, MockQWidget)

        # Test cleanup
        component.cleanup()
        assert component.cleanup_called
        assert not component.is_initialized

    def test_dependency_injection_integration(self, app, container, mock_service):
        """Test that dependency injection works correctly."""

        # Register service in container
        container.register_singleton(type(mock_service), lambda: mock_service)

        class DIComponent(ViewableComponentBase):
            def initialize(self):
                # Test service resolution
                self.service = self.resolve_service(type(mock_service))
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

        component = DIComponent(container)
        component.initialize()

        assert hasattr(component, "service")
        assert component.service is mock_service
        assert component.service.get_data() == "mock_data"

    def test_signal_system_functionality(self, app, container):
        """Test that component signals work correctly."""

        class SignalComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

            def trigger_error(self):
                self.emit_error("Test error")

            def trigger_data_change(self):
                self.data_changed.emit({"test": "data"})

            def trigger_state_change(self):
                self.state_changed.emit("test_state", "new_value")

        component = SignalComponent(container)

        # Test signal connections
        ready_received = []
        error_received = []
        data_received = []
        state_received = []

        component.component_ready.connect(lambda: ready_received.append(True))
        component.component_error.connect(lambda msg: error_received.append(msg))
        component.data_changed.connect(lambda data: data_received.append(data))
        component.state_changed.connect(
            lambda state, value: state_received.append((state, value))
        )

        # Test signal emissions
        component.initialize()
        assert len(ready_received) == 1

        component.trigger_error()
        assert len(error_received) == 1
        assert "Test error" in error_received[0]

        component.trigger_data_change()
        assert len(data_received) == 1
        assert data_received[0] == {"test": "data"}

        component.trigger_state_change()
        assert len(state_received) == 1
        assert state_received[0] == ("test_state", "new_value")

    def test_error_handling_and_recovery(self, app, container):
        """Test error handling and recovery mechanisms."""

        class ErrorComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

            def cause_error(self):
                try:
                    raise ValueError("Test error")
                except Exception as e:
                    self.emit_error("Component error occurred", e)

        component = ErrorComponent(container)
        component.initialize()

        # Test error emission
        error_messages = []
        component.component_error.connect(lambda msg: error_messages.append(msg))

        component.cause_error()
        assert len(error_messages) == 1
        assert "ErrorComponent: Component error occurred" in error_messages[0]
        assert "ValueError" in error_messages[0]

    def test_memory_management(self, app, container):
        """Test memory management and cleanup."""

        class MemoryComponent(ViewableComponentBase):
            def __init__(self, container, parent=None):
                super().__init__(container, parent)
                self.cleanup_handlers_called = []

            def initialize(self):
                self._widget = MockQWidget()

                # Add cleanup handlers
                self.add_cleanup_handler(
                    lambda: self.cleanup_handlers_called.append("handler1")
                )
                self.add_cleanup_handler(
                    lambda: self.cleanup_handlers_called.append("handler2")
                )

                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

        component = MemoryComponent(container)
        component.initialize()

        # Verify widget exists
        assert component.widget is not None

        # Test cleanup
        component.cleanup()

        # Verify cleanup handlers were called
        assert len(component.cleanup_handlers_called) == 2
        assert "handler1" in component.cleanup_handlers_called
        assert "handler2" in component.cleanup_handlers_called

        # Verify state is reset
        assert not component.is_initialized
        assert component.widget is None

    def test_service_resolution_error_handling(self, app, container):
        """Test error handling when service resolution fails."""

        class ServiceErrorComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

            def try_resolve_missing_service(self):
                return self.resolve_service(str)  # String type not registered

        component = ServiceErrorComponent(container)
        component.initialize()

        # Test that service resolution error is handled properly
        with pytest.raises(RuntimeError, match="Failed to resolve str"):
            component.try_resolve_missing_service()

    def test_widget_utility_methods(self, app, container):
        """Test widget utility methods."""

        class UtilityComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._widget.resize(800, 600)
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

        component = UtilityComponent(container)
        component.initialize()

        # Test size methods
        width, height = component.get_size()
        assert width == 800
        assert height == 600

        # Test enable/disable
        component.set_enabled(False)
        assert not component.widget.isEnabled()

        component.set_enabled(True)
        assert component.widget.isEnabled()

        # Test visibility
        component.set_visible(False)
        assert not component.widget.isVisible()

        component.set_visible(True)
        assert component.widget.isVisible()

    def test_string_representations(self, app, container):
        """Test string representation methods."""

        class StringComponent(ViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

        component = StringComponent(container)

        # Test before initialization
        str_repr = str(component)
        assert "StringComponent" in str_repr
        assert "not initialized" in str_repr

        # Test after initialization
        component.initialize()
        str_repr = str(component)
        assert "StringComponent" in str_repr
        assert "initialized" in str_repr

        # Test detailed representation
        repr_str = repr(component)
        assert "StringComponent" in repr_str
        assert "initialized=True" in repr_str
        assert "has_widget=True" in repr_str


class TestAsyncViewableComponentBase:
    """Test suite for AsyncViewableComponentBase functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for Qt widget tests."""
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        yield app

    @pytest.fixture
    def container(self):
        """Create a fresh DI container for each test."""
        return DIContainer()

    def test_async_component_inheritance(self, app, container):
        """Test that AsyncViewableComponentBase inherits from ViewableComponentBase."""

        class AsyncComponent(AsyncViewableComponentBase):
            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

            async def async_initialize(self):
                # Simulate async initialization
                pass

            async def async_cleanup(self):
                # Simulate async cleanup
                pass

        component = AsyncComponent(container)
        assert isinstance(component, ViewableComponentBase)
        assert hasattr(component, "async_initialize")
        assert hasattr(component, "async_cleanup")

    @pytest.mark.asyncio
    async def test_async_methods(self, app, container):
        """Test async initialization and cleanup methods."""

        class AsyncComponent(AsyncViewableComponentBase):
            def __init__(self, container, parent=None):
                super().__init__(container, parent)
                self.async_init_called = False
                self.async_cleanup_called = False

            def initialize(self):
                self._widget = MockQWidget()
                self._initialized = True
                self.component_ready.emit()

            def get_widget(self):
                return self._widget

            async def async_initialize(self):
                self.async_init_called = True

            async def async_cleanup(self):
                self.async_cleanup_called = True

        component = AsyncComponent(container)
        component.initialize()

        # Test async methods
        await component.async_initialize()
        assert component.async_init_called

        await component.async_cleanup()
        assert component.async_cleanup_called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
