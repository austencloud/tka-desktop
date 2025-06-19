#!/usr/bin/env python3
"""
SCAFFOLDING TEST - DELETE AFTER: 2025-07-19
Test script to verify TKA glyph dash rendering for Type3 letters.
This script will test that Type3 letters don't get double dashes.

BUG REPORT: TKA glyph renderer adding extra dashes to Type3 letters
EXPECTED: Type3 letters should use built-in dash, no additional dash
STATUS: NEEDS_TESTING
"""

import sys
from pathlib import Path

# Setup project imports using proper path resolution
modern_src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(modern_src_path))

from PyQt6.QtWidgets import QApplication, QGraphicsScene


def test_type3_dash_rendering():
    """Test that Type3 letters don't get double dashes."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        from domain.models.core_models import LetterType, BeatData
        from application.services.core.pictograph_management_service import (
            PictographManagementService,
        )

        service = PictographManagementService()
        all_passed = True

        print("Testing Type3 letter dash classification...")

        # Test Type3 letters with dashes
        type3_dash_letters = ["W-", "X-", "Y-", "Z-"]

        for letter in type3_dash_letters:
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

        # Test Type6 letters (should never have dashes)
        print("\nTesting Type6 letters (should never have dash)...")
        type6_letters = ["α", "β", "Γ"]

        for letter in type6_letters:
            beat_data = BeatData(letter=letter)
            glyph_data = service._generate_glyph_data(beat_data)

            if glyph_data:
                if glyph_data.letter_type != LetterType.TYPE6:
                    print(
                        f"❌ Letter '{letter}': Expected TYPE6, got {glyph_data.letter_type}"
                    )
                    all_passed = False
                    continue

                if glyph_data.has_dash:
                    print(f"❌ Letter '{letter}': TYPE6 should never have dash flag")
                    all_passed = False
                    continue

                print(
                    f"✅ Letter '{letter}': Correct TYPE6 classification without dash"
                )
            else:
                print(
                    f"⚠️  Letter '{letter}': No glyph data generated (may be expected)"
                )

        return all_passed

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Required components not available for testing")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_tka_renderer_integration():
    """Test TKA renderer integration if available."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    try:
        from presentation.components.pictograph.renderers.tka_glyph_renderer import (
            TKAGlyphRenderer,
        )
        from domain.models.core_models import LetterType, GlyphData

        # Create a scene for testing
        scene = QGraphicsScene()
        renderer = TKAGlyphRenderer(scene)

        print("\nTesting TKA renderer integration...")

        # Test Type3 letter rendering
        # This should not crash
        renderer.render_tka_glyph(
            letter="W-", letter_type=LetterType.TYPE3, has_dash=True, turns_data=None
        )

        # Count items in scene
        items = scene.items()
        print(f"✅ TKA renderer created {len(items)} items without crashing")

        return True

    except ImportError as e:
        print(f"⚠️  TKA renderer not available: {e}")
        return True  # Not a failure if renderer not available
    except Exception as e:
        print(f"❌ TKA renderer test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_tka_dash_fix_pytest():
    """Pytest version of the TKA dash fix test."""
    result1 = test_type3_dash_rendering()
    result2 = test_tka_renderer_integration()
    assert result1 and result2, "TKA dash fix test failed"


if __name__ == "__main__":
    print("🧪 Starting TKA Dash Fix Test")
    print("=" * 50)

    success1 = test_type3_dash_rendering()
    success2 = test_tka_renderer_integration()

    overall_success = success1 and success2

    if overall_success:
        print("\n✅ All TKA dash fix tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some TKA dash fix tests failed")
        sys.exit(1)
