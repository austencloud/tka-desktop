from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
)
from PyQt6.QtGui import QFont

from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame
from main_window.main_widget.settings_dialog.styles.dark_theme_styler import (
    DarkThemeStyler,
)
from main_window.main_widget.settings_dialog.ui.settings_dialog_action_buttons import (
    SettingsDialogActionButtons,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogStyler:
    @staticmethod
    def apply_styles(dialog: "SettingsDialog"):
        """Applies consistent styles to the SettingsDialog."""
        font = QFont()
        font.setPointSize(14)
        dialog.ui.sidebar.setFont(font)

        dialog.ui.content_area.setStyleSheet(
            """
            QStackedWidget {
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )

        dialog.ui.sidebar.setStyleSheet(
            """
            QListWidget {
                background-color: #2E2E2E;
                border-radius: 5px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #505050;
            }
            QListWidget::item:selected {
                background-color: #6A6A6A;
                font-weight: bold;
            }
        """
        )

        # Apply styling once instead of looping unnecessarily
        DarkThemeStyler.apply_dark_mode(dialog)

        for tab in dialog.ui.tab_selection_manager.tabs.values():
            DarkThemeStyler.style_tab_widget(tab)

        elements = {
            QPushButton: DarkThemeStyler.style_button,
            QLabel: DarkThemeStyler.style_label,
            QComboBox: DarkThemeStyler.style_combo_box,
            QSpinBox: DarkThemeStyler.style_spinbox,
            CardFrame: DarkThemeStyler.style_frame,
            SettingsDialogActionButtons: DarkThemeStyler.style_frame,
        }

        for widget_type, style_function in elements.items():
            for widget in dialog.findChildren(widget_type):
                style_function(widget)
