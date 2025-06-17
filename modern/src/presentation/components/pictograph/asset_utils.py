"""
Asset utilities for pictograph rendering.

Handles path management and asset loading for SVG files.
"""

import os


def get_image_path(filename: str) -> str:
    """Get the path to an image file from the root assets directory."""
    assets_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "..",
        "..",
        "..",
        "images",
        filename,
    )
    normalized_path = os.path.normpath(assets_path)

    if not os.path.exists(normalized_path):
        print(f"Warning: Asset not found: {normalized_path}")
        print("Please ensure required assets are in root/images/")

    return normalized_path
