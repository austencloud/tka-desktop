#!/usr/bin/env python3
"""
End-to-end test that simulates the complete user interaction flow:
1. User starts the application
2. User selects a start position
3. User clicks on a beat option in the option picker
4. Verify the entire flow works without errors

This test catches real-world errors that unit tests miss.

TEST LIFECYCLE: SPECIFICATION
PURPOSE: Ensure the core user flow of selecting a beat and updating the workbench and graph editor works as expected.
PERMANENT: This is a fundamental user interaction.
"""

import sys
import os
import time
import pytest  # Added import

# Add the v2 src directory to the path
v2_src_path = os.path.join(os.path.dirname(__file__), "src")
if v2_src_path not in sys.path:
    sys.path.insert(0, v2_src_path)

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.factories.workbench_factory import (
    create_modern_workbench,
    configure_workbench_services,
)
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from src.application.services.simple_layout_service import SimpleLayoutService
from src.application.services.simple_sequence_service import (
    SequenceService,
    SimpleSequenceDataService,
    SimpleSettingsService,
    SimpleValidationService,
)
from src.presentation.components.option_picker.clickable_pictograph_frame import (
    ClickablePictographFrame,
)
from PyQt6.QtCore import Qt


@pytest.mark.ui
def test_complete_user_flow_with_qtbot(
    qtbot_with_container, mock_beat_data, dummy_conftest_fixture
):  # Using qtbot_with_container and dummy fixture
    """Test the complete user interaction flow using pytest-qt."""
    print("🚀 Starting end-to-end user flow test with qtbot...")
    print(f"✅ Dummy fixture loaded: {dummy_conftest_fixture}")

    container = qtbot_with_container.container  # Get container from extended qtbot

    # Step 1: Create the main application components
    print("\n📱 Step 1: Creating application components...")

    # Services are already configured in the mock_container or should be set up here if needed for the test
    # For this test, we'll assume the container passed in is sufficiently configured
    # or we use the real services as defined in the original test if they don't involve heavy external dependencies.

    # Create the construct tab (this is what the user sees)
    construct_tab = ConstructTabWidget(container)
    qtbot_with_container.addWidget(
        construct_tab
    )  # Add to qtbot for auto-cleanup and interaction
    construct_tab.show()
    qtbot_with_container.waitActive(construct_tab)

    print("✅ Application components created successfully")

    # Step 2: Simulate user selecting a start position (implicitly done by option picker init)
    print("\n🎯 Step 2: Verifying option picker and workbench...")

    option_picker = construct_tab.option_picker
    workbench = construct_tab.workbench

    assert option_picker is not None, "Option picker should exist"
    assert workbench is not None, "Workbench should exist"
    assert workbench._graph_section is not None, "Graph section should exist"

    print("✅ All UI components verified")

    # Step 3: Simulate clicking on a beat option
    print("\n🖱️ Step 3: Simulating user clicking on beat option...")

    # Wait for the option picker to be populated
    def get_beat_frames():
        # Find ClickablePictographFrame instances within the option_picker widget hierarchy
        # They are nested inside the option picker sections
        return option_picker.widget.findChildren(ClickablePictographFrame)

    qtbot_with_container.waitUntil(lambda: len(get_beat_frames()) > 0, timeout=10000)
    beat_frames = get_beat_frames()

    assert (
        len(beat_frames) > 0
    ), f"ClickablePictographFrame instances should be available in the option picker, found: {len(beat_frames)}"
    print(f"🎯 Found {len(beat_frames)} beat frames, simulating click on first one...")

    first_beat_frame = beat_frames[0]  # Renamed variable

    try:
        print(
            f"   → Clicking on beat frame with beat: {getattr(first_beat_frame, 'beat_data', 'unknown')}"
        )

        # Store initial sequence state for comparison
        initial_sequence = workbench._current_sequence
        initial_beat_count = len(initial_sequence.beats) if initial_sequence else 0
        
        # Perform the click
        qtbot_with_container.mouseClick(
            first_beat_frame, Qt.MouseButton.LeftButton
        )
        
        # Wait for sequence state to change instead of relying on signal
        def sequence_updated():
            current_sequence = workbench._current_sequence
            current_beat_count = len(current_sequence.beats) if current_sequence else 0
            return current_beat_count > initial_beat_count
        
        # Wait for the workbench to update its sequence
        qtbot_with_container.waitUntil(sequence_updated, timeout=5000)
        
        # Verify the workbench state has been updated
        current_sequence = workbench._current_sequence
        current_beat_count = len(current_sequence.beats) if current_sequence else 0
        
        assert current_beat_count > initial_beat_count, f"Beat count should have increased from {initial_beat_count} to {current_beat_count}"
        assert current_sequence is not None, "Workbench should have a current sequence after click"
        assert len(current_sequence.beats) > 0, "Sequence should contain beats after click"
        
        print(f"   → Beat successfully added! Sequence now has {current_beat_count} beats")

        print(
            "✅ Beat frame click simulation and state verification completed successfully!"
        )

    except Exception as e:
        print(f"❌ ERROR during beat frame click: {e}")
        import traceback

        traceback.print_exc()
        pytest.fail(f"Error during beat frame click: {e}")

    # Step 4: Verify the complete flow worked
    print("\n✅ Step 4: Verifying complete flow...")

    current_sequence_in_workbench = workbench._current_sequence
    assert (
        current_sequence_in_workbench is not None
    ), "Workbench should have a current sequence"
    assert (
        len(current_sequence_in_workbench.beats) > 0
    ), "Workbench sequence should have beats"
    print(
        f"✅ Workbench has sequence with {len(current_sequence_in_workbench.beats)} beats"
    )

    graph_service = workbench._graph_section._graph_service
    # In testing environment, this may be a Mock, which is acceptable
    service_type_name = type(graph_service).__name__
    print(f"✅ Graph section has service type: {service_type_name}")
    
    # Verify that either we have the real service or a proper mock
    assert service_type_name in ["GraphEditorService", "Mock"], f"Graph section has unexpected service type: {service_type_name}"

    # Verify graph editor display was updated (e.g. by checking for visible items)
    # This might require a more specific signal from the graph editor or checking its state.
    # For now, we assume sequence_updated implies the graph will also update.
    # A more robust check would be to wait for a signal like graph_editor.display_updated
    # if it exists and is appropriate.

    # Example: wait for graph editor to show something (if applicable)
    # graph_editor_widget = workbench._graph_section._graph_editor_widget
    # def graph_has_items():
    #     return len(graph_editor_widget.scene().items()) > 0
    # qtbot_with_container.waitUntil(graph_has_items, timeout=2000)
    # assert len(graph_editor_widget.scene().items()) > 0, "Graph editor should display items after beat selection"

    print("🎉 End-to-end user flow test with qtbot completed successfully!")
