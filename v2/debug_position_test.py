#!/usr/bin/env python3
"""
Quick test script to debug the position matching service
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_position_matching():
    print("🔍 Testing Position Matching Service...")

    try:
        from application.services.positioning.position_matching_service import (
            PositionMatchingService,
        )

        print("✅ Successfully imported PositionMatchingService")

        # Create the service
        position_service = PositionMatchingService()
        print("✅ Successfully created PositionMatchingService instance")

        # Test with alpha1 (what we expect from start position alpha1_alpha1)
        print("\n🎯 Testing get_next_options('alpha1')...")
        options = position_service.get_next_options("alpha1")

        print(f"📊 Results:")
        print(f"   - Number of options: {len(options) if options else 0}")

        if options:
            print(f"   - Option types: {[type(opt).__name__ for opt in options[:3]]}")
            letters = [
                opt.letter if hasattr(opt, "letter") else "N/A" for opt in options
            ]
            print(f"   - Letters found: {letters}")
        else:
            print("   - No options returned!")

    except Exception as e:
        print(f"❌ Error testing position matching: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_position_matching()
