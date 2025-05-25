from typing import TYPE_CHECKING, Optional, Dict
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath


class ProfilePictureManager:
    """Manages user profile pictures, including storage and processing."""

    _profile_pictures: Dict[str, QPixmap] = {}

    @classmethod
    def save_profile_picture(cls, username: str, pixmap: QPixmap) -> None:
        """Saves a profile picture for a user."""
        if pixmap and not pixmap.isNull():
            # Make sure the image is square
            square_pixmap = cls.crop_to_square(pixmap)
            cls._profile_pictures[username] = square_pixmap

    @classmethod
    def get_profile_picture(cls, username: str) -> Optional[QPixmap]:
        """Gets a user's profile picture if available."""
        return cls._profile_pictures.get(username)

    @classmethod
    def delete_profile_picture(cls, username: str) -> None:
        """Removes a user's profile picture."""
        if username in cls._profile_pictures:
            del cls._profile_pictures[username]

    @classmethod
    def crop_to_square(cls, pixmap: QPixmap) -> QPixmap:
        """Crops a pixmap to a square based on the smaller dimension."""
        if pixmap.isNull():
            return pixmap

        width = pixmap.width()
        height = pixmap.height()

        # Determine the size of the square
        size = min(width, height)

        # Calculate position to crop from center
        x = (width - size) // 2
        y = (height - size) // 2

        # Crop the image
        cropped = pixmap.copy(x, y, size, size)
        return cropped

    @classmethod
    def create_circular_pixmap(cls, pixmap: QPixmap, size: int) -> QPixmap:
        """Creates a circular version of the pixmap at the specified size."""
        if pixmap.isNull():
            return pixmap

        # Create a square pixmap of the desired size
        square_pixmap = cls.crop_to_square(pixmap).scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        # Create a new transparent pixmap
        rounded = QPixmap(size, size)
        rounded.fill(Qt.GlobalColor.transparent)

        # Create a circular path
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)

        # Draw the original image clipped by the circular path
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, square_pixmap)
        painter.end()

        return rounded
