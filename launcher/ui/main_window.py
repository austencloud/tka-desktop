# Updated main_window.py - Responsive Layout
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
    QTabWidget,
    QStatusBar,
    QSystemTrayIcon,
    QMenu,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction, QShortcut, QKeySequence, QResizeEvent
from datetime import datetime
import time
from .tabs.dashboard_tab import DashboardTab
from .styles import StyleManager
from .notifications import NotificationManager
from .command_palette import CommandPalette


class LauncherWindow(QMainWindow):
    def __init__(
        self,
        config,
        process_manager,
        recent_actions_manager,
        favorites_manager,
        process_monitor,
        cache,
        workflow_manager,
    ):
        super().__init__()
        self.config = config
        self.process_manager = process_manager
        self.recent_actions_manager = recent_actions_manager
        self.favorites_manager = favorites_manager
        self.process_monitor = process_monitor
        self.cache = cache
        self.workflow_manager = workflow_manager
        self.notifications = NotificationManager(self)

        self.setup_ui()
        self.setup_system_tray()
        self.setup_shortcuts()
        self.setup_monitoring()

    def setup_ui(self):
        self.setWindowTitle("🚀 Kinetic Constructor - Advanced Launcher")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_main_style())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.create_header(layout)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(StyleManager.get_tab_style())

        self.dashboard_tab = DashboardTab(
            self.recent_actions_manager,
            self.favorites_manager,
            self.process_manager,
            self.cache,
            self.workflow_manager,
        )
        self.tab_widget.addTab(self.dashboard_tab, "🏠 Dashboard")

        try:
            from .tabs.monitor_tab import MonitorTab

            self.monitor_tab = MonitorTab(self.process_manager)
            self.tab_widget.addTab(self.monitor_tab, "📊 Monitor")
        except ImportError:
            pass

        layout.addWidget(self.tab_widget)
        self.create_status_bar()

    def create_header(self, layout):
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(
            f"""
            QFrame {{
                {StyleManager.get_gradient_background()}
                border: none;
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 0px;
            }}
        """
        )

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 10, 25, 10)
        header_layout.setSpacing(15)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel("🚀 Kinetic Constructor")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(
            """
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ffffff, stop:0.5 #e8e8ff, stop:1 #ffffff);
            margin: 0px;
        """
        )

        subtitle = QLabel("Advanced Development Launcher")
        subtitle.setFont(QFont("Segoe UI", 11, QFont.Weight.Normal))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8); margin: 0px;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        # Compact quick actions
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(8)

        self.theme_toggle = QPushButton("🌙")
        self.settings_btn = QPushButton("⚙️")
        self.minimize_btn = QPushButton("📌")

        for btn in [self.theme_toggle, self.settings_btn, self.minimize_btn]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(StyleManager.get_button_style("compact", compact=True))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            quick_actions.addWidget(btn)

        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.minimize_btn.clicked.connect(self.hide)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(quick_actions)

        layout.addWidget(header)

    def create_status_bar(self):
        status_bar = self.statusBar()
        if status_bar:
            status_bar.setFixedHeight(25)  # Compact status bar
            status_bar.setStyleSheet(
                """
                QStatusBar {
                    background: rgba(255, 255, 255, 0.05);
                    color: white;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    font-size: 11px;
                }
            """
            )

            self.status_label = QLabel("Ready")
            self.time_label = QLabel()

            status_bar.addWidget(self.status_label)
            status_bar.addPermanentWidget(self.time_label)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()

    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize to update layout"""
        super().resizeEvent(event)
        # Notify tabs of size change
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if tab:
                handle_resize = getattr(tab, "handle_resize", None)
                if handle_resize and callable(handle_resize):
                    handle_resize(event.size())

    def get_main_style(self):
        return f"""
            QMainWindow {{
                {StyleManager.get_gradient_background()}
            }}
            {StyleManager.get_tab_style()}
        """

    def get_compact_button_style(self):
        return StyleManager.get_button_style("compact", compact=True)

    def setup_system_tray(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            app_style = self.style()
            if app_style:
                self.tray_icon.setIcon(
                    app_style.standardIcon(app_style.StandardPixmap.SP_ComputerIcon)
                )

            tray_menu = QMenu()
            show_action = QAction("Show Launcher", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)

            tray_menu.addSeparator()
            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(self.close_application)
            tray_menu.addAction(quit_action)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()

    def setup_shortcuts(self):
        self.show_shortcut = QShortcut(QKeySequence("Ctrl+Space"), self)
        self.show_shortcut.activated.connect(self.toggle_window)

        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.focus_search)

        self.command_palette_shortcut = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        self.command_palette_shortcut.activated.connect(self.show_command_palette)

    def setup_monitoring(self):
        self.process_monitor.status_update.connect(
            lambda title, status: self.dashboard_tab.update_system_status(status)
        )

        # Connect process manager signals to notifications
        if hasattr(self.process_manager, "process_started"):
            self.process_manager.process_started.connect(
                lambda name: self.notifications.show_notification(
                    f"Started {name}", "success"
                )
            )
        if hasattr(self.process_manager, "process_error"):
            self.process_manager.process_error.connect(
                lambda name, error: self.notifications.show_notification(
                    f"Error in {name}: {error[:50]}...", "error"
                )
            )

        self.process_monitor.start()

    def toggle_theme(self):
        current_theme = getattr(self.config, "theme", "dark")
        new_theme = "light" if current_theme == "dark" else "dark"

        if hasattr(self.config, "set"):
            self.config.set("theme", new_theme)

        current_style = self.styleSheet()
        if "#1a1a1a" in current_style:
            self.setStyleSheet(
                current_style.replace("#1a1a1a", "#f0f0f0").replace(
                    "#2d2d2d", "#e0e0e0"
                )
            )
            self.theme_toggle.setText("🌞")
        else:
            self.setStyleSheet(
                current_style.replace("#f0f0f0", "#1a1a1a").replace(
                    "#e0e0e0", "#2d2d2d"
                )
            )
            self.theme_toggle.setText("🌙")

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        if hasattr(self, "time_label"):
            self.time_label.setText(current_time)

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def focus_search(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            search_input = getattr(current_tab, "search_input", None)
            if search_input:
                search_input.setFocus()
                return

            for attr_name in ["apps_grid", "dev_grid", "main_apps_grid", "tools_grid"]:
                grid = getattr(current_tab, attr_name, None)
                if grid and hasattr(grid, "search_input"):
                    grid.search_input.setFocus()
                    return

    def show_command_palette(self):
        from ..data.app_definitions import AppDefinitions

        palette = CommandPalette(AppDefinitions.get_all(), self)
        palette.command_selected.connect(self.handle_command)
        palette.exec()

    def handle_command(self, action, data):
        if action == "launch_app" and data:
            self.dashboard_tab.launch_application(data)
            start_time = time.time()
            success = True  # We'll assume success for now
            launch_time = time.time() - start_time
            self.cache.record_app_launch(data.title, success, launch_time)
        elif action == "toggle_theme":
            self.toggle_theme()
        elif action == "clear_cache":
            self.cache.clear_cache()
            self.notifications.show_notification(
                "Cache cleared successfully", "success"
            )
        elif action == "minimize":
            self.hide()
        elif action == "exit":
            self.close_application()
        elif action == "show_settings":
            self.notifications.show_notification(
                "Settings dialog not implemented yet", "info"
            )

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()

    def close_application(self):
        if hasattr(self, "process_manager"):
            self.process_manager.terminate_all()
        if hasattr(self, "process_monitor"):
            self.process_monitor.stop()
            self.process_monitor.wait()
        self.close()

    def show_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec()

    def closeEvent(self, event):
        if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.close_application()
            event.accept()
