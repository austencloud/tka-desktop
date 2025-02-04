from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from splash_screen.splash_screen import SplashScreen


class SplashGeometryManager:
    def __init__(self, splash_screen: "SplashScreen"):
        self.splash_screen = splash_screen
        self.target_screen = splash_screen.target_screen
        self.center_on_screen()

    def center_on_screen(self):
        screen_geometry = self.target_screen.geometry()
        self.splash_screen.setGeometry(
            screen_geometry.x()
            + (screen_geometry.width() - self.splash_screen.width()) // 2,
            screen_geometry.y()
            + (screen_geometry.height() - self.splash_screen.height()) // 2,
            self.splash_screen.width(),
            self.splash_screen.height(),
        )
