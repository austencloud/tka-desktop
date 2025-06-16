"""
Settings for the codex exporter.
"""

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from legacy.src.legacy_settings_manager.legacy_settings_manager import LegacySettingsManager


class CodexExporterSettings:
    """Settings for the codex exporter."""

    DEFAULT_CODEX_EXPORTER_SETTINGS = {
        "last_red_turns": 1.0,
        "last_blue_turns": 0.0,
        "grid_mode": "diamond",
    }

    def __init__(self, settings_manager: "LegacySettingsManager") -> None:
        """Initialize the codex exporter settings.

        Args:
            settings_manager: The settings manager
        """
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_last_red_turns(self) -> float:
        """Get the last used red turns value.

        Returns:
            The last used red turns value
        """
        return self.settings.value(
            "codex_exporter/last_red_turns",
            self.DEFAULT_CODEX_EXPORTER_SETTINGS["last_red_turns"],
            type=float,
        )

    def set_last_red_turns(self, turns: Union[int, float]) -> None:
        """Set the last used red turns value.

        Args:
            turns: The turns value to save
        """
        self.settings.setValue("codex_exporter/last_red_turns", float(turns))
        self.settings.sync()

    def get_last_blue_turns(self) -> float:
        """Get the last used blue turns value.

        Returns:
            The last used blue turns value
        """
        return self.settings.value(
            "codex_exporter/last_blue_turns",
            self.DEFAULT_CODEX_EXPORTER_SETTINGS["last_blue_turns"],
            type=float,
        )

    def set_last_blue_turns(self, turns: Union[int, float]) -> None:
        """Set the last used blue turns value.

        Args:
            turns: The turns value to save
        """
        self.settings.setValue("codex_exporter/last_blue_turns", float(turns))
        self.settings.sync()

    def get_grid_mode(self) -> str:
        """Get the last used grid mode.

        Returns:
            The last used grid mode ('diamond' or 'box')
        """
        return self.settings.value(
            "codex_exporter/grid_mode",
            self.DEFAULT_CODEX_EXPORTER_SETTINGS["grid_mode"],
            type=str,
        )

    def set_grid_mode(self, grid_mode: str) -> None:
        """Set the grid mode.

        Args:
            grid_mode: The grid mode to save ('diamond' or 'box')
        """
        self.settings.setValue("codex_exporter/grid_mode", grid_mode)
        self.settings.sync()
