from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QStackedLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.editable_label_manager import (
    EditableLabelManager,
)
from PyQt6.QtGui import QTextOption, QResizeEvent


class EditableLabel(QWidget):
    def __init__(
        self,
        parent,
        label_text: str,
        align=Qt.AlignmentFlag.AlignLeft,
        bg_color="#FFFFFF",
        multi_line=False,
    ):
        super().__init__(parent)

        self._align = align
        self._bg_color = bg_color
        self.multi_line = multi_line

        self.label = self._create_label(label_text)
        self.edit = self._create_edit_widget()

        self.layout: QStackedLayout = self._configure_layout()
        self.apply_styles()

        self.label.mousePressEvent = self._show_edit
        self.edit.installEventFilter(self)
        self.setCursor(Qt.CursorShape.IBeamCursor)

    def change_edit_background_color(self, color):
        self.setStyleSheet(
            f"background-color: {color}; border: 1px solid gray; padding: 5px;"
        )

    def _create_label(self, text):
        label = QLabel(text, self)
        label.setAlignment(self._align)
        if self.multi_line:
            label.setWordWrap(True)
            label.setTextFormat(Qt.TextFormat.PlainText)
        return label

    def _create_edit_widget(self) -> QTextEdit | QLineEdit:
        if self.multi_line:
            edit = QTextEdit(self)
            edit.setWordWrapMode(QTextOption.WrapMode.WordWrap)
            edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            edit.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
            )
        else:
            edit = QLineEdit(self)
            edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return edit

    def _configure_layout(self) -> QStackedLayout:
        layout = QStackedLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        return layout

    def apply_styles(self, margin_top_bottom=0) -> None:
        """Apply consistent styling to label and edit without excess expansion."""
        self.label.setStyleSheet("padding: 0px; margin: 0px;")
        border_style = (
            f"border: 1px solid gray; padding: 5px; margin: {margin_top_bottom}px 0px;"
            if margin_top_bottom
            else "padding: 0px; margin: 0px;"
        )
        self.edit.setStyleSheet(f"background-color: {self._bg_color}; {border_style}")
        self.edit.setAlignment(self._align)

    def _show_edit(self, event=None) -> None:
        EditableLabelManager.set_active(self)
        if self.multi_line:
            self.edit.setPlainText(self.label.text())
        else:
            self.edit.setText(self.label.text())
        self.edit.setFont(self.label.font())
        self.layout.setCurrentWidget(self.edit)
        self.edit.setFocus()
        self.edit.selectAll()

    def _hide_edit(self) -> None:
        text = self.edit.toPlainText() if self.multi_line else self.edit.text()
        if self.multi_line:
            self.label.setTextFormat(Qt.TextFormat.PlainText)
            self.label.setWordWrap(True)
        self.label.setText(text or self.label.text())
        self.layout.setCurrentWidget(self.label)

        EditableLabelManager.clear_active()

    # def eventFilter(self, source, event) -> bool:
    #     """Filter for Enter key to commit and align height in edit mode."""
    #     if (
    #         source == self.edit
    #         and event.type() == QEvent.Type.KeyPress
    #         and event.key() == Qt.Key.Key_Return
    #         and (
    #             not self.multi_line
    #             or event.modifiers() == Qt.KeyboardModifier.NoModifier
    #         )
    #     ):
    #         self._hide_edit()
    #         return True
    #     return super().eventFilter(source, event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize both label and edit widgets to prevent overflow."""
        super().resizeEvent(event)
