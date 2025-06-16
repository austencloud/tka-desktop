# src/main_window/main_widget/sequence_card_tab/loading/loading_dialog.py
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class SequenceCardLoadingDialog(QDialog):
    """A dialog that shows loading progress for sequence card data."""

    canceled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading Sequence Cards")
        self.setMinimumWidth(400)
        self.setMinimumHeight(150)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
        )
        self.setModal(True)

        self._setup_ui()

    def _setup_ui(self):
        """Set up the dialog UI with progress bar and status labels."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title label
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)

        title_label = QLabel("Loading Sequence Cards")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(separator)

        # Operation label
        self.operation_label = QLabel("Loading sequence card data...")
        self.operation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.operation_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% (%v/%m)")
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 5px;
                text-align: center;
                height: 25px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
                border-radius: 5px;
            }
        """
        )
        main_layout.addWidget(self.progress_bar)

        # Cancel button
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5722;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """
        )
        self.cancel_button.clicked.connect(self.on_cancel)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def on_cancel(self):
        """Handle cancel button click."""
        self.canceled.emit()
        self.reject()

    def set_progress(self, current: int, total: int):
        """Update the progress bar."""
        if total > 0:
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)

    def set_operation(self, operation: str):
        """Update the operation label."""
        self.operation_label.setText(operation)
