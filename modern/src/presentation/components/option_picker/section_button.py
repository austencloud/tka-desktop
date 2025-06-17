from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from .letter_types import LetterType

if TYPE_CHECKING:
    from .option_picker_section import OptionPickerSection


class LetterTypeTextPainter:
    """Legacy's exact color scheme for letter type text"""

    COLORS = {
        "Shift": "#6F2DA8",
        "Dual": "#00b3ff",
        "Dash": "#26e600",
        "Cross": "#26e600",
        "Static": "#eb7d00",
        "-": "#000000",
    }

    @classmethod
    def get_colored_text(cls, text: str) -> str:
        """Generate Legacy-style colored HTML text"""
        type_words = text.split("-")
        styled_words = [
            f"<span style='color: {cls.COLORS.get(word, 'black')};'>{word}</span>"
            for word in type_words
        ]
        if "-" in text:
            return "-".join(styled_words)
        return "".join(styled_words)


class OptionPickerSectionButton(QPushButton):
    """
    Legacy-exact section button with embedded QLabel for HTML rendering.
    Matches Legacy's oval shape, transparent background, and dynamic sizing.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSection"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self.is_expanded = True  # Legacy-style: sections start expanded
        self._base_background_color = (
            "rgba(255, 255, 255, 200)"  # Legacy's exact background
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create embedded label for HTML text exactly like Legacy
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Legacy-exact layout: no margins, center alignment
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate Legacy-style HTML text
        self._paint_text(section_widget.letter_type)

        # Apply Legacy-exact styling
        self._set_initial_styles()

    def _paint_text(self, letter_type: str) -> None:
        """Generate and set Legacy-exact HTML text"""
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: str) -> str:
        """Generate Legacy-exact HTML text format"""
        # Map letter types to legacy's exact format
        type_texts = {
            "Type1": "Type 1 - Dual Shift",
            "Type2": "Type 2 - Shift",
            "Type3": "Type 3 - Cross Shift",
            "Type4": "Type 4 - Dash",
            "Type5": "Type 5 - Dual Dash",
            "Type6": "Type 6 - Static",
        }

        # Get legacy's exact text format
        display_text = type_texts.get(letter_type, letter_type)

        # Apply legacy's color scheme to the words
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
        """Get legacy's exact color for each word type"""
        colors = {
            "Dual": "#00b3ff",  # Blue for Dual
            "Shift": "#6F2DA8",  # Purple for Shift
            "Cross": "#26e600",  # Green for Cross
            "Dash": "#26e600",  # Green for Dash
            "Static": "#eb7d00",  # Orange for Static
        }
        return colors.get(word, "#000000")

    def _set_initial_styles(self) -> None:
        """Apply Legacy-exact initial styling"""
        # Legacy-exact bold font
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        # Apply initial style
        self._update_style()

    def _update_style(self, background_color: Optional[str] = None) -> None:
        """
        Legacy-exact button styling: oval shape, transparent background, no borders.
        """
        background_color = background_color or "rgba(255, 255, 255, 0.3)"

        # Force a substantial border radius for visible rounding
        border_radius = 18

        style = (
            f"QPushButton {{"
            f"  background: {background_color};"
            f"  border: 1px solid rgba(255, 255, 255, 0.4);"
            f"  border-radius: {border_radius}px;"
            f"  padding: 8px 20px;"
            f"  margin: 2px;"
            f"  font-weight: bold;"
            f"  min-height: 36px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: rgba(255, 255, 255, 0.45);"
            f"  border: 2px solid rgba(255, 255, 255, 0.6);"
            f"  border-radius: {border_radius}px;"
            f"}}"
            f"QPushButton:pressed {{"
            f"  background: rgba(255, 255, 255, 0.55);"
            f"  border: 1px solid rgba(255, 255, 255, 0.7);"
            f"  border-radius: {border_radius}px;"
            f"}}"
        )
        self.setStyleSheet(style)

    # ---------- Legacy-EXACT HOVER / PRESS / RELEASE STATES ----------

    def enterEvent(self, event) -> None:
        """Legacy-exact hover effect with gradient"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Legacy-exact leave effect"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Legacy-exact press effect"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Legacy-exact release effect"""
        self._update_style()
        super().mouseReleaseEvent(event)

    # ---------- Legacy-EXACT RESIZE LOGIC ----------

    def resizeEvent(self, event) -> None:
        """
        Legacy-exact dynamic sizing: adapts to parent size with proper font scaling.
        Matches Legacy's 87px-102px height range.
        """
        super().resizeEvent(event)

        # Legacy-exact sizing calculation with fallback
        if self.section_widget.mw_size_provider and callable(
            self.section_widget.mw_size_provider
        ):
            parent_height = self.section_widget.mw_size_provider().height()
        else:
            # Fallback to reasonable default
            parent_height = 800

        font_size = max(parent_height // 70, 10)
        label_height = max(int(font_size * 3), 20)
        label_width = max(int(label_height * 6), 100)

        # Apply Legacy-exact font sizing
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)

        # Legacy-exact button sizing
        self.setFixedSize(QSize(label_width, label_height))

        # Reapply style for correct border radius
        self._update_style()

    def toggle_expansion(self) -> None:
        """Toggle section expansion state and update text"""
        self.is_expanded = not self.is_expanded
        self._paint_text(self.section_widget.letter_type)
