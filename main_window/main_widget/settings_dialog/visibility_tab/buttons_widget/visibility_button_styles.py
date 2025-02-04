class VisibilityButtonStyles:
    @staticmethod
    def hovered(border_radius: int):
        return (
            f"background-color: #E0E0E0; color: black; "
            f"border: 2px solid #9E9E9E; border-radius: {border_radius}px; "
            "padding: 5px;"
        )

    @staticmethod
    def default(border_radius: int):
        return (
            f"background-color: #F5F5F5; color: black; "
            f"border: 1px solid #9E9E9E; border-radius: {border_radius}px; "
            "padding: 10px;"
        )

    @staticmethod
    def toggled(border_radius: int):
        return (
            f"background-color: #4CAF50; color: white; "
            f"border: 2px solid #388E3C; border-radius: {border_radius}px; "
            "padding: 10px;"
        )
