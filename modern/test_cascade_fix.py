#!/usr/bin/env python3
"""
Test to confirm the triple refresh fix

This test specifically monitors refresh counts to ensure we've eliminated
the cascade refresh issue while maintaining picker reactivity.
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

    # Workbench services
    container.register_singleton(ISequenceWorkbenchService, SequenceManagementService)
    container.register_singleton(IBeatDeletionService, SequenceManagementService)
    container.register_singleton(IDictionaryService, SequenceManagementService)
    container.register_singleton(IFullScreenService, FullScreenService)

    # Graph editor needs UI state service
    ui_state_service = container.resolve(IUIStateManagementService)
    graph_editor_service = GraphEditorService(ui_state_service)
    container.register_instance(IGraphEditorService, graph_editor_service)

    print("✅ DI services configured successfully!")


class RefreshCountMonitor:
    """Monitor refresh counts to verify cascade fix"""

    def __init__(self):
        self.refresh_counts = {
            "sequence_modified": 0,
            "option_picker_refresh": 0,
            "picker_transitions": 0,
            "workbench_modifications": 0,
        }
        self.last_operation = ""

    def reset_counts(self, operation_name: str):
        """Reset counts for a new operation"""
        self.refresh_counts = {key: 0 for key in self.refresh_counts}
        self.last_operation = operation_name
        print(f"\n🔄 MONITORING: {operation_name}")

    def increment(self, counter_type: str):
        """Increment a specific counter"""
        self.refresh_counts[counter_type] += 1
        print(f"   {counter_type}: {self.refresh_counts[counter_type]}")

    def report(self):
        """Report final counts"""
        print(f"\n📊 REFRESH REPORT for {self.last_operation}:")
        for key, count in self.refresh_counts.items():
            print(f"   {key}: {count}")

        # Check if we have eliminated cascades
        if (
            self.refresh_counts["sequence_modified"] <= 1
            and self.refresh_counts["option_picker_refresh"] <= 1
        ):
            print("✅ FIXED: No cascade refreshes detected!")
        else:
            print("❌ ISSUE: Still seeing cascade refreshes")


class CascadeFixTest:
    """Test class for cascade refresh fix verification"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        # Setup DI container
        self.container = get_container()
        configure_test_services(self.container)

        # Create construct tab
        print("🏗️ Creating construct tab...")
        self.construct_tab = ConstructTabWidget(self.container)
        self.construct_tab.setWindowTitle("Cascade Fix Test")
        self.construct_tab.resize(1200, 800)

        # Setup monitoring
        self.monitor = RefreshCountMonitor()
        self._connect_monitoring_signals()

    def _connect_monitoring_signals(self):
        """Connect signals for monitoring refresh counts"""
        if self.construct_tab.signal_coordinator:
            # Monitor sequence modifications
            self.construct_tab.signal_coordinator.sequence_modified.connect(
                lambda seq: self.monitor.increment("sequence_modified")
            )

            # Monitor picker transitions
            original_transition_to_option = (
                self.construct_tab.layout_manager.transition_to_option_picker
            )
            original_transition_to_start = (
                self.construct_tab.layout_manager.transition_to_start_position_picker
            )

            def monitored_transition_to_option():
                self.monitor.increment("picker_transitions")
                original_transition_to_option()

            def monitored_transition_to_start():
                self.monitor.increment("picker_transitions")
                original_transition_to_start()

            self.construct_tab.layout_manager.transition_to_option_picker = (
                monitored_transition_to_option
            )
            self.construct_tab.layout_manager.transition_to_start_position_picker = (
                monitored_transition_to_start
            )

        # Monitor workbench modifications
        if self.construct_tab.sequence_manager:
            original_handle_workbench = (
                self.construct_tab.sequence_manager.handle_workbench_modified
            )

            def monitored_handle_workbench(sequence):
                self.monitor.increment("workbench_modifications")
                original_handle_workbench(sequence)

            self.construct_tab.sequence_manager.handle_workbench_modified = (
                monitored_handle_workbench
            )

        # Monitor option picker refreshes
        if self.construct_tab.option_picker_manager:
            original_refresh = (
                self.construct_tab.option_picker_manager.refresh_from_sequence
            )

            def monitored_refresh(sequence):
                self.monitor.increment("option_picker_refresh")
                original_refresh(sequence)

            self.construct_tab.option_picker_manager.refresh_from_sequence = (
                monitored_refresh
            )

    def run_cascade_fix_test(self):
        """Run comprehensive cascade fix test"""
        print("🚀 Starting cascade fix verification test...")

        # Create test data
        beat1 = BeatData(beat_number=1, letter="A")
        beat2 = BeatData(beat_number=2, letter="B")
        test_sequence = SequenceData(name="Test Sequence", beats=[beat1, beat2])

        def test_step_1():
            print("\n=== TEST 1: Set initial sequence ===")
            self.monitor.reset_counts("Setting initial sequence")
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(test_sequence)
            QTimer.singleShot(1500, test_step_2)

        def test_step_2():
            self.monitor.report()
            print("\n=== TEST 2: Clear sequence ===")
            self.monitor.reset_counts("Clearing sequence")
            if self.construct_tab.workbench:
                self.construct_tab.workbench._handle_clear()
            QTimer.singleShot(1500, test_step_3)

        def test_step_3():
            self.monitor.report()
            print("\n=== TEST 3: Set sequence again ===")
            self.monitor.reset_counts("Setting sequence again")
            if self.construct_tab.workbench:
                self.construct_tab.workbench.set_sequence(test_sequence)
            QTimer.singleShot(1500, test_step_4)

        def test_step_4():
            self.monitor.report()
            print("\n=== TEST 4: Add beat to sequence ===")
            self.monitor.reset_counts("Adding beat to sequence")
            new_beat = BeatData(beat_number=3, letter="C")
            if self.construct_tab.sequence_manager:
                self.construct_tab.sequence_manager.add_beat_to_sequence(new_beat)
            QTimer.singleShot(1500, test_complete)

        def test_complete():
            self.monitor.report()
            print("\n" + "=" * 60)
            print("🏁 CASCADE FIX TEST COMPLETE!")
            print("=" * 60)

            # Summary analysis
            print("\n📈 EXPECTED RESULTS (after fix):")
            print("   • Each operation should trigger at most 1 sequence_modified")
            print("   • Each operation should trigger at most 1 option_picker_refresh")
            print("   • No cascading refreshes")
            print("   • Picker transitions should work correctly")

            print(
                "\n🎯 If you see counts of 1 for each operation, the cascade fix is working!"
            )

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

        # Start cascade fix test
        self.run_cascade_fix_test()

        return self.app.exec()


def main():
    """Main test function"""
    print("🔧 Starting Cascade Fix Verification Test")
    print("=" * 50)

    try:
        test = CascadeFixTest()
        return test.run()
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
