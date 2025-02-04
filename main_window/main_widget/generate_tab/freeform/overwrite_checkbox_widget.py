from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class OverwriteCheckboxWidget(QWidget):
    clicked = pyqtSignal(bool)  # Emitted when the checkbox toggles

    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__(generate_tab)
        self.generate_tab = generate_tab
        self.checkbox = QCheckBox("", self)
        text = "Overwrite sequence"
        self.label = QLabel(text, self)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )

        # Layout
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        # layout.addStretch(1)

        # Connect the checkbox toggle to a signal if needed
        self.checkbox.stateChanged.connect(self._checkbox_toggled)

    def _checkbox_toggled(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.clicked.emit(is_checked)

    def setChecked(self, checked: bool):
        self.checkbox.setChecked(checked)

    def isChecked(self) -> bool:
        return self.checkbox.isChecked()

    def setText(self, text: str):
        self.label.setText(text)

    def text(self) -> str:
        return self.label.text()

    def set_label_color(self, color: str):
        # Apply color just to the label, not the checkbox
        existing_style = self.label.styleSheet()
        new_style = f"{existing_style} color: {color};"
        self.label.setStyleSheet(new_style)

    def mousePressEvent(self, event: QMouseEvent):
        # If the user clicks on the label portion, toggle the checkbox.
        # Check if the click is outside the checkbox rect to avoid conflict.
        checkbox_rect = self.checkbox.geometry()
        if not checkbox_rect.contains(event.pos()):
            self.checkbox.toggle()  # Toggle state
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font = self.font()
        font.setPointSize(self.generate_tab.main_widget.height() // 65)
        self.label.setFont(font)
        # self.label.setFont(QFont("Arial", self.height() // 50, 0))