"""
Launcher Progress Profiler

Profiles the Modern application startup to identify why the launcher gets stuck at 86%.
Provides detailed timing analysis of each progress step.
"""

import time
import sys
from pathlib import Path
from typing import Dict, List, Optional
import threading

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class ProgressProfiler:
    """Profiles progress updates during application startup."""

    def __init__(self):
        self.progress_events: List[Dict] = []
        self.start_time = time.perf_counter()
        self.last_progress = 0
        self.stuck_threshold = 2.0  # Consider stuck if no progress for 2 seconds

    def log_progress(self, progress: int, message: str):
        """Log a progress update with timing information."""
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time

        # Calculate time since last progress update
        time_since_last = 0
        if self.progress_events:
            time_since_last = current_time - self.progress_events[-1]["timestamp"]

        event = {
            "progress": progress,
            "message": message,
            "timestamp": current_time,
            "elapsed_total": elapsed,
            "time_since_last": time_since_last,
            "is_stuck": time_since_last > self.stuck_threshold,
        }

        self.progress_events.append(event)

        # Print real-time analysis
        stuck_indicator = " 🚨 STUCK!" if event["is_stuck"] else ""
        print(
            f"[{elapsed:.3f}s] {progress}% - {message} (+{time_since_last:.3f}s){stuck_indicator}"
        )

        self.last_progress = progress

    def analyze_bottlenecks(self):
        """Analyze the progress events to identify bottlenecks."""
        print("\n" + "=" * 80)
        print("LAUNCHER PROGRESS BOTTLENECK ANALYSIS")
        print("=" * 80)

        if not self.progress_events:
            print("No progress events recorded!")
            return

        # Find the longest delays
        delays = []
        for i, event in enumerate(self.progress_events):
            if event["time_since_last"] > 0.1:  # Only consider delays > 100ms
                delays.append(
                    {
                        "progress": event["progress"],
                        "message": event["message"],
                        "delay": event["time_since_last"],
                        "previous_progress": (
                            self.progress_events[i - 1]["progress"] if i > 0 else 0
                        ),
                    }
                )

        # Sort by delay duration
        delays.sort(key=lambda x: x["delay"], reverse=True)

        print(f"🔍 IDENTIFIED {len(delays)} SIGNIFICANT DELAYS:")
        print("-" * 50)

        for i, delay in enumerate(delays[:10]):  # Top 10 delays
            print(
                f"{i+1}. {delay['previous_progress']}% → {delay['progress']}%: {delay['delay']:.3f}s"
            )
            print(f"   Message: {delay['message']}")
            print()

        # Check for the 86% issue specifically
        stuck_at_86 = [
            e
            for e in self.progress_events
            if e["progress"] <= 86 and e["time_since_last"] > 1.0
        ]
        if stuck_at_86:
            print("🚨 CONFIRMED: Application gets stuck around 86%!")
            for event in stuck_at_86:
                print(
                    f"   Stuck at {event['progress']}% for {event['time_since_last']:.3f}s"
                )
                print(f"   Message: {event['message']}")

        return delays


class MonitoredSplashScreen:
    """Wrapper around splash screen to monitor progress updates."""

    def __init__(self, real_splash, profiler: ProgressProfiler):
        self.real_splash = real_splash
        self.profiler = profiler

    def update_progress(self, value: int, message: str = ""):
        """Monitor progress updates and forward to real splash screen."""
        self.profiler.log_progress(value, message)
        if self.real_splash:
            self.real_splash.update_progress(value, message)

    def __getattr__(self, name):
        """Forward all other attributes to the real splash screen."""
        return getattr(self.real_splash, name)


