# TKA Launcher - Perfect UI Layout with Accessibility-First Design
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QApplication,
    QMessageBox,
    QFrame,
    QScrollArea,
    QPushButton,
    QLabel,
    QTabWidget,
)
from PyQt6.QtCore import (
    QTimer,
    QThread,
    pyqtSignal,
    Qt,
    QPropertyAnimation,
    QEasingCurve,
)
from PyQt6.QtGui import QKeySequence, QFont, QFontMetrics, QShortcut
import sys
import subprocess
from pathlib import Path

from .components import QuickLaunchBar, CategoryTabs, StatusBar
from .components.command_palette import CommandPalette
from .components.health_indicator import HealthIndicator
from .components.responsive_grid import ResponsiveAppGrid
from .styles import StyleManager
from ..core.accessibility import AccessibilityManager
from ..core.animations import AnimationManager


class HealthChecker(QThread):
    """Background health monitoring with detailed system metrics"""

    health_updated = pyqtSignal(bool, dict)  # is_healthy, metrics

    def run(self):
        try:
            result = subprocess.run(
                [sys.executable, "unified_dev_test.py"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=Path.cwd(),
            )

            is_healthy = result.returncode == 0 and "🟢 READY" in result.stdout

            # Extract system metrics from output
            metrics = self._parse_system_metrics(result.stdout)
            self.health_updated.emit(is_healthy, metrics)
        except Exception as e:
            self.health_updated.emit(False, {"error": str(e)})

    def _parse_system_metrics(self, output: str) -> dict:
        """Parse system metrics from health check output"""
        import psutil

        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 1),
            "running_processes": len(psutil.pids()),
            "health_output": output,
        }


