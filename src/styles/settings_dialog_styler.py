from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt
from .dark_theme_styler import DarkThemeStyler
from .base_dialog_styler import BaseDialogStyler

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class SettingsDialogStyler(BaseDialogStyler):
    @staticmethod
    def apply_styles(dialog: "SettingsDialog"):
        """
        Applies both the common base styling (dark theme, buttons, combos)
        and modern styling for the Settings Dialog components.
        """
        # 1) Apply the shared base styling
        BaseDialogStyler.apply_styles(dialog)

        # 2) Now apply modernized styling for the Settings Dialog

        # Set modern font for sidebar
        font = QFont()
        # Scale font size based on dialog width
        font_size = max(10, int(dialog.width() * 0.015))
        font.setPointSize(font_size)
        font.setWeight(QFont.Weight.Medium)  # Slightly bolder
        dialog.ui.sidebar.setFont(font)

        # Set sidebar width proportional to dialog width
        sidebar_width = int(dialog.width() * 0.2)  # 20% of dialog width
        dialog.ui.sidebar.setFixedWidth(sidebar_width)

        # Style the sidebar with modern look and hover effects
        dialog.ui.sidebar.setStyleSheet(
            f"""
            QListWidget {{
                background-color: #252526;
                border-radius: 8px;
                border: none;
                padding: 10px 5px;
                margin-right: 10px;
            }}
            
            QListWidget::item {{
                color: #cccccc;
                height: {max(30, int(dialog.height() * 0.07))}px;
                padding-left: {max(10, int(dialog.width() * 0.02))}px;
                border-radius: 6px;
                margin-bottom: 5px;
            }}
            
            QListWidget::item:hover {{
                background-color: #37373d;
                color: #ffffff;
                border-left: 3px solid rgba(86, 156, 214, 0.5);
                padding-left: {max(7, int(dialog.width() * 0.02) - 3)}px;
            }}
            
            QListWidget::item:selected {{
                background-color: #37373d;
                color: #ffffff;
                border-left: 4px solid #569cd6;
                padding-left: {max(6, int(dialog.width() * 0.02) - 4)}px;
                font-weight: bold;
            }}
            
            QListWidget::item:focus {{
                outline: none;
            }}
        """
        )

        # Style the content area
        dialog.ui.content_area.setStyleSheet(
            f"""
            QStackedWidget {{
                background-color: #1e1e1e;
                border-radius: {max(6, int(dialog.width() * 0.01))}px;
                padding: {max(10, int(dialog.width() * 0.015))}px;
            }}
        """
        )

        # Style the action buttons for a more modern look
        dialog.ui.action_buttons.setStyleSheet(
            f"""
            QWidget {{
                background-color: #252526;
                border-radius: 8px;
                padding: {max(5, int(dialog.width() * 0.01))}px;
                margin-top: {max(5, int(dialog.width() * 0.01))}px;
            }}
            
            QPushButton {{
                background-color: #2d2d30;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: {max(5, int(dialog.width() * 0.01))}px {max(10, int(dialog.width() * 0.02))}px;
                font-size: {max(10, int(dialog.width() * 0.014))}px;
                min-width: {max(80, int(dialog.width() * 0.1))}px;
            }}
            
            QPushButton:hover {{
                background-color: #3e3e42;
            }}
            
            QPushButton:pressed {{
                background-color: #0e639c;
            }}
            
            QPushButton#confirmButton {{
                background-color: #0e639c;
            }}
            
            QPushButton#confirmButton:hover {{
                background-color: #1177bb;
            }}
            
            QPushButton#confirmButton:pressed {{
                background-color: #0d5689;
            }}
            
            QPushButton#cancelButton {{
                background-color: #3a3a3a;
            }}
        """
        )

        # Apply consistent styling to tab content
        for tab in dialog.ui.tab_selection_manager.tabs.values():
            # Style tab content
            tab.setStyleSheet(
                f"""
                QWidget {{
                    background-color: transparent;
                }}
                
                QLabel {{
                    color: #e0e0e0;
                    font-size: {max(10, int(dialog.width() * 0.014))}px;
                }}
                
                QGroupBox {{
                    font-size: {max(12, int(dialog.width() * 0.016))}px;
                    font-weight: bold;
                    color: #e0e0e0;
                    border: 1px solid #3a3a3a;
                    border-radius: {max(6, int(dialog.width() * 0.01))}px;
                    margin-top: {max(10, int(dialog.width() * 0.015))}px;
                    padding-top: {max(10, int(dialog.width() * 0.015))}px;
                }}
                
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 10px;
                    left: 15px;
                }}
            """
            )

            # Let the dark theme styler handle specific controls
            DarkThemeStyler.style_tab_widget(tab)
