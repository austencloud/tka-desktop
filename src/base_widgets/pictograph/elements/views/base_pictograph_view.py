from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame, QMenu
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QAction

from base_widgets.pictograph.managers.pictograph_data_copier import dictCopier


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class BasePictographView(QGraphicsView):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__(pictograph)
        if pictograph:
            self.pictograph = pictograph
            self.pictograph.elements.view = self

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def contextMenuEvent(self, event: QEvent) -> None:
        context_menu = QMenu(self)
        copy_action = QAction("Copy Dictionary", self)
        copy_action.triggered.connect(
            self.pictograph.managers.data_copier.copy_pictograph_data
        )
        context_menu.addAction(copy_action)
        context_menu.exec(QCursor.pos())
