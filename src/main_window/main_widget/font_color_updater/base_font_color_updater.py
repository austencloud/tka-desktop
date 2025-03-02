from PyQt6.QtWidgets import QWidget, QCheckBox


class BaseFontColorUpdater:
    def __init__(self, font_color: str):
        """
        :param font_color: The color (e.g. "black" or "white") to apply.
        """
        self.font_color = font_color

    def _apply_font_color(self, widget: QWidget) -> None:
        """Apply self.font_color to a single widget, with special handling for QCheckBox."""
        if isinstance(widget, QCheckBox):
            widget.setStyleSheet(
                f"""
                QCheckBox {{
                    color: {self.font_color};
                }}
                QCheckBox::indicator {{
                    background-color: white; 
                    border: 2px solid #ccc;
                    width: 18px;
                    height: 18px;
                }}
                QCheckBox::indicator:checked {{
                    border: 2px solid #68d4ff;
                    background-color: white;
                }}
                """
            )
        else:
            if widget:
                existing_style = widget.styleSheet() or ""
                new_style = f"{existing_style} color: {self.font_color};"
                widget.setStyleSheet(new_style)

    def _apply_font_colors(self, widgets: list[QWidget]) -> None:
        """Apply font color to a list of widgets."""
        for w in widgets:
            self._apply_font_color(w)

    def update(self):
        """Apply font color to the relevant widgets."""
        raise NotImplementedError("Subclasses must implement this method.")
