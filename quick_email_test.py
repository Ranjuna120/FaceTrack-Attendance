#!/usr/bin/env python3
"""
Quick Email Test Script
"""
from email_notifier import EmailNotifier
from simple_advanced_attendance import SimpleAdvancedAttendanceManager
import pandas as pd
from datetime import datetime

def quick_email_test():
    print("📧 Email Notifications Quick Test")
    print("=" * 40)
    
    # Initialize email notifier
    email_notifier = EmailNotifier()
    
    # Get email configuration
    sender_email = input("Enter your email: ")
    sender_password = input("Enter your app password: ")
    recipient_email = input("Enter recipient email: ")
    
    # Configure email
    try:
        email_notifier.configure(sender_email, sender_password)
        print("✅ Email configured successfully!")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return
    
    # Send test email
    try:
        # Create sample attendance data
        attendance_data = pd.DataFrame([
            {"Name": "Test User", "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            {"Name": "Sample Person", "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ])
        
        success, message = email_notifier.send_daily_report(recipient_email, attendance_data)
        
        if success:
            print("✅ Test email sent successfully!")
            print(f"Message: {message}")
        else:
            print(f"❌ Failed to send email: {message}")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")

if __name__ == "__main__":
    quick_email_test()
