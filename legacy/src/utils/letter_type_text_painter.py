# letter_type_text_painter.py
class LetterTypeTextPainter:
    COLORS = {
        "Shift": "#6F2DA8",
        "Dual": "#00b3ff",
        "Dash": "#26e600",
        "Cross": "#26e600",
        "Static": "#eb7d00",
        "-": "#000000",
    }

    @classmethod
    def get_colored_text(cls, text: str, bold: bool = False) -> str:
        type_words = text.split("-")
        styled_words = [
            (
                f"<span style='color: {cls.COLORS.get(word, 'black')};"
                f"{' font-weight: bold;' if bold else ''}'>{word}</span>"
            )
            for word in type_words
        ]
        if "-" in text:
            return "-".join(styled_words)
        return "".join(styled_words)