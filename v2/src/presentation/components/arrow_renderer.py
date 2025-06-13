"""
Arrow renderer for pictograph components.

Handles rendering of arrow elements with positioning, rotation, and mirroring.
"""

import os
import re
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from src.presentation.components.asset_utils import get_image_path
from src.domain.models.core_models import MotionData, Location, MotionType
from src.application.services.motion_orientation_service import (
    MotionOrientationService,
    Orientation,
)
from src.domain.models.pictograph_models import ArrowData, PictographData
from src.application.services.arrow_mirror_service import ArrowMirrorService
from src.application.services.arrow_positioning_service import ArrowPositioningService


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
            Location.NORTH: (0, -self.HAND_RADIUS),
            Location.EAST: (self.HAND_RADIUS, 0),
            Location.SOUTH: (0, self.HAND_RADIUS),
            Location.WEST: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST: (self.HAND_RADIUS * 0.707, -self.HAND_RADIUS * 0.707),
            Location.SOUTHEAST: (self.HAND_RADIUS * 0.707, self.HAND_RADIUS * 0.707),
            Location.SOUTHWEST: (-self.HAND_RADIUS * 0.707, self.HAND_RADIUS * 0.707),
            Location.NORTHWEST: (-self.HAND_RADIUS * 0.707, -self.HAND_RADIUS * 0.707),
        }

    def render_arrow(self, color: str, motion_data: MotionData) -> None:
        """Render an arrow using SVG files."""
        arrow_svg_path = self._get_arrow_svg_file(motion_data)

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

                self.scene.addItem(arrow_item)

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
        return self.location_coordinates.get(location, (0, 0))

    def _load_svg_file(self, file_path: str) -> str:
        """Load SVG file content as string."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
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
