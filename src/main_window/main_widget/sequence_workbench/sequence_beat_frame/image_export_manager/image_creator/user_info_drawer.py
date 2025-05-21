from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QFont, QFontMetrics, QImage
from datetime import datetime

from .font_margin_helper import FontMarginHelper

if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator


class UserInfoDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.base_font_bold_italic = QFont("Georgia", 50, QFont.Weight.Bold)
        self.base_font_italic = QFont("Georgia", 50, QFont.Weight.Normal)

    def draw_user_info(
        self,
        image: QImage,
        options: dict[str, any],
        num_filled_beats: int,
    ) -> None:
        base_margin = 50
        font_bold_italic, margin = FontMarginHelper.adjust_font_and_margin(
            self.base_font_bold_italic,
            num_filled_beats,
            base_margin,
            self.image_creator.beat_scale,
        )
        font_italic, _ = FontMarginHelper.adjust_font_and_margin(
            self.base_font_italic,
            num_filled_beats,
            base_margin,
            self.image_creator.beat_scale,
        )

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        user_name = options["user_name"]
        export_date = self._format_export_date(
            options.get("export_date", datetime.now().strftime("%m-%d-%Y"))
        )
        add_info = options.get("add_user_info", False)
        notes = options.get("notes", "Created using The Kinetic Alphabet")

        # Calculate text widths
        export_date_width = self._get_text_width(font_italic, export_date)
        notes_width = self._get_text_width(font_italic, notes)

        if add_info:
            # Draw user name
            self._draw_text(
                painter, image, user_name, font_bold_italic, margin, "bottom-left"
            )

            # Draw notes text
            self._draw_text(
                painter,
                image,
                notes,
                font_italic,
                margin,
                "bottom-center",
                notes_width,
            )

            # Draw export date
            self._draw_text(
                painter,
                image,
                export_date,
                font_italic,
                margin,
                "bottom-right",
                export_date_width,
            )

        painter.end()

    def _format_export_date(self, date_str: str) -> str:
        return "-".join([str(int(part)) for part in date_str.split("-")])

    def _draw_text(
        self,
        painter: QPainter,
        image: QImage,
        text: str,
        font: QFont,
        margin: int,
        position: str,
        text_width: int = None,
    ) -> None:
        painter.setFont(font)
        if not text_width:
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(text)
        else:
            metrics = QFontMetrics(font)

        # Get the border width from the image creator
        border_width = 3  # Same as in ImageCreator._create_image

        if position == "bottom-left":
            x = margin + border_width
            y = image.height() - margin - border_width
        elif position == "bottom-center":
            x = (image.width() - text_width) // 2
            y = image.height() - margin - border_width
        elif position == "bottom-right":
            x = image.width() - text_width - margin - border_width
            y = image.height() - margin - border_width

        painter.drawText(x, y, text)

    def _get_text_width(self, font: QFont, text: str) -> int:
        metrics = QFontMetrics(font)
        return metrics.horizontalAdvance(text)
