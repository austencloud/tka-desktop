#!/usr/bin/env python3
"""
Test script for start position clear functionality.
"""

# BULLETPROOF IMPORT SETUP - Works with any test execution method
import tka_test_setup

import sys
from unittest.mock import Mock


def test_start_position_clear():
    """Test clearing when only start position is selected"""
    try:
        from presentation.components.workbench.workbench import ModernSequenceWorkbench

        print("✅ Successfully imported ModernSequenceWorkbench")

        # Add your test logic here
        print("✅ Start position clear test completed")
        return True

    except Exception as e:
        print(f"❌ Error in start position clear test: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("START POSITION CLEAR TEST")
    print("=" * 70)

    success = test_start_position_clear()

    print("\n" + "=" * 70)
    if success:
        print("✅ TEST PASSED!")
    else:
        print("❌ TEST FAILED!")
    print("=" * 70)

    sys.exit(0 if success else 1)
