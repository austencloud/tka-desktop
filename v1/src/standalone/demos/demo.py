#!/usr/bin/env python3
"""
Demonstration script for standalone tab functionality.

This script shows how to use the standalone tab system and provides
examples of different ways to launch tabs.
"""

import sys
import os
import subprocess
import time

# Add src directory to path
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Also add project root
project_root = os.path.dirname(src_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def demo_launcher_help():
    """Demonstrate the launcher help functionality."""
    print("=" * 60)
    print("DEMO: Launcher Help")
    print("=" * 60)

    launcher_path = os.path.join(
        project_root, "src", "standalone", "core", "launcher.py"
    )

    print("Running: python src/standalone/core/launcher.py --help")
    print()

    result = subprocess.run(
        [sys.executable, launcher_path, "--help"],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    print(result.stdout)


def demo_config_system():
    """Demonstrate the configuration system."""
    print("=" * 60)
    print("DEMO: Configuration System")
    print("=" * 60)

    from standalone.config import get_standalone_config

    config = get_standalone_config()

    print(f"Total configured tabs: {len(config.tabs)}")
    print(f"Default launch mode: {config.default_launch_mode.value}")
    print(f"Context menus enabled: {config.enable_context_menus}")
    print()

    print("Tab configurations:")
    for tab_name, tab_config in config.tabs.items():
        print(f"  {tab_name}:")
        print(f"    Display name: {tab_config.display_name}")
        print(f"    Standalone capable: {tab_config.can_run_standalone}")
        print(f"    Launch mode: {tab_config.launch_mode.value}")
        print(f"    Description: {tab_config.description}")
        print()


def demo_factory_imports():
    """Demonstrate that all factories can be imported."""
    print("=" * 60)
    print("DEMO: Factory Import System")
    print("=" * 60)

    from standalone.core.launcher import TAB_FACTORIES, get_factory_class

    print("Available tab factories:")
    for tab_name, (module_path, class_name) in TAB_FACTORIES.items():
        try:
            factory_class = get_factory_class(tab_name)
            print(f"  ✅ {tab_name}: {class_name} from {module_path}")
        except Exception as e:
            print(f"  ❌ {tab_name}: Failed to import - {e}")
    print()


def demo_standalone_runner():
    """Demonstrate the standalone runner system."""
    print("=" * 60)
    print("DEMO: Standalone Runner System")
    print("=" * 60)

    from standalone.core.base_runner import BaseStandaloneRunner
    from standalone.core.launcher import get_factory_class

    # Create a runner for the construct tab (but don't run it)
    factory_class = get_factory_class("construct")
    runner = BaseStandaloneRunner("construct", factory_class)

    print(f"Created runner for: {runner.tab_name}")
    print(f"Factory class: {runner.tab_factory_class.__name__}")
    print(f"Runner type: {type(runner).__name__}")
    print()

    print("Runner capabilities:")
    print("  - Configures import paths automatically")
    print("  - Initializes dependency injection")
    print("  - Creates minimal coordinator")
    print("  - Handles Qt application lifecycle")
    print("  - Provides error handling and logging")
    print()


def demo_integration_possibilities():
    """Show integration possibilities with the main application."""
    print("=" * 60)
    print("DEMO: Integration Possibilities")
    print("=" * 60)

    print("The enhanced tab switcher provides:")
    print("  - Right-click context menus on tab buttons")
    print("  - 'Switch to Tab' (internal) option")
    print("  - 'Open in New Window' (external) option")
    print("  - 'Close External Tab' option (if running)")
    print("  - Process management and tracking")
    print()

    print("Integration example code:")
    print(
        """
    # In MainWidget initialization:
    from main_window.main_widget.enhanced_tab_switcher import EnhancedTabSwitcher
    
    self.tab_switcher = EnhancedTabSwitcher(self, app_context)
    
    # Connect signals
    self.tab_switcher.external_tab_launched.connect(self.on_external_tab_launched)
    
    # Enable context menus
    tab_button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    tab_button.customContextMenuRequested.connect(
        lambda pos: self.show_tab_context_menu(tab_name, pos)
    )
    """
    )
    print()


def demo_usage_examples():
    """Show usage examples."""
    print("=" * 60)
    print("DEMO: Usage Examples")
    print("=" * 60)

    print("Command line usage:")
    print("  python src/standalone/core/launcher.py construct")
    print("  python src/standalone/core/launcher.py generate")
    print("  python src/standalone/core/launcher.py browse")
    print("  python src/standalone/core/launcher.py learn")
    print("  python src/standalone/core/launcher.py sequence_card")
    print()

    print("Individual scripts:")
    print("  python src/standalone/tabs/construct.py")
    print("  python src/standalone/tabs/generate.py")
    print("  python src/standalone/tabs/browse.py")
    print("  python src/standalone/tabs/learn.py")
    print("  python src/standalone/tabs/sequence_card.py")
    print()

    print("Module syntax:")
    print("  python -m standalone.core.launcher construct")
    print("  python -m standalone.tabs.construct")
    print()

    print("Debug mode:")
    print("  python src/standalone/core/launcher.py --debug construct")
    print()


def main():
    """Run all demonstrations."""
    print("🎉 STANDALONE TAB FUNCTIONALITY DEMONSTRATION")
    print()

    demos = [
        demo_config_system,
        demo_factory_imports,
        demo_standalone_runner,
        demo_integration_possibilities,
        demo_usage_examples,
        demo_launcher_help,
    ]

    for demo in demos:
        try:
            demo()
            time.sleep(1)  # Brief pause between demos
        except Exception as e:
            print(f"❌ Demo {demo.__name__} failed: {e}")
            import traceback

            traceback.print_exc()
            print()

    print("=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print()
    print("🚀 Your tabs are now ready to run as standalone applications!")
    print()
    print("Try it out:")
    print("  python src/standalone/core/launcher.py construct")
    print()


if __name__ == "__main__":
    main()
