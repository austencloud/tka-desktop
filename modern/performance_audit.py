"""
Performance Audit Tool for Modern Application

Comprehensive profiling tool to measure startup performance and start position
selection workflow. Provides detailed timing analysis to identify bottlenecks.
"""

import time
import cProfile
import pstats
import io
import functools
import sys
from pathlib import Path
from typing import Dict, List, Callable, Any
from contextlib import contextmanager
import traceback

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class PerformanceProfiler:
    """Detailed performance profiler for Modern application."""

    def __init__(self):
        self.timing_data: Dict[str, List[float]] = {}
        self.call_stack: List[str] = []
        self.detailed_logs: List[str] = []

    def log(self, message: str):
        """Log a detailed message with timestamp."""
        timestamp = time.perf_counter()
        self.detailed_logs.append(f"[{timestamp:.6f}] {message}")
        print(f"[{timestamp:.6f}] {message}")

    @contextmanager
    def time_operation(self, operation_name: str):
        """Context manager to time an operation."""
        start_time = time.perf_counter()
        self.call_stack.append(operation_name)
        self.log(f"START: {operation_name}")

        try:
            yield
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time

            if operation_name not in self.timing_data:
                self.timing_data[operation_name] = []
            self.timing_data[operation_name].append(duration)

            self.call_stack.pop()
            self.log(f"END: {operation_name} - Duration: {duration:.6f}s")

    def time_function(self, func_name: str = None):
        """Decorator to time function execution."""

        def decorator(func):
            name = func_name or f"{func.__module__}.{func.__name__}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with self.time_operation(name):
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def generate_report(self) -> str:
        """Generate comprehensive performance report."""
        report = []
        report.append("=" * 80)
        report.append("PERFORMANCE AUDIT REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary of all operations
        report.append("OPERATION TIMING SUMMARY:")
        report.append("-" * 40)

        sorted_operations = sorted(
            self.timing_data.items(), key=lambda x: max(x[1]), reverse=True
        )

        for operation, times in sorted_operations:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            total_time = sum(times)

            report.append(f"{operation}:")
            report.append(f"  Calls: {len(times)}")
            report.append(f"  Total: {total_time:.6f}s")
            report.append(f"  Average: {avg_time:.6f}s")
            report.append(f"  Min: {min_time:.6f}s")
            report.append(f"  Max: {max_time:.6f}s")
            report.append("")

        # Top bottlenecks
        report.append("TOP 5 PERFORMANCE BOTTLENECKS:")
        report.append("-" * 40)

        for i, (operation, times) in enumerate(sorted_operations[:5]):
            max_time = max(times)
            report.append(f"{i+1}. {operation}: {max_time:.6f}s")

        report.append("")
        report.append("DETAILED EXECUTION LOG:")
        report.append("-" * 40)
        for log_entry in self.detailed_logs:
            report.append(log_entry)

        return "\n".join(report)


def profile_application_startup():
    """Profile the complete application startup sequence."""
    profiler = PerformanceProfiler()

    try:
        with profiler.time_operation("Total Application Startup"):
            profiler.log("Starting application startup profiling...")

            # Import and setup
            with profiler.time_operation("Module Imports"):
                from PyQt6.QtWidgets import QApplication
                from main import KineticConstructorModern
                from core.dependency_injection.di_container import DIContainer
                from core.events import get_event_bus, reset_event_bus

            # QApplication creation
            with profiler.time_operation("QApplication Creation"):
                app = QApplication([])

            # Event bus initialization
            with profiler.time_operation("Event Bus Initialization"):
                reset_event_bus()
                event_bus = get_event_bus()

            # DI Container creation
            with profiler.time_operation("DI Container Creation"):
                container = DIContainer()

            # Main window creation
            with profiler.time_operation("Main Window Creation"):
                main_window = KineticConstructorModern()

            # Service registration (if accessible)
            try:
                with profiler.time_operation("Service Registration"):
                    # Try to access service registration methods
                    if hasattr(main_window, "_register_services"):
                        main_window._register_services()
                    elif hasattr(main_window, "_setup_services"):
                        main_window._setup_services()
            except Exception as e:
                profiler.log(f"Service registration profiling failed: {e}")

            # UI initialization
            with profiler.time_operation("UI Initialization"):
                # Try to access UI setup methods
                if hasattr(main_window, "_setup_ui"):
                    main_window._setup_ui()
                elif hasattr(main_window, "setupUi"):
                    main_window.setupUi()

            profiler.log("Application startup profiling completed")

            # Clean up
            app.quit()

    except Exception as e:
        profiler.log(f"Error during startup profiling: {e}")
        traceback.print_exc()

    return profiler


def profile_start_position_picker():
    """Profile start position picker initialization and population."""
    profiler = PerformanceProfiler()

    try:
        with profiler.time_operation("Start Position Picker Detailed Profiling"):
            profiler.log("Starting detailed start position picker profiling...")

            # Import required modules
            with profiler.time_operation("Start Position Imports"):
                from PyQt6.QtWidgets import QApplication
                from presentation.components.start_position_picker.start_position_picker import (
                    StartPositionPicker,
                    StartPositionOption,
                )
                from application.services.data.pictograph_dataset_service import (
                    PictographDatasetService,
                )

            # Create minimal app
            with profiler.time_operation("QApplication Setup"):
                app = QApplication([])

            # Profile dataset service initialization (this seems to be a bottleneck)
            with profiler.time_operation("Dataset Service Initialization"):
                dataset_service = PictographDatasetService()
                profiler.log(f"Dataset service created: {type(dataset_service)}")

            # Profile start position picker creation
            with profiler.time_operation("Start Position Picker Creation"):
                picker = StartPositionPicker()
                profiler.log(f"Start position picker created: {type(picker)}")

            # Profile individual start position option creation
            with profiler.time_operation("Individual Start Position Option Creation"):
                # Test creating a single option to see the cost
                option = StartPositionOption("alpha1_alpha1", "diamond")
                profiler.log(f"Single start position option created: {type(option)}")

            # Profile the _load_start_positions method specifically
            with profiler.time_operation("Load Start Positions Method"):
                picker._load_start_positions()
                profiler.log("Start positions loaded")

            # Profile grid mode switching
            with profiler.time_operation("Grid Mode Switch"):
                picker.set_grid_mode("box")
                profiler.log("Grid mode switched to box")

            app.quit()

    except Exception as e:
        profiler.log(f"Error during start position picker profiling: {e}")
        traceback.print_exc()

    return profiler


def profile_start_position_transition():
    """Profile the start position selection to option picker transition."""
    profiler = PerformanceProfiler()

    try:
        with profiler.time_operation("Start Position Transition Profiling"):
            profiler.log("Starting start position transition profiling...")

            # Import required modules
            with profiler.time_operation("Transition Imports"):
                from PyQt6.QtWidgets import QApplication
                from presentation.tabs.construct.layout_manager import (
                    ConstructTabLayoutManager,
                )
                from presentation.components.start_position_picker.start_position_picker import (
                    StartPositionPicker,
                )

            # Create minimal app
            with profiler.time_operation("QApplication Setup"):
                app = QApplication([])

            # Profile layout manager creation (contains both pickers)
            with profiler.time_operation("Layout Manager Creation"):
                layout_manager = ConstructTabLayoutManager()
                profiler.log(f"Layout manager created: {type(layout_manager)}")

            # Profile start position selection simulation
            with profiler.time_operation("Start Position Selection Simulation"):
                # Simulate selecting a start position
                if hasattr(layout_manager, "start_position_picker"):
                    picker = layout_manager.start_position_picker
                    profiler.log("Found start position picker in layout manager")

                    # Profile the selection handler
                    with profiler.time_operation("Selection Handler"):
                        if hasattr(layout_manager, "_handle_start_position_selection"):
                            layout_manager._handle_start_position_selection(
                                "alpha1_alpha1"
                            )
                        elif hasattr(layout_manager, "handle_start_position_selected"):
                            layout_manager.handle_start_position_selected(
                                "alpha1_alpha1"
                            )
                        profiler.log("Start position selection handled")

                else:
                    profiler.log("Start position picker not found in layout manager")

            # Profile option picker initialization
            with profiler.time_operation("Option Picker Initialization"):
                # Check if option picker gets initialized during transition
                if hasattr(layout_manager, "option_picker"):
                    profiler.log("Option picker found")
                elif hasattr(layout_manager, "picker_stack"):
                    profiler.log("Picker stack found - checking for option picker")

            app.quit()

    except Exception as e:
        profiler.log(f"Error during start position transition profiling: {e}")
        traceback.print_exc()

    return profiler


def run_comprehensive_audit():
    """Run the complete performance audit."""
    print("Starting Comprehensive Performance Audit...")
    print("=" * 60)

    # Profile application startup
    print("\n1. PROFILING APPLICATION STARTUP...")
    startup_profiler = profile_application_startup()

    # Profile start position picker
    print("\n2. PROFILING START POSITION PICKER...")
    picker_profiler = profile_start_position_picker()

    # Profile start position transition
    print("\n3. PROFILING START POSITION TRANSITION...")
    transition_profiler = profile_start_position_transition()

    # Generate combined report
    print("\n4. GENERATING PERFORMANCE REPORT...")

    report = []
    report.append("COMPREHENSIVE PERFORMANCE AUDIT REPORT")
    report.append("=" * 80)
    report.append("")

    report.append("1. APPLICATION STARTUP PERFORMANCE:")
    report.append(startup_profiler.generate_report())
    report.append("")

    report.append("2. START POSITION PICKER PERFORMANCE:")
    report.append(picker_profiler.generate_report())
    report.append("")

    report.append("3. START POSITION TRANSITION PERFORMANCE:")
    report.append(transition_profiler.generate_report())

    # Save report to file
    report_content = "\n".join(report)
    with open("performance_audit_report.txt", "w") as f:
        f.write(report_content)

    print("\n" + "=" * 60)
    print("PERFORMANCE AUDIT COMPLETED")
    print("Report saved to: performance_audit_report.txt")
    print("=" * 60)

    return report_content


if __name__ == "__main__":
    run_comprehensive_audit()
