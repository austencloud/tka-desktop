from PyQt6.QtGui import QFont


class FontMarginHelper:
    @staticmethod
    def adjust_font_and_margin(
        base_font: QFont, num_filled_beats: int, base_margin: int, beat_scale: float
    ):
        # Get the base font size, ensuring it's at least 1
        base_font_size = max(1, base_font.pointSize())

        if num_filled_beats <= 1:
            font_size = max(1, int(base_font_size / 2.3))
            margin = max(1, base_margin // 3)
        elif num_filled_beats == 2:
            font_size = max(1, int(base_font_size / 1.5))
            margin = max(1, base_margin // 2)
        else:
            font_size = base_font_size
            margin = base_margin

        # Ensure the scaled font size is at least 1
        scaled_font_size = max(1, int(font_size * beat_scale))

        adjusted_font = QFont(
            base_font.family(),
            scaled_font_size,
            base_font.weight(),
            base_font.italic(),
        )
        return adjusted_font, max(1, int(margin * beat_scale))
