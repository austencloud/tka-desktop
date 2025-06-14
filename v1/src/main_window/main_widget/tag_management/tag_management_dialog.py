from typing import TYPE_CHECKING, List, Optional
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

from main_window.main_widget.metadata_extractor import MetaDataExtractor

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class TagManagementDialog(QDialog):
    """Dialog for managing tags for a sequence."""
    
    tagsUpdated = pyqtSignal(list)  # Signal emitted when tags are updated
    
    def __init__(self, main_widget: "MainWidget", thumbnail_path: str):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.thumbnail_path = thumbnail_path
        self.metadata_extractor = MetaDataExtractor()
        self.current_tags = self.metadata_extractor.get_tags(thumbnail_path)
        
        self.setWindowTitle("Manage Tags")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        self._setup_ui()
        self._populate_tag_list()
    
    def _setup_ui(self):
        """Set up the dialog UI components."""
        main_layout = QVBoxLayout(self)
        
        # Instructions label
        instructions = QLabel("Add tags to help organize your sequences. Tags can be used for filtering in the browse tab.")
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Tag list
        self.tag_list = QListWidget()
        self.tag_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        main_layout.addWidget(self.tag_list)
        
        # New tag input
        input_layout = QHBoxLayout()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Enter new tag...")
        self.tag_input.returnPressed.connect(self._add_tag)
        
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self._add_tag)
        
        input_layout.addWidget(self.tag_input)
        input_layout.addWidget(self.add_button)
        main_layout.addLayout(input_layout)
        
        # Remove tag button
        self.remove_button = QPushButton("Remove Selected Tag")
        self.remove_button.clicked.connect(self._remove_selected_tag)
        main_layout.addWidget(self.remove_button)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._save_tags)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)
    
    def _populate_tag_list(self):
        """Populate the tag list with current tags."""
        self.tag_list.clear()
        for tag in self.current_tags:
            item = QListWidgetItem(tag)
            self.tag_list.addItem(item)
    
    def _add_tag(self):
        """Add a new tag to the list."""
        tag_text = self.tag_input.text().strip()
        if not tag_text:
            return
        
        # Check if tag already exists
        for i in range(self.tag_list.count()):
            if self.tag_list.item(i).text().lower() == tag_text.lower():
                QMessageBox.warning(
                    self, "Duplicate Tag", f"The tag '{tag_text}' already exists."
                )
                return
        
        # Add the tag
        self.tag_list.addItem(tag_text)
        self.tag_input.clear()
    
    def _remove_selected_tag(self):
        """Remove the selected tag from the list."""
        selected_items = self.tag_list.selectedItems()
        if not selected_items:
            QMessageBox.information(
                self, "No Selection", "Please select a tag to remove."
            )
            return
        
        for item in selected_items:
            self.tag_list.takeItem(self.tag_list.row(item))
    
    def _save_tags(self):
        """Save the tags to the sequence metadata."""
        tags = []
        for i in range(self.tag_list.count()):
            tags.append(self.tag_list.item(i).text())
        
        try:
            self.metadata_extractor.set_tags(self.thumbnail_path, tags)
            self.tagsUpdated.emit(tags)
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to save tags: {str(e)}"
            )