def profile_launcher_startup(debug_mode=True):
    """Profile the complete launcher startup sequence."""
    profiler = ProgressProfiler()

    mode_text = "DEBUG MODE" if debug_mode else "RELEASE MODE"
    print(f"🔍 PROFILING LAUNCHER STARTUP SEQUENCE - {mode_text}")
    print("=" * 60)
    print("Monitoring progress updates to identify 86% bottleneck...")
    print()

    try:
        # Import Qt components
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QGuiApplication
        from main import KineticConstructorModern
        from presentation.components.ui.splash_screen import SplashScreen

        # Create QApplication
        app = QApplication([])

        # Set debug mode if requested
        if debug_mode:
            import os

            os.environ["PYTHONDEBUG"] = "1"
            print("🐛 DEBUG MODE ENABLED - This will show debug-specific delays")

        # Create splash screen
        screen = QGuiApplication.primaryScreen()
        splash = SplashScreen(target_screen=screen)

        # Wrap splash screen with monitoring
        monitored_splash = MonitoredSplashScreen(splash, profiler)

        # Show splash screen
        splash.show_animated()

        # Create main window with monitored splash
        profiler.log_progress(0, "Starting application initialization...")

        main_window = KineticConstructorModern(
            splash_screen=monitored_splash,
            target_screen=screen,
            parallel_mode=False,
            parallel_geometry=None,
            enable_api=False,  # Disable API to focus on UI bottlenecks
        )

        profiler.log_progress(100, "Application startup completed!")

        # Clean up
        app.quit()

    except Exception as e:
        profiler.log_progress(-1, f"ERROR: {e}")
        print(f"❌ Error during profiling: {e}")
        import traceback

        traceback.print_exc()

    # Analyze results
    delays = profiler.analyze_bottlenecks()

    return profiler, delays


def create_detailed_timing_report(profiler: ProgressProfiler, delays: List[Dict]):
    """Create a detailed timing report for the launcher bottleneck."""

    report = []
    report.append("# LAUNCHER 86% BOTTLENECK - DETAILED TIMING REPORT")
    report.append("=" * 60)
    report.append("")

    # Executive summary
    total_time = (
        profiler.progress_events[-1]["elapsed_total"] if profiler.progress_events else 0
    )
    report.append(f"**Total Startup Time:** {total_time:.3f}s")
    report.append(f"**Progress Events:** {len(profiler.progress_events)}")
    report.append("")

    # Progress timeline
    report.append("## PROGRESS TIMELINE")
    report.append("-" * 30)
    for event in profiler.progress_events:
        stuck_marker = " 🚨" if event["is_stuck"] else ""
        report.append(
            f"{event['elapsed_total']:6.3f}s | {event['progress']:3d}% | {event['message']}{stuck_marker}"
        )
    report.append("")

    # Top bottlenecks
    report.append("## TOP BOTTLENECKS")
    report.append("-" * 30)
    for i, delay in enumerate(delays[:5]):
        report.append(
            f"{i+1}. {delay['previous_progress']}% → {delay['progress']}%: {delay['delay']:.3f}s"
        )
        report.append(f"   {delay['message']}")
        report.append("")

    # 86% specific analysis
    report.append("## 86% BOTTLENECK ANALYSIS")
    report.append("-" * 30)

    # Find events around 86%
    around_86 = [e for e in profiler.progress_events if 83 <= e["progress"] <= 90]
    if around_86:
        report.append("Progress events around 86%:")
        for event in around_86:
            report.append(
                f"  {event['progress']}%: {event['message']} (+{event['time_since_last']:.3f}s)"
            )

    # Save report
    report_content = "\n".join(report)
    with open("launcher_86_bottleneck_report.txt", "w") as f:
        f.write(report_content)

    print("\n📊 Detailed timing report saved to: launcher_86_bottleneck_report.txt")
    return report_content


if __name__ == "__main__":
    print("🚀 Starting Launcher Progress Profiling...")

    # Test in debug mode (where the issue occurs)
    print("\n" + "=" * 60)
    print("TESTING IN DEBUG MODE (where 86% issue occurs)")
    print("=" * 60)
    profiler_debug, delays_debug = profile_launcher_startup(debug_mode=True)

    if delays_debug:
        print(f"\n🎯 Creating detailed timing report for DEBUG MODE...")
        try:
            create_detailed_timing_report(profiler_debug, delays_debug)
        except UnicodeEncodeError:
            # Handle unicode issue by creating a simpler report
            print("📊 SIMPLIFIED DEBUG MODE REPORT:")
            for i, delay in enumerate(delays_debug[:5]):
                print(
                    f"{i+1}. {delay['previous_progress']}% to {delay['progress']}%: {delay['delay']:.3f}s"
                )
                print(f"   {delay['message']}")

        print("\n💡 NEXT STEPS:")
        print("1. Identify debug-specific operations causing delays")
        print("2. Implement conditional debug optimizations")
        print("3. Test fixes in both debug and release modes")
    else:
        print("\n✅ No significant delays found in debug mode!")
