from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
import os

from enums.letter.letter import Letter

from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class StartToEndPosGlyph(QGraphicsItemGroup):
    name = "Positions"

    def __init__(self, pictograph: "LegacyPictograph"):
        super().__init__()
        self.pictograph = pictograph

        self.start_glyph = QGraphicsSvgItem(self)
        self.arrow_glyph = QGraphicsSvgItem(self)
        self.end_glyph = QGraphicsSvgItem(self)

        # Load SVG renderers
        self.renderer_start = QSvgRenderer()
        self.renderer_arrow = QSvgRenderer()
        self.renderer_end = QSvgRenderer()

        # Set paths
        self.SVG_BASE_PATH = get_image_path("letters_trimmed/Type6")
        self.SVG_ARROW_PATH = get_image_path("arrow.svg")
        self.SVG_PATHS = {"alpha": "α.svg", "beta": "β.svg", "gamma": "Γ.svg"}

    def set_start_to_end_pos_glyph(self):
        # if the letter is alpha, beta, or gamma then don't show the start to end pos glyph
        if not self.pictograph.state.letter:
            return
        if self.pictograph.state.letter in [Letter.α, Letter.β, Letter.Γ]:
            return
        start_pos = "".join(filter(str.isalpha, self.pictograph.state.start_pos))
        end_pos = "".join(filter(str.isalpha, self.pictograph.state.end_pos))

        svg_file_start = os.path.join(
            self.SVG_BASE_PATH, self.SVG_PATHS.get(start_pos, "")
        )
        svg_file_end = os.path.join(self.SVG_BASE_PATH, self.SVG_PATHS.get(end_pos, ""))
        svg_file_arrow = self.SVG_ARROW_PATH

        if (
            self.renderer_start.load(svg_file_start)
            and self.renderer_arrow.load(svg_file_arrow)
            and self.renderer_end.load(svg_file_end)
        ):

            self.start_glyph.setSharedRenderer(self.renderer_start)
            self.arrow_glyph.setSharedRenderer(self.renderer_arrow)
            self.end_glyph.setSharedRenderer(self.renderer_end)

            self.scale_and_position_glyphs()

            # Adjust visibility based on settings
            visible = AppContext.settings_manager().visibility.get_glyph_visibility(
                "Positions"
            )
            if self.scene() is None:
                self.pictograph.addItem(self)
            self.setVisible(visible)
        else:
            print(
                f"Failed to load SVG files: {svg_file_start}, {svg_file_arrow}, {svg_file_end}"
            )

    def scale_and_position_glyphs(self):
        # Apply a uniform scaling
        scale_factor = 0.75
        self.start_glyph.setScale(scale_factor)
        self.arrow_glyph.setScale(scale_factor)
        self.end_glyph.setScale(scale_factor)

        # Position glyphs horizontally
        spacing = 25  # Adjust the spacing value as desired
        self.start_glyph.setPos(0, 0)

        self.end_glyph.setPos(
            self.start_glyph.boundingRect().width() * scale_factor
            + self.arrow_glyph.boundingRect().width() * scale_factor
            + spacing,
            0,
        )

        total_width = (
            self.start_glyph.boundingRect().width() * scale_factor
            + self.arrow_glyph.boundingRect().width() * scale_factor
            + self.end_glyph.boundingRect().width() * scale_factor
            + spacing
        )
        x_position = (self.pictograph.width()) // 2 - (total_width // 2)
        y_position = 50

        self.arrow_glyph.setPos(
            self.start_glyph.boundingRect().width() * scale_factor
            + spacing * scale_factor,
            self.start_glyph.boundingRect().height() * scale_factor // 2
            - self.arrow_glyph.boundingRect().height() * scale_factor,
        )
        self.setPos(x_position, y_position)

    def get_all_items(self):
        return [self.start_glyph, self.arrow_glyph, self.end_glyph]
