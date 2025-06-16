"""
Thumbnail Processor - Handles image processing and quality enhancement.

Extracted from ThumbnailImageLabel to follow Single Responsibility Principle.
"""

import logging
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QColor
from typing import Optional


class ThumbnailProcessor:
    """
    Handles thumbnail image processing with high-quality scaling.
    
    Responsibilities:
    - Load and validate images
    - Apply multi-step scaling for quality
    - Create error pixmaps when needed
    - Maintain aspect ratios
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def process_image(self, source_path: str, target_size: QSize) -> QPixmap:
        """
        Process image using Qt SmoothTransformation for consistent quality.
        
        Args:
            source_path: Path to source image
            target_size: Target size for thumbnail
            
        Returns:
            High-quality QPixmap using SmoothTransformation
        """
        try:
            # Load original image
            original_pixmap = QPixmap(source_path)
            if original_pixmap.isNull():
                self.logger.error(f"Failed to load image: {source_path}")
                return self.create_error_pixmap(target_size)
            
            # Calculate target dimensions maintaining aspect ratio
            original_size = original_pixmap.size()
            aspect_ratio = original_size.width() / original_size.height()
            
            if target_size.width() / target_size.height() > aspect_ratio:
                new_h = target_size.height()
                new_w = int(target_size.height() * aspect_ratio)
            else:
                new_w = target_size.width()
                new_h = int(target_size.width() / aspect_ratio)
            
            target_w, target_h = new_w, new_h
            scale_factor = min(
                target_w / original_size.width(), target_h / original_size.height()
            )
            
            # Enhanced multi-step scaling with Qt
            if scale_factor < 0.6:  # Lower threshold for better quality
                return self._multi_step_scaling(original_pixmap, target_w, target_h, scale_factor)
            else:
                # Single-step high-quality scaling
                return original_pixmap.scaled(
                    target_w,
                    target_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                
        except Exception as e:
            self.logger.error(f"Image processing failed for {source_path}: {e}")
            return self.create_error_pixmap(target_size)
    
    def _multi_step_scaling(self, original_pixmap: QPixmap, target_w: int, target_h: int, scale_factor: float) -> QPixmap:
        """
        Apply multi-step scaling for better quality on aggressive downscaling.
        
        Args:
            original_pixmap: Original QPixmap
            target_w: Target width
            target_h: Target height
            scale_factor: Overall scale factor
            
        Returns:
            Multi-step scaled QPixmap
        """
        original_size = original_pixmap.size()
        
        if scale_factor < 0.4:
            # Very aggressive downscaling - use 3 stages
            intermediate_factor1 = 0.7
            intermediate_factor2 = 0.5
            
            # Stage 1
            intermediate_w1 = int(original_size.width() * intermediate_factor1)
            intermediate_h1 = int(original_size.height() * intermediate_factor1)
            stage1_pixmap = original_pixmap.scaled(
                intermediate_w1,
                intermediate_h1,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            
            # Stage 2
            intermediate_w2 = int(original_size.width() * intermediate_factor2)
            intermediate_h2 = int(original_size.height() * intermediate_factor2)
            stage2_pixmap = stage1_pixmap.scaled(
                intermediate_w2,
                intermediate_h2,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            
            # Final stage
            return stage2_pixmap.scaled(
                target_w,
                target_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        else:
            # Moderate downscaling - use 2 stages
            intermediate_factor = 0.75
            intermediate_w = int(original_size.width() * intermediate_factor)
            intermediate_h = int(original_size.height() * intermediate_factor)
            
            # Step 1: Scale to intermediate size
            intermediate_pixmap = original_pixmap.scaled(
                intermediate_w,
                intermediate_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            
            # Step 2: Scale to final size
            return intermediate_pixmap.scaled(
                target_w,
                target_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
    
    def create_error_pixmap(self, size: QSize) -> QPixmap:
        """
        Create error pixmap when image processing fails.
        
        Args:
            size: Size for the error pixmap
            
        Returns:
            Error QPixmap with placeholder text
        """
        pixmap = QPixmap(size)
        pixmap.fill(QColor(200, 200, 200))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Image\nError")
        painter.end()
        
        return pixmap
    
    def calculate_aspect_ratio(self, pixmap: QPixmap) -> float:
        """
        Calculate aspect ratio of a pixmap.
        
        Args:
            pixmap: QPixmap to calculate ratio for
            
        Returns:
            Aspect ratio (width/height)
        """
        if pixmap.isNull() or pixmap.height() == 0:
            return 1.0
        return pixmap.width() / pixmap.height()
