"""
Image drag and drop handler for the main widget.

This module provides comprehensive drag and drop functionality for images,
allowing users to drag images from external applications and drop them
onto the application window.
"""

import os
import logging
from typing import TYPE_CHECKING, List, Optional, Callable
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtWidgets import QWidget, QMessageBox

if TYPE_CHECKING:
    from core.application_context import ApplicationContext

logger = logging.getLogger(__name__)


class ImageDragDropHandler(QObject):
    """
    Handles drag and drop operations for images.
    
    This class provides:
    1. Detection of image files being dragged
    2. Validation of supported image formats
    3. Processing of dropped images
    4. Integration with existing image handling systems
    5. User feedback and error handling
    """
    
    # Signals for communication with other components
    image_dropped = pyqtSignal(str)  # image_path
    images_dropped = pyqtSignal(list)  # list of image_paths
    drop_error = pyqtSignal(str)  # error_message
    
    # Supported image formats
    SUPPORTED_FORMATS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.svg', '.ico', '.ppm', '.pgm', '.pbm'
    }
    
    def __init__(self, parent_widget: QWidget, app_context: "ApplicationContext"):
        """
        Initialize the image drag and drop handler.
        
        Args:
            parent_widget: The widget that will accept drops
            app_context: Application context for accessing services
        """
        super().__init__(parent_widget)
        
        self.parent_widget = parent_widget
        self.app_context = app_context
        self.enabled = True
        
        # Callbacks for different drop scenarios
        self.single_image_callback: Optional[Callable[[str], None]] = None
        self.multiple_images_callback: Optional[Callable[[List[str]], None]] = None
        
        # Enable drag and drop on the parent widget
        self._setup_drag_drop()
        
        logger.info("ImageDragDropHandler initialized")
    
    def _setup_drag_drop(self) -> None:
        """Set up drag and drop on the parent widget."""
        self.parent_widget.setAcceptDrops(True)
        
        # Store original event handlers if they exist
        self._original_drag_enter = getattr(self.parent_widget, 'dragEnterEvent', None)
        self._original_drag_move = getattr(self.parent_widget, 'dragMoveEvent', None)
        self._original_drop = getattr(self.parent_widget, 'dropEvent', None)
        
        # Override event handlers
        self.parent_widget.dragEnterEvent = self.drag_enter_event
        self.parent_widget.dragMoveEvent = self.drag_move_event
        self.parent_widget.dropEvent = self.drop_event
    
    def set_single_image_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for when a single image is dropped."""
        self.single_image_callback = callback
    
    def set_multiple_images_callback(self, callback: Callable[[List[str]], None]) -> None:
        """Set callback for when multiple images are dropped."""
        self.multiple_images_callback = callback
    
    def enable(self) -> None:
        """Enable drag and drop functionality."""
        self.enabled = True
        self.parent_widget.setAcceptDrops(True)
        logger.debug("Image drag and drop enabled")
    
    def disable(self) -> None:
        """Disable drag and drop functionality."""
        self.enabled = False
        self.parent_widget.setAcceptDrops(False)
        logger.debug("Image drag and drop disabled")
    
    def drag_enter_event(self, event: QDragEnterEvent) -> None:
        """Handle drag enter events."""
        if not self.enabled:
            event.ignore()
            return
        
        # Check if the drag contains files
        if event.mimeData().hasUrls():
            # Check if any of the files are images
            image_files = self._extract_image_files(event.mimeData())
            if image_files:
                event.acceptProposedAction()
                logger.debug(f"Drag enter accepted: {len(image_files)} image(s)")
                return
        
        # Check for image data directly
        if self._has_image_data(event.mimeData()):
            event.acceptProposedAction()
            logger.debug("Drag enter accepted: direct image data")
            return
        
        # Call original handler if it exists
        if self._original_drag_enter:
            self._original_drag_enter(event)
        else:
            event.ignore()
    
    def drag_move_event(self, event: QDragMoveEvent) -> None:
        """Handle drag move events."""
        if not self.enabled:
            event.ignore()
            return
        
        # Accept the same conditions as drag enter
        if event.mimeData().hasUrls() or self._has_image_data(event.mimeData()):
            event.acceptProposedAction()
        else:
            # Call original handler if it exists
            if self._original_drag_move:
                self._original_drag_move(event)
            else:
                event.ignore()
    
    def drop_event(self, event: QDropEvent) -> None:
        """Handle drop events."""
        if not self.enabled:
            event.ignore()
            return
        
        try:
            # Extract image files from the drop
            image_files = self._extract_image_files(event.mimeData())
            
            if image_files:
                self._process_dropped_images(image_files)
                event.acceptProposedAction()
                logger.info(f"Successfully processed {len(image_files)} dropped image(s)")
                return
            
            # Check for direct image data
            if self._has_image_data(event.mimeData()):
                self._process_image_data(event.mimeData())
                event.acceptProposedAction()
                logger.info("Successfully processed dropped image data")
                return
            
            # Call original handler if it exists
            if self._original_drop:
                self._original_drop(event)
            else:
                event.ignore()
                
        except Exception as e:
            error_msg = f"Error processing dropped images: {str(e)}"
            logger.error(error_msg)
            self.drop_error.emit(error_msg)
            self._show_error_message("Drop Error", error_msg)
            event.ignore()
    
    def _extract_image_files(self, mime_data: QMimeData) -> List[str]:
        """Extract image file paths from mime data."""
        image_files = []
        
        if mime_data.hasUrls():
            for url in mime_data.urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if self._is_image_file(file_path):
                        image_files.append(file_path)
        
        return image_files
    
    def _is_image_file(self, file_path: str) -> bool:
        """Check if a file is a supported image format."""
        try:
            path = Path(file_path)
            return path.suffix.lower() in self.SUPPORTED_FORMATS and path.exists()
        except Exception:
            return False
    
    def _has_image_data(self, mime_data: QMimeData) -> bool:
        """Check if mime data contains direct image data."""
        return (mime_data.hasImage() or 
                mime_data.hasFormat("image/png") or
                mime_data.hasFormat("image/jpeg") or
                mime_data.hasFormat("image/gif") or
                mime_data.hasFormat("image/bmp"))
    
    def _process_dropped_images(self, image_files: List[str]) -> None:
        """Process a list of dropped image files."""
        if not image_files:
            return
        
        # Emit signals
        if len(image_files) == 1:
            self.image_dropped.emit(image_files[0])
            if self.single_image_callback:
                self.single_image_callback(image_files[0])
        else:
            self.images_dropped.emit(image_files)
            if self.multiple_images_callback:
                self.multiple_images_callback(image_files)
    
    def _process_image_data(self, mime_data: QMimeData) -> None:
        """Process direct image data from mime data."""
        # This could be implemented to handle images copied from web browsers, etc.
        # For now, we'll just log that we received image data
        logger.info("Received direct image data (not yet implemented)")
        self.drop_error.emit("Direct image data drops are not yet supported. Please save the image and drag the file instead.")
    
    def _show_error_message(self, title: str, message: str) -> None:
        """Show an error message to the user."""
        try:
            QMessageBox.warning(self.parent_widget, title, message)
        except Exception as e:
            logger.error(f"Failed to show error message: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources and restore original event handlers."""
        if hasattr(self.parent_widget, 'dragEnterEvent'):
            if self._original_drag_enter:
                self.parent_widget.dragEnterEvent = self._original_drag_enter
            else:
                delattr(self.parent_widget, 'dragEnterEvent')
        
        if hasattr(self.parent_widget, 'dragMoveEvent'):
            if self._original_drag_move:
                self.parent_widget.dragMoveEvent = self._original_drag_move
            else:
                delattr(self.parent_widget, 'dragMoveEvent')
        
        if hasattr(self.parent_widget, 'dropEvent'):
            if self._original_drop:
                self.parent_widget.dropEvent = self._original_drop
            else:
                delattr(self.parent_widget, 'dropEvent')
        
        logger.info("ImageDragDropHandler cleaned up")
