from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QScrollArea,
    QGridLayout,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from .app_card import AppCard


class SearchableAppGrid(QWidget):
    def __init__(self, apps, parent=None):
        super().__init__(parent)
        self.all_apps = apps
        self.filtered_apps = apps.copy()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        search_layout = QHBoxLayout()
        search_label = QLabel("🔍")
        search_label.setFont(QFont("Segoe UI", 12))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search applications, features, or tags..."
        )
        self.search_input.textChanged.connect(self.filter_apps)
        self.search_input.setMinimumHeight(32)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(12)

        scroll.setWidget(self.grid_widget)
        layout.addWidget(scroll)

        self.populate_grid()

    def populate_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            child = self.grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        cols = 3
        for i, app in enumerate(self.filtered_apps):
            row, col = divmod(i, cols)

            card = AppCard(app)
            card.launch_requested.connect(self.handle_app_launch)
            self.grid_layout.addWidget(card, row, col)

    def filter_apps(self, text):
        if not text:
            self.filtered_apps = self.all_apps.copy()
        else:
            text_lower = text.lower()
            self.filtered_apps = [
                app
                for app in self.all_apps
                if (
                    text_lower in app.title.lower()
                    or text_lower in app.description.lower()
                    or any(text_lower in tag.lower() for tag in app.tags)
                )
            ]
        self.populate_grid()

    def handle_app_launch(self, app):
        main_window = self.window()
        if hasattr(main_window, "launch_application"):
            main_window.launch_application(app)
