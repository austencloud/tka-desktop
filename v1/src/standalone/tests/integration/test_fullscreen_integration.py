#!/usr/bin/env python3
"""
Full screen integration test for standalone construct tab.

This test validates the complete integration of the full screen functionality
in the standalone construct tab environment.
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def test_fullscreen_integration():
    """Test the full screen integration in standalone construct tab."""

    try:
        print("🧪 FULL SCREEN INTEGRATION TEST")
        print("=" * 40)

        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        from standalone.core.base_runner import create_standalone_runner
        from main_window.main_widget.construct_tab.construct_tab_factory import (
            ConstructTabFactory,
        )

        # Initialize Qt application
        app = QApplication(sys.argv)

        # Create standalone construct tab
        print("1. Creating standalone construct tab...")
        runner = create_standalone_runner("construct", ConstructTabFactory)
        runner.configure_import_paths()
        runner.initialize_logging()
        runner.app_context = runner.initialize_dependency_injection()

        coordinator = runner.create_minimal_coordinator()
        tab_widget = runner.create_tab_with_coordinator(coordinator)

        from standalone.core.base_runner import StandaloneTabWindow

        window = StandaloneTabWindow(tab_widget, "construct", coordinator)
        window.show()

        print("✅ Standalone construct tab created and shown")

        # Build test sequence
        print("\n2. Building test sequence...")
        try:
            # Create a minimal test sequence
            test_sequence = [
                {"word": "IntegrationTest"},
                {"sequence_start_position": True, "start_pos": "alpha1"},
                {
                    "beat": 1,
                    "letter": "α",
                    "start_pos": "alpha1",
                    "end_pos": "beta5",
                    "motion_type": "pro",
                    "prop_rot_dir": "cw",
                    "turns": 0,
                    "blue_attributes": {
                        "motion_type": "static",
                        "prop_rot_dir": "cw",
                        "start_loc": "alpha1",
                        "end_loc": "alpha1",
                        "turns": 0,
                    },
                    "red_attributes": {
                        "motion_type": "pro",
                        "prop_rot_dir": "ccw",
                        "start_loc": "alpha1",
                        "end_loc": "beta5",
                        "turns": 0,
                    },
                },
                {
                    "beat": 2,
                    "letter": "β",
                    "start_pos": "beta5",
                    "end_pos": "gamma11",
                    "motion_type": "pro",
                    "prop_rot_dir": "ccw",
                    "turns": 1,
                    "blue_attributes": {
                        "motion_type": "pro",
                        "prop_rot_dir": "ccw",
                        "start_loc": "beta5",
                        "end_loc": "gamma11",
                        "turns": 1,
                    },
                    "red_attributes": {
                        "motion_type": "static",
                        "prop_rot_dir": "cw",
                        "start_loc": "beta5",
                        "end_loc": "beta5",
                        "turns": 0,
                    },
                },
            ]

            # Try to set the sequence in the coordinator's JSON manager
            if hasattr(coordinator, "json_manager") and hasattr(
                coordinator.json_manager, "loader_saver"
            ):
                coordinator.json_manager.loader_saver.current_sequence = test_sequence
                print(f"✅ Test sequence built: {len(test_sequence)} entries")
            else:
                print("⚠️  Could not set sequence in JSON manager")

        except Exception as e:
            print(f"❌ Failed to build test sequence: {e}")
            return 1

        # Test full screen functionality
        print("\n3. Testing full screen functionality...")
        try:
            # Get the full screen viewer from the sequence workbench
            sequence_workbench = coordinator.widget_manager.get_widget(
                "sequence_workbench"
            )
            if sequence_workbench and hasattr(sequence_workbench, "full_screen_viewer"):
                full_screen_viewer = sequence_workbench.full_screen_viewer

                # Trigger the full screen view
                print("   Triggering full screen view...")
                full_screen_viewer.view_full_screen()

                print("✅ Full screen functionality tested successfully")
            else:
                print("❌ Could not access full screen viewer")
                return 1

        except Exception as e:
            print(f"❌ Full screen test failed: {e}")
            import traceback

            traceback.print_exc()
            return 1

        print("\n✅ ALL INTEGRATION TESTS PASSED!")

        # Keep window open briefly for verification
        def close_test():
            print("\n🏁 Integration test complete! Closing application...")
            window.close()
            app.quit()

        timer = QTimer()
        timer.timeout.connect(close_test)
        timer.setSingleShot(True)
        timer.start(5000)  # 5 seconds

        print("\n⏱️  Test will run for 5 seconds...")
        print(
            "🎯 You should see the standalone construct tab with full screen functionality!"
        )

        return app.exec()

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = test_fullscreen_integration()
    print(f"\nIntegration test completed with exit code: {result}")
    if result == 0:
        print("✅ Full screen integration test passed")
    else:
        print("❌ Full screen integration test failed")
    sys.exit(result)
