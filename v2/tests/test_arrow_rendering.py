#!/usr/bin/env python3
"""
Test script to verify arrow rendering pipeline in V2 pictograph system.
"""

import sys
import os

sys.path.append("src")

from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView
from PyQt6.QtCore import Qt
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from src.domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)
from src.presentation.components.pictograph.renderers.arrow_renderer import (
    ArrowRenderer,
)
from src.presentation.components.pictograph.pictograph_scene import PictographScene


def test_svg_loading():
    """Test basic SVG loading functionality."""
    print("=== Testing SVG Loading ===")

    from src.presentation.components.pictograph.asset_utils import get_image_path

    # Test different motion types
    test_cases = [
        ("PRO", "arrows/pro/from_radial/pro_1.0.svg"),
        ("STATIC", "arrows/static/from_radial/static_0.0.svg"),
        ("ANTI", "arrows/anti/from_radial/anti_1.0.svg"),
        ("DASH", "arrows/dash/from_radial/dash_1.0.svg"),
    ]

    for motion_type, svg_path in test_cases:
        full_path = get_image_path(svg_path)
        exists = os.path.exists(full_path)
        print(f"{motion_type}: {svg_path} -> {exists}")

        if exists:
            # Test SVG renderer
            renderer = QSvgRenderer(full_path)
            valid = renderer.isValid()
            print(f"  SVG renderer valid: {valid}")

            if valid:
                # Test QGraphicsSvgItem
                item = QGraphicsSvgItem()
                item.setSharedRenderer(renderer)
                bounds = item.boundingRect()
                print(f"  Bounding rect: {bounds.width()}x{bounds.height()}")
        print()


def test_motion_data_to_svg_mapping():
    """Test motion data to SVG file mapping."""
    print("=== Testing Motion Data to SVG Mapping ===")

    # Create test motion data
    test_motions = [
        MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.WEST,
            end_loc=Location.NORTH,
            turns=1.0,
            start_ori="in",
            end_ori="out",
        ),
        MotionData(
            motion_type=MotionType.STATIC,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.SOUTH,
            end_loc=Location.SOUTH,
            turns=0.0,
            start_ori="in",
            end_ori="in",
        ),
    ]

    # Create a dummy scene for testing
    scene = PictographScene()
    arrow_renderer = ArrowRenderer(scene)

    for i, motion_data in enumerate(test_motions):
        print(f"Motion {i+1}: {motion_data.motion_type.value}")
        svg_path = arrow_renderer._get_arrow_svg_file(motion_data)
        exists = os.path.exists(svg_path)
        print(f"  SVG path: {svg_path}")
        print(f"  File exists: {exists}")

        if exists:
            # Test SVG content loading
            svg_content = arrow_renderer._load_svg_file(svg_path)
            has_content = len(svg_content) > 0
            print(f"  SVG content loaded: {has_content}")

            # Test color transformation
            colored_svg = arrow_renderer._apply_color_transformation(
                svg_content, "blue"
            )
            has_blue_color = "#2E3192" in colored_svg
            print(f"  Color transformation applied: {has_blue_color}")
        print()


def test_svg_renderer_creation():
    """Test SVG renderer creation without full scene."""
    print("=== Testing SVG Renderer Creation ===")

    from src.presentation.components.pictograph.asset_utils import get_image_path

    # Test creating SVG renderer directly
    svg_path = get_image_path("arrows/pro/from_radial/pro_1.0.svg")
    print(f"Testing SVG path: {svg_path}")
    print(f"File exists: {os.path.exists(svg_path)}")

    if os.path.exists(svg_path):
        # Test file content
        try:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"SVG content length: {len(content)} characters")
                print(f"Contains <svg>: {'<svg' in content}")
                print(f"Contains viewBox: {'viewBox' in content}")
        except Exception as e:
            print(f"Error reading SVG file: {e}")

        # Test QSvgRenderer creation
        try:
            renderer = QSvgRenderer(svg_path)
            print(f"QSvgRenderer created: {renderer is not None}")
            print(f"QSvgRenderer valid: {renderer.isValid()}")
            if renderer.isValid():
                default_size = renderer.defaultSize()
                print(f"Default size: {default_size.width()}x{default_size.height()}")
        except Exception as e:
            print(f"Error creating QSvgRenderer: {e}")
            import traceback

            traceback.print_exc()


def test_color_transformation():
    """Test SVG color transformation without Qt objects."""
    print("=== Testing Color Transformation ===")

    from src.presentation.components.pictograph.asset_utils import get_image_path

    svg_path = get_image_path("arrows/pro/from_radial/pro_1.0.svg")

    if os.path.exists(svg_path):
        try:
            # Load SVG content
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            print(f"Original SVG length: {len(svg_content)}")

            # Test color transformation logic (without creating ArrowRenderer)
            import re

            COLOR_MAP = {
                "blue": "#2E3192",
                "red": "#ED1C24",
            }

            target_color = COLOR_MAP.get("blue", "#2E3192")

            patterns = [
                re.compile(r'(fill=")([^"]*)(")'),
                re.compile(r"(fill:\s*)([^;]*)(;)"),
                re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
            ]

            transformed_svg = svg_content
            for pattern in patterns:
                transformed_svg = pattern.sub(
                    lambda m: m.group(1) + target_color + m.group(len(m.groups())),
                    transformed_svg,
                )

            print(f"Transformed SVG length: {len(transformed_svg)}")
            print(f"Contains target color: {target_color in transformed_svg}")

        except Exception as e:
            print(f"Error in color transformation test: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    print("Arrow Rendering Pipeline Test")
    print("=" * 40)

    test_svg_loading()
    test_motion_data_to_svg_mapping()
    test_svg_renderer_creation()
    test_color_transformation()

    print("Test completed.")
