from typing import TYPE_CHECKING

from styles.styled_button import StyledButton

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GenerateSequenceButton(StyledButton):
    def __init__(
        self, sequence_generator_widget: "GenerateTab", text: str, overwrite: bool
    ):
        super().__init__(text)
        self.clicked.connect(
            lambda: sequence_generator_widget.controller.handle_generate_sequence(
                overwrite=overwrite
            )
        )
        self.main_widget = sequence_generator_widget.main_widget

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.main_widget.width()
        font_size = width // 80
        button_height = self.main_widget.height() // 14
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)
        self.setFixedWidth(self.main_widget.width() // 6)
        self.setFixedHeight(button_height)
