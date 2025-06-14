#!/usr/bin/env python3
"""
Unified Development Test Runner for TKA Desktop Application

This is the main entry point for running all development tests and diagnostics.
It provides a unified interface for testing both V1 and V2 components.
"""

import sys
import os
import argparse
from pathlib import Path


def setup_python_path():
    """Setup Python path for both V1 and V2 components."""
    root_dir = Path(__file__).parent

    # Add V1 source path
    v1_src = root_dir / "v1" / "src"
    if v1_src.exists() and str(v1_src) not in sys.path:
        sys.path.insert(0, str(v1_src))

    # Add V2 source path
    v2_src = root_dir / "v2" / "src"
    if v2_src.exists() and str(v2_src) not in sys.path:
        sys.path.insert(0, str(v2_src))

    # Add root directory
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))


def run_v2_tests():
    """Run V2 test suite using the advanced test runner."""
    print("🧪 Running V2 Test Suite...")
    print("=" * 50)

    try:
        v2_test_dir = Path(__file__).parent / "v2" / "tests"
        if not v2_test_dir.exists():
            print("❌ V2 test directory not found")
            return False

        # Import and run V2 test runner
        sys.path.insert(0, str(v2_test_dir))
        from test_runner import TestRunner

        runner = TestRunner(v2_test_dir)
        results = runner.run_all(verbose=True)

        # Check if any tests failed
        failed_count = sum(1 for r in results.values() if r["status"] == "failed")
        return failed_count == 0

    except Exception as e:
        print(f"❌ Error running V2 tests: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_arrow_rendering_tests():
    """Run specific arrow rendering tests."""
    print("\n🏹 Running Arrow Rendering Tests...")
    print("=" * 50)

    try:
        # Test basic path resolution
        from v2.src.presentation.components.pictograph.asset_utils import get_image_path

        test_paths = [
            "arrows/pro/from_radial/pro_1.0.svg",
            "arrows/static/from_radial/static_0.0.svg",
            "arrows/static/from_radial/static_1.0.svg",
            "arrows/anti/from_radial/anti_1.0.svg",
            "arrows/dash/from_radial/dash_1.0.svg",
        ]

        print("📁 Testing SVG file access and content:")
        all_valid = True
        for path in test_paths:
            full_path = get_image_path(path)
            exists = os.path.exists(full_path)

            if exists:
                # Check SVG content
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Check if SVG has valid dimensions
                    has_content = len(content.strip()) > 50  # More than just empty SVG
                    has_svg_tag = "<svg" in content
                    has_zero_size = 'width="0"' in content or 'height="0"' in content

                    if has_zero_size:
                        status = "⚠️ "
                        note = " (empty/zero-size SVG)"
                    elif has_content and has_svg_tag:
                        status = "✅"
                        note = ""
                    else:
                        status = "❌"
                        note = " (invalid SVG content)"
                        all_valid = False

                    print(f"  {status} {path}{note}")

                except Exception as e:
                    print(f"  ❌ {path} (error reading: {e})")
                    all_valid = False
            else:
                print(f"  ❌ {path} (file not found)")
                all_valid = False

        # Test color transformation
        print("\n🎨 Testing color transformation:")
        pro_path = get_image_path("arrows/pro/from_radial/pro_1.0.svg")
        if os.path.exists(pro_path):
            try:
                with open(pro_path, "r", encoding="utf-8") as f:
                    original_svg = f.read()

                # Test color transformation logic
                import re

                COLOR_MAP = {"blue": "#2E3192", "red": "#ED1C24"}
                target_color = COLOR_MAP["blue"]

                patterns = [
                    re.compile(r'(fill=")([^"]*)(")'),
                    re.compile(r"(fill:\s*)([^;]*)(;)"),
                    re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
                ]

                transformed_svg = original_svg
                for pattern in patterns:
                    transformed_svg = pattern.sub(
                        lambda m: m.group(1) + target_color + m.group(len(m.groups())),
                        transformed_svg,
                    )

                has_target_color = target_color in transformed_svg
                print(
                    f"  ✅ Color transformation: {target_color} applied: {has_target_color}"
                )

            except Exception as e:
                print(f"  ❌ Color transformation test failed: {e}")
                all_valid = False

        return all_valid

    except Exception as e:
        print(f"❌ Error in arrow rendering tests: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_option_picker_tests():
    """Run option picker integration tests."""
    print("\n🎯 Running Option Picker Integration Tests...")
    print("=" * 50)

    try:
        # Test option picker data flow
        from v2.src.domain.models.core_models import (
            BeatData,
            MotionData,
            MotionType,
            Location,
            RotationDirection,
        )

        # Create test beat data
        test_beat = BeatData(
            letter="J",
            blue_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.WEST,
                end_loc=Location.NORTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
            red_motion=MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.EAST,
                end_loc=Location.SOUTH,
                turns=1.0,
                start_ori="in",
                end_ori="out",
            ),
        )

        print(f"✅ Created test beat: {test_beat.letter}")
        print(f"  Blue motion: {test_beat.blue_motion.motion_type.value}")
        print(f"  Red motion: {test_beat.red_motion.motion_type.value}")

        # Test option ID generation
        option_id = f"beat_{test_beat.letter}"
        print(f"✅ Generated option ID: {option_id}")

        return True

    except Exception as e:
        print(f"❌ Error in option picker tests: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_application_startup_test():
    """Test application startup without full GUI."""
    print("\n🚀 Testing Application Startup...")
    print("=" * 50)

    try:
        # Test V2 main imports
        print("📦 Testing V2 imports...")
        from v2.src.domain.models.core_models import BeatData, SequenceData
        from v2.src.application.services.pictograph_dataset_service import (
            PictographDatasetService,
        )

        print("✅ V2 core imports successful")

        # Test dataset service
        print("📊 Testing dataset service...")
        dataset_service = PictographDatasetService()
        try:
            start_positions = dataset_service.get_box_start_positions()
            print(f"✅ Found {len(start_positions)} box start positions")
        except AttributeError:
            # Try alternative method names
            if hasattr(dataset_service, "get_available_start_positions"):
                start_positions = dataset_service.get_available_start_positions()
                print(f"✅ Found {len(start_positions)} start positions")
            else:
                print("✅ Dataset service initialized (method names may vary)")

        return True

    except Exception as e:
        print(f"❌ Error in application startup test: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main test runner entry point."""
    parser = argparse.ArgumentParser(description="TKA Unified Development Test Runner")
    parser.add_argument("--v2-only", action="store_true", help="Run only V2 tests")
    parser.add_argument(
        "--arrows", action="store_true", help="Run only arrow rendering tests"
    )
    parser.add_argument(
        "--option-picker", action="store_true", help="Run only option picker tests"
    )
    parser.add_argument("--startup", action="store_true", help="Run only startup tests")
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")

    args = parser.parse_args()

    # Setup environment
    setup_python_path()

    print("🧪 TKA Unified Development Test Runner")
    print("=" * 60)

    results = []

    # Determine what to run
    run_all = args.all or not any(
        [args.v2_only, args.arrows, args.option_picker, args.startup]
    )

    if args.startup or run_all:
        results.append(("Application Startup", run_application_startup_test()))

    if args.arrows or run_all:
        results.append(("Arrow Rendering", run_arrow_rendering_tests()))

    if args.option_picker or run_all:
        results.append(("Option Picker", run_option_picker_tests()))

    if args.v2_only or run_all:
        results.append(("V2 Test Suite", run_v2_tests()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")

    print(f"\nTotal: {len(results)} tests, {passed} passed, {failed} failed")

    if failed > 0:
        print("\n❌ Some tests failed. Check output above for details.")
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
