#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-07-19
Test script to verify that VTG and elemental glyphs are properly hidden for Type 2 letters.

BUG REPORT: VTG and elemental glyphs showing for Type 2 letters when they shouldn't
EXPECTED: Type 2 letters (W,X,Y,Z,Σ,Δ,θ,Ω) should hide VTG and elemental glyphs
STATUS: NEEDS_TESTING
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_glyph_visibility_fix():
    """Test that Type 2 letters (W,X,Y,Z) don't show VTG/elemental glyphs."""
    print("🧪 Testing VTG and elemental glyph visibility fix...")

    try:
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )
        from domain.models.core_models import LetterType, BeatData

        # Initialize the service
        service = PictographManagementService()

        # Test cases: Type 2 letters that should NOT show VTG/elemental glyphs
        type2_letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]

        # Test cases: Type 1 letters that SHOULD show VTG/elemental glyphs
        type1_letters = ["A", "B", "D", "G"]

        all_passed = True

        print("\n--- Testing Type 2 letters (should NOT show VTG/elemental glyphs) ---")
        for letter in type2_letters:
            try:
                # Determine letter type using the service's method
                letter_type = service._determine_letter_type(letter)

                if letter_type != LetterType.TYPE2:
                    print(f"❌ Letter '{letter}': expected TYPE2, got {letter_type}")
                    all_passed = False
                    continue

                # Create dummy beat data to test glyph data generation
                beat_data = BeatData(letter=letter)
                glyph_data = service._generate_glyph_data(beat_data)

                if glyph_data:
                    if glyph_data.show_vtg:
                        print(
                            f"❌ Letter '{letter}': VTG glyph should be hidden but show_vtg=True"
                        )
                        all_passed = False
                        continue

                    if glyph_data.show_elemental:
                        print(
                            f"❌ Letter '{letter}': Elemental glyph should be hidden but show_elemental=True"
                        )
                        all_passed = False
                        continue

                    print(f"✅ Letter '{letter}': correctly hides VTG and elemental glyphs")
                else:
                    print(f"⚠️  Letter '{letter}': no glyph data generated")
                    
            except Exception as e:
                print(f"❌ Letter '{letter}': Error testing - {e}")
                all_passed = False

        print("\n--- Testing Type 1 letters (SHOULD show VTG/elemental glyphs) ---")
        for letter in type1_letters:
            try:
                # Determine letter type using the service's method
                letter_type = service._determine_letter_type(letter)

                if letter_type != LetterType.TYPE1:
                    print(f"❌ Letter '{letter}': expected TYPE1, got {letter_type}")
                    all_passed = False
                    continue

                # Create dummy beat data to test glyph data generation
                beat_data = BeatData(letter=letter)
                glyph_data = service._generate_glyph_data(beat_data)

                if glyph_data:
                    if not glyph_data.show_vtg:
                        print(
                            f"❌ Letter '{letter}': VTG glyph should be shown but show_vtg=False"
                        )
                        all_passed = False
                        continue

                    if not glyph_data.show_elemental:
                        print(
                            f"❌ Letter '{letter}': Elemental glyph should be shown but show_elemental=False"
                        )
                        all_passed = False
                        continue

                    print(f"✅ Letter '{letter}': correctly shows VTG and elemental glyphs")
                else:
                    print(f"⚠️  Letter '{letter}': no glyph data generated")
                    
            except Exception as e:
                print(f"❌ Letter '{letter}': Error testing - {e}")
                all_passed = False

        if all_passed:
            print(
                "\n🎉 All tests passed! VTG and elemental glyph visibility fix is working correctly!"
            )
            print(
                "✅ Type 2 letters (W,X,Y,Z,Σ,Δ,θ,Ω) now properly hide VTG and elemental glyphs"
            )
            print("✅ Type 1 letters still properly show VTG and elemental glyphs")
            return True
        else:
            print("\n❌ Some tests failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_glyph_visibility_fix_pytest():
    """Pytest version of the glyph visibility fix test."""
    result = test_glyph_visibility_fix()
    assert result, "Glyph visibility fix test failed"


if __name__ == "__main__":
    print("🧪 Starting Glyph Visibility Fix Test")
    print("=" * 50)
    success = test_glyph_visibility_fix()

    if success:
        print(f"\n🎉 GLYPH VISIBILITY FIX VERIFIED!")
        sys.exit(0)
    else:
        print(f"\n❌ FIX VERIFICATION FAILED")
        sys.exit(1)
