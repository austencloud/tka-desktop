from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class BaseLocationCalculator:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow
        self.pictograph = arrow.pictograph

    def calculate_location(self) -> str:
        raise NotImplementedError(
            "Each calculator must implement its own location calculation method."
        )
