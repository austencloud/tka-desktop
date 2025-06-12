# Command Palette - Global Search and Quick Actions
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, 
    QListWidgetItem, QLabel, QFrame, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QPalette
from typing import List, Dict, Any
import re


class CommandPaletteItem:
    """Represents an item in the command palette"""
    def __init__(self, title: str, description: str, icon: str, action_type: str, 
                 data: Any = None, keywords: List[str] = None):
        self.title = title
        self.description = description
        self.icon = icon
        self.action_type = action_type  # 'app', 'command', 'recent'
        self.data = data
        self.keywords = keywords or []
        self.score = 0  # For fuzzy search ranking


class CommandPalette(QFrame):
    """
    Spotlight/VS Code style command palette with fuzzy search
    
    Features:
    - Global search across applications, commands, and recent actions
    - Fuzzy matching with intelligent scoring
    - Keyboard navigation (arrow keys, enter, escape)
    - Recent actions and suggestions
    - Accessibility-first design
    """
    
    item_selected = pyqtSignal(object)  # CommandPaletteItem
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items: List[CommandPaletteItem] = []
        self.filtered_items: List[CommandPaletteItem] = []
        self.recent_actions: List[CommandPaletteItem] = []
        self.setup_ui()
        self.setup_accessibility()
        self.setup_animations()
        
    def setup_ui(self):
        """Create the command palette interface"""
        self.setObjectName("commandPalette")
        self.setFixedSize(600, 400)
        self.setFrameStyle(QFrame.Shape.Box)
        
        # Apply glassmorphism styling
        self.setStyleSheet("""
            QFrame#commandPalette {
                background: rgba(30, 30, 30, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with search input
        header = self.create_header()
        layout.addWidget(header)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.setObjectName("resultsList")
        self.results_list.setAccessibleName("Search results")
        self.results_list.setAccessibleDescription("Use arrow keys to navigate, Enter to select")
        self.results_list.itemClicked.connect(self.on_item_clicked)
        self.results_list.setStyleSheet("""
            QListWidget#resultsList {
                background: transparent;
                border: none;
                outline: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px 16px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
            }
            QListWidget::item:selected {
                background: rgba(74, 144, 226, 0.3);
                border-left: 3px solid #4a90e2;
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.results_list)
        
        # Footer with shortcuts
        footer = self.create_footer()
        layout.addWidget(footer)
        
    def create_header(self) -> QWidget:
        """Create search input header"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px 12px 0 0;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setFont(QFont("Segoe UI", 16))
        layout.addWidget(search_icon)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search applications, commands, or type to filter...")
        self.search_input.setAccessibleName("Command palette search")
        self.search_input.setAccessibleDescription("Type to search applications and commands")
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: white;
                font-size: 16px;
                font-weight: 500;
                padding: 4px 8px;
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
        """)
        layout.addWidget(self.search_input)
        
        return header
        
    def create_footer(self) -> QWidget:
        """Create footer with keyboard shortcuts"""
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 0 0 12px 12px;
            }
        """)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(16, 8, 16, 8)
        
        shortcuts = [
            ("↑↓", "Navigate"),
            ("Enter", "Select"),
            ("Esc", "Close"),
            ("Ctrl+K", "Clear")
        ]
        
        for key, desc in shortcuts:
            shortcut_label = QLabel(f"{key} {desc}")
            shortcut_label.setStyleSheet("""
                QLabel {
                    color: rgba(255, 255, 255, 0.7);
                    font-size: 11px;
                    padding: 2px 8px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 4px;
                }
            """)
            layout.addWidget(shortcut_label)
            
        layout.addStretch()
        
        return footer
        
    def setup_accessibility(self):
        """Configure accessibility features"""
        self.setAccessibleName("Command Palette")
        self.setAccessibleDescription(
            "Global search for applications and commands. "
            "Type to search, use arrow keys to navigate, Enter to select."
        )
        
        # Keyboard shortcuts
        self.escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.escape_shortcut.activated.connect(self.hide_palette)
        
        self.enter_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.enter_shortcut.activated.connect(self.select_current_item)
        
        self.up_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        self.up_shortcut.activated.connect(self.navigate_up)
        
        self.down_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        self.down_shortcut.activated.connect(self.navigate_down)
        
    def setup_animations(self):
        """Setup smooth show/hide animations"""
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(200)
        
    def show_palette(self):
        """Show the command palette with animation"""
        if self.parent():
            # Center on parent window
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + parent_rect.height() // 4
            self.move(x, y)
        
        self.show()
        self.search_input.setFocus()
        self.search_input.clear()
        self.load_default_items()
        
        # Announce to screen readers
        self.setAccessibleDescription(
            f"Command palette opened. {len(self.items)} items available. "
            "Type to search or use arrow keys to browse."
        )
        
    def hide_palette(self):
        """Hide the command palette"""
        self.hide()
        self.closed.emit()
        
    def load_default_items(self):
        """Load default items when palette opens"""
        # This will be populated by the main window
        self.populate_results(self.items[:10])  # Show first 10 items
        
    def add_items(self, items: List[CommandPaletteItem]):
        """Add items to the palette"""
        self.items.extend(items)
        
    def on_search_changed(self, text: str):
        """Handle search input changes with fuzzy matching"""
        if not text.strip():
            self.populate_results(self.items[:10])
            return
            
        # Fuzzy search with scoring
        self.filtered_items = self.fuzzy_search(text)
        self.populate_results(self.filtered_items[:10])
        
    def fuzzy_search(self, query: str) -> List[CommandPaletteItem]:
        """Perform fuzzy search with intelligent scoring"""
        query_lower = query.lower()
        results = []
        
        for item in self.items:
            score = 0
            
            # Exact title match gets highest score
            if query_lower in item.title.lower():
                score += 100
                
            # Description match
            if query_lower in item.description.lower():
                score += 50
                
            # Keyword matches
            for keyword in item.keywords:
                if query_lower in keyword.lower():
                    score += 30
                    
            # Character-by-character fuzzy matching
            if self.fuzzy_match(query_lower, item.title.lower()):
                score += 20
                
            if score > 0:
                item.score = score
                results.append(item)
                
        return sorted(results, key=lambda x: x.score, reverse=True)
        
    def fuzzy_match(self, query: str, text: str) -> bool:
        """Simple fuzzy matching algorithm"""
        query_idx = 0
        for char in text:
            if query_idx < len(query) and char == query[query_idx]:
                query_idx += 1
        return query_idx == len(query)
        
    def populate_results(self, items: List[CommandPaletteItem]):
        """Populate the results list"""
        self.results_list.clear()
        
        for item in items:
            list_item = QListWidgetItem()
            list_item.setText(f"{item.icon} {item.title}")
            list_item.setToolTip(item.description)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.results_list.addItem(list_item)
            
        if items:
            self.results_list.setCurrentRow(0)
            
    def navigate_up(self):
        """Navigate up in results"""
        current = self.results_list.currentRow()
        if current > 0:
            self.results_list.setCurrentRow(current - 1)
            
    def navigate_down(self):
        """Navigate down in results"""
        current = self.results_list.currentRow()
        if current < self.results_list.count() - 1:
            self.results_list.setCurrentRow(current + 1)
            
    def select_current_item(self):
        """Select the currently highlighted item"""
        current_item = self.results_list.currentItem()
        if current_item:
            self.on_item_clicked(current_item)
            
    def on_item_clicked(self, list_item: QListWidgetItem):
        """Handle item selection"""
        palette_item = list_item.data(Qt.ItemDataRole.UserRole)
        if palette_item:
            self.item_selected.emit(palette_item)
            self.hide_palette()
