#!/usr/bin/env python3
"""
Test option picker reactivity with proper DI setup

Tests the automatic switching between start position picker and option picker
based on sequence state changes, particularly after clearing sequences.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Core DI setup
from core.dependency_injection.di_container import DIContainer, get_container
from core.interfaces.core_services import ILayoutService, IUIStateManagementService
from core.interfaces.workbench_services import (
    ISequenceWorkbenchService,
    IFullScreenService,
    IBeatDeletionService,
    IGraphEditorService,
    IDictionaryService,
)

# Services
from application.services.core.sequence_management_service import (
    SequenceManagementService,
)
from application.services.ui.ui_state_management_service import UIStateManagementService
from application.services.ui.full_screen_service import FullScreenService
from application.services.graph_editor_service import GraphEditorService
from application.services.layout.layout_management_service import (
    LayoutManagementService,
)

# Domain models
from domain.models.core_models import SequenceData, BeatData

# Construct tab components
from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget


def configure_test_services(container: DIContainer):
    """Configure all services needed for the construct tab test"""
    print("🔧 Configuring DI services...")

    # Core services
    container.register_singleton(ILayoutService, LayoutManagementService)
    container.register_singleton(IUIStateManagementService, UIStateManagementService)

    # Workbench services (using SequenceManagementService for consolidation)
    container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
    container.register_singleton(IBeatDeletionService, SequenceManagementService)
    container.register_singleton(IDictionaryService, SequenceManagementService)
    container.register_singleton(IFullScreenService, FullScreenService)

    # Graph editor needs UI state service
    ui_state_service = container.resolve(IUIStateManagementService)
    graph_editor_service = GraphEditorService(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    print("✅ DI services configured successfully!")


class OptionPickerReactivityTest:
    """Test class for option picker reactivity"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        # Setup DI container
        self.container = get_container()
        configure_test_services(self.container)

        # Create construct tab
        print("🏗️ Creating construct tab...")
        self.construct_tab = ConstructTabWidget(self.container)
        self.construct_tab.setWindowTitle("Option Picker Reactivity Test")
        self.construct_tab.resize(1200, 800)

        # Connect signals for testing
        self._connect_test_signals()

        # Test sequence
        self.test_sequence_counter = 0

    def _connect_test_signals(self):
        """Connect signals for testing"""
        if self.construct_tab.signal_coordinator:
            self.construct_tab.signal_coordinator.sequence_modified.connect(
                self._on_sequence_modified
            )
            self.construct_tab.signal_coordinator.start_position_set.connect(
                self._on_start_position_set
            )

    def _on_sequence_modified(self, sequence):
        """Handle sequence modification for testing"""
        print(
            f"🔔 TEST: Sequence modified with {sequence.length if sequence else 0} beats"
        )

    def _on_start_position_set(self, position_key):
        """Handle start position set for testing"""
        print(f"🔔 TEST: Start position set: {position_key}")

    def run_automated_test(self):
        """Run automated test sequence"""
        print("🚀 Starting automated option picker reactivity test...")

        # Create test beats
        beat1 = BeatData(beat_number=1, letter="A")
        beat2 = BeatData(beat_number=2, letter="B")
        test_sequence = SequenceData(name="Test Sequence", beats=[beat1, beat2])

        def test_step_1():
            print(
                "\n📋 TEST STEP 1: Setting initial sequence (should show option picker)"
            )
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(test_sequence)
            QTimer.singleShot(2000, test_step_2)

        def test_step_2():
            print(
                "\n📋 TEST STEP 2: Clearing sequence (should switch to start position picker)"
            )
            if self.construct_tab.workbench:
                # Clear via workbench (simulates clicking clear button)
                self.construct_tab.workbench._handle_clear()
            QTimer.singleShot(2000, test_step_3)

        def test_step_3():
            print(
                "\n📋 TEST STEP 3: Setting sequence again (should switch back to option picker)"
            )
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(test_sequence)
            QTimer.singleShot(2000, test_step_4)

        def test_step_4():
            print(
                "\n📋 TEST STEP 4: Setting empty sequence (should switch to start position picker)"
            )
            empty_sequence = SequenceData.empty()
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(empty_sequence)
            QTimer.singleShot(2000, test_complete)

        def test_complete():
            print("\n✅ TEST COMPLETE: All option picker reactivity tests finished!")
            print("📊 Summary:")
            print("   • Sequence with beats → Option picker should be visible")
            print("   • Clear/empty sequence → Start position picker should be visible")
            print("   • Signal flow should prevent cascading refreshes")

        # Start the test sequence
        QTimer.singleShot(1000, test_step_1)

    def run(self):
        """Run the test"""
        self.construct_tab.show()

        # Display current picker state
        if hasattr(self.construct_tab.layout_manager, "picker_stack"):
            current_index = (
                self.construct_tab.layout_manager.picker_stack.currentIndex()
            )
            picker_type = (
                "Start Position Picker" if current_index == 0 else "Option Picker"
            )
            print(f"📊 Initial picker state: {picker_type} (index {current_index})")

        # Start automated test
        self.run_automated_test()

        print("🎯 Running option picker reactivity test...")
        print("   Watch for automatic picker switching as sequences change!")

        return self.app.exec()


def main():
    """Main test function"""
    print("🔧 Starting Option Picker Reactivity Test")
    print("=" * 50)

    try:
        test = OptionPickerReactivityTest()
        return test.run()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the modern/ directory")
        return 1
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
