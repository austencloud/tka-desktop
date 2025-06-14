"""
Arrow renderer for pictograph components.

Handles rendering of arrow elements with positioning, rotation, and mirroring.
"""

import os
import re
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import get_image_path
from domain.models.core_models import MotionData, Location, MotionType
from domain.models.pictograph_models import ArrowData, PictographData
from application.services.arrow_mirror_service import ArrowMirrorService
from application.services.arrow_positioning_service import ArrowPositioningService


class ArrowRenderer:
    """Handles arrow rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1

        self.arrow_mirroring_service = ArrowMirrorService()
        self.arrow_positioning_service = ArrowPositioningService()

        self.location_coordinates = {
            Location.NORTH.value: (0, -self.HAND_RADIUS),
            Location.EAST.value: (self.HAND_RADIUS, 0),
            Location.SOUTH.value: (0, self.HAND_RADIUS),
            Location.WEST.value: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.NORTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
        }

    def render_arrow(self, color: str, motion_data: MotionData) -> None:
        """Render an arrow using SVG files."""
        arrow_svg_path = self._get_arrow_svg_file(motion_data)
        print(
            f"Arrow render: {color} {motion_data.motion_type} - SVG exists: {os.path.exists(arrow_svg_path)}"
        )

        if os.path.exists(arrow_svg_path):
            arrow_item = QGraphicsSvgItem()

            # Apply color transformation to SVG data
            svg_data = self._load_svg_file(arrow_svg_path)
            colored_svg_data = self._apply_color_transformation(svg_data, color)

            renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
            if renderer.isValid():
                arrow_item.setSharedRenderer(renderer)

                # NO INDIVIDUAL SCALING - positioning service assumes full-size scene
                # All scaling will be applied to the entire scene as final step

                position_x, position_y, rotation = (
                    self._calculate_arrow_position_with_service(color, motion_data)
                )
                print(
                    f"Arrow position: {color} at ({position_x:.1f}, {position_y:.1f})"
                )

                # CRITICAL: Set transform origin to arrow's visual center BEFORE rotation
                bounds = arrow_item.boundingRect()
                arrow_item.setTransformOriginPoint(bounds.center())

                # Now apply rotation around the visual center
                arrow_item.setRotation(rotation)

                arrow_data = ArrowData(
                    motion_data=motion_data,
                    color=color,
                    turns=motion_data.turns,
                    position_x=position_x,
                    position_y=position_y,
                    rotation_angle=rotation,
                )
                self.arrow_mirroring_service.update_arrow_mirror(arrow_item, arrow_data)

                # POSITIONING FORMULA:
                # Get bounding rect AFTER all transformations (scaling + rotation)
                # This ensures we have the correct bounds for positioning calculation
                final_bounds = arrow_item.boundingRect()

                # final_pos = calculated_pos - bounding_rect_center
                # This ensures the arrow's visual center appears exactly at the calculated position
                # regardless of rotation angle, achieving pixel-perfect positioning accuracy
                final_x = position_x - final_bounds.center().x()
                final_y = position_y - final_bounds.center().y()

                arrow_item.setPos(final_x, final_y)
                arrow_item.setZValue(100)  # Bring arrows to front
                print(
                    f"Arrow added to scene: {color} at setPos({final_x:.1f}, {final_y:.1f})"
                )
                self.scene.addItem(arrow_item)
            else:
                print(f"Invalid SVG renderer for {color} arrow")
        else:
            print(f"Missing SVG: {arrow_svg_path}")

    def _get_arrow_svg_file(self, motion_data: MotionData) -> str:
        """Get the correct arrow SVG file path with proper motion type mapping."""
        turns_str = f"{motion_data.turns:.1f}"

        if motion_data.motion_type == MotionType.STATIC:
            return get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.PRO:
            return get_image_path(f"arrows/pro/from_radial/pro_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.ANTI:
            return get_image_path(f"arrows/anti/from_radial/anti_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.DASH:
            return get_image_path(f"arrows/dash/from_radial/dash_{turns_str}.svg")
        elif motion_data.motion_type == MotionType.FLOAT:
            return get_image_path("arrows/float.svg")
        else:
            # Fallback to static for unknown motion types
            return get_image_path(f"arrows/static/from_radial/static_{turns_str}.svg")

    def _calculate_arrow_position_with_service(
        self, color: str, motion_data: MotionData
    ) -> tuple[float, float, float]:
        """Calculate arrow position using the complete positioning service."""
        arrow_data = ArrowData(
            motion_data=motion_data,
            color=color,
            turns=motion_data.turns,
        )

        pictograph_data = PictographData(arrows={color: arrow_data})

        return self.arrow_positioning_service.calculate_arrow_position(
            arrow_data, pictograph_data
        )

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location.value, (0, 0))

    def _load_svg_file(self, file_path: str) -> str:
        """Load SVG file content as string."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

                # Extract dimensions from SVG content for debugging
                import re

                width_match = re.search(r'width="([^"]*)"', content)
                height_match = re.search(r'height="([^"]*)"', content)
                viewbox_match = re.search(r'viewBox="([^"]*)"', content)

                width = width_match.group(1) if width_match else "not found"
                height = height_match.group(1) if height_match else "not found"
                viewbox = viewbox_match.group(1) if viewbox_match else "not found"

                print(f"✓ Loaded SVG from: {file_path}")
                print(f"  📏 Dimensions: width={width}, height={height}")
                print(f"  📐 ViewBox: {viewbox}")
                print(f"  📄 Content length: {len(content)} characters")

                # Check if this is an empty/invisible SVG
                if width == "0" or height == "0":
                    print(
                        f"  ⚠️  WARNING: SVG has zero dimensions! This arrow will be invisible."
                    )

                return content
        except Exception as e:
            print(f"Error loading SVG file {file_path}: {e}")
            return ""

    def _apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data based on arrow color."""
        if not svg_data:
            return svg_data

        # Color mapping based on reference implementation
        COLOR_MAP = {
            "blue": "#2E3192",  # Reference blue color
            "red": "#ED1C24",  # Reference red color
        }

        target_color = COLOR_MAP.get(color.lower(), "#2E3192")  # Default to blue

        # Pattern to match CSS fill properties in SVG
        # This matches both fill attributes and CSS style properties
        patterns = [
            # CSS fill property: fill="#color"
            re.compile(r'(fill=")([^"]*)(")'),
            # CSS style attribute: fill: #color;
            re.compile(r"(fill:\s*)([^;]*)(;)"),
            # Class definition: .st0 { fill: #color; }
            re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
        ]

        # Apply color transformation using all patterns
        for pattern in patterns:
            svg_data = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())), svg_data
            )

        return svg_data
