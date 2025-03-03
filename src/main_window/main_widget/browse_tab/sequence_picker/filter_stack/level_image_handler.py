import os
from functools import partial
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QLabel,
)
from PyQt6.QtCore import Qt, QEvent, QObject, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen


if TYPE_CHECKING:
    from base_widgets.base_go_back_button import MainWidget


class LevelImageHandler(QObject):
    def __init__(
        self, image_dir: str, main_widget: "MainWidget", on_level_click: callable
    ):
        super().__init__()
        self.image_dir = image_dir
        self.main_widget = main_widget
        self.on_level_click = on_level_click
        self.original_pixmaps: dict[int, QPixmap] = {}
        self.level_images: dict[int, QLabel] = {}

    def create_image_placeholder(self, level: int) -> QLabel:
        image_placeholder = QLabel()
        image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_placeholder.setProperty("level", level)
        image_path = os.path.join(self.image_dir, f"level_{level}.png")
        if os.path.exists(image_path):
            original_pixmap = QPixmap(image_path)
            self.original_pixmaps[level] = original_pixmap
            image_placeholder.setCursor(Qt.CursorShape.PointingHandCursor)
            image_placeholder.mousePressEvent = partial(self._handle_image_click, level)
            image_placeholder.installEventFilter(self)
        else:
            image_placeholder.setText("No Image Available")
        self.level_images[level] = image_placeholder
        return image_placeholder

    def _handle_image_click(self, level: int, event: QEvent) -> None:
        self.on_level_click(level)

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if isinstance(source, QLabel):
            level = source.property("level")
            if level is not None:
                if event.type() == QEvent.Type.Enter:
                    self.apply_hover_effect(level, source)
                    return True
                elif event.type() == QEvent.Type.Leave:
                    self.remove_hover_effect(level, source)
                    return True
        return super().eventFilter(source, event)

    def apply_hover_effect(self, level: int, label: QLabel) -> None:
        original_pixmap = self.original_pixmaps.get(level)
        if original_pixmap:
            bordered_pixmap = self.add_border_to_pixmap(
                original_pixmap, 4, Qt.GlobalColor.yellow
            )
            scaled_pixmap = self.scale_pixmap(bordered_pixmap)
            label.setPixmap(scaled_pixmap)

    def remove_hover_effect(self, level: int, label: QLabel) -> None:
        original_pixmap = self.original_pixmaps.get(level)
        if original_pixmap:
            scaled_pixmap = self.scale_pixmap(original_pixmap)
            label.setPixmap(scaled_pixmap)

    def add_border_to_pixmap(
        self, pixmap: QPixmap, border_width: int, color: Qt.GlobalColor
    ) -> QPixmap:
        bordered = QPixmap(pixmap.size())
        bordered.fill(Qt.GlobalColor.transparent)
        painter = QPainter(bordered)
        painter.drawPixmap(0, 0, pixmap)
        pen = QPen(color)
        pen.setWidth(border_width)
        painter.setPen(pen)
        painter.drawRect(
            border_width // 2,
            border_width // 2,
            pixmap.width() - border_width,
            pixmap.height() - border_width,
        )
        painter.end()
        return bordered

    def scale_images(self) -> None:
        for level, label in self.level_images.items():
            original_pixmap = self.original_pixmaps.get(level)
            if original_pixmap:
                scaled_pixmap = self.scale_pixmap(original_pixmap)
                label.setPixmap(scaled_pixmap)

    def scale_pixmap(self, pixmap: QPixmap) -> QPixmap:
        size = max(1, self.main_widget.width() // 6)
        return pixmap.scaled(
            QSize(size, size),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
