from PyQt6.QtGui import QPalette, QColor, QCursor
from PyQt6.QtWidgets import QWidget, QTabWidget, QPushButton, QFrame, QLabel, QComboBox, QSpinBox
from PyQt6.QtCore import Qt


class DarkThemeStyler:
    """A centralized dark mode styler for the settings dialog."""

    # Dark Theme Colors
    DARK_BG = "#121212"
    LIGHT_BG = "#1E1E1E"
    ACCENT_COLOR = "#BB86FC"
    TEXT_COLOR = "#E0E0E0"
    BORDER_COLOR = "#333333"
    BUTTON_HOVER = "#3700B3"

    # Gradient Styles from NavButton
    ACTIVE_BG_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 #1e3c72,
            stop:0.3 #6c9ce9,
            stop:0.6 #4a77d4,
            stop:1 #2a52be
        );
    """
    HOVER_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(200, 200, 200, 1),
            stop:0.5 rgba(175, 175, 175, 1),
            stop:1 rgba(150, 150, 150, 1)
        );
    """
    DARK_HOVER_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 #333333,
            stop:0.5 #555555,
            stop:1 #333333
        );
    """
    DEFAULT_BG_GRADIENT = """
        background: qlineargradient(
            spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 #222222,
            stop:0.5 #333333,
            stop:1 #222222
        );
    """

    @staticmethod
    def apply_dark_mode(widget: QWidget):
        """Apply dark mode styles to a generic QWidget."""
        widget.setStyleSheet(
            f"background-color: {DarkThemeStyler.DARK_BG}; color: {DarkThemeStyler.TEXT_COLOR};"
        )

    @staticmethod
    def style_tab_widget(tab_widget: QTabWidget):
        """Apply dark mode styles to a QTabWidget."""
        palette = tab_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(DarkThemeStyler.LIGHT_BG))
        tab_widget.setPalette(palette)

        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                background: {DarkThemeStyler.LIGHT_BG};
                border: 1px solid {DarkThemeStyler.BORDER_COLOR};
            }}
            QTabBar::tab {{
                {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                color: {DarkThemeStyler.TEXT_COLOR};
                padding: 10px;
            }}
            QTabBar::tab:selected {{
                background: {DarkThemeStyler.ACCENT_COLOR};
                color: black;
            }}
            QTabBar::tab:hover {{
                background: {DarkThemeStyler.BUTTON_HOVER};
            }}
        """)

    @staticmethod
    def style_button(button: QPushButton):
        """Apply dark mode styles to a QPushButton with hover and pressed animations."""
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setStyleSheet(f"""
            QPushButton {{
                {DarkThemeStyler.DEFAULT_BG_GRADIENT}
                border: 2px solid {DarkThemeStyler.BORDER_COLOR};
                color: {DarkThemeStyler.TEXT_COLOR};
                padding: 8px 12px;
                font-weight: bold;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                {DarkThemeStyler.HOVER_GRADIENT}
            }}
            QPushButton:pressed {{
                background-color: {DarkThemeStyler.BORDER_COLOR};
            }}
        """)

    @staticmethod
    def style_frame(frame: QFrame):
        """Apply dark mode styles to a QFrame."""
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DarkThemeStyler.LIGHT_BG};
                border: 1px solid {DarkThemeStyler.BORDER_COLOR};
            }}
        """)

    @staticmethod
    def style_label(label: QLabel):
        """Apply dark mode styles to a QLabel."""
        label.setStyleSheet(f"color: {DarkThemeStyler.TEXT_COLOR}; font-weight: bold;")

    @staticmethod
    def style_combo_box(combo_box: QComboBox):
        """Apply dark mode styles to a QComboBox."""
        combo_box.setStyleSheet(f"""
            QComboBox {{
                background-color: {DarkThemeStyler.LIGHT_BG};
                color: {DarkThemeStyler.TEXT_COLOR};
                border: 1px solid {DarkThemeStyler.BORDER_COLOR};
                padding: 5px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {DarkThemeStyler.DARK_BG};
                color: {DarkThemeStyler.TEXT_COLOR};
                selection-background-color: {DarkThemeStyler.ACCENT_COLOR};
            }}
        """)

    @staticmethod
    def style_spinbox(spinbox: QSpinBox):
        """Apply dark mode styles to a QSpinBox."""
        spinbox.setStyleSheet(f"""
            QSpinBox {{
                background-color: {DarkThemeStyler.LIGHT_BG};
                color: {DarkThemeStyler.TEXT_COLOR};
                border: 1px solid {DarkThemeStyler.BORDER_COLOR};
                padding: 5px;
            }}
        """)

