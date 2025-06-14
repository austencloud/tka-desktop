#!/usr/bin/env python3
"""
Test script to verify TKA glyph dash rendering for Type3 letters.
This script will test that Type3 letters don't get double dashes.
"""

import sys
import os
sys.path.append('v2/src')

from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow
from PyQt6.QtCore import Qt

from domain.models.core_models import LetterType, BeatData, GlyphData
from presentation.components.pictograph.renderers.tka_glyph_renderer import TKAGlyphRenderer


def test_type3_dash_rendering():
    """Test that Type3 letters don't get double dashes."""
    app = QApplication(sys.argv)
    
    # Create a scene for testing
    scene = QGraphicsScene()
    renderer = TKAGlyphRenderer(scene)
    
    # Test a Type3 letter (should have dash in SVG, no additional dash)
    print("Testing Type3 letter 'W-'...")
    renderer.render_tka_glyph(
        letter="W-",
        letter_type=LetterType.TYPE3,
        has_dash=True,
        turns_data=None
    )
    
    # Count items in scene
    items = scene.items()
    print(f"Total items in scene: {len(items)}")
    
    # Look for TKA group
    tka_groups = [item for item in items if hasattr(item, 'childItems')]
    if tka_groups:
        tka_group = tka_groups[0]
        child_items = tka_group.childItems()
        print(f"Child items in TKA group: {len(child_items)}")
        
        # Should only be 1 item (the letter SVG with built-in dash)
        # If there are 2 items, that means there's an extra dash
        if len(child_items) == 1:
            print("✅ SUCCESS: Type3 letter has only 1 component (letter with built-in dash)")
        elif len(child_items) == 2:
            print("❌ FAILURE: Type3 letter has 2 components (extra dash added)")
        else:
            print(f"❓ UNEXPECTED: Type3 letter has {len(child_items)} components")
    
    # Test a regular letter that should get a separate dash
    scene.clear()
    print("\nTesting Type4 letter 'Φ' with dash...")
    renderer.render_tka_glyph(
        letter="Φ",
        letter_type=LetterType.TYPE4,
        has_dash=True,
        turns_data=None
    )
    
    items = scene.items()
    print(f"Total items in scene: {len(items)}")
    
    tka_groups = [item for item in items if hasattr(item, 'childItems')]
    if tka_groups:
        tka_group = tka_groups[0]
        child_items = tka_group.childItems()
        print(f"Child items in TKA group: {len(child_items)}")
        
        # Should be 2 items (letter SVG + separate dash)
        if len(child_items) == 2:
            print("✅ SUCCESS: Type4 letter has 2 components (letter + separate dash)")
        else:
            print(f"❓ UNEXPECTED: Type4 letter has {len(child_items)} components")
    
    app.quit()


if __name__ == "__main__":
    test_type3_dash_rendering()
