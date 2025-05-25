#!/usr/bin/env python3
"""
Debug script to see what's happening with tab creation.
"""

import sys
import os
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_tab_creation():
    """Debug what happens when we create tabs."""
    print("🔍 DEBUGGING TAB CREATION")
    print("=" * 60)
    
    try:
        # Start the application with more detailed logging
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            cwd="/f/CODE/the-kinetic-constructor-desktop",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for initialization
        time.sleep(8)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application started successfully")
            
            # Terminate the process
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            
            print("\n🔍 ANALYZING APPLICATION LOGS")
            print("=" * 60)
            
            # Look for tab creation logs
            lines = stderr.split('\n')
            
            tab_creation_logs = []
            stack_population_logs = []
            error_logs = []
            
            for line in lines:
                if 'Created' in line and 'Tab' in line:
                    tab_creation_logs.append(line)
                elif 'Added' in line and 'stack' in line:
                    stack_population_logs.append(line)
                elif 'ERROR' in line or 'Failed' in line:
                    error_logs.append(line)
            
            print("📋 TAB CREATION LOGS:")
            if tab_creation_logs:
                for log in tab_creation_logs:
                    print(f"  ✅ {log}")
            else:
                print("  ❌ No tab creation logs found")
            
            print("\n📋 STACK POPULATION LOGS:")
            if stack_population_logs:
                for log in stack_population_logs:
                    print(f"  ✅ {log}")
            else:
                print("  ❌ No stack population logs found")
            
            print("\n📋 ERROR LOGS:")
            if error_logs:
                for log in error_logs:
                    print(f"  ❌ {log}")
            else:
                print("  ✅ No errors found")
            
            # Look for specific patterns
            print("\n🔍 SPECIFIC PATTERN ANALYSIS:")
            print("=" * 60)
            
            # Check if tabs are being created
            if any('GenerateTab' in log for log in tab_creation_logs):
                print("✅ GenerateTab is being created")
            else:
                print("❌ GenerateTab is NOT being created")
            
            if any('BrowseTab' in log for log in tab_creation_logs):
                print("✅ BrowseTab is being created")
            else:
                print("❌ BrowseTab is NOT being created")
            
            if any('LearnTab' in log for log in tab_creation_logs):
                print("✅ LearnTab is being created")
            else:
                print("❌ LearnTab is NOT being created")
            
            if any('ConstructTab' in log for log in tab_creation_logs):
                print("✅ ConstructTab is being created")
            else:
                print("❌ ConstructTab is NOT being created")
            
            # Check if essential widgets are being added
            if any('sequence_workbench' in log for log in stack_population_logs):
                print("✅ sequence_workbench is being added to stack")
            else:
                print("❌ sequence_workbench is NOT being added to stack")
            
            if any('codex' in log for log in stack_population_logs):
                print("✅ codex is being added to stack")
            else:
                print("❌ codex is NOT being added to stack")
            
            # Check for tab switching
            tab_switch_logs = [line for line in lines if 'Switched from' in line or 'switch' in line.lower()]
            print(f"\n📋 TAB SWITCHING LOGS ({len(tab_switch_logs)} found):")
            for log in tab_switch_logs[:5]:  # Show first 5
                print(f"  📝 {log}")
            
            # Check for initialization completion
            init_logs = [line for line in lines if 'initialized' in line.lower() or 'initialization' in line.lower()]
            print(f"\n📋 INITIALIZATION LOGS ({len(init_logs)} found):")
            for log in init_logs[-5:]:  # Show last 5
                print(f"  📝 {log}")
            
            return True
            
        else:
            # Process crashed
            stdout, stderr = process.communicate()
            print("❌ Application crashed")
            print(f"Return code: {process.returncode}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return False

def main():
    """Run debug."""
    success = debug_tab_creation()
    
    if success:
        print("\n🎯 DEBUGGING COMPLETED")
        print("Check the logs above to understand what's happening with tab creation.")
    else:
        print("\n❌ DEBUGGING FAILED")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
