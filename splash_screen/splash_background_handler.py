from typing import TYPE_CHECKING, Optional

from main_window.main_widget.main_background_widget.backgrounds.aurora.aurora_background import (
    AuroraBackground,
)
from main_window.main_widget.main_background_widget.backgrounds.aurora_borealis_background import (
    AuroraBorealisBackground,
)
from main_window.main_widget.main_background_widget.backgrounds.base_background import (
    BaseBackground,
)
from main_window.main_widget.main_background_widget.backgrounds.bubbles_background import (
    BubblesBackground,
)
from main_window.main_widget.main_background_widget.backgrounds.snowfall.snowfall_background import (
    SnowfallBackground,
)
from main_window.main_widget.main_background_widget.backgrounds.starfield.starfield_background import (
    StarfieldBackground,
)


if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashBackgroundHandler:
    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self.background_manager: Optional[BaseBackground] = None
        self.is_animating = False  # Flag to prevent overlapping animations

    def setup_background_manager(self):
        """Initializes the background manager based on the current background type."""
        self.bg_type = (
            self.splash_screen.settings_manager.global_settings.get_background_type()
        )
        self.background_manager = self.get_background_manager()
        self.splash_screen.background_manager = self.background_manager
        if self.background_manager:
            # Connect the update_required signal to the main widget's update method
            self.background_manager.update_required.connect(self.splash_screen.update)
            # Start the background animation
            # self.background_manager.start_animation()

    # def apply_background(self):
    #     """Applies or reapplies the background manager."""
    #     if self.background_manager:
    #         # Stop existing animation before applying a new background
    #         self.background_manager.stop_animation()
    #         self.background_manager.update_required.disconnect(
    #             self.splash_screen.update
    #         )

    #     self.setup_background_manager()

    def get_background_manager(self) -> Optional[BaseBackground]:
        """Returns an instance of the appropriate BackgroundManager based on bg_type."""

        self.splash_screen.font_color_updater.update_splash_font_colors(self.bg_type)
        background_manager_map = {
            "Starfield": StarfieldBackground,
            "Aurora": AuroraBackground,
            "AuroraBorealis": AuroraBorealisBackground,
            "Snowfall": SnowfallBackground,
            "Bubbles": BubblesBackground,
        }
        manager_class = background_manager_map.get(self.bg_type)
        return manager_class(self.splash_screen) if manager_class else None

    def stop_animation(self):
        """Stops the background animation."""
        if self.background_manager:
            self.background_manager.stop_animation()
