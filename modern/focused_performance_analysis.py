"""
Focused Performance Analysis

Based on the comprehensive audit, this script analyzes the specific bottlenecks
identified in the Modern application startup and start position selection workflow.
"""

import time
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def analyze_position_matching_service_duplication():
    """Analyze the duplicate Position matching service initialization."""
    print("=" * 80)
    print("ANALYZING POSITION MATCHING SERVICE DUPLICATION")
    print("=" * 80)

    start_time = time.perf_counter()

    # Import and create the service
    from application.services.positioning.position_matching_service import (
        PositionMatchingService,
    )

    print(
        f"[{time.perf_counter() - start_time:.6f}s] Importing PositionMatchingService"
    )

    # First initialization
    init1_start = time.perf_counter()
    service1 = PositionMatchingService()
    init1_time = time.perf_counter() - init1_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] First initialization: {init1_time:.6f}s"
    )

    # Second initialization (duplicate)
    init2_start = time.perf_counter()
    service2 = PositionMatchingService()
    init2_time = time.perf_counter() - init2_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Second initialization: {init2_time:.6f}s"
    )

    print(f"\n🔍 ANALYSIS:")
    print(f"   - First init: {init1_time:.6f}s")
    print(f"   - Second init: {init2_time:.6f}s")
    print(f"   - Total waste: {init1_time + init2_time:.6f}s")
    print(f"   - Services are same instance: {service1 is service2}")

    return init1_time + init2_time


def analyze_pictograph_pool_duplication():
    """Analyze the duplicate Pictograph pool initialization."""
    print("\n" + "=" * 80)
    print("ANALYZING PICTOGRAPH POOL DUPLICATION")
    print("=" * 80)

    from PyQt6.QtWidgets import QApplication, QWidget

    app = QApplication([])

    start_time = time.perf_counter()

    # Import and create the pool manager (this is what actually gets initialized)
    from presentation.components.option_picker.pictograph_pool_manager import (
        PictographPoolManager,
    )

    print(f"[{time.perf_counter() - start_time:.6f}s] Importing PictographPoolManager")

    # Create a parent widget for the pool
    parent = QWidget()

    # First initialization
    init1_start = time.perf_counter()
    pool1 = PictographPoolManager(parent)
    pool1.initialize_pool()
    init1_time = time.perf_counter() - init1_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] First initialization: {init1_time:.6f}s"
    )

    # Second initialization (duplicate)
    init2_start = time.perf_counter()
    pool2 = PictographPoolManager(parent)
    pool2.initialize_pool()
    init2_time = time.perf_counter() - init2_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Second initialization: {init2_time:.6f}s"
    )

    print(f"\n🔍 ANALYSIS:")
    print(f"   - First init: {init1_time:.6f}s")
    print(f"   - Second init: {init2_time:.6f}s")
    print(f"   - Total waste: {init1_time + init2_time:.6f}s")
    print(f"   - Pools are same instance: {pool1 is pool2}")

    app.quit()
    return init1_time + init2_time


def analyze_start_position_option_creation():
    """Analyze the cost of creating individual start position options."""
    print("\n" + "=" * 80)
    print("ANALYZING START POSITION OPTION CREATION")
    print("=" * 80)

    from PyQt6.QtWidgets import QApplication

    app = QApplication([])

    start_time = time.perf_counter()

    # Import the components
    from presentation.components.start_position_picker.start_position_picker import (
        StartPositionOption,
    )
    from application.services.data.pictograph_dataset_service import (
        PictographDatasetService,
    )

    print(f"[{time.perf_counter() - start_time:.6f}s] Imports completed")

    # Analyze dataset service creation (used by each option)
    dataset_start = time.perf_counter()
    dataset_service = PictographDatasetService()
    dataset_time = time.perf_counter() - dataset_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Dataset service creation: {dataset_time:.6f}s"
    )

    # Analyze single option creation
    option_start = time.perf_counter()
    option = StartPositionOption("alpha1_alpha1", "diamond")
    option_time = time.perf_counter() - option_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Single option creation: {option_time:.6f}s"
    )

    # Analyze multiple option creation (like in real usage)
    positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    multi_start = time.perf_counter()
    options = []
    for pos in positions:
        opt = StartPositionOption(pos, "diamond")
        options.append(opt)
    multi_time = time.perf_counter() - multi_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Three options creation: {multi_time:.6f}s"
    )

    print(f"\n🔍 ANALYSIS:")
    print(f"   - Dataset service: {dataset_time:.6f}s")
    print(f"   - Single option: {option_time:.6f}s")
    print(f"   - Three options: {multi_time:.6f}s")
    print(f"   - Average per option: {multi_time/3:.6f}s")

    app.quit()
    return multi_time


