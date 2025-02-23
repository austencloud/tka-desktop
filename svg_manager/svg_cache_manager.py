from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )


class SvgCacheManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager
        self.file_path_cache = {}
        self.svg_content_cache = {}

    def store_svg_data_in_cache(self, file_path: str, svg_data: str):
        self.svg_content_cache[file_path] = svg_data
