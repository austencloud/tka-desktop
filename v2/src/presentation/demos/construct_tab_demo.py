from typing import Optional
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.dependency_injection.di_container import (
    DIContainer,
    get_container,
)
from src.core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from src.application.services.simple_layout_service import SimpleLayoutService
from src.application.services.simple_sequence_service import (
    SequenceService,
    SimpleSequenceDataService,
    SimpleSettingsService,
    SimpleValidationService,
)
from src.presentation.factories.workbench_factory import configure_workbench_services
from src.domain.models.core_models import SequenceData
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget


class ConstructTabDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 Kinetic Constructor v2 - Construct Tab")
        self.setMinimumSize(1400, 900)

        self.container = get_container()
        self._configure_services()
        self._setup_ui()

    def _configure_services(self):
        self.container.register_singleton(ILayoutService, SimpleLayoutService)
        self.container.register_singleton(ISettingsService, SimpleSettingsService)
        self.container.register_singleton(
            ISequenceDataService, SimpleSequenceDataService
        )
        self.container.register_singleton(IValidationService, SimpleValidationService)
        self.container.register_singleton(SequenceService, SequenceService)
        configure_workbench_services(self.container)

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        title = QLabel("🔧 Kinetic Constructor v2 - Construct Tab")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title)

        desc = QLabel(
            "Modern implementation of the Construct tab with legacy layout:\n"
            "• Left: Sequence Workbench (2/3 width) • Right: Start Position + Option Pickers (1/3 width)\n"
            "• Zero technical debt • Clean dependency injection • Modular architecture"
        )
        desc.setStyleSheet(
            """
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #2196f3;
                border-radius: 5px;
                padding: 10px;
                margin: 10px 0;
                color: #1976d2;
            }
        """
        )
        layout.addWidget(desc)

        self.construct_tab = ConstructTabWidget(self.container)
        self.construct_tab.sequence_created.connect(self._on_sequence_created)
        self.construct_tab.sequence_modified.connect(self._on_sequence_modified)
        layout.addWidget(self.construct_tab)

        self.status_label = QLabel("Ready - Select a start position to begin")
        self.status_label.setStyleSheet(
            """
            QLabel {
                background-color: #f1f8e9;
                border: 1px solid #4caf50;
                border-radius: 3px;
                padding: 8px;
                color: #388e3c;
            }
        """
        )
        layout.addWidget(self.status_label)

    def _on_sequence_created(self, sequence: SequenceData):
        self.status_label.setText(f"✅ New sequence created: {sequence.length} beats")

    def _on_sequence_modified(self, sequence: SequenceData):
        self.status_label.setText(f"🔄 Sequence modified: {sequence.length} beats")
