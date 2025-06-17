"""
Arrow renderer for pictograph components.

Handles rendering of arrow elements with positioning, rotation, and mirroring.
"""

import os
import re
from typing import Optional, TYPE_CHECKING
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from presentation.components.pictograph.asset_utils import get_image_path
from domain.models.core_models import MotionData, Location, MotionType
from domain.models.pictograph_models import ArrowData, PictographData
from application.services.positioning.arrow_management_service import (
    ArrowManagementService,
)

if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene


class ArrowRenderer:
    """Handles arrow rendering for pictographs."""

    def __init__(self, scene: "PictographScene"):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1

        self.arrow_service = ArrowManagementService()

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

    def render_arrow(
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: Optional[PictographData] = None,
    ) -> None:
        """Render an arrow using SVG files."""
        # CRITICAL FIX: Static motions with 0 turns should be completely invisible
        if motion_data.motion_type == MotionType.STATIC and motion_data.turns == 0.0:
            return

        arrow_svg_path = self._get_arrow_svg_file(motion_data)

        if os.path.exists(arrow_svg_path):
            arrow_item = QGraphicsSvgItem()

            # Apply color transformation to SVG data
            svg_data = self._load_svg_file(arrow_svg_path)
            colored_svg_data = self._apply_color_transformation(svg_data, color)

            renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
            if renderer.isValid():
                arrow_item.setSharedRenderer(renderer)

                position_x, position_y, rotation = (
                    self._calculate_arrow_position_with_service(
                        color, motion_data, full_pictograph_data
                    )
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
                self.arrow_service.apply_mirror_transform(
                    arrow_item, self.arrow_service.should_mirror_arrow(arrow_data)
                )

                # POSITIONING FORMULA:
                # Get bounding rect AFTER all transformations (scaling + rotation)
                # This ensures we have the correct bounds for positioning calculation
                final_bounds = (
                    arrow_item.boundingRect()
                )  # final_pos = calculated_pos - bounding_rect_center
                # This ensures the arrow's visual center appears exactly at the calculated position
                # regardless of rotation angle, achieving pixel-perfect positioning accuracy
                final_x = position_x - final_bounds.center().x()
                final_y = position_y - final_bounds.center().y()

                arrow_item.setPos(final_x, final_y)
                arrow_item.setZValue(100)  # Bring arrows to front
                self.scene.addItem(arrow_item)
            else:
                pass  # Invalid SVG renderer
        else:
            pass  # Missing SVG file

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
        self,
        color: str,
        motion_data: MotionData,
        full_pictograph_data: Optional[PictographData] = None,
    ) -> tuple[float, float, float]:
        """Calculate arrow position using the complete positioning service."""
        arrow_data = ArrowData(
            motion_data=motion_data,
            color=color,
            turns=motion_data.turns,
        )  # Use full pictograph data if available for Type 3 detection
        if full_pictograph_data:
            pictograph_data = full_pictograph_data
        else:
            pictograph_data = PictographData(arrows={color: arrow_data})

        return self.arrow_service.calculate_arrow_position(arrow_data, pictograph_data)

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location.value, (0, 0))

    def _load_svg_file(self, file_path: str) -> str:
        """Load SVG file content as string."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

                # Extract dimensions from SVG content for debugging
                width_match = re.search(r'width="([^"]*)"', content)
                height_match = re.search(r'height="([^"]*)"', content)
                viewbox_match = re.search(r'viewBox="([^"]*)"', content)

                # Store for potential debugging use
                _ = width_match.group(1) if width_match else "not found"
                _ = height_match.group(1) if height_match else "not found"
                _ = viewbox_match.group(1) if viewbox_match else "not found"

                return content
        except Exception:
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
