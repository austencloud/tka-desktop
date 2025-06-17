# Modern backgrounds package
from .background_factory import BackgroundFactory
from .aurora_background import AuroraBackground
from .bubbles_background import BubblesBackground
from .snowfall_background import SnowfallBackground
from .starfield_background import StarfieldBackground
from .background_widget import MainBackgroundWidget

__all__ = [
    "MainBackgroundWidget",
    "BackgroundFactory",
    "AuroraBackground",
    "BubblesBackground",
    "SnowfallBackground",
    "StarfieldBackground",
]
