class ColorUtils:
    @staticmethod
    def lighten_color(color_hex: str) -> str:
        """
        Lightens a given hex color by a factor of 2 (makes it brighter).

        Args:
            color_hex (str): The hex color code to lighten (e.g., "#RRGGBB").

        Returns:
            str: The lightened hex color code (e.g., "rgb(r, g, b)").
        """
        r, g, b = (
            int(color_hex[1:3], 16),
            int(color_hex[3:5], 16),
            int(color_hex[5:7], 16),
        )
        whitened_r = min(255, r + (255 - r) // 2)
        whitened_g = min(255, g + (255 - g) // 2)
        whitened_b = min(255, b + (255 - b) // 2)
        whitened_color = f"rgb({whitened_r}, {whitened_g}, {whitened_b})"
        return whitened_color
