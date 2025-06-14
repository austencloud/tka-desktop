from typing import Tuple
from core.interfaces.core_services import ILayoutService


class SimpleLayoutService(ILayoutService):
    def get_component_size(self, component_name: str) -> Tuple[int, int]:
        sizes = {
            "start_position_picker": (400, 600),
            "option_picker": (400, 600),
            "workbench": (800, 600),
        }
        return sizes.get(component_name, (300, 400))

    def get_layout_spacing(self) -> int:
        return 10

    def get_margin_size(self) -> int:
        return 20

    def calculate_component_size(
        self, base_size: Tuple[int, int], ratio: float
    ) -> Tuple[int, int]:
        return (int(base_size[0] * ratio), int(base_size[1] * ratio))

    def get_layout_ratio(self) -> float:
        return 1.0

    def get_main_window_size(self) -> Tuple[int, int]:
        return (1200, 800)

    def get_picker_size(self) -> Tuple[int, int]:
        return (400, 600)

    def get_workbench_size(self) -> Tuple[int, int]:
        return (800, 600)

    def set_layout_ratio(self, ratio: float) -> None:
        pass
