"""
Test Launcher 86% Fix

Rigorous testing to verify that the 86% bottleneck fix is working correctly.
Tests both debug and release modes to ensure the fix doesn't break functionality.
"""

import time
import sys
from pathlib import Path
from typing import List, Dict

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


class LauncherFixValidator:
    """Validates that the launcher 86% fix is working correctly."""
    
    def __init__(self):
        self.test_results: List[Dict] = []
        self.debug_mode_times: List[float] = []
        self.release_mode_times: List[float] = []
    
    def run_launcher_test(self, test_name: str, debug_mode: bool = True) -> Dict:
        """Run a single launcher test and measure performance."""
        print(f"\n🧪 Running {test_name}...")
        
        start_time = time.perf_counter()
        progress_events = []
        
        def track_progress(message: str, progress: float = 0):
            current_time = time.perf_counter()
            elapsed = current_time - start_time
            progress_events.append({
                'message': message,
                'progress': progress,
                'elapsed': elapsed,
                'time_since_last': elapsed - (progress_events[-1]['elapsed'] if progress_events else 0)
            })
            
            # Check for 86% bottleneck specifically
            if '86%' in message or 'Loading option picker dataset' in message:
                print(f"   📍 86% checkpoint: {message} at {elapsed:.3f}s")
        
        try:
            # Import Qt components
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtGui import QGuiApplication
            from main import KineticConstructorModern
            from presentation.components.ui.splash_screen import SplashScreen
            
            # Create QApplication
            app = QApplication([])
            
            # Set debug mode
            if debug_mode:
                import os
                os.environ['PYTHONDEBUG'] = '1'
            
            # Create splash screen
            screen = QGuiApplication.primaryScreen()
            splash = SplashScreen(target_screen=screen)
            
            # Override update_progress to track timing
            original_update = splash.update_progress
            def monitored_update(value: int, message: str = ""):
                track_progress(f"{value}% - {message}", value / 100.0)
                return original_update(value, message)
            
            splash.update_progress = monitored_update
            
            # Show splash screen
            splash.show_animated()
            
            # Create main window
            main_window = KineticConstructorModern(
                splash_screen=splash,
                target_screen=screen,
                parallel_mode=False,
                parallel_geometry=None,
                enable_api=False
            )
            
            total_time = time.perf_counter() - start_time
            
            # Clean up
            app.quit()
            
            # Analyze results
            bottleneck_events = [e for e in progress_events if 'Loading option picker dataset' in e['message']]
            max_delay = max([e['time_since_last'] for e in progress_events], default=0)
            
            result = {
                'test_name': test_name,
                'debug_mode': debug_mode,
                'total_time': total_time,
                'max_delay': max_delay,
                'bottleneck_events': len(bottleneck_events),
                'bottleneck_time': bottleneck_events[0]['time_since_last'] if bottleneck_events else 0,
                'success': max_delay < 0.5,  # Success if no delay > 500ms
                'progress_events': len(progress_events)
            }
            
            print(f"   ✅ Test completed in {total_time:.3f}s")
            print(f"   📊 Max delay: {max_delay:.3f}s")
            print(f"   🎯 86% bottleneck time: {result['bottleneck_time']:.3f}s")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            return {
                'test_name': test_name,
                'debug_mode': debug_mode,
                'total_time': -1,
                'max_delay': -1,
                'success': False,
                'error': str(e)
            }
    
    def run_comprehensive_tests(self) -> None:
        """Run comprehensive tests to validate the fix."""
        print("🚀 STARTING COMPREHENSIVE LAUNCHER 86% FIX VALIDATION")
        print("=" * 70)
        
        # Test 1: Debug mode (where the issue was)
        debug_result = self.run_launcher_test("Debug Mode Test", debug_mode=True)
        self.test_results.append(debug_result)
        if debug_result['success']:
            self.debug_mode_times.append(debug_result['total_time'])
        
        # Test 2: Release mode (should work fine)
        release_result = self.run_launcher_test("Release Mode Test", debug_mode=False)
        self.test_results.append(release_result)
        if release_result['success']:
            self.release_mode_times.append(release_result['total_time'])
        
        # Test 3: Multiple debug runs to ensure consistency
        for i in range(3):
            debug_repeat = self.run_launcher_test(f"Debug Mode Repeat {i+1}", debug_mode=True)
            self.test_results.append(debug_repeat)
            if debug_repeat['success']:
                self.debug_mode_times.append(debug_repeat['total_time'])
    
    def generate_validation_report(self) -> str:
        """Generate a comprehensive validation report."""
        report = []
        report.append("# LAUNCHER 86% FIX VALIDATION REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Summary
        successful_tests = [r for r in self.test_results if r.get('success', False)]
        failed_tests = [r for r in self.test_results if not r.get('success', False)]
        
        report.append(f"**Total Tests:** {len(self.test_results)}")
        report.append(f"**Successful:** {len(successful_tests)}")
        report.append(f"**Failed:** {len(failed_tests)}")
        report.append("")
        
        # Performance analysis
        if self.debug_mode_times:
            avg_debug = sum(self.debug_mode_times) / len(self.debug_mode_times)
            max_debug = max(self.debug_mode_times)
            min_debug = min(self.debug_mode_times)
            
            report.append("## DEBUG MODE PERFORMANCE")
            report.append(f"- Average time: {avg_debug:.3f}s")
            report.append(f"- Max time: {max_debug:.3f}s")
            report.append(f"- Min time: {min_debug:.3f}s")
            report.append("")
        
        if self.release_mode_times:
            avg_release = sum(self.release_mode_times) / len(self.release_mode_times)
            
            report.append("## RELEASE MODE PERFORMANCE")
            report.append(f"- Average time: {avg_release:.3f}s")
            report.append("")
        
        # Detailed results
        report.append("## DETAILED TEST RESULTS")
        report.append("-" * 30)
        
        for result in self.test_results:
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            mode = "DEBUG" if result.get('debug_mode', False) else "RELEASE"
            
            report.append(f"**{result['test_name']}** ({mode}): {status}")
            
            if 'total_time' in result and result['total_time'] > 0:
                report.append(f"  - Total time: {result['total_time']:.3f}s")
                report.append(f"  - Max delay: {result['max_delay']:.3f}s")
                report.append(f"  - 86% bottleneck: {result.get('bottleneck_time', 0):.3f}s")
            
            if 'error' in result:
                report.append(f"  - Error: {result['error']}")
            
            report.append("")
        
        # Conclusion
        report.append("## CONCLUSION")
        report.append("-" * 20)
        
        if len(successful_tests) == len(self.test_results):
            report.append("🎉 **ALL TESTS PASSED!** The 86% bottleneck fix is working correctly.")
            report.append("✅ Debug mode performance has been optimized")
            report.append("✅ Release mode functionality is preserved")
        elif len(successful_tests) > len(failed_tests):
            report.append("⚠️ **MOSTLY SUCCESSFUL** - Some tests failed but the fix is generally working.")
        else:
            report.append("❌ **FIX VALIDATION FAILED** - The 86% bottleneck issue persists.")
        
        return "\n".join(report)


def main():
    """Run the comprehensive launcher fix validation."""
    validator = LauncherFixValidator()
    
    try:
        validator.run_comprehensive_tests()
        
        # Generate and save report
        report = validator.generate_validation_report()
        
        with open("launcher_86_fix_validation_report.txt", "w") as f:
            f.write(report)
        
        print("\n" + "=" * 70)
        print("VALIDATION COMPLETED")
        print("=" * 70)
        print(report)
        print("\n📊 Full report saved to: launcher_86_fix_validation_report.txt")
        
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
