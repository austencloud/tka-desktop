from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QWidget,
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
    QFrame,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QEvent

from main_window.main_widget.settings_dialog.beat_layout_tab.beat_layout_tab import (
    BeatLayoutTab,
)
from main_window.main_widget.settings_dialog.prop_type_tab.prop_type_tab import (
    PropTypeTab,
)
from main_window.main_widget.settings_dialog.styles.card_frame import CardFrame
from main_window.main_widget.settings_dialog.styles.dark_theme_styler import (
    DarkThemeStyler,
)
from main_window.main_widget.settings_dialog.user_profile_tab.user_profile_tab import (
    UserProfileTab,
)
from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
    VisibilityTab,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SettingsDialog(QDialog):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setWindowTitle("Settings")

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        self.setLayout(main_layout)

        self.sidebar = QListWidget(self)
        self.sidebar.setFixedWidth(220)
        self.sidebar.setSpacing(10)
        self.sidebar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.content_area = QStackedWidget(self)

        self.user_profile_tab = UserProfileTab(self)
        self.prop_type_tab = PropTypeTab(self)
        self.visibility_tab = VisibilityTab(self)
        self.beat_layout_tab = BeatLayoutTab(self)

        self._add_sidebar_item("User Profile", self.user_profile_tab)
        self._add_sidebar_item("Prop Type", self.prop_type_tab)
        self._add_sidebar_item("Visibility", self.visibility_tab)
        self._add_sidebar_item("Beat Layout", self.beat_layout_tab)

        self.sidebar.setCurrentRow(0)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, stretch=1)

    def _add_sidebar_item(self, name: str, widget: QWidget):
        item = QListWidgetItem(name)
        self.sidebar.addItem(item)
        self.content_area.addWidget(widget)

        self.sidebar.currentRowChanged.connect(
            lambda index: self.content_area.setCurrentIndex(index)
        )

    def _apply_styles(self):
        font = QFont()
        font.setPointSize(14)
        self.sidebar.setFont(font)

        # self.setStyleSheet("color: white;")

        self.content_area.setStyleSheet(
            """
            QStackedWidget {
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )

        self.sidebar.setStyleSheet(
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

        """Apply dark mode styles to all relevant widgets in settings dialog."""
        DarkThemeStyler.apply_dark_mode(self)
        self.tabs = [
            self.user_profile_tab,
            self.prop_type_tab,
            self.visibility_tab,
            self.beat_layout_tab,
        ]
        for tab in self.tabs:
            DarkThemeStyler.style_tab_widget(tab)

        for button in self.findChildren(QPushButton):
            DarkThemeStyler.style_button(button)

        for label in self.findChildren(QLabel):
            DarkThemeStyler.style_label(label)

        for combo_box in self.findChildren(QComboBox):
            DarkThemeStyler.style_combo_box(combo_box)

        for spinbox in self.findChildren(QSpinBox):
            DarkThemeStyler.style_spinbox(spinbox)

        for frame in self.findChildren(CardFrame):
            DarkThemeStyler.style_frame(frame)

    def resizeEvent(self, event: QEvent):
        self.update_size()
        super().resizeEvent(event)

    def update_size(self):
        height = int(self.main_widget.height() * 0.8)
        width = int(height * 1.2)
        self.setFixedSize(width, height)
