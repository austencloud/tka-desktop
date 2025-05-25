"""
Image drop processor for handling dropped images.

This module processes images that are dropped onto the application,
providing various options for what to do with them.
"""

import os
import shutil
import logging
from typing import TYPE_CHECKING, List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from core.application_context import ApplicationContext

logger = logging.getLogger(__name__)


class ImageDropProcessor(QObject):
    """
    Processes images that are dropped onto the application.
    
    This class provides:
    1. Image validation and analysis
    2. Multiple processing options for dropped images
    3. Integration with existing image systems
    4. User choice dialogs for processing options
    5. Background processing for large images
    """
    
    # Signals for processing status
    processing_started = pyqtSignal(str)  # image_path
    processing_completed = pyqtSignal(str, dict)  # image_path, result_data
    processing_failed = pyqtSignal(str, str)  # image_path, error_message
    
    def __init__(self, app_context: "ApplicationContext"):
        """
        Initialize the image drop processor.
        
        Args:
            app_context: Application context for accessing services
        """
        super().__init__()
        
        self.app_context = app_context
        self.processing_queue: List[str] = []
        self.is_processing = False
        
        # Processing options
        self.processing_options = {
            "import_to_library": "Import to Image Library",
            "set_as_background": "Set as Background Image",
            "create_sequence_card": "Create Sequence Card",
            "analyze_for_pictographs": "Analyze for Pictographs",
            "open_in_viewer": "Open in Image Viewer"
        }
        
        logger.info("ImageDropProcessor initialized")
    
    def process_single_image(self, image_path: str) -> None:
        """
        Process a single dropped image.
        
        Args:
            image_path: Path to the image file
        """
        logger.info(f"Processing single image: {os.path.basename(image_path)}")
        
        # Validate the image
        if not self._validate_image(image_path):
            error_msg = f"Invalid or corrupted image: {os.path.basename(image_path)}"
            logger.error(error_msg)
            self.processing_failed.emit(image_path, error_msg)
            return
        
        # Show processing options dialog
        self._show_processing_options_dialog(image_path)
    
    def process_multiple_images(self, image_paths: List[str]) -> None:
        """
        Process multiple dropped images.
        
        Args:
            image_paths: List of image file paths
        """
        logger.info(f"Processing {len(image_paths)} images")
        
        # Validate all images first
        valid_images = []
        for image_path in image_paths:
            if self._validate_image(image_path):
                valid_images.append(image_path)
            else:
                logger.warning(f"Skipping invalid image: {os.path.basename(image_path)}")
        
        if not valid_images:
            error_msg = "No valid images found in the dropped files"
            logger.error(error_msg)
            self.processing_failed.emit("", error_msg)
            return
        
        # Show batch processing options dialog
        self._show_batch_processing_dialog(valid_images)
    
    def _validate_image(self, image_path: str) -> bool:
        """
        Validate an image file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            True if the image is valid, False otherwise
        """
        try:
            path = Path(image_path)
            
            # Check if file exists
            if not path.exists():
                return False
            
            # Check file size (reject files larger than 50MB)
            if path.stat().st_size > 50 * 1024 * 1024:
                logger.warning(f"Image too large: {path.stat().st_size} bytes")
                return False
            
            # Try to load the image to verify it's valid
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                return False
            
            # Check dimensions (reject images larger than 10000x10000)
            if pixmap.width() > 10000 or pixmap.height() > 10000:
                logger.warning(f"Image dimensions too large: {pixmap.width()}x{pixmap.height()}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating image {image_path}: {e}")
            return False
    
    def _show_processing_options_dialog(self, image_path: str) -> None:
        """Show dialog for choosing how to process a single image."""
        dialog = ImageProcessingDialog(image_path, self.processing_options)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_option = dialog.get_selected_option()
            self._execute_processing_option(image_path, selected_option)
    
    def _show_batch_processing_dialog(self, image_paths: List[str]) -> None:
        """Show dialog for choosing how to process multiple images."""
        dialog = BatchImageProcessingDialog(image_paths, self.processing_options)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_option = dialog.get_selected_option()
            for image_path in image_paths:
                self._execute_processing_option(image_path, selected_option)
    
    def _execute_processing_option(self, image_path: str, option: str) -> None:
        """
        Execute the selected processing option.
        
        Args:
            image_path: Path to the image file
            option: Selected processing option
        """
        self.processing_started.emit(image_path)
        
        try:
            if option == "import_to_library":
                self._import_to_library(image_path)
            elif option == "set_as_background":
                self._set_as_background(image_path)
            elif option == "create_sequence_card":
                self._create_sequence_card(image_path)
            elif option == "analyze_for_pictographs":
                self._analyze_for_pictographs(image_path)
            elif option == "open_in_viewer":
                self._open_in_viewer(image_path)
            else:
                raise ValueError(f"Unknown processing option: {option}")
            
            result_data = {"option": option, "success": True}
            self.processing_completed.emit(image_path, result_data)
            
        except Exception as e:
            error_msg = f"Failed to process image with option '{option}': {str(e)}"
            logger.error(error_msg)
            self.processing_failed.emit(image_path, error_msg)
    
    def _import_to_library(self, image_path: str) -> None:
        """Import image to the application's image library."""
        # Create images directory if it doesn't exist
        images_dir = Path("images/imported")
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        original_name = Path(image_path).name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{timestamp}_{original_name}"
        destination = images_dir / new_name
        
        # Copy the image
        shutil.copy2(image_path, destination)
        logger.info(f"Imported image to library: {new_name}")
    
    def _set_as_background(self, image_path: str) -> None:
        """Set the image as the application background."""
        # This would integrate with the background system
        logger.info(f"Setting background image: {os.path.basename(image_path)}")
        # TODO: Implement background setting functionality
    
    def _create_sequence_card(self, image_path: str) -> None:
        """Create a sequence card from the image."""
        # This would integrate with the sequence card system
        logger.info(f"Creating sequence card from: {os.path.basename(image_path)}")
        # TODO: Implement sequence card creation functionality
    
    def _analyze_for_pictographs(self, image_path: str) -> None:
        """Analyze the image for pictographs."""
        # This would integrate with the pictograph analysis system
        logger.info(f"Analyzing for pictographs: {os.path.basename(image_path)}")
        # TODO: Implement pictograph analysis functionality
    
    def _open_in_viewer(self, image_path: str) -> None:
        """Open the image in the application's image viewer."""
        # This would integrate with the full screen overlay or image viewer
        logger.info(f"Opening in viewer: {os.path.basename(image_path)}")
        # TODO: Implement image viewer functionality


