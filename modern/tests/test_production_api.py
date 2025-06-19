#!/usr/bin/env python3
"""
Test script for the Production API
Verifies all endpoints and service integration.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


async def test_production_api():
    """Test the production API endpoints."""
    print("🚀 Testing TKA Desktop Production API")
    print("=" * 50)

    try:
        # Import the production API (standardized import)
        from infrastructure.api.production_api import app, initialize_services

        # Initialize services
        print("📋 Initializing services...")
        initialize_services()
        print("✅ Services initialized successfully")

        # Test basic imports and service availability
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Test health endpoint
        print("\n🏥 Testing health endpoint...")
        response = client.get("/api/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"Health Status: {health_data.get('status')}")
            print(f"Services: {health_data.get('services')}")
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return False

        # Test status endpoint
        print("\n📊 Testing status endpoint...")
        response = client.get("/api/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            status_data = response.json()
            print(f"API Status: {status_data.get('status')}")
            print(f"Version: {status_data.get('version')}")
            print("✅ Status check passed")
        else:
            print("❌ Status check failed")
            return False

        # Test performance metrics endpoint
        print("\n⚡ Testing performance metrics...")
        response = client.get("/api/performance")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            perf_data = response.json()
            print(f"Performance data retrieved: {perf_data.get('success')}")
            print("✅ Performance metrics passed")
        else:
            print("❌ Performance metrics failed")
            return False

        # Test sequence creation
        print("\n📝 Testing sequence creation...")
        sequence_data = {"name": "Test Sequence", "length": 4}
        response = client.post("/api/sequences", json=sequence_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            seq_data = response.json()
            print(f"Created sequence: {seq_data.get('id')}")
            print(f"Sequence name: {seq_data.get('name')}")
            print(f"Beat count: {len(seq_data.get('beats', []))}")
            print("✅ Sequence creation passed")
        else:
            print(f"❌ Sequence creation failed: {response.text}")
            return False

        # Test command status
        print("\n🎮 Testing command status...")
        response = client.get("/api/commands/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            cmd_data = response.json()
            print(f"Command system available: {cmd_data.get('success')}")
            print(f"Can undo: {cmd_data.get('can_undo')}")
            print(f"Can redo: {cmd_data.get('can_redo')}")
            print("✅ Command status passed")
        else:
            print("❌ Command status failed")
            return False

        # Test event stats
        print("\n📡 Testing event statistics...")
        response = client.get("/api/events/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            event_data = response.json()
            print(f"Event stats retrieved: {event_data.get('success')}")
            print("✅ Event statistics passed")
        else:
            print("❌ Event statistics failed")
            return False

        print("\n🎉 All API tests passed!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure FastAPI is installed: pip install fastapi uvicorn")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_api_documentation():
    """Test API documentation generation."""
    print("\n📚 Testing API Documentation...")

    try:
        from infrastructure.api.production_api import app

        # Get OpenAPI schema
        openapi_schema = app.openapi()

        print(f"API Title: {openapi_schema.get('info', {}).get('title')}")
        print(f"API Version: {openapi_schema.get('info', {}).get('version')}")
        print(f"API Description: {openapi_schema.get('info', {}).get('description')}")

        # Count endpoints
        paths = openapi_schema.get("paths", {})
        endpoint_count = sum(len(methods) for methods in paths.values())

        print(f"Total endpoints: {endpoint_count}")
        print(f"Endpoint paths: {list(paths.keys())}")

        # Check for required endpoints
        required_endpoints = [
            "/api/health",
            "/api/status",
            "/api/performance",
            "/api/sequences",
            "/api/commands/undo",
            "/api/commands/redo",
            "/api/events/stats",
        ]

        missing_endpoints = []
        for endpoint in required_endpoints:
            if endpoint not in paths:
                missing_endpoints.append(endpoint)

        if missing_endpoints:
            print(f"❌ Missing endpoints: {missing_endpoints}")
            return False
        else:
            print("✅ All required endpoints present")
            return True

    except Exception as e:
        print(f"❌ Documentation test failed: {e}")
        return False


async def main():
    """Run all API tests."""
    print("🔧 TKA Desktop Production API Test Suite")
    print("=" * 60)

    # Test API functionality
    api_test_passed = await test_production_api()

    # Test API documentation
    doc_test_passed = test_api_documentation()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"API Functionality: {'✅ PASS' if api_test_passed else '❌ FAIL'}")
    print(f"API Documentation: {'✅ PASS' if doc_test_passed else '❌ FAIL'}")

    overall_success = api_test_passed and doc_test_passed
    print(
        f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print("\n🎉 Production API is ready for deployment!")
        print("📋 Next steps:")
        print("  1. Run with: uvicorn infrastructure.api.production_api:app --reload")
        print("  2. Access docs at: http://localhost:8000/api/docs")
        print("  3. Access health check at: http://localhost:8000/api/health")
    else:
        print("\n⚠️ API needs fixes before production deployment")

    return overall_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
