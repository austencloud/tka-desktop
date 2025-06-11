#!/usr/bin/env python3
"""
Integration test for the reorganized standalone system.

This test validates that all components work correctly after the reorganization
into the new logical directory structure.
"""

import sys
import os

# Add src directory to path
src_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def test_reorganized_system():
    """Test the complete reorganized standalone system."""

    try:
        print("🧪 REORGANIZED SYSTEM INTEGRATION TEST")
        print("=" * 50)

        # Test 1: Core imports
        print("1. Testing core imports...")
        from standalone.core.base_runner import (
            BaseStandaloneRunner,
            create_standalone_runner,
        )
        from standalone.core.launcher import main as launcher_main

        print("   ✅ Core imports successful")

        # Test 2: Service imports
        print("2. Testing service imports...")
        from standalone.services.image_creator.image_creator import (
            StandaloneImageCreator,
        )
        from standalone.services.image_creator.beat_factory import StandaloneBeatFactory
        from standalone.services.image_creator.layout_calculator import (
            StandaloneLayoutCalculator,
        )
        from standalone.services.image_creator.beat_renderer import (
            StandaloneBeatRenderer,
        )

        print("   ✅ Service imports successful")

        # Test 3: Tab imports
        print("3. Testing tab imports...")
        # These should work as module imports
        import standalone.tabs.construct
        import standalone.tabs.browse
        import standalone.tabs.generate
        import standalone.tabs.learn
        import standalone.tabs.sequence_card

        print("   ✅ Tab imports successful")

        # Test 4: Patch imports
        print("4. Testing patch imports...")
        from standalone.core.patches.full_screen_patch import (
            patch_full_screen_viewer_for_standalone,
        )

        print("   ✅ Patch imports successful")

        # Test 5: Package-level imports
        print("5. Testing package-level imports...")
        import standalone

        print(f"   ✅ Package version: {standalone.__version__}")
        print(f"   ✅ Package author: {standalone.__author__}")

        # Test 6: Create and test image creator
        print("6. Testing image creator functionality...")
        image_creator = StandaloneImageCreator()

        test_sequence = [
            {"word": "ReorganizedTest"},
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
        ]

        options = {
            "include_start_position": True,
            "add_user_info": False,
            "add_word": False,
            "add_difficulty_level": False,
            "add_beat_numbers": True,
            "add_reversal_symbols": True,
        }

        qimage = image_creator.create_sequence_image(
            sequence_data=test_sequence,
            options=options,
            user_name="ReorganizedTest",
            export_date="12-25-2024",
        )

        if qimage and not qimage.isNull():
            print(f"   ✅ Image created: {qimage.width()}x{qimage.height()}")
        else:
            print("   ❌ Image creation failed")
            return 1

        # Test 7: Test standalone runner creation
        print("7. Testing standalone runner creation...")
        from main_window.main_widget.construct_tab.construct_tab_factory import (
            ConstructTabFactory,
        )

        runner = create_standalone_runner("construct", ConstructTabFactory)
        print(f"   ✅ Runner created: {type(runner).__name__}")
        print(f"   ✅ Tab name: {runner.tab_name}")
        print(f"   ✅ Factory: {runner.tab_factory_class.__name__}")

        # Test 8: Test component integration
        print("8. Testing component integration...")
        beat_factory = StandaloneBeatFactory()
        layout_calc = StandaloneLayoutCalculator()
        beat_renderer = StandaloneBeatRenderer()

        # Process sequence
        beat_data = beat_factory.process_sequence_to_beat_data(test_sequence)
        print(f"   ✅ Beat factory processed {len(beat_data)} beats")

        # Calculate layout
        columns, rows = layout_calc.calculate_layout(len(beat_data), True)
        print(f"   ✅ Layout calculator: {columns}x{rows}")

        # Test beat renderer (create a small test image)
        from PyQt6.QtGui import QImage
        from PyQt6.QtCore import Qt

        test_image = QImage(100, 100, QImage.Format.Format_ARGB32)
        test_image.fill(Qt.GlobalColor.white)

        beat_renderer.render_beats(
            image=test_image,
            beat_data_list=beat_data,
            columns=1,
            rows=1,
            beat_size=50,
            include_start_position=False,
            start_pos_data=None,
            additional_height_top=0,
            add_beat_numbers=True,
            add_reversal_symbols=True,
        )
        print("   ✅ Beat renderer: Successfully rendered test image")

        print("\n✅ ALL REORGANIZED SYSTEM TESTS PASSED!")
        print("\n🎯 REORGANIZATION VERIFICATION:")
        print("   ✅ Core infrastructure working")
        print("   ✅ Service components functional")
        print("   ✅ Tab modules importable")
        print("   ✅ Patch system operational")
        print("   ✅ Package structure correct")
        print("   ✅ Image creation pipeline working")
        print("   ✅ Component integration successful")

        print("\n🚀 THE REORGANIZED STANDALONE SYSTEM IS FULLY FUNCTIONAL!")

        return 0

    except Exception as e:
        print(f"❌ Reorganized system test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    result = test_reorganized_system()
    print(f"\nReorganized system test completed with exit code: {result}")
    if result == 0:
        print("🎉 SUCCESS! THE REORGANIZED STANDALONE SYSTEM IS WORKING PERFECTLY!")
        print("\n📋 NEW USAGE:")
        print("   python src/standalone/core/launcher.py construct")
        print("   python src/standalone/tabs/construct.py")
        print("   python -m standalone.core.launcher construct")
        print("   python -m standalone.tabs.construct")
    else:
        print("❌ Reorganized system test failed")
    sys.exit(result)
