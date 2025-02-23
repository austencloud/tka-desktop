# settings_dialog_styler.py
from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from .dark_theme_styler import DarkThemeStyler
from .base_dialog_styler import BaseDialogStyler

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog

class SettingsDialogStyler(BaseDialogStyler):
    @staticmethod
    def apply_styles(dialog: "SettingsDialog"):
        """
        Applies both the common base styling (dark theme, buttons, combos)
        and the extra logic for the SettingsDialog's .ui.sidebar, .ui.content_area, etc.
        """
        # 1) apply the shared style
        BaseDialogStyler.apply_styles(dialog)

        # 2) now do the special code for SettingsDialog:
        # e.g. set bigger font on the sidebar, etc.
        font = QFont()
        font.setPointSize(14)
        dialog.ui.sidebar.setFont(font)

        # maybe style the content area
        dialog.ui.content_area.setStyleSheet("""
            QStackedWidget {
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # style the sidebar
        dialog.ui.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2E2E2E;
                border-radius: 5px;
                font-size: 14px;
            }
            ...
        """)

        # Then loop over .ui.tab_selection_manager.tabs
        for tab in dialog.ui.tab_selection_manager.tabs.values():
            DarkThemeStyler.style_tab_widget(tab)

        # That's it! The rest is already done by the base.
