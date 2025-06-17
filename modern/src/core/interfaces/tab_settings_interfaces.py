from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum


class PropType(Enum):
    STAFF = "Staff"
    CLUB = "Club"
    FAN = "Fan"
    BUUGENG = "Buugeng"
    SWORD = "Sword"
    GUITAR = "Guitar"
    UKULELE = "Ukulele"


class IUserProfileService(ABC):
    @abstractmethod
    def get_current_user(self) -> str:
        pass

    @abstractmethod
    def set_current_user(self, user: str) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> List[str]:
        pass


class IPropTypeService(ABC):
    @abstractmethod
    def get_current_prop_type(self) -> PropType:
        pass

    @abstractmethod
    def set_prop_type(self, prop_type: PropType) -> None:
        pass

    @abstractmethod
    def get_available_prop_types(self) -> List[PropType]:
        pass


class IVisibilityService(ABC):
    @abstractmethod
    def get_glyph_visibility(self, glyph_name: str) -> bool:
        pass

    @abstractmethod
    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        pass

    @abstractmethod
    def get_motion_visibility(self, color: str) -> bool:
        pass

    @abstractmethod
    def set_motion_visibility(self, color: str, visible: bool) -> None:
        pass


class IBeatLayoutService(ABC):
    @abstractmethod
    def get_layout_for_length(self, length: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_layout_for_length(self, length: int, rows: int, cols: int) -> None:
        pass


class IImageExportService(ABC):
    @abstractmethod
    def get_export_option(self, option: str) -> Any:
        pass

    @abstractmethod
    def set_export_option(self, option: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_all_export_options(self) -> Dict[str, Any]:
        pass
