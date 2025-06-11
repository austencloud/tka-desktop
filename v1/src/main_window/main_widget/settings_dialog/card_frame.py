from PyQt6.QtWidgets import QFrame


class CardFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet(
            """
            QFrame {
                border-radius: 15px;
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
                padding: 15px;
            }
        """
        )
