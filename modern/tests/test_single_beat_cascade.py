#!/usr/bin/env python3
"""
Single Beat Cascade Test

Tests that adding a single beat to a sequence doesn't cause cascade refreshes.
This is a more controlled test than the interactive cascade test.
"""

import sys
import os
from pathlib import Path

# Add the modern directory to the Python path
modern_dir = Path(__file__).parent
sys.path.insert(0, str(modern_dir))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from domain.models.core_models import BeatData, SequenceData

# Import DI components
try:
    from infrastructure.config.di_container import DIContainer
except ImportError:
    try:
        from src.infrastructure.config.di_container import DIContainer
    except ImportError:
        print("⚠️ Could not import DIContainer, creating minimal mock")

        class DIContainer:
            def configure_services(self):
                pass


class SingleBeatCascadeMonitor:
    """Monitor for tracking single beat addition cascade refreshes"""

    def __init__(self):
        self.reset_counts()

    def reset_counts(self):
        """Reset all counts"""
        self.sequence_modified_count = 0
        self.option_picker_refresh_count = 0
        self.picker_transitions_count = 0
        self.workbench_modifications_count = 0

    def track_sequence_modified(self):
        """Track sequence modification"""
        self.sequence_modified_count += 1
        print(f"   sequence_modified: {self.sequence_modified_count}")

    def track_option_picker_refresh(self):
        """Track option picker refresh"""
        self.option_picker_refresh_count += 1
        print(f"   option_picker_refresh: {self.option_picker_refresh_count}")

    def track_picker_transition(self):
        """Track picker transition"""
        self.picker_transitions_count += 1
        print(f"   picker_transitions: {self.picker_transitions_count}")

    def track_workbench_modification(self):
        """Track workbench modification"""
        self.workbench_modifications_count += 1
        print(f"   workbench_modifications: {self.workbench_modifications_count}")

    def report(self, operation_name="Operation"):
        """Report the current counts"""
        print(f"📊 REFRESH REPORT for {operation_name}:")
        print(f"   sequence_modified: {self.sequence_modified_count}")
        print(f"   option_picker_refresh: {self.option_picker_refresh_count}")
        print(f"   picker_transitions: {self.picker_transitions_count}")
        print(f"   workbench_modifications: {self.workbench_modifications_count}")

        # Check if we have cascade refreshes
        max_count = max(
            self.sequence_modified_count,
            self.option_picker_refresh_count,
            self.picker_transitions_count,
        )

        if max_count <= 1:
            print("✅ FIXED: No cascade refreshes detected!")
        else:
            print("❌ ISSUE: Still seeing cascade refreshes")


def test_single_beat_cascade():
    """Test that adding a single beat doesn't cause cascade refreshes"""

    print("🔧 Starting Single Beat Cascade Test")
    print("=" * 50)

    # Setup DI container
    print("🔧 Configuring DI services...")
    di_container = DIContainer()
    di_container.configure_services()
    print("✅ DI services configured successfully!")

    # Create construct tab with DI
    print("🏗️ Creating construct tab...")
    from src.presentation.tabs.construct.construct_tab_widget import ConstructTabWidget

    construct_tab = ConstructTabWidget(workbench_getter=None, workbench_setter=None)

    # Create monitor
    monitor = SingleBeatCascadeMonitor()

    # Connect monitoring signals
    if construct_tab.signal_coordinator:
        construct_tab.signal_coordinator.sequence_modified.connect(
            lambda: monitor.track_sequence_modified()
        )

    if (
        construct_tab.option_picker_manager
        and construct_tab.option_picker_manager.option_picker
    ):
        # Mock the refresh method to track calls
        original_refresh = construct_tab.option_picker_manager.refresh_from_sequence

        def tracked_refresh(*args, **kwargs):
            monitor.track_option_picker_refresh()
            return original_refresh(*args, **kwargs)

        construct_tab.option_picker_manager.refresh_from_sequence = tracked_refresh

    if construct_tab.layout_manager:
        # Mock the transition methods to track calls
        original_transition_to_option = (
            construct_tab.layout_manager.transition_to_option_picker
        )

        def tracked_transition_to_option(*args, **kwargs):
            monitor.track_picker_transition()
            return original_transition_to_option(*args, **kwargs)

        construct_tab.layout_manager.transition_to_option_picker = (
            tracked_transition_to_option
        )

        original_transition_to_start = (
            construct_tab.layout_manager.transition_to_start_position_picker
        )

        def tracked_transition_to_start(*args, **kwargs):
            monitor.track_picker_transition()
            return original_transition_to_start(*args, **kwargs)

        construct_tab.layout_manager.transition_to_start_position_picker = (
            tracked_transition_to_start
        )

    print("📊 Initial state set up")

    # Test 1: Set up initial sequence with 2 beats
    print("\n=== TEST 1: Set up initial sequence ===")
    monitor.reset_counts()

    # Create a simple 2-beat sequence
    beat1 = BeatData(beat_number=1, letter="α", duration=1.0, is_blank=False)
    beat2 = BeatData(beat_number=2, letter="Ψ", duration=1.0, is_blank=False)
    initial_sequence = SequenceData(beats=[beat1, beat2])

    # Simulate sequence modification from workbench
    if construct_tab.sequence_manager:
        print("🔄 MONITORING: Setting initial sequence")
        construct_tab.sequence_manager.handle_workbench_modified(initial_sequence)

    monitor.report("Setting initial sequence")

    # Test 2: Add a single beat
    print("\n=== TEST 2: Add single beat ===")
    monitor.reset_counts()

    # Create a new beat to add
    new_beat = BeatData(beat_number=3, letter="L", duration=1.0, is_blank=False)

    print("🔄 MONITORING: Adding single beat")
    if construct_tab.sequence_manager:
        construct_tab.sequence_manager.add_beat_to_sequence(new_beat)

    monitor.report("Adding single beat")

    # Test 3: Add another single beat
    print("\n=== TEST 3: Add another single beat ===")
    monitor.reset_counts()

    # Create another new beat to add
    another_beat = BeatData(beat_number=4, letter="G", duration=1.0, is_blank=False)

    print("🔄 MONITORING: Adding another single beat")
    if construct_tab.sequence_manager:
        construct_tab.sequence_manager.add_beat_to_sequence(another_beat)

    monitor.report("Adding another single beat")

    print("\n" + "=" * 60)
    print("🏁 SINGLE BEAT CASCADE TEST COMPLETE!")
    print("=" * 60)

    print("\n📈 EXPECTED RESULTS (after fix):")
    print("   • Each single beat addition should trigger at most 1 sequence_modified")
    print(
        "   • Each single beat addition should trigger at most 1 option_picker_refresh"
    )
    print("   • No cascading refreshes for individual operations")

    print("\n🎯 If all counts are 1, the cascade fix is working for beat additions!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Use QTimer to run the test after the event loop starts
    QTimer.singleShot(100, test_single_beat_cascade)
    QTimer.singleShot(3000, app.quit)  # Quit after 3 seconds

    app.exec()
