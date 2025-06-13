from typing import List, Dict, Optional
from enum import Enum
from ..core.config import Paths


class AppPriority(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DEBUG = "debug"


class AppCategory(Enum):
    MAIN_APPLICATIONS = "main_applications"
    DEVELOPMENT_TOOLS = "development_tools"
    SYSTEM_UTILITIES = "system_utilities"


class AppType(Enum):
    MAIN_APPLICATION = "main_application"
    STANDALONE_TOOL = "standalone_tool"
    DEVELOPMENT_TOOL = "development_tool"


class AppDefinition:
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        category: AppCategory,
        priority: AppPriority = AppPriority.SECONDARY,
        app_type: AppType = AppType.MAIN_APPLICATION,
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
        self.app_type = app_type
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
            category=AppCategory.MAIN_APPLICATIONS,
            priority=AppPriority.PRIMARY,
            app_type=AppType.MAIN_APPLICATION,
            script_path="v1/main.py",
            working_dir=".",
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+1",
            tags=["production", "main", "v1"],
        ),
        AppDefinition(
            title="V2 Main Application",
            description="Next-generation kinetic constructor with modern architecture",
            icon="🚀",
            category=AppCategory.MAIN_APPLICATIONS,
            priority=AppPriority.PRIMARY,
            app_type=AppType.MAIN_APPLICATION,
            script_path="v2/main.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
            keyboard_shortcut="Ctrl+2",
            tags=["v2", "modern", "main"],
        ),
        AppDefinition(
            title="Construct Tab",
            description="Standalone construct tab component",
            icon="🔧",
            category=AppCategory.SYSTEM_UTILITIES,
            priority=AppPriority.SECONDARY,
            app_type=AppType.STANDALONE_TOOL,
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["construct"],
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+Shift+C",
            tags=["construct", "component"],
        ),
        AppDefinition(
            title="Sequence Generator",
            description="Automated sequence generation tools",
            icon="✨",
            category=AppCategory.SYSTEM_UTILITIES,
            priority=AppPriority.SECONDARY,
            app_type=AppType.STANDALONE_TOOL,
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["generate"],
            env={"PYTHONPATH": "v1/src"},
            keyboard_shortcut="Ctrl+G",
            tags=["generate", "automation"],
        ),
        AppDefinition(
            title="Browse Tab",
            description="Sequence library browser and manager",
            icon="📚",
            category=AppCategory.SYSTEM_UTILITIES,
            priority=AppPriority.SECONDARY,
            app_type=AppType.STANDALONE_TOOL,
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
            category=AppCategory.DEVELOPMENT_TOOLS,
            priority=AppPriority.PRIMARY,
            app_type=AppType.DEVELOPMENT_TOOL,
            script_path="unified_dev_test.py",
            working_dir=".",
            keyboard_shortcut="F5",
            tags=["health", "validation", "testing"],
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
