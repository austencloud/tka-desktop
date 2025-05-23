# src/main_window/main_widget/sequence_card_tab/export/export_config.py
import logging
from typing import Dict, Any, Tuple, Optional
from PyQt6.QtCore import Qt


class ExportConfig:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.print_settings = {
            "page_width_inches": 8.5,
            "page_height_inches": 11.0,
            "dpi": 600,
            "page_width_pixels": int(8.5 * 600),
            "page_height_pixels": int(11.0 * 600),
        }
        
        self.export_settings = {
            "format": "PNG",
            "quality": 100,
            "dpi": 600,
            "background_color": Qt.GlobalColor.white,
            "compression": 0,
            "page_margin_left": int(0.25 * 600),
            "page_margin_top": int(0.5 * 600),
            "page_margin_right": int(0.25 * 600),
            "page_margin_bottom": int(0.5 * 600),
            "cell_spacing": int(0.125 * 600),
            "cell_padding": int(0.05 * 600),
            "grid_rows": 3,
            "grid_cols": 2,
            "grid_dimensions": {
                4: (2, 2),
                8: (2, 4),
                16: (4, 4),
            },
        }
    
    def get_print_setting(self, key: str, default: Any = None) -> Any:
        return self.print_settings.get(key, default)
    
    def get_export_setting(self, key: str, default: Any = None) -> Any:
        return self.export_settings.get(key, default)
    
    def set_print_setting(self, key: str, value: Any) -> None:
        self.print_settings[key] = value
        self.logger.debug(f"Set print setting {key} to {value}")
    
    def set_export_setting(self, key: str, value: Any) -> None:
        self.export_settings[key] = value
        self.logger.debug(f"Set export setting {key} to {value}")
    
    def get_grid_dimensions(self, sequence_length: Optional[int] = None) -> Tuple[int, int]:
        if sequence_length is None:
            return (
                self.get_export_setting("grid_rows", 3),
                self.get_export_setting("grid_cols", 2)
            )
        
        grid_dimensions = self.get_export_setting("grid_dimensions", {})
        
        if sequence_length in grid_dimensions:
            return grid_dimensions[sequence_length]
        
        if sequence_length <= 4:
            return (2, 2)
        elif sequence_length <= 8:
            return (2, 4)
        else:
            return (4, 4)
    
    def get_content_area(self) -> Dict[str, int]:
        page_width = self.get_print_setting("page_width_pixels")
        page_height = self.get_print_setting("page_height_pixels")
        margin_left = self.get_export_setting("page_margin_left")
        margin_top = self.get_export_setting("page_margin_top")
        margin_right = self.get_export_setting("page_margin_right")
        margin_bottom = self.get_export_setting("page_margin_bottom")
        
        content_width = page_width - margin_left - margin_right
        content_height = page_height - margin_top - margin_bottom
        
        return {
            "x": margin_left,
            "y": margin_top,
            "width": content_width,
            "height": content_height
        }
    
    def get_cell_dimensions(self, rows: int, cols: int) -> Dict[str, int]:
        content_area = self.get_content_area()
        cell_spacing = self.get_export_setting("cell_spacing")
        
        available_width = content_area["width"] - (cols - 1) * cell_spacing
        available_height = content_area["height"] - (rows - 1) * cell_spacing
        
        cell_width = available_width // cols
        cell_height = available_height // rows
        
        return {
            "width": cell_width,
            "height": cell_height,
            "spacing": cell_spacing
        }
