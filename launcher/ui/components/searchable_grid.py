from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QGridLayout,
)
from typing import List
from .animated_card import AnimatedCard


class SearchableGrid(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = []
        self.filtered_cards = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search applications and tools...")
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12), 
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 25px;
                padding: 12px 20px;
                color: white;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 2px solid rgba(102, 126, 234, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.15), 
                    stop:1 rgba(118, 75, 162, 0.15));
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
        """
        )
        self.search_input.textChanged.connect(self.filter_cards)

        self.view_combo = QComboBox()
        self.view_combo.addItems(["Grid View", "List View", "Compact"])
        self.view_combo.setStyleSheet(
            """
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12), 
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 10px 15px;
                color: white;
                font-weight: 600;
                font-family: 'Segoe UI';
                min-width: 120px;
            }
            QComboBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.2), 
                    stop:1 rgba(118, 75, 162, 0.2));
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0px;
                height: 0px;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid white;
            }
            QComboBox QAbstractItemView {
                background: rgba(26, 26, 46, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: white;
                selection-background-color: rgba(102, 126, 234, 0.5);
            }
        """
        )
        self.view_combo.currentTextChanged.connect(self.change_view)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.view_combo)
        layout.addLayout(search_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea { 
                border: none; 
                background: transparent; 
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 0.8), 
                    stop:1 rgba(118, 75, 162, 0.8));
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(102, 126, 234, 1.0), 
                    stop:1 rgba(118, 75, 162, 1.0));
            }
        """
        )
        self.content_widget = QWidget()
        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setSpacing(12)

        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)

        self.current_view = "Grid View"

    def add_card(self, card: AnimatedCard) -> None:
        self.cards.append(card)
        self.filtered_cards.append(card)
        self.refresh_layout()

    def filter_cards(self, text: str) -> None:
        self.filtered_cards = [
            card
            for card in self.cards
            if text.lower() in card.title_label.text().lower()
            or text.lower() in card.desc_label.text().lower()
        ]
        self.refresh_layout()

    def change_view(self, view_type: str) -> None:
        self.current_view = view_type
        self.refresh_layout()

    def refresh_layout(self) -> None:
        for i in reversed(range(self.content_layout.count())):
            item = self.content_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        cols = (
            1
            if self.current_view == "List View"
            else (4 if self.current_view == "Compact" else 3)
        )

        for i, card in enumerate(self.filtered_cards):
            if self.current_view == "Compact":
                card.setMaximumHeight(80)
                card.setMinimumHeight(80)
            else:
                card.setMaximumHeight(120)
                card.setMinimumHeight(120)
            self.content_layout.addWidget(card, i // cols, i % cols)

    def handle_resize(self, size):
        """Handle parent resize events"""
        self.refresh_layout()
