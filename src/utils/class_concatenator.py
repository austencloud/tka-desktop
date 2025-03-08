import os
import re
import sys
import winsound  # For a built-in system success sound on Windows
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
)
from PyQt6.QtCore import QUrl

class ClassConcatenatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Python Class Concatenator")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select a directory to concatenate classes:")
        layout.addWidget(self.label)

        self.select_dir_button = QPushButton("Select Directory")
        self.select_dir_button.clicked.connect(self.select_directory)
        layout.addWidget(self.select_dir_button)

        self.run_button = QPushButton("Concatenate Classes")
        self.run_button.clicked.connect(self.concatenate_classes)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.selected_directory = ""

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selected_directory = directory
            self.label.setText(f"Selected Directory: {directory}")

    def concatenate_classes(self):
        if not self.selected_directory:
            QMessageBox.warning(self, "Error", "Please select a directory first.")
            return

        dir_name = os.path.basename(self.selected_directory)
        output_file = os.path.join(self.selected_directory, f"concatenated_{dir_name}.py")

        try:
            imports = set()
            class_definitions = []
            with open(output_file, "w") as outfile:
                for root, _, files in os.walk(self.selected_directory):
                    for file in files:
                        if file.endswith(".py"):
                            file_path = os.path.join(root, file)
                            with open(file_path, "r") as infile:
                                content = infile.read()
                                for line in content.splitlines():
                                    if line.startswith("import") or line.startswith("from"):
                                        imports.add(line)
                                class_definitions.append(f"# From {file}\n" + content)
                outfile.write("\n".join(sorted(imports)) + "\n\n")
                for class_definition in class_definitions:
                    outfile.write(class_definition + "\n\n")
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            QMessageBox.information(
                self, "Success", f"Classes concatenated into {output_file}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassConcatenatorApp()
    window.show()
    sys.exit(app.exec())
