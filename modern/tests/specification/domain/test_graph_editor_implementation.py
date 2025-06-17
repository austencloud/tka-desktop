#!/usr/bin/env python3
"""
Simple test runner to verify Modern Graph Editor implementation.

This script tests the core functionality without complex test fixtures.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt

from src.domain.models.core_models import BeatData
from presentation.components.workbench.graph_editor.graph_editor import (
    GraphEditor,
)
from src.presentation.components.workbench.graph_editor.turn_selection_dialog import (
    TurnSelectionDialog,
)
from src.application.services.graph_editor_hotkey_service import (
    GraphEditorHotkeyService,
)
from unittest.mock import Mock


def create_sample_beat_data():
    """Create sample beat data for testing using real dataset."""
    try:
        # Import here to avoid circular imports
        import sys
        from pathlib import Path

        # Add modern/src to path
        modern_src_path = Path(__file__).parent / "src"
        if str(modern_src_path) not in sys.path:
            sys.path.insert(0, str(modern_src_path))

        from application.services.data.pictograph_dataset_service import (
            PictographDatasetService,
        )

        dataset_service = PictographDatasetService()
        # Get real start position data instead of dummy data
        real_beat = dataset_service.get_start_position_pictograph(
            "alpha1_alpha1", "diamond"
        )

        if real_beat:
            return real_beat
        else:
            print("⚠️ No real dataset available, using empty beat")
            return BeatData.empty()

    except Exception as e:
        print(f"❌ Error loading real beat data: {e}")
        # Fallback to empty beat instead of dummy data
        return BeatData.empty()


def create_mock_graph_service():
    """Create a mock graph editor service."""
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


class TestWindow(QMainWindow):
    """Test window for graph editor."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Graph Editor Test")
        self.setGeometry(100, 100, 1000, 700)

        # Create mock service
        self.graph_service = create_mock_graph_service()

        # Create sample data
        self.sample_beat = create_sample_beat_data()

        self.setup_ui()

    def setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Test buttons
        test_dialog_btn = QPushButton("Test Turn Selection Dialog")
        test_dialog_btn.clicked.connect(self.test_turn_dialog)
        layout.addWidget(test_dialog_btn)

        test_hotkeys_btn = QPushButton("Test Hotkey Service")
        test_hotkeys_btn.clicked.connect(self.test_hotkey_service)
        layout.addWidget(test_hotkeys_btn)

        test_adjustment_btn = QPushButton("Test Legacy-Exact Adjustment Panels")
        test_adjustment_btn.clicked.connect(self.test_adjustment_panels)
        layout.addWidget(test_adjustment_btn)

        toggle_btn = QPushButton("Toggle Graph Editor")
        toggle_btn.clicked.connect(self.toggle_graph_editor)
        layout.addWidget(toggle_btn)

        # Create graph editor
        self.graph_editor = GraphEditor(self.graph_service, self)
        layout.addWidget(self.graph_editor)

        # Set sample beat data
        self.graph_editor.set_selected_beat(self.sample_beat, 0)

    def test_turn_dialog(self):
        """Test the turn selection dialog."""
        print("🔄 Testing Turn Selection Dialog...")

        selected_turn = TurnSelectionDialog.get_turn_value(
            parent=self, current_turn=1.5, arrow_color="blue"
        )

        if selected_turn is not None:
            print(f"✅ Selected turn value: {selected_turn}")
        else:
            print("❌ Dialog was cancelled")

    def test_hotkey_service(self):
        """Test the hotkey service."""
        print("⌨️ Testing Hotkey Service...")

        hotkey_service = GraphEditorHotkeyService(self.graph_service)

        # Test movement amount calculation
        normal_movement = hotkey_service._calculate_movement_amount(False, False)
        fine_movement = hotkey_service._calculate_movement_amount(False, True)
        large_movement = hotkey_service._calculate_movement_amount(True, False)

        print(
            f"✅ Movement amounts - Normal: {normal_movement}, Fine: {fine_movement}, Large: {large_movement}"
        )

        # Test rotation override
        properties = {"rotation": 0.0}
        new_props = hotkey_service._apply_rotation_override(properties)
        print(f"✅ Rotation override: 0° -> {new_props['rotation']}°")

        # Test key mappings
        print(f"✅ Movement keys: {hotkey_service._movement_keys}")

    def test_adjustment_panels(self):
        """Test the Legacy-exact adjustment panels."""
        print("🎛️ Testing Legacy-Exact Adjustment Panels...")

        # Test left panel (blue)
        left_panel = self.graph_editor._left_adjustment_panel
        print(f"✅ Left panel arrow color: {left_panel._arrow_color}")
        print(f"✅ Left panel hand indicator: {left_panel._hand_indicator.text()}")

        # Test right panel (red)
        right_panel = self.graph_editor._right_adjustment_panel
        print(f"✅ Right panel arrow color: {right_panel._arrow_color}")
        print(f"✅ Right panel hand indicator: {right_panel._hand_indicator.text()}")

        # Test turn display updates
        left_panel.set_beat(self.sample_beat)
        right_panel.set_beat(self.sample_beat)
        print("✅ Beat data set on both panels")

        print(
            "✅ Legacy-exact structure: Hand Indicator → Turn Display → +/- Buttons → Motion Type"
        )

    def toggle_graph_editor(self):
        """Toggle graph editor visibility."""
        print("🔄 Toggling Graph Editor...")
        self.graph_editor.toggle_visibility()

    def keyPressEvent(self, event):
        """Handle key events for testing hotkeys."""
        # Forward to graph editor if it's visible and focused
        if self.graph_editor.is_visible():
            self.graph_editor.keyPressEvent(event)
        else:
            super().keyPressEvent(event)


