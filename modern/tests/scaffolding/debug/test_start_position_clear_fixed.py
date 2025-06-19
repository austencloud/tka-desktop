#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-08-19
Test script to verify start position view behavior when sequence is cleared.

BUG REPORT: Start position view disappears when sequence is cleared
EXPECTED: Start position should persist across sequence clears (like legacy)
STATUS: ACTIVE - Test fails, start position view visibility incorrect
AUDIT_DATE: 2025-06-19
AUDIT_RESULT: FAIL - Start position view not visible when expected
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Modern imports with proper paths
from presentation.components.workbench.workbench import ModernSequenceWorkbench
from core.dependency_injection.di_container import DIContainer
from domain.models.core_models import SequenceData, BeatData
from core.interfaces.core_services import ILayoutService
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)
from application.services.layout.layout_management_service import (
    LayoutManagementService,
)
from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from application.services.ui.full_screen_service import FullScreenService
from application.services.graph_editor_service import GraphEditorService


def configure_test_services(container: DIContainer):
    """Configure all services needed for the workbench test."""
    # Register core services
    container.register_singleton(ILayoutService, LayoutManagementService)

    # Create sequence management service for multiple interfaces
    sequence_service = SequenceManagementService()
    container.register_instance(ISequenceWorkbenchService, sequence_service)
    container.register_instance(IBeatDeletionService, sequence_service)
    container.register_instance(IDictionaryService, sequence_service)

    # Register other services
    container.register_singleton(IFullScreenService, FullScreenService)
    container.register_singleton(IGraphEditorService, GraphEditorService)


def test_start_position_clear():
    """Test that start position view remains visible when sequence is cleared."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        # Create container and configure services
        container = DIContainer()
        configure_test_services(container)

        # Resolve required services
        layout_service = container.resolve(ILayoutService)
        workbench_service = container.resolve(ISequenceWorkbenchService)
        fullscreen_service = container.resolve(IFullScreenService)
        deletion_service = container.resolve(IBeatDeletionService)
        graph_service = container.resolve(IGraphEditorService)
        dictionary_service = container.resolve(IDictionaryService)

        # Create workbench
        workbench = ModernSequenceWorkbench(
            layout_service=layout_service,
            workbench_service=workbench_service,
            fullscreen_service=fullscreen_service,
            deletion_service=deletion_service,
            graph_service=graph_service,
            dictionary_service=dictionary_service,
        )

        # Create test start position data
        test_start_position = BeatData.empty()
        # Note: Using modern BeatData structure

        # Set start position
        workbench.set_start_position(test_start_position)

        # Create a sequence with some beats
        test_sequence = SequenceData.empty()
        test_beat = BeatData.empty()
        test_sequence.beats.append(test_beat)

        # Set sequence
        workbench.set_sequence(test_sequence)

        print("Initial state:")
        print(f"- Sequence length: {len(test_sequence.beats)}")
        print(f"- Start position set: {workbench.get_start_position() is not None}")

        # Check start position view visibility
        beat_frame = workbench._beat_frame_section._beat_frame
        start_pos_view = beat_frame._start_position_view
        print(f"- Start position view visible: {start_pos_view.isVisible()}")
        print(
            f"- Start position view has data: {start_pos_view.get_position_data() is not None}"
        )

        # Clear the sequence
        empty_sequence = SequenceData.empty()
        workbench.set_sequence(empty_sequence)

        print("\nAfter clearing sequence:")
        print(f"- Sequence length: {len(empty_sequence.beats)}")
        print(f"- Start position set: {workbench.get_start_position() is not None}")
        print(f"- Start position view visible: {start_pos_view.isVisible()}")
        print(
            f"- Start position view has data: {start_pos_view.get_position_data() is not None}"
        )

        # The start position view should STILL be visible, even with empty sequence
        # AND the start position data should still be preserved (like legacy)
        expected_visible = True
        expected_has_data = True  # Start position should persist across sequence clears

        success = True

        if start_pos_view.isVisible() == expected_visible:
            print("✓ Start position view visibility is correct")
        else:
            print("✗ Start position view visibility is incorrect")
            success = False

        if (start_pos_view.get_position_data() is not None) == expected_has_data:
            print("✓ Start position data persistence is correct")
        else:
            print("✗ Start position data persistence is incorrect")
            print(
                "  Expected start position to persist when sequence is cleared (like legacy)"
            )
            success = False

        return success

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_start_position_clear_pytest():
    """Pytest version of the start position clear test."""
    result = test_start_position_clear()
    assert result, "Start position clear test failed"


if __name__ == "__main__":
    print("🧪 Running Start Position Clear Test")
    print("=" * 50)
    success = test_start_position_clear()
    if success:
        print("\n✅ Test completed successfully")
        sys.exit(0)
    else:
        print("\n❌ Test failed")
        sys.exit(1)
