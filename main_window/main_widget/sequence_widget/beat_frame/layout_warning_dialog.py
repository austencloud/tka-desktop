from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class LayoutWarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Warning")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        message = QLabel(
            "You are setting the number of beats to fewer than the number of filled beats. "
            "Do you wish to proceed and clear the excess beats?",
            self,
        )
        message.setWordWrap(True)
        layout.addWidget(message)

        button_layout = QHBoxLayout()
        self.proceed_button = QPushButton("Proceed", self)
        self.cancel_button = QPushButton("Cancel", self)

        button_layout.addWidget(self.proceed_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.proceed_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
