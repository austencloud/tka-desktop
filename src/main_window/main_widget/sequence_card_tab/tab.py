# src/main_window/main_widget/sequence_card_tab/tab.py
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, QTimer
from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from .content_area import SequenceCardContentArea
from .header import SequenceCardHeader
from .initializer import USE_PRINTABLE_LAYOUT, SequenceCardInitializer
from .resource_manager import SequenceCardResourceManager
from .settings_handler import SequenceCardSettingsHandler
from .components.navigation.sidebar import SequenceCardNavSidebar
from .components.pages.factory import SequenceCardPageFactory
from .core.refresher import SequenceCardRefresher
from .components.pages.printable_factory import PrintablePageFactory
from .components.pages.printable_layout import PaperSize, PaperOrientation
from .export.image_exporter import SequenceCardImageExporter
from .export.page_exporter import SequenceCardPageExporter
from .components.display.printable_displayer import PrintableDisplayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceCardTab(QWidget):
    def __init__(
        self,
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.global_settings = settings_manager.get_global_settings()

        self.pages = []
        self.initialized = False
        self.currently_displayed_length = 16
        self.is_initializing = False
        self.load_start_time = 0

        self.settings_manager_obj = SequenceCardSettingsHandler(settings_manager)
        self.resource_manager = SequenceCardResourceManager(self)
        self.initializer = SequenceCardInitializer(self)
        self.content_area = SequenceCardContentArea(self)

        self._create_components()
        self.init_ui()

    def _create_components(self):
        self.nav_sidebar = SequenceCardNavSidebar(self)

        if hasattr(self.settings_manager_obj, "saved_length"):
            self.nav_sidebar.selected_length = self.settings_manager_obj.saved_length

        if USE_PRINTABLE_LAYOUT:
            self.page_factory = PrintablePageFactory(self)
        else:
            self.page_factory = SequenceCardPageFactory(self)

        if USE_PRINTABLE_LAYOUT:
            self.printable_displayer = PrintableDisplayer(self)
            self.printable_displayer.set_paper_size(PaperSize.A4)
            self.printable_displayer.set_orientation(PaperOrientation.PORTRAIT)

            if hasattr(self.settings_manager_obj, "saved_column_count"):
                self.printable_displayer.columns_per_row = (
                    self.settings_manager_obj.saved_column_count
                )

        self.image_exporter = SequenceCardImageExporter(self)
        self.page_exporter = SequenceCardPageExporter(self)
        self.refresher = SequenceCardRefresher(self)
        self.pages = []

    def init_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.header = SequenceCardHeader(self)
        self.layout.addWidget(self.header)

        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)

        sidebar_width = 200
        self.nav_sidebar.setFixedWidth(sidebar_width)
        self.nav_sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        self.content_layout.addWidget(self.nav_sidebar, 0)
        self.content_layout.addWidget(self.content_area.scroll_area, 1)

        self.layout.addLayout(self.content_layout, 1)

        if hasattr(self.nav_sidebar, "length_selected"):
            self.nav_sidebar.length_selected.connect(self._on_length_selected)

    def update_column_count(self, column_count: int):
        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            self.printable_displayer.set_columns_per_row(column_count)

    def _on_length_selected(self, length: int):
        self.currently_displayed_length = length
        self.settings_manager_obj.save_length(length)

        if self.is_initializing:
            return

        self.content_area.clear_layout()
        self.header.description_label.setText(
            f"Loading {length if length > 0 else 'all'}-step sequences..."
        )

        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            if (
                hasattr(self.printable_displayer, "manager")
                and self.printable_displayer.manager.is_loading
            ):
                logging.debug(
                    f"Cancelling in-progress loading operation before loading length {length}"
                )
                self.printable_displayer.manager.cancel_loading()

            self.printable_displayer.display_sequences(length)
            self._sync_pages_from_displayer()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            self.initialized = True
            self.setCursor(Qt.CursorShape.WaitCursor)
            QTimer.singleShot(50, self.initializer.initialize_content)

    def load_sequences(self):
        selected_length = self.nav_sidebar.selected_length
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"
        self.header.description_label.setText(f"Loading {length_text} sequences...")
        QApplication.processEvents()

        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            self.printable_displayer.display_sequences(selected_length)
            self._sync_pages_from_displayer()
        else:
            pass

    def regenerate_all_images(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        original_text = self.header.description_label.text()
        self.header.description_label.setText("Regenerating images... Please wait")
        QApplication.processEvents()

        try:
            if hasattr(self.image_exporter, "export_all_images"):
                self.image_exporter.export_all_images()

            selected_length = self.nav_sidebar.selected_length

            if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
                self.printable_displayer.display_sequences(selected_length)
                self._sync_pages_from_displayer()

            self.header.description_label.setText("Images regenerated successfully!")
            QTimer.singleShot(
                3000, lambda: self.header.description_label.setText(original_text)
            )

        except Exception as e:
            self.header.description_label.setText(f"Error regenerating: {str(e)}")
            QTimer.singleShot(
                5000, lambda: self.header.description_label.setText(original_text)
            )
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _sync_pages_from_displayer(self):
        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            if hasattr(self.printable_displayer, "pages"):
                self.pages = self.printable_displayer.pages
            elif hasattr(self.printable_displayer, "manager") and hasattr(
                self.printable_displayer.manager, "pages"
            ):
                self.pages = self.printable_displayer.manager.pages

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.initialized and hasattr(self.nav_sidebar, "selected_length"):
            QTimer.singleShot(300, self.load_sequences)

    def on_scroll_area_resize(self):
        if self.resource_manager.resize_timer.isActive():
            self.resource_manager.resize_timer.stop()
        self.resource_manager.resize_timer.start(250)

    def refresh_layout_after_resize(self):
        if not self.initialized or not hasattr(self.nav_sidebar, "selected_length"):
            return

        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            logging.debug("Refreshing layout after resize")
            self.printable_displayer.refresh_layout()
            self._sync_pages_from_displayer()

    def cleanup(self):
        self.resource_manager.cleanup()

    def closeEvent(self, event):
        self.cleanup()
        super().closeEvent(event)
