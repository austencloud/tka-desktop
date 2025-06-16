#!/usr/bin/env python3
"""
TKA Parallel Testing Launcher
=============================

Main launcher that verifies data structures and deploys side-by-side testing.
Ensures 100% confidence before running parallel tests.

LIFECYCLE: SCAFFOLDING
DELETE_AFTER: Legacy deprecation complete
PURPOSE: Safe launcher for Legacy/Modern parallel testing with verification
"""

import sys
import asyncio
import subprocess
from pathlib import Path


def print_banner():
    """Print TKA parallel testing banner."""
    print("🚀 TKA PARALLEL TESTING FRAMEWORK")
    print("=" * 50)
    print("Legacy/Modern Functional Equivalence Validation")
    print("Side-by-Side Visual Testing")
    print("=" * 50)


def run_verification() -> bool:
    """Run data structure verification."""
    print("\n🔍 PHASE 1: DATA STRUCTURE VERIFICATION")
    print("=" * 45)
    print("Verifying 100% accuracy before deployment...")

    try:
        # Run verification script
        result = subprocess.run(
            [sys.executable, "verify_data_structures.py"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
        )

        # Print verification output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print("\n✅ VERIFICATION PASSED - Ready for deployment")
            return True
        else:
            print(f"\n❌ VERIFICATION FAILED - Exit code: {result.returncode}")
            print("🚫 Cannot proceed with deployment until issues are resolved")
            return False

    except Exception as e:
        print(f"❌ Verification script failed: {e}")
        return False


async def run_deployment():
    """Run side-by-side deployment."""
    print("\n🚀 PHASE 2: SIDE-BY-SIDE DEPLOYMENT")
    print("=" * 40)
    print("Deploying Legacy and Modern applications for visual testing...")

    try:
        # Import and run deployment
        from deploy_side_by_side_test import main as deploy_main

        exit_code = await deploy_main()

        if exit_code == 0:
            print("\n🎉 DEPLOYMENT COMPLETED SUCCESSFULLY")
        else:
            print(f"\n❌ DEPLOYMENT FAILED - Exit code: {exit_code}")

        return exit_code

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


def show_pre_deployment_checklist():
    """Show pre-deployment checklist."""
    print("\n📋 PRE-DEPLOYMENT CHECKLIST")
    print("=" * 30)
    print("Before running parallel tests, ensure:")
    print("  ✅ Legacy TKA application is available and functional")
    print("  ✅ Modern TKA application is available and functional")
    print("  ✅ Both applications can start without errors")
    print("  ✅ Monitor configuration supports side-by-side viewing")
    print("  ✅ No other TKA instances are running")

    response = input("\n❓ Are all prerequisites met? (y/N): ").strip().lower()
    return response in ["y", "yes"]


def show_deployment_options():
    """Show deployment options."""
    print("\n🎯 DEPLOYMENT OPTIONS")
    print("=" * 25)
    print("1. Full verification + deployment (recommended)")
    print("2. Skip verification, deploy directly (risky)")
    print("3. Verification only (no deployment)")
    print("4. Exit")

    while True:
        try:
            choice = input("\n🎯 Select option (1-4): ").strip()

            if choice in ["1", "2", "3", "4"]:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
            return 4


async def main():
    """Main launcher routine."""
    print_banner()

    try:
        # Show pre-deployment checklist
        if not show_pre_deployment_checklist():
            print("\n⚠️  Prerequisites not met. Please resolve issues and try again.")
            return 1

        # Show deployment options
        choice = show_deployment_options()

        if choice == 4:
            print("\n👋 Exiting...")
            return 0

        elif choice == 3:
            # Verification only
            if run_verification():
                print("\n🎉 Verification completed successfully!")
                print("✅ Data structures are ready for deployment")
                return 0
            else:
                print("\n❌ Verification failed")
                return 1

        elif choice == 2:
            # Skip verification, deploy directly
            print("\n⚠️  SKIPPING VERIFICATION - PROCEEDING DIRECTLY TO DEPLOYMENT")
            print("🚨 This is risky and may result in incorrect test results!")

            confirm = (
                input("❓ Are you sure you want to skip verification? (y/N): ")
                .strip()
                .lower()
            )
            if confirm not in ["y", "yes"]:
                print("👍 Smart choice! Running verification first...")
                choice = 1  # Fall through to full verification + deployment
            else:
                return await run_deployment()

        if choice == 1:
            # Full verification + deployment (recommended)
            print("\n🎯 RUNNING FULL VERIFICATION + DEPLOYMENT")

            # Step 1: Verification
            if not run_verification():
                print("\n🚫 DEPLOYMENT ABORTED - Verification failed")
                print("Please fix verification issues and try again.")
                return 1

            # Step 2: Deployment
            print("\n✅ Verification passed! Proceeding to deployment...")
            input("⏸️  Press Enter to continue to deployment...")

            return await run_deployment()

        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Launcher interrupted by user")
        return 1

    except Exception as e:
        print(f"❌ Launcher failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


def show_usage():
    """Show usage information."""
    print("TKA Parallel Testing Launcher")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python launch_parallel_testing.py")
    print()
    print("This launcher will:")
    print("  1. Verify data structure accuracy (100% confidence)")
    print("  2. Deploy Legacy and Modern applications side-by-side")
    print("  3. Provide interactive testing interface")
    print()
    print("Requirements:")
    print("  - TKA Legacy application available")
    print("  - TKA Modern application available")
    print("  - PyQt6 installed")
    print("  - Dual monitor setup (recommended)")
    print()
    print("Features:")
    print("  - Real-time visual comparison")
    print("  - Automated action synchronization")
    print("  - Interactive test scenario selection")
    print("  - Comprehensive logging and screenshots")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        show_usage()
        sys.exit(0)

    exit_code = asyncio.run(main())
    sys.exit(exit_code)
