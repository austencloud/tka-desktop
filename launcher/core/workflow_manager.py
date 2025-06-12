import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class WorkflowStep:
    app_name: str
    delay_seconds: int = 0
    condition: Optional[str] = None  # "if_success", "if_failure", "always"


@dataclass
class Workflow:
    name: str
    description: str
    steps: List[WorkflowStep]
    icon: str = "⚡"


class WorkflowManager(QObject):
    workflow_started = pyqtSignal(str)
    workflow_completed = pyqtSignal(str, bool)
    step_completed = pyqtSignal(str, str, bool)

    def __init__(self, config_dir: Path, process_manager):
        super().__init__()
        self.config_dir = config_dir
        self.process_manager = process_manager
        self.workflows_file = config_dir / "workflows.json"
        self.workflows = self.load_workflows()
        self.active_workflows = {}

    def load_workflows(self) -> Dict[str, Workflow]:
        if self.workflows_file.exists():
            with open(self.workflows_file, "r") as f:
                data = json.load(f)
                workflows = {}
                for name, workflow_data in data.items():
                    steps = [WorkflowStep(**step) for step in workflow_data["steps"]]
                    workflow_data["steps"] = steps
                    workflows[name] = Workflow(**workflow_data)
                return workflows

        # Default workflows
        return {
            "dev_environment": Workflow(
                name="Development Environment",
                description="Start full development setup",
                steps=[
                    WorkflowStep("🔧 V1 Main Application", 0),
                    WorkflowStep("🧪 Run All Tests", 2, "if_success"),
                ],
            ),
            "quick_test": Workflow(
                name="Quick Test Suite",
                description="Run tests and format code",
                steps=[
                    WorkflowStep("🧪 Run All Tests", 0),
                    WorkflowStep("📝 Format Code", 1, "if_success"),
                    WorkflowStep("🔍 Lint Code", 1, "if_success"),
                ],
            ),
        }

    def save_workflows(self):
        data = {}
        for name, workflow in self.workflows.items():
            workflow_dict = asdict(workflow)
            data[name] = workflow_dict
        with open(self.workflows_file, "w") as f:
            json.dump(data, f, indent=2)

    def add_workflow(self, workflow: Workflow):
        self.workflows[workflow.name] = workflow
        self.save_workflows()

    def execute_workflow(self, workflow_name: str):
        if workflow_name not in self.workflows:
            return False

        workflow = self.workflows[workflow_name]
        self.workflow_started.emit(workflow_name)
        self.active_workflows[workflow_name] = {
            "workflow": workflow,
            "current_step": 0,
            "results": [],
        }

        self._execute_next_step(workflow_name)
        return True

    def _execute_next_step(self, workflow_name: str):
        active = self.active_workflows.get(workflow_name)
        if not active:
            return

        workflow = active["workflow"]
        current_step_idx = active["current_step"]

        if current_step_idx >= len(workflow.steps):
            # Workflow complete
            success = all(result["success"] for result in active["results"])
            self.workflow_completed.emit(workflow_name, success)
            del self.active_workflows[workflow_name]
            return

        step = workflow.steps[current_step_idx]

        # Check condition
        if step.condition and active["results"]:
            last_result = active["results"][-1]
            if step.condition == "if_success" and not last_result["success"]:
                self._skip_step(workflow_name, step)
                return
            elif step.condition == "if_failure" and last_result["success"]:
                self._skip_step(workflow_name, step)
                return

        # Execute step after delay
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(
            step.delay_seconds * 1000, lambda: self._launch_step(workflow_name, step)
        )

    def _launch_step(self, workflow_name: str, step: WorkflowStep):
        # Find app definition and launch
        from ..data.app_definitions import AppDefinitions

        apps = AppDefinitions.get_all()
        app_def = next((app for app in apps if step.app_name in app.title), None)

        if app_def:
            success = self._launch_app(app_def)
            self._record_step_result(workflow_name, step, success)
        else:
            self._record_step_result(workflow_name, step, False)

    def _skip_step(self, workflow_name: str, step: WorkflowStep):
        self._record_step_result(workflow_name, step, True, skipped=True)

    def _record_step_result(
        self, workflow_name: str, step: WorkflowStep, success: bool, skipped=False
    ):
        active = self.active_workflows.get(workflow_name)
        if not active:
            return

        active["results"].append(
            {"step": step.app_name, "success": success, "skipped": skipped}
        )
        active["current_step"] += 1

        self.step_completed.emit(workflow_name, step.app_name, success)
        self._execute_next_step(workflow_name)

    def _launch_app(self, app_def) -> bool:
        # Use process manager to launch
        if app_def.script_path:
            process = self.process_manager.launch_or_restart_app(
                app_def.title, app_def.script_path, app_def.args, app_def.env
            )
        elif app_def.command:
            process = self.process_manager.execute_command(
                app_def.command, app_def.working_dir, app_def.env
            )
        return process is not None
