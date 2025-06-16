from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING, Literal

from data.constants import (
    ALPHA1,
    BOX,
    DIAMOND,
    ALPHA5,
    BETA3,
    BETA7,
    GAMMA10,
    GAMMA14,
    GAMMA4,
    GAMMA8,
    QUARTER_OPP,
    QUARTER_SAME,
    SPLIT_OPP,
    SPLIT_SAME,
    TOG_OPP,
    TOG_SAME,
)
from main_window.main_widget.grid_mode_checker import GridModeChecker
from src.legacy_settings_manager.global_settings.app_context import AppContext
from utils.path_helpers import get_data_path, get_image_path


if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


SVG_PATHS = {
    SPLIT_SAME: "SS.svg",
    SPLIT_OPP: "SO.svg",
    TOG_SAME: "TS.svg",
    TOG_OPP: "TO.svg",
    QUARTER_SAME: "QS.svg",
    QUARTER_OPP: "QO.svg",
}

SVG_BASE_PATH = get_image_path("vtg_glyphs")
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class VTG_Glyph(QGraphicsSvgItem):
    name = "VTG"

    def __init__(self, pictograph: "LegacyPictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def set_vtg_mode(self) -> None:
        from enums.letter.letter_type import LetterType

        from data.constants import (
            SPLIT_SAME,
            SPLIT_OPP,
            TOG_SAME,
            TOG_OPP,
            QUARTER_SAME,
            QUARTER_OPP,
        )
        from utils.path_helpers import get_data_path

        if not self.pictograph.state.letter_type in [LetterType.Type1]:
            self.setVisible(False)

        SVG_BASE_PATH = get_image_path("vtg_glyphs")
        SVG_PATHS = {
            SPLIT_SAME: f"{SVG_BASE_PATH}/SS.svg",
            SPLIT_OPP: f"{SVG_BASE_PATH}/SO.svg",
            TOG_SAME: f"{SVG_BASE_PATH}/TS.svg",
            TOG_OPP: f"{SVG_BASE_PATH}/TO.svg",
            QUARTER_SAME: f"{SVG_BASE_PATH}/QS.svg",
            QUARTER_OPP: f"{SVG_BASE_PATH}/QO.svg",
        }

        self.pictograph.state.vtg_mode = self.determine_vtg_mode()
        svg_path = SVG_PATHS.get(self.pictograph.state.vtg_mode, "")
        if svg_path:
            self.renderer: QSvgRenderer = QSvgRenderer(svg_path)
            if self.renderer.isValid():
                self.setSharedRenderer(self.renderer)
                if not self.scene():
                    self.pictograph.addItem(self)
                self.position_vtg_glyph()

                self.setVisible(
                    AppContext.settings_manager().visibility.get_glyph_visibility("VTG")
                )

    def determine_vtg_mode(self) -> Literal["SS", "SO", "TS", "TO", "QS", "QO"]:
        if not self.pictograph.state.letter:
            return
        letter_str = self.pictograph.state.letter.value
        start_pos = self.pictograph.state.start_pos
        grid_mode = GridModeChecker.get_grid_mode(self.pictograph.state.pictograph_data)

        mode_mapping = {
            DIAMOND: {
                "A": SPLIT_SAME,
                "B": SPLIT_SAME,
                "C": SPLIT_SAME,
                "D": SPLIT_OPP if start_pos in [BETA3, BETA7] else TOG_OPP,
                "E": SPLIT_OPP if start_pos in [BETA3, BETA7] else TOG_OPP,
                "F": SPLIT_OPP if start_pos in [BETA3, BETA7] else TOG_OPP,
                "G": TOG_SAME,
                "H": TOG_SAME,
                "I": TOG_SAME,
                "J": SPLIT_OPP if start_pos in [ALPHA1, ALPHA5] else TOG_OPP,
                "K": SPLIT_OPP if start_pos in [ALPHA1, ALPHA5] else TOG_OPP,
                "L": SPLIT_OPP if start_pos in [ALPHA1, ALPHA5] else TOG_OPP,
                "M": QUARTER_OPP,
                "N": QUARTER_OPP,
                "O": QUARTER_OPP,
                "P": QUARTER_OPP,
                "Q": QUARTER_OPP,
                "R": QUARTER_OPP,
                "S": QUARTER_SAME,
                "T": QUARTER_SAME,
                "U": QUARTER_SAME,
                "V": QUARTER_SAME,
            },
            BOX: {
                "A": SPLIT_SAME,
                "B": SPLIT_SAME,
                "C": SPLIT_SAME,
                "D": QUARTER_OPP,
                "E": QUARTER_OPP,
                "F": QUARTER_OPP,
                "G": TOG_SAME,
                "H": TOG_SAME,
                "I": TOG_SAME,
                "J": QUARTER_OPP,
                "K": QUARTER_OPP,
                "L": QUARTER_OPP,
                "M": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "N": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "O": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "P": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "Q": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "R": (
                    SPLIT_OPP
                    if start_pos in [GAMMA10, GAMMA8, GAMMA14, GAMMA4]
                    else TOG_OPP
                ),
                "S": QUARTER_SAME,
                "T": QUARTER_SAME,
                "U": QUARTER_SAME,
                "V": QUARTER_SAME,
            },
        }

        return mode_mapping.get(grid_mode, {}).get(
            letter_str, self.pictograph.state.vtg_mode
        )

    def position_vtg_glyph(self) -> None:
        pictograph_width = self.pictograph.width()
        pictograph_height = self.pictograph.height()

        scale_factor = 0.7
        self.setScale(scale_factor)

        border_percentage = 0.03
        additional_margin_percentage = 0.03

        border_offset_width = pictograph_width * border_percentage
        border_offset_height = pictograph_height * border_percentage
        additional_margin_width = pictograph_width * additional_margin_percentage
        additional_margin_height = pictograph_height * additional_margin_percentage

        effective_pictograph_width = pictograph_width - 2 * (
            border_offset_width + additional_margin_width
        )
        effective_pictograph_height = pictograph_height - 2 * (
            border_offset_height + additional_margin_height
        )

        scaled_width = self.boundingRect().width() * scale_factor
        scaled_height = self.boundingRect().height() * scale_factor

        x = (
            effective_pictograph_width
            - scaled_width
            + (border_offset_width + additional_margin_width)
        )
        y = (
            effective_pictograph_height
            - scaled_height
            + (border_offset_height + additional_margin_height)
        )

        self.setPos(x, y)
        self.setTransformOriginPoint(scaled_width / 2, scaled_height / 2)
