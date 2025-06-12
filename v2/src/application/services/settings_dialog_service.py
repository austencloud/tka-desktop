from typing import Optional
from PyQt6.QtWidgets import QWidget

from src.core.interfaces.settings_interfaces import (
    ISettingsDialogService,
    ISettingsService,
)
from src.presentation.components.ui.settings.modern_settings_dialog import (
    ModernSettingsDialog,
)


class SettingsDialogService(ISettingsDialogService):
    def __init__(
        self,
        settings_service: ISettingsService,
        parent_widget: Optional[QWidget] = None,
    ):
        self.settings_service = settings_service
        self.parent_widget = parent_widget
        self._dialog: Optional[ModernSettingsDialog] = None

    def show_settings_dialog(self) -> None:
        if self._dialog is None:
            self._dialog = ModernSettingsDialog(
                self.settings_service, self.parent_widget
            )
            self._dialog.finished.connect(self._on_dialog_closed)

        # Center on parent if available
        if self.parent_widget:
            parent_rect = self.parent_widget.geometry()
            dialog_rect = self._dialog.geometry()
            x = parent_rect.center().x() - dialog_rect.width() // 2
            y = parent_rect.center().y() - dialog_rect.height() // 2
            self._dialog.move(x, y)

        self._dialog.show()
        self._dialog.raise_()
        self._dialog.activateWindow()

    def close_settings_dialog(self) -> None:
        if self._dialog:
            self._dialog.close()

    def _on_dialog_closed(self):
        self._dialog = None
