from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ISettingsService(ABC):
    @abstractmethod
    def get_setting(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set_setting(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_all_settings(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def save_settings(self) -> None:
        pass


class ISettingsDialogService(ABC):
    @abstractmethod
    def show_settings_dialog(self) -> None:
        pass

    @abstractmethod
    def close_settings_dialog(self) -> None:
        pass
