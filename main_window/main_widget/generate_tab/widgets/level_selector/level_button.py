from PyQt6.QtWidgets import QWidget, QLabel, QStackedLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QMouseEvent


class LevelButton(QWidget):
    clicked = pyqtSignal(int)  # Custom signal to emit the level number

    def __init__(self, level: int, icon_path: str, parent=None):
        super().__init__(parent)
        self.level = level

        # Create a stacked layout
        self.layout: QStackedLayout = QStackedLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the background image (icon)
        self.icon_label = QLabel(self)
        pixmap = QPixmap(icon_path).scaled(
            60,
            60,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the number label
        self.number_label = QLabel(str(level), self)
        self.number_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        self.number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.number_label.setStyleSheet("color: white; background: transparent;")

        # Add both widgets to the stacked layout
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.number_label)

        # Set the widget to be interactive
        self.setFixedSize(70, 70)  # Adjust size to fit the image and label
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: "QMouseEvent"):
        """Handle mouse press event and emit the custom signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.level)
