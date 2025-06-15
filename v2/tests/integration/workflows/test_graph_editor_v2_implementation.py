"""
Integration tests for V2 Graph Editor implementation.

Tests the complete V2 graph editor functionality including:
- V2 native pictograph rendering
- Functional adjustment panels
- Turn selection dialog
- Hotkey system integration
"""

import pytest
from unittest.mock import Mock, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from src.presentation.components.workbench.graph_editor.modern_graph_editor import (
    ModernGraphEditor,
)
from src.presentation.components.workbench.graph_editor.modern_pictograph_container import (
    ModernPictographContainer,
)
from src.presentation.components.workbench.graph_editor.modern_adjustment_panel import (
    ModernAdjustmentPanel,
)
from src.presentation.components.workbench.graph_editor.turn_selection_dialog import (
    TurnSelectionDialog,
)
from src.application.services.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)
from src.domain.models.core_models import BeatData, MotionData, MotionType, Location


@pytest.fixture
def app():
    """Create QApplication for testing."""
    return QApplication.instance() or QApplication([])


@pytest.fixture
def mock_graph_service():
    """Create mock graph editor service."""
    service = Mock()
    service.get_selected_arrow.return_value = "blue"
    service.get_selected_beat.return_value = None
    service.apply_turn_adjustment.return_value = True
    service.apply_orientation_adjustment.return_value = True
    service.update_arrow_position.return_value = True
    service.update_arrow_rotation.return_value = True
    service.set_arrow_selection.return_value = None
    service.update_graph_display.return_value = None
    service.set_selected_beat.return_value = None
    service.update_beat_adjustments.return_value = None
    return service


@pytest.fixture
def sample_beat_data():
    """Create real sample beat data using PictographDatasetService."""
    from application.services.data.pictograph_dataset_service import (
        PictographDatasetService,
    )
    from src.domain.models.core_models import BeatData

    dataset_service = PictographDatasetService()
    beat_data = dataset_service.get_start_position_pictograph(
        "alpha1_alpha1", "diamond"
    )

    # Fallback to empty beat if dataset unavailable
    if not beat_data:
        beat_data = BeatData.empty().update(letter="A")

    return beat_data


class TestModernPictographContainer:
    """Test V2 native pictograph container."""

    def test_pictograph_container_creation(self, app, mock_graph_service):
        """Test pictograph container can be created."""
        parent = Mock()
        parent._graph_editor = Mock()
        parent._graph_editor._graph_service = mock_graph_service

        container = ModernPictographContainer(parent)
        assert container is not None
        assert hasattr(container, "_pictograph_service")

    def test_set_beat_data(self, app, mock_graph_service, sample_beat_data):
        """Test setting beat data on pictograph container."""
        parent = Mock()
        parent._graph_editor = Mock()
        parent._graph_editor._graph_service = mock_graph_service

        container = ModernPictographContainer(parent)
        container.set_beat(sample_beat_data)

        assert container._current_beat == sample_beat_data

    def test_arrow_selection_signal(self, app, mock_graph_service):
        """Test arrow selection signal emission."""
        parent = Mock()
        parent._graph_editor = Mock()
        parent._graph_editor._graph_service = mock_graph_service

        container = ModernPictographContainer(parent)

        # Mock signal connection
        signal_received = []
        container.arrow_selected.connect(
            lambda arrow_id: signal_received.append(arrow_id)
        )

        # Simulate arrow click
        container._on_arrow_clicked("blue")

        assert "blue" in signal_received


class TestModernAdjustmentPanel:
    """Test functional adjustment panels."""

    def test_adjustment_panel_creation(self, app, mock_graph_service):
        """Test adjustment panel can be created."""
        parent = Mock()
        parent._graph_service = mock_graph_service

        panel = ModernAdjustmentPanel(parent, side="left")
        assert panel is not None
        assert panel._side == "left"

    def test_turn_value_retrieval(self, app, mock_graph_service, sample_beat_data):
        """Test getting current turn values from beat data."""
        parent = Mock()
        parent._graph_service = mock_graph_service

        panel = ModernAdjustmentPanel(parent, side="left")
        panel.set_beat(sample_beat_data)

        blue_turns = panel._get_current_turn_value("blue")
        red_turns = panel._get_current_turn_value("red")

        assert blue_turns == 1.0
        assert red_turns == 0.5

    def test_turn_application(self, app, mock_graph_service):
        """Test applying turn values through service."""
        parent = Mock()
        parent._graph_service = mock_graph_service

        panel = ModernAdjustmentPanel(parent, side="left")

        # Test turn application
        panel._apply_turn("blue", 2.0)

        mock_graph_service.apply_turn_adjustment.assert_called_with("blue", 2.0)

    def test_orientation_application(self, app, mock_graph_service):
        """Test applying orientation values through service."""
        parent = Mock()
        parent._graph_service = mock_graph_service

        panel = ModernAdjustmentPanel(parent, side="right")

        # Test orientation application
        panel._apply_orientation("red", "clock")

        mock_graph_service.apply_orientation_adjustment.assert_called_with(
            "red", "clock"
        )


