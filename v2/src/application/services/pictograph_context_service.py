"""
Pictograph Context Service - Focused Context Configuration Operations

Handles all pictograph context and configuration operations including:
- Context-specific pictograph configuration
- Glyph generation and management
- Context-aware display settings
- Pictograph rendering configuration

This service provides a clean, focused interface for pictograph context operations
while maintaining the proven configuration algorithms.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum

from domain.models.pictograph_models import PictographData


class PictographContext(Enum):
    """Different contexts where pictographs are displayed."""

    SEQUENCE_EDITOR = "sequence_editor"
    DICTIONARY_BROWSER = "dictionary_browser"
    BEAT_FRAME = "beat_frame"
    THUMBNAIL = "thumbnail"
    FULL_VIEW = "full_view"
    EXPORT = "export"


class IPictographContextService(ABC):
    """Interface for pictograph context operations."""

    @abstractmethod
    def configure_for_context(
        self, pictograph: PictographData, context: PictographContext
    ) -> Dict[str, Any]:
        """Configure pictograph for specific context."""
        pass

    @abstractmethod
    def get_glyph_for_pictograph(self, pictograph: PictographData) -> str:
        """Generate glyph representation for pictograph."""
        pass

    @abstractmethod
    def get_display_settings(self, context: PictographContext) -> Dict[str, Any]:
        """Get display settings for context."""
        pass


class PictographContextService(IPictographContextService):
    """
    Focused pictograph context service.

    Provides comprehensive pictograph context management including:
    - Context-specific pictograph configuration
    - Glyph generation and management
    - Context-aware display settings
    - Pictograph rendering configuration
    """

    def __init__(self):
        # Context configurations
        self._context_configs = self._load_context_configs()
        self._glyph_cache: Dict[str, str] = {}

    def configure_for_context(
        self, pictograph: PictographData, context: PictographContext
    ) -> Dict[str, Any]:
        """Configure pictograph for specific context."""
        config = self._context_configs.get(context, {})

        # Base configuration
        pictograph_config = {
            "pictograph": pictograph,
            "context": context,
            "show_grid": config.get("show_grid", True),
            "show_arrows": config.get("show_arrows", True),
            "show_props": config.get("show_props", True),
            "scale_factor": config.get("scale_factor", 1.0),
            "background_color": config.get("background_color", "white"),
        }

        # Context-specific adjustments
        if context == PictographContext.THUMBNAIL:
            pictograph_config.update(
                {
                    "show_grid": False,
                    "scale_factor": 0.3,
                    "simplified_arrows": True,
                }
            )
        elif context == PictographContext.SEQUENCE_EDITOR:
            pictograph_config.update(
                {
                    "show_grid": True,
                    "scale_factor": 0.8,
                    "interactive": True,
                }
            )
        elif context == PictographContext.FULL_VIEW:
            pictograph_config.update(
                {
                    "show_grid": True,
                    "scale_factor": 1.2,
                    "high_quality": True,
                }
            )
        elif context == PictographContext.EXPORT:
            pictograph_config.update(
                {
                    "show_grid": False,
                    "scale_factor": 2.0,
                    "high_quality": True,
                    "transparent_background": True,
                }
            )

        return pictograph_config

    def get_glyph_for_pictograph(self, pictograph: PictographData) -> str:
        """Generate glyph representation for pictograph."""
        # Generate cache key
        glyph_key = self._generate_glyph_key(pictograph)

        # Check cache first
        if glyph_key in self._glyph_cache:
            return self._glyph_cache[glyph_key]

        # Generate glyph
        glyph = self._generate_glyph(pictograph)

        # Cache the result
        self._glyph_cache[glyph_key] = glyph

        return glyph

    def get_display_settings(self, context: PictographContext) -> Dict[str, Any]:
        """Get display settings for context."""
        return self._context_configs.get(context, {})

    def update_context_config(
        self, context: PictographContext, config: Dict[str, Any]
    ) -> None:
        """Update configuration for a context."""
        if context not in self._context_configs:
            self._context_configs[context] = {}

        self._context_configs[context].update(config)

    def get_rendering_hints(
        self, pictograph: PictographData, context: PictographContext
    ) -> Dict[str, Any]:
        """Get rendering hints for pictograph in context."""
        hints = {
            "anti_aliasing": True,
            "smooth_scaling": True,
            "cache_enabled": True,
        }

        # Context-specific hints
        if context == PictographContext.THUMBNAIL:
            hints.update(
                {
                    "fast_rendering": True,
                    "reduced_quality": True,
                    "cache_enabled": True,
                }
            )
        elif context == PictographContext.EXPORT:
            hints.update(
                {
                    "high_quality": True,
                    "vector_output": True,
                    "cache_enabled": False,
                }
            )

        return hints

    def clear_glyph_cache(self) -> None:
        """Clear the glyph cache."""
        self._glyph_cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get glyph cache statistics."""
        return {
            "cache_size": len(self._glyph_cache),
            "cached_glyphs": list(self._glyph_cache.keys()),
        }

    # Private helper methods

    def _generate_glyph_key(self, pictograph: PictographData) -> str:
        """Generate a unique key for pictograph glyph caching."""
        # Create key based on pictograph content
        key_parts = []

        # Add arrow information
        for color, arrow in pictograph.arrows.items():
            if arrow.motion_data:
                motion = arrow.motion_data
                key_parts.append(
                    f"{color}:{motion.motion_type.value}:{motion.start_loc.value}:{motion.end_loc.value}"
                )

        # Add grid information
        grid = pictograph.grid_data
        key_parts.append(f"grid:{grid.grid_mode.value}")

        # Add metadata
        letter = pictograph.metadata.get("letter", "")
        if letter:
            key_parts.append(f"letter:{letter}")

        return "|".join(key_parts)

    def _generate_glyph(self, pictograph: PictographData) -> str:
        """Generate glyph representation for pictograph."""
        if pictograph.is_blank:
            return "○"  # Empty circle for blank pictographs

        # Get letter from metadata
        letter = pictograph.metadata.get("letter", "")
        if letter:
            return letter.upper()

        # Generate based on arrows
        arrow_count = len(pictograph.arrows)
        if arrow_count == 0:
            return "○"
        elif arrow_count == 1:
            return "◐"  # Half-filled circle
        elif arrow_count == 2:
            return "●"  # Filled circle
        else:
            return "◆"  # Diamond for complex pictographs

    def _load_context_configs(self) -> Dict[PictographContext, Dict[str, Any]]:
        """Load context-specific configurations."""
        return {
            PictographContext.SEQUENCE_EDITOR: {
                "show_grid": True,
                "show_arrows": True,
                "show_props": True,
                "scale_factor": 0.8,
                "background_color": "white",
                "interactive": True,
            },
            PictographContext.DICTIONARY_BROWSER: {
                "show_grid": False,
                "show_arrows": True,
                "show_props": True,
                "scale_factor": 0.6,
                "background_color": "transparent",
                "interactive": False,
            },
            PictographContext.BEAT_FRAME: {
                "show_grid": True,
                "show_arrows": True,
                "show_props": True,
                "scale_factor": 1.0,
                "background_color": "white",
                "interactive": True,
            },
            PictographContext.THUMBNAIL: {
                "show_grid": False,
                "show_arrows": True,
                "show_props": False,
                "scale_factor": 0.3,
                "background_color": "transparent",
                "interactive": False,
                "simplified_arrows": True,
            },
            PictographContext.FULL_VIEW: {
                "show_grid": True,
                "show_arrows": True,
                "show_props": True,
                "scale_factor": 1.2,
                "background_color": "white",
                "interactive": True,
                "high_quality": True,
            },
            PictographContext.EXPORT: {
                "show_grid": False,
                "show_arrows": True,
                "show_props": True,
                "scale_factor": 2.0,
                "background_color": "transparent",
                "interactive": False,
                "high_quality": True,
                "vector_output": True,
            },
        }
