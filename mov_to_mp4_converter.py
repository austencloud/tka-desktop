import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class MOVtoMP4Converter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MOV to MP4 Converter")

        # Input file selection
        self.input_label = QLabel("Input .mov file:")
        self.input_line_edit = QLineEdit()
        self.input_browse_button = QPushButton("Browse...")

        # Output file selection
        self.output_label = QLabel("Output .mp4 file:")
        self.output_line_edit = QLineEdit()
        self.output_browse_button = QPushButton("Browse...")

        # Convert button
        self.convert_button = QPushButton("Convert")

        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_line_edit)
        self.layout.addWidget(self.input_browse_button)
        self.layout.addWidget(self.output_label)
        self.layout.addWidget(self.output_line_edit)
        self.layout.addWidget(self.output_browse_button)
        self.layout.addWidget(self.convert_button)

        self.setLayout(self.layout)

        # Connect buttons to functions
        self.input_browse_button.clicked.connect(self.browse_input_file)
        self.output_browse_button.clicked.connect(self.browse_output_file)
        self.convert_button.clicked.connect(self.convert_video)

    def browse_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Input MOV File", "", "MOV Files (*.mov)"
        )
        if file_name:
            self.input_line_edit.setText(file_name)

    def browse_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Select Output MP4 File", "", "MP4 Files (*.mp4)"
        )
        if file_name:
            self.output_line_edit.setText(file_name)

    def convert_video(self):
        input_file = self.input_line_edit.text()
        output_file = self.output_line_edit.text()

        if not input_file:
            QMessageBox.warning(self, "Error", "Please select an input .mov file.")
            return

        if not output_file:
            QMessageBox.warning(self, "Error", "Please select an output .mp4 file.")
            return

        # Use full path to ffmpeg
        ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Update this path as needed

        # Call ffmpeg to convert the video
        try:
            command = [ffmpeg_path, "-i", input_file, output_file]
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode('utf-8')
                QMessageBox.critical(
                    self, "Conversion Failed",
                    f"An error occurred during conversion:\n{error_message}"
                )
            else:
                QMessageBox.information(
                    self, "Conversion Successful",
                    "The video has been converted successfully."
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"An error occurred:\n{str(e)}"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MOVtoMP4Converter()
    window.show()
    sys.exit(app.exec())
