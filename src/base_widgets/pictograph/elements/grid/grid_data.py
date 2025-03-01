from typing import Optional
from PyQt6.QtCore import QPointF
from .grid_layer import GridLayer
from .grid_point import GridPoint


class GridData:
    def __init__(self, data: dict[str, dict[str, dict[str, str]]]) -> None:
        self.all_layer2_points: dict[str, GridPoint] = {}
        self.all_hand_points_normal: dict[str, GridPoint] = {}
        self.all_hand_points_strict: dict[str, GridPoint] = {}
        self.all_layer2_points_strict: dict[str, GridPoint] = {}
        self.all_outer_points: dict[str, GridPoint] = {}
        self.center_points: dict[str, QPointF] = {}

        for mode, mode_data in data.items():
            layer2_normal = GridLayer(mode_data["layer2_points"]["normal"])
            self.all_layer2_points.update(layer2_normal.points)

            layer2_strict = GridLayer(mode_data["layer2_points"]["strict"])
            self.all_layer2_points_strict.update(layer2_strict.points)

            hand_normal = GridLayer(mode_data["hand_points"]["normal"])
            self.all_hand_points_normal.update(hand_normal.points)

            hand_strict = GridLayer(mode_data["hand_points"]["strict"])
            self.all_hand_points_strict.update(hand_strict.points)

            outer_points = GridLayer(mode_data["outer_points"])
            self.all_outer_points.update(outer_points.points)

            center_coords = mode_data.get("center_point", "None")
            if center_coords != "None":
                try:
                    x, y = map(float, center_coords.strip("()").split(", "))
                    self.center_points[mode] = QPointF(x, y)
                except ValueError:
                    self.center_points[mode] = QPointF(0, 0)
            else:
                self.center_points[mode] = QPointF(0, 0)

    def get_shift_coord(self, point_name: str) -> Optional[QPointF]:
        point = self.all_layer2_points.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:

            return None

    def get_static_dash_coord(self, point_name: str) -> Optional[QPointF]:
        point = self.all_hand_points_normal.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:

            return None

    def get_point(
        self, layer: dict[str, GridPoint], pos: QPointF
    ) -> Optional[GridPoint]:
        min_distance = float("inf")
        closest_point = None
        for point in layer.values():
            if point.coordinates:
                distance = (pos - point.coordinates).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

        return closest_point
