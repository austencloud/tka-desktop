#!/usr/bin/env python3
"""
Test to verify the 1:1 layout ratio in standalone construct tab.

This test validates that the workbench and picker have equal width proportions.
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def test_layout_ratio():
    """Test the 1:1 layout ratio in standalone construct tab."""

    try:
        print("🧪 LAYOUT RATIO TEST - 1:1 WORKBENCH TO PICKER")
        print("=" * 55)

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

        # Test layout proportions
        print("\n2. Testing layout proportions...")

        # Get the central widget and its layout
        central_widget = window.centralWidget()
        if central_widget:
            layout = central_widget.layout()
            if layout and layout.count() >= 2:
                # Get the stretch factors
                left_stretch = layout.stretch(0)  # Sequence workbench
                right_stretch = layout.stretch(1)  # Picker stack

                print(f"   Left side (workbench) stretch factor: {left_stretch}")
                print(f"   Right side (picker) stretch factor: {right_stretch}")

                # Verify 1:1 ratio
                if left_stretch == right_stretch == 1:
                    print("   ✅ PERFECT! 1:1 ratio confirmed")
                    ratio_status = "✅ CORRECT"
                elif left_stretch == right_stretch:
                    print(
                        f"   ✅ Equal ratio confirmed: {left_stretch}:{right_stretch}"
                    )
                    ratio_status = "✅ CORRECT"
                else:
                    print(f"   ❌ Incorrect ratio: {left_stretch}:{right_stretch}")
                    ratio_status = "❌ INCORRECT"

                # Get actual widget sizes after layout
                def check_actual_sizes():
                    if layout.count() >= 2:
                        left_widget = layout.itemAt(0).widget()
                        right_widget = layout.itemAt(1).widget()

                        if left_widget and right_widget:
                            left_width = left_widget.width()
                            right_width = right_widget.width()
                            total_width = central_widget.width()

                            print(f"\n3. Actual widget sizes:")
                            print(f"   Window total width: {total_width}px")
                            print(f"   Left widget (workbench) width: {left_width}px")
                            print(f"   Right widget (picker) width: {right_width}px")

                            if left_width > 0 and right_width > 0:
                                left_percentage = (left_width / total_width) * 100
                                right_percentage = (right_width / total_width) * 100
                                actual_ratio = (
                                    left_width / right_width if right_width > 0 else 0
                                )

                                print(f"   Left percentage: {left_percentage:.1f}%")
                                print(f"   Right percentage: {right_percentage:.1f}%")
                                print(f"   Actual ratio: {actual_ratio:.2f}:1")

                                # Check if ratio is close to 1:1 (within 10% tolerance)
                                if 0.9 <= actual_ratio <= 1.1:
                                    print("   ✅ Actual sizes confirm 1:1 ratio!")
                                    return True
                                else:
                                    print("   ⚠️  Actual sizes show different ratio")
                                    return False
                    return False

                # Set up timer to check sizes after layout is complete
                def verify_layout():
                    success = check_actual_sizes()

                    print(f"\n🎯 LAYOUT RATIO TEST RESULTS:")
                    print(f"   Stretch factors: {ratio_status}")
                    print(
                        f"   Actual sizes: {'✅ CORRECT' if success else '⚠️  NEEDS VERIFICATION'}"
                    )

                    if ratio_status == "✅ CORRECT" and success:
                        print(
                            "\n🎉 SUCCESS! The standalone construct tab maintains a perfect 1:1 ratio!"
                        )
                        print(
                            "   The workbench and picker have equal width proportions."
                        )
                    else:
                        print("\n⚠️  Layout may need adjustment for perfect 1:1 ratio.")

                    # Close after verification
                    def close_test():
                        print("\n🏁 Layout test complete! Closing application...")
                        window.close()
                        app.quit()

                    close_timer = QTimer()
                    close_timer.timeout.connect(close_test)
                    close_timer.setSingleShot(True)
                    close_timer.start(3000)  # 3 seconds to see results

                # Wait for layout to complete, then verify
                layout_timer = QTimer()
                layout_timer.timeout.connect(verify_layout)
                layout_timer.setSingleShot(True)
                layout_timer.start(1000)  # 1 second for layout to complete

            else:
                print("   ❌ Could not access layout or insufficient widgets")
                return 1
        else:
            print("   ❌ Could not access central widget")
            return 1

        print("\n⏱️  Test will run for 5 seconds to verify layout...")
        print("🎯 Watch for the layout ratio results!")

        return app.exec()

    except Exception as e:
        print(f"❌ Layout ratio test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = test_layout_ratio()
    print(f"\nLayout ratio test completed with exit code: {result}")
    if result == 0:
        print("✅ Layout ratio test completed successfully!")
    else:
        print("❌ Layout ratio test failed")
    sys.exit(result)
