#!/usr/bin/env python3
"""
Debug arrow bounding rect behavior to understand positioning.
"""

import sys
from pathlib import Path

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QGraphicsScene
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from src.presentation.components.asset_utils import get_image_path


def test_arrow_bounding_rect_debug():
    """Debug arrow bounding rect behavior with different rotations."""
    print("🔍 Arrow Bounding Rect Debug Test")
    print("=" * 50)
    
    # Create minimal Qt application for graphics items
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    scene = QGraphicsScene()
    
    # Test different arrow rotations
    test_rotations = [0, 45, 90, 135, 180, 225, 270, 315]
    arrow_svg_path = get_image_path("arrows/pro/from_radial/pro_1.0.svg")
    
    print(f"Testing arrow: {arrow_svg_path}")
    print(f"Arrow scale: 0.7")
    print()
    
    for rotation in test_rotations:
        print(f"🎯 Rotation: {rotation}°")
        print("-" * 30)
        
        # Create arrow item
        arrow_item = QGraphicsSvgItem()
        renderer = QSvgRenderer(arrow_svg_path)
        if renderer.isValid():
            arrow_item.setSharedRenderer(renderer)
            
            # Apply scale
            arrow_scale = 0.7
            arrow_item.setScale(arrow_scale)
            
            # Get bounds before rotation
            bounds_before = arrow_item.boundingRect()
            print(f"  Bounds before rotation: {bounds_before.width():.1f} x {bounds_before.height():.1f}")
            print(f"  Center before rotation: ({bounds_before.center().x():.1f}, {bounds_before.center().y():.1f})")
            
            # Set transform origin and apply rotation
            arrow_item.setTransformOriginPoint(bounds_before.center())
            arrow_item.setRotation(rotation)
            
            # Get bounds after rotation
            bounds_after = arrow_item.boundingRect()
            print(f"  Bounds after rotation: {bounds_after.width():.1f} x {bounds_after.height():.1f}")
            print(f"  Center after rotation: ({bounds_after.center().x():.1f}, {bounds_after.center().y():.1f})")
            
            # Calculate positioning using both methods
            target_x, target_y = 400.0, 300.0  # Example target position
            
            # Method 1: Using pre-rotation bounds (current implementation before fix)
            final_x_old = target_x - bounds_before.center().x()
            final_y_old = target_y - bounds_before.center().y()
            
            # Method 2: Using post-rotation bounds (fixed implementation)
            final_x_new = target_x - bounds_after.center().x()
            final_y_new = target_y - bounds_after.center().y()
            
            print(f"  Target position: ({target_x}, {target_y})")
            print(f"  setPos() with pre-rotation bounds: ({final_x_old:.1f}, {final_y_old:.1f})")
            print(f"  setPos() with post-rotation bounds: ({final_x_new:.1f}, {final_y_new:.1f})")
            
            # Calculate difference
            diff_x = final_x_new - final_x_old
            diff_y = final_y_new - final_y_old
            diff_magnitude = (diff_x**2 + diff_y**2)**0.5
            
            print(f"  Positioning difference: ({diff_x:.1f}, {diff_y:.1f}) magnitude: {diff_magnitude:.1f}")
            
            # Test actual visual center position
            if rotation == 0:
                print(f"  📋 Reference (0°): This should be our baseline")
            elif diff_magnitude > 1.0:
                print(f"  ⚠️  Significant difference detected!")
            else:
                print(f"  ✅ Minimal difference (< 1px)")
        
        print()
    
    print("=" * 50)
    print("🔍 ANALYSIS:")
    print("=" * 50)
    print("• If bounding rects change significantly with rotation:")
    print("  → Post-rotation bounds calculation is critical")
    print("  → Our fix should improve positioning accuracy")
    print()
    print("• If bounding rects remain similar across rotations:")
    print("  → The issue may be elsewhere in the positioning pipeline")
    print("  → Need to investigate quadrant adjustments or coordinate calculations")
    print()
    print("• If differences are minimal (< 1px):")
    print("  → The consistent distances might be correct")
    print("  → The positioning system may already be working as intended")


if __name__ == "__main__":
    test_arrow_bounding_rect_debug()
