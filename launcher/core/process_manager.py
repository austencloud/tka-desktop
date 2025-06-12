from PyQt6.QtCore import QProcess, pyqtSignal, QObject
from PyQt6.QtWidgets import QMessageBox
from pathlib import Path
from typing import List, Dict, Optional, Union, Callable
import os


class ProcessManager(QObject):
    process_started = pyqtSignal(str)
    process_finished = pyqtSignal(str, int)
    process_output = pyqtSignal(str, str)
    process_error = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.processes: List[QProcess] = []
        self.process_callbacks: Dict[QProcess, Callable] = {}
        self.app_processes: Dict[str, QProcess] = {}

    def execute_command(
        self,
        command: Union[List[str], str],
        working_dir: str = "",
        env: Optional[Dict[str, str]] = None,
        callback: Optional[Callable] = None,
    ) -> Optional[QProcess]:
        process = QProcess(self)

        process.finished.connect(
            lambda exit_code, exit_status: self._on_process_finished(
                process, exit_code, exit_status
            )
        )
        process.readyReadStandardOutput.connect(lambda: self._on_stdout_ready(process))
        process.readyReadStandardError.connect(lambda: self._on_stderr_ready(process))

        if working_dir:
            abs_working_dir = os.path.abspath(working_dir)
            if os.path.exists(abs_working_dir):
                process.setWorkingDirectory(abs_working_dir)
            else:
                self.process_error.emit(
                    "Process Manager",
                    f"Working directory not found: {abs_working_dir}",
                )
                return None
        else:
            process.setWorkingDirectory(os.getcwd())

        process_env = process.processEnvironment()
        process_env.insert("PYTHONIOENCODING", "utf-8")
        if env:
            for key, value in env.items():
                process_env.insert(key, value)
        process.setProcessEnvironment(process_env)

        if callback:
            self.process_callbacks[process] = callback

        try:
            if isinstance(command, list):
                program = command[0]
                arguments = command[1:]
                self.process_started.emit(f"{program} {' '.join(arguments)}")
                process.start(program, arguments)
            else:
                self.process_started.emit(command)
                process.start("cmd", ["/c", command])

            self.processes.append(process)
            return process

        except Exception as e:
            self.process_error.emit("Process Manager", f"Failed to start process: {e}")
            return None

    def execute_python_script(
        self,
        script_path: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        callback: Optional[Callable] = None,
    ) -> Optional[QProcess]:
        abs_script_path = os.path.abspath(script_path)

        if not os.path.exists(abs_script_path):
            self.process_error.emit(
                "Process Manager", f"Script not found: {abs_script_path}"
            )
            return None

        cmd = ["python", abs_script_path]
        if args:
            cmd.extend(args)

        working_dir = os.path.dirname(abs_script_path)
        return self.execute_command(cmd, working_dir, env, callback)

    def terminate_all(self):
        for process in self.processes[:]:
            if process.state() != QProcess.ProcessState.NotRunning:
                process.terminate()
                if not process.waitForFinished(3000):
                    process.kill()

    def get_active_processes(self) -> List[QProcess]:
        return [
            p for p in self.processes if p.state() != QProcess.ProcessState.NotRunning
        ]

    def launch_or_restart_app(
        self,
        app_name: str,
        script_path: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
    ) -> Optional[QProcess]:
        if app_name in self.app_processes:
            existing_process = self.app_processes[app_name]
            if existing_process.state() != QProcess.ProcessState.NotRunning:
                self._safely_terminate_process(existing_process, app_name)

        process = self.execute_python_script(script_path, args, env)
        if process:
            self.app_processes[app_name] = process
        return process

    def _safely_terminate_process(self, process: QProcess, app_name: str) -> None:
        """Safely terminate a process without affecting the launcher."""
        try:
            # First, disconnect all signals to prevent interference
            process.finished.disconnect()
            process.readyReadStandardOutput.disconnect()
            process.readyReadStandardError.disconnect()

            # Remove from tracking immediately
            if app_name in self.app_processes:
                del self.app_processes[app_name]

            if process in self.processes:
                self.processes.remove(process)

            # Clean termination attempt
            if process.state() != QProcess.ProcessState.NotRunning:
                process.terminate()

                # Give it time to close gracefully
                if not process.waitForFinished(3000):
                    process.kill()
                    process.waitForFinished(1000)

        except Exception as e:
            # If anything goes wrong, force kill and continue
            try:
                process.kill()
                process.waitForFinished(1000)
            except:
                pass

    def is_app_running(self, app_name: str) -> bool:
        if app_name not in self.app_processes:
            return False
        process = self.app_processes[app_name]
        return process.state() != QProcess.ProcessState.NotRunning

    def get_app_status(self, app_name: str) -> str:
        if not self.is_app_running(app_name):
            return "Stopped"
        return "Running"

    def _on_process_finished(self, process: QProcess, exit_code: int, exit_status):
        if process in self.processes:
            self.processes.remove(process)

        if process in self.process_callbacks:
            callback = self.process_callbacks.pop(process)
            if callback is not None:
                callback(exit_code)

        cmd_name = process.program() if hasattr(process, "program") else "Process"
        self.process_finished.emit(cmd_name, exit_code)

        if exit_code != 0:
            stderr_data = (
                process.readAllStandardError().data().decode("utf-8", errors="ignore")
            )
            if stderr_data:
                self.process_error.emit(cmd_name, stderr_data)

        for app_name, app_process in list(self.app_processes.items()):
            if app_process == process:
                del self.app_processes[app_name]
                break

    def _on_stdout_ready(self, process: QProcess):
        data = process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        if data.strip():
            cmd_name = process.program() if hasattr(process, "program") else "Process"
            self.process_output.emit(cmd_name, data.strip())

    def _on_stderr_ready(self, process: QProcess):
        data = process.readAllStandardError().data().decode("utf-8", errors="ignore")
        if data.strip():
            cmd_name = process.program() if hasattr(process, "program") else "Process"

            # Filter out informational logging that shouldn't be treated as errors
            if self._is_informational_message(data):
                self.process_output.emit(
                    cmd_name, data.strip()
                )  # Treat as normal output
            else:
                self.process_error.emit(cmd_name, data.strip())

    def _is_informational_message(self, message: str) -> bool:
        """Check if stderr message is informational rather than an actual error."""
        info_patterns = [
            "- INFO -",
            "Starting",
            "Initialized",
            "Loading",
            "Created",
            "version",
            "Python 3.",
            "Qt version",
            "Application started",
        ]

        error_patterns = [
            "ERROR",
            "CRITICAL",
            "Exception",
            "Traceback",
            "Failed",
            "could not",
            "cannot",
            "No such file",
        ]

        message_lower = message.lower()

        # If it contains clear error indicators, it's an error
        if any(pattern.lower() in message_lower for pattern in error_patterns):
            return False

        # If it contains info indicators, it's informational
        if any(pattern.lower() in message_lower for pattern in info_patterns):
            return True

        # Default: treat as error to be safe
        return False
