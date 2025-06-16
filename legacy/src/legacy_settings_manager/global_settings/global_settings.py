from typing import TYPE_CHECKING
from enums.prop_type import PropType
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import DIAMOND
from .prop_type_changer import PropTypeChanger
from legacy_settings_manager.settings_logger import log_setting_get, log_setting_set

if TYPE_CHECKING:
    from ..legacy_settings_manager import LegacySettingsManager


class GlobalSettings:
    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        self.settings = settings_manager.settings
        self.settings_manager = settings_manager
        self.prop_type_changer = PropTypeChanger(self.settings_manager)
        self._background_type = self.settings.value(
            "global/background_type", "Snowfall"
        )
        self._font_color = self._compute_font_color(self._background_type)

    def _compute_font_color(self, bg_type: str) -> str:
        return (
            "black" if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"] else "white"
        )

    # GETTERS
    def get_current_settings_dialog_tab(self) -> str:
        """Retrieve the last opened tab from settings."""
        value = self.settings.value(
            "global/current_settings_dialog_tab", "User Profile", type=str
        )
        log_setting_get("global/current_settings_dialog_tab", value)
        return value

    def set_current_settings_dialog_tab(self, tab: str) -> None:
        """Store the currently active tab."""
        log_setting_set("global/current_settings_dialog_tab", tab)
        self.settings.setValue("global/current_settings_dialog_tab", str(tab))

    def get_grow_sequence(self) -> bool:
        value = self.settings.value("global/grow_sequence", True, type=bool)
        log_setting_get("global/grow_sequence", value)
        return value

    def get_prop_type(self) -> PropType:
        prop_type_key: str = self.settings.value("global/prop_type", "Staff")
        prop_type_key = prop_type_key.capitalize()
        return PropType[prop_type_key]

    def get_background_type(self) -> str:
        return self.settings.value("global/background_type", "Snowfall")

    def get_current_tab(self) -> str:
        return self.settings.value("global/current_tab", "construct", type=str)

    def get_grid_mode(self) -> str:
        return self.settings.value("global/grid_mode", DIAMOND)

    def get_show_welcome_screen(self) -> bool:
        return self.settings.value("global/show_welcome_screen", True, type=bool)

    def get_enable_fades(self) -> bool:
        return self.settings.value("global/enable_fades", True, type=bool)

    def get_current_font_color(self) -> str:
        return self._font_color

    # SETTERS

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        log_setting_set("global/grow_sequence", grow_sequence)
        self.settings.setValue("global/grow_sequence", grow_sequence)

    def set_prop_type(
        self, prop_type: PropType, pictographs: list["LegacyPictograph"]
    ) -> None:
        self.settings.setValue("global/prop_type", prop_type.name)
        self.prop_type_changer.apply_prop_type(pictographs)

    def set_background_type(self, background_type: str) -> None:
        if background_type != self._background_type:
            self.settings.setValue("global/background_type", background_type)
            self._background_type = background_type
            self._font_color = self._compute_font_color(background_type)
            self.settings_manager.background_changed.emit(background_type)

    def set_current_tab(self, tab: str) -> None:
        """Store the current tab as a plain string to avoid @Variant(PyQt_PyObject)."""
        self.settings.setValue("global/current_tab", str(tab))

    def set_grid_mode(self, grid_mode: str) -> None:
        self.settings.setValue("global/grid_mode", grid_mode)

    def set_show_welcome_screen(self, show_welcome_screen: bool) -> None:
        self.settings.setValue("global/show_welcome_screen", show_welcome_screen)

    def set_enable_fades(self, enable: bool) -> None:
        self.settings.setValue("global/enable_fades", enable)
