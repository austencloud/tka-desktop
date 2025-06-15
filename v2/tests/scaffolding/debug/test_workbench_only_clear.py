#!/usr/bin/env python3
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Workbench-only clear sequence testing to isolate crash point
DELETE_AFTER: 2025-07-15
CREATED: 2025-06-14
AUTHOR: @austencloud
RELATED_ISSUE: Workbench clear sequence isolation testing
"""

import sys
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer

# Add v2 to path
v2_path = Path(__file__).parent
if str(v2_path) not in sys.path:
    sys.path.insert(0, str(v2_path))

try:
    from core.dependency_injection.di_container import SimpleContainer
    from src.core.interfaces.core_services import ILayoutService
    from src.core.interfaces.workbench_services import (
        ISequenceWorkbenchService,
        IFullScreenService,
        IBeatDeletionService,
        IGraphEditorService,
        IDictionaryService,
    )
    from src.application.services.simple_layout_service import SimpleLayoutService
    from src.application.services.workbench_services import (
        SequenceWorkbenchService,
        FullScreenService,
        BeatDeletionService,
        DictionaryService,
    )
    from src.application.services.graph_editor_service import GraphEditorService
    from presentation.components.workbench.workbench import ModernSequenceWorkbench
    from src.domain.models.core_models import SequenceData, BeatData
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_workbench_only_clear():
    """Test clear sequence using only the workbench component."""
    print("🧪 Testing workbench-only clear sequence...")

    app = QApplication(sys.argv)

    try:
        # Create container and register services
        container = SimpleContainer()
        container.register_singleton(ILayoutService, SimpleLayoutService)
        container.register_singleton(
            ISequenceWorkbenchService, SequenceWorkbenchService
        )
        container.register_singleton(IFullScreenService, FullScreenService)
        container.register_singleton(IBeatDeletionService, BeatDeletionService)
        container.register_singleton(IGraphEditorService, GraphEditorService)
        container.register_singleton(IDictionaryService, DictionaryService)

        # Create workbench directly
        layout_service = container.get(ILayoutService)
        workbench_service = container.get(ISequenceWorkbenchService)
        fullscreen_service = container.get(IFullScreenService)
        deletion_service = container.get(IBeatDeletionService)
        graph_service = container.get(IGraphEditorService)
        dictionary_service = container.get(IDictionaryService)

        workbench = ModernSequenceWorkbench(
            layout_service=layout_service,
            workbench_service=workbench_service,
            fullscreen_service=fullscreen_service,
            deletion_service=deletion_service,
            graph_service=graph_service,
            dictionary_service=dictionary_service,
        )

        print("✅ Workbench created successfully")

        # Create a test window to hold the workbench
        test_window = QWidget()
        test_layout = QVBoxLayout(test_window)
        test_layout.addWidget(workbench)
        test_window.show()

        # Add some beats to the sequence first
        print("🔄 Adding beats to sequence...")
        test_beats = []
        for i in range(3):
            beat = BeatData.empty().update(
                beat_number=i + 1, letter=f"Beat{i+1}", duration=1.0, is_blank=False
            )
            test_beats.append(beat)

        test_sequence = SequenceData(beats=test_beats)
        workbench.set_sequence(test_sequence)

        current_sequence = workbench.get_sequence()
        print(
            f"📊 Sequence set: {current_sequence.length if current_sequence else 0} beats"
        )

        # Now test the clear operation
        print("🗑️ Testing clear sequence operation...")

        # Set up a timeout to detect hanging
        timeout_occurred = False

        def timeout_handler():
            nonlocal timeout_occurred
            timeout_occurred = True
            print("❌ CLEAR OPERATION TIMED OUT - HANGING DETECTED")
            app.quit()

        timeout_timer = QTimer()
        timeout_timer.timeout.connect(timeout_handler)
        timeout_timer.start(5000)  # 5 second timeout

        # Execute clear operation
        try:
            workbench._handle_clear()
            timeout_timer.stop()

            if not timeout_occurred:
                # Check result
                cleared_sequence = workbench.get_sequence()
                cleared_length = cleared_sequence.length if cleared_sequence else 0

                print(f"📊 After clear: {cleared_length} beats")

                if cleared_length == 0:
                    print(
                        "✅ CLEAR SEQUENCE FIX CONFIRMED: Operation completed successfully!"
                    )
                    return True
                else:
                    print(f"❌ Clear sequence failed: {cleared_length} beats remaining")
                    return False
            else:
                return False

        except Exception as e:
            timeout_timer.stop()
            print(f"❌ Clear sequence crashed: {e}")
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        traceback.print_exc()
        return False


def test_workbench_signal_emission():
    """Test workbench signal emission in isolation."""
    print("\n🧪 Testing workbench signal emission in isolation...")

    app = QApplication(sys.argv)

    try:
        # Create container and register services
        container = SimpleContainer()
        container.register_singleton(ILayoutService, SimpleLayoutService)
        container.register_singleton(
            ISequenceWorkbenchService, SequenceWorkbenchService
        )
        container.register_singleton(IFullScreenService, FullScreenService)
        container.register_singleton(IBeatDeletionService, BeatDeletionService)
        container.register_singleton(IGraphEditorService, GraphEditorService)
        container.register_singleton(IDictionaryService, DictionaryService)

        # Create workbench directly
        layout_service = container.get(ILayoutService)
        workbench_service = container.get(ISequenceWorkbenchService)
        fullscreen_service = container.get(IFullScreenService)
        deletion_service = container.get(IBeatDeletionService)
        graph_service = container.get(IGraphEditorService)
        dictionary_service = container.get(IDictionaryService)

        workbench = ModernSequenceWorkbench(
            layout_service=layout_service,
            workbench_service=workbench_service,
            fullscreen_service=fullscreen_service,
            deletion_service=deletion_service,
            graph_service=graph_service,
            dictionary_service=dictionary_service,
        )

        print("✅ Workbench created for signal test")

        # Connect a simple signal handler
        signal_received = False

        def on_sequence_modified(sequence):
            nonlocal signal_received
            signal_received = True
            print(f"📡 Signal received: {sequence.length if sequence else 0} beats")

        workbench.sequence_modified.connect(on_sequence_modified)

        # Test signal emission
        print("🔄 Testing signal emission...")
        empty_sequence = SequenceData.empty()

        # Set up timeout
        timeout_occurred = False

        def timeout_handler():
            nonlocal timeout_occurred
            timeout_occurred = True
            print("❌ SIGNAL EMISSION TIMED OUT")
            app.quit()

        timeout_timer = QTimer()
        timeout_timer.timeout.connect(timeout_handler)
        timeout_timer.start(3000)  # 3 second timeout

        # Emit signal
        workbench.sequence_modified.emit(empty_sequence)

        # Process events briefly
        app.processEvents()
        timeout_timer.stop()

        if signal_received and not timeout_occurred:
            print("✅ Signal emission works correctly")
            return True
        else:
            print("❌ Signal emission failed or timed out")
            return False

    except Exception as e:
        print(f"❌ Signal test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test function."""
    print("🔍 WORKBENCH-ONLY CLEAR SEQUENCE TEST")
    print("=" * 50)

    # Test 1: Signal emission in isolation
    signal_test_result = test_workbench_signal_emission()

    # Test 2: Full clear operation
    clear_test_result = test_workbench_only_clear()

    print("\n📊 TEST RESULTS:")
    print(f"   Signal Emission: {'✅ PASS' if signal_test_result else '❌ FAIL'}")
    print(f"   Clear Operation: {'✅ PASS' if clear_test_result else '❌ FAIL'}")

    if signal_test_result and clear_test_result:
        print("\n🎉 ALL TESTS PASSED - Clear sequence fix confirmed!")
        return 0
    else:
        print("\n❌ TESTS FAILED - Clear sequence still has issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
