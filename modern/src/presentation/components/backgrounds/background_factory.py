from typing import Dict, Type
from .base_background import BaseBackground
from .aurora_background import AuroraBackground
from .aurora_borealis_background import AuroraBorealisBackground
from .bubbles_background import BubblesBackground
from .snowfall_background import SnowfallBackground
from .starfield_background import StarfieldBackground


class BackgroundFactory:
    _backgrounds: Dict[str, Type[BaseBackground]] = {
        "Aurora": AuroraBackground,
        "AuroraBorealis": AuroraBorealisBackground,
        "Bubbles": BubblesBackground,
        "Snowfall": SnowfallBackground,
        "Starfield": StarfieldBackground,
    }

    @classmethod
    def create_background(cls, background_type: str, parent=None) -> BaseBackground:
        if background_type not in cls._backgrounds:
            raise ValueError(f"Unknown background type: {background_type}")
        return cls._backgrounds[background_type](parent)

    @classmethod
    def get_available_backgrounds(cls) -> list[str]:
        return list(cls._backgrounds.keys())
