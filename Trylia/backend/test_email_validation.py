#!/usr/bin/env python3
"""
Test email validation with different email addresses
"""

from validation_utils import ContactFormValidator

def test_email_validation():
    """Test email validation with various email addresses"""
    
    test_emails = [
        # Valid emails that should pass
        ("test@gmail.com", True),
        ("business@company.com", True),
        ("user@example.org", True),
        ("contact@test.com", True),
        # ("tripathishivam8528@gmail.com", True),
        ("admin@mydomain.net", True),
        
        # Invalid emails that should fail
        ("invalid-email", False),
        ("@gmail.com", False),
        ("test@", False),
        ("", False),
        ("test.gmail.com", False),
    ]
    
    print("🧪 Testing Email Validation")
    print("=" * 40)
    
    all_passed = True
    
    for email, should_pass in test_emails:
        is_valid, result = ContactFormValidator.validate_email(email)
        
        if is_valid == should_pass:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False
        
        print(f"{status} {email:<25} -> {is_valid}")
        if not is_valid and should_pass:
            print(f"     Error: {result}")
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All email validation tests passed!")
    else:
        print("❌ Some email validation tests failed!")
    
    return all_passed

if __name__ == "__main__":
    test_email_validation()