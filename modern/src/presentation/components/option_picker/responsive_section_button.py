from typing import Optional, TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt, QSize, pyqtSignal

if TYPE_CHECKING:
    from .option_picker_section import OptionPickerSection


class ResponsiveSectionButton(QPushButton):
    """
    Responsive section button that adapts its size based on available screen space.
    Integrates with ResponsiveSizingManager for dynamic sizing.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSection"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self.is_expanded = True
        self._base_background_color = "rgba(255, 255, 255, 200)"
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Dynamic sizing properties
        self._responsive_sizing: Optional[Dict] = None
        self._min_font_size = 8
        self._max_font_size = 16
        self._font_scale_factor = 0.7  # Proportion of header height for font

        # Create embedded label for HTML text
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Setup layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate text and apply initial styling
        self._paint_text(section_widget.letter_type)
        self._set_initial_styles()

    def set_responsive_sizing(self, sizing_config: Dict):
        """Update button sizing based on responsive sizing configuration"""
        self._responsive_sizing = sizing_config
        self._apply_responsive_sizing()

    def _apply_responsive_sizing(self):
        """Apply responsive sizing to the button"""
        if not self._responsive_sizing:
            return

        # Get header height from sizing config
        header_height = self._responsive_sizing.get("header_height", 40)
        container_width = self._responsive_sizing.get("container_width", 800)

        # Calculate font size based on header height
        font_size = max(
            self._min_font_size,
            min(self._max_font_size, int(header_height * self._font_scale_factor)),
        )

        # Calculate button dimensions
        button_height = header_height
        button_width = min(
            container_width // 3, int(button_height * 6)
        )  # Maintain aspect ratio

        # Apply sizing
        self.setFixedSize(QSize(button_width, button_height))

        # Update font
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)

        # Reapply styling with new dimensions
        self._update_style()

    def _paint_text(self, letter_type: str) -> None:
        """Generate and set HTML text"""
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: str) -> str:
        """Generate HTML text format"""
        type_texts = {
            "Type1": "Type 1 - Dual Shift",
            "Type2": "Type 2 - Shift",
            "Type3": "Type 3 - Cross Shift",
            "Type4": "Type 4 - Dash",
            "Type5": "Type 5 - Dual Dash",
            "Type6": "Type 6 - Static",
        }

        display_text = type_texts.get(letter_type, letter_type)
        words = display_text.split()
        styled_words = []

        for word in words:
            if word in ["Dual", "Shift", "Cross", "Dash", "Static"]:
                color = self._get_word_color(word)
                styled_words.append(f"<span style='color: {color};'>{word}</span>")
            elif word in ["Type", "1", "2", "3", "4", "5", "6", "-"]:
                styled_words.append(f"<span style='color: #000000;'>{word}</span>")
            else:
                styled_words.append(word)

        return " ".join(styled_words)

    def _get_word_color(self, word: str) -> str:
        """Get color for word types"""
        colors = {
            "Dual": "#00b3ff",
            "Shift": "#6F2DA8",
            "Cross": "#26e600",
            "Dash": "#26e600",
            "Static": "#eb7d00",
        }
        return colors.get(word, "#000000")

    def _set_initial_styles(self) -> None:
        """Apply initial styling"""
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self._update_style()

    def _update_style(self, background_color: Optional[str] = None) -> None:
        """Update button styling with responsive dimensions"""
        background_color = background_color or "rgba(255, 255, 255, 0.3)"

        # Calculate border radius based on current height
        border_radius = min(18, self.height() // 2)

        style = (
            f"QPushButton {{"
            f"  background: {background_color};"
            f"  border: 1px solid rgba(255, 255, 255, 0.4);"
            f"  border-radius: {border_radius}px;"
            f"  padding: 4px 12px;"
            f"  margin: 2px;"
            f"  font-weight: bold;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: rgba(255, 255, 255, 0.45);"
            f"  border: 2px solid rgba(255, 255, 255, 0.6);"
            f"}}"
            f"QPushButton:pressed {{"
            f"  background: rgba(255, 255, 255, 0.55);"
            f"  border: 1px solid rgba(255, 255, 255, 0.7);"
            f"}}"
        )
        self.setStyleSheet(style)

    # Event handlers
    def enterEvent(self, event) -> None:
        """Hover effect"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Leave effect"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Press effect"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Release effect"""
        self._update_style()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        """Handle resize events"""
        super().resizeEvent(event)

        # If we have responsive sizing config, apply it
        if self._responsive_sizing:
            self._apply_responsive_sizing()
        else:
            # Fallback to legacy-style sizing
            self._apply_legacy_sizing()

    def _apply_legacy_sizing(self):
        """Fallback legacy-style sizing when responsive sizing is not available"""
        if hasattr(self.section_widget, "mw_size_provider") and callable(
            self.section_widget.mw_size_provider
        ):
            try:
                parent_height = self.section_widget.mw_size_provider().height()
                font_size = max(parent_height // 70, 10)
                label_height = max(int(font_size * 3), 20)
                label_width = max(int(label_height * 6), 100)

                font = self.label.font()
                font.setPointSize(font_size)
                self.label.setFont(font)

                self.setFixedSize(QSize(label_width, label_height))
                self._update_style()
            except Exception:
                # If legacy sizing fails, use minimal defaults
                self.setFixedSize(QSize(120, 30))

    def toggle_expansion(self) -> None:
        """Toggle section expansion state"""
        self.is_expanded = not self.is_expanded
        self._paint_text(self.section_widget.letter_type)
