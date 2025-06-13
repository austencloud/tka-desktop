# Responsive App Grid - Adaptive Layout with Performance Optimization
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QResizeEvent
from typing import List, Dict, Any

from .app_card import AppCard
from ...data.app_definitions import AppType


class ResponsiveAppGrid(QScrollArea):
    """
    Responsive application grid that adapts to window size

    Features:
    - Automatic column calculation based on width
    - Smooth responsive transitions
    - Virtual scrolling for performance
    - Keyboard navigation support
    - Accessibility-optimized layout
    - Grid/list view toggle
    """

    app_launched = pyqtSignal(object)
    view_changed = pyqtSignal(str)  # 'grid' or 'list'

    def __init__(self, apps: List[Any] | None = None, parent=None):
        super().__init__(parent)
        self.apps = apps if apps is not None else []
        self.filtered_apps = self.apps.copy()
        self.min_card_width = 380  # Increase from 280
        self.max_card_width = 600  # Add maximum to prevent overstretching
        self.card_height_normal = 140  # Increase from 60 for compact mode
        self.card_height_expanded = 200  # For main applications

        # Initialize UI components that will be created
        self.container: QFrame
        self.main_layout: QVBoxLayout
        self.search_bar: QWidget
        self.hero_section: QWidget
        self.grid_frame: QFrame
        self.categories_layout: QVBoxLayout
        self.search_input: Any
        self.count_label: QLabel

        self.setup_ui()
        self.setup_accessibility()

    def setup_ui(self):
        """Initialize the streamlined responsive grid interface"""
        self.setObjectName("responsiveGrid")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.container = QFrame()
        self.container.setObjectName("gridContainer")
        self.setWidget(self.container)

        self.main_layout = QVBoxLayout(self.container)
        self.main_layout.setSpacing(16)  # Reduced from 32
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Reduced from 40

        # Compact search bar only
        self.search_bar = self.create_compact_search_bar()
        self.main_layout.addWidget(self.search_bar)

        # Direct app grid without hero section
        self.grid_frame = QFrame()
        self.grid_layout = QVBoxLayout(self.grid_frame)
        self.grid_layout.setSpacing(12)  # Reduced from 28
        self.main_layout.addWidget(self.grid_frame)

        self.main_layout.addStretch()

        self.setStyleSheet(
            """
            QScrollArea#responsiveGrid {
                background: transparent;
                border: none;
            }
            QFrame#gridContainer {
                background: transparent;
            }
        """
        )

        self.populate_grid()

    def create_compact_search_bar(self) -> QWidget:
        """Create compact search bar for filtering applications"""
        from PyQt6.QtWidgets import QLineEdit

        search_container = QFrame()
        search_container.setFixedHeight(40)  # Reduced from 60
        search_container.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
            }
        """
        )

        layout = QHBoxLayout(search_container)
        layout.setContentsMargins(12, 8, 12, 8)  # Reduced margins
        layout.setSpacing(8)  # Reduced spacing

        # Compact search icon
        search_icon = QLabel("🔍")
        search_icon.setFont(QFont("Segoe UI", 12))  # Smaller icon
        search_icon.setStyleSheet(
            "color: rgba(255, 255, 255, 0.7); background: transparent;"
        )
        layout.addWidget(search_icon)

        # Compact search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search applications...")
        self.search_input.setFont(QFont("Segoe UI", 11))  # Smaller font
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 11px;
                padding: 4px 0;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
        """
        )
        self.search_input.textChanged.connect(self.perform_search)
        layout.addWidget(self.search_input, 1)

        # App count display
        self.count_label = QLabel()
        self.count_label.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 10px;
                font-weight: 500;
                background: transparent;
                padding: 2px 8px;
            }
        """
        )
        self.update_count_label()
        layout.addWidget(self.count_label)

        return search_container

    def setup_accessibility(self):
        """Configure accessibility features"""
        self.setAccessibleName("Application Grid")
        self.setAccessibleDescription(
            f"Grid of {len(self.apps)} applications. "
            "Use Tab to navigate between applications, Enter to launch."
        )

    def set_view_mode(self, mode: str):
        """View mode is fixed as list"""
        pass

    def populate_grid(self):
        # Clear existing items
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        if not self.filtered_apps:
            empty_state = self.create_empty_state()
            self.grid_layout.addWidget(empty_state)
            return

        # Separate apps by type
        main_apps = [
            app
            for app in self.filtered_apps
            if hasattr(app, "app_type") and app.app_type == AppType.MAIN_APPLICATION
        ]
        standalone_tools = [
            app
            for app in self.filtered_apps
            if hasattr(app, "app_type") and app.app_type == AppType.STANDALONE_TOOL
        ]
        dev_tools = [
            app
            for app in self.filtered_apps
            if hasattr(app, "app_type") and app.app_type == AppType.DEVELOPMENT_TOOL
        ]

        # Calculate responsive columns
        viewport = self.viewport()
        container_width = viewport.width() if viewport else 1200
        padding = 40
        spacing = 16
        available_width = container_width - padding

        # Dynamic column calculation
        columns = max(1, min(4, available_width // self.min_card_width))

        # Main Applications Section
        if main_apps:
            section_header = self.create_section_header(
                "🚀 Main Applications", len(main_apps)
            )
            self.grid_layout.addWidget(section_header)

            main_container = self.create_app_section(main_apps, columns, expanded=True)
            self.grid_layout.addWidget(main_container)

            # Add spacing between sections
            spacer = QFrame()
            spacer.setFixedHeight(24)
            spacer.setStyleSheet("background: transparent;")
            self.grid_layout.addWidget(spacer)

        # Standalone Tools Section
        if standalone_tools:
            section_header = self.create_section_header(
                "🔧 Standalone Tools", len(standalone_tools)
            )
            self.grid_layout.addWidget(section_header)

            tools_container = self.create_app_section(
                standalone_tools, columns, expanded=False
            )
            self.grid_layout.addWidget(tools_container)

            spacer = QFrame()
            spacer.setFixedHeight(24)
            spacer.setStyleSheet("background: transparent;")
            self.grid_layout.addWidget(spacer)

        # Development Tools Section
        if dev_tools:
            section_header = self.create_section_header(
                "🛠️ Development Tools", len(dev_tools)
            )
            self.grid_layout.addWidget(section_header)

            dev_container = self.create_app_section(dev_tools, columns, expanded=False)
            self.grid_layout.addWidget(dev_container)

        self.update_count_label()

    def create_section_header(self, title: str, count: int) -> QWidget:
        header = QFrame()
        header.setFixedHeight(40)
        header.setStyleSheet(
            """
            QFrame {
                background: transparent;
                border-bottom: 2px solid rgba(74, 144, 226, 0.3);
                margin-bottom: 8px;
            }
        """
        )

        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 8)

        title_label = QLabel(f"{title}")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(
            "color: white; background: transparent; border: none;"
        )
        layout.addWidget(title_label)

        count_label = QLabel(f"{count} apps")
        count_label.setFont(QFont("Segoe UI", 11))
        count_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.6); background: transparent; border: none;"
        )
        layout.addWidget(count_label)

        layout.addStretch()

        return header

    def create_app_section(
        self, apps: List[Any], columns: int, expanded: bool
    ) -> QWidget:
        container = QFrame()
        container.setStyleSheet("QFrame { background: transparent; }")

        layout = QGridLayout(container)
        layout.setSpacing(16)  # Increase spacing between cards
        layout.setContentsMargins(0, 0, 0, 0)

        for i, app in enumerate(apps):
            row = i // columns
            col = i % columns

            card = AppCard(app, compact=False, expanded=expanded)

            # Set dynamic sizing
            card.setMinimumWidth(self.min_card_width)
            card.setMaximumWidth(self.max_card_width)

            if expanded:
                card.setFixedHeight(self.card_height_expanded)
            else:
                card.setFixedHeight(self.card_height_normal)

            card.launch_requested.connect(self.app_launched.emit)
            card.setAccessibleName(f"Launch {app.title}")
            card.setAccessibleDescription(f"{app.description}. Press Enter to launch.")

            layout.addWidget(card, row, col)

        # Fill remaining columns with stretch
        total_apps = len(apps)
        last_row = (total_apps - 1) // columns
        last_col = (total_apps - 1) % columns

        for col in range(last_col + 1, columns):
            layout.setColumnStretch(col, 1)

        return container

    def create_empty_state(self) -> QWidget:
        empty = QFrame()
        empty.setFixedHeight(200)
        empty.setStyleSheet(
            """
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 2px dashed rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """
        )

        layout = QVBoxLayout(empty)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        icon = QLabel("🔍")
        icon.setFont(QFont("Segoe UI", 48))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("color: rgba(255, 255, 255, 0.6); background: transparent;")
        layout.addWidget(icon)

        title = QLabel("No applications found")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        layout.addWidget(title)

        subtitle = QLabel("Try adjusting your search terms")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            "color: rgba(255, 255, 255, 0.6); background: transparent;"
        )
        layout.addWidget(subtitle)

        return empty

    def perform_search(self, text: str):
        """Perform search filtering on applications"""
        if not text.strip():
            self.filtered_apps = self.apps.copy()
            app_titles = [app.title for app in self.filtered_apps]
            total = len(app_titles)
            self.count_label.setText(f"{total} apps")
            self.populate_grid()
            return

        self.filtered_apps = []

        text_lower = text.lower()

        for app in self.apps:
            # Search in title, description, and tags
            if (
                text_lower in app.title.lower()
                or text_lower in app.description.lower()
                or any(text_lower in tag.lower() for tag in getattr(app, "tags", []))
            ):
                self.filtered_apps.append(app)

        filtered = len(self.filtered_apps)
        self.populate_grid()
        self.update_count_label()

        text = f"{filtered} apps"

    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize"""
        super().resizeEvent(event)

    def get_layout_info(self) -> Dict[str, Any]:
        """Get current layout information"""
        viewport = self.viewport()
        viewport_width = viewport.width() if viewport else 0
        return {
            "view_mode": "list",
            "columns": 3,
            "total_apps": len(self.apps),
            "filtered_apps": len(self.filtered_apps),
            "viewport_width": viewport_width,
        }

    def update_count_label(self):
        """Update the application count label"""
        total = len(self.apps)
        filtered = len(self.filtered_apps)

        if filtered == total:
            text = f"{total} apps"
        else:
            text = f"{filtered} of {total} apps"

        self.count_label.setText(text)

    def filter_apps(self, apps: List[Any]):
        """Update filtered applications and refresh grid"""
        self.filtered_apps = apps
        self.populate_grid()

        count = len(apps)
        self.setAccessibleDescription(
            f"Filter applied. {count} applications shown. "
            "Use Tab to navigate, Enter to launch."
        )

    def set_apps(self, apps: List[Any]):
        """Set new application list"""
        self.apps = apps
        self.filtered_apps = apps.copy()
        self.populate_grid()
