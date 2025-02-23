from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QToolButton, QLabel
from PyQt6.QtGui import (
    QIcon,
    QPixmap,
    QImage,
    QCursor,
    qRed,
    qGreen,
    qBlue,
    qAlpha,
    qRgba,
)
from PyQt6.QtCore import Qt, QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class LevelSelector(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.normal_pixmaps: list[QPixmap] = []
        self.grayscale_pixmaps: list[QPixmap] = []
        self.buttons: list[QToolButton] = []
        self.info_labels: list[QLabel] = []
        self.current_level = self.generate_tab.settings.get_setting("level")
        self.default_icon_size = QSize(64, 64)
        self._load_pixmaps()
        self._init_ui()
        self._apply_styles()

    def _load_pixmaps(self):
        for level in [1, 2, 3]:
            pixmap = QPixmap(f"images/icons/level_{level}.png")
            if pixmap.isNull():
                pixmap = QPixmap(64, 64)
                pixmap.fill(Qt.GlobalColor.transparent)

            self.normal_pixmaps.append(pixmap)
            self.grayscale_pixmaps.append(self._create_grayscale_pixmap(pixmap))

    def _create_grayscale_pixmap(self, color_pixmap: QPixmap) -> QPixmap:
        image = color_pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
        width = image.width()
        height = image.height()
        for y in range(height):
            for x in range(width):
                pixel = image.pixel(x, y)
                alpha = qAlpha(pixel)
                r = qRed(pixel)
                g = qGreen(pixel)
                b = qBlue(pixel)
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                new_pixel = qRgba(gray, gray, gray, alpha)
                image.setPixel(x, y, new_pixel)
        return QPixmap.fromImage(image)

    def _init_ui(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.main_layout.addStretch(4)

        level_data = [
            ("No Turns", "Base motions only\nNo turns added"),
            ("Whole Turns", "Whole turns allowed\nRadial orientations only"),
            ("Half Turns", "Half turns allowed\nRadial/nonradial orientations"),
        ]

        for i, (label_text, info_text) in enumerate(level_data):
            vbox = QVBoxLayout()
            vbox.setSpacing(5)
            vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

            button = QToolButton()
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button.setCheckable(True)
            button.setText(label_text)
            button.clicked.connect(lambda _, idx=i: self.set_level(idx + 1))
            button.setToolTip(info_text)

            info_label = QLabel(label_text)
            info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            info_label.setStyleSheet(
                "color: white; font-size: 12pt; font-weight: bold;"
            )

            self.buttons.append(button)
            self.info_labels.append(info_label)

            vbox.addWidget(button, alignment=Qt.AlignmentFlag.AlignHCenter)
            vbox.addWidget(info_label)

            self.main_layout.addLayout(vbox)
            self.main_layout.addStretch(1)

        self.main_layout.addStretch(3)
        self.setLayout(self.main_layout)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QToolButton {
                background: transparent;
                border: none;
                margin: 0;
                padding: 0;
                outline: 0;
            }
            QToolButton:hover:!checked {
                background: rgba(200, 200, 200, 30);
                border-radius: 10px;
            }
            QToolButton:checked {
                background: rgba(255, 255, 255, 20);
                border-bottom: 3px solid rgba(255, 255, 255, 80);
                border-radius: 10px 10px 0 0;
            }
            """
        )

    def set_level(self, level: int):
        self.current_level = level
        for i, btn in enumerate(self.buttons):
            btn.setChecked((i + 1) == level)
        self._update_icons()
        self._update_sequence_settings(level)

    def _update_icons(self):
        icon_size = self._desired_icon_size()
        for i, btn in enumerate(self.buttons):
            is_selected = (i + 1) == self.current_level
            source_pixmap = (
                self.normal_pixmaps[i] if is_selected else self.grayscale_pixmaps[i]
            )
            scaled = source_pixmap.scaled(
                icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            btn.setIcon(QIcon(scaled))
            btn.setIconSize(icon_size)
            btn_size = icon_size.width() + 10
            btn.setFixedSize(btn_size, btn_size)

    def _desired_icon_size(self) -> QSize:
        parent_size = self.generate_tab.size()
        side = max(32, parent_size.width() // 10)
        return QSize(side, side)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_icons()

    def _update_sequence_settings(self, level: int):
        self.generate_tab.settings.set_setting("level", str(level))
        
        adjuster = self.generate_tab.turn_intensity
        adjuster.setVisible(level > 1)
        if level > 1:
            adjuster.adjust_values(level)