class LauncherWindow(QMainWindow):
    """
    TKA Launcher - Perfect UI Layout with Accessibility-First Design

    Features:
    - Command palette for power users (Ctrl+Space)
    - Quick launch bar with primary applications
    - Responsive category-based navigation
    - Advanced system health monitoring
    - Complete keyboard navigation
    - WCAG 2.1 AA accessibility compliance
    - Smooth 60fps animations
    """

    def __init__(self):
        super().__init__()
        self.accessibility_manager = AccessibilityManager.instance()
        self.animation_manager = AnimationManager()
        self.command_palette = None
        self.health_indicator = None

        self.setup_accessibility_foundation()
        self.setup_ui()
        self.setup_keyboard_navigation()
        self.setup_visual_feedback()
        self.start_health_check()

    def setup_accessibility_foundation(self):
        """WCAG 2.1 AA compliance setup"""
        self.setAccessibleName("TKA Kinetic Constructor Launcher")
        self.setAccessibleDescription(
            "Desktop application launcher with quick access to development tools, "
            "design applications, and system utilities. Press Ctrl+Space for command palette."
        )

        # Configure window properties for accessibility
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_ui(self):
        """Create the perfect launcher layout hierarchy"""
        self.setWindowTitle("🚀 TKA Kinetic Constructor Launcher")
        self.setMinimumSize(1200, 800)  # Increase minimum size
        self.resize(1400, 900)  # Larger default size

        # Apply enhanced glassmorphism styling
        self.setStyleSheet(StyleManager.get_main_style())

        # Central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        try:
            from ..data.app_definitions import AppDefinitions

            all_apps = AppDefinitions.get_all()

            # 1. GLOBAL HEADER - compact health indicator only
            header = self.create_global_header([])
            main_layout.addWidget(header)

            # 2. MAIN CONTENT - full width application grid
            app_panel = self.create_application_panel(all_apps)
            main_layout.addWidget(app_panel, 1)  # Expand to fill

            # 3. STATUS FOOTER - system state feedback
            footer = self.create_status_footer()
            main_layout.addWidget(footer)

            # 4. COMMAND PALETTE - overlay (initially hidden)
            self.setup_command_palette(all_apps)

        except Exception as e:
            QMessageBox.critical(
                self, "Setup Error", f"Failed to initialize launcher: {e}"
            )
            # Fallback to basic layout
            self.create_fallback_ui()

    def create_global_header(self, primary_apps) -> QWidget:
        """Minimal header with only health status"""
        header = QFrame()
        header.setObjectName("globalHeader")
        header.setAccessibleName("System status")
        header.setFixedHeight(40)  # Slightly larger for better visibility
        header.setStyleSheet(
            """
            QFrame#globalHeader {
                background: rgba(255, 255, 255, 0.03);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
        """
        )

        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 4, 12, 4)  # Minimal margins

        # Push health indicator to the right
        layout.addStretch()

        # Compact system health indicator
        self.health_indicator = HealthIndicator()
        self.health_indicator.setMaximumHeight(20)  # Smaller indicator
        self.health_indicator.health_clicked.connect(self.on_health_clicked)
        layout.addWidget(self.health_indicator)

        return header

    def create_application_panel(self, all_apps) -> QWidget:
        """Main application grid with responsive layout"""
        app_panel = QFrame()
        app_panel.setObjectName("applicationPanel")
        app_panel.setAccessibleName("Application grid")

        layout = QVBoxLayout(app_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Responsive application grid
        self.app_grid = ResponsiveAppGrid(all_apps)
        self.app_grid.app_launched.connect(self.launch_application)
        self.app_grid.view_changed.connect(self.on_view_changed)
        layout.addWidget(self.app_grid)

        return app_panel

    def create_status_footer(self) -> QWidget:
        """Minimal status bar"""
        footer = QFrame()
        footer.setObjectName("statusFooter")
        footer.setAccessibleName("Status bar")
        footer.setFixedHeight(24)  # Smaller footer
        footer.setStyleSheet(
            """
            QFrame#statusFooter {
                background: rgba(255, 255, 255, 0.03);
                border-top: 1px solid rgba(255, 255, 255, 0.05);
            }
        """
        )

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(12, 4, 12, 4)  # Minimal margins

        # Compact status message
        self.status_label = QLabel("Ready")
        self.status_label.setAccessibleName("Status message")
        self.status_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.6); font-size: 10px;"  # Smaller font
        )
        layout.addWidget(self.status_label)

        layout.addStretch()

        return footer

    def setup_shortcuts(self):
        try:
            from ..data.app_definitions import AppDefinitions

            for app in AppDefinitions.get_all():
                if app.keyboard_shortcut:
                    shortcut = QShortcut(QKeySequence(app.keyboard_shortcut), self)
                    shortcut.activated.connect(lambda a=app: self.launch_application(a))
        except Exception:
            pass

    def launch_application(self, app):
        """Launch application with enhanced feedback and accessibility"""
        import os

        # Update status and announce launch
        self.status_label.setText(f"Launching {app.title}...")
        self.accessibility_manager.announce_app_launch(app.title, 3)

        try:
            if app.script_path:
                cmd = [sys.executable, app.script_path]
                if app.args:
                    cmd.extend(app.args)

                env = None
                if app.env:
                    env = os.environ.copy()
                    env.update(app.env)

                working_dir = app.working_dir if app.working_dir else None
                subprocess.Popen(cmd, env=env, cwd=working_dir)

            elif app.command:
                working_dir = app.working_dir if app.working_dir else None
                env = None
                if app.env:
                    env = os.environ.copy()
                    env.update(app.env)

                subprocess.Popen(app.command, env=env, cwd=working_dir)

            # Success feedback
            self.status_label.setText(f"{app.title} launched successfully")
            self.accessibility_manager.announce_app_launch_success(app.title)

        except Exception as e:
            error_msg = f"Failed to launch {app.title}: {str(e)}"
            self.status_label.setText(error_msg)
            self.accessibility_manager.announce_app_launch_failure(app.title, str(e))
            QMessageBox.warning(
                self, "Launch Error", f"Failed to launch {app.title}:\n{str(e)}"
            )

    def start_health_check(self):
        QTimer.singleShot(2000, self.run_health_check)

    def run_health_check(self):
        """Run system health check with enhanced feedback"""
        self.health_checker = HealthChecker()
        self.health_checker.health_updated.connect(self.on_health_updated)
        self.health_checker.start()

    def on_health_updated(self, is_healthy: bool, metrics: dict):
        """Handle health check results"""
        if self.health_indicator:
            self.health_indicator.update_health_display(is_healthy, metrics)

        # Announce significant health changes
        if hasattr(self, "_last_health_status"):
            if self._last_health_status != is_healthy:
                status_text = (
                    "System health restored" if is_healthy else "System issues detected"
                )
                self.accessibility_manager.announce_system_health(
                    is_healthy, status_text
                )

        self._last_health_status = is_healthy

    def setup_command_palette(self, all_apps):
        """Initialize command palette with application data"""
        from .components.command_palette import CommandPaletteItem

        self.command_palette = CommandPalette(self)
        self.command_palette.hide()
        self.command_palette.item_selected.connect(self.on_palette_item_selected)
        self.command_palette.closed.connect(self.on_palette_closed)

        # Populate with applications
        palette_items = []
        for app in all_apps:
            item = CommandPaletteItem(
                title=app.title,
                description=app.description,
                icon=app.icon,
                action_type="app",
                data=app,
                keywords=app.tags + [app.title.lower(), app.description.lower()],
            )
            palette_items.append(item)

        # Add system commands
        system_commands = [
            CommandPaletteItem(
                "System Health Check",
                "Run comprehensive system validation",
                "🎯",
                "command",
                "health_check",
            ),
            CommandPaletteItem(
                "Toggle High Contrast",
                "Enable/disable high contrast mode",
                "🔲",
                "command",
                "toggle_contrast",
            ),
            CommandPaletteItem(
                "Show Keyboard Shortcuts",
                "Display all keyboard shortcuts",
                "⌨️",
                "command",
                "show_shortcuts",
            ),
        ]
        palette_items.extend(system_commands)

        self.command_palette.add_items(palette_items)

    def show_command_palette(self):
        """Show the command palette"""
        if self.command_palette:
            self.command_palette.show_palette()

    def on_palette_item_selected(self, item):
        """Handle command palette item selection"""
        if item.action_type == "app":
            self.launch_application(item.data)
        elif item.action_type == "command":
            self.execute_system_command(item.data)

    def on_palette_closed(self):
        """Handle command palette closing"""
        # Return focus to main window
        self.setFocus()

    def execute_system_command(self, command: str):
        """Execute system commands from palette"""
        if command == "health_check":
            self.run_health_check()
        elif command == "toggle_contrast":
            current = self.accessibility_manager.high_contrast_mode
            self.accessibility_manager.set_high_contrast_mode(not current)
        elif command == "show_shortcuts":
            self.show_keyboard_shortcuts()

    def on_health_clicked(self):
        """Handle health indicator click"""
        # Could show detailed health dialog
        pass

    def on_view_changed(self, view_mode: str):
        """Handle view mode changes"""
        self.accessibility_manager.announce(f"View changed to {view_mode} mode")

    def create_fallback_ui(self):
        """Create clean fallback UI if main setup fails"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Error message
        error_label = QLabel(
            "Failed to load full launcher interface.\nBasic mode active."
        )
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background: rgba(231, 76, 60, 0.2);
                border: 1px solid rgba(231, 76, 60, 0.4);
                border-radius: 8px;
                padding: 20px;
            }
        """
        )
        layout.addWidget(error_label)

        # Clean basic launch buttons with clear labels
        basic_apps = [
            ("V1 Main Application", "v1/main.py"),
            ("V2 Demo Application", "v2/demo_new_architecture.py"),
            ("System Health Check", "unified_dev_test.py"),
        ]

        for title, script in basic_apps:
            btn = QPushButton(title)
            btn.setFixedHeight(50)
            btn.clicked.connect(
                lambda checked=False, s=script: self.launch_basic_app(s)
            )
            btn.setStyleSheet(
                """
                QPushButton {
                    background: rgba(74, 144, 226, 0.3);
                    border: 1px solid rgba(74, 144, 226, 0.5);
                    border-radius: 6px;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 12px;
                }
                QPushButton:hover {
                    background: rgba(74, 144, 226, 0.4);
                    border-color: rgba(74, 144, 226, 0.7);
                }
                QPushButton:pressed {
                    background: rgba(74, 144, 226, 0.5);
                }
            """
            )
            layout.addWidget(btn)

    def launch_basic_app(self, script_path: str):
        """Launch application in basic mode"""
        try:
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            QMessageBox.warning(
                self, "Launch Error", f"Failed to launch {script_path}:\n{str(e)}"
            )

    def setup_keyboard_navigation(self):
        """Configure comprehensive keyboard navigation"""
        # Global shortcuts that work anywhere
        global_shortcuts = {
            "Ctrl+Space": self.show_command_palette,
            "F5": self.run_health_check,
            "Ctrl+,": self.show_preferences,
            "Escape": self.close_overlays,
            "Ctrl+Q": self.close,
            "Ctrl+F": self.focus_search,
        }

        for key, handler in global_shortcuts.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(handler)

        # Register navigation groups with accessibility manager
        if hasattr(self, "app_grid"):
            self.accessibility_manager.register_navigation_group(
                "applications", [self.app_grid]
            )

    def focus_search(self):
        """Focus the search bar in the application grid"""
        if hasattr(self, "app_grid") and hasattr(self.app_grid, "search_input"):
            self.app_grid.search_input.setFocus()
            self.app_grid.search_input.selectAll()

    def setup_visual_feedback(self):
        """Setup smooth animations and visual feedback"""
        # Configure animation manager
        self.animation_manager.set_reduced_motion(False)  # Could be user preference

        # Connect animation events
        self.animation_manager.animation_started.connect(self.on_animation_started)
        self.animation_manager.animation_finished.connect(self.on_animation_finished)

    def on_animation_started(self, animation_name: str):
        """Handle animation start"""
        pass  # Could add logging or feedback

    def on_animation_finished(self, animation_name: str):
        """Handle animation completion"""
        pass  # Could add logging or feedback

    def launch_quick_app(self, index: int):
        """Launch application from quick launch bar by index"""
        # This would need to be implemented based on quick launch bar structure
        pass

    def show_preferences(self):
        """Show preferences dialog"""
        QMessageBox.information(
            self, "Preferences", "Preferences dialog not yet implemented"
        )

    def close_overlays(self):
        """Close any open overlays like command palette"""
        if self.command_palette and self.command_palette.isVisible():
            self.command_palette.hide_palette()

    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts help"""
        shortcuts_text = """
        Global Shortcuts:
        Ctrl+Space - Open command palette
        F5 - Run health check
        Ctrl+, - Preferences
        Escape - Close overlays
        Ctrl+Q - Quit application
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kinetic Constructor Launcher")

    window = LauncherWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
