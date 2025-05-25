from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .image_export_manager import ImageExportManager


class ImageExportLayoutHandler:
    def __init__(self, image_export_manager: "ImageExportManager"):
        self.image_export_manager = image_export_manager
        self.beat_frame = image_export_manager.beat_frame

    @property
    def include_start_pos(self):
        # Dynamically fetch the current setting from the export manager
        return self.image_export_manager.include_start_pos

    def get_current_beat_frame_layout(self, beat_count: int) -> tuple[int, int]:
        """
        Get the current layout from the beat frame's layout manager.
        This ensures the exported image matches the current beat frame layout.

        Returns a tuple of (rows, columns) to match the format used in the beat frame layout.
        """
        return self.beat_frame.layout_manager.calculate_layout(beat_count)

    def calculate_layout(
        self, filled_beat_count: int, include_start_pos: bool
    ) -> tuple[int, int]:
        """
        Determine the layout based on the current beat frame layout and adjust for start position if needed.

        Returns a tuple of (columns, rows) for the image layout.
        """
        # Get the current layout from the beat frame
        # Note: beat_frame_layout_manager.calculate_layout returns (rows, columns)
        rows, columns = self.get_current_beat_frame_layout(filled_beat_count)

        # If including start position and it's not already accounted for in the layout,
        # adjust the layout to accommodate it
        if include_start_pos:
            # Add an extra column for the start position if needed
            # Return in (columns, rows) format for the image creator
            return (columns + 1, rows) if filled_beat_count > 0 else (1, 1)

        # Return in (columns, rows) format for the image creator
        return (columns, rows)

    def calculate_layout_with_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout considering an additional column for the start position.
        """
        # For backward compatibility, keep this method but use the new approach
        return self.calculate_layout(filled_beat_count, True)

    def calculate_layout_without_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout without the start position affecting the column count.
        """
        # For backward compatibility, keep this method but use the new approach
        return self.calculate_layout(filled_beat_count, False)

    def calculate_optimal_layout(
        self, beat_count: int, layout_options: dict
    ) -> tuple[int, int]:
        """
        Shared logic for calculating layout which can be customized further using provided layout options.
        """
        # For backward compatibility, keep this method
        if beat_count in layout_options:
            return layout_options[beat_count]
        return self.get_fallback_layout(beat_count)

    def get_layout_options_with_start(self) -> dict[int, tuple[int, int]]:
        """
        Layout options when including the start position in the layout.
        """
        return {
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (4, 1),
            4: (5, 1),
            5: (4, 2),
            6: (4, 2),
            7: (5, 2),
            8: (5, 2),
            9: (4, 3),
            10: (6, 2),
            11: (5, 3),
            12: (4, 4),
            13: (5, 4),
            14: (5, 4),
            15: (5, 4),
            16: (5, 4),
            17: (5, 5),
            18: (5, 5),
            19: (5, 5),
            20: (6, 4),
            21: (5, 6),
            22: (5, 6),
            23: (5, 6),
            24: (7, 4),
            25: (5, 7),
            26: (5, 7),
            27: (5, 7),
            28: (5, 7),
            29: (5, 8),
            30: (8, 4),
            31: (5, 8),
            32: (9, 4),
            33: (5, 9),
            34: (5, 9),
            35: (5, 9),
            36: (10, 4),
            37: (5, 10),
            38: (5, 10),
            39: (5, 10),
            40: (11, 4),
            41: (5, 11),
            42: (5, 11),
            43: (5, 11),
            44: (5, 11),
            45: (5, 12),
            46: (5, 12),
            47: (5, 12),
            48: (5, 12),
            49: (5, 13),
            50: (5, 13),
            51: (5, 13),
            52: (5, 13),
            53: (5, 14),
            54: (5, 14),
            55: (5, 14),
            56: (5, 14),
            57: (5, 15),
            58: (5, 15),
            59: (5, 15),
            60: (5, 15),
            61: (5, 16),
            62: (5, 16),
            63: (5, 16),
            64: (5, 16),
        }

    def get_layout_options_without_start(self) -> dict[int, tuple[int, int]]:
        """
        Define or adjust layout options for various counts of filled beats without the start position.
        Customize this as needed if different from layouts with start position.
        """
        return {
            0: (1, 1),
            1: (1, 1),
            2: (2, 1),
            3: (3, 1),
            4: (4, 1),
            5: (3, 2),
            6: (3, 2),
            7: (4, 2),
            8: (4, 2),
            9: (3, 3),
            10: (5, 2),
            11: (4, 3),
            12: (3, 4),
            13: (4, 4),
            14: (4, 4),
            15: (4, 4),
            16: (4, 4),
            17: (4, 5),
            18: (9, 2),
            19: (4, 5),
            20: (5, 4),
            21: (4, 6),
            22: (4, 6),
            23: (4, 6),
            24: (6, 4),
            25: (4, 7),
            26: (4, 7),
            27: (4, 7),
            28: (7, 4),
            29: (4, 8),
            30: (4, 8),
            31: (4, 8),
            32: (8, 4),
            33: (4, 9),
            34: (4, 9),
            35: (4, 9),
            36: (9, 4),
            37: (4, 10),
            38: (4, 10),
            39: (4, 10),
            40: (10, 4),
            41: (4, 11),
            42: (4, 11),
            43: (4, 11),
            44: (11, 4),
            45: (4, 12),
            46: (4, 12),
            47: (4, 12),
            48: (12, 4),
            49: (4, 13),
            50: (4, 13),
            51: (4, 13),
            52: (13, 4),
            53: (4, 14),
            54: (4, 14),
            55: (4, 14),
            56: (14, 4),
            57: (4, 15),
            58: (4, 15),
            59: (4, 15),
            60: (15, 4),
            61: (4, 16),
            62: (4, 16),
            63: (4, 16),
            64: (16, 4),
        }
