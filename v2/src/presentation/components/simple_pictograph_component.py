"""
Simple pictograph component for Kinetic Constructor v2.

This component renders pictographs using V2 SVG assets with modern architecture.
"""

import os
from typing import Optional
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QWidget,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QBrush, QColor

from ...domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from ...application.services.arrow_mirror_service import ArrowMirrorService
from ...application.services.arrow_positioning_service import ArrowPositioningService
from ...domain.models.pictograph_models import ArrowData, PictographData


def get_image_path(filename: str) -> str:
    """Get the path to an image file from the V2 assets directory."""
    assets_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "assets",
        "images",
        filename,
    )
    normalized_path = os.path.normpath(assets_path)

    if not os.path.exists(normalized_path):
        print(f"Warning: Asset not found: {normalized_path}")
        print("Please ensure required assets are in v2/src/assets/images/")

    return normalized_path


class SimplePictographScene(QGraphicsScene):
    """Graphics scene for rendering pictographs using V2 assets."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.beat_data: Optional[BeatData] = None

        self.arrow_mirroring_service = ArrowMirrorService()
        self.arrow_positioning_service = ArrowPositioningService()

        self.SCENE_SIZE = 950
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.RADIUS = 300
        self.HAND_RADIUS = 143.1

        self.setSceneRect(0, 0, self.SCENE_SIZE, self.SCENE_SIZE)
        self.setBackgroundBrush(QBrush(QColor(255, 255, 255)))

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

    def update_beat(self, beat_data: BeatData) -> None:
        """Update the scene with new beat data."""
        self.beat_data = beat_data
        self.clear()
        self._render_pictograph()

    def _render_pictograph(self) -> None:
        """Render the pictograph elements."""
        if not self.beat_data:
            print("🔍 RENDER DEBUG: No beat_data")
            return

        print(f"🔍 RENDER DEBUG: beat_data.letter = {self.beat_data.letter}")
        print(f"🔍 RENDER DEBUG: beat_data.blue_motion = {self.beat_data.blue_motion}")
        print(f"🔍 RENDER DEBUG: beat_data.red_motion = {self.beat_data.red_motion}")

        # Render grid (always box grid for now)
        self._render_grid()

        # Render props for blue and red motions
        if self.beat_data.blue_motion:
            print("🔍 RENDER DEBUG: Rendering blue prop")
            self._render_prop("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            print("🔍 RENDER DEBUG: Rendering red prop")
            self._render_prop("red", self.beat_data.red_motion)

        # Render arrows for blue and red motions
        if self.beat_data.blue_motion:
            print("🔍 RENDER DEBUG: Rendering blue arrow")
            self._render_arrow("blue", self.beat_data.blue_motion)
        if self.beat_data.red_motion:
            print("🔍 RENDER DEBUG: Rendering red arrow")
            self._render_arrow("red", self.beat_data.red_motion)

        # Render letter
        self._render_letter()

    def _render_grid(self) -> None:
        """Render the grid using SVG assets."""
        grid_svg_path = get_image_path("grid/diamond_grid.svg")

        if os.path.exists(grid_svg_path):
            grid_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(grid_svg_path)

            if renderer.isValid():
                grid_item.setSharedRenderer(renderer)
                grid_item.setScale(1.0)
                grid_item.setPos(0, 0)
                self.addItem(grid_item)

    def _render_prop(self, color: str, motion_data: MotionData) -> None:
        """Render a prop using SVG files with exact scaling and rotation."""
        prop_svg_path = get_image_path("props/simple_staff.svg")

        if os.path.exists(prop_svg_path):
            prop_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(prop_svg_path)
            if renderer.isValid():
                prop_item.setSharedRenderer(renderer)

                prop_scale = 0.8
                prop_item.setScale(prop_scale)

                end_pos = self._get_location_position(motion_data.end_loc)
                target_hand_point_x = self.CENTER_X + end_pos[0]
                target_hand_point_y = self.CENTER_Y + end_pos[1]

                prop_rotation = self._calculate_prop_rotation(motion_data)
                bounds = prop_item.boundingRect()
                prop_item.setTransformOriginPoint(bounds.center())
                prop_item.setRotation(prop_rotation)

                self._place_prop_at_hand_point(
                    prop_item, target_hand_point_x, target_hand_point_y
                )

                self.addItem(prop_item)

    def _place_prop_at_hand_point(
        self, prop_item: QGraphicsSvgItem, target_x: float, target_y: float
    ) -> None:
        """Position prop using coordinate system approach."""
        from PyQt6.QtCore import QPointF

        bounds = prop_item.boundingRect()
        center_point_in_local_coords = bounds.center()
        center_point_in_scene = prop_item.mapToScene(center_point_in_local_coords)
        target_hand_point = QPointF(target_x, target_y)
        offset = target_hand_point - center_point_in_scene
        new_position = prop_item.pos() + offset
        prop_item.setPos(new_position)

    def _render_arrow(self, color: str, motion_data: MotionData) -> None:
        """Render an arrow using SVG files."""
        arrow_svg_path = self._get_arrow_svg_file(motion_data)

        if os.path.exists(arrow_svg_path):
            arrow_item = QGraphicsSvgItem()
            renderer = QSvgRenderer(arrow_svg_path)
            if renderer.isValid():
                arrow_item.setSharedRenderer(renderer)

                arrow_scale = 0.7
                arrow_item.setScale(arrow_scale)

                position_x, position_y, rotation = (
                    self._calculate_arrow_position_with_service(color, motion_data)
                )

                print(
                    f"🔍 VISUAL DEBUG {color} arrow: service returned ({position_x:.1f}, {position_y:.1f}) @ {rotation:.1f}°"
                )

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

                bounds = arrow_item.boundingRect()
                final_x = position_x - (bounds.width() * arrow_scale) / 2
                final_y = position_y - (bounds.height() * arrow_scale) / 2

                print(
                    f"🔍 VISUAL DEBUG {color} arrow: bounds {bounds.width():.1f}x{bounds.height():.1f}, scale {arrow_scale}"
                )
                print(
                    f"🔍 VISUAL DEBUG {color} arrow: centering offset ({(bounds.width() * arrow_scale) / 2:.1f}, {(bounds.height() * arrow_scale) / 2:.1f})"
                )
                print(
                    f"🔍 VISUAL DEBUG {color} arrow: FINAL setPos({final_x:.1f}, {final_y:.1f})"
                )

                arrow_item.setPos(final_x, final_y)

                self.addItem(arrow_item)

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
        # Create arrow data for the positioning service
        arrow_data = ArrowData(
            motion_data=motion_data,
            color=color,
            turns=motion_data.turns,
        )

        # Create minimal pictograph data for the service
        pictograph_data = PictographData(arrows={color: arrow_data})

        # Use the positioning service to calculate position and rotation
        return self.arrow_positioning_service.calculate_arrow_position(
            arrow_data, pictograph_data
        )

    def _calculate_arrow_position(
        self, motion_data: MotionData
    ) -> tuple[float, float, float]:
        """Calculate arrow position and rotation using exact algorithms."""
        if motion_data.motion_type == MotionType.STATIC:
            start_pos = self._get_location_position(motion_data.start_loc)
            x = self.CENTER_X + start_pos[0] * 0.7
            y = self.CENTER_Y + start_pos[1] * 0.7
            rotation = self._calculate_static_rotation(motion_data.start_loc)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.PRO:
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.CENTER_X + arrow_pos[0]
            y = self.CENTER_Y + arrow_pos[1]
            rotation = self._calculate_pro_rotation(motion_data, arrow_location)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.ANTI:
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.CENTER_X + arrow_pos[0]
            y = self.CENTER_Y + arrow_pos[1]
            rotation = self._calculate_anti_rotation(motion_data, arrow_location)
            return x, y, rotation
        elif motion_data.motion_type == MotionType.DASH:
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.CENTER_X + arrow_pos[0]
            y = self.CENTER_Y + arrow_pos[1]
            rotation = self._calculate_dash_rotation(motion_data, arrow_location)
            return x, y, rotation
        else:
            arrow_location = self._calculate_arrow_location(motion_data)
            arrow_pos = self._get_location_position(arrow_location)
            x = self.CENTER_X + arrow_pos[0]
            y = self.CENTER_Y + arrow_pos[1]

            if motion_data.motion_type == MotionType.FLOAT:
                rotation = self._calculate_float_rotation(motion_data, arrow_location)
            else:
                rotation = self._calculate_motion_rotation((0, 0), arrow_pos)
            return x, y, rotation

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location, (0, 0))

    def _calculate_static_rotation(self, location: Location) -> float:
        """Calculate rotation for static arrows."""
        location_angles = {
            Location.NORTH: 180.0,
            Location.NORTHEAST: 225.0,
            Location.EAST: 270.0,
            Location.SOUTHEAST: 315.0,
            Location.SOUTH: 0.0,
            Location.SOUTHWEST: 45.0,
            Location.WEST: 90.0,
            Location.NORTHWEST: 135.0,
        }
        return location_angles.get(location, 0.0)

    def _calculate_arrow_location(self, motion_data: MotionData) -> Location:
        """Calculate arrow location based on motion data."""
        if motion_data.motion_type == MotionType.STATIC:
            return motion_data.start_loc
        elif motion_data.motion_type in [
            MotionType.PRO,
            MotionType.ANTI,
            MotionType.FLOAT,
        ]:
            return self._calculate_shift_arrow_location(
                motion_data.start_loc, motion_data.end_loc
            )
        elif motion_data.motion_type == MotionType.DASH:
            if motion_data.turns == 0:
                return motion_data.start_loc
            else:
                return self._calculate_shift_arrow_location(
                    motion_data.start_loc, motion_data.end_loc
                )
        else:
            return motion_data.start_loc

    def _calculate_shift_arrow_location(
        self, start_loc: Location, end_loc: Location
    ) -> Location:
        """Calculate arrow location for shift motions."""
        direction_pairs = {
            frozenset({Location.NORTH, Location.EAST}): Location.NORTHEAST,
            frozenset({Location.EAST, Location.SOUTH}): Location.SOUTHEAST,
            frozenset({Location.SOUTH, Location.WEST}): Location.SOUTHWEST,
            frozenset({Location.WEST, Location.NORTH}): Location.NORTHWEST,
            frozenset({Location.NORTHEAST, Location.NORTHWEST}): Location.NORTH,
            frozenset({Location.NORTHEAST, Location.SOUTHEAST}): Location.EAST,
            frozenset({Location.SOUTHWEST, Location.SOUTHEAST}): Location.SOUTH,
            frozenset({Location.NORTHWEST, Location.SOUTHWEST}): Location.WEST,
        }
        return direction_pairs.get(frozenset({start_loc, end_loc}), start_loc)

    def _calculate_pro_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for pro arrows."""
        direction_map = {
            RotationDirection.CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            },
            RotationDirection.COUNTER_CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            },
        }
        prop_rot_dir = motion_data.prop_rot_dir
        return float(direction_map.get(prop_rot_dir, {}).get(arrow_location, 0))

    def _calculate_anti_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for anti arrows."""
        direction_map = {
            RotationDirection.CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 225,
                Location.SOUTH: 135,
                Location.WEST: 45,
                Location.NORTHEAST: 270,
                Location.SOUTHEAST: 180,
                Location.SOUTHWEST: 90,
                Location.NORTHWEST: 0,
            },
            RotationDirection.COUNTER_CLOCKWISE: {
                Location.NORTH: 315,
                Location.EAST: 45,
                Location.SOUTH: 135,
                Location.WEST: 225,
                Location.NORTHEAST: 0,
                Location.SOUTHEAST: 90,
                Location.SOUTHWEST: 180,
                Location.NORTHWEST: 270,
            },
        }
        prop_rot_dir = motion_data.prop_rot_dir
        return float(direction_map.get(prop_rot_dir, {}).get(arrow_location, 0))

    def _calculate_dash_rotation(
        self, motion_data: MotionData, arrow_location: Optional[Location] = None
    ) -> float:
        """Calculate rotation for dash arrows."""
        if arrow_location is None:
            arrow_location = self._calculate_arrow_location(motion_data)

        if motion_data.prop_rot_dir == RotationDirection.NO_ROTATION:
            no_rotation_map = {
                (Location.NORTH, Location.SOUTH): 90,
                (Location.EAST, Location.WEST): 180,
                (Location.SOUTH, Location.NORTH): 270,
                (Location.WEST, Location.EAST): 0,
                (Location.SOUTHEAST, Location.NORTHWEST): 225,
                (Location.SOUTHWEST, Location.NORTHEAST): 315,
                (Location.NORTHWEST, Location.SOUTHEAST): 45,
                (Location.NORTHEAST, Location.SOUTHWEST): 135,
            }
            return float(
                no_rotation_map.get((motion_data.start_loc, motion_data.end_loc), 0)
            )
        else:
            arrow_pos = self._get_location_position(arrow_location)
            center_pos = (0, 0)
            return self._calculate_motion_rotation(center_pos, arrow_pos)

    def _calculate_float_rotation(
        self, motion_data: MotionData, arrow_location: Location
    ) -> float:
        """Calculate rotation for float arrows."""
        clockwise_map = {
            Location.NORTH: 315,
            Location.EAST: 45,
            Location.SOUTH: 135,
            Location.WEST: 225,
            Location.NORTHEAST: 0,
            Location.SOUTHEAST: 90,
            Location.SOUTHWEST: 180,
            Location.NORTHWEST: 270,
        }
        counter_clockwise_map = {
            Location.NORTH: 45,
            Location.EAST: 135,
            Location.SOUTH: 225,
            Location.WEST: 315,
            Location.NORTHEAST: 90,
            Location.SOUTHEAST: 180,
            Location.SOUTHWEST: 270,
            Location.NORTHWEST: 0,
        }

        return float(clockwise_map.get(arrow_location, 0))

    def _calculate_motion_rotation(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> float:
        """Calculate rotation for motion arrows."""
        import math

        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        if dx == 0 and dy == 0:
            return 0.0

        angle = math.degrees(math.atan2(dy, dx))
        return angle - 90.0

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """Calculate prop rotation using exact rotation algorithms."""
        location = motion_data.end_loc
        if location in [Location.NORTH, Location.SOUTH, Location.EAST, Location.WEST]:
            grid_mode = "DIAMOND"
        else:
            grid_mode = "BOX"

        if motion_data.motion_type == MotionType.STATIC:
            orientation = "IN"
        elif motion_data.prop_rot_dir == RotationDirection.CLOCKWISE:
            orientation = "CLOCK"
        elif motion_data.prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE:
            orientation = "COUNTER"
        else:
            orientation = "IN"

        if grid_mode == "DIAMOND":
            angle_map = {
                "IN": {
                    Location.NORTH: 90,
                    Location.SOUTH: 270,
                    Location.WEST: 0,
                    Location.EAST: 180,
                },
                "OUT": {
                    Location.NORTH: 270,
                    Location.SOUTH: 90,
                    Location.WEST: 180,
                    Location.EAST: 0,
                },
                "CLOCK": {
                    Location.NORTH: 0,
                    Location.SOUTH: 180,
                    Location.WEST: 270,
                    Location.EAST: 90,
                },
                "COUNTER": {
                    Location.NORTH: 180,
                    Location.SOUTH: 0,
                    Location.WEST: 90,
                    Location.EAST: 270,
                },
            }
        else:
            angle_map = {
                "IN": {
                    Location.NORTHEAST: 135,
                    Location.NORTHWEST: 45,
                    Location.SOUTHWEST: 315,
                    Location.SOUTHEAST: 225,
                },
                "OUT": {
                    Location.NORTHEAST: 315,
                    Location.NORTHWEST: 225,
                    Location.SOUTHWEST: 135,
                    Location.SOUTHEAST: 45,
                },
                "CLOCK": {
                    Location.NORTHEAST: 45,
                    Location.NORTHWEST: 315,
                    Location.SOUTHWEST: 225,
                    Location.SOUTHEAST: 135,
                },
                "COUNTER": {
                    Location.NORTHEAST: 225,
                    Location.NORTHWEST: 135,
                    Location.SOUTHWEST: 45,
                    Location.SOUTHEAST: 315,
                },
            }

        rotation_angle = angle_map.get(orientation, {}).get(location, 0)
        return float(rotation_angle)

    def _render_letter(self) -> None:
        """Render the letter if present."""
        if not self.beat_data or not self.beat_data.letter:
            return

        from PyQt6.QtWidgets import QGraphicsTextItem
        from PyQt6.QtGui import QFont

        letter_item = QGraphicsTextItem(self.beat_data.letter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        letter_item.setFont(font)

        letter_item.setPos(self.CENTER_X - 10, self.CENTER_Y + self.RADIUS + 20)
        self.addItem(letter_item)


class SimplePictographComponent(QWidget):
    """Simple pictograph component using V2 assets and modern architecture."""

    pictograph_updated = pyqtSignal(object)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[SimplePictographScene] = None
        self.view: Optional[QGraphicsView] = None

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the UI components with proper scaling to fit container."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scene = SimplePictographScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.view.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.view.setFrameStyle(0)

        layout.addWidget(self.view)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setMinimumSize(100, 100)
        self.resize(200, 200)

        self._fit_view()

    def update_from_beat(self, beat_data: BeatData) -> None:
        """Update the pictograph from beat data."""
        self.current_beat = beat_data
        if self.scene:
            self.scene.update_beat(beat_data)
            self._fit_view()
        self.pictograph_updated.emit(beat_data)

    def get_current_beat(self) -> Optional[BeatData]:
        return self.current_beat

    def clear_pictograph(self) -> None:
        self.current_beat = None
        if self.scene:
            self.scene.clear()

    def _fit_view(self) -> None:
        """Fit the view to properly scale and center the pictograph in container."""
        if self.view and self.scene:
            self.view.resetTransform()

            container_size = min(self.view.width(), self.view.height())

            scene_size = self.scene.SCENE_SIZE
            target_scale = (container_size * 0.9) / scene_size

            self.view.scale(target_scale, target_scale)

            self.view.centerOn(self.scene.CENTER_X, self.scene.CENTER_Y)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._fit_view()
