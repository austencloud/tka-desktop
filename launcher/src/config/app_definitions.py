from typing import List
from ..models.app_definition import AppDefinition


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
