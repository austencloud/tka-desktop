# ui_utils.py
def calc_font_size(parent_height: int, factor: float = 0.03, min_size: int = 10) -> int:
    return max(int(parent_height * factor), min_size)


def calc_label_size(text: str, font) -> tuple[int, int]:
    from PyQt6.QtGui import QFontMetrics

    fm = QFontMetrics(font)
    return fm.horizontalAdvance(text) + 20, fm.height() + 20
