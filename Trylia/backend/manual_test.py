#!/usr/bin/env python3
"""
Manual test script to verify backend endpoints
"""

import requests
import json
import sys

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Backend is not running!")
        return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_contact_options_endpoint():
    """Test the contact options endpoint"""
    print("\n🔍 Testing /api/contact/options endpoint...")
    try:
        response = requests.get('http://localhost:5000/api/contact/options', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Contact options endpoint working!")
            print(f"   Company sizes: {len(data['options']['companySizes'])} options")
            print(f"   Inquiry types: {len(data['options']['inquiryTypes'])} options")
            print(f"   Countries: {len(data['options']['countries'])} options")
            return True
        else:
            print(f"❌ Contact options endpoint failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Backend is not running!")
        return False
    except Exception as e:
        print(f"❌ Contact options endpoint error: {e}")
        return False

def test_contact_submit_endpoint():
    """Test the contact submit endpoint with sample data"""
    print("\n🔍 Testing /api/contact endpoint...")
    
    sample_data = {
        "companyName": "Test Company",
        "websiteUrl": "https://example.com",
        "contactPerson": "John Doe",
        "businessEmail": "test@gmail.com",
        "phoneNumber": "+1234567890",
        "companySize": "1-10 employees",
        "inquiryType": "Demo Request",
        "message": "This is a test message for the contact form.",
        "meetingMode": "Google Meet",
        "country": "United States"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/contact',
            json=sample_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Contact submit endpoint working!")
            data = response.json()
            print(f"   Response: {data['message']}")
            return True
        else:
            print(f"❌ Contact submit endpoint failed with status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Backend is not running!")
        return False
    except Exception as e:
        print(f"❌ Contact submit endpoint error: {e}")
        return False

def main():
    print("🧪 Trylia Backend Manual Test")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n❌ Backend is not running or not accessible.")
        print("💡 Please start the backend first:")
        print("   cd backend")
        print("   start_backend_fixed.bat")
        return False
    
    # Test contact options endpoint
    if not test_contact_options_endpoint():
        print("\n❌ Contact options endpoint failed.")
        return False
    
    # Test contact submit endpoint
    if not test_contact_submit_endpoint():
        print("\n❌ Contact submit endpoint failed.")
        return False
    
    print("\n🎉 All backend endpoints are working correctly!")
    print("\n📋 Your backend is ready for the frontend to connect.")
    print("💡 You can now start the React frontend and test the contact form.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)