from typing import TYPE_CHECKING
import re
from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from svg_manager.svg_manager import SvgManager


class SvgColorHandler:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    @staticmethod
    def apply_color_transformations(svg_data: str, new_color: str) -> str:
        """
        If new_color is RED or BLUE, then use COLOR_MAP.
        If new_color is already a hex string (#ED1C24 / #2E3192), use it directly.
        """
        COLOR_MAP = {RED: HEX_RED, BLUE: HEX_BLUE}

        # 1) Detect if we already got a hex color
        if new_color and new_color.startswith("#"):
            new_hex_color = new_color
        else:
            # 2) Maybe "BLUE", "RED", or something else
            new_hex_color = COLOR_MAP.get(new_color, None)

        if not new_hex_color:
            # If we still don't have a color, nothing to replace.
            return svg_data

        class_color_pattern = re.compile(
            r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)(#[a-fA-F0-9]{6})([^}]*?\})"
        )
        fill_pattern = re.compile(r'(fill=")(#[a-fA-F0-9]{6})(")')

        def replace_color(match):
            return match.group(1) + new_hex_color + match.group(4)

        svg_data = class_color_pattern.sub(replace_color, svg_data)
        svg_data = fill_pattern.sub(replace_color, svg_data)

        return svg_data
