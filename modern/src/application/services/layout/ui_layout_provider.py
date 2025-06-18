"""
UI Layout Provider

Provides basic UI layout information and component sizing.
This class preserves all original UI layout logic including
main window sizing, workbench/picker ratio calculations,
and component size calculations.
"""

from typing import Tuple

from PyQt6.QtCore import QSize


class UILayoutProvider:
    """
    Provides basic UI layout information and component sizing.

    This class preserves all original UI layout logic including
    main window sizing, workbench/picker ratio calculations,
    and component size calculations.
    """

    def __init__(self, main_window_size: QSize, layout_ratio: Tuple[int, int]):
        """Initialize with window size and layout ratio."""
        self._main_window_size = main_window_size
        self._layout_ratio = layout_ratio

    def get_main_window_size(self) -> QSize:
        """Get the main window size."""
        return self._main_window_size

    def get_workbench_size(self) -> QSize:
        """Get the workbench area size."""
        # Calculate workbench size based on main window and ratio
        total_width = self._main_window_size.width()
        total_height = self._main_window_size.height()

        # Account for margins and spacing
        usable_width = total_width - 60  # 60px for margins and spacing
        usable_height = total_height - 100  # 100px for header and margins

        # Calculate workbench width based on ratio
        ratio_total = self._layout_ratio[0] + self._layout_ratio[1]
        workbench_width = int(usable_width * self._layout_ratio[0] / ratio_total)

        return QSize(workbench_width, usable_height)

    def get_picker_size(self) -> QSize:
        """Get the option picker size."""
        # Calculate picker size based on main window and ratio
        total_width = self._main_window_size.width()
        total_height = self._main_window_size.height()

        # Account for margins and spacing
        usable_width = total_width - 60  # 60px for margins and spacing
        usable_height = total_height - 100  # 100px for header and margins

        # Calculate picker width based on ratio
        ratio_total = self._layout_ratio[0] + self._layout_ratio[1]
        picker_width = int(usable_width * self._layout_ratio[1] / ratio_total)

        return QSize(picker_width, usable_height)

    def get_layout_ratio(self) -> Tuple[int, int]:
        """Get the layout ratio (workbench:picker)."""
        return self._layout_ratio

    def set_layout_ratio(self, ratio: Tuple[int, int]) -> None:
        """Set the layout ratio."""
        self._layout_ratio = ratio

    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        """Calculate component size based on parent and type."""
        parent_width = parent_size.width()
        parent_height = parent_size.height()

        if component_type == "beat_frame":
            # Beat frame takes most of the workbench area
            return QSize(int(parent_width * 0.85), int(parent_height * 0.9))

        elif component_type == "button_panel":
            # Button panel is narrow vertical strip
            return QSize(int(parent_width * 0.15), int(parent_height * 0.9))

        elif component_type == "option_picker":
            # Option picker takes full picker area
            return QSize(parent_width, parent_height)

        elif component_type == "start_position_picker":
            # Start position picker takes full picker area
            return QSize(parent_width, parent_height)

        elif component_type == "pictograph":
            # Individual pictograph size
            return QSize(120, 120)

        else:
            # Default size for unknown components
            return QSize(int(parent_width * 0.8), int(parent_height * 0.8))

    def set_main_window_size(self, size: QSize) -> None:
        """Set the main window size (for dynamic updates)."""
        self._main_window_size = size
