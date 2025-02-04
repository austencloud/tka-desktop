from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

if TYPE_CHECKING:
    from .splash_screen import SplashScreen


class SplashFontColorUpdater:
    def __init__(self, splash_screen: "SplashScreen"):
        self.splash = splash_screen

    def update_splash_font_colors(self, bg_type):
        self.bg_type = bg_type
        self.font_color = self.get_font_color()

        splash_screen_labels = [
            self.splash.title_label,
            self.splash.currently_loading_label,
            self.splash.created_by_label,
            self.splash.progress_bar.percentage_label,
            self.splash.progress_bar.loading_label,
        ]
        self._apply_font_colors(splash_screen_labels)

    def get_font_color(self) -> str:
        """Return the appropriate font color based on the background type."""
        return (
            "black"
            if self.bg_type in ["Rainbow", "AuroraBorealis", "Aurora"]
            else "white"
        )

    def _apply_font_color(self, widget: QWidget) -> None:
        existing_style = widget.styleSheet()
        new_style = f"{existing_style} color: {self.font_color};"
        widget.setStyleSheet(new_style)

    def _apply_font_colors(self, widgets: list[QWidget]) -> None:
        for w in widgets:
            self._apply_font_color(w)
