from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from ....domain.models.core_models import BeatData
from ..pictograph_component import PictographComponent


class ClickablePictographFrame(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, beat_data: BeatData, parent=None):
        super().__init__(parent)
        self.beat_data = beat_data
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)

        square_size = 160
        self.setFixedSize(square_size, square_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)

        self.pictograph_component = PictographComponent()
        self.pictograph_component.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.pictograph_component.update_from_beat(beat_data)
        layout.addWidget(self.pictograph_component)

        self.setStyleSheet(
            """
            ClickablePictographFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 6px;
            }
            ClickablePictographFrame:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
                border-width: 3px;
            }
        """
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"beat_{self.beat_data.letter}")
        super().mousePressEvent(event)
