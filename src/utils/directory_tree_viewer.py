import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QLineEdit,
    QLabel,
    QMessageBox,
    QHBoxLayout,
    QCheckBox,
)


class DirectoryTreeViewer(QWidget):
    def __init__(self):
        super().__init__()
        # Get the root directory - because life's too short to click "Browse" every time
        self.default_path = (
            r"F:\\CODE\\the-kinetic-constructor-desktop"  # Project directory
        )

        self.default_exclude_dirs = {
            ".git",
            ".vscode",
            "__pycache__",
            ".pytest_cache",
            "logs",
            "build",
            "dist",
            "node_modules",
            "Output",
            "temp",
            "cached",
            "generated",
            "test_results",
            "arrow_placement",
        }
        self.default_exclude_files = {
            ".gitattributes",
            ".gitignore",
            ".DS_Store",
            "Thumbs.db",
            "desktop.ini",
            "trace_log.txt",
            "profiling_output.txt",
        }
        self.initUI()
        # Generate the tree immediately - instant gratification!
        self.generate_tree()

    def initUI(self):
        self.setWindowTitle("Directory Tree Viewer")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout()

        # Directory Selection (pre-filled with root directory)
        self.path_input = QLineEdit()
        self.path_input.setText(self.default_path)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_directory)

        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        layout.addLayout(path_layout)

        # Exclude Filter Input
        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText("Additional exclusions (comma-separated)")
        layout.addWidget(QLabel("Exclude Directories & Files:"))
        layout.addWidget(self.exclude_input)

        # Limit Number of Items
        self.limit_checkbox = QCheckBox("Limit to 20 items per folder")
        self.limit_checkbox.setChecked(True)
        layout.addWidget(self.limit_checkbox)

        # Generate Tree Button
        self.generate_button = QPushButton("Generate Tree")
        self.generate_button.clicked.connect(self.generate_tree)
        layout.addWidget(self.generate_button)

        # Output Display
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        # Buttons (Copy & Save)
        button_layout = QHBoxLayout()
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.save_button = QPushButton("Save to File")
        self.save_button.clicked.connect(self.save_to_file)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # The rest of the methods remain unchanged
    def select_directory(self):
        """Opens a dialog to select a directory."""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.path_input.setText(dir_path)

    def generate_tree(self):
        """Generates and displays the directory tree."""
        path = self.path_input.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Error", "Please select a valid directory.")
            return

        user_exclusions = {
            d.strip() for d in self.exclude_input.text().split(",") if d.strip()
        }
        exclude_dirs = self.default_exclude_dirs | user_exclusions
        exclude_files = self.default_exclude_files | user_exclusions

        limit_items = self.limit_checkbox.isChecked()
        tree_structure = self.get_directory_tree(
            path, exclude_dirs, exclude_files, limit_items
        )
        self.text_output.setPlainText(tree_structure)

    def get_directory_tree(
        self, path, exclude_dirs, exclude_files, limit_items, indent=""
    ):
        """Recursively generates a directory tree structure."""
        tree_output = []
        try:
            items = [
                item
                for item in os.listdir(path)
                if item not in exclude_dirs
                and not any(item.endswith(ext) for ext in exclude_files)
            ]
        except OSError:
            tree_output.append(f"{indent} [Error opening directory]")
            return "\n".join(tree_output)

        if limit_items and len(items) > 20:
            items_to_show = items[:20]
            remaining_count = len(items) - 20
        else:
            items_to_show = items
            remaining_count = 0

        for i, item in enumerate(items_to_show):
            item_path = os.path.join(path, item)
            is_last = i == len(items_to_show) - 1
            prefix = "└── " if is_last else "├── "
            tree_output.append(
                indent + prefix + item + ("/" if os.path.isdir(item_path) else "")
            )

            if os.path.isdir(item_path):
                tree_output.append(
                    self.get_directory_tree(
                        item_path,
                        exclude_dirs,
                        exclude_files,
                        limit_items,
                        indent + ("    " if is_last else "│   "),
                    )
                )

        if remaining_count > 0:
            tree_output.append(indent + f"└── ... ({remaining_count} more items)")

        return "\n".join(tree_output)

    def copy_to_clipboard(self):
        """Copies the directory tree to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_output.toPlainText())
        QMessageBox.information(self, "Copied", "Directory tree copied to clipboard!")

    def save_to_file(self):
        """Saves the directory tree to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Tree", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.text_output.toPlainText())
            QMessageBox.information(
                self, "Saved", f"Directory tree saved to {file_path}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirectoryTreeViewer()
    window.show()
    sys.exit(app.exec())
