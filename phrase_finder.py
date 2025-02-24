import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

class PhraseFinder(QWidget):
    """PhraseFinder is a PyQt6-based GUI application that allows users to search for a specific phrase within Python files in a given directory. The application provides functionality to select a search directory, specify an output file, and input the phrase to search for. It then searches through the Python files in the specified directory, extracts relevant class definitions containing the phrase, and writes the results to the output file.
    Attributes:
        search_dir (str): The default directory to search for Python files.
        output_file (str): The default file to write the search results.
        default_phrase (str): The default phrase to search for in the Python files.
    Methods:
        __init__(): Initializes the PhraseFinder application, setting up the UI and default values.
        init_ui(): Sets up the user interface components, including labels, buttons, and input fields.
        choose_directory(): Opens a dialog for the user to select a directory to search for Python files.
        choose_output_file(): Opens a dialog for the user to select an output file to save the search results.
        on_search_clicked(): Handles the search button click event, performing the search and writing results to the output file.
        search_and_concatenate(directory, phrase, out_file): Searches for the specified phrase in Python files within the given directory, extracts matching class definitions, and writes them to the output file.
        extract_global_section(lines): Extracts the global section (all lines before the first top-level class) from a list of lines from a file.
        split_into_class_blocks(lines): Splits a list of lines from a file into blocks corresponding to top-level class definitions.
    Usage:
        To use the PhraseFinder application, create an instance of the PhraseFinder class and call its methods as needed to set up the search parameters and perform the search."""
        
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phrase Finder")

        # Default search directory and output file
        self.search_dir = r"main_window"
        self.output_file = r"found_phrase_matches.py"
        self.default_phrase = "paintEvent"  # or any default phrase

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.dir_label = QLabel(f"Search Directory:\n{self.search_dir}")
        layout.addWidget(self.dir_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.dir_button = QPushButton("Choose Directory")
        self.dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.dir_button)

        self.phrase_input = QLineEdit()
        self.phrase_input.setPlaceholderText("Enter phrase to find...")
        self.phrase_input.setText(self.default_phrase)
        layout.addWidget(self.phrase_input)

        self.search_button = QPushButton("Search and Concatenate")
        self.search_button.clicked.connect(self.on_search_clicked)
        layout.addWidget(self.search_button)

        self.output_label = QLabel(f"Results will be written to:\n{self.output_file}")
        layout.addWidget(self.output_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.out_button = QPushButton("Choose Output File")
        self.out_button.clicked.connect(self.choose_output_file)
        layout.addWidget(self.out_button)

        self.setLayout(layout)

    def choose_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", self.search_dir)
        if dir_path:
            self.search_dir = dir_path
            self.dir_label.setText(f"Search Directory:\n{self.search_dir}")

    def choose_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", self.output_file)
        if file_path:
            self.output_file = file_path
            self.output_label.setText(f"Results will be written to:\n{self.output_file}")

    def on_search_clicked(self):
        phrase = self.phrase_input.text().strip()
        if not phrase:
            self.output_label.setText("Please enter a phrase to search for.")
            return

        matches_found = self.search_and_concatenate(self.search_dir, phrase, self.output_file)
        if matches_found == 0:
            self.output_label.setText(f"No matches found for '{phrase}'.")
        else:
            self.output_label.setText(
                f"Found {matches_found} matching classes for '{phrase}'.\nResults saved to:\n{self.output_file}"
            )

    # -------------------------------------------------------------------------
    def search_and_concatenate(self, directory, phrase, out_file):
        """
        For each .py file in 'directory' (recursively):
          1. Extract the global section (all lines before the first top-level class).
          2. Split the remainder of the file into top-level class blocks.
          3. For each class block that (when joined) contains the search phrase,
             output:
               - A file header (once per file)
               - The global section (global imports)
               - The entire class block exactly as it appears.
        Returns the total number of matching classes.
        """
        total_matched = 0

        with open(out_file, "w", encoding="utf-8") as out:
            out.write(f"# GENERATED FILE: Matching classes for phrase: '{phrase}'\n")
            out.write(f"# Search directory: {directory}\n\n")

            for root, _, files in os.walk(directory):
                for file in files:
                    if not file.endswith(".py"):
                        continue
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            all_lines = f.readlines()
                    except Exception:
                        continue

                    # Get global section (from start until first top-level class)
                    global_section = self.extract_global_section(all_lines)
                    # Split into class blocks (each block is kept verbatim)
                    class_blocks = self.split_into_class_blocks(all_lines)
                    if not class_blocks:
                        continue

                    matched_blocks = []
                    for start_line, block in class_blocks:
                        block_text = "".join(block)
                        if phrase in block_text:
                            matched_blocks.append((start_line, block))

                    if matched_blocks:
                        out.write("# -------------------------------------------------------\n")
                        out.write(f"# File: {full_path}\n")
                        out.write("# -------------------------------------------------------\n")
                        # Write the global section first (all global imports)
                        out.writelines(global_section)
                        out.write("\n")
                        for (lineno, block) in matched_blocks:
                            out.write(f"# [Line {lineno}]\n")
                            out.writelines(block)
                            total_matched += 1

        return total_matched

    def extract_global_section(self, lines):
        """
        Given a list of lines from a file, return the lines from the start
        up to (but not including) the first top-level class definition.
        """
        global_lines = []
        for line in lines:
            if re.match(r'^\s*class\s+', line):
                break
            global_lines.append(line)
        return global_lines

    def split_into_class_blocks(self, lines):
        """
        Splits the file (given as a list of lines) into blocks corresponding
        to top-level class definitions.
        Returns a list of tuples: (start_line_number, block_lines)
        where start_line_number is 1-indexed.
        """
        class_pattern = re.compile(r'^\s*class\s+')
        indices = [i for i, line in enumerate(lines) if class_pattern.match(line)]
        blocks = []
        for idx, start in enumerate(indices):
            end = indices[idx+1] if idx+1 < len(indices) else len(lines)
            block = lines[start:end]
            blocks.append((start + 1, block))
        return blocks

def main():
    app = QApplication(sys.argv)
    window = PhraseFinder()
    window.resize(600, 300)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
