from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class PictographRepository(ABC):
    @abstractmethod
    def get_pictograph_data(self, pictograph_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_pictograph_data(self, pictograph_id: str, data: Dict[str, Any]) -> bool:
        pass


class BeatFrameLayoutRepository(ABC):
    @abstractmethod
    def get_layout(self, layout_type: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_all_layouts(self) -> Dict[str, Dict[str, Any]]:
        pass


class ArrowPlacementRepository(ABC):
    @abstractmethod
    def get_placement_data(self, pictograph_type: str) -> Dict[str, Any]:
        pass


class ConfigurationRepository(ABC):
    @abstractmethod
    def get_default_settings(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_setting(self, key: str, value: Any) -> bool:
        pass
