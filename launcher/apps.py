from typing import List


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


class AppDefinitions:
    """Central place to list launch targets."""

    @staticmethod
    def all() -> List[AppDefinition]:
        return [
            AppDefinition("Legacy", "Full legacy TKA", "legacy/main.py", icon="🔧"),
            AppDefinition("Modern", "Modern TKA demo", "modern/main.py", icon="✨"),
            AppDefinition(
                "Parallel",
                "Legacy/Modern side-by-side testing",
                "parallel_test_launcher.py",
                icon="🔄",
            ),
            AppDefinition("Dev", "Debug helpers", "test_dev_tools.py", icon="🛠"),
        ]
