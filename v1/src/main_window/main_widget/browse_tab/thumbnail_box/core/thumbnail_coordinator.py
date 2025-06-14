"""
Thumbnail Coordinator - Orchestrates thumbnail processing components.

This coordinator replaces the complex logic in ThumbnailImageLabel with a clean
architecture that follows the Single Responsibility Principle.
"""

import logging
from typing import TYPE_CHECKING, Optional
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QPixmap

from .thumbnail_processor import ThumbnailProcessor
from .thumbnail_cache_manager import ThumbnailCacheManager
from .thumbnail_event_handler import ThumbnailEventHandler
from .thumbnail_size_calculator import ThumbnailSizeCalculator

if TYPE_CHECKING:
    from ..thumbnail_box import ThumbnailBox


class ThumbnailCoordinator:
    """
    Coordinates thumbnail processing operations using focused components.
    
    This coordinator orchestrates:
    - Image processing and quality enhancement
    - Cache management (disk caching with metadata)
    - Size calculations for different view modes
    - Event handling for user interactions
    - Asynchronous loading and quality enhancement
    
    Each responsibility is handled by a dedicated component following SRP.
    """
    
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        self.thumbnail_box = thumbnail_box
        self.logger = logging.getLogger(__name__)
        
        # Initialize specialized components
        self.processor = ThumbnailProcessor()
        self.cache_manager = ThumbnailCacheManager()
        self.event_handler = ThumbnailEventHandler(thumbnail_box)
        self.size_calculator = ThumbnailSizeCalculator(thumbnail_box)
        
        # Deferred loading timer
        self._load_timer = QTimer()
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._load_pending_image)
        self._pending_path: Optional[str] = None
        self._pending_index: Optional[int] = None
        
        # Quality enhancement timer
        self._quality_timer = QTimer()
        self._quality_timer.setSingleShot(True)
        self._quality_timer.timeout.connect(self._enhance_image_quality)
        self._needs_quality_enhancement = False
        
        self.logger.info("ThumbnailCoordinator initialized with component architecture")
    
    def process_thumbnail_sync(self, image_path: str, is_sequence_viewer: bool) -> QPixmap:
        """
        Process thumbnail synchronously with high quality.
        
        Args:
            image_path: Path to the image file
            is_sequence_viewer: Whether in sequence viewer mode
            
        Returns:
            Processed QPixmap ready for display
        """
        try:
            # Calculate target size based on view mode
            target_size = self.size_calculator.calculate_target_size(is_sequence_viewer)
            
            # Check cache first
            cached_pixmap = self.cache_manager.get_cached_thumbnail(image_path, target_size)
            if cached_pixmap and not cached_pixmap.isNull():
                self.logger.debug(f"Cache hit for thumbnail: {image_path}")
                return cached_pixmap
            
            # Process image with high quality
            processed_pixmap = self.processor.process_image(image_path, target_size)
            
            # Cache the result
            if not processed_pixmap.isNull():
                self.cache_manager.cache_thumbnail(image_path, processed_pixmap, target_size)
            
            return processed_pixmap
            
        except Exception as e:
            self.logger.error(f"Error processing thumbnail {image_path}: {e}")
            return self.processor.create_error_pixmap(target_size)
    
    def process_thumbnail_async(self, image_path: str, index: int) -> None:
        """
        Process thumbnail asynchronously to avoid UI blocking.
        
        Args:
            image_path: Path to the image file
            index: Index in thumbnail list
        """
        self._pending_path = image_path
        self._pending_index = index
        self._load_timer.start(1)  # Start with minimal delay
    
    def _load_pending_image(self) -> None:
        """Load pending image with ultra quality processing."""
        if self._pending_path and self._pending_index is not None:
            try:
                # Delegate to synchronous processing
                is_sequence_viewer = self.thumbnail_box.in_sequence_viewer
                processed_pixmap = self.process_thumbnail_sync(self._pending_path, is_sequence_viewer)
                
                # Notify completion (this would be handled by the main label)
                self.logger.debug(f"Async processing completed: {self._pending_path}")
                
            except Exception as e:
                self.logger.error(f"Error in async thumbnail loading: {e}")
            finally:
                self._pending_path = None
                self._pending_index = None
    
    def _enhance_image_quality(self) -> None:
        """Enhance image quality if needed."""
        if self._needs_quality_enhancement:
            # This would trigger additional quality enhancement
            self.logger.debug("Enhancing image quality")
            self._needs_quality_enhancement = False
    
    def handle_mouse_press(self, event) -> None:
        """Handle mouse press events."""
        self.event_handler.handle_mouse_press(event)
    
    def handle_enter_event(self, event) -> None:
        """Handle mouse enter events."""
        self.event_handler.handle_enter_event(event)
    
    def handle_leave_event(self, event) -> None:
        """Handle mouse leave events."""
        self.event_handler.handle_leave_event(event)
    
    def set_selection_state(self, selected: bool) -> None:
        """Set selection state."""
        self.event_handler.set_selection_state(selected)
    
    def get_border_color(self) -> Optional[str]:
        """Get current border color."""
        return self.event_handler.get_border_color()
    
    def clear_cache(self) -> None:
        """Clear all caches."""
        self.cache_manager.clear_cache()
        self.logger.info("Thumbnail caches cleared")
