from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QTextEdit,
)


class MonitorTab(QWidget):
    def __init__(self, process_manager, parent=None):
        super().__init__(parent)
        self.process_manager = process_manager
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 5)

        main_layout = QHBoxLayout()

        process_group = QGroupBox("🔄 Running Processes")
        process_group.setStyleSheet(self.get_group_style())
        process_layout = QVBoxLayout(process_group)

        self.process_list = QListWidget()
        self.process_list.setStyleSheet(
            """
            QListWidget {
                background: transparent;
                border: none;
                color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """
        )
        process_layout.addWidget(self.process_list)

        console_group = QGroupBox("📝 Console Output")
        console_group.setStyleSheet(self.get_group_style())
        console_layout = QVBoxLayout(console_group)

        self.console_output = QTextEdit()
        self.console_output.setStyleSheet(
            """
            QTextEdit {
                background: #1e1e1e;
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """
        )
        self.console_output.setReadOnly(True)
        console_layout.addWidget(self.console_output)

        main_layout.addWidget(process_group)
        main_layout.addWidget(console_group)
        layout.addLayout(main_layout)

    def connect_signals(self):
        self.process_manager.process_started.connect(self.log_message)
        self.process_manager.process_finished.connect(self.on_process_finished)
        self.process_manager.process_output.connect(self.on_process_output)
        self.process_manager.process_error.connect(self.on_process_error)

    def update_process_list(self):
        self.process_list.clear()
        for i, process in enumerate(self.process_manager.get_active_processes()):
            status = (
                "Running"
                if process.state() == process.ProcessState.Running
                else "Starting"
            )
            self.process_list.addItem(f"Process {i+1}: {status}")

    def log_message(self, message: str):
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_output.append(f"[{timestamp}] {message}")

    def on_process_finished(self, name: str, exit_code: int):
        self.update_process_list()
        if exit_code == 0:
            self.log_message(f"{name} completed successfully")
        else:
            self.log_message(f"{name} failed with exit code {exit_code}")

    def on_process_output(self, name: str, output: str):
        self.log_message(f"Output from {name}: {output}")

    def on_process_error(self, name: str, error: str):
        self.log_message(f"Error from {name}: {error}")

    def get_group_style(self):
        return """
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                margin: 2px;
                padding-top: 15px;
                font-weight: bold;
                font-size: 12px;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                background: rgba(26, 26, 26, 0.9);
                border-radius: 4px;
            }
        """

    def handle_resize(self, size):
        """Handle parent resize events"""
        pass
