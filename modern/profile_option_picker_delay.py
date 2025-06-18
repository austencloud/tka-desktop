"""
Option Picker Delay Profiler

Profiles the specific delay in option picker refresh to identify bottlenecks
in the start position to option picker transition workflow.
"""

import time
import sys
from pathlib import Path
from typing import Dict, List
import functools

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class OptionPickerProfiler:
    """Profiles option picker refresh operations to identify delays."""

    def __init__(self):
        self.timing_data: Dict[str, List[float]] = {}
        self.call_stack: List[str] = []
        self.detailed_logs: List[str] = []

    def log(self, message: str):
        """Log a detailed message with timestamp."""
        timestamp = time.perf_counter()
        self.detailed_logs.append(f"[{timestamp:.6f}] {message}")
        print(f"[{timestamp:.6f}] {message}")

    def time_function(self, func_name: str = None):
        """Decorator to time function execution."""

        def decorator(func):
            name = func_name or f"{func.__module__}.{func.__name__}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.perf_counter()
                self.call_stack.append(name)
                self.log(f"START: {name}")

                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.perf_counter()
                    duration = end_time - start_time

                    if name not in self.timing_data:
                        self.timing_data[name] = []
                    self.timing_data[name].append(duration)

                    self.call_stack.pop()
                    self.log(f"END: {name} - Duration: {duration:.6f}s")

            return wrapper

        return decorator


