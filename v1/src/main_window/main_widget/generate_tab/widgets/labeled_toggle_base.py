from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from typing import TYPE_CHECKING
from base_widgets.pytoggle import PyToggle

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class LabeledToggleBase(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        generate_tab: "GenerateTab",
        left_text: str,
        right_text: str,
    ):
        super().__init__(generate_tab)
        self.generate_tab = generate_tab
        self.left_text = left_text
        self.right_text = right_text

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Create clickable labels
        self.left_label = QLabel(self.left_text)
        self.right_label = QLabel(self.right_text)

        # Enable mouse tracking to capture clicks
        self.left_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.right_label.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self.toggle = PyToggle()
        self.toggle.stateChanged.connect(self._on_toggled)

        # Add labels and toggle switch to layout
        self.layout.addWidget(self.left_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.right_label)

        # Enable event filtering for clickable labels
        self.left_label.installEventFilter(self)
        self.right_label.installEventFilter(self)

        self.update_label_styles()

    def eventFilter(self, source, event):
        """Captures mouse clicks on labels to toggle the switch."""
        if event.type() == QEvent.Type.MouseButtonPress:
            if source == self.left_label:
                self.set_state(False)  # Set toggle to left side
            elif source == self.right_label:
                self.set_state(True)  # Set toggle to right side
            return True  # Stop further event processing
        return super().eventFilter(source, event)

    def _on_toggled(self, state: bool):
        self.update_label_styles()
        self.toggled.emit(state)
        self._handle_toggle_changed(state)

    def _handle_toggle_changed(self, state: bool):
        """Override this in subclasses."""
        print("This method should be overridden in the subclass.")

    def set_state(self, is_checked: bool):
        """Externally set the toggle state and update UI."""
        was_blocked = self.toggle.blockSignals(True)
        self.toggle.setChecked(is_checked)

        # Adjust toggle position instantly
        if is_checked:
            self.toggle.circle_position = self.toggle.width() - 26
        else:
            self.toggle.circle_position = 3

        self.toggle.blockSignals(was_blocked)
        self.update_label_styles()

    def update_label_styles(self):
        """Updates the label styles based on the toggle state."""
        if self.toggle.isChecked():
            self.left_label.setStyleSheet("font-weight: normal; color: gray;")
            self.right_label.setStyleSheet("font-weight: bold; color: white;")
        else:
            self.left_label.setStyleSheet("font-weight: bold; color: white;")
            self.right_label.setStyleSheet("font-weight: normal; color: gray;")

    def resizeEvent(self, event):
        """Adjusts font sizes dynamically."""
        font_size = self.generate_tab.main_widget.width() // 75
        font = self.left_label.font()
        font.setPointSize(font_size)

        self.left_label.setFont(font)
        self.right_label.setFont(font)

        super().resizeEvent(event)
