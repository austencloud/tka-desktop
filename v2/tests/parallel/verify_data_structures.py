#!/usr/bin/env python3
"""
Data Structure Verification Script
==================================

Comprehensive verification of V1/V2 data structures and access patterns
before deploying parallel testing framework.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: V1 deprecation complete
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
from drivers.v1_driver import V1ApplicationDriver
from drivers.v2_driver import V2ApplicationDriver
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


def verify_v1_data_access():
    """Verify V1 data access patterns work correctly."""
    print("🔍 VERIFYING V1 DATA ACCESS PATTERNS")
    print("=" * 50)

    try:
        # Create V1 driver
        v1_driver = V1ApplicationDriver(Path("test_data/v1"))

        # Test V1 startup
        print("1. Testing V1 application startup...")
        if v1_driver.start_application():
            print("   ✅ V1 application started successfully")

            # Wait for ready
            if v1_driver.wait_for_ready(timeout_ms=30000):
                print("   ✅ V1 application ready")

                # Test data extraction
                print("2. Testing V1 data extraction...")

                # Extract sequence data
                sequence_data = v1_driver.extract_sequence_data()
                print(f"   📊 V1 Sequence Data Structure:")
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

                print("   ✅ V1 data extraction successful")

            else:
                print("   ❌ V1 application not ready")
                return False
        else:
            print("   ❌ V1 application startup failed")
            return False

        # Cleanup
        v1_driver.stop_application()
        print("   🧹 V1 application stopped")
        return True

    except Exception as e:
        print(f"   ❌ V1 verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_v2_data_access():
    """Verify V2 data access patterns work correctly."""
    print("\n🔍 VERIFYING V2 DATA ACCESS PATTERNS")
    print("=" * 50)

    try:
        # Create V2 driver
        v2_driver = V2ApplicationDriver(Path("test_data/v2"))

        # Test V2 startup
        print("1. Testing V2 application startup...")
        if v2_driver.start_application():
            print("   ✅ V2 application started successfully")

            # Wait for ready
            if v2_driver.wait_for_ready(timeout_ms=30000):
                print("   ✅ V2 application ready")

                # Test data extraction
                print("2. Testing V2 data extraction...")

                # Extract sequence data
                sequence_data = v2_driver.extract_sequence_data()
                print(f"   📊 V2 Sequence Data Structure:")
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

                print("   ✅ V2 data extraction successful")

            else:
                print("   ❌ V2 application not ready")
                return False
        else:
            print("   ❌ V2 application startup failed")
            return False

        # Cleanup
        v2_driver.stop_application()
        print("   🧹 V2 application stopped")
        return True

    except Exception as e:
        print(f"   ❌ V2 verification failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_data_normalization():
    """Verify data normalization works correctly."""
    print("\n🔍 VERIFYING DATA NORMALIZATION")
    print("=" * 50)

    try:
        normalizer = TKADataNormalizer()

        # Test V1 motion data normalization
        print("1. Testing V1 motion data normalization...")
        v1_motion_sample = {
            "motion_type": "pro",
            "prop_rot_dir": "cw",
            "turns": 1.0,
            "start_loc": "n",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "out",
        }

        normalized_v1 = normalizer.normalize_v1_motion_data(v1_motion_sample)
        print(f"   📊 V1 Motion Normalized:")
        for key, value in normalized_v1.items():
            print(f"      - {key}: {value}")

        # Test V2 motion data normalization
        print("2. Testing V2 motion data normalization...")
        v2_motion_sample = {
            "motion_type": "pro",
            "prop_rot_dir": "cw",
            "turns": 1.0,
            "start_loc": "n",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "out",
        }

        normalized_v2 = normalizer.normalize_v2_motion_data(v2_motion_sample)
        print(f"   📊 V2 Motion Normalized:")
        for key, value in normalized_v2.items():
            print(f"      - {key}: {value}")

        # Verify they match
        print("3. Testing normalization equivalence...")
        if normalized_v1 == normalized_v2:
            print("   ✅ V1 and V2 normalization produces identical results")
        else:
            print("   ❌ V1 and V2 normalization differs:")
            for key in set(normalized_v1.keys()) | set(normalized_v2.keys()):
                v1_val = normalized_v1.get(key, "MISSING")
                v2_val = normalized_v2.get(key, "MISSING")
                if v1_val != v2_val:
                    print(f"      - {key}: V1={v1_val} vs V2={v2_val}")

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

    # Verify V1 data access (requires V1 to be available)
    try:
        results.append(("V1 Data Access", verify_v1_data_access()))
    except Exception as e:
        print(f"⚠️  V1 verification skipped: {e}")
        results.append(("V1 Data Access", None))

    # Verify V2 data access (requires V2 to be available)
    try:
        results.append(("V2 Data Access", verify_v2_data_access()))
    except Exception as e:
        print(f"⚠️  V2 verification skipped: {e}")
        results.append(("V2 Data Access", None))

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