def profile_option_picker_refresh():
    """Profile the option picker refresh operation that's causing delays."""
    profiler = OptionPickerProfiler()

    print("🔍 PROFILING OPTION PICKER REFRESH DELAY")
    print("=" * 60)

    try:
        # Import required modules
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QGuiApplication
        from main import KineticConstructorModern

        # Create QApplication
        app = QApplication([])

        # Create main window
        screen = QGuiApplication.primaryScreen()
        main_window = KineticConstructorModern(
            target_screen=screen,
            parallel_mode=False,
            parallel_geometry=None,
            enable_api=False,
        )

        main_window.show()

        # Wait for initialization
        app.processEvents()
        time.sleep(1)

        print("✅ Application initialized, starting option picker profiling...")

        # Get the construct tab and its components
        construct_tab = None
        for i in range(main_window.tab_widget.count()):
            if "construct" in main_window.tab_widget.tabText(i).lower():
                main_window.tab_widget.setCurrentIndex(i)
                construct_tab = main_window.tab_widget.currentWidget()
                break

        if not construct_tab:
            print("❌ Could not find construct tab")
            return

        # Get the layout manager and option picker
        layout_manager = construct_tab.layout_manager
        option_picker = layout_manager.option_picker

        if not option_picker:
            print("❌ Could not find option picker")
            return

        print("✅ Found option picker, instrumenting methods...")

        # Instrument key methods with profiling
        original_refresh = option_picker.refresh_options_from_modern_sequence
        original_load_combinations = (
            option_picker._beat_loader.load_motion_combinations
            if option_picker._beat_loader
            else None
        )
        original_update_display = (
            option_picker._display_manager.update_beat_display
            if option_picker._display_manager
            else None
        )

        # Wrap methods with profiling
        if original_refresh:
            option_picker.refresh_options_from_modern_sequence = profiler.time_function(
                "refresh_options_from_modern_sequence"
            )(original_refresh)

        if original_load_combinations:
            option_picker._beat_loader.load_motion_combinations = (
                profiler.time_function("load_motion_combinations")(
                    original_load_combinations
                )
            )

        if original_update_display:
            option_picker._display_manager.update_beat_display = profiler.time_function(
                "update_beat_display"
            )(original_update_display)

        # Also instrument position matching service
        from application.services.positioning.position_matching_service import (
            PositionMatchingService,
        )

        position_service = PositionMatchingService()
        original_get_next_options = position_service.get_next_options
        position_service.get_next_options = profiler.time_function("get_next_options")(
            original_get_next_options
        )

        # Instrument pictograph pool operations
        if option_picker._pool_manager:
            original_get_pool_frame = option_picker._pool_manager.get_pool_frame
            option_picker._pool_manager.get_pool_frame = profiler.time_function(
                "get_pool_frame"
            )(original_get_pool_frame)

        print("✅ Methods instrumented, triggering start position selection...")

        # Use the existing beat loader method that we know causes the delay
        print("🎯 Triggering option picker refresh (this is where the delay occurs)...")

        # Create sample sequence data like what the real application uses
        sequence_data = [
            {"metadata": "sequence_info"},
            {
                "id": "test-beat-id",
                "beat_number": 1,
                "letter": "α",
                "duration": 1.0,
                "blue_motion": {
                    "motion_type": "static",
                    "prop_rot_dir": "no_rot",
                    "start_loc": "s",
                    "end_loc": "s",
                    "turns": 0.0,
                    "start_ori": "in",
                    "end_ori": "in",
                },
                "red_motion": {
                    "motion_type": "static",
                    "prop_rot_dir": "no_rot",
                    "start_loc": "n",
                    "end_loc": "n",
                    "turns": 0.0,
                    "start_ori": "in",
                    "end_ori": "in",
                },
                "end_pos": "alpha1",  # This is what triggers the position matching
            },
        ]

        # This is the operation that takes 390-450ms
        start_time = time.perf_counter()
        if option_picker._beat_loader:
            beat_options = option_picker._beat_loader.load_motion_combinations(
                sequence_data
            )
            if option_picker._display_manager:
                option_picker._display_manager.update_beat_display(beat_options)
        total_time = time.perf_counter() - start_time

        print(f"⏱️ Total refresh time: {total_time:.3f}s")

        # Generate timing report
        print("\n" + "=" * 60)
        print("OPTION PICKER DELAY ANALYSIS")
        print("=" * 60)

        sorted_operations = sorted(
            profiler.timing_data.items(), key=lambda x: max(x[1]), reverse=True
        )

        print("TOP BOTTLENECKS:")
        for i, (operation, times) in enumerate(sorted_operations[:10]):
            avg_time = sum(times) / len(times)
            max_time = max(times)
            print(f"{i+1}. {operation}: {max_time:.6f}s (avg: {avg_time:.6f}s)")

        print(f"\nTOTAL MEASURED TIME: {total_time:.6f}s")
        print(
            f"ACCOUNTED TIME: {sum(max(times) for times in profiler.timing_data.values()):.6f}s"
        )

        # Clean up
        app.quit()

        return profiler.timing_data

    except Exception as e:
        print(f"❌ Error during profiling: {e}")
        import traceback

        traceback.print_exc()
        return {}


def analyze_option_picker_bottlenecks():
    """Analyze the specific bottlenecks in option picker refresh."""
    print("🚀 Starting Option Picker Delay Analysis...")

    timing_data = profile_option_picker_refresh()

    if timing_data:
        print("\n🎯 OPTIMIZATION RECOMMENDATIONS:")

        # Analyze the bottlenecks
        for operation, times in timing_data.items():
            max_time = max(times)
            if max_time > 0.1:  # More than 100ms
                print(f"⚠️ BOTTLENECK: {operation} takes {max_time:.3f}s")

                if "get_next_options" in operation:
                    print("   💡 Optimization: Cache position matching results")
                elif "update_beat_display" in operation:
                    print("   💡 Optimization: Batch UI updates, lazy loading")
                elif "get_pool_frame" in operation:
                    print("   💡 Optimization: Pre-allocate pool frames")
                elif "load_motion_combinations" in operation:
                    print("   💡 Optimization: Cache motion combinations")

        print("\n📊 Performance target: Reduce total time from ~450ms to <100ms")
    else:
        print("❌ No timing data collected")


if __name__ == "__main__":
    analyze_option_picker_bottlenecks()
