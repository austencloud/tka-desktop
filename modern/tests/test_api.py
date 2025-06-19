#!/usr/bin/env python3
"""
Test script for TKA Desktop API.
Verifies that all API endpoints work correctly.
"""

import requests
import json
import time
import sys
from typing import Dict, Any


def test_api_endpoint(url: str, method: str = "GET", data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Test a single API endpoint."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return {
            "success": True,
            "status_code": response.status_code,
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def test_tka_api(base_url: str = "http://localhost:8000"):
    """Test all TKA API endpoints."""
    print("🧪 Testing TKA Desktop API")
    print("=" * 50)
    
    tests = [
        {
            "name": "Status Check",
            "url": f"{base_url}/api/status",
            "method": "GET",
            "expected_keys": ["status", "version", "api_enabled"]
        },
        {
            "name": "Get Current Sequence (initially empty)",
            "url": f"{base_url}/api/current-sequence",
            "method": "GET"
        },
        {
            "name": "Create New Sequence",
            "url": f"{base_url}/api/sequences",
            "method": "POST",
            "data": {
                "name": "API Test Sequence",
                "length": 4
            },
            "expected_keys": ["id", "name", "beats"]
        },
        {
            "name": "Get Current Sequence (after creation)",
            "url": f"{base_url}/api/current-sequence",
            "method": "GET",
            "expected_keys": ["id", "name", "beats"]
        },
        {
            "name": "Test Undo (mock)",
            "url": f"{base_url}/api/undo",
            "method": "POST"
        },
        {
            "name": "Test Redo (mock)",
            "url": f"{base_url}/api/redo",
            "method": "POST"
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n🔍 Testing: {test['name']}")
        print(f"   {test['method']} {test['url']}")
        
        result = test_api_endpoint(
            test['url'], 
            test['method'], 
            test.get('data')
        )
        
        if result['success']:
            print(f"   ✅ Success (HTTP {result['status_code']})")
            
            # Check expected keys if specified
            if 'expected_keys' in test and result['data']:
                missing_keys = []
                for key in test['expected_keys']:
                    if key not in result['data']:
                        missing_keys.append(key)
                
                if missing_keys:
                    print(f"   ⚠️  Missing expected keys: {missing_keys}")
                else:
                    print(f"   ✅ All expected keys present")
            
            # Pretty print response data
            if result['data']:
                print(f"   📄 Response: {json.dumps(result['data'], indent=2)}")
        else:
            print(f"   ❌ Failed: {result['error']}")
            if result.get('status_code'):
                print(f"   HTTP {result['status_code']}")
        
        results.append({
            "test": test['name'],
            "success": result['success'],
            "details": result
        })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        for result in results:
            if not result['success']:
                print(f"   - {result['test']}: {result['details'].get('error', 'Unknown error')}")
        return False


def check_api_server_running(base_url: str = "http://localhost:8000") -> bool:
    """Check if the API server is running."""
    try:
        response = requests.get(f"{base_url}/api/status", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    """Main test function."""
    base_url = "http://localhost:8000"
    
    print("🚀 TKA Desktop API Test Suite")
    print("=" * 50)
    
    # Check if server is running
    print("🔍 Checking if API server is running...")
    if not check_api_server_running(base_url):
        print("❌ API server is not running!")
        print("   Please start TKA Desktop with API enabled")
        print("   Or run: python main.py")
        sys.exit(1)
    
    print("✅ API server is running")
    
    # Wait a moment for server to be fully ready
    time.sleep(1)
    
    # Run tests
    success = test_tka_api(base_url)
    
    if success:
        print("\n🎉 All API tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some API tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
