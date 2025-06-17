class AppDefinition:
    def __init__(
        self,
        title: str,
        description: str,
        script_path: str = "",
        command: str = "",
        icon: str | None = "",
    ) -> None:
        self.title = title
        self.description = description
        self.script_path = script_path
        self.command = command
        self.icon = icon or "💻"
