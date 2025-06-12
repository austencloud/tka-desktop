from PyQt6.QtWidgets import QTabWidget
from .searchable_app_grid import SearchableAppGrid


class CategoryTabs(QTabWidget):
    def __init__(self, apps_by_category, parent=None):
        super().__init__(parent)
        self.apps_by_category = apps_by_category
        self.setup_tabs()

    def setup_tabs(self):
        category_icons = {
            "MAIN": "🚀",
            "UTILITIES": "🔧",
            "DEVELOPMENT": "👨‍💻",
            "TESTING": "🧪",
        }

        for category_name, apps in self.apps_by_category.items():
            if apps:
                icon = category_icons.get(category_name, "📁")
                grid = SearchableAppGrid(apps)
                self.addTab(grid, f"{icon} {category_name.title()}")
