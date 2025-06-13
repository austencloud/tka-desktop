from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QApplication,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from typing import List, Dict, Optional
import sys
import subprocess


class AccessibilityManager:
    _instance: Optional["AccessibilityManager"] = None

    def __init__(self) -> None:
        if AccessibilityManager._instance is not None:
            raise RuntimeError("AccessibilityManager is a singleton")
        AccessibilityManager._instance = self

    @classmethod
    def instance(cls) -> "AccessibilityManager":
        if cls._instance is None:
            cls._instance = AccessibilityManager()
        return cls._instance

    def configure_widget_accessibility(
        self, widget: QWidget, name: str, description: str = ""
    ) -> None:
        widget.setAccessibleName(name)
        if description:
            widget.setAccessibleDescription(description)
        widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


class AppDefinition:
    def __init__(
        self,
        title: str,
        description: str,
        script_path: str = "",
        command: str = "",
        icon: str = "🚀",
        tags: Optional[List[str]] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        working_dir: str = "",
    ) -> None:
        self.title = title
        self.description = description
        self.script_path = script_path
        self.command = command
        self.icon = icon
        self.tags = tags or []
        self.args = args or []
        self.env = env or {}
        self.working_dir = working_dir


class AppDefinitions:
    @staticmethod
    def get_all() -> List[AppDefinition]:
        return [
            AppDefinition(
                "🔧 V1 Main Application",
                "Full TKA application with all features",
                "v1/main.py",
            ),
            AppDefinition(
                "🆕 V2 Demo Application", "Modern architecture demo", "v2/main.py"
            ),
            AppDefinition(
                "🧪 Run All Tests", "Comprehensive test suite", "unified_dev_test.py"
            ),
            AppDefinition(
                "🎯 Debug Tools", "Development diagnostics", "test_dev_tools.py"
            ),
        ]


class LauncherWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.accessibility_manager = AccessibilityManager.instance()
        self.setup_window()
        self.setup_layout()
        self.setup_keyboard_shortcuts()

    def setup_window(self) -> None:
        self.setWindowTitle("🚀 TKA Kinetic Constructor Launcher")
        self.setMinimumSize(800, 600)
        self.resize(1200, 800)
        self.setAccessibleName("TKA Kinetic Constructor Launcher")

    def setup_layout(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        apps = AppDefinitions.get_all()
        for app in apps:
            btn = QPushButton(f"{app.icon} {app.title}")
            btn.clicked.connect(lambda checked=False, a=app: self.launch_app(a))
            btn.setStyleSheet(
                """
                QPushButton {
                    background: rgba(74, 144, 226, 0.3);
                    border: 1px solid rgba(74, 144, 226, 0.5);
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    text-align: left;
                    padding: 16px;
                    margin: 4px;
                }
                QPushButton:hover {
                    background: rgba(74, 144, 226, 0.4);
                }
                QPushButton:pressed {
                    background: rgba(74, 144, 226, 0.5);
                }
            """
            )
            layout.addWidget(btn, 1)

    def setup_keyboard_shortcuts(self) -> None:
        shortcuts = {
            "F5": self.refresh,
            "Ctrl+Q": self.close,
        }
        for key, handler in shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(handler)

    def launch_app(self, app: AppDefinition) -> None:
        try:
            if app.script_path:
                subprocess.Popen([sys.executable, app.script_path])
            elif app.command:
                subprocess.Popen(app.command, shell=True)
        except Exception as e:
            QMessageBox.warning(
                self, "Launch Error", f"Failed to launch {app.title}:\n{str(e)}"
            )

    def refresh(self) -> None:
        self.close()
        self.__init__()
        self.show()

    def move_to_secondary_monitor(self) -> None:
        screens = QApplication.screens()
        screen = (
            screens[1]
            if len(screens) > 1 and not getattr(sys, "frozen", False)
            else QApplication.primaryScreen()
        )
        if screen:
            geo = screen.availableGeometry()
            w, h = int(geo.width() * 0.8), int(geo.height() * 0.8)
            x = geo.x() + (geo.width() - w) // 2
            y = geo.y() + (geo.height() - h) // 2
            self.setGeometry(x, y, w, h)


class LauncherApplication(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)
        self.setStyle("Fusion")
        self.setApplicationName("Kinetic Constructor Launcher")
        self.setOrganizationName("Kinetic Constructor")

    def run(self) -> int:
        window = LauncherWindow()
        window.show()
        window.move_to_secondary_monitor()
        return self.exec()


def main() -> int:
    app = LauncherApplication(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
