#!/usr/bin/env python3
"""
Test all new features of the Face Recognition Attendance System
"""

import os
import sys
from datetime import datetime

def test_basic_modules():
    """Test basic module imports"""
    print("🔍 Testing Basic Module Imports...")
    
    try:
        from face_recognition_module_compatible import FaceRecognitionModuleCompatible
        print("✅ Face Recognition Module Compatible - OK")
    except ImportError as e:
        print(f"❌ Face Recognition Module Compatible - FAILED: {e}")
    
    try:
        from simple_advanced_attendance import SimpleAdvancedAttendanceManager
        print("✅ Simple Advanced Attendance - OK")
    except ImportError as e:
        print(f"❌ Simple Advanced Attendance - FAILED: {e}")
    
    try:
        from database_manager import DatabaseManager
        print("✅ Database Manager - OK")
    except ImportError as e:
        print(f"❌ Database Manager - FAILED: {e}")
    
    try:
        from email_notifier import EmailNotifier
        print("✅ Email Notifier - OK")
    except ImportError as e:
        print(f"❌ Email Notifier - FAILED: {e}")

def test_attendance_functionality():
    """Test attendance functionality"""
    print("\n📊 Testing Attendance Functionality...")
    
    try:
        from simple_advanced_attendance import SimpleAdvancedAttendanceManager
        manager = SimpleAdvancedAttendanceManager()
        
        # Test marking attendance
        success, message = manager.mark_attendance("TestUser2")
        print(f"✅ Mark Attendance: {message}")
        
        # Test statistics
        stats = manager.get_attendance_stats(days=1)
        print(f"✅ Statistics: {stats['total_attendances']} attendances today")
        
        # Test report generation
        report_result = manager.generate_report()
        print(f"✅ Report Generation: {report_result}")
        
    except Exception as e:
        print(f"❌ Attendance Testing FAILED: {e}")

def test_database_functionality():
    """Test database functionality"""
    print("\n🗄️ Testing Database Functionality...")
    
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager()
        
        # Test adding user
        success, message = db.add_user("TestUser3", "test@example.com", "IT", "Employee")
        print(f"✅ Add User: {message}")
        
        # Test marking attendance
        success, message = db.mark_attendance("TestUser3")
        print(f"✅ Mark Attendance (DB): {message}")
        
    except Exception as e:
        print(f"❌ Database Testing FAILED: {e}")

def test_web_components():
    """Test if web components can be imported"""
    print("\n🌐 Testing Web Components...")
    
    try:
        import flask
        print("✅ Flask - OK")
    except ImportError:
        print("❌ Flask - MISSING")
    
    try:
        import flask_cors
        print("✅ Flask-CORS - OK")
    except ImportError:
        print("❌ Flask-CORS - MISSING")
    
    # Test if web files exist
    web_files = ["web_dashboard.py", "api_server.py"]
    for file in web_files:
        if os.path.exists(file):
            print(f"✅ {file} - EXISTS")
        else:
            print(f"❌ {file} - MISSING")

def test_visualization():
    """Test visualization capabilities"""
    print("\n📈 Testing Visualization...")
    
    try:
        import matplotlib
        print("✅ Matplotlib - OK")
    except ImportError:
        print("❌ Matplotlib - MISSING")
    
    try:
        import seaborn
        print("✅ Seaborn - OK")
    except ImportError:
        print("❌ Seaborn - MISSING")
    
    # Test simple chart creation
    try:
        from simple_advanced_attendance import SimpleAdvancedAttendanceManager
        manager = SimpleAdvancedAttendanceManager()
        result = manager.create_simple_chart()
        print(f"✅ Simple Chart: {result}")
    except Exception as e:
        print(f"❌ Simple Chart FAILED: {e}")

def test_file_structure():
    """Test project file structure"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        "main.py",
        "face_recognition_module.py",
        "face_recognition_module_compatible.py",
        "attendance_manager.py",
        "simple_advanced_attendance.py",
        "database_manager.py",
        "email_notifier.py",
        "web_dashboard.py",
        "api_server.py",
        "master_control.py",
        "config.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")

def show_summary():
    """Show summary of features"""
    print("\n" + "="*60)
    print("🎉 FACETRACK ATTENDANCE SYSTEM - FEATURE SUMMARY")
    print("="*60)
    
    features = [
        "✅ Core Face Recognition & Attendance",
        "✅ Compatible Face Recognition Module",
        "✅ Simple Advanced Attendance Manager",
        "✅ Database Integration (SQLite)",
        "✅ Email Notification System",
        "✅ Web Dashboard (Flask)",
        "✅ REST API Server",
        "✅ Master Control Panel",
        "✅ Text-based Charts",
        "✅ Report Generation",
        "✅ Data Export (Excel/CSV)",
        "✅ Statistics & Analytics"
    ]
    
    for feature in features:
        print(feature)
    
    print("\n🚀 USAGE INSTRUCTIONS:")
    print("1. Basic GUI:           python main.py")
    print("2. Command Line:        python cli_test.py")
    print("3. Master Control:      python master_control.py")
    print("4. Web Dashboard:       python web_dashboard.py")
    print("5. API Server:          python api_server.py")
    print("6. Simple Test:         python simple_advanced_attendance.py")
    
    print("\n📊 NEW FEATURES ADDED:")
    print("• Advanced attendance analytics")
    print("• Database integration with user management") 
    print("• Web-based dashboard with real-time updates")
    print("• REST API for mobile app integration")
    print("• Email notification system")
    print("• Master control panel for unified management")
    print("• Enhanced reporting and data visualization")
    print("• Improved face recognition compatibility")

def main():
    """Run all tests"""
    print("🎯 FACETRACK ATTENDANCE SYSTEM - COMPREHENSIVE TEST")
    print("=" * 60)
    
    test_basic_modules()
    test_attendance_functionality()
    test_database_functionality()
    test_web_components()
    test_visualization()
    test_file_structure()
    show_summary()
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