class ImageProcessingDialog(QDialog):
    """Dialog for choosing how to process a single dropped image."""
    
    def __init__(self, image_path: str, options: Dict[str, str]):
        super().__init__()
        
        self.image_path = image_path
        self.options = options
        self.selected_option = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        self.setWindowTitle("Process Dropped Image")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Image info
        image_name = os.path.basename(self.image_path)
        info_label = QLabel(f"How would you like to process '{image_name}'?")
        layout.addWidget(info_label)
        
        # Options combo box
        self.options_combo = QComboBox()
        for key, value in self.options.items():
            self.options_combo.addItem(value, key)
        layout.addWidget(self.options_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_selected_option(self) -> str:
        """Get the selected processing option."""
        return self.options_combo.currentData()


class BatchImageProcessingDialog(QDialog):
    """Dialog for choosing how to process multiple dropped images."""
    
    def __init__(self, image_paths: List[str], options: Dict[str, str]):
        super().__init__()
        
        self.image_paths = image_paths
        self.options = options
        self.selected_option = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the dialog UI."""
        self.setWindowTitle("Process Dropped Images")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout(self)
        
        # Image info
        info_label = QLabel(f"How would you like to process {len(self.image_paths)} images?")
        layout.addWidget(info_label)
        
        # Options combo box
        self.options_combo = QComboBox()
        for key, value in self.options.items():
            self.options_combo.addItem(value, key)
        layout.addWidget(self.options_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_selected_option(self) -> str:
        """Get the selected processing option."""
        return self.options_combo.currentData()
