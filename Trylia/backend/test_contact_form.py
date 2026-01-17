#!/usr/bin/env python3
"""
Test contact form without email dependencies
"""

import requests
import json

def test_contact_form_submission():
    """Test contact form submission with proper data"""
    
    print("🧪 Testing Contact Form Submission")
    print("=" * 50)
    
    # Test data with valid email
    test_data = {
        "companyName": "Acme Corporation",
        "websiteUrl": "https://acme.com",
        "contactPerson": "John Smith",
        "businessEmail": "john.smith@acme.com",
        "phoneNumber": "+1-555-123-4567",
        "companySize": "51-200 employees",
        "inquiryType": "Integration Request",
        "message": "We are interested in integrating Trylia's virtual try-on technology into our e-commerce platform. We have over 10,000 clothing items and serve customers globally. Please provide information about your API, pricing, and implementation timeline.",
        "meetingMode": "Google Meet",
        "meetingTime": "2024-12-15T14:00:00",
        "country": "United States"
    }
    
    try:
        print("📤 Submitting contact form...")
        response = requests.post(
            'http://localhost:5000/api/contact',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Contact form submitted successfully!")
            print(f"📧 Email sent: {data.get('emailSent', 'Unknown')}")
            print(f"📬 Confirmation sent: {data.get('confirmationSent', 'Unknown')}")
            print(f"💬 Message: {data.get('message', 'No message')}")
            return True
        else:
            print("❌ Contact form submission failed!")
            try:
                error_data = response.json()
                print(f"🚨 Error: {error_data}")
            except:
                print(f"🚨 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Backend is not running!")
        print("💡 Please start the backend first:")
        print("   cd backend")
        print("   python api_server.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🚀 Trylia Contact Form Test")
    print("=" * 30)
    
    # Test if backend is running
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend health check failed")
            return False
    except:
        print("❌ Backend is not accessible")
        return False
    
    # Test contact form
    success = test_contact_form_submission()
    
    if success:
        print("\n🎉 Contact form is working correctly!")
        print("💡 The form will work even without email configuration.")
        print("📧 To enable email sending, configure SMTP settings in .env file.")
    else:
        print("\n❌ Contact form test failed!")
    
    return success

if __name__ == "__main__":
    main()