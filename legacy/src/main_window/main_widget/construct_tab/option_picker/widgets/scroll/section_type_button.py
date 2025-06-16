from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent
from enums.letter.letter_type import LetterType
from utils.letter_type_text_painter import LetterTypeTextPainter

if TYPE_CHECKING:
    from .section_widget import OptionPickerSectionWidget


class OptionPickerSectionTypeButton(QPushButton):
    """
    A push-button that embeds a QLabel to display HTML from LetterTypeTextPainter,
    while the push-button itself handles hover, press, release, etc.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSectionWidget"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self._base_background_color = "rgba(255, 255, 255, 200)"
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create a label that will render HTML
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Put the label inside the button via a layout
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate HTML from the letter type
        self._paint_text(section_widget.letter_type)

        # Initial style
        self._set_initial_styles()

    def _paint_text(self, letter_type: LetterType) -> None:
        # Get the HTML from LetterTypeTextPainter
        html_text = self._generate_html_text(letter_type)
        # Set the label's text to that HTML
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: LetterType) -> str:
        # Example: "Dual-Shift" => <span style='color: #...'>Dual</span>-<span>Shift</span>
        letter_type_str = letter_type.name
        styled_type_name = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )
        return f"{letter_type_str[0:4]} {letter_type_str[4]}: {styled_type_name}"

    def _set_initial_styles(self) -> None:
        # Optionally set a bold font
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        # Force an initial style update
        self._update_style()

    def _update_style(self, background_color: str = None) -> None:
        """
        Updates the push-button's background, corners, etc. We do NOT set text here,
        because the text is handled by the embedded label.
        """
        background_color = background_color or self._base_background_color
        style = (
            f"QPushButton {{"
            f"  background-color: {background_color};"
            f"  font-weight: bold;"
            f"  border: none;"
            f"  border-radius: {self.height() // 2}px;"
            f"  padding: 5px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  border: 2px solid black;"
            f"}}"
        )
        self.setStyleSheet(style)

    # ---------- HOVER / PRESS / RELEASE STATES ----------

    def enterEvent(self, event) -> None:
        # Example: apply a gradient on hover
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()  # or rely on QPushButton's built-in .clicked signal
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._update_style()
        super().mouseReleaseEvent(event)

    # ---------- RESIZE LOGIC ----------

    def resizeEvent(self, event) -> None:
        """
        This can adapt the button's size to the parent's size,
        and adjust the label's font, etc.
        """
        super().resizeEvent(event)

        parent_height = self.section_widget.mw_size_provider().height()
        font_size = max(parent_height // 70, 10)
        label_height = max(int(font_size * 3), 20)
        label_width = max(int(label_height * 6), 100)

        # Adjust label's font
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)

        # Resize the push-button
        self.setFixedSize(QSize(label_width, label_height))

        # Reapply style so corner radius is correct
        self._update_style()