class TestTurnSelectionDialog:
    """Test turn selection dialog."""

    def test_dialog_creation(self, app):
        """Test turn selection dialog can be created."""
        dialog = TurnSelectionDialog(current_turn=1.5, arrow_color="blue")
        assert dialog is not None
        assert dialog._current_turn == 1.5
        assert dialog._arrow_color == "blue"

    def test_turn_values_available(self, app):
        """Test all expected turn values are available."""
        dialog = TurnSelectionDialog()
        expected_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        assert dialog._turn_values == expected_values

    def test_static_method(self, app):
        """Test static method for getting turn value."""
        # This would normally show a dialog, but we can test the method exists
        assert hasattr(TurnSelectionDialog, "get_turn_value")
        assert callable(TurnSelectionDialog.get_turn_value)


class TestGraphEditorHotkeyService:
    """Test hotkey system integration."""

    def test_hotkey_service_creation(self, app, mock_graph_service):
        """Test hotkey service can be created."""
        service = GraphEditorHotkeyService(mock_graph_service)
        assert service is not None
        assert service._graph_service == mock_graph_service

    def test_movement_key_mapping(self, app, mock_graph_service):
        """Test WASD key mappings are correct."""
        service = GraphEditorHotkeyService(mock_graph_service)

        expected_mappings = {
            Qt.Key.Key_W: "up",
            Qt.Key.Key_A: "left",
            Qt.Key.Key_S: "down",
            Qt.Key.Key_D: "right",
        }

        assert service._movement_keys == expected_mappings

    def test_movement_amount_calculation(self, app, mock_graph_service):
        """Test movement amount calculation with modifiers."""
        service = GraphEditorHotkeyService(mock_graph_service)

        # Normal movement
        assert service._calculate_movement_amount(False, False) == 1.0

        # Fine movement (Ctrl)
        assert service._calculate_movement_amount(False, True) == 0.1

        # Large movement (Shift)
        assert service._calculate_movement_amount(True, False) == 5.0

    def test_rotation_override_angles(self, app, mock_graph_service):
        """Test rotation override cycles through correct angles."""
        service = GraphEditorHotkeyService(mock_graph_service)

        # Test cycling through angles
        properties = {"rotation": 0.0}
        new_props = service._apply_rotation_override(properties)
        assert new_props["rotation"] == 45

        properties = {"rotation": 315.0}
        new_props = service._apply_rotation_override(properties)
        assert new_props["rotation"] == 0  # Cycles back to start


class TestModernGraphEditor:
    """Test complete graph editor integration."""

    def test_graph_editor_creation(self, app, mock_graph_service):
        """Test graph editor can be created with all components."""
        editor = ModernGraphEditor(mock_graph_service)
        assert editor is not None
        assert editor._graph_service == mock_graph_service
        assert editor._pictograph_container is not None
        assert editor._left_adjustment_panel is not None
        assert editor._right_adjustment_panel is not None

    def test_focus_policy_set(self, app, mock_graph_service):
        """Test graph editor has focus policy for hotkeys."""
        editor = ModernGraphEditor(mock_graph_service)
        assert editor.focusPolicy() == Qt.FocusPolicy.StrongFocus

    def test_beat_data_propagation(self, app, mock_graph_service, sample_beat_data):
        """Test beat data is properly propagated to components."""
        editor = ModernGraphEditor(mock_graph_service)
        editor.set_selected_beat(sample_beat_data, 0)

        assert editor._selected_beat == sample_beat_data
        assert editor._selected_beat_index == 0

    def test_arrow_selection_propagation(self, app, mock_graph_service):
        """Test arrow selection is properly propagated."""
        editor = ModernGraphEditor(mock_graph_service)

        # Simulate arrow selection
        editor._on_arrow_selected("red")

        assert editor._selected_arrow_id == "red"
        mock_graph_service.set_arrow_selection.assert_called_with("red")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
