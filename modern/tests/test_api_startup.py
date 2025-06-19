#!/usr/bin/env python3
"""
Test script for API server startup with Windows permission error handling.
"""

import sys
from pathlib import Path

# Add the modern src path to import our modules
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def test_api_server_startup():
    """Test the API server startup with different scenarios."""
    print("🧪 Testing API Server Startup with Windows Permission Handling")
    print("=" * 60)

    try:
        from src.infrastructure.api.api_integration import (
            start_api_server,
            get_api_integration,
            TKAAPIIntegration,
        )

        print("\n1. Testing API server enabled with auto port finding...")
        # Test 1: Normal startup with auto port finding
        api_integration = TKAAPIIntegration(enabled=True)
        print(f"   API enabled: {api_integration.enabled}")
        print(f"   Startup failed flag: {api_integration._startup_failed}")

        print("\n2. Testing port availability check...")
        # Test 2: Check if we can test port availability
        can_bind_8000 = api_integration._test_port_availability("127.0.0.1", 8000)
        print(f"   Can bind to port 8000: {can_bind_8000}")

        print("\n3. Testing safe port finding...")
        # Test 3: Find a safe port
        safe_port = api_integration._find_safe_port("127.0.0.1", 8000)
        print(f"   Safe port found: {safe_port}")

        print("\n4. Testing API server startup...")
        # Test 4: Try to start the API server
        success = start_api_server(enabled=True, auto_port=True)
        print(f"   API server started: {success}")

        if success:
            api = get_api_integration()
            server_url = api.get_server_url()
            docs_url = api.get_docs_url()
            print(f"   Server URL: {server_url}")
            print(f"   Docs URL: {docs_url}")

            # Stop the server
            print("\n5. Stopping API server...")
            api.stop_api_server()
            print("   API server stopped")

        print("\n6. Testing disabled API server...")
        # Test 5: Test with disabled API
        disabled_integration = TKAAPIIntegration(enabled=False)
        disabled_integration.start_api_server()
        print(f"   Disabled API attempted startup (should skip)")

        print("\n✅ All tests completed successfully!")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(
            "   Make sure FastAPI and uvicorn are installed: pip install fastapi uvicorn"
        )
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_api_server_startup()
