# src/main_window/main_widget/sequence_card_tab/loading/progress_dialog.py
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
import psutil


class SequenceCardProgressDialog(QDialog):
    """A dialog that shows progress during sequence card image regeneration."""

    canceled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Regenerating Sequence Card Images")
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)
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

        title_label = QLabel("Regenerating Sequence Card Images")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(separator)

        # Current file label
        self.current_file_label = QLabel("Initializing...")
        self.current_file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.current_file_label)

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

        # Status label
        self.status_label = QLabel("0/0 images processed")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Statistics labels
        stats_layout = QHBoxLayout()

        self.regenerated_label = QLabel("Regenerated: 0")
        self.skipped_label = QLabel("Skipped: 0")
        self.failed_label = QLabel("Failed: 0")

        stats_layout.addWidget(self.regenerated_label)
        stats_layout.addWidget(self.skipped_label)
        stats_layout.addWidget(self.failed_label)

        main_layout.addLayout(stats_layout)

        # Memory usage label
        self.memory_label = QLabel("Memory usage: 0 MB")
        self.memory_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.memory_label.setStyleSheet("color: #666666; font-size: 10px;")
        main_layout.addWidget(self.memory_label)

        # Add a separator line
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(separator2)

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
            percentage = int((current / total) * 100)
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(current)
            self.status_label.setText(f"{current}/{total} images processed")

    def set_current_file(self, file_path: str):
        """Update the current file label."""
        # Truncate the path if it's too long
        if len(file_path) > 60:
            file_path = "..." + file_path[-57:]
        self.current_file_label.setText(f"Processing: {file_path}")

    def set_statistics(
        self, regenerated: int, skipped: int, failed: int, efficiency: float = None
    ):
        """
        Update the statistics labels.

        Args:
            regenerated: Number of regenerated images
            skipped: Number of skipped images
            failed: Number of failed images
            efficiency: Optional cache efficiency percentage
        """
        # Update basic statistics
        self.regenerated_label.setText(f"Regenerated: {regenerated}")

        # Add efficiency percentage to skipped label if provided
        if efficiency is not None:
            self.skipped_label.setText(
                f"Skipped: {skipped} (Efficiency: {efficiency:.1f}%)"
            )

            # Change color based on efficiency
            if efficiency > 90:  # Excellent efficiency
                self.skipped_label.setStyleSheet("color: #00aa00; font-weight: bold;")
            elif efficiency > 70:  # Good efficiency
                self.skipped_label.setStyleSheet("color: #00aa00;")
            elif efficiency > 50:  # Moderate efficiency
                self.skipped_label.setStyleSheet("color: #888800;")
            else:  # Poor efficiency
                self.skipped_label.setStyleSheet("color: #aa5500;")
        else:
            self.skipped_label.setText(f"Skipped: {skipped}")
            self.skipped_label.setStyleSheet("")

        self.failed_label.setText(f"Failed: {failed}")

    def update_memory_usage(self):
        """Update the memory usage label with current process memory information."""
        try:
            # Get current process
            process = psutil.Process()

            # Get memory info in MB
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)

            # Update label
            self.memory_label.setText(f"Memory usage: {memory_mb:.1f} MB")

            # Change color based on memory usage
            if memory_mb > 1000:  # Over 1GB
                self.memory_label.setStyleSheet("color: #ff0000; font-size: 10px;")
            elif memory_mb > 500:  # Over 500MB
                self.memory_label.setStyleSheet("color: #ff6600; font-size: 10px;")
            else:
                self.memory_label.setStyleSheet("color: #666666; font-size: 10px;")
        except Exception as e:
            print(f"Error updating memory usage: {e}")
            self.memory_label.setText("Memory usage: Unknown")

    def set_operation(self, operation: str):
        """Update the current operation label."""
        self.current_file_label.setText(operation)
