from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from Enums.Enums import LetterType

from typing import TYPE_CHECKING

from utilities.path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from .tka_glyph import TKA_Glyph

SVG_PATHS = {
    LetterType.Type1: "Type1/{letter}.svg",
    LetterType.Type2: "Type2/{letter}.svg",
    LetterType.Type3: "Type2/{letter[0]}.svg",
    LetterType.Type4: "Type4/{letter}.svg",
    LetterType.Type5: "Type4/{letter[0]}.svg",
    LetterType.Type6: "Type6/{letter}.svg",
}

SVG_BASE_PATH = get_images_and_data_path("images/letters_trimmed")
SVG_PATHS = {
    letter_type: f"{SVG_BASE_PATH}/{path}" for letter_type, path in SVG_PATHS.items()
}


class TKALetter(QGraphicsSvgItem):
    def __init__(self, glyph: "TKA_Glyph") -> None:
        super().__init__(glyph)
        self.glyph = glyph
        self.renderer = None

    def set_letter(self) -> None:
        if not self.glyph.pictograph.letter:
            return
        letter_type = LetterType.get_letter_type(self.glyph.pictograph.letter)
        self.glyph.pictograph.letter_type = letter_type
        svg_path: str = SVG_PATHS.get(letter_type, "")
        svg_path = svg_path.format(letter=self.glyph.pictograph.letter.value)
        self.renderer: QSvgRenderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            x = int(self.boundingRect().height() / 1.5)
            y = int(
                self.glyph.pictograph.height() - (self.boundingRect().height() * 1.7)
            )
            self.setPos(x, y)
