#!/usr/bin/env python3
"""
Test script to verify TKA glyph dash rendering for Type3 letters.
This script will test that Type3 letters don't get double dashes.
"""

import sys
import os

sys.path.append("v2/src")

from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow
from PyQt6.QtCore import Qt

from domain.models.core_models import LetterType, BeatData, GlyphData
from presentation.components.pictograph.renderers.tka_glyph_renderer import (
    TKAGlyphRenderer,
)


def test_type3_dash_rendering():
    """Test that Type3 letters don't get double dashes."""
    app = QApplication(sys.argv)

    # Create a scene for testing
    scene = QGraphicsScene()
    renderer = TKAGlyphRenderer(scene)

    # Test a Type3 letter (should have dash in SVG, no additional dash)
    print("Testing Type3 letter 'W-'...")
    renderer.render_tka_glyph(
        letter="W-", letter_type=LetterType.TYPE3, has_dash=True, turns_data=None
    )

    # Count items in scene
    items = scene.items()
    print(f"Total items in scene: {len(items)}")

    for i, item in enumerate(items):
        print(f"  Item {i}: {type(item).__name__}")
        if hasattr(item, "childItems"):
            child_items = item.childItems()
            print(f"    Child items: {len(child_items)}")
            for j, child in enumerate(child_items):
                print(f"      Child {j}: {type(child).__name__}")
    # Test a regular letter that should get a separate dash
    scene.clear()
    print("\nTesting Type5 letter 'Φ-' (should have built-in dash)...")
    renderer.render_tka_glyph(
        letter="Φ-", letter_type=LetterType.TYPE5, has_dash=True, turns_data=None
    )

    items = scene.items()
    print(f"Total items in scene: {len(items)}")

    for i, item in enumerate(items):
        print(f"  Item {i}: {type(item).__name__}")
        if hasattr(item, "childItems"):
            child_items = item.childItems()
            print(f"    Child items: {len(child_items)}")
            for j, child in enumerate(child_items):
                print(f"      Child {j}: {type(child).__name__}")
    # Test before our fix behavior (simulate Type2 with manual dash)
    scene.clear()
    print("\nTesting Type2 letter 'W-' with separate dash...")
    renderer.render_tka_glyph(
        letter="W-",
        letter_type=LetterType.TYPE2,
        has_dash=True,  # This should add separate dash
        turns_data=None,
    )

    items = scene.items()
    print(f"Total items in scene: {len(items)}")

    for i, item in enumerate(items):
        print(f"  Item {i}: {type(item).__name__}")
        if hasattr(item, "childItems"):
            child_items = item.childItems()
            print(f"    Child items: {len(child_items)}")
            for j, child in enumerate(child_items):
                print(f"      Child {j}: {type(child).__name__}")

    # Test Type6 letters (should never have dashes)
    scene.clear()
    print("\nTesting Type6 letter 'α' (should never have dash)...")
    renderer.render_tka_glyph(
        letter="α",
        letter_type=LetterType.TYPE6,
        has_dash=True,  # Even if has_dash=True, should not add dash
        turns_data=None,
    )

    items = scene.items()
    print(f"Total items in scene: {len(items)}")

    for i, item in enumerate(items):
        print(f"  Item {i}: {type(item).__name__}")
        if hasattr(item, "childItems"):
            child_items = item.childItems()
            print(f"    Child items: {len(child_items)}")
            for j, child in enumerate(child_items):
                print(f"      Child {j}: {type(child).__name__}")

    app.quit()


if __name__ == "__main__":
    test_type3_dash_rendering()
