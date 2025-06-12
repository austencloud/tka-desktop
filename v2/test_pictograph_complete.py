#!/usr/bin/env python3
"""
Enhanced test for v2 glyph rendering system with grid background and positioning validation.

This script tests the complete pictograph rendering including:
- Diamond grid background
- All four glyph types with correct positioning
- Position validation against v1 reference
"""

import sys
import os
from pathlib import Path

# Add v2 source to Python path
v2_src = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src))

from PyQt6.QtWidgets import QApplication, QGraphicsScene, QMainWindow, QGraphicsView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QPainter

# Import all renderers
from presentation.components.grid_renderer import GridRenderer
from presentation.components.elemental_glyph_renderer import ElementalGlyphRenderer
from presentation.components.vtg_glyph_renderer import VTGGlyphRenderer
from presentation.components.tka_glyph_renderer import TKAGlyphRenderer
from presentation.components.position_glyph_renderer import PositionGlyphRenderer

# Import models
from domain.models.core_models import VTGMode, ElementalType, LetterType


def test_complete_pictograph_rendering():
    """Test complete pictograph rendering with grid and all glyphs positioned correctly."""
    app = QApplication(sys.argv)

    print("🎨 Starting V2 Complete Pictograph Test...")
    print("=" * 60)

    # Create test scene
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 950, 950)
    scene.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

    # Initialize all renderers
    grid_renderer = GridRenderer(scene)
    elemental_renderer = ElementalGlyphRenderer(scene)
    vtg_renderer = VTGGlyphRenderer(scene)
    tka_renderer = TKAGlyphRenderer(scene)
    position_renderer = PositionGlyphRenderer(scene)

    print(f"📊 Initial scene items: {len(scene.items())}")

    # 1. Render diamond grid background (FIRST - as background layer)
    print("\n🔷 Step 1: Rendering Diamond Grid Background...")
    try:
        grid_renderer.render_grid()
        grid_items = len(scene.items())
        print(f"   ✅ Grid rendered successfully")
        print(f"   📊 Items after grid: {grid_items}")
        if scene.items():
            grid_item = scene.items()[-1]
            grid_pos = grid_item.pos()
            grid_rect = grid_item.boundingRect()
            print(f"   📍 Grid position: ({grid_pos.x():.1f}, {grid_pos.y():.1f})")
            print(f"   📏 Grid size: {grid_rect.width():.1f}x{grid_rect.height():.1f}")
    except Exception as e:
        print(f"   ❌ Grid rendering failed: {e}")

    # 2. Render elemental glyph (TOP-RIGHT)
    print("\n🔥 Step 2: Rendering Elemental Glyph (Fire - Top-Right)...")
    try:
        elemental_renderer.render_elemental_glyph(VTGMode.SPLIT_OPP, "Type1")
        elemental_items = len(scene.items())
        print(f"   ✅ Elemental glyph rendered successfully")
        print(f"   📊 Items after elemental: {elemental_items}")
        if elemental_items > grid_items:
            elemental_item = scene.items()[-(elemental_items - grid_items)]
            elemental_pos = elemental_item.pos()
            elemental_rect = elemental_item.boundingRect()
            print(
                f"   📍 Elemental position: ({elemental_pos.x():.1f}, {elemental_pos.y():.1f})"
            )
            print(
                f"   📏 Elemental size: {elemental_rect.width():.1f}x{elemental_rect.height():.1f}"
            )

            # Validate top-right positioning
            expected_x = 950 - elemental_rect.width() - (950 * 0.04)
            expected_y = 950 * 0.04
            x_ok = abs(elemental_pos.x() - expected_x) < 5
            y_ok = abs(elemental_pos.y() - expected_y) < 5
            print(
                f"   🎯 Position validation: X={'✅' if x_ok else '❌'}, Y={'✅' if y_ok else '❌'}"
            )
    except Exception as e:
        print(f"   ❌ Elemental rendering failed: {e}")

    # 3. Render VTG glyph (BOTTOM-RIGHT - FIXED)
    print("\n📊 Step 3: Rendering VTG Glyph (SO - Bottom-Right)...")
    try:
        vtg_renderer.render_vtg_glyph(VTGMode.SPLIT_OPP, "Type1")
        vtg_items = len(scene.items())
        print(f"   ✅ VTG glyph rendered successfully")
        print(f"   📊 Items after VTG: {vtg_items}")
        if vtg_items > elemental_items:
            vtg_item = scene.items()[-(vtg_items - elemental_items)]
            vtg_pos = vtg_item.pos()
            vtg_rect = vtg_item.boundingRect()
            print(f"   📍 VTG position: ({vtg_pos.x():.1f}, {vtg_pos.y():.1f})")
            print(f"   📏 VTG size: {vtg_rect.width():.1f}x{vtg_rect.height():.1f}")

            # Validate bottom-right positioning (FIXED)
            expected_x = 950 - vtg_rect.width() - (950 * 0.04)
            expected_y = 950 - vtg_rect.height() - (950 * 0.04)
            x_ok = abs(vtg_pos.x() - expected_x) < 5
            y_ok = abs(vtg_pos.y() - expected_y) < 5
            print(
                f"   🎯 Position validation: X={'✅' if x_ok else '❌'}, Y={'✅' if y_ok else '❌'}"
            )
            print(f"   🔧 Expected: ({expected_x:.1f}, {expected_y:.1f})")
    except Exception as e:
        print(f"   ❌ VTG rendering failed: {e}")

    # 4. Render TKA glyph (BOTTOM-LEFT)
    print("\n🔤 Step 4: Rendering TKA Glyph (A - Bottom-Left)...")
    try:
        tka_renderer.render_tka_glyph("A", LetterType.TYPE1, False, None)
        tka_items = len(scene.items())
        print(f"   ✅ TKA glyph rendered successfully")
        print(f"   📊 Items after TKA: {tka_items}")
        if tka_items > vtg_items:
            tka_item = scene.items()[-(tka_items - vtg_items)]
            tka_pos = tka_item.pos()
            tka_rect = tka_item.boundingRect()
            print(f"   📍 TKA position: ({tka_pos.x():.1f}, {tka_pos.y():.1f})")
            print(f"   📏 TKA size: {tka_rect.width():.1f}x{tka_rect.height():.1f}")

            # Validate bottom-left positioning
            letter_height = 60  # Approximate letter height
            expected_x = letter_height / 1.5
            expected_y = 950 - (letter_height * 1.7)
            x_ok = abs(tka_pos.x() - expected_x) < 20
            y_ok = abs(tka_pos.y() - expected_y) < 20
            print(
                f"   🎯 Position validation: X={'✅' if x_ok else '❌'}, Y={'✅' if y_ok else '❌'}"
            )
    except Exception as e:
        print(f"   ❌ TKA rendering failed: {e}")

    # 5. Render position glyph (TOP-CENTER - FIXED)
    print("\n🏹 Step 5: Rendering Position Glyph (α→β - Top-Center)...")
    try:
        position_renderer.render_position_glyph("alpha", "beta", "A")
        position_items = len(scene.items())
        print(f"   ✅ Position glyph rendered successfully")
        print(f"   📊 Items after position: {position_items}")
        if position_items > tka_items:
            position_item = scene.items()[-(position_items - tka_items)]
            position_pos = position_item.pos()
            position_rect = position_item.boundingRect()
            print(
                f"   📍 Position position: ({position_pos.x():.1f}, {position_pos.y():.1f})"
            )
            print(
                f"   📏 Position size: {position_rect.width():.1f}x{position_rect.height():.1f}"
            )

            # Validate top-center positioning (FIXED)
            expected_x = (950 - position_rect.width()) / 2
            expected_y = 50
            x_ok = abs(position_pos.x() - expected_x) < 5
            y_ok = abs(position_pos.y() - expected_y) < 5
            print(
                f"   🎯 Position validation: X={'✅' if x_ok else '❌'}, Y={'✅' if y_ok else '❌'}"
            )
            print(f"   🔧 Expected: ({expected_x:.1f}, {expected_y:.1f})")
    except Exception as e:
        print(f"   ❌ Position rendering failed: {e}")

    # Final summary
    final_items = len(scene.items())
    print(f"\n🎯 FINAL RESULTS:")
    print(f"   📊 Total scene items: {final_items}")
    print(f"   🔷 Grid: Background layer")
    print(f"   🔥 Elemental: Top-right corner")
    print(f"   📊 VTG: Bottom-right corner (FIXED)")
    print(f"   🔤 TKA: Bottom-left corner")
    print(f"   🏹 Position: Top-center (FIXED)")

    # Optional: Show the scene in a window for visual verification
    create_visual_test = True
    if create_visual_test:
        print(f"\n👁️ Creating visual test window...")
        window = QMainWindow()
        view = QGraphicsView(scene)
        view.setRenderHints(QPainter.RenderHint.Antialiasing)
        window.setCentralWidget(view)
        window.setWindowTitle("V2 Glyph Positioning Test - All Fixed")
        window.resize(1000, 1000)
        window.show()

        print(f"   ✅ Visual test window created")
        print(f"   👁️ Check that all glyphs are positioned correctly:")
        print(f"      - Diamond grid as background")
        print(f"      - Elemental glyph (fire) in TOP-RIGHT")
        print(f"      - VTG glyph (SO) in BOTTOM-RIGHT")
        print(f"      - TKA glyph (A) in BOTTOM-LEFT")
        print(f"      - Position glyph (α→β) in TOP-CENTER")

        # Keep the app running to see the visual result
        sys.exit(app.exec())

    print(f"\n✅ V2 Glyph Rendering Test Complete!")


if __name__ == "__main__":
    test_complete_pictograph_rendering()
