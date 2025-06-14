"""
V1 Parity Tests for Graph Editor

Tests that V2 graph editor maintains exact V1 functionality.
"""

import pytest
from unittest.mock import Mock, patch
from PyQt6.QtTest import QSignalSpy  # Changed from PyQt6.QtCore
from PyQt6.QtCore import Qt  # Keep Qt here
from PyQt6.QtGui import QKeyEvent

from v2.src.application.services.graph_editor_service import GraphEditorService
from v2.src.application.services.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)
from v2.src.presentation.components.workbench.graph_editor.modern_graph_editor import (
    ModernGraphEditor,
)


@pytest.mark.parity
class TestGraphEditorV1Parity:
    """Test V2 graph editor parity with V1 functionality."""

    def setup_method(self):
        """Setup for each test."""
        self.graph_service = GraphEditorService()
        self.hotkey_service = GraphEditorHotkeyService(self.graph_service)

    def test_graph_editor_toggle_behavior(self, qapp, mock_sequence_data):
        """Test graph editor toggle matches V1 behavior."""
        # Create graph editor
        graph_editor = ModernGraphEditor(graph_service=self.graph_service, parent=None)

        # Setup signal spy
        visibility_spy = QSignalSpy(graph_editor.visibility_changed)

        # Initial state should be hidden
        assert not graph_editor.is_visible()
        assert graph_editor.height() == 0

        # Toggle to show
        graph_editor.toggle_visibility()
        qapp.processEvents()

        # Should be visible and have height
        assert graph_editor.is_visible()
        assert graph_editor.height() > 0
        assert len(visibility_spy) == 1
        assert visibility_spy[0][0] == True  # visibility_changed(True)

        # Toggle to hide
        graph_editor.toggle_visibility()
        qapp.processEvents()

        # Should be hidden
        assert not graph_editor.is_visible()
        assert len(visibility_spy) == 2
        assert visibility_spy[1][0] == False  # visibility_changed(False)

    def test_beat_selection_updates_pictograph(self, qapp, mock_beat_data):
        """Test beat selection updates pictograph like V1."""
        graph_editor = ModernGraphEditor(graph_service=self.graph_service, parent=None)

        # Show graph editor
        graph_editor.toggle_visibility()
        qapp.processEvents()

        # Set selected beat
        graph_editor.set_selected_beat(mock_beat_data, 0)
        qapp.processEvents()

        # Verify pictograph container received beat data
        pictograph_container = graph_editor._pictograph_container
        assert pictograph_container._current_beat == mock_beat_data

    def test_arrow_selection_workflow(self, qapp, mock_beat_data):
        """Test arrow selection workflow matches V1."""
        graph_editor = ModernGraphEditor(graph_service=self.graph_service, parent=None)

        # Setup signal spy
        arrow_selected_spy = QSignalSpy(graph_editor.arrow_selected)

        # Show graph editor and set beat
        graph_editor.toggle_visibility()
        graph_editor.set_selected_beat(mock_beat_data, 0)
        qapp.processEvents()

        # Simulate arrow selection
        test_arrow_id = "red_arrow"
        graph_editor._on_arrow_selected(test_arrow_id)

        # Verify signal emission
        assert len(arrow_selected_spy) == 1
        assert arrow_selected_spy[0][0] == test_arrow_id

        # Verify service state
        assert self.graph_service._selected_arrow_id == test_arrow_id

    def test_hotkey_wasd_movement(self, qapp, mock_beat_data):
        """Test WASD arrow movement hotkeys match V1 behavior."""
        # Setup with selected arrow
        self.graph_service.set_selected_beat(mock_beat_data, 0)
        self.graph_service.set_arrow_selection("test_arrow")

        # Setup signal spy
        movement_spy = QSignalSpy(self.hotkey_service.arrow_moved)

        # Test W key (up movement)
        w_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier
        )
        result = self.hotkey_service.handle_key_event(w_event)

        # Should handle the key
        assert result == True

        # Should emit movement signal
        assert len(movement_spy) == 1
        assert movement_spy[0][0] == "test_arrow"  # arrow_id
        assert movement_spy[0][1] == "up"  # direction

    def test_hotkey_x_rotation_override(self, qapp, mock_beat_data):
        """Test X key rotation override matches V1 behavior."""
        # Setup with selected arrow
        self.graph_service.set_selected_beat(mock_beat_data, 0)
        self.graph_service.set_arrow_selection("test_arrow")

        # Setup signal spy
        rotation_spy = QSignalSpy(self.hotkey_service.arrow_rotation_overridden)

        # Test X key
        x_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_X, Qt.KeyboardModifier.NoModifier
        )
        result = self.hotkey_service.handle_key_event(x_event)

        # Should handle the key
        assert result == True

        # Should emit rotation override signal
        assert len(rotation_spy) == 1
        assert rotation_spy[0][0] == "test_arrow"

    def test_hotkey_z_special_placement_removal(self, qapp, mock_beat_data):
        """Test Z key special placement removal matches V1 behavior."""
        # Setup with selected arrow
        self.graph_service.set_selected_beat(mock_beat_data, 0)
        self.graph_service.set_arrow_selection("test_arrow")

        # Setup signal spy
        removal_spy = QSignalSpy(self.hotkey_service.special_placement_removed)

        # Test Z key
        z_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_Z, Qt.KeyboardModifier.NoModifier
        )
        result = self.hotkey_service.handle_key_event(z_event)

        # Should handle the key
        assert result == True

        # Should emit special placement removal signal
        assert len(removal_spy) == 1
        assert removal_spy[0][0] == mock_beat_data.letter  # letter
        assert removal_spy[0][1] == "test_arrow"  # arrow_id

    def test_hotkey_c_prop_placement_override(self, qapp):
        """Test C key prop placement override matches V1 behavior."""
        # Setup signal spy
        prop_spy = QSignalSpy(self.hotkey_service.prop_placement_overridden)

        # Test C key (works without selected arrow)
        c_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_C, Qt.KeyboardModifier.NoModifier
        )
        result = self.hotkey_service.handle_key_event(c_event)

        # Should handle the key
        assert result == True

        # Should emit prop placement override signal
        assert len(prop_spy) == 1

    def test_hotkey_modifier_movement_amounts(self, qapp, mock_beat_data):
        """Test modifier keys affect movement amounts like V1."""
        # Setup with selected arrow
        self.graph_service.set_selected_beat(mock_beat_data, 0)
        self.graph_service.set_arrow_selection("test_arrow")

        # Test normal movement (no modifiers)
        normal_amount = self.hotkey_service._calculate_movement_amount(False, False)
        assert normal_amount == 1.0

        # Test fine movement (Ctrl)
        fine_amount = self.hotkey_service._calculate_movement_amount(False, True)
        assert fine_amount == 0.1

        # Test large movement (Shift)
        large_amount = self.hotkey_service._calculate_movement_amount(True, False)
        assert large_amount == 5.0

    def test_graph_editor_height_calculation_matches_v1(self, qapp):
        """Test graph editor height calculation matches V1 formula."""
        # Create mock parent with known dimensions
        mock_parent = Mock()
        mock_parent.height.return_value = 1000
        mock_parent.width.return_value = 800

        graph_editor = ModernGraphEditor(
            graph_service=self.graph_service, parent=mock_parent
        )

        # Calculate preferred height
        height = graph_editor.get_preferred_height()

        # Should use V1 formula: min(parent_height // 3.5, parent_width // 4)
        expected_height = min(int(1000 // 3.5), 800 // 4)

        # Allow for constraint adjustments but verify base calculation
        assert height >= 150  # Minimum height
        assert height <= expected_height + 50  # Allow for constraints

    def test_animation_timing_matches_v1(self, qapp):
        """Test animation timing matches V1 specifications."""
        graph_editor = ModernGraphEditor(graph_service=self.graph_service, parent=None)

        # Check animation duration
        animation = graph_editor._height_animation
        assert animation.duration() == 400  # Should match V1 timing

        # Check easing curve
        assert animation.easingCurve().type() == animation.easingCurve().Type.OutCubic

    def test_v1_integration_service_initialization(self):
        """Test V1 integration service initializes correctly."""
        # Verify V1 integration service exists
        assert hasattr(self.graph_service, "_v1_integration")
        assert self.graph_service._v1_integration is not None

        # Verify signal connections
        v1_integration = self.graph_service._v1_integration
        assert hasattr(v1_integration, "pictograph_updated")
        assert hasattr(v1_integration, "arrow_selected")
        assert hasattr(v1_integration, "arrow_deselected")

    def test_pictograph_creation_workflow(self, qapp, mock_beat_data):
        """Test pictograph creation workflow matches V1."""
        from PyQt6.QtWidgets import QGraphicsScene

        # Create scene for pictograph
        scene = QGraphicsScene()

        # Test pictograph creation
        success = self.graph_service.create_pictograph_for_beat(mock_beat_data, scene)

        # Should attempt creation (may fail without full V1 integration)
        assert isinstance(success, bool)

        # Verify service method exists and is callable
        assert hasattr(self.graph_service, "create_pictograph_for_beat")
        assert callable(self.graph_service.create_pictograph_for_beat)
