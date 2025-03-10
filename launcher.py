import os
import sys

# Set up the Python path before ANY imports
if getattr(sys, 'frozen', False):
    # Running as executable
    base_dir = sys._MEIPASS
    print(f"Running from PyInstaller bundle at {base_dir}")
    
    # Add base_dir to path (critical for imports)
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    
    # Show directory contents for debugging
    print(f"Contents of _internal: {os.listdir(base_dir)}")
    
    # Create a customized Python path for imports
    custom_path = []
    
    # 1. Add the base directory itself
    custom_path.append(base_dir)
    
    # 2. Add the src directory if it exists
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir):
        custom_path.append(src_dir)
    
    # Replace sys.path with our custom path
    sys.path = custom_path + sys.path
    print(f"Modified sys.path: {sys.path}")

# Now run the application by directly executing the code in main.py
# This avoids import problems entirely

# Define the main function inline (copied from your original main.py)
def run_application():
    # Import all required modules
    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import QApplication
    from main_window.main_widget.json_manager.json_manager import JsonManager
    from main_window.main_widget.json_manager.special_placement_saver import SpecialPlacementSaver
    from main_window.main_window import MainWindow
    from utils.path_helpers import get_data_path
    from settings_manager.settings_manager import SettingsManager
    from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
    from splash_screen.splash_screen import SplashScreen
    from profiler import Profiler
    from utils.call_tracer import CallTracer
    from settings_manager.global_settings.app_context import AppContext
    from utils.paint_event_supressor import PaintEventSuppressor
    
    # Debug output
    print("Successfully imported all modules!")
    
    # Set up project directory and log file
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        PROJECT_DIR = sys._MEIPASS
    
    LOG_FILE_PATH = get_data_path("trace_log.txt")
    log_file = open(LOG_FILE_PATH, "w")
    
    # Initialize application
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")
    
    settings_manager = SettingsManager()
    splash_screen = SplashScreen(app, settings_manager)
    app.processEvents()
    
    profiler = Profiler()
    json_manager = JsonManager()
    special_placement_handler = SpecialPlacementSaver()
    special_placement_loader = SpecialPlacementLoader()
    
    AppContext.init(
        settings_manager,
        json_manager,
        special_placement_handler,
        special_placement_loader=special_placement_loader,
    )
    
    # Create main window
    main_window = MainWindow(profiler, splash_screen)
    AppContext._main_window = main_window
    
    main_window.show()
    main_window.raise_()
    
    QTimer.singleShot(0, lambda: splash_screen.close())
    
    # Set up event handlers
    PaintEventSuppressor.install_message_handler()
    tracer = CallTracer(PROJECT_DIR, log_file)
    sys.settrace(tracer.trace_calls)
    
    # Run application
    exit_code = main_window.exec(app)
    sys.exit(exit_code)

# Run the application
if __name__ == "__main__":
    run_application()