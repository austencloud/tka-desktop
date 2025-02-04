from PyQt6.QtGui import QFont


class FontMarginHelper:
    @staticmethod
    def adjust_font_and_margin(
        base_font: QFont, num_filled_beats: int, base_margin: int, beat_scale
    ):
        if num_filled_beats == 1:
            font_size = base_font.pointSize() // 2.3
            margin = base_margin // 3
        elif num_filled_beats == 2:
            font_size = base_font.pointSize() // 1.5
            margin = base_margin // 2
        else:
            font_size = base_font.pointSize()
            margin = base_margin

        adjusted_font = QFont(
            base_font.family(),
            int(font_size * beat_scale),
            base_font.weight(),
            base_font.italic(),
        )
        return adjusted_font, int(margin * beat_scale)
