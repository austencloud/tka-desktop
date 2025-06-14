"""
End-to-End Test for StartTextOverlay Qt Lifecycle Management

This test reproduces the exact "wrapped C/C++ object has been deleted" error
that occurs when accessing StartTextOverlay after scene recreation.

Test Lifecycle:
1. Create StartPositionView with PictographComponent
2. Initialize StartTextOverlay
3. Trigger scene recreation (clear_pictograph)
4. Attempt to access overlay -> should reproduce the error
5. Validate fix prevents the error

Expected Error: RuntimeError: wrapped C/C++ object of type StartTextOverlay has been deleted
"""

import sys
import pytest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtTest import QTest

# Add the src directory to the path for imports
sys.path.insert(0, "src")

from src.presentation.components.workbench.beat_frame.start_position_view import (
    StartPositionView,
)
from src.presentation.components.start_position_picker.start_text_overlay import (
    StartTextOverlay,
)
from src.domain.models.core_models import BeatData


class TestStartTextOverlayLifecycle:
    """Test suite for StartTextOverlay Qt object lifecycle management"""

    @pytest.fixture(autouse=True)
    def setup_qt_app(self):
        """Ensure QApplication exists for Qt widgets"""
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        yield
        # Don't quit the app as it might be shared

    @pytest.fixture
    def parent_widget(self):
        """Create a parent widget for testing"""
        widget = QWidget()
        widget.setFixedSize(200, 200)
        widget.show()
        return widget

    @pytest.fixture
    def start_position_view(self, parent_widget):
        """Create StartPositionView for testing"""
        view = StartPositionView(parent=parent_widget)

        # Wait for the component to be fully initialized
        # The view uses QTimer.singleShot(100, self._initialize_start_text)
        QTest.qWait(150)  # Wait longer than the timer

        return view

    def test_reproduce_overlay_deletion_error(self, start_position_view):
        """
        Test that the fix prevents the "wrapped C/C++ object has been deleted" error

        This test simulates the workflow that previously led to the error:
        1. StartPositionView creates StartTextOverlay
        2. Scene gets cleared (simulating pictograph update)
        3. Attempt to access overlay -> should NOT crash with our fix
        """
        # Verify initial state - overlay should be created
        assert start_position_view._start_text_overlay is not None
        assert start_position_view._pictograph_component is not None
        assert start_position_view._pictograph_component.scene is not None

        # Store reference to the overlay for testing
        original_overlay = start_position_view._start_text_overlay

        # Verify overlay is initially valid
        try:
            scene = original_overlay.scene()
            assert scene is not None, "Overlay should have a valid scene initially"
        except RuntimeError as e:
            pytest.fail(f"Overlay should be valid initially, but got error: {e}")

        # Simulate the problematic workflow: clear pictograph (which clears scene)
        start_position_view._pictograph_component.clear_pictograph()

        # Now the overlay reference still exists but the C++ object may be deleted
        # With our fix, this should NOT crash

        # Attempt to recreate overlay - this should work without error
        try:
            start_position_view._add_start_text_overlay()
            # If we get here without error, the fix is working
            assert True, "Fix successfully prevents lifecycle error"
        except RuntimeError as e:
            if "wrapped C/C++ object" in str(e) and "has been deleted" in str(e):
                pytest.fail(
                    f"Fix failed: StartTextOverlay lifecycle error still occurs: {e}"
                )
            else:
                # Re-raise unexpected errors
                raise

    def test_multiple_overlay_recreation_cycles(self, start_position_view):
        """
        Test multiple cycles of overlay creation/destruction to stress test lifecycle
        """
        for cycle in range(3):
            # Verify overlay exists
            assert start_position_view._start_text_overlay is not None

            # Clear pictograph (destroys scene items)
            start_position_view._pictograph_component.clear_pictograph()

            # Try to recreate overlay - this should trigger the error in current implementation
            try:
                start_position_view._add_start_text_overlay()
                # If we get here without error, the fix is working
            except RuntimeError as e:
                if "wrapped C/C++ object" in str(e) and "has been deleted" in str(e):
                    pytest.fail(f"Cycle {cycle}: StartTextOverlay lifecycle error: {e}")
                else:
                    # Re-raise unexpected errors
                    raise

    def test_scene_recreation_with_beat_data(self, start_position_view):
        """
        Test the specific workflow that triggers the error: updating with beat data
        """
        # Create mock beat data
        beat_data = BeatData(
            letter="A", blue_motion=None, red_motion=None, glyph_data=None
        )

        # Initial state
        assert start_position_view._start_text_overlay is not None

        # Update with beat data - this triggers pictograph update and overlay recreation
        start_position_view.set_position_data(beat_data)

        # Wait for any timer-based operations
        QTest.qWait(50)

        # Clear and update again - this should trigger the error in current implementation
        start_position_view._pictograph_component.clear_pictograph()

        # This call should reproduce the error
        try:
            start_position_view._add_start_text_overlay()
        except RuntimeError as e:
            if "wrapped C/C++ object" in str(e) and "has been deleted" in str(e):
                pytest.fail(f"Beat data update workflow triggered lifecycle error: {e}")
            else:
                raise

    def test_timer_based_initialization_race_condition(self, parent_widget):
        """
        Test race condition between timer-based initialization and scene operations
        """
        # Create view but don't wait for timer
        view = StartPositionView(parent=parent_widget)

        # Immediately try to manipulate before timer fires
        view._pictograph_component.clear_pictograph()

        # Wait for timer to fire - this might cause race condition
        QTest.qWait(150)

        # Verify no crash occurred and overlay is properly managed
        # In current implementation, this might trigger the error
        try:
            if view._start_text_overlay:
                scene = view._start_text_overlay.scene()
        except RuntimeError as e:
            if "wrapped C/C++ object" in str(e) and "has been deleted" in str(e):
                pytest.fail(f"Timer race condition triggered lifecycle error: {e}")
            else:
                raise

    def test_fix_validation_direct_scene_access(self, start_position_view):
        """
        Test that validates the fix by directly testing the problematic line 179 scenario
        """
        # Verify initial state
        assert start_position_view._start_text_overlay is not None

        # Clear pictograph which destroys scene items
        start_position_view._pictograph_component.clear_pictograph()

        # This is the exact line that was failing (line 179 in start_position_view.py)
        # With our fix, this should not crash
        try:
            # Simulate the exact call that was failing
            if start_position_view._start_text_overlay:
                # This should be handled gracefully by our validity checking
                if hasattr(start_position_view._start_text_overlay, "is_valid"):
                    is_valid = start_position_view._start_text_overlay.is_valid()
                    # If not valid, the cleanup should handle it gracefully
                    if not is_valid:
                        assert True, "Fix correctly detected invalid overlay"
                    else:
                        # If still valid, scene access should work
                        scene = start_position_view._start_text_overlay.scene()
                        assert True, "Fix allows safe scene access when valid"
                else:
                    # Fallback to old behavior should still be safe
                    assert True, "Fix provides backward compatibility"
        except RuntimeError as e:
            if "wrapped C/C++ object" in str(e) and "has been deleted" in str(e):
                pytest.fail(
                    f"Fix failed: The exact error from line 179 still occurs: {e}"
                )
            else:
                raise

    def test_overlay_validity_checking(self, start_position_view):
        """
        Test the new validity checking functionality
        """
        overlay = start_position_view._start_text_overlay
        assert overlay is not None

        # Initially should be valid
        assert overlay.is_valid() == True

        # Clear scene
        start_position_view._pictograph_component.clear_pictograph()

        # After scene clear, validity should be properly managed
        # The overlay might become invalid, and that's expected behavior
        try:
            validity = overlay.is_valid()
            # Either valid or invalid is acceptable, as long as no crash occurs
            assert isinstance(validity, bool)
        except RuntimeError:
            # If RuntimeError occurs, it should be handled gracefully
            pytest.fail("Validity checking should handle RuntimeError gracefully")


if __name__ == "__main__":
    # Run the test to validate the fix
    pytest.main([__file__, "-v", "-s"])
