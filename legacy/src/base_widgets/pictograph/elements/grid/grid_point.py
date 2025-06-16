from typing import Optional
from PyQt6.QtCore import QPointF


class GridPoint:
    def __init__(self, name: str, coordinates: Optional[QPointF]) -> None:
        self.name = name
        self.coordinates = coordinates
