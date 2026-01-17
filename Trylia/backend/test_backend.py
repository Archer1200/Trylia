#!/usr/bin/env python3
"""
Quick test script to check if backend can start
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"❌ Flask-CORS import failed: {e}")
        return False
    
    try:
        import email_validator
        print("✅ email_validator imported successfully")
    except ImportError as e:
        print(f"❌ email_validator import failed: {e}")
        print("💡 Run: pip install email-validator==2.1.0")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"⚠️  python-dotenv import failed: {e}")
        print("💡 Run: pip install python-dotenv==1.0.0")
        print("📝 This is optional, but recommended")
    
    return True

def test_local_imports():
    """Test if local modules can be imported"""
    print("\n🔍 Testing local imports...")
    
    try:
        from email_service import email_service
        print("✅ email_service imported successfully")
    except ImportError as e:
        print(f"❌ email_service import failed: {e}")
        return False
    
    try:
        from validation_utils import ContactFormValidator
        print("✅ validation_utils imported successfully")
    except ImportError as e:
        print(f"❌ validation_utils import failed: {e}")
        return False
    
    return True

def test_flask_app():
    """Test if Flask app can be created"""
    print("\n🔍 Testing Flask app creation...")
    
    try:
        from flask import Flask
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        @app.route('/test')
        def test():
            return {'status': 'ok'}
        
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    print("🚀 Trylia Backend Test Script")
    print("=" * 50)
    
    # Test basic imports
    if not test_imports():
        print("\n❌ Basic imports failed. Please install missing packages.")
        return False
    
    # Test local imports
    if not test_local_imports():
        print("\n❌ Local imports failed. Check file locations.")
        return False
    
    # Test Flask app
    if not test_flask_app():
        print("\n❌ Flask app test failed.")
        return False
    
    print("\n🎉 All tests passed! Backend should start successfully.")
    print("\n📋 Next steps:")
    print("1. Run: python api_server.py")
    print("2. Check: http://localhost:5000/health")
    print("3. Test: http://localhost:5000/api/contact/options")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)