"""
Enhanced tab switcher that supports both internal and external tab launching.

This extends the existing tab switcher to provide options for running tabs
as separate processes while maintaining the existing internal functionality.
"""

import subprocess
import sys
import os
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QMenu, QAction
from PyQt6.QtCore import QProcess, pyqtSignal
from PyQt6.QtGui import QIcon

from main_window.main_widget.main_widget_tab_switcher import MainWidgetTabSwitcher
from main_window.main_widget.tab_name import TabName

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from core.application_context import ApplicationContext


class ExternalTabProcess:
    """Manages an external tab process."""

    def __init__(self, tab_name: str, process: QProcess):
        self.tab_name = tab_name
        self.process = process
        self.is_running = True

        # Connect process signals
        self.process.finished.connect(self._on_finished)
        self.process.errorOccurred.connect(self._on_error)

    def _on_finished(self, exit_code: int):
        """Handle process completion."""
        self.is_running = False
        print(f"External {self.tab_name} tab process finished with code {exit_code}")

    def _on_error(self, error):
        """Handle process error."""
        self.is_running = False
        print(f"External {self.tab_name} tab process error: {error}")

    def terminate(self):
        """Terminate the external process."""
        if self.is_running and self.process.state() == QProcess.ProcessState.Running:
            self.process.terminate()
            if not self.process.waitForFinished(3000):  # Wait 3 seconds
                self.process.kill()


class EnhancedTabSwitcher(MainWidgetTabSwitcher):
    """
    Enhanced tab switcher with external process support.

    This extends the existing tab switcher to provide:
    - Right-click context menu for external launching
    - Process management for external tabs
    - Seamless integration with existing functionality
    """

    # Signal emitted when external tab is launched
    external_tab_launched = pyqtSignal(str)  # tab_name

    def __init__(
        self, main_widget: "MainWidget", app_context: "ApplicationContext" = None
    ):
        super().__init__(main_widget, app_context)

        # Track external processes
        self.external_processes: dict[str, ExternalTabProcess] = {}

        # Get project root for launching standalone tabs
        self.project_root = self._get_project_root()

    def _get_project_root(self) -> str:
        """Get the project root directory."""
        # Start from this file and go up to find the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while current_dir != os.path.dirname(current_dir):  # Not at filesystem root
            if os.path.exists(os.path.join(current_dir, "src", "main.py")):
                return current_dir
            current_dir = os.path.dirname(current_dir)

        # Fallback: assume we're in src/main_window/main_widget
        return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    def create_tab_context_menu(self, tab_name: TabName) -> QMenu:
        """
        Create a context menu for tab operations.

        Args:
            tab_name: The tab to create menu for

        Returns:
            QMenu with tab operations
        """
        menu = QMenu(f"{tab_name.value.title()} Tab Options")

        # Internal switch action (default behavior)
        switch_action = QAction(f"Switch to {tab_name.value.title()}", menu)
        switch_action.triggered.connect(lambda: self.switch_to_tab(tab_name))
        menu.addAction(switch_action)

        menu.addSeparator()

        # External launch action
        external_action = QAction(f"Open {tab_name.value.title()} in New Window", menu)
        external_action.triggered.connect(lambda: self.launch_tab_externally(tab_name))
        menu.addAction(external_action)

        # If external process is running, add terminate option
        if tab_name.value in self.external_processes:
            process_info = self.external_processes[tab_name.value]
            if process_info.is_running:
                menu.addSeparator()
                terminate_action = QAction(
                    f"Close External {tab_name.value.title()}", menu
                )
                terminate_action.triggered.connect(
                    lambda: self.terminate_external_tab(tab_name)
                )
                menu.addAction(terminate_action)

        return menu

    def launch_tab_externally(self, tab_name: TabName) -> bool:
        """
        Launch a tab as an external process.

        Args:
            tab_name: The tab to launch externally

        Returns:
            True if launch was successful, False otherwise
        """
        try:
            # Check if already running externally
            if tab_name.value in self.external_processes:
                process_info = self.external_processes[tab_name.value]
                if process_info.is_running:
                    print(f"External {tab_name.value} tab is already running")
                    return False

            # Create the command to launch the standalone tab
            launcher_path = os.path.join(
                self.project_root, "src", "standalone", "launcher.py"
            )

            if not os.path.exists(launcher_path):
                print(f"Launcher not found at {launcher_path}")
                return False

            # Create QProcess for better integration with Qt
            process = QProcess()

            # Set working directory to project root
            process.setWorkingDirectory(self.project_root)

            # Prepare command
            python_executable = sys.executable
            args = [launcher_path, tab_name.value]

            print(
                f"Launching external {tab_name.value} tab: {python_executable} {' '.join(args)}"
            )

            # Start the process
            process.start(python_executable, args)

            if not process.waitForStarted(5000):  # Wait 5 seconds for start
                print(f"Failed to start external {tab_name.value} tab")
                return False

            # Track the process
            self.external_processes[tab_name.value] = ExternalTabProcess(
                tab_name.value, process
            )

            # Emit signal
            self.external_tab_launched.emit(tab_name.value)

            print(f"Successfully launched external {tab_name.value} tab")
            return True

        except Exception as e:
            print(f"Error launching external {tab_name.value} tab: {e}")
            return False

    def terminate_external_tab(self, tab_name: TabName) -> bool:
        """
        Terminate an external tab process.

        Args:
            tab_name: The tab to terminate

        Returns:
            True if termination was successful, False otherwise
        """
        if tab_name.value not in self.external_processes:
            return False

        try:
            process_info = self.external_processes[tab_name.value]
            process_info.terminate()

            # Remove from tracking
            del self.external_processes[tab_name.value]

            print(f"Terminated external {tab_name.value} tab")
            return True

        except Exception as e:
            print(f"Error terminating external {tab_name.value} tab: {e}")
            return False

    def cleanup_external_processes(self):
        """Clean up all external processes on application shutdown."""
        for tab_name in list(self.external_processes.keys()):
            self.terminate_external_tab(TabName(tab_name))

    def get_external_tab_status(self, tab_name: TabName) -> Optional[str]:
        """
        Get the status of an external tab.

        Args:
            tab_name: The tab to check

        Returns:
            Status string or None if not running externally
        """
        if tab_name.value not in self.external_processes:
            return None

        process_info = self.external_processes[tab_name.value]
        if process_info.is_running:
            return "running"
        else:
            return "terminated"
