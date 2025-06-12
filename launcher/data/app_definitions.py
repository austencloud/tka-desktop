from typing import List, Dict, Optional
from enum import Enum
from ..core.config import Paths


class AppPriority(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DEBUG = "debug"


class AppCategory(Enum):
    MAIN = "main"
    DEVELOPMENT = "development"
    UTILITIES = "utilities"
    TESTING = "testing"


class AppDefinition:
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        category: AppCategory,
        priority: AppPriority = AppPriority.SECONDARY,
        script_path: str = "",
        command: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        working_dir: str = "",
        args: Optional[List[str]] = None,
        keyboard_shortcut: str = "",
        tags: Optional[List[str]] = None,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.category = category
        self.priority = priority
        self.script_path = script_path
        self.command = command or []
        self.env = env or {}
        self.working_dir = working_dir
        self.args = args or []
        self.keyboard_shortcut = keyboard_shortcut
        self.tags = tags or []


class AppDefinitions:
    APPLICATIONS = [
        AppDefinition(
            title="V1 Main Application",
            description="Production kinetic constructor with full feature set",
            icon="🚀",
            category=AppCategory.MAIN,
            priority=AppPriority.PRIMARY,
            script_path="v1/main.py",
            working_dir=".",
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+1",
            tags=["production", "main", "v1"],
        ),
        AppDefinition(
            title="V2 Architecture Demo",
            description="Next-generation architecture preview",
            icon="⚡",
            category=AppCategory.MAIN,
            priority=AppPriority.PRIMARY,
            script_path="v2/demo_new_architecture.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
            keyboard_shortcut="Ctrl+2",
            tags=["preview", "v2", "architecture"],
        ),
        AppDefinition(
            title="Construct Workspace",
            description="Standalone beat sequence construction",
            icon="🔨",
            category=AppCategory.UTILITIES,
            priority=AppPriority.SECONDARY,
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["construct"],
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+C",
            tags=["construct", "beats", "sequence"],
        ),
        AppDefinition(
            title="Generate Workspace",
            description="Automated sequence generation tools",
            icon="✨",
            category=AppCategory.UTILITIES,
            priority=AppPriority.SECONDARY,
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["generate"],
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+G",
            tags=["generate", "automation"],
        ),
        AppDefinition(
            title="Browse Library",
            description="Sequence library browser and manager",
            icon="📚",
            category=AppCategory.UTILITIES,
            priority=AppPriority.SECONDARY,
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["browse"],
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+B",
            tags=["browse", "library", "search"],
        ),
    ]

    DEVELOPMENT = [
        AppDefinition(
            title="System Health Check",
            description="Comprehensive development environment validation",
            icon="🎯",
            category=AppCategory.DEVELOPMENT,
            priority=AppPriority.PRIMARY,
            script_path="unified_dev_test.py",
            working_dir=".",
            keyboard_shortcut="F5",
            tags=["health", "validation", "testing"],
        ),
        AppDefinition(
            title="V2 Architecture Test",
            description="Validate V2 system components and rendering",
            icon="🧪",
            category=AppCategory.TESTING,
            priority=AppPriority.SECONDARY,
            script_path="v2/test_final_complete.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
            keyboard_shortcut="F6",
            tags=["v2", "testing", "validation"],
        ),
        AppDefinition(
            title="Pictograph Renderer",
            description="Test pictograph generation and positioning",
            icon="🖼️",
            category=AppCategory.TESTING,
            priority=AppPriority.SECONDARY,
            script_path="v2/test_pictograph_rendering.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
            tags=["pictograph", "rendering", "visual"],
        ),
        AppDefinition(
            title="Debug Pictograph",
            description="Debug pictograph rendering with breakpoints",
            icon="🐛",
            category=AppCategory.TESTING,
            priority=AppPriority.DEBUG,
            command=[
                "python",
                "-m",
                "debugpy",
                "--listen",
                "5684",
                "--wait-for-client",
                "v2/test_pictograph_rendering.py",
            ],
            working_dir=".",
            env={"PYTHONPATH": "v2"},
            keyboard_shortcut="F7",
            tags=["debug", "pictograph", "breakpoints"],
        ),
    ]

    @classmethod
    def get_by_category(cls, category: AppCategory) -> List[AppDefinition]:
        all_apps = cls.APPLICATIONS + cls.DEVELOPMENT
        return [app for app in all_apps if app.category == category]

    @classmethod
    def get_by_priority(cls, priority: AppPriority) -> List[AppDefinition]:
        all_apps = cls.APPLICATIONS + cls.DEVELOPMENT
        return [app for app in all_apps if app.priority == priority]

    @classmethod
    def get_primary_apps(cls) -> List[AppDefinition]:
        return cls.get_by_priority(AppPriority.PRIMARY)

    @classmethod
    def search_by_tags(cls, tags: List[str]) -> List[AppDefinition]:
        all_apps = cls.APPLICATIONS + cls.DEVELOPMENT
        return [app for app in all_apps if any(tag in app.tags for tag in tags)]

    @classmethod
    def get_all(cls) -> List[AppDefinition]:
        return cls.APPLICATIONS + cls.DEVELOPMENT
