#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-07-19
Test script to verify TKA glyph dash rendering fix.

BUG REPORT: Type3 letters getting double dashes (built-in + additional)
EXPECTED: Type3 letters should only have built-in dash, no additional dash
STATUS: NEEDS_TESTING
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from PyQt6.QtWidgets import QApplication, QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


def test_dash_rendering():
    """Test that Type3 letters don't get double dashes."""

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        from domain.models.core_models import GlyphData, LetterType, BeatData
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        # Use the service to generate proper glyph data
        service = PictographManagementService()

        # Test Type3 letter (should have dash built into SVG, no additional dash)
        print("Testing Type3 letter 'W-':")

        # Create beat data with Type3 letter
        beat_data = BeatData(letter="W-")
        glyph_data = service._generate_glyph_data(beat_data)

        if not glyph_data:
            print("❌ No glyph data generated")
            return False

        print(f"Letter type: {glyph_data.letter_type}")
        print(f"Has dash: {glyph_data.has_dash}")
        print(f"Show TKA: {glyph_data.show_tka}")

        # Verify it's classified as TYPE3
        if glyph_data.letter_type != LetterType.TYPE3:
            print(f"❌ Expected TYPE3, got {glyph_data.letter_type}")
            return False

        # Verify it has dash flag set
        if not glyph_data.has_dash:
            print("❌ Expected has_dash=True for W-")
            return False

        print("✅ SUCCESS: Type3 letter properly classified with dash flag")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Required components not available for testing")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_dash_rendering_multiple_types():
    """Test dash rendering for multiple letter types."""

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        from domain.models.core_models import GlyphData, LetterType, BeatData
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        service = PictographManagementService()
        all_passed = True

        # Test cases: Type3 letters with built-in dashes
        type3_test_cases = ["W-", "X-", "Y-", "Z-"]

        print("\n--- Testing Type3 letters (should have built-in dash only) ---")
        for letter in type3_test_cases:
            beat_data = BeatData(letter=letter)
            glyph_data = service._generate_glyph_data(beat_data)

            if not glyph_data:
                print(f"❌ Letter '{letter}': No glyph data generated")
                all_passed = False
                continue

            # Verify it's classified as TYPE3
            if glyph_data.letter_type != LetterType.TYPE3:
                print(
                    f"❌ Letter '{letter}': Expected TYPE3, got {glyph_data.letter_type}"
                )
                all_passed = False
                continue

            # Verify it has dash flag set
            if not glyph_data.has_dash:
                print(f"❌ Letter '{letter}': Expected has_dash=True")
                all_passed = False
                continue

            print(f"✅ Letter '{letter}': Correct TYPE3 classification with dash")

        # Test non-dash letters
        print("\n--- Testing non-dash letters (should not have dash flag) ---")
        non_dash_letters = ["W", "X", "Y", "Z", "A", "B"]

        for letter in non_dash_letters:
            beat_data = BeatData(letter=letter)
            glyph_data = service._generate_glyph_data(beat_data)

            if glyph_data and glyph_data.has_dash:
                print(f"❌ Letter '{letter}': Should not have dash flag")
                all_passed = False
            else:
                print(f"✅ Letter '{letter}': Correctly no dash flag")

        return all_passed

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_dash_fix_pytest():
    """Pytest version of the dash fix test."""
    result1 = test_dash_rendering()
    result2 = test_dash_rendering_multiple_types()
    assert result1 and result2, "Dash fix test failed"


if __name__ == "__main__":
    print("🧪 Starting Dash Fix Test")
    print("=" * 50)

    success1 = test_dash_rendering()
    success2 = test_dash_rendering_multiple_types()

    overall_success = success1 and success2

    if overall_success:
        print("\n✅ All dash fix tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some dash fix tests failed")
        sys.exit(1)
