from PyQt6.QtCore import QPointF
from .grid_point import GridPoint



class GridLayer:
    def __init__(self, points_data: dict[str, str]) -> None:
        self.points: dict[str, GridPoint] = {}
        for name, coords in points_data.items():
            if coords != "None":
                try:
                    x, y = map(float, coords.strip("()").split(", "))
                    self.points[name] = GridPoint(name, QPointF(x, y))
                except ValueError:
                    self.points[name] = GridPoint(name, None)
            else:
                self.points[name] = GridPoint(name, None)
