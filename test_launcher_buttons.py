#!/usr/bin/env python3
"""
Test script to verify all launcher button connections work properly.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    print("=== Testing Imports ===")
    try:
        from launcher.core.application import LauncherApplication
        from launcher.data.app_definitions import AppDefinitions
        from launcher.core.process_manager import ProcessManager

        print("✅ All core imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_app_definitions():
    print("\n=== Testing App Definitions ===")
    try:
        from launcher.data.app_definitions import AppDefinitions

        apps = AppDefinitions.get_by_category("applications")
        dev_tools = AppDefinitions.get_by_category("dev_tools")

        print(f"✅ Found {len(apps)} application definitions")
        print(f"✅ Found {len(dev_tools)} dev tool definitions")

        print("\nApplication buttons:")
        for app in apps:
            script_exists = os.path.exists(app.script_path) if app.script_path else True
            status = "✅" if script_exists else "❌"
            print(f"  {status} {app.title} - {app.script_path or app.command}")

        print("\nDev tool buttons:")
        for tool in dev_tools:
            print(f"  📋 {tool.title} - {tool.command or tool.script_path}")

        return True
    except Exception as e:
        print(f"❌ App definitions test failed: {e}")
        return False


def test_file_paths():
    print("\n=== Testing File Path Existence ===")
    from launcher.data.app_definitions import AppDefinitions

    all_apps = AppDefinitions.get_all()
    missing_files = []

    for app in all_apps:
        if app.script_path:
            if not os.path.exists(app.script_path):
                missing_files.append((app.title, app.script_path))
                print(f"❌ Missing: {app.script_path} for {app.title}")
            else:
                print(f"✅ Found: {app.script_path}")

    if missing_files:
        print(f"\n⚠️  {len(missing_files)} files need attention")
        return False
    else:
        print("✅ All script paths exist")
        return True


def test_process_manager():
    print("\n=== Testing Process Manager ===")
    try:
        from launcher.core.process_manager import ProcessManager
        from PyQt6.QtWidgets import QApplication

        app = QApplication([])
        pm = ProcessManager()

        test_process = pm.execute_command(["python", "--version"])
        if test_process:
            print("✅ Process manager can execute commands")
            test_process.waitForFinished(3000)
        else:
            print("❌ Process manager failed to execute test command")
            return False

        app.quit()
        return True
    except Exception as e:
        print(f"❌ Process manager test failed: {e}")
        return False


def main():
    print("🧪 LAUNCHER BUTTON CONNECTION TEST")
    print("=" * 50)

    tests = [test_imports, test_app_definitions, test_file_paths, test_process_manager]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print("✅ Launcher buttons should work correctly!")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("❌ Some button connections may have issues")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
