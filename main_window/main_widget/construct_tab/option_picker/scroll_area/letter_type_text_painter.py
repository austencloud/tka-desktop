class LetterTypeTextPainter:
    COLORS = {
        "Shift": "#6F2DA8",  # purple
        "Dual": "#00b3ff",  # cyan
        "Dash": "#26e600",  # green
        "Cross": "#26e600",  # green
        "Static": "#eb7d00",  # orange
        "-": "#000000",  # black
    }

    @classmethod
    def get_colored_text(cls, text: str, bold: bool = False) -> str:
        """Returns the input text colored based on type keywords and bold if specified."""
        type_words = text.split("-")
        styled_words = [
            (
                f"<span style='color: {cls.COLORS.get(word, 'black')};"
                f"{' font-weight: bold;' if bold else ''}'>{word}</span>"
            )
            for word in type_words
        ]
        return "-".join(styled_words) if "-" in text else "".join(styled_words)
