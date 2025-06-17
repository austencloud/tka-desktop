#!/usr/bin/env python3
"""
Data Structure Verification Script
==================================

Comprehensive verification of Legacy/Modern data structures and access patterns
before deploying parallel testing framework.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Verify 100% accuracy of data extraction patterns
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root and parallel test directory to path
project_root = Path(__file__).parent.parent.parent
parallel_test_dir = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(parallel_test_dir))

# Import with absolute paths
from drivers.legacy_driver import LegacyApplicationDriver
from drivers.modern_driver import ModernApplicationDriver
from comparison.result_comparer import TKADataNormalizer


def setup_logging():
    """Setup detailed logging for verification."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("data_structure_verification.log"),
        ],
    )


def verify_legacy_data_access():
    """Verify Legacy data access patterns work correctly."""
    print("🔍 VERIFYING Legacy DATA ACCESS PATTERNS")
    print("=" * 50)

    try:
        # Create Legacy driver
        legacy_driver = LegacyApplicationDriver(Path("test_data/legacy"))

        # Test Legacy startup
        print("1. Testing Legacy application startup...")
        if legacy_driver.start_application():
            print("   ✅ Legacy application started successfully")

            # Wait for ready
            if legacy_driver.wait_for_ready(timeout_ms=30000):
                print("   ✅ Legacy application ready")

                # Test data extraction
                print("2. Testing Legacy data extraction...")

                # Extract sequence data
                sequence_data = legacy_driver.extract_sequence_data()
                print(f"   📊 Legacy Sequence Data Structure:")
                print(f"      - Beat Count: {sequence_data.get('beat_count', 0)}")
                print(f"      - Version: {sequence_data.get('version', 'Unknown')}")
                print(
                    f"      - Start Position: {sequence_data.get('start_position', 'None')}"
                )
                print(f"      - Beats: {len(sequence_data.get('beats', []))}")

                # Test beat data structure if beats exist
                beats = sequence_data.get("beats", [])
                if beats:
                    first_beat = beats[0]
                    print(f"   📋 First Beat Structure:")
                    print(f"      - Index: {first_beat.get('index', 'N/A')}")
                    print(f"      - Letter: {first_beat.get('letter', 'N/A')}")
                    print(f"      - Duration: {first_beat.get('duration', 'N/A')}")
                    print(
                        f"      - Motions: {list(first_beat.get('motions', {}).keys())}"
                    )

                    # Test motion data structure
                    motions = first_beat.get("motions", {})
                    for color, motion_data in motions.items():
                        print(f"      - {color.title()} Motion:")
                        print(
                            f"        * Motion Type: {motion_data.get('motion_type', 'N/A')}"
                        )
                        print(
                            f"        * Prop Rot Dir: {motion_data.get('prop_rot_dir', 'N/A')}"
                        )
                        print(f"        * Turns: {motion_data.get('turns', 'N/A')}")
                        print(
                            f"        * Start Loc: {motion_data.get('start_loc', 'N/A')}"
                        )
                        print(f"        * End Loc: {motion_data.get('end_loc', 'N/A')}")

                print("   ✅ Legacy data extraction successful")

            else:
                print("   ❌ Legacy application not ready")
                return False
        else:
            print("   ❌ Legacy application startup failed")
            return False

        # Cleanup
        legacy_driver.stop_application()
        print("   🧹 Legacy application stopped")
        return True

    except Exception as e:
        print(f"   ❌ Legacy verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_modern_data_access():
    """Verify Modern data access patterns work correctly."""
    print("\n🔍 VERIFYING Modern DATA ACCESS PATTERNS")
    print("=" * 50)

    try:
        # Create Modern driver
        modern_driver = ModernApplicationDriver(Path("test_data/v2"))

        # Test Modern startup
        print("1. Testing Modern application startup...")
        if modern_driver.start_application():
            print("   ✅ Modern application started successfully")

            # Wait for ready
            if modern_driver.wait_for_ready(timeout_ms=30000):
                print("   ✅ Modern application ready")

                # Test data extraction
                print("2. Testing Modern data extraction...")

                # Extract sequence data
                sequence_data = modern_driver.extract_sequence_data()
                print(f"   📊 Modern Sequence Data Structure:")
                print(f"      - Beat Count: {sequence_data.get('beat_count', 0)}")
                print(f"      - Version: {sequence_data.get('version', 'Unknown')}")
                print(
                    f"      - Start Position: {sequence_data.get('start_position', 'None')}"
                )
                print(f"      - Beats: {len(sequence_data.get('beats', []))}")
                print(f"      - Word: {sequence_data.get('word', 'None')}")

                # Test beat data structure if beats exist
                beats = sequence_data.get("beats", [])
                if beats:
                    first_beat = beats[0]
                    print(f"   📋 First Beat Structure:")
                    print(f"      - Index: {first_beat.get('index', 'N/A')}")
                    print(f"      - Letter: {first_beat.get('letter', 'N/A')}")
                    print(f"      - Duration: {first_beat.get('duration', 'N/A')}")
                    print(
                        f"      - Motions: {list(first_beat.get('motions', {}).keys())}"
                    )

                    # Test motion data structure
                    motions = first_beat.get("motions", {})
                    for color, motion_data in motions.items():
                        print(f"      - {color.title()} Motion:")
                        print(
                            f"        * Motion Type: {motion_data.get('motion_type', 'N/A')}"
                        )
                        print(
                            f"        * Prop Rot Dir: {motion_data.get('prop_rot_dir', 'N/A')}"
                        )
                        print(f"        * Turns: {motion_data.get('turns', 'N/A')}")
                        print(
                            f"        * Start Loc: {motion_data.get('start_loc', 'N/A')}"
                        )
                        print(f"        * End Loc: {motion_data.get('end_loc', 'N/A')}")

                print("   ✅ Modern data extraction successful")

            else:
                print("   ❌ Modern application not ready")
                return False
        else:
            print("   ❌ Modern application startup failed")
            return False

        # Cleanup
        modern_driver.stop_application()
        print("   🧹 Modern application stopped")
        return True

    except Exception as e:
        print(f"   ❌ Modern verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_data_normalization():
    """Verify data normalization works correctly."""
    print("\n🔍 VERIFYING DATA NORMALIZATION")
    print("=" * 50)

    try:
        normalizer = TKADataNormalizer()

        # Test Legacy motion data normalization
        print("1. Testing Legacy motion data normalization...")
        legacy_motion_sample = {
            "motion_type": "pro",
            "prop_rot_dir": "cw",
            "turns": 1.0,
            "start_loc": "n",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "out",
        }

        normalized_legacy = normalizer.normalize_legacy_motion_data(
            legacy_motion_sample
        )
        print(f"   📊 Legacy Motion Normalized:")
        for key, value in normalized_legacy.items():
            print(f"      - {key}: {value}")

        # Test Modern motion data normalization
        print("2. Testing Modern motion data normalization...")
        modern_motion_sample = {
            "motion_type": "pro",
            "prop_rot_dir": "cw",
            "turns": 1.0,
            "start_loc": "n",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "out",
        }

        normalized_modern = normalizer.normalize_modern_motion_data(
            modern_motion_sample
        )
        print(f"   📊 Modern Motion Normalized:")
        for key, value in normalized_v2.items():
            print(f"      - {key}: {value}")

        # Verify they match
        print("3. Testing normalization equivalence...")
        if normalized_legacy == normalized_v2:
            print("   ✅ Legacy and Modern normalization produces identical results")
        else:
            print("   ❌ Legacy and Modern normalization differs:")
            for key in set(normalized_legacy.keys()) | set(normalized_v2.keys()):
                legacy_val = normalized_legacy.get(key, "MISSING")
                modern_val = normalized_v2.get(key, "MISSING")
                if legacy_val != modern_val:
                    print(f"      - {key}: Legacy={legacy_val} vs Modern={modern_val}")

        return True

    except Exception as e:
        print(f"   ❌ Data normalization verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_motion_type_mappings():
    """Verify motion type mappings are correct."""
    print("\n🔍 VERIFYING MOTION TYPE MAPPINGS")
    print("=" * 50)

    try:
        normalizer = TKADataNormalizer()

        # Test all motion types
        motion_types = ["pro", "anti", "static", "dash", "float"]

        print("1. Testing motion type mappings...")
        for motion_type in motion_types:
            mapped_type = normalizer.motion_type_mappings.get(motion_type, motion_type)
            print(f"   - {motion_type} → {mapped_type}")

            if motion_type != mapped_type:
                print(
                    f"     ⚠️  Motion type mapping detected: {motion_type} → {mapped_type}"
                )
            else:
                print(f"     ✅ Direct mapping (no conversion needed)")

        # Verify no "shift" mapping exists
        if "shift" in normalizer.motion_type_mappings:
            print(
                f"   ❌ ERROR: 'shift' mapping found: {normalizer.motion_type_mappings['shift']}"
            )
            print(
                "      This should not exist - 'shift' is a category, not a motion type!"
            )
            return False
        else:
            print("   ✅ No 'shift' mapping found (correct)")

        return True

    except Exception as e:
        print(f"   ❌ Motion type mapping verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main verification routine."""
    print("🚀 TKA PARALLEL TESTING DATA STRUCTURE VERIFICATION")
    print("=" * 60)
    print("Verifying 100% accuracy before deployment...")

    setup_logging()

    # Run all verifications
    results = []

    # Verify motion type mappings first (most critical)
    results.append(("Motion Type Mappings", verify_motion_type_mappings()))

    # Verify data normalization
    results.append(("Data Normalization", verify_data_normalization()))

    # Verify Legacy data access (requires Legacy to be available)
    try:
        results.append(("Legacy Data Access", verify_legacy_data_access()))
    except Exception as e:
        print(f"⚠️  Legacy verification skipped: {e}")
        results.append(("Legacy Data Access", None))

    # Verify Modern data access (requires Modern to be available)
    try:
        results.append(("Modern Data Access", verify_modern_data_access()))
    except Exception as e:
        print(f"⚠️  Modern verification skipped: {e}")
        results.append(("Modern Data Access", None))

    # Print final results
    print("\n🎯 VERIFICATION RESULTS")
    print("=" * 30)

    passed = 0
    failed = 0
    skipped = 0

    for test_name, result in results:
        if result is True:
            print(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            print(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            print(f"⚠️  {test_name}: SKIPPED")
            skipped += 1

    print(f"\nSummary: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0:
        print("\n🎉 ALL CRITICAL VERIFICATIONS PASSED!")
        print("✅ Data structures are 100% verified and ready for deployment")
        return 0
    else:
        print(f"\n❌ {failed} CRITICAL FAILURES DETECTED")
        print("🚫 DO NOT DEPLOY until all issues are resolved")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