def analyze_main_window_creation_bottlenecks():
    """Analyze what's causing the 1.13s delay in main window creation."""
    print("\n" + "=" * 80)
    print("ANALYZING MAIN WINDOW CREATION BOTTLENECKS")
    print("=" * 80)

    from PyQt6.QtWidgets import QApplication

    app = QApplication([])

    start_time = time.perf_counter()

    # Import main window
    from main import KineticConstructorModern

    print(f"[{time.perf_counter() - start_time:.6f}s] Main window import completed")

    # Analyze service configuration
    config_start = time.perf_counter()
    window = KineticConstructorModern()
    config_time = time.perf_counter() - config_start
    print(
        f"[{time.perf_counter() - start_time:.6f}s] Main window creation: {config_time:.6f}s"
    )

    print(f"\n🔍 ANALYSIS:")
    print(f"   - Total main window creation: {config_time:.6f}s")
    print(f"   - This includes service configuration, UI setup, and background setup")

    app.quit()
    return config_time


def run_focused_analysis():
    """Run the focused performance analysis."""
    print("🔍 FOCUSED PERFORMANCE ANALYSIS")
    print("Analyzing specific bottlenecks identified in comprehensive audit")
    print("=" * 80)

    # Analyze each bottleneck
    position_matching_waste = analyze_position_matching_service_duplication()
    pictograph_pool_waste = analyze_pictograph_pool_duplication()
    start_option_cost = analyze_start_position_option_creation()
    main_window_cost = analyze_main_window_creation_bottlenecks()

    # Generate summary
    print("\n" + "=" * 80)
    print("PERFORMANCE BOTTLENECK SUMMARY")
    print("=" * 80)

    total_waste = position_matching_waste + pictograph_pool_waste

    print(f"🚨 TOP PERFORMANCE ISSUES:")
    print(f"   1. Main Window Creation: {main_window_cost:.6f}s")
    print(f"      - Contains service duplication and heavy initialization")
    print(f"   2. Service Duplication Waste: {total_waste:.6f}s")
    print(f"      - Position matching: {position_matching_waste:.6f}s")
    print(f"      - Pictograph pool: {pictograph_pool_waste:.6f}s")
    print(f"   3. Start Position Options: {start_option_cost:.6f}s")
    print(f"      - Each option creates its own dataset service")

    print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
    print(f"   - Eliminate service duplication: Save ~{total_waste:.6f}s")
    print(f"   - Use singleton pattern for heavy services")
    print(f"   - Lazy load start position options")
    print(f"   - Cache pictograph data instead of reloading")

    print(f"\n🎯 EXPECTED IMPROVEMENT:")
    potential_savings = total_waste + (
        start_option_cost * 0.7
    )  # 70% improvement on options
    print(f"   - Potential time savings: {potential_savings:.6f}s")
    print(f"   - From ~2.0s to ~{2.0 - potential_savings:.6f}s startup time")
    print(f"   - Performance improvement: {(potential_savings/2.0)*100:.1f}%")


if __name__ == "__main__":
    run_focused_analysis()