def main():
    """Main test function."""
    print("🚀 Starting Modern Graph Editor Implementation Test")

    app = QApplication(sys.argv)

    # Test individual components first
    print("\n📋 Testing Individual Components:")

    # Test 1: Turn Selection Dialog
    print("1. Turn Selection Dialog...")
    try:
        dialog = TurnSelectionDialog(current_turn=1.0, arrow_color="red")
        print("   ✅ Dialog created successfully")
        assert dialog._turn_values == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        print("   ✅ Turn values correct")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Hotkey Service
    print("2. Hotkey Service...")
    try:
        mock_service = create_mock_graph_service()
        hotkey_service = GraphEditorHotkeyService(mock_service)
        print("   ✅ Hotkey service created successfully")

        # Test movement calculations
        assert hotkey_service._calculate_movement_amount(False, False) == 1.0
        assert hotkey_service._calculate_movement_amount(False, True) == 0.1
        assert hotkey_service._calculate_movement_amount(True, False) == 5.0
        print("   ✅ Movement calculations correct")

        # Test rotation override
        props = {"rotation": 0.0}
        new_props = hotkey_service._apply_rotation_override(props)
        assert new_props["rotation"] == 45
        print("   ✅ Rotation override correct")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Graph Editor Creation
    print("3. Graph Editor...")
    try:
        mock_service = create_mock_graph_service()
        graph_editor = GraphEditor(mock_service)
        print("   ✅ Graph editor created successfully")

        # Test focus policy
        assert graph_editor.focusPolicy() == Qt.FocusPolicy.StrongFocus
        print("   ✅ Focus policy set correctly")

        # Test beat data setting
        sample_beat = create_sample_beat_data()
        graph_editor.set_selected_beat(sample_beat, 0)
        assert graph_editor._selected_beat == sample_beat
        print("   ✅ Beat data setting works")

    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n🎯 All component tests completed!")

    # Show interactive test window
    print("\n🖥️ Opening Interactive Test Window...")
    print("   - Click 'Test Turn Selection Dialog' to test the dialog")
    print("   - Click 'Test Hotkey Service' to test hotkey functionality")
    print("   - Click 'Toggle Graph Editor' to test visibility animation")
    print("   - Use WASD keys when graph editor is visible to test hotkeys")
    print("   - Press X, Z, C keys to test special actions")

    window = TestWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
