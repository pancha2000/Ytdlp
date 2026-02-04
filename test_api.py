#!/usr/bin/env python3
"""
YouTube API Test Script
API එක හරියටද වැඩ කරන්නේ කියලා test කරන්න
"""

import requests
import json
import time

# API base URL (local or deployed)
BASE_URL = "http://localhost:8000"

# Test video URL
TEST_VIDEO = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test health endpoint"""
    print_section("Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    try:
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_video_info():
    """Test video info endpoint"""
    print_section("Testing Video Info Endpoint")
    try:
        response = requests.get(
            f"{BASE_URL}/api/info",
            params={"url": TEST_VIDEO},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_best():
    """Test download with best quality"""
    print_section("Testing Download - Best Quality")
    try:
        response = requests.get(
            f"{BASE_URL}/api/download",
            params={"url": TEST_VIDEO, "quality": "best"},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('download_url'):
            print(f"✅ Download URL received")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_audio():
    """Test download with audio only"""
    print_section("Testing Download - Audio Only")
    try:
        response = requests.get(
            f"{BASE_URL}/api/download",
            params={"url": TEST_VIDEO, "quality": "audio"},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('download_url'):
            print(f"✅ Audio download URL received")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_url():
    """Test with invalid URL"""
    print_section("Testing Invalid URL Handling")
    try:
        response = requests.get(
            f"{BASE_URL}/api/download",
            params={"url": "https://invalid-url.com"},
            headers={"User-Agent": "Mozilla/5.0"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Should return 400 for invalid URL
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_bot_detection():
    """Test bot detection"""
    print_section("Testing Bot Detection")
    try:
        # Send request without user-agent (should be detected as bot)
        response = requests.get(
            f"{BASE_URL}/api/download",
            params={"url": TEST_VIDEO}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Should return 403 for bot request
        if response.status_code == 403:
            print(f"✅ Bot detection working")
            return True
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_rate_limit():
    """Test rate limiting"""
    print_section("Testing Rate Limiting")
    try:
        print("Sending 7 rapid requests (limit is 5 per minute)...")
        results = []
        
        for i in range(7):
            response = requests.get(
                f"{BASE_URL}/api/download",
                params={"url": TEST_VIDEO, "quality": "audio"},
                headers={"User-Agent": "Mozilla/5.0"}
            )
            results.append(response.status_code)
            print(f"Request {i+1}: Status {response.status_code}")
            time.sleep(0.5)
        
        # Should have at least one 429 (rate limit) response
        if 429 in results:
            print(f"✅ Rate limiting working")
            return True
        else:
            print(f"⚠️  No rate limit hit (might need adjustment)")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  YouTube Download API - Test Suite")
    print("="*60)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Video Info", test_video_info),
        ("Download Best", test_download_best),
        ("Download Audio", test_download_audio),
        ("Invalid URL", test_invalid_url),
        ("Bot Detection", test_bot_detection),
        ("Rate Limiting", test_rate_limit),
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"❌ {name} failed with exception: {e}")
            results[name] = False
        time.sleep(1)  # Wait between tests
    
    # Print summary
    print_section("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    import sys
    
    # Check if custom URL provided
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
        print(f"Using custom API URL: {BASE_URL}")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
