from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QListWidget,
    QGridLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime
from ..components.searchable_grid import SearchableGrid
from ..components.animated_card import AnimatedCard
from ...data.app_definitions import AppDefinitions


class DashboardTab(QWidget):
    def __init__(
        self,
        recent_actions_manager,
        favorites_manager,
        process_manager=None,
        parent=None,
    ):
        super().__init__(parent)
        self.recent_actions_manager = recent_actions_manager
        self.favorites_manager = favorites_manager
        self.process_manager = process_manager
        self.setup_ui()

        if self.process_manager:
            self.process_manager.process_started.connect(
                lambda: self.update_button_states()
            )
            self.process_manager.process_finished.connect(
                lambda: self.update_button_states()
            )

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        welcome = QLabel(f"Welcome! {datetime.now().strftime('%B %d, %Y')}")
        welcome.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        welcome.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(welcome)

        content_grid = QVBoxLayout()
        content_grid.setSpacing(15)

        apps_section = self.create_apps_section()
        content_grid.addWidget(apps_section, 3)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        dev_tools_section = self.create_dev_tools_section()
        status_section = self.create_status_section()

        bottom_row.addWidget(dev_tools_section, 3)
        bottom_row.addWidget(status_section, 1)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_row)
        content_grid.addWidget(bottom_widget, 2)

        layout.addLayout(content_grid)

    def create_apps_section(self):
        apps_group = QGroupBox("🚀 Main Applications")
        apps_group.setStyleSheet(self.get_group_style())
        apps_layout = QVBoxLayout(apps_group)
        apps_layout.setContentsMargins(15, 25, 15, 15)

        apps_grid = QGridLayout()
        apps_grid.setSpacing(15)

        try:
            from ...data.app_definitions import AppDefinitions

            apps = AppDefinitions.get_by_category("applications")[:6]

            for i, app_def in enumerate(apps):
                btn = self.create_app_button(app_def)
                row = i // 3
                col = i % 3
                apps_grid.addWidget(btn, row, col)

        except Exception:
            pass

        apps_layout.addLayout(apps_grid)
        return apps_group

    def create_dev_tools_section(self):
        dev_group = QGroupBox("🛠️ Development Tools")
        dev_group.setStyleSheet(self.get_group_style())
        dev_layout = QVBoxLayout(dev_group)
        dev_layout.setContentsMargins(15, 25, 15, 15)

        dev_grid = QGridLayout()
        dev_grid.setSpacing(12)

        try:
            from ...data.app_definitions import AppDefinitions

            tools = AppDefinitions.get_by_category("dev_tools")[:4]

            for i, tool_def in enumerate(tools):
                btn = self.create_app_button(tool_def, compact=True)
                row = i // 2
                col = i % 2
                dev_grid.addWidget(btn, row, col)

        except Exception:
            pass

        dev_layout.addLayout(dev_grid)
        return dev_group

    def create_status_section(self):
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        status_layout.setSpacing(10)

        recent_group = QGroupBox("📋 Recent")
        recent_group.setStyleSheet(self.get_compact_group_style())
        recent_layout = QVBoxLayout(recent_group)
        recent_layout.setContentsMargins(10, 20, 10, 10)

        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(80)
        self.recent_list.setStyleSheet(
            """
            QListWidget {
                background: transparent;
                border: none;
                color: white;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 3px 5px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )
        recent_layout.addWidget(self.recent_list)

        system_group = QGroupBox("🖥️ System")
        system_group.setStyleSheet(self.get_compact_group_style())
        system_layout = QVBoxLayout(system_group)
        system_layout.setContentsMargins(10, 20, 10, 10)

        self.cpu_label = QLabel("CPU: Normal")
        self.memory_label = QLabel("Memory: Available")
        self.processes_label = QLabel("Processes: 0")

        for label in [self.cpu_label, self.memory_label, self.processes_label]:
            label.setStyleSheet("color: white; font-size: 11px; padding: 2px;")
            system_layout.addWidget(label)

        status_layout.addWidget(recent_group)
        status_layout.addWidget(system_group)
        return status_widget

    def create_app_button(self, app_def, compact=False):
        btn = QPushButton()

        if compact:
            btn.setMinimumSize(180, 80)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        else:
            btn.setMinimumSize(220, 95)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        btn.setText(f"{app_def.icon}\n{app_def.title}")
        btn.setToolTip(app_def.description)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btn.setStyleSheet(
            f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12), 
                    stop:0.5 rgba(102, 126, 234, 0.1), 
                    stop:1 rgba(118, 75, 162, 0.1));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: {'15px' if compact else '18px'};
                color: white;
                font-size: {'12px' if compact else '14px'};
                font-weight: 700;
                text-align: center;
                padding: {'8px' if compact else '12px'};
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.4), 
                    stop:0.5 rgba(118, 75, 162, 0.35), 
                    stop:1 rgba(102, 126, 234, 0.4));
                border: 2px solid rgba(255, 255, 255, 0.6);
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.7), 
                    stop:1 rgba(118, 75, 162, 0.7));
                border: 2px solid rgba(255, 255, 255, 0.8);
            }}
        """
        )

        btn.clicked.connect(lambda: self.launch_application(app_def))
        return btn

    def launch_application(self, app_def):
        if not self.process_manager:
            return

        self.recent_actions_manager.add_action(app_def.title)

        if app_def.script_path:
            process = self.process_manager.launch_or_restart_app(
                app_def.title, app_def.script_path, app_def.args, app_def.env
            )
        elif app_def.command:
            process = self.process_manager.execute_command(
                app_def.command, app_def.working_dir, app_def.env
            )

        if not process:
            print(f"Failed to launch {app_def.title}")
        else:
            self.update_button_states()

    def update_recent_actions(self):
        self.recent_list.clear()
        items = self.recent_actions_manager.create_list_items()[:3]  # Show only last 3
        for item in items:
            self.recent_list.addItem(item)

    def update_system_status(self, status):
        self.cpu_label.setText(f"CPU: {status.get('cpu', 'Unknown')}")
        self.memory_label.setText(f"Memory: {status.get('memory', 'Unknown')}")
        self.processes_label.setText(f"Processes: {status.get('active_processes', 0)}")

    def update_button_states(self):
        layout = self.layout()
        if not layout:
            return

        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QWidget):
                    self._update_buttons_in_widget(widget)

    def _update_buttons_in_widget(self, widget):
        for child in widget.findChildren(QPushButton):
            button_text = child.text()
            if "\n" in button_text:
                app_title = button_text.split("\n")[1]
                if self.process_manager and self.process_manager.is_app_running(
                    app_title
                ):
                    child.setStyleSheet(self._get_running_button_style(child))
                    child.setToolTip(f"{app_title} (Running - Click to restart)")
                else:
                    child.setStyleSheet(self._get_default_button_style(child))
                    child.setToolTip(f"{app_title} (Stopped - Click to start)")

    def _get_running_button_style(self, btn):
        compact = btn.minimumHeight() < 90
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.3), 
                    stop:0.5 rgba(39, 174, 96, 0.25), 
                    stop:1 rgba(46, 204, 113, 0.3));
                border: 2px solid rgba(46, 204, 113, 0.6);
                border-radius: {'15px' if compact else '18px'};
                color: white;
                font-size: {'12px' if compact else '14px'};
                font-weight: 700;
                text-align: center;
                padding: {'8px' if compact else '12px'};
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 0.4), 
                    stop:0.5 rgba(192, 57, 43, 0.35), 
                    stop:1 rgba(231, 76, 60, 0.4));
                border: 2px solid rgba(231, 76, 60, 0.8);
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 0.7), 
                    stop:1 rgba(192, 57, 43, 0.7));
                border: 2px solid rgba(231, 76, 60, 1.0);
            }}
        """

    def _get_default_button_style(self, btn):
        compact = btn.minimumHeight() < 90
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12), 
                    stop:0.5 rgba(102, 126, 234, 0.1), 
                    stop:1 rgba(118, 75, 162, 0.1));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: {'15px' if compact else '18px'};
                color: white;
                font-size: {'12px' if compact else '14px'};
                font-weight: 700;
                text-align: center;
                padding: {'8px' if compact else '12px'};
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.4), 
                    stop:0.5 rgba(118, 75, 162, 0.35), 
                    stop:1 rgba(102, 126, 234, 0.4));
                border: 2px solid rgba(255, 255, 255, 0.6);
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.7), 
                    stop:1 rgba(118, 75, 162, 0.7));
                border: 2px solid rgba(255, 255, 255, 0.8);
            }}
        """

    def get_group_style(self):
        return """
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08), 
                    stop:1 rgba(255, 255, 255, 0.04));
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                font-weight: 600;
                font-size: 13px;
                color: white;
                padding-top: 8px;
                margin-top: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: rgba(255, 255, 255, 0.9);
            }
        """

    def get_compact_group_style(self):
        return """
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.06), 
                    stop:1 rgba(255, 255, 255, 0.03));
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                color: white;
                padding-top: 6px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 8px;
                color: rgba(255, 255, 255, 0.8);
            }
        """

    def handle_resize(self, size):
        pass
