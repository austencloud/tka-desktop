from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from .letter_types import LetterType

if TYPE_CHECKING:
    from .option_picker_section import OptionPickerSection


class LetterTypeTextPainter:
    """V1's exact color scheme for letter type text"""

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
        """Generate V1-style colored HTML text"""
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
    V1-exact section button with embedded QLabel for HTML rendering.
    Matches V1's oval shape, transparent background, and dynamic sizing.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSection"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self.is_expanded = True  # V1-style: sections start expanded
        self._base_background_color = (
            "rgba(255, 255, 255, 200)"  # V1's exact background
        )
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create embedded label for HTML text exactly like V1
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # V1-exact layout: no margins, center alignment
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate V1-style HTML text
        self._paint_text(section_widget.letter_type)

        # Apply V1-exact styling
        self._set_initial_styles()

    def _paint_text(self, letter_type: str) -> None:
        """Generate and set V1-exact HTML text"""
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: str) -> str:
        """Generate V1-exact HTML text format"""
        # Get description and type name from V2's LetterType class
        description, type_name = LetterType.get_type_description(letter_type)

        # Extract plain text from HTML description for color processing
        import re

        plain_description = re.sub(r"<[^>]+>", "", description)

        # Generate V1-style colored HTML text
        styled_type_name = LetterTypeTextPainter.get_colored_text(plain_description)
        return f"{type_name}: {styled_type_name}"

    def _set_initial_styles(self) -> None:
        """Apply V1-exact initial styling"""
        # V1-exact bold font
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        # Apply initial style
        self._update_style()

    def _update_style(self, background_color: Optional[str] = None) -> None:
        """
        V1-exact button styling: oval shape, transparent background, no borders.
        """
        background_color = background_color or self._base_background_color
        style = (
            f"QPushButton {{"
            f"  background-color: {background_color};"
            f"  font-weight: bold;"
            f"  border: none;"
            f"  border-radius: {self.height() // 2}px;"  # V1's oval shape
            f"  padding: 5px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  border: 2px solid black;"  # V1's hover effect
            f"}}"
        )
        self.setStyleSheet(style)

    # ---------- V1-EXACT HOVER / PRESS / RELEASE STATES ----------

    def enterEvent(self, event) -> None:
        """V1-exact hover effect with gradient"""
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """V1-exact leave effect"""
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """V1-exact press effect"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """V1-exact release effect"""
        self._update_style()
        super().mouseReleaseEvent(event)

    # ---------- V1-EXACT RESIZE LOGIC ----------

    def resizeEvent(self, event) -> None:
        """
        V1-exact dynamic sizing: adapts to parent size with proper font scaling.
        Matches V1's 87px-102px height range.
        """
        super().resizeEvent(event)

        # V1-exact sizing calculation with fallback
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

        # Apply V1-exact font sizing
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)

        # V1-exact button sizing
        self.setFixedSize(QSize(label_width, label_height))

        # Reapply style for correct border radius
        self._update_style()

    def toggle_expansion(self) -> None:
        """Toggle section expansion state and update text"""
        self.is_expanded = not self.is_expanded
        self._paint_text(self.section_widget.letter_type)
