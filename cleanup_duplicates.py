#!/usr/bin/env python3
"""
Remove duplicate and unnecessary files from FaceTrack-Attendance project
"""

import os
import shutil

def cleanup_duplicate_files():
    """Remove duplicate and unnecessary files"""
    
    # Files to remove (duplicates or obsolete)
    files_to_remove = [
        # Duplicate utilities
        "utils.py",  # Keep utils_enhanced.py instead
        
        # Duplicate test files
        "test_fixes.py",  # Keep test_all_features.py (more comprehensive)
        "test_compatible.py",  # Keep test_all_features.py
        
        # Duplicate attendance managers
        "advanced_attendance.py",  # Keep simple_advanced_attendance.py (more complete)
        
        # Unnecessary launcher
        "advanced_launcher.py",  # Keep master_control.py (more comprehensive)
        
        # Unnecessary web starter
        "start_web_dashboard.py",  # Can run web_dashboard.py directly
        
        # Debug file (not needed in production)
        "debug_face_recognition.py",
        
        # CLI test (basic functionality covered in other files)
        "cli_test.py",
        
        # Backup/temp files
        "GITHUB_ABOUT_DESCRIPTION.md"  # Was undone by user
    ]
    
    # Directories that might have temp files
    temp_dirs = ["__pycache__", ".qodo"]
    
    print("🧹 Cleaning up duplicate and unnecessary files...")
    print("=" * 50)
    
    removed_count = 0
    
    # Remove duplicate files
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file}: {e}")
        else:
            print(f"⚪ Not found: {file}")
    
    # Remove temp directories
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"✅ Removed directory: {temp_dir}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {temp_dir}: {e}")
    
    print("=" * 50)
    print(f"🎉 Cleanup complete! Removed {removed_count} items.")
    
    # Show remaining core files
    print("\n📂 Core files remaining:")
    core_files = [
        "main.py",
        "face_recognition_module.py", 
        "face_recognition_module_compatible.py",
        "attendance_manager.py",
        "simple_advanced_attendance.py",
        "database_manager.py",
        "web_dashboard.py",
        "api_server.py",
        "email_notifier.py",
        "email_config_gui.py",
        "master_control.py",
        "utils_enhanced.py",
        "test_all_features.py",
        "config.py",
        "logger.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file in core_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing: {file}")
    
    print("\n🎯 Recommended file structure after cleanup:")
    print("""
    📁 FaceTrack-Attendance/
    ├── 🎯 Core Application
    │   ├── main.py                          # Basic GUI
    │   ├── master_control.py                # Advanced control panel
    │   └── config.py                        # Configuration
    │
    ├── 🤖 Face Recognition
    │   ├── face_recognition_module.py       # Original module
    │   └── face_recognition_module_compatible.py  # Enhanced version
    │
    ├── 📊 Attendance Management
    │   ├── attendance_manager.py            # Basic attendance
    │   ├── simple_advanced_attendance.py    # Advanced features
    │   └── database_manager.py              # Database operations
    │
    ├── 🌐 Web & API
    │   ├── web_dashboard.py                 # Web interface
    │   └── api_server.py                    # REST API
    │
    ├── 📧 Notifications
    │   ├── email_notifier.py                # Email system
    │   └── email_config_gui.py              # Email GUI
    │
    ├── 🔧 Utilities
    │   ├── utils_enhanced.py                # Utility functions
    │   ├── logger.py                        # Logging
    │   └── test_all_features.py             # Testing
    │
    └── 📁 Data & Config
        ├── data/                            # Database & files
        ├── templates/                       # Web templates
        ├── requirements.txt                 # Dependencies
        └── README.md                        # Documentation
    """)

if __name__ == "__main__":
    # Ask for confirmation
    response = input("🤔 Do you want to remove duplicate files? (y/N): ").lower()
    if response in ['y', 'yes']:
        cleanup_duplicate_files()
    else:
        print("❌ Cleanup cancelled.")
