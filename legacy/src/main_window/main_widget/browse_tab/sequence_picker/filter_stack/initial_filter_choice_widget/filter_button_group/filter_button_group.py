from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt, QTimer, QSize

from main_window.main_widget.browse_tab.sequence_picker.filter_stack.initial_filter_choice_widget.filter_button_group.filter_button import (
    FilterButton,
)

if TYPE_CHECKING:
    from ..initial_filter_choice_widget import InitialFilterChoiceWidget


class FilterButtonGroup(QWidget):
    """A modern 2025 filter button group with responsive design and glass-morphism effects."""

    def __init__(
        self,
        label: str,
        description: str,
        handler: callable,
        filter_choice_widget: "InitialFilterChoiceWidget",
    ):
        super().__init__()
        self.main_widget = filter_choice_widget.main_widget
        self.settings_manager = self.main_widget.settings_manager
        self.filter_choice_widget = filter_choice_widget

        # Modern responsive sizing
        self._setup_responsive_sizing()

        self.button = FilterButton(label)
        self.button.clicked.connect(handler)

        # Enhanced responsiveness with proper timing
        QTimer.singleShot(50, self._ensure_modern_responsiveness)

        self.description_label = QLabel(description)
        self._setup_modern_layout()
        self._apply_modern_styling()

    def _setup_responsive_sizing(self):
        """Setup modern responsive sizing policies."""
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setMinimumSize(QSize(120, 80))
        self.setMaximumSize(QSize(200, 120))

    def _setup_modern_layout(self):
        """Setup modern layout with proper spacing and alignment."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button with responsive sizing
        layout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)

        # Description label with modern typography
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _apply_modern_styling(self):
        """Apply PyQt6-compatible modern styling to the button group."""
        # Modern container styling (PyQt6-compatible)
        self.setStyleSheet(
            """
            FilterButtonGroup {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin: 4px;
                padding: 8px;
            }
        """
        )

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Modern responsive resize handling with proper scaling."""
        if not self.main_widget:
            super().resizeEvent(event)
            return

        # Calculate responsive dimensions based on container size
        container_width = (
            self.filter_choice_widget.width()
            if hasattr(self.filter_choice_widget, "width")
            else 800
        )
        container_height = (
            self.filter_choice_widget.height()
            if hasattr(self.filter_choice_widget, "height")
            else 600
        )

        # Modern responsive button sizing (percentage-based)
        button_width = max(100, min(180, container_width // 6))
        button_height = max(40, min(60, container_height // 12))

        # Set button size with modern proportions
        self.button.setFixedSize(button_width, button_height)

        # Modern typography scaling
        self._update_modern_typography(container_width)

        super().resizeEvent(event)

    def _update_modern_typography(self, container_width: int):
        """Update typography with modern responsive scaling."""
        # Button font with proper scaling
        button_font = QFont("Segoe UI, Arial, sans-serif")
        button_font_size = max(10, min(16, container_width // 60))
        button_font.setPointSize(button_font_size)
        button_font.setWeight(QFont.Weight.Medium)
        self.button.setFont(button_font)

        # Description label with modern typography
        desc_font_size = max(8, min(12, container_width // 80))
        color = self._get_modern_text_color()

        self.description_label.setStyleSheet(
            f"""
            QLabel {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: {desc_font_size}px;
                font-weight: 400;
                color: {color};
                line-height: 1.4;
                margin-top: 4px;
            }}
        """
        )

    def _get_modern_text_color(self) -> str:
        """Get modern text color with proper contrast."""
        try:
            return self.settings_manager.global_settings.get_current_font_color()
        except:
            return "rgba(255, 255, 255, 0.9)"  # Modern high-contrast fallback

    def _ensure_modern_responsiveness(self):
        """Ensure modern responsiveness with enhanced activation."""
        try:
            # Enhanced button activation
            self.button.setEnabled(True)
            self.button.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
            self.button.update()

            # Ensure proper focus policies
            self.button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            # Force layout update
            self.updateGeometry()

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(f"Error in modern responsiveness setup: {e}")
