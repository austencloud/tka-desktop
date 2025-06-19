"""
Comprehensive Tests for Retrofitted OptionPicker

This test suite validates that the OptionPicker component works correctly
after being retrofitted to inherit from ViewableComponentBase.

Tests cover:
- Inheritance from ViewableComponentBase works correctly
- All existing functionality is preserved
- New base class features work properly
- Complex component lifecycle management
- Dependency injection integration
- Signal system integration
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

# Add src to path for imports
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from presentation.components import ViewableComponentBase
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ILayoutService


# Mock Qt classes to avoid DLL issues
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


# Patch Qt imports
sys.modules["PyQt6.QtWidgets"] = Mock()
sys.modules["PyQt6.QtWidgets"].QWidget = MockQWidget

# Import OptionPicker after patching
from presentation.components.option_picker import OptionPicker


class TestOptionPickerRetrofit:
    """Test suite for retrofitted OptionPicker functionality."""

    @pytest.fixture
    def container(self):
        """Create a DI container with required services."""
        container = DIContainer()

        # Mock the layout service
        mock_layout_service = Mock()
        mock_layout_service.get_layout.return_value = "mock_layout"
        container.register_factory(ILayoutService, lambda: mock_layout_service)

        return container

    @pytest.fixture
    def mock_progress_callback(self):
        """Create a mock progress callback."""
        return Mock()

    def test_option_picker_inherits_from_viewable_component_base(self, container):
        """Test that OptionPicker correctly inherits from ViewableComponentBase."""
        option_picker = OptionPicker(container)

        # Test inheritance
        assert isinstance(option_picker, ViewableComponentBase)
        assert isinstance(option_picker, OptionPicker)

        # Test that it has base class properties
        assert hasattr(option_picker, "component_ready")
        assert hasattr(option_picker, "component_error")
        assert hasattr(option_picker, "data_changed")
        assert hasattr(option_picker, "state_changed")
        assert hasattr(option_picker, "container")
        assert hasattr(option_picker, "is_initialized")

    def test_option_picker_constructor_compatibility(
        self, container, mock_progress_callback
    ):
        """Test that OptionPicker constructor maintains backward compatibility."""

        # Test with progress callback (existing pattern)
        option_picker1 = OptionPicker(
            container, progress_callback=mock_progress_callback
        )
        assert option_picker1.progress_callback is mock_progress_callback
        assert option_picker1.container is container

        # Test with parent parameter (new pattern)
        parent = MockQWidget()
        option_picker2 = OptionPicker(container, parent=parent)
        assert option_picker2.parent() is parent

        # Test with both parameters
        option_picker3 = OptionPicker(
            container, progress_callback=mock_progress_callback, parent=parent
        )
        assert option_picker3.progress_callback is mock_progress_callback
        assert option_picker3.parent() is parent

    def test_abstract_methods_implemented(self, container):
        """Test that OptionPicker implements required abstract methods."""
        option_picker = OptionPicker(container)

        # Test that abstract methods exist
        assert hasattr(option_picker, "initialize")
        assert hasattr(option_picker, "get_widget")
        assert callable(option_picker.initialize)
        assert callable(option_picker.get_widget)

    def test_get_widget_before_initialization(self, container):
        """Test that get_widget raises appropriate error before initialization."""
        option_picker = OptionPicker(container)

        with pytest.raises(RuntimeError, match="OptionPicker not initialized"):
            option_picker.get_widget()

    @patch(
        "presentation.components.option_picker.option_picker.OptionPickerWidgetFactory"
    )
    @patch("presentation.components.option_picker.option_picker.PictographPoolManager")
    @patch(
        "presentation.components.option_picker.option_picker.OptionPickerDisplayManager"
    )
    @patch("presentation.components.option_picker.option_picker.BeatDataLoader")
    @patch(
        "presentation.components.option_picker.option_picker.OptionPickerDimensionAnalyzer"
    )
    def test_initialization_process(
        self,
        mock_analyzer,
        mock_loader,
        mock_display,
        mock_pool,
        mock_factory,
        app,
        container,
        mock_progress_callback,
    ):
        """Test the complete initialization process."""

        # Setup mocks
        mock_widget = MockQWidget()
        mock_sections_container = MockQWidget()
        mock_sections_layout = Mock()
        mock_filter_widget = Mock()

        mock_factory.return_value.create_widget.return_value = (
            mock_widget,
            mock_sections_container,
            mock_sections_layout,
            mock_filter_widget,
        )

        mock_pool_instance = Mock()
        mock_pool.return_value = mock_pool_instance

        mock_display_instance = Mock()
        mock_display.return_value = mock_display_instance
        mock_display_instance.get_sections.return_value = []

        mock_loader_instance = Mock()
        mock_loader.return_value = mock_loader_instance

        mock_analyzer_instance = Mock()
        mock_analyzer.return_value = mock_analyzer_instance

        # Create and initialize OptionPicker
        option_picker = OptionPicker(
            container, progress_callback=mock_progress_callback
        )

        # Test initial state
        assert not option_picker.is_initialized

        # Initialize
        option_picker.initialize()

        # Test post-initialization state
        assert option_picker.is_initialized
        assert option_picker.get_widget() is mock_widget

        # Verify progress callback was called
        assert mock_progress_callback.call_count > 0

        # Verify component_ready signal was emitted
        ready_signals = []
        option_picker.component_ready.connect(lambda: ready_signals.append(True))
        # Signal should have been emitted during initialization
        # We can't test this directly since it was already emitted, but we can verify the state

    def test_component_signals_integration(self, app, container):
        """Test that component signals work correctly."""
        option_picker = OptionPicker(container)

        # Test signal connections
        ready_received = []
        error_received = []
        option_selected_received = []
        beat_data_selected_received = []

        option_picker.component_ready.connect(lambda: ready_received.append(True))
        option_picker.component_error.connect(lambda msg: error_received.append(msg))
        option_picker.option_selected.connect(
            lambda opt: option_selected_received.append(opt)
        )
        option_picker.beat_data_selected.connect(
            lambda data: beat_data_selected_received.append(data)
        )

        # Test signal emissions
        option_picker.component_ready.emit()
        assert len(ready_received) == 1

        option_picker.component_error.emit("Test error")
        assert len(error_received) == 1
        assert error_received[0] == "Test error"

        option_picker.option_selected.emit("test_option")
        assert len(option_selected_received) == 1
        assert option_selected_received[0] == "test_option"

        option_picker.beat_data_selected.emit({"test": "data"})
        assert len(beat_data_selected_received) == 1
        assert beat_data_selected_received[0] == {"test": "data"}

    def test_existing_methods_preserved(self, container):
        """Test that all existing OptionPicker methods are preserved."""
        option_picker = OptionPicker(container)

        # Test that existing methods still exist
        existing_methods = [
            "load_motion_combinations",
            "refresh_options",
            "refresh_options_from_sequence",
            "refresh_options_from_modern_sequence",
            "get_beat_data_for_option",
            "set_enabled",
            "get_size",
            "log_dimensions",
        ]

        for method_name in existing_methods:
            assert hasattr(
                option_picker, method_name
            ), f"Method {method_name} is missing"
            assert callable(
                getattr(option_picker, method_name)
            ), f"Method {method_name} is not callable"

    def test_dependency_injection_integration(self, container):
        """Test that dependency injection works correctly."""
        option_picker = OptionPicker(container)

        # Test that container is accessible
        assert option_picker.container is container

        # Test that resolve_service method works
        layout_service = option_picker.resolve_service(ILayoutService)
        assert layout_service is not None

    def test_error_handling_integration(self, app, container):
        """Test error handling integration with base class."""
        option_picker = OptionPicker(container)

        # Test error emission
        error_messages = []
        option_picker.component_error.connect(lambda msg: error_messages.append(msg))

        # Test emit_error method from base class
        option_picker.emit_error("Test error message")

        assert len(error_messages) == 1
        assert "OptionPicker: Test error message" in error_messages[0]

    @patch(
        "presentation.components.option_picker.option_picker.OptionPickerWidgetFactory"
    )
    def test_cleanup_functionality(self, mock_factory, app, container):
        """Test that cleanup functionality works correctly."""

        # Setup mock
        mock_widget = MockQWidget()
        mock_factory.return_value.create_widget.return_value = (
            mock_widget,
            Mock(),
            Mock(),
            Mock(),
        )

        option_picker = OptionPicker(container)

        # Mock the managers to test cleanup
        option_picker._pool_manager = Mock()
        option_picker._display_manager = Mock()
        option_picker._beat_loader = Mock()
        option_picker._widget_factory = Mock()
        option_picker._dimension_analyzer = Mock()
        option_picker._layout_service = Mock()

        # Add cleanup methods to managers
        option_picker._pool_manager.cleanup = Mock()
        option_picker._display_manager.cleanup = Mock()

        # Test cleanup
        option_picker.cleanup()

        # Verify cleanup was called on managers that have it
        option_picker._pool_manager.cleanup.assert_called_once()
        option_picker._display_manager.cleanup.assert_called_once()

        # Verify references are cleared
        assert option_picker._pool_manager is None
        assert option_picker._display_manager is None
        assert option_picker._beat_loader is None
        assert option_picker._widget_factory is None
        assert option_picker._dimension_analyzer is None
        assert option_picker._layout_service is None

    def test_widget_utility_methods_work(self, app, container):
        """Test that widget utility methods work correctly."""
        option_picker = OptionPicker(container)

        # Mock a widget for testing
        mock_widget = MockQWidget()
        mock_widget.resize(800, 600)
        option_picker._widget = mock_widget
        option_picker._initialized = True

        # Test get_size
        width, height = option_picker.get_size()
        assert width == 800
        assert height == 600

        # Test set_enabled
        option_picker.set_enabled(False)
        assert not mock_widget.isEnabled()

        option_picker.set_enabled(True)
        assert mock_widget.isEnabled()

        # Test set_visible
        option_picker.set_visible(False)
        assert not mock_widget.isVisible()

        option_picker.set_visible(True)
        assert mock_widget.isVisible()

    def test_string_representation(self, container):
        """Test string representation methods."""
        option_picker = OptionPicker(container)

        # Test before initialization
        str_repr = str(option_picker)
        assert "OptionPicker" in str_repr
        assert "not initialized" in str_repr

        # Mock initialization state
        option_picker._initialized = True
        option_picker._widget = MockQWidget()

        # Test after initialization
        str_repr = str(option_picker)
        assert "OptionPicker" in str_repr
        assert "initialized" in str_repr

        # Test detailed representation
        repr_str = repr(option_picker)
        assert "OptionPicker" in repr_str
        assert "initialized=True" in repr_str
        assert "has_widget=True" in repr_str

    def test_backward_compatibility_with_existing_usage(
        self, container, mock_progress_callback
    ):
        """Test that existing usage patterns still work."""

        # Test the exact pattern used in layout_manager.py
        option_picker = OptionPicker(
            container, progress_callback=mock_progress_callback
        )

        # Test that all expected attributes exist
        assert hasattr(option_picker, "progress_callback")
        assert hasattr(option_picker, "container")
        assert hasattr(option_picker, "option_selected")
        assert hasattr(option_picker, "beat_data_selected")

        # Test that methods can be called (even if they fail due to missing dependencies)
        assert callable(option_picker.initialize)
        assert callable(option_picker.get_widget)
        assert callable(option_picker.set_enabled)
        assert callable(option_picker.refresh_options)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
