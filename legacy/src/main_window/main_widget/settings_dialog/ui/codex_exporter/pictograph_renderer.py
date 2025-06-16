"""
Renders pictographs for the codex exporter.
"""

from typing import TYPE_CHECKING, Union
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )
    from main_window.main_widget.settings_dialog.ui.codex_exporter.codex_exporter_tab import (
        CodexExporterTab,
    )


class PictographRenderer:
    """Renders pictographs for the codex exporter."""

    def __init__(self, parent: Union["ImageExportTab", "CodexExporterTab"]):
        """Initialize the renderer.
        Args:
            parent: The parent tab (either ImageExportTab or CodexExporterTab)
        """
        self.parent = parent

    def create_pictograph_image(
        self, pictograph: "LegacyPictograph", add_border: bool = False
    ) -> QImage:
        """Create a QImage from a pictograph.
        Args:
            pictograph: The pictograph to convert to an image
            add_border: Whether to add a border
        Returns:
            The created image
        """
        size = 950
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        pictograph.render(painter)
        painter.end()
        return image

    def create_pictograph_image_with_border(
        self, pictograph: "LegacyPictograph"
    ) -> QImage:
        """Create a QImage from a pictograph with a black border.
        Args:
            pictograph: The pictograph to convert to an image
        Returns:
            The created image
        """
        border_width = 2
        standard_size = 800
        image_size = standard_size + (border_width * 2)
        image = QImage(image_size, image_size, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.black)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.fillRect(
            border_width,
            border_width,
            standard_size,
            standard_size,
            Qt.GlobalColor.white,
        )
        target_rect = image.rect()
        target_rect = target_rect.adjusted(
            border_width, border_width, -border_width, -border_width
        )
        if hasattr(pictograph.elements, "view") and pictograph.elements.view:
            painter.save()
            painter.translate(target_rect.topLeft())
            scale_factor = target_rect.width() / 950
            painter.scale(scale_factor, scale_factor)
            pictograph.elements.view.render(painter)
            painter.restore()
        else:
            pictograph.render(painter, target_rect)
        painter.end()
        return image
