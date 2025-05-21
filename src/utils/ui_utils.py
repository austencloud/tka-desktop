# ui_utils.py
def calc_font_size(parent_height: int, factor: float = 0.03, min_size: int = 10) -> int:
    return max(int(parent_height * factor), min_size)


def calc_label_size(text: str, font) -> tuple[int, int]:
    from PyQt6.QtGui import QFontMetrics

    fm = QFontMetrics(font)
    return fm.horizontalAdvance(text) + 20, fm.height() + 20


def ensure_positive_size(size: int, min_value: int = 1) -> int:
    """Ensure a size value is positive to avoid Qt warnings.

    Args:
        size: The size value to check
        min_value: The minimum allowed value (default: 1)

    Returns:
        A size value that is at least min_value
    """
    return max(size, min_value)
