# src/main_window/main_widget/sequence_card_tab/components/display/image_label_factory.py
from typing import Dict, Any
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageLabelFactory:
    """
    Creates and configures image labels for sequence card display.
    
    This class is responsible for:
    1. Creating labels for displaying sequence card images
    2. Configuring label properties and styling
    3. Storing metadata in label properties
    """
    
    def create_image_label(self, sequence: Dict[str, Any], pixmap: QPixmap) -> QLabel:
        """
        Create a label for displaying the image without redundant header.

        Args:
            sequence: The sequence data (used for metadata if needed)
            pixmap: The image to display

        Returns:
            QLabel: A label containing the image
        """
        # Create a simple image label without the header
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setScaledContents(False)

        # Store sequence metadata in the label's properties for potential future use
        if sequence and "word" in sequence:
            image_label.setProperty("sequence_word", sequence["word"])
        if (
            sequence
            and "metadata" in sequence
            and "sequence_length" in sequence["metadata"]
        ):
            image_label.setProperty(
                "sequence_length", sequence["metadata"]["sequence_length"]
            )

        # Set size policy
        image_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        image_label.setFixedSize(pixmap.size())

        return image_label
