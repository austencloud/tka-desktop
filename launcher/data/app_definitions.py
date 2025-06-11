from typing import List, Dict, Tuple, Callable, Optional


class AppDefinition:
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        category: str,
        script_path: str = "",
        command: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        working_dir: str = "",
        args: Optional[List[str]] = None,
    ):
        self.title = title
        self.description = description
        self.icon = icon
        self.category = category
        self.script_path = script_path
        self.command = command or []
        self.env = env or {}
        self.working_dir = working_dir
        self.args = args or []


class AppDefinitions:
    APPLICATIONS = [
        AppDefinition(
            title="🔧 V1 Main Application",
            description="Launch the main V1 application",
            icon="🔧",
            category="applications",
            script_path="v1/src/main.py",
            working_dir=".",
            env={"PYTHONPATH": "v1/src"},
        ),
        AppDefinition(
            title="🔍 V1 Debug Mode",
            description="Launch V1 with debugging enabled",
            icon="🔍",
            category="applications",
            script_path="v1/src/main.py",
            working_dir=".",
            env={"PYTHONDEBUG": "1", "PYTHONPATH": "v1/src"},
        ),
        AppDefinition(
            title="🆕 V2 Demo",
            description="Launch the new V2 architecture demo",
            icon="🆕",
            category="applications",
            script_path="v2/demo_new_architecture.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
        ),
        AppDefinition(
            title="🏗️ Construct Tab",
            description="Launch standalone construct tab",
            icon="🏗️",
            category="applications",
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["construct"],
            env={"PYTHONPATH": "v1/src"},
        ),
        AppDefinition(
            title="🎨 Generate Tab",
            description="Launch standalone generate tab",
            icon="🎨",
            category="applications",
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["generate"],
            env={"PYTHONPATH": "v1/src"},
        ),
        AppDefinition(
            title="📖 Browse Tab",
            description="Launch standalone browse tab",
            icon="📖",
            category="applications",
            script_path="v1/src/standalone/core/launcher.py",
            working_dir=".",
            args=["browse"],
            env={"PYTHONPATH": "v1/src"},
        ),
    ]

    DEV_TOOLS = [
        AppDefinition(
            title="🧪 Run All Tests",
            description="Execute complete test suite",
            icon="🧪",
            category="dev_tools",
            command=["python", "-m", "pytest", "tests/"],
            working_dir="v1",
            env={"PYTHONPATH": "src"},
        ),
        AppDefinition(
            title="🔧 Standalone Tests",
            description="Run standalone system tests",
            icon="🔧",
            category="dev_tools",
            command=["python", "-m", "pytest", "src/standalone/tests/"],
            working_dir="v1",
            env={"PYTHONPATH": "src"},
        ),
        AppDefinition(
            title="📝 Format Code",
            description="Format code with black",
            icon="📝",
            category="dev_tools",
            command=["python", "-m", "black", "src/", "--line-length=88"],
            working_dir="v1",
        ),
        AppDefinition(
            title="🔍 Lint Code",
            description="Run linting with flake8",
            icon="🔍",
            category="dev_tools",
            command=[
                "python",
                "-m",
                "flake8",
                "src/",
                "--max-line-length=88",
                "--exclude=__pycache__,*.pyc",
            ],
            working_dir="v1",
        ),
        AppDefinition(
            title="🧹 Clean Cache",
            description="Clear Python cache files",
            icon="🧹",
            category="dev_tools",
            command=[
                "python",
                "-c",
                "import shutil, os; [shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True) for root, dirs, files in os.walk('.') if '__pycache__' in dirs]",
            ],
            working_dir=".",
        ),
        AppDefinition(
            title="📊 V2 Test",
            description="Test V2 architecture",
            icon="📊",
            category="dev_tools",
            script_path="v2/test_simple.py",
            working_dir=".",
            env={"PYTHONPATH": "v2"},
        ),
    ]

    @classmethod
    def get_by_category(cls, category: str) -> List[AppDefinition]:
        if category == "applications":
            return cls.APPLICATIONS
        elif category == "dev_tools":
            return cls.DEV_TOOLS
        return []

    @classmethod
    def get_all(cls) -> List[AppDefinition]:
        return cls.APPLICATIONS + cls.DEV_TOOLS
