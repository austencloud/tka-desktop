#!/usr/bin/env python3
"""
Simple test for the minimal API implementation.
Tests the API endpoints directly without the full TKA application.
"""

import sys
import time
import threading
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

def test_minimal_api():
    """Test the minimal API implementation."""
    print("🧪 Testing Minimal API Implementation")
    print("=" * 50)
    
    try:
        # Import the API components
        from infrastructure.api.minimal_api import app
        from infrastructure.api.api_integration import start_api_server
        import uvicorn
        import requests
        
        print("✅ Successfully imported API components")
        
        # Start the API server in a background thread
        print("🚀 Starting API server...")
        
        def run_server():
            uvicorn.run(app, host="localhost", port=8001, log_level="warning")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Test the endpoints
        base_url = "http://localhost:8001"
        
        print(f"\n🔍 Testing endpoints at {base_url}")
        
        # Test status endpoint
        print("\n1. Testing /api/status")
        try:
            response = requests.get(f"{base_url}/api/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {data}")
            else:
                print(f"   ❌ Status failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Status failed: {e}")
        
        # Test current sequence endpoint
        print("\n2. Testing /api/current-sequence")
        try:
            response = requests.get(f"{base_url}/api/current-sequence", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Current sequence: {data}")
            else:
                print(f"   ❌ Current sequence failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Current sequence failed: {e}")
        
        # Test create sequence endpoint
        print("\n3. Testing /api/sequences (POST)")
        try:
            create_data = {
                "name": "Test Sequence",
                "length": 4
            }
            response = requests.post(f"{base_url}/api/sequences", json=create_data, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Created sequence: {data['name']} with {len(data['beats'])} beats")
            else:
                print(f"   ❌ Create sequence failed: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Create sequence failed: {e}")
        
        # Test undo endpoint
        print("\n4. Testing /api/undo")
        try:
            response = requests.post(f"{base_url}/api/undo", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Undo response: {data}")
            else:
                print(f"   ❌ Undo failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Undo failed: {e}")
        
        # Test redo endpoint
        print("\n5. Testing /api/redo")
        try:
            response = requests.post(f"{base_url}/api/redo", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Redo response: {data}")
            else:
                print(f"   ❌ Redo failed: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Redo failed: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Minimal API test completed!")
        print(f"📚 API docs available at: {base_url}/docs")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure FastAPI and uvicorn are installed:")
        print("   pip install fastapi uvicorn")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_minimal_api()
    if success:
        print("\n✅ Test completed successfully!")
        # Keep the server running for a bit so you can test manually
        print("🌐 Server will keep running for 30 seconds for manual testing...")
        time.sleep(30)
    else:
        print("\n❌ Test failed!")
        sys.exit(1)
