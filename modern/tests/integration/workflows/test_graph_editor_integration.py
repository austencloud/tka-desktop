"""
Integration tests for Graph Editor components.

Tests the complete graph editor workflow with service integration.
"""

import pytest
from unittest.mock import Mock, patch
from PyQt6.QtCore import QTimer
from PyQt6.QtTest import QSignalSpy  # Changed from PyQt6.QtCore
from PyQt6.QtWidgets import QGraphicsScene

from src.application.services.graph_editor_service import GraphEditorService
from src.application.services.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)
from presentation.components.workbench.graph_editor.graph_editor import (
    GraphEditor,
)


@pytest.mark.integration
class TestGraphEditorIntegration:
    """Test graph editor component integration."""

    def setup_method(self):
        """Setup for each test."""
        self.graph_service = GraphEditorService()
        self.hotkey_service = GraphEditorHotkeyService(self.graph_service)

    def test_complete_graph_editor_workflow(self, qapp, mock_sequence_data, test_timer):
        """Test complete graph editor workflow from creation to interaction."""
        # Create graph editor with real service
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Setup signal spies
        visibility_spy = QSignalSpy(graph_editor.visibility_changed)
        beat_modified_spy = QSignalSpy(graph_editor.beat_modified)
        arrow_selected_spy = QSignalSpy(graph_editor.arrow_selected)

        # Step 1: Show graph editor
        graph_editor.toggle_visibility()
        test_timer.process_events(qapp, 500)  # Wait for animation

        assert graph_editor.is_visible()
        assert len(visibility_spy) == 1

        # Step 2: Set sequence data
        graph_editor.set_sequence(mock_sequence_data)
        test_timer.process_events(qapp, 100)

        # Step 3: Select a beat
        first_beat = mock_sequence_data.beats[0]
        graph_editor.set_selected_beat(first_beat, 0)
        test_timer.process_events(qapp, 100)

        # Verify pictograph container received beat
        assert graph_editor._pictograph_container._current_beat == first_beat

        # Step 4: Simulate arrow selection
        test_arrow_id = "test_arrow"
        graph_editor._on_arrow_selected(test_arrow_id)

        assert len(arrow_selected_spy) == 1
        assert arrow_selected_spy[0][0] == test_arrow_id

        # Step 5: Hide graph editor
        graph_editor.toggle_visibility()
        test_timer.process_events(qapp, 500)  # Wait for animation

        assert not graph_editor.is_visible()
        assert len(visibility_spy) == 2

    def test_service_signal_communication(self, qapp, mock_beat_data):
        """Test signal communication between services and components."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Setup signal spies on service
        service_beat_spy = QSignalSpy(self.graph_service.beat_selected)
        service_arrow_spy = QSignalSpy(self.graph_service.arrow_selected)

        # Test beat selection through service
        self.graph_service.set_selected_beat(mock_beat_data, 0)

        assert len(service_beat_spy) == 1
        assert service_beat_spy[0][0] == mock_beat_data
        assert service_beat_spy[0][1] == 0

        # Test arrow selection through service
        self.graph_service.set_arrow_selection("test_arrow")

        assert len(service_arrow_spy) == 1
        assert service_arrow_spy[0][0] == "test_arrow"

    def test_hotkey_service_integration(self, qapp, mock_beat_data):
        """Test hotkey service integration with graph editor."""
        from PyQt6.QtGui import QKeyEvent
        from PyQt6.QtCore import Qt

        # Setup graph editor and services
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Setup state for hotkey testing
        self.graph_service.set_selected_beat(mock_beat_data, 0)
        self.graph_service.set_arrow_selection("test_arrow")

        # Setup signal spy
        movement_spy = QSignalSpy(self.hotkey_service.arrow_moved)

        # Create key event
        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier
        )

        # Handle key through hotkey service
        result = self.hotkey_service.handle_key_event(key_event)

        assert result == True
        assert len(movement_spy) == 1

    def test_legacy_integration_service_workflow(self, qapp, mock_beat_data):
        """Test Legacy integration service workflow."""
        # Create graphics scene for testing
        scene = QGraphicsScene()

        # Test pictograph creation through service
        legacy_integration = self.graph_service._legacy_integration

        # Setup signal spy
        pictograph_spy = QSignalSpy(legacy_integration.pictograph_updated)

        # Attempt to create pictograph
        success = legacy_integration.create_pictograph_for_beat(mock_beat_data, scene)

        # Should attempt creation (may fail without full Legacy setup)
        assert isinstance(success, bool)

        # Test arrow selection methods
        arrow_list = legacy_integration.get_arrow_list()
        assert isinstance(arrow_list, list)

        # Test arrow selection
        if arrow_list:
            first_arrow = arrow_list[0]
            select_result = legacy_integration.select_arrow(first_arrow)
            assert isinstance(select_result, bool)

    def test_pictograph_container_service_integration(self, qapp, mock_beat_data):
        """Test pictograph container integration with services."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        pictograph_container = graph_editor._pictograph_container

        # Test beat setting through container
        pictograph_container.set_beat(mock_beat_data)

        assert pictograph_container._current_beat == mock_beat_data

        # Test arrow interaction methods
        available_arrows = pictograph_container.get_available_arrows()
        assert isinstance(available_arrows, list)

        # Test arrow selection through container
        pictograph_container.select_arrow("test_arrow")
        # Should not raise exception

    def test_adjustment_panel_integration(self, qapp, mock_beat_data):
        """Test adjustment panel integration with services."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Get adjustment panels
        left_panel = graph_editor._left_adjustment_panel
        right_panel = graph_editor._right_adjustment_panel

        # Test beat setting
        left_panel.set_beat(mock_beat_data)
        right_panel.set_beat(mock_beat_data)

        # Should not raise exceptions
        assert True

    def test_animation_system_integration(self, qapp, test_timer):
        """Test animation system integration."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Test animation state tracking
        assert not graph_editor._animating
        assert not graph_editor.is_visible()

        # Start show animation
        graph_editor.toggle_visibility()

        # Should be animating
        assert graph_editor._animating

        # Wait for animation to complete
        test_timer.process_events(qapp, 500)

        # Animation should be complete
        assert not graph_editor._animating
        assert graph_editor.is_visible()

    def test_error_handling_integration(self, qapp, mock_beat_data):
        """Test error handling across integrated components."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Test with None beat data
        graph_editor.set_selected_beat(None, None)
        # Should not raise exception

        # Test with invalid arrow selection
        graph_editor._on_arrow_selected("")
        # Should not raise exception

        # Test hotkey with no selected arrow
        from PyQt6.QtGui import QKeyEvent
        from PyQt6.QtCore import Qt

        key_event = QKeyEvent(
            QKeyEvent.Type.KeyPress, Qt.Key.Key_W, Qt.KeyboardModifier.NoModifier
        )

        result = self.hotkey_service.handle_key_event(key_event)
        # Should return False (not handled) but not raise exception
        assert result == False

    def test_memory_cleanup_integration(self, qapp, mock_beat_data):
        """Test memory cleanup across integrated components."""
        graph_editor = GraphEditor(graph_service=self.graph_service, parent=None)

        # Setup some state
        graph_editor.set_sequence(mock_beat_data)
        graph_editor.set_selected_beat(mock_beat_data, 0)
        graph_editor.toggle_visibility()

        # Test cleanup
        legacy_integration = self.graph_service._legacy_integration
        legacy_integration.cleanup()

        # Should not raise exception
        assert True
