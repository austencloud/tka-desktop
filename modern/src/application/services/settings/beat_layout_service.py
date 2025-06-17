from typing import Tuple, Dict, Any
from src.core.interfaces.tab_settings_interfaces import IBeatLayoutService
from src.core.interfaces.core_services import IUIStateManagementService


class BeatLayoutService(IBeatLayoutService):
    """Service for managing beat frame layout settings"""

    def __init__(self, ui_state_service: IUIStateManagementService):
        self.ui_state_service = ui_state_service
        self._default_layouts = {
            2: (1, 2),  # 2 beats: 1 row, 2 columns
            3: (1, 3),  # 3 beats: 1 row, 3 columns
            4: (2, 2),  # 4 beats: 2 rows, 2 columns
            5: (1, 5),  # 5 beats: 1 row, 5 columns
            6: (2, 3),  # 6 beats: 2 rows, 3 columns
            7: (1, 7),  # 7 beats: 1 row, 7 columns
            8: (2, 4),  # 8 beats: 2 rows, 4 columns
            9: (3, 3),  # 9 beats: 3 rows, 3 columns
            10: (2, 5),  # 10 beats: 2 rows, 5 columns
            12: (3, 4),  # 12 beats: 3 rows, 4 columns
            16: (4, 4),  # 16 beats: 4 rows, 4 columns
        }

    def get_layout_for_length(self, sequence_length: int) -> Tuple[int, int]:
        """Get the layout (rows, cols) for a given sequence length"""
        layout_key = f"beat_layout_{sequence_length}"
        stored_layout = self.ui_state_service.get_setting(layout_key)

        if (
            stored_layout
            and isinstance(stored_layout, (list, tuple))
            and len(stored_layout) == 2
        ):
            return tuple(stored_layout)

        # Return default layout or calculate one
        return self._default_layouts.get(
            sequence_length, self._calculate_layout(sequence_length)
        )

    def set_layout_for_length(self, sequence_length: int, rows: int, cols: int) -> None:
        """Set the layout for a specific sequence length"""
        layout_key = f"beat_layout_{sequence_length}"
        self.ui_state_service.set_setting(layout_key, (rows, cols))

    def _calculate_layout(self, length: int) -> Tuple[int, int]:
        """Calculate a reasonable layout for any sequence length"""
        if length <= 0:
            return (1, 1)

        # For lengths not in defaults, try to make a reasonable grid
        import math

        # Try to make it roughly square
        cols = int(math.ceil(math.sqrt(length)))
        rows = int(math.ceil(length / cols))

        return (rows, cols)

    def get_default_sequence_length(self) -> int:
        """Get the default sequence length setting"""
        return self.ui_state_service.get_setting("default_sequence_length", 4)

    def set_default_sequence_length(self, length: int) -> None:
        """Set the default sequence length"""
        if length > 0:
            self.ui_state_service.set_setting("default_sequence_length", length)

    def get_layout_options_for_length(
        self, sequence_length: int
    ) -> Dict[str, Tuple[int, int]]:
        """Get available layout options for a sequence length"""
        options = {}

        # Add some common layout variations
        length = sequence_length

        # Single row
        options[f"1 × {length}"] = (1, length)

        # Try different factorizations
        for rows in range(1, length + 1):
            if length % rows == 0:
                cols = length // rows
                options[f"{rows} × {cols}"] = (rows, cols)

        # Add some non-perfect grids if reasonable
        import math

        sqrt_len = int(math.sqrt(length))

        for r in range(max(1, sqrt_len - 1), sqrt_len + 3):
            c = math.ceil(length / r)
            if r * c >= length:
                options[f"{r} × {c}"] = (r, c)

        return options

    def reset_layout_for_length(self, sequence_length: int) -> None:
        """Reset layout for a specific length to default"""
        layout_key = f"beat_layout_{sequence_length}"
        # Remove the custom setting to fall back to default
        current_settings = self.ui_state_service.get_all_settings()
        if layout_key in current_settings:
            del current_settings[layout_key]
            # Note: This is a simplification - in a real implementation you'd want
            # a proper "remove_setting" method on the UI state service

    def get_grow_sequence_setting(self) -> bool:
        """Get whether sequences should grow automatically"""
        return self.ui_state_service.get_setting("grow_sequence", False)

    def set_grow_sequence_setting(self, grow: bool) -> None:
        """Set whether sequences should grow automatically"""
        self.ui_state_service.set_setting("grow_sequence", grow)
