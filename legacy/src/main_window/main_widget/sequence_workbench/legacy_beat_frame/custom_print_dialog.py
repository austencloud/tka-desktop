from typing import TYPE_CHECKING
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsView,
    QSpinBox,
    QLabel,
    QGraphicsScene,
)


if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
        LegacyBeatFrame,
    )


class CustomPrintDialog(QDialog):
    def __init__(self, pixmap: QPixmap, beat_frame: "LegacyBeatFrame") -> None:
        super().__init__(beat_frame)
        self.pixmap = pixmap
        self.beat_frame = beat_frame
        self.printer = QPrinter()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Print Preview")

        preview_layout = self._setup_preview_layout()
        self.controls_layout = self._setup_controls_layout()

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(preview_layout, 1)
        main_layout.addLayout(self.controls_layout, 1)

        self.resize_custom_print_dialog(
            self.beat_frame.width() + 200, self.beat_frame.height()
        )

    def _setup_preview_layout(self) -> QVBoxLayout:
        preview_column_layout = QVBoxLayout()
        self.sequence_viewer = QGraphicsView(self)
        self.sequence_viewer.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.sequence_viewer.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scene = QGraphicsScene(self)
        self.sequence_viewer.setScene(self.scene)

        # make sure the scene's view matches the aspect ratio of the pixmap
        # scale the pixmap to fit the view's limitations
        self.preview_pixmap_item = self.scene.addPixmap(self.pixmap)
        self.sequence_viewer.fitInView(
            self.preview_pixmap_item, Qt.AspectRatioMode.KeepAspectRatio
        )
        self.sequence_viewer.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.sequence_viewer.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.sequence_viewer.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.update_preview()
        preview_column_layout.addWidget(self.sequence_viewer)
        return preview_column_layout

    def _setup_controls_layout(self) -> QVBoxLayout:
        controls_layout = QVBoxLayout()
        controls_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        )
        copies_layout = QHBoxLayout()
        self.copies_label = QLabel("Copies:", self)
        current_word = self.beat_frame.get.current_word()
        self.label_current_word = QLabel(f"Current Word: {current_word}", self)
        self.copies_spinbox = QSpinBox(self)
        self.copies_spinbox.setMinimum(1)
        controls_layout.addWidget(self.label_current_word)
        copies_layout.addWidget(self.copies_label)
        copies_layout.addWidget(self.copies_spinbox)
        controls_layout.addLayout(copies_layout)
        self.print_button = QPushButton("Print", self)
        self.print_button.clicked.connect(self.print)
        controls_layout.addWidget(self.print_button)
        return controls_layout

    def update_preview(self) -> None:
        self.scene.clear()
        self.preview_pixmap_item = self.scene.addPixmap(self.pixmap)
        if not self.preview_pixmap_item.pixmap().isNull():
            self.sequence_viewer.fitInView(
                self.preview_pixmap_item, Qt.AspectRatioMode.KeepAspectRatio
            )

    def print(self) -> None:
        self.printer.setCopyCount(self.copies_spinbox.value())

        dialog = QPrintDialog(self.printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.perform_print()

    def perform_print(self) -> None:
        painter = QPainter(self.printer)

        rect = self.printer.pageRect(QPrinter.Unit.Point)
        scale_factor = min(
            rect.width() / self.pixmap.width(), rect.height() / self.pixmap.height()
        )
        scaled_pixmap = self.pixmap.scaled(
            self.pixmap.size() * scale_factor, Qt.AspectRatioMode.KeepAspectRatio
        )
        x = int((rect.width() - scaled_pixmap.width()) / 2)
        y = int((rect.height() - scaled_pixmap.height()) / 2)

        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

    def resize_custom_print_dialog(self, width: int, height: int) -> None:
        self.setFixedSize(width, height)
        scene_aspect_ratio = (
            self.sequence_viewer.sceneRect().width()
            / self.sequence_viewer.sceneRect().height()
        )
        self.sequence_viewer.setFixedWidth(int(self.width() // 2))
        self.sequence_viewer.setFixedHeight(int(self.width() // 2 / scene_aspect_ratio))
        self.sequence_viewer.fitInView(
            self.preview_pixmap_item, Qt.AspectRatioMode.KeepAspectRatio
        )
