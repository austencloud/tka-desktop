
from styles.base_styled_button import BaseStyledButton
class SidebarButton(BaseStyledButton):
    """A specialized button for the sidebar with custom behavior."""

    def __init__(self, section_key: str):
        super().__init__(section_key)
        self.section_key = section_key
        self.clicked.connect(self.emit_clicked_signal)

    def emit_clicked_signal(self) -> None:
        """Emit signal when clicked, passing the section key."""
        self.clicked_signal.emit(self.section_key)
