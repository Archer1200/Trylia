#!/usr/bin/env python3
"""
View contact form submissions from server logs
"""

import os
import re
from datetime import datetime

def parse_log_file():
    """Parse the API server log file for contact form submissions"""
    
    log_file = "api_server.log"
    
    if not os.path.exists(log_file):
        print("❌ No log file found. Make sure the backend server has been running.")
        return
    
    print("📋 Contact Form Submissions from Server Logs")
    print("=" * 60)
    
    submissions = []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            # Look for contact form submissions
            if "Received contact form submission from" in line:
                # Extract timestamp and company name
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - INFO - Received contact form submission from (.+)', line)
                if match:
                    timestamp = match.group(1)
                    company = match.group(2)
                    submissions.append((timestamp, company))
        
        if submissions:
            print(f"📊 Found {len(submissions)} contact form submissions:\n")
            
            for i, (timestamp, company) in enumerate(submissions, 1):
                print(f"{i}. 🏢 {company}")
                print(f"   📅 {timestamp}")
                print()
        else:
            print("📭 No contact form submissions found in logs.")
            print("💡 Submit a test form to see it appear here.")
    
    except Exception as e:
        print(f"❌ Error reading log file: {e}")

def show_recent_activity():
    """Show recent server activity"""
    
    log_file = "api_server.log"
    
    if not os.path.exists(log_file):
        print("❌ No log file found.")
        return
    
    print("\n📈 Recent Server Activity")
    print("=" * 30)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Get last 10 lines
        recent_lines = lines[-10:]
        
        for line in recent_lines:
            if any(keyword in line for keyword in ['contact', 'POST', 'GET']):
                # Clean up the line for display
                clean_line = line.strip()
                if 'contact' in clean_line.lower():
                    print(f"📧 {clean_line}")
                elif 'POST' in clean_line:
                    print(f"📤 {clean_line}")
                elif 'GET' in clean_line:
                    print(f"📥 {clean_line}")
    
    except Exception as e:
        print(f"❌ Error reading recent activity: {e}")

def main():
    print("🔍 Trylia Contact Form Submission Viewer")
    print("=" * 45)
    print()
    
    # Parse submissions
    parse_log_file()
    
    # Show recent activity
    show_recent_activity()
    
    print("\n💡 Tips:")
    print("   - All form submissions are logged even without email setup")
    print("   - Check this script after each form submission")
    print("   - Configure email to get notifications automatically")
    print()
    print("📧 To setup email notifications: run setup_email.bat")

if __name__ == "__main__":
    main()