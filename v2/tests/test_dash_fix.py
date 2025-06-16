#!/usr/bin/env python3
"""Test script to verify TKA glyph dash rendering fix."""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "v2", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), "legacy", "src"))

from PyQt6.QtWidgets import QApplication, QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from v2.src.domain.models.core_models import GlyphData
from legacy.src.enums.letter.letter_type import LetterType
from v2.src.presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)


def test_dash_rendering():
    """Test that Type3 letters don't get double dashes."""

    app = (
        QApplication(sys.argv)
        if not QApplication.instance()
        else QApplication.instance()
    )
    scene = QGraphicsScene()
    # Test Type3 letter (should have dash built into SVG, no additional dash)
    print("Testing Type3 letter 'W-':")
    type3_glyph_data = GlyphData(
        letter="W-", letter_type=LetterType.TYPE3, has_dash=True
    )

    renderer = TKAGlyphRenderer(scene)
    renderer.render_glyph(type3_glyph_data)

    # Count items in scene
    items = scene.items()
    print(f"Total items in scene: {len(items)}")

    # Find the TKA group
    tka_groups = [item for item in items if hasattr(item, "childItems")]
    if tka_groups:
        tka_group = tka_groups[0]
        child_count = len(tka_group.childItems())
        print(f"Children in TKA group: {child_count}")

        if child_count == 1:
            print(
                "✅ SUCCESS: Type3 letter has only 1 child (letter with built-in dash)"
            )
        else:
            print(
                f"❌ ISSUE: Type3 letter has {child_count} children (may have extra dash)"
            )
    else:
        print("❌ ERROR: No TKA group found")


if __name__ == "__main__":
    test_dash_rendering()
