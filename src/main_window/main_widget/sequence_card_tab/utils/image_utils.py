# src/main_window/main_widget/sequence_card_tab/utils/image_utils.py
import io
from typing import Optional
from PyQt6.QtGui import QImage
from PyQt6.QtCore import Qt, QSize, QBuffer
from PIL import Image, ImageEnhance


class ImageProcessor:
    """
    Utility class for processing images with optimized quality and performance.
    
    This class provides:
    1. High-quality image scaling
    2. Memory-efficient image processing
    3. Format conversion between QImage/QPixmap and PIL Image
    4. Image enhancement and effects
    """
    
    @staticmethod
    def scale_image(
        image: QImage, 
        target_size: QSize, 
        keep_aspect_ratio: bool = True,
        high_quality: bool = True
    ) -> QImage:
        """
        Scale an image with high quality.
        
        Args:
            image: Source QImage
            target_size: Target size
            keep_aspect_ratio: Whether to maintain aspect ratio
            high_quality: Whether to use high-quality scaling
            
        Returns:
            Scaled QImage
        """
        if image.isNull():
            return QImage()
            
        # Determine transformation mode
        transform_mode = (
            Qt.TransformationMode.SmoothTransformation 
            if high_quality 
            else Qt.TransformationMode.SmoothTransformation
        )
        
        # Determine aspect ratio mode
        aspect_mode = (
            Qt.AspectRatioMode.KeepAspectRatio 
            if keep_aspect_ratio 
            else Qt.AspectRatioMode.IgnoreAspectRatio
        )
        
        # Scale the image
        return image.scaled(
            target_size.width(),
            target_size.height(),
            aspect_mode,
            transform_mode
        )
    
    @staticmethod
    def qimage_to_pil(qimage: QImage) -> Optional[Image.Image]:
        """
        Convert QImage to PIL Image.
        
        Args:
            qimage: Source QImage
            
        Returns:
            PIL Image or None if conversion fails
        """
        if qimage.isNull():
            return None
            
        # Convert to ARGB32 format
        qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
        
        # Save to buffer
        buffer = QBuffer()
        buffer.open(QBuffer.OpenModeFlag.ReadWrite)
        qimage.save(buffer, "PNG")
        buffer.seek(0)
        
        # Load with PIL
        try:
            pil_image = Image.open(io.BytesIO(buffer.data().data()))
            return pil_image.copy()  # Return a copy to ensure buffer can be released
        except Exception as e:
            print(f"Error converting QImage to PIL Image: {e}")
            return None
    
    @staticmethod
    def pil_to_qimage(pil_image: Image.Image) -> QImage:
        """
        Convert PIL Image to QImage.
        
        Args:
            pil_image: Source PIL Image
            
        Returns:
            QImage
        """
        if pil_image is None:
            return QImage()
            
        # Convert to RGB or RGBA
        if pil_image.mode != "RGB" and pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")
            
        # Save to buffer
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Load as QImage
        return QImage.fromData(buffer.getvalue())
    
    @staticmethod
    def enhance_image(
        image: QImage, 
        brightness: float = 1.0,
        contrast: float = 1.0,
        sharpness: float = 1.0
    ) -> QImage:
        """
        Enhance an image with adjustable parameters.
        
        Args:
            image: Source QImage
            brightness: Brightness factor (1.0 = original)
            contrast: Contrast factor (1.0 = original)
            sharpness: Sharpness factor (1.0 = original)
            
        Returns:
            Enhanced QImage
        """
        # Convert to PIL
        pil_image = ImageProcessor.qimage_to_pil(image)
        if pil_image is None:
            return image
            
        # Apply enhancements
        if brightness != 1.0:
            pil_image = ImageEnhance.Brightness(pil_image).enhance(brightness)
        if contrast != 1.0:
            pil_image = ImageEnhance.Contrast(pil_image).enhance(contrast)
        if sharpness != 1.0:
            pil_image = ImageEnhance.Sharpness(pil_image).enhance(sharpness)
            
        # Convert back to QImage
        return ImageProcessor.pil_to_qimage(pil_image)
