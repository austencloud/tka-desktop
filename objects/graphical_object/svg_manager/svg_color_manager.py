from typing import TYPE_CHECKING
import re
from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )


class SvgColorManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    @staticmethod
    def apply_color_transformations(svg_data: str, new_color: str) -> str:
        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}
        new_hex_color = COLOR_MAP.get(new_color)

        class_color_pattern = re.compile(
            r"(\.st0\s*\{.*?fill:\s*)(#[a-fA-F0-9]{6})(.*?\})"
        )
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')

        def replace_color(match):
            return match.group(1) + new_hex_color + match.group(3)

        svg_data = class_color_pattern.sub(replace_color, svg_data)
        svg_data = fill_pattern.sub(replace_color, svg_data)
        return svg_data
