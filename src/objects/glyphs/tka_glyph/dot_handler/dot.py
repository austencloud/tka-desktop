# dot.py

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from objects.glyphs.tka_glyph.tka_glyph import DotHandler


_DOT_RENDERER_CACHE = {}


class Dot(QGraphicsSvgItem):
    def __init__(self, dot_handler: "DotHandler"):
        super().__init__()
        self.dot_handler = dot_handler
        self.renderer = None  # Initialize renderer to None by default

        try:
            # Get the path to the SVG file
            dot_path = get_image_path("same_opp_dot.svg")

            # Check if the renderer is already in the cache
            self.renderer = _DOT_RENDERER_CACHE.get(dot_path)

            # If not in cache, try to create a new renderer
            if not self.renderer:
                try:
                    # Check if the file exists
                    import os

                    if not os.path.exists(dot_path):
                        print(f"Warning: Dot SVG file not found at {dot_path}")
                        return

                    # Create a new renderer
                    new_renderer = QSvgRenderer(dot_path)
                    if new_renderer.isValid():
                        _DOT_RENDERER_CACHE[dot_path] = new_renderer
                        self.renderer = new_renderer
                    else:
                        print(
                            f"Warning: Could not create valid renderer for {dot_path}"
                        )
                except Exception as e:
                    print(f"Error creating SVG renderer for dot: {e}")
                    return

            # Set the shared renderer if it exists and is valid
            if self.renderer is not None and self.renderer.isValid():
                self.setSharedRenderer(self.renderer)
            else:
                print("Warning: No valid renderer available for dot")

        except Exception as e:
            print(f"Error initializing Dot: {e}")
            # Ensure renderer is None if initialization fails
            self.renderer = None
